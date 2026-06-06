import pymysql

conn = pymysql.connect(host="localhost", user="root", password="123456", database="exam_platform", charset="utf8mb4")
c = conn.cursor()

# Clear
c.execute("SET FOREIGN_KEY_CHECKS=0")
for t in ["question_knowledge","paper_question","exam_question","user_answer","wrong_question","favorite","note","exam_record","question"]:
    c.execute(f"DELETE FROM {t}")
c.execute("SET FOREIGN_KEY_CHECKS=1")
conn.commit()

# Read seed.sql
with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed.sql", "r", encoding="utf-8-sig") as f:
    content = f.read()

# Remove USE statement and comments
content = content.replace("USE exam_platform;", "")

# Split by INSERT
parts = content.split("INSERT INTO")
for part in parts:
    if not part.strip():
        continue
    sql = "INSERT INTO" + part
    # Find the end - look for the last ); in the statement
    # Simple: find the first ); that ends the VALUES block
    end_idx = sql.find(";\n\n")
    if end_idx < 0:
        end_idx = sql.find(";\nUPDATE") 
    if end_idx < 0:
        end_idx = sql.find(";\n--") 
    if end_idx < 0:
        end_idx = sql.rfind(");") + 2
    
    sql = sql[:end_idx+1].strip()
    if not sql or len(sql) < 20:
        continue
    
    try:
        c.execute(sql)
        conn.commit()
        print(f"OK: {sql[10:60].strip()}...")
    except Exception as e:
        # Try to parse the table name
        table = sql.split()[0].strip()
        print(f"FAIL: {table} - {str(e)[:80]}")

c.execute("SELECT COUNT(*) FROM question")
print(f"\nTotal questions: {c.fetchone()[0]}")
conn.close()
