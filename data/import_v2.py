import pymysql

conn = pymysql.connect(host="localhost", user="root", password="123456", database="exam_platform", charset="utf8mb4", autocommit=True)
c = conn.cursor()

# Clear
c.execute("SET FOREIGN_KEY_CHECKS=0")
for t in ["question_knowledge","paper_question","exam_question","user_answer","wrong_question","favorite","note","exam_record","question"]:
    c.execute(f"DELETE FROM {t}")
c.execute("SET FOREIGN_KEY_CHECKS=1")

# Read seed.sql and find just the question INSERT block
with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed.sql", "r", encoding="utf-8-sig") as f:
    content = f.read()

# Find INSERT INTO question ... VALUES ( ... );
# Strategy: locate the question INSERT, grab everything until the closing );
q_start = content.find("INSERT INTO question")
q_end = content.find(";\n\nINSERT INTO paper_question", q_start)
if q_end < 0:
    q_end = content.find(";\n\n--", q_start)
if q_end < 0:
    # Find last ) before next section
    q_end = content.find(";\n\nINSERT INTO question_knowledge", q_start)
if q_end < 0:
    q_end = content.find(";\nUPDATE", q_start)

question_sql = content[q_start:q_end+1].strip()
print(f"Question SQL length: {len(question_sql)} chars")

try:
    c.execute(question_sql)
    print("Question INSERT executed successfully")
except Exception as e:
    print(f"Question INSERT error: {str(e)[:200]}")

c.execute("SELECT COUNT(*) FROM question")
print(f"Questions: {c.fetchone()[0]}")

# Also exec paper_question and question_knowledge
for table in ["paper_question", "question_knowledge"]:
    start = content.find(f"INSERT INTO {table}")
    end = content.find(";\n", start + 50)
    if end < 0:
        end = content.find(";", start + 50)
    sql = content[start:end+1].strip()
    if sql:
        try:
            c.execute(sql)
            print(f"{table}: OK")
        except Exception as e:
            print(f"{table}: {str(e)[:80]}")

c.execute("SELECT COUNT(*) FROM question")
print(f"\nTotal questions: {c.fetchone()[0]}")
conn.close()
