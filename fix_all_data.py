import json, pymysql, os

data_dir = r'D:\桌面\毕设\exam-platform\data'
conn = pymysql.connect(host='localhost', user='root', password='123456', database='exam_platform', charset='utf8mb4')
cur = conn.cursor()

# =====================
# Step 1: Match DB questions with raw data by year+order
# =====================
with open(os.path.join(data_dir, 'questions_raw.json'), 'r', encoding='utf-8') as f:
    raw = json.load(f)

# Build lookup: (year, order_index) -> num
year_order_to_num = {}
for year_str, qlist in raw.items():
    year = int(year_str)
    for idx, q in enumerate(qlist):
        year_order_to_num[(year, idx)] = q.get('num', idx+1)

# Get all DB questions sorted
cur.execute("SELECT id, year, subject_id, chapter_id FROM question WHERE type='SINGLE' ORDER BY year, id")
db_questions = cur.fetchall()
print(f'DB SINGLE questions: {len(db_questions)}')

# Group by year and index
from collections import defaultdict
year_qs = defaultdict(list)
for q in db_questions:
    year_qs[q[1]].append(q)

# Subject mapping by question number
def get_subject(num):
    if 1 <= num <= 11: return 10
    elif 12 <= num <= 22: return 20
    elif 23 <= num <= 32: return 30
    elif 33 <= num <= 40: return 40
    return None

def get_chapter(subject, num):
    if subject == 10:
        parts = [(1,3,101),(4,5,102),(6,7,103),(8,9,104),(10,10,105),(11,11,106)]
    elif subject == 20:
        parts = [(12,13,201),(14,15,202),(16,17,203),(18,19,204),(20,21,205),(22,22,206)]
    elif subject == 30:
        parts = [(23,25,301),(26,27,302),(28,29,303),(30,30,304),(31,32,305)]
    elif subject == 40:
        parts = [(33,34,401),(35,35,402),(36,37,403),(38,39,404),(40,40,405)]
    else:
        return None
    for lo, hi, ch in parts:
        if lo <= num <= hi:
            return ch
    return None

fixed_subj = 0
fixed_ch = 0
for year, qlist in year_qs.items():
    for idx, q in enumerate(qlist):
        qid, qyear, _, _ = q
        num = year_order_to_num.get((year, idx), idx+1)
        subject = get_subject(num)
        chapter = get_chapter(subject, num) if subject else None
        if subject:
            cur.execute("UPDATE question SET subject_id=%s WHERE id=%s AND subject_id!=%s", (subject, qid, subject))
            if cur.rowcount > 0: fixed_subj += 1
        if chapter:
            cur.execute("UPDATE question SET chapter_id=%s WHERE id=%s AND chapter_id!=%s", (chapter, qid, chapter))
            if cur.rowcount > 0: fixed_ch += 1

conn.commit()
print(f'Fixed subject_id: {fixed_subj}')
print(f'Fixed chapter_id: {fixed_ch}')

# =====================
# Step 2: Fix MULTI questions similarly
# =====================
# Multi-choice in 408: Q41-45 (or similar), each year has specific multi questions
# Typically: DS 41-42, CO 43-44, OS 45, CN 46-48 (varies by year)
# For simplicity map based on known patterns
# 2009-2021 multi questions: 5 per year (Q41-45)
multi_subj_map = {
    41: 10, 42: 10,  # DS
    43: 20, 44: 20,  # CO
    45: 30,           # OS
    46: 40, 47: 40,  # CN (some years)
}
multi_ch_map = {
    41: 103, 42: 104,  # DS: tree, graph
    43: 203, 44: 205,  # CO: storage, CPU
    45: 302,           # OS: sync
    46: 404, 47: 405,  # CN: network, transport
}

cur.execute("SELECT id, year FROM question WHERE type='MULTI' ORDER BY year, id")
multi_qs = cur.fetchall()
print(f'DB MULTI questions: {len(multi_qs)}')

multi_by_year = defaultdict(list)
for q in multi_qs:
    multi_by_year[q[1]].append(q[0])

m_fixed = 0
for year, qids in multi_by_year.items():
    for idx, qid in enumerate(qids):
        qnum = 41 + idx  # Multi questions start at 41
        subject = multi_subj_map.get(qnum, 20)
        chapter = multi_ch_map.get(qnum, 203)
        cur.execute("UPDATE question SET subject_id=%s, chapter_id=%s WHERE id=%s", (subject, chapter, qid))
        m_fixed += 1

conn.commit()
print(f'Fixed MULTI: {m_fixed}')

# =====================
# Step 3: Add 2022-2025 papers
# =====================
for year in [2022, 2023, 2024, 2025]:
    cur.execute("SELECT id FROM exam_paper WHERE year = %s", (year,))
    if not cur.fetchone():
        cur.execute("INSERT INTO exam_paper (subject_id, duration, question_count, year, name) VALUES (1, 180, 47, %s, %s)",
                    (year, f'{year}年408计算机基础综合真题'))
        print(f'Added paper: {year}')
conn.commit()

# =====================
# Step 4: Rebuild paper_question links
# =====================
cur.execute("DELETE FROM paper_question")
conn.commit()

link_count = 0
for year in range(2009, 2026):
    cur.execute("SELECT id FROM exam_paper WHERE year = %s", (year,))
    paper = cur.fetchone()
    if not paper:
        continue
    paper_id = paper[0]
    
    cur.execute("SELECT id FROM question WHERE year = %s", (year,))
    for row in cur.fetchall():
        cur.execute("INSERT IGNORE INTO paper_question (paper_id, question_id, sort_order) VALUES (%s, %s, %s)", 
                    (paper_id, row[0], 0))
        link_count += 1

conn.commit()
print(f'Paper-question links: {link_count}')

cur.close()
conn.close()
print('Done!')
