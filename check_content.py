import json, pymysql

# Check actual DB content for a single choice question
conn = pymysql.connect(host='localhost', user='root', password='123456', database='exam_platform', charset='utf8mb4')
cur = conn.cursor()

cur.execute("SELECT id, year, type, content FROM question WHERE year=2009 AND type='SINGLE' LIMIT 3")
for row in cur.fetchall():
    print(f'ID={row[0]} year={row[1]} type={row[2]}')
    print(f'  Content: {row[3][:200]}')
    print()

# Check questions_raw.json text
with open(r'D:\桌面\毕设\exam-platform\data\questions_raw.json', 'r', encoding='utf-8') as f:
    raw = json.load(f)

q2009 = raw['2009']
print(f'\nquestions_raw.json 2009 first question:')
q = q2009[0]
print(f'  num={q["num"]}')
print(f'  content={q["content"][:150]}')
print(f'  answer={q["answer"]}')
print(f'  options={json.dumps(q.get("options",{}), ensure_ascii=False)[:100]}')

cur.close()
conn.close()
