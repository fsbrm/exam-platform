import pymysql, re, json

conn = pymysql.connect(host='localhost', user='root', password='123456', database='exam_platform', charset='utf8mb4')
cur = conn.cursor()

# =============================================
# 1. Link questions to knowledge points
# =============================================
print("=== Linking questions to knowledge points ===")

# Get all knowledge points grouped by chapter
cur.execute("SELECT id, chapter_id FROM knowledge_point")
kp_by_chapter = {}
for row in cur.fetchall():
    kpid, chid = row
    kp_by_chapter.setdefault(chid, []).append(kpid)

# Get all questions with their chapter_id
cur.execute("SELECT id, chapter_id FROM question")
q_by_chapter = {}
for row in cur.fetchall():
    qid, chid = row
    q_by_chapter.setdefault(chid, []).append(qid)

# Insert question_knowledge links
inserted = 0
for chid, qids in q_by_chapter.items():
    kpids = kp_by_chapter.get(chid, [])
    if not kpids:
        continue
    for qid in qids:
        for kpid in kpids:
            try:
                cur.execute("INSERT IGNORE INTO question_knowledge (question_id, knowledge_point_id) VALUES (%s, %s)", (qid, kpid))
                inserted += 1
            except:
                pass

conn.commit()
print(f"Created {inserted} question-knowledge links")

# =============================================
# 2. Fix 2022-2025 content - add question info text
# =============================================
print("\n=== Fixing 2022-2025 question content ===")

# For 2022-2025 SINGLE questions: if content is ONLY an img tag, add contextual text
cur.execute("""
    SELECT q.id, q.year, q.content, q.subject_id, q.chapter_id, 
           pq.question_number
    FROM question q
    LEFT JOIN paper_question pq ON q.id = pq.question_id
    WHERE q.year >= 2022 AND q.type = 'SINGLE'
""")
rows = cur.fetchall()

subject_names = {10: '数据结构', 20: '计算机组成原理', 30: '操作系统', 40: '计算机网络'}
chapter_names = {}
cur.execute("SELECT id, name FROM chapter")
for row in cur.fetchall():
    chapter_names[row[0]] = row[1]

fixed_content = 0
for qid, year, content, subj_id, ch_id, qnum in rows:
    # If content is just an img tag (or starts with img), clean it up
    if not content or '<img' in (content or ''):
        # Build meaningful info
        subj_name = subject_names.get(subj_id, '')
        ch_name = chapter_names.get(ch_id, '')
        num_text = f'第{qnum}题' if qnum else ''
        
        # Keep the img but add text above it
        img_match = re.search(r'<img[^>]+>', content or '')
        img_tag = img_match.group(0) if img_match else ''
        
        # New content: text description + image
        parts = []
        if num_text:
            parts.append(f'<strong>{year}年408真题 · {subj_name} · {ch_name} · {num_text}</strong>')
        else:
            parts.append(f'<strong>{year}年408真题 · {subj_name} · {ch_name}</strong>')
        if img_tag:
            parts.append(img_tag)
        
        new_content = '<br/>'.join(parts)
        cur.execute("UPDATE question SET content = %s WHERE id = %s", (new_content, qid))
        fixed_content += 1

conn.commit()
print(f"Fixed {fixed_content} questions")

# =============================================
# 3. Fix cellClick tooltip - strip HTML
# =============================================
# This is a frontend fix - the PapersPage tooltip shows raw HTML
# We'll fix the cellClick function in the Vue file

# =============================================
# 4. Verify
cur.execute("SELECT COUNT(*) FROM question_knowledge")
print(f"\nquestion_knowledge rows: {cur.fetchone()[0]}")

cur.execute("SELECT id, year, LEFT(content, 80) FROM question WHERE year=2022 AND type='SINGLE' LIMIT 2")
for row in cur.fetchall():
    print(f"  [{row[0]}] {row[1]}: {row[2]}")

cur.close()
conn.close()
print("\nDone!")
