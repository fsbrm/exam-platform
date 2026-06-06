import pymysql

conn = pymysql.connect(host="localhost", user="root", password="123456", database="exam_platform", charset="utf8mb4", autocommit=True)
c = conn.cursor()

# Clear
c.execute("SET FOREIGN_KEY_CHECKS=0")
for t in ["question_knowledge","paper_question","exam_question","user_answer","wrong_question","favorite","note","exam_record","question"]:
    c.execute(f"DELETE FROM {t}")
c.execute("SET FOREIGN_KEY_CHECKS=1")
print("Cleared")

# Read and exec question INSERT
with open(r"D:\seed_temp.sql", "r", encoding="utf-8-sig") as f:
    content = f.read()

q_start = content.find("INSERT INTO question")
q_end = content.find(";\n\nINSERT INTO paper_question", q_start)

question_sql = content[q_start:q_end+1].strip()
print(f"SQL length: {len(question_sql)}")

try:
    c.execute(question_sql)
    print("OK! Questions imported")
except Exception as e:
    print(f"Error: {str(e)[:200]}")

c.execute("SELECT COUNT(*) FROM question")
total = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM question WHERE content LIKE %s", ("%<img%",))
img = c.fetchone()[0]
print(f"Questions: {total}, With screenshots: {img}")

# Import paper_question and question_knowledge
for table in ["paper_question", "question_knowledge"]:
    start = content.find(f"INSERT INTO {table}")
    end = content.find(";\n", start + 50)
    sql = content[start:end+1].strip()
    try:
        c.execute(sql)
        print(f"{table}: OK")
    except Exception as e:
        print(f"{table}: {str(e)[:80]}")

c.execute("SELECT COUNT(*) FROM question")
print(f"\nFinal: {c.fetchone()[0]} questions")
conn.close()
