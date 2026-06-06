import pymysql

conn = pymysql.connect(host='localhost', user='root', password='123456', database='exam_platform', charset='utf8mb4')
cur = conn.cursor()

# Clear existing links
cur.execute("DELETE FROM question_knowledge")
conn.commit()

# Get knowledge points ordered by chapter and sort_order
cur.execute("SELECT id, chapter_id, sort_order FROM knowledge_point ORDER BY chapter_id, sort_order")
kps = cur.fetchall()

# Group by chapter and preserve order
from collections import defaultdict
kp_by_chapter = defaultdict(list)
for kpid, chid, sort_order in kps:
    kp_by_chapter[chid].append(kpid)

# Get questions with chapter_id
cur.execute("SELECT id, chapter_id FROM question ORDER BY chapter_id, id")
questions = cur.fetchall()

# For each chapter, assign questions to KPs round-robin style
# This ensures each KP gets unique questions
inserted = 0
chapter_questions = defaultdict(list)
for qid, chid in questions:
    if chid:
        chapter_questions[chid].append(qid)

for chid, qids in chapter_questions.items():
    kpids = kp_by_chapter.get(chid, [])
    if not kpids:
        continue
    
    # Distribute questions among KPs: each question goes to 1 KP (round-robin)
    # Plus some overlap for larger chapters
    for i, qid in enumerate(qids):
        # Primary KP: round-robin
        primary_kp = kpids[i % len(kpids)]
        cur.execute("INSERT IGNORE INTO question_knowledge (question_id, knowledge_id) VALUES (%s, %s)", (qid, primary_kp))
        inserted += 1
        
        # Secondary KP: next in rotation (for chapters with >2 KPs)
        if len(kpids) >= 3:
            secondary_kp = kpids[(i + 1) % len(kpids)]
            cur.execute("INSERT IGNORE INTO question_knowledge (question_id, knowledge_id) VALUES (%s, %s)", (qid, secondary_kp))
            inserted += 1

conn.commit()

# Verify distribution
cur.execute("""
    SELECT kp.id, kp.name, COUNT(qk.question_id) as cnt
    FROM knowledge_point kp
    LEFT JOIN question_knowledge qk ON kp.id = qk.knowledge_id
    GROUP BY kp.id, kp.name
    ORDER BY kp.chapter_id, kp.sort_order
    LIMIT 15
""")
for row in cur.fetchall():
    print(f"  KP {row[0]} [{row[1]}]: {row[2]} questions")

cur.execute("SELECT COUNT(*) FROM question_knowledge")
total = cur.fetchone()[0]
print(f"\nTotal links: {total}")

# Verify uniqueness: each question should have different KP sets
cur.execute("""
    SELECT question_id, COUNT(*) as cnt
    FROM question_knowledge
    GROUP BY question_id
    ORDER BY cnt DESC
    LIMIT 5
""")
for row in cur.fetchall():
    print(f"  Q{row[0]}: {row[1]} KPs")

cur.close()
conn.close()
print("Done!")
