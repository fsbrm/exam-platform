import json, pymysql, os

data_dir = r'D:\桌面\毕设\exam-platform\data'
conn = pymysql.connect(host='localhost', user='root', password='123456', database='exam_platform', charset='utf8mb4')
cur = conn.cursor()

# 1. Load questions_raw.json (has proper text for 2009-2021)
with open(os.path.join(data_dir, 'questions_raw.json'), 'r', encoding='utf-8') as f:
    raw = json.load(f)

# Build flat list: (year, num) -> question data
raw_map = {}
for year_str, qlist in raw.items():
    year = int(year_str)
    for q in qlist:
        raw_map[(year, q['num'])] = q

# 2. Get all SINGLE questions from DB ordered by year, id
cur.execute("SELECT id, year, content, chapter_id, subject_id FROM question WHERE type='SINGLE' ORDER BY year, id")
singles = cur.fetchall()

# Group by year and index
from collections import defaultdict
by_year = defaultdict(list)
for s in singles:
    by_year[s[1]].append(s)

# 3. Restore text content - use questions_raw.json text
fixed = 0
for year, qlist in by_year.items():
    year_qs = raw.get(str(year), [])
    if not year_qs:
        continue
    
    for idx, q in enumerate(qlist):
        qid, qyear, old_content, ch_id, subj_id = q
        
        if idx >= len(year_qs):
            continue
        
        rq = year_qs[idx]
        text = rq['content']
        answer = rq.get('answer', '')
        options = rq.get('options', {})
        
        # Build clean content: text only, no screenshot
        # Add a small "查看原题截图" link at the bottom
        qnum = rq['num']
        page_num = (qnum - 1) // 5 + 1  # ~5 questions per page
        img_path = f'/images/questions/{year}_p{page_num:02d}.png'
        
        # Only include screenshot if it helps (for questions with diagrams)
        # For now, use text-only content
        new_content = text
        
        # Update DB
        cur.execute("""
            UPDATE question SET content = %s, answer = %s, options = %s
            WHERE id = %s
        """, (new_content, answer, json.dumps(options, ensure_ascii=False), qid))
        fixed += 1

conn.commit()
print(f'Fixed SINGLE: {fixed}')

# 4. Handle MULTI questions similarly
# For multi-choice, the raw data might be structured differently
# Let's check if there's multi data in questions_raw.json
# Actually questions_raw only has SINGLE (40 per year). MULTI are separate.

# For MULTI questions, let's keep existing content but remove the full-page screenshot
cur.execute("SELECT id, content FROM question WHERE type='MULTI'")
multi_fixed = 0
for row in cur.fetchall():
    qid, content = row
    if content and '<img' in content:
        # Remove img tag, keep text
        import re
        clean = re.sub(r'<img[^>]*>', '', content).strip()
        if clean and clean != content:
            cur.execute("UPDATE question SET content = %s WHERE id = %s", (clean, qid))
            multi_fixed += 1

conn.commit()
print(f'Fixed MULTI: {multi_fixed}')

# 5. Verify
cur.execute("SELECT id, year, type, LEFT(content, 60) FROM question WHERE type='SINGLE' AND year=2009 LIMIT 3")
for row in cur.fetchall():
    print(f'  [{row[0]}] {row[1]} {row[2]}: {row[3]}...')

cur.close()
conn.close()
print('Done!')
