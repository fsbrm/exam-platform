import pymysql

conn = pymysql.connect(host="localhost", user="root", password="123456", database="exam_platform", charset="utf8mb4", autocommit=True)
cursor = conn.cursor()

# Clear
cursor.execute("SET FOREIGN_KEY_CHECKS=0")
for t in ["question_knowledge","paper_question","exam_question","user_answer","wrong_question","favorite","note","exam_record","question"]:
    cursor.execute(f"DELETE FROM {t}")
cursor.execute("SET FOREIGN_KEY_CHECKS=1")
print("Cleared old data")

# Read and execute raw SQL
with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed.sql", "r", encoding="utf-8") as f:
    sql = f.read()

# Remove USE statement
sql = sql.replace("USE exam_platform;\n", "")

# Execute with multi=True (handles multiple statements)
try:
    for result in cursor.execute(sql, multi=True):
        pass  # consume all results
    print("Executed seed.sql")
except Exception as e:
    print(f"Error: {e}")

cursor.execute("SELECT COUNT(*) FROM question")
total = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM question WHERE content LIKE '%%<img%%'")
img = cursor.fetchone()[0]
print(f"Total questions: {total}")
print(f"With screenshots: {img}")

conn.close()
