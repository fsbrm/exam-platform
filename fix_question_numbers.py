import pymysql

conn = pymysql.connect(host='localhost', user='root', password='123456', database='exam_platform', charset='utf8mb4')
cur = conn.cursor()

# Get all papers
cur.execute("SELECT id, year FROM exam_paper ORDER BY year")
papers = cur.fetchall()

for paper_id, year in papers:
    # Get questions for this paper, grouped by type
    cur.execute("""
        SELECT pq.id as pq_id, q.id as qid, q.type 
        FROM paper_question pq 
        JOIN question q ON pq.question_id = q.id 
        WHERE pq.paper_id = %s 
        ORDER BY FIELD(q.type, 'SINGLE', 'MULTI', 'COMPREHENSIVE'), q.id
    """, (paper_id,))
    
    rows = cur.fetchall()
    
    # Assign numbers: SINGLE=1-40, MULTI=41+, COMPREHENSIVE=41+
    single_num = 0
    multi_num = 40  # Start after 40
    comp_num = 47   # Start after multi (roughly)
    
    for pq_id, qid, qtype in rows:
        if qtype == 'SINGLE':
            single_num += 1
            qnum = single_num
        elif qtype == 'MULTI':
            multi_num += 1
            qnum = multi_num
        elif qtype == 'COMPREHENSIVE':
            comp_num += 1
            qnum = comp_num
        else:
            continue
        
        cur.execute("UPDATE paper_question SET question_number = %s WHERE id = %s", (qnum, pq_id))
    
    print(f"  {year}: {len(rows)} questions numbered")

conn.commit()
cur.close()
conn.close()
print('Done!')
