import pymysql

conn = pymysql.connect(host='localhost', user='root', password='123456', database='exam_platform', charset='utf8mb4')
cur = conn.cursor()

cur.execute("SELECT id, year FROM exam_paper ORDER BY year")
papers = cur.fetchall()

for paper_id, year in papers:
    # SINGLE: 1-40 (by id order)
    cur.execute("""
        SELECT pq.id FROM paper_question pq 
        JOIN question q ON pq.question_id = q.id 
        WHERE pq.paper_id = %s AND q.type = 'SINGLE'
        ORDER BY q.id
    """, (paper_id,))
    singles = cur.fetchall()
    for i, (pq_id,) in enumerate(singles):
        cur.execute("UPDATE paper_question SET question_number = %s WHERE id = %s", (i + 1, pq_id))
    
    # COMPREHENSIVE: 41-47 (by id order)
    cur.execute("""
        SELECT pq.id FROM paper_question pq 
        JOIN question q ON pq.question_id = q.id 
        WHERE pq.paper_id = %s AND q.type = 'COMPREHENSIVE'
        ORDER BY q.id
    """, (paper_id,))
    comps = cur.fetchall()
    for i, (pq_id,) in enumerate(comps[:7]):
        cur.execute("UPDATE paper_question SET question_number = %s WHERE id = %s", (41 + i, pq_id))
    
    # MULTI: assign 41-47 (same range, share with comprehensive)
    cur.execute("""
        SELECT pq.id FROM paper_question pq 
        JOIN question q ON pq.question_id = q.id 
        WHERE pq.paper_id = %s AND q.type = 'MULTI'
        ORDER BY q.id
    """, (paper_id,))
    multis = cur.fetchall()
    for i, (pq_id,) in enumerate(multis[:7]):
        cur.execute("UPDATE paper_question SET question_number = %s WHERE id = %s", (41 + i, pq_id))
    
    print(f"  {year}: SINGLE={len(singles)}, COMP={len(comps)}, MULTI={len(multis)}")

conn.commit()
cur.close()
conn.close()
print('Done!')
