import pymysql
conn = pymysql.connect(host="localhost", user="root", password="123456", database="exam_platform", charset="utf8mb4")
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM question")
total = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM question WHERE content LIKE %s", ("%<img%",))
img = c.fetchone()[0]
print(f"Questions: {total}")
print(f"With screenshots: {img}")
c.execute("SELECT id, SUBSTRING(content,1,80) FROM question WHERE id=1")
row = c.fetchone()
if row:
    print(f"\nQ1 sample: {row[1]}")
c.execute("SELECT id, SUBSTRING(content,1,80) FROM question WHERE id=41")
row = c.fetchone()
if row:
    print(f"Q41 sample: {row[1]}")
conn.close()
