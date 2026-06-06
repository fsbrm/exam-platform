import pymysql, re

conn = pymysql.connect(host='localhost', user='root', password='123456', database='exam_platform', charset='utf8mb4')
cur = conn.cursor()

# Fix SINGLE questions for 2022-2025: remove img tags from content
cur.execute("""
    SELECT id, year, content FROM question 
    WHERE year >= 2022 AND type = 'SINGLE' AND content LIKE '%<img%'
""")
rows = cur.fetchall()
print(f"Found {len(rows)} SINGLE questions with img tags (2022-2025)")

fixed = 0
for qid, year, content in rows:
    clean = re.sub(r'<img[^>]*>', '', content).strip()
    if clean:
        cur.execute("UPDATE question SET content = %s WHERE id = %s", (clean, qid))
        fixed += 1

# Also fix MULTI questions
cur.execute("""
    SELECT id, year, content FROM question 
    WHERE year >= 2022 AND type IN ('MULTI') AND content LIKE '%<img%'
""")
mrows = cur.fetchall()
print(f"Found {len(mrows)} MULTI questions with img tags (2022-2025)")

for qid, year, content in mrows:
    clean = re.sub(r'<img[^>]*>', '', content).strip()
    if clean:
        cur.execute("UPDATE question SET content = %s WHERE id = %s", (clean, qid))
        fixed += 1

conn.commit()

# Also fix 2026 placeholder questions
cur.execute("""
    SELECT id, year, content FROM question 
    WHERE year = 2026 AND content LIKE '%<img%'
""")
r2026 = cur.fetchall()
for qid, year, content in r2026:
    clean = re.sub(r'<img[^>]*>', '', content).strip()
    if clean:
        cur.execute("UPDATE question SET content = %s WHERE id = %s", (clean, qid))
        fixed += 1

conn.commit()

# Verify
cur.execute("SELECT id, year, LEFT(content, 60) FROM question WHERE year=2025 AND type='SINGLE' LIMIT 2")
for row in cur.fetchall():
    print(f"  [{row[0]}] {row[1]}: {row[2]}")

cur.close()
conn.close()
print(f"Fixed {fixed} questions total")
