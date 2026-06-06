import json, pymysql, os

data_dir = r'D:\桌面\毕设\exam-platform\data'
conn = pymysql.connect(host='localhost', user='root', password='123456', database='exam_platform', charset='utf8mb4')
cur = conn.cursor()

with open(os.path.join(data_dir, 'all_comp_q.json'), 'r', encoding='utf-8') as f:
    comp_qs = json.load(f)

print(f'Total comprehensive questions: {len(comp_qs)}')

# Comp question subject mapping
# s field values: 10=DS, 20=CO, 30=OS, 40=CN  
# ch field: chapter code like 101, 201, 301, 401 etc.

imported = 0
skipped = 0
for cq in comp_qs:
    year = cq.get('y')
    content = cq.get('c', '')
    answer = cq.get('a', '')
    s = int(cq.get('s', 10))
    ch = int(cq.get('ch', 101))
    
    if not year or not content:
        skipped += 1
        continue
    
    # Check if already exists
    cur.execute("SELECT id FROM question WHERE year=%s AND type='COMPREHENSIVE' AND content LIKE %s LIMIT 1",
                (year, f'%{content[:30]}%'))
    if cur.fetchone():
        skipped += 1
        continue
    
    cur.execute("""
        INSERT INTO question (chapter_id, subject_id, type, difficulty, content, answer, year)
        VALUES (%s, %s, 'COMPREHENSIVE', 'MEDIUM', %s, %s, %s)
    """, (ch, s, content, answer, year))
    imported += 1

conn.commit()

# Now link comprehensive questions to papers
link_count = 0
cur.execute("SELECT id, year FROM question WHERE type='COMPREHENSIVE'")
for row in cur.fetchall():
    qid, year = row
    cur.execute("SELECT id FROM exam_paper WHERE year=%s", (year,))
    paper = cur.fetchone()
    if paper:
        cur.execute("INSERT IGNORE INTO paper_question (paper_id, question_id, sort_order) VALUES (%s, %s, 0)",
                    (paper[0], qid))
        link_count += 1

conn.commit()

print(f'Imported: {imported}')
print(f'Skipped: {skipped}')
print(f'Comp paper links: {link_count}')

# Verify counts
cur.execute("SELECT type, COUNT(*) FROM question GROUP BY type")
for row in cur.fetchall():
    print(f'  {row[0]}: {row[1]}')

cur.execute("SELECT COUNT(*) FROM paper_question")
print(f'Total paper_question links: {cur.fetchone()[0]}')

cur.close()
conn.close()
print('Done!')
