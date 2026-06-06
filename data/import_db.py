import pymysql

conn = pymysql.connect(host="localhost", user="root", password="123456", database="exam_platform", charset="utf8mb4")
cursor = conn.cursor()

# Clear existing questions first
cursor.execute("SET FOREIGN_KEY_CHECKS=0")
cursor.execute("TRUNCATE TABLE question_knowledge")
cursor.execute("TRUNCATE TABLE paper_question")
cursor.execute("TRUNCATE TABLE exam_question")
cursor.execute("TRUNCATE TABLE user_answer")
cursor.execute("TRUNCATE TABLE wrong_question")
cursor.execute("TRUNCATE TABLE favorite")
cursor.execute("TRUNCATE TABLE note")
cursor.execute("TRUNCATE TABLE exam_record")
cursor.execute("DELETE FROM question")
cursor.execute("SET FOREIGN_KEY_CHECKS=1")
print("Cleared old data")

# Import seed.sql
with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed.sql", "r", encoding="utf-8") as f:
    sql = f.read()

# Execute in chunks
statements = sql.split(";\n")
ok = 0
for stmt in statements:
    stmt = stmt.strip()
    if not stmt or stmt.startswith("--") or stmt == "USE exam_platform":
        continue
    try:
        cursor.execute(stmt)
        ok += 1
    except Exception as e:
        err = str(e)[:100]
        if "Duplicate" in err or "Base table" in err:
            pass
        else:
            print(f"  Error: {err}")

conn.commit()
cursor.execute("SELECT COUNT(*) FROM question")
count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM question WHERE content LIKE '%<img%'")
img_count = cursor.fetchone()[0]
print(f"\nTotal questions: {count}")
print(f"With screenshots: {img_count}")

conn.close()
print("Done!")
