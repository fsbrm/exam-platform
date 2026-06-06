import pymysql, re

conn = pymysql.connect(host='localhost', user='root', password='123456', database='exam_platform', charset='utf8mb4')
cur = conn.cursor()

# Find all 2022-2025 SINGLE questions that have my wrapper label
cur.execute("""
    SELECT id, year, content FROM question 
    WHERE year >= 2022 AND type = 'SINGLE' AND content LIKE '%<strong>%'
""")
rows = cur.fetchall()

fixed = 0
for qid, year, content in rows:
    # Remove the <strong> wrapper line, keep only the img tag
    # Pattern: <strong>...</strong><br/><img ... />
    clean = re.sub(r'<strong>.*?</strong>\s*<br\s*/?>', '', content)
    clean = clean.strip()
    
    if clean:
        cur.execute("UPDATE question SET content = %s WHERE id = %s", (clean, qid))
        fixed += 1

conn.commit()

# Verify
cur.execute("SELECT id, year, LEFT(content, 80) FROM question WHERE year=2023 AND type='SINGLE' LIMIT 2")
for row in cur.fetchall():
    print(f"  [{row[0]}] {row[1]}: {row[2]}")

cur.close()
conn.close()
print(f"Cleaned {fixed} questions")
