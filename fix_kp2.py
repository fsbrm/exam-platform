import pymysql

conn = pymysql.connect(host='localhost', user='root', password='123456', database='exam_platform', charset='utf8mb4')
cur = conn.cursor()

# Get all knowledge points grouped by chapter
cur.execute("SELECT id, chapter_id FROM knowledge_point")
kp_by_chapter = {}
for row in cur.fetchall():
    kpid, chid = row
    kp_by_chapter.setdefault(chid, []).append(kpid)

print(f"Knowledge points: {sum(len(v) for v in kp_by_chapter.values())} total, {len(kp_by_chapter)} chapters")

# Get questions grouped by chapter
cur.execute("SELECT id, chapter_id FROM question")
q_by_chapter = {}
for row in cur.fetchall():
    qid, chid = row
    if chid:
        q_by_chapter.setdefault(chid, []).append(qid)

print(f"Questions with chapter: {sum(len(v) for v in q_by_chapter.values())}")

# Link them
inserted = 0
for chid, qids in q_by_chapter.items():
    kpids = kp_by_chapter.get(chid, [])
    if not kpids:
        continue
    for qid in qids:
        for kpid in kpids:
            cur.execute("INSERT IGNORE INTO question_knowledge (question_id, knowledge_id) VALUES (%s, %s)", (qid, kpid))
            inserted += cur.rowcount

conn.commit()

cur.execute("SELECT COUNT(*) FROM question_knowledge")
print(f"Total links: {cur.fetchone()[0]}")
print(f"Inserted this run: {inserted}")

cur.close()
conn.close()
