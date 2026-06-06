import json, pymysql

conn = pymysql.connect(host='localhost', user='root', password='123456', database='exam_platform', charset='utf8mb4')
cursor = conn.cursor()

# Delete existing comprehensive questions and their knowledge links
cursor.execute("DELETE FROM question_knowledge WHERE question_id IN (SELECT id FROM question WHERE type='COMPREHENSIVE')")
cursor.execute("DELETE FROM question WHERE type='COMPREHENSIVE'")
print("Cleared existing comprehensive questions")

with open(r'D:\桌面\毕设\exam-platform\data\all_comp_q.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

count = 0
for q in questions:
    y, c, a, ch, s = q['y'], q['c'], q['a'], q['ch'], q['s']
    cursor.execute('SELECT id FROM knowledge_point WHERE chapter_id=%s LIMIT 1', (ch,))
    kp = cursor.fetchone()
    kp_id = kp[0] if kp else None
    cursor.execute(
        'INSERT INTO question (chapter_id, subject_id, type, difficulty, content, answer, year) VALUES (%s,%s,%s,%s,%s,%s,%s)',
        (ch, s, 'COMPREHENSIVE', 'MEDIUM', c, a, y)
    )
    qid = cursor.lastrowid
    if kp_id:
        cursor.execute('INSERT INTO question_knowledge (question_id, knowledge_id) VALUES (%s,%s)', (qid, kp_id))
    count += 1
    if count % 20 == 0:
        print(f'Inserted {count} questions...')

conn.commit()
print(f'Total inserted: {count} comprehensive questions')
cursor.close()
conn.close()