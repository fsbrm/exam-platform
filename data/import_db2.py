import pymysql, re

conn = pymysql.connect(host="localhost", user="root", password="123456", database="exam_platform", charset="utf8mb4")
cursor = conn.cursor()

# Clear old data
cursor.execute("SET FOREIGN_KEY_CHECKS=0")
for t in ["question_knowledge","paper_question","exam_question","user_answer","wrong_question","favorite","note","exam_record","question"]:
    cursor.execute(f"DELETE FROM {t}")
cursor.execute("SET FOREIGN_KEY_CHECKS=1")
print("Cleared")

# Read seed.sql
with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed.sql", "r", encoding="utf-8") as f:
    content = f.read()

# Split by INSERT statements, execute each complete INSERT
# Find all INSERT INTO ... VALUES blocks
blocks = re.split(r';\s*\n(?=INSERT|USE|UPDATE|SELECT)', content)
# Actually, more robust: find INSERT ... VALUES ... ; blocks
# The seed.sql has large INSERT statements with many VALUES rows

# Simpler: find the INSERT INTO question block and execute it as one statement
pattern = r'(INSERT INTO question\s+\([^)]+\)\s+VALUES\s+)(.*?);'
question_match = re.search(pattern, content, re.DOTALL)

if question_match:
    # Split VALUES part into chunks to avoid max_allowed_packet issues
    values_part = question_match.group(2)
    header = question_match.group(1)
    
    # Split into individual value tuples
    # Each tuple ends with ),\n or );
    tuples = re.findall(r'\([^)]+\)(?:,|\s*$)', values_part)
    print(f"Found {len(tuples)} question tuples")
    
    # Execute in chunks of 100
    chunk_size = 100
    for i in range(0, len(tuples), chunk_size):
        chunk = tuples[i:i+chunk_size]
        sql = header + ',\n'.join(chunk).rstrip(',') + ';'
        try:
            cursor.execute(sql)
        except Exception as e:
            print(f"  Chunk {i//chunk_size} error: {str(e)[:100]}")
    
    conn.commit()
    print("Questions imported")

cursor.execute("SELECT COUNT(*) FROM question")
total = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM question WHERE content LIKE '%<img%'")
img = cursor.fetchone()[0]
print(f"\nTotal: {total}, With screenshots: {img}")

conn.close()
print("Done!")
