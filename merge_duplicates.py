import pymysql, re

conn = pymysql.connect(host='localhost', user='root', password='123456', database='exam_platform', charset='utf8mb4')
cur = conn.cursor()

# For each paper, find duplicate question_numbers and merge COMPREHENSIVE+MULTI
cur.execute("SELECT id, year FROM exam_paper ORDER BY year")
papers = cur.fetchall()

merged = 0
for paper_id, year in papers:
    # Find duplicate question numbers
    cur.execute("""
        SELECT pq.question_number, q.id, q.type, q.content, q.answer, q.analysis
        FROM paper_question pq JOIN question q ON pq.question_id = q.id
        WHERE pq.paper_id = %s AND pq.question_number >= 41
        ORDER BY pq.question_number, FIELD(q.type, 'MULTI', 'COMPREHENSIVE')
    """, (paper_id,))
    
    rows = cur.fetchall()
    
    # Group by question_number
    from collections import defaultdict
    by_num = defaultdict(list)
    for qnum, qid, qtype, content, answer, analysis in rows:
        by_num[qnum].append((qid, qtype, content, answer, analysis))
    
    for qnum, entries in by_num.items():
        if len(entries) < 2:
            continue
        
        # Find COMPREHENSIVE (has img) and MULTI (has text)
        comp = None
        multi = None
        for qid, qtype, content, answer, analysis in entries:
            if qtype == 'COMPREHENSIVE':
                comp = (qid, content, answer, analysis)
            elif qtype == 'MULTI':
                multi = (qid, content, answer, analysis)
        
        if comp and multi:
            # Merge: Use COMPREHENSIVE's screenshot + MULTI's answer/analysis
            comp_content = comp[1] or ''
            multi_content = multi[1] or ''
            multi_answer = multi[2] or ''
            multi_analysis = multi[3] or ''
            
            # Build merged content
            if comp_content and '<img' in comp_content:
                # Extract img from COMPREHENSIVE
                img_match = re.search(r'<img[^>]+>', comp_content)
                img_tag = img_match.group(0) if img_match else ''
                # Remove leading <br/> from multi_content
                text_content = re.sub(r'^<br\s*/?>', '', multi_content).strip()
                merged_content = f'{img_tag}<br/>{text_content}' if text_content else comp_content
            else:
                merged_content = comp_content
            
            # Update COMPREHENSIVE with merged content and MULTI's answer
            cur.execute("""
                UPDATE question SET content = %s, answer = %s, analysis = %s
                WHERE id = %s
            """, (merged_content, multi_answer or comp[2], multi_analysis or comp[3], comp[0]))
            
            # Remove MULTI from paper_question
            cur.execute("DELETE FROM paper_question WHERE question_id = %s AND paper_id = %s", (multi[0], paper_id))
            
            merged += 1
            print(f"  {year} Q{qnum}: merged (COMP={comp[0]}, MULTI={multi[0]})")

conn.commit()
print(f"Merged {merged} duplicates")

# Clean up: remove orphaned MULTI questions (no longer in any paper)
cur.execute("""
    SELECT q.id FROM question q 
    WHERE q.type = 'MULTI' AND q.id NOT IN (SELECT question_id FROM paper_question)
""")
orphans = cur.fetchall()
for (qid,) in orphans:
    cur.execute("DELETE FROM question WHERE id = %s", (qid,))
    cur.execute("DELETE FROM question_knowledge WHERE question_id = %s", (qid,))
conn.commit()
print(f"Removed {len(orphans)} orphaned MULTI questions")

cur.execute("SELECT COUNT(*) FROM question")
print(f"Total questions: {cur.fetchone()[0]}")

cur.close()
conn.close()
