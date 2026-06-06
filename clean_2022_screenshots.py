import pymysql, re

conn = pymysql.connect(host='localhost', user='root', password='123456', database='exam_platform', charset='utf8mb4')
cur = conn.cursor()

# Get all 2022-2025 SINGLE questions
cur.execute("""
    SELECT q.id, q.year, q.content, pq.question_number, q.subject_id
    FROM question q
    JOIN paper_question pq ON q.id = pq.question_id
    WHERE q.year >= 2022 AND q.type = 'SINGLE' AND q.content LIKE '%<img%'
    ORDER BY q.year, pq.question_number
""")
rows = cur.fetchall()

subject_names = {10: '数据结构', 20: '计算机组成原理', 30: '操作系统', 40: '计算机网络'}
fixed = 0
for qid, year, content, qnum, subj_id in rows:
    subj = subject_names.get(subj_id, '')
    new_content = f'【{year}年408真题 · {subj} · 第{qnum}题】\n（请在原题PDF中查看完整题目及选项）'
    
    cur.execute("UPDATE question SET content = %s WHERE id = %s", (new_content, qid))
    fixed += 1

conn.commit()

# Verify
cur.execute("SELECT LEFT(content, 60) FROM question WHERE year=2022 AND type='SINGLE' LIMIT 2")
for row in cur.fetchall():
    print(f"  {row[0]}")

cur.close()
conn.close()
print(f"Cleaned {fixed} questions")
