import pymysql, os, re

conn = pymysql.connect(host='localhost', user='root', password='123456', database='exam_platform', charset='utf8mb4')
cur = conn.cursor()

img_dir = r'D:\桌面\毕设\exam-platform\frontend\public\images\questions'

# Get all images grouped by year
imgs_by_year = {}
for img in os.listdir(img_dir):
    year = img[:4]
    if year.isdigit():
        imgs_by_year.setdefault(int(year), []).append(img)

# Sort images for each year
for y in imgs_by_year:
    imgs_by_year[y].sort()

# Get all comprehensive questions
cur.execute("SELECT id, year, subject_id, content FROM question WHERE type='COMPREHENSIVE' ORDER BY year, id")
comp_qs = cur.fetchall()

# Comprehensive questions per year: 7 questions (41-47)
# Subject mapping: 41=DS, 42=DS, 43=CO, 44=CO, 45=OS, 46=OS, 47=CN
# Pages typically: Q41-42 on page 8, Q43-44 on page 9, Q45-46 on page 10, Q47 on page 11
# But this varies. Let's assign pages based on question index within year

fixed = 0
for qid, year, subject_id, content in comp_qs:
    # Skip if already has img tag
    if '<img' in (content or ''):
        continue
    
    year_imgs = imgs_by_year.get(year, [])
    if not year_imgs:
        continue
    
    # Determine which page to use based on question index
    # Count existing comp questions for this year to determine index
    cur.execute("SELECT COUNT(*) FROM question WHERE year=%s AND type='COMPREHENSIVE' AND id <= %s", (year, qid))
    idx = cur.fetchone()[0] - 1  # 0-based index
    
    # Map index to page (starts from about page 8 for comprehensive)
    # Comprehensive questions typically start around page 7-8
    # Let's use a fixed mapping
    page_idx = 7 + (idx // 2)  # 2 questions per page roughly
    
    # Find matching screenshot
    # Screenshots named like: 2009_p01.png, 2009_p02.png, etc.
    target_page = f'{year}_p{page_idx+1:02d}.png'
    
    # Check if this exact page exists
    img_path = f'/images/questions/{target_page}'
    full_path = os.path.join(img_dir, target_page)
    
    if os.path.exists(full_path):
        img_html = f'<img src="{img_path}" style="max-width:100%;margin:8px 0;border:1px solid #e5e7eb;border-radius:8px"/><br/>\n'
        new_content = img_html + (content or '')
        
        # Update DB
        cur.execute("UPDATE question SET content=%s WHERE id=%s", (new_content, qid))
        fixed += 1
    else:
        # Try to find any image for this year as fallback
        fallback = year_imgs[min(page_idx, len(year_imgs)-1)]
        img_path = f'/images/questions/{fallback}'
        img_html = f'<img src="{img_path}" style="max-width:100%;margin:8px 0;border:1px solid #e5e7eb;border-radius:8px"/><br/>\n'
        new_content = img_html + (content or '')
        cur.execute("UPDATE question SET content=%s WHERE id=%s", (new_content, qid))
        fixed += 1

conn.commit()
print(f'Added screenshots to {fixed}/{len(comp_qs)} comprehensive questions')

# Verify
cur.execute("SELECT id, year, LEFT(content, 80) FROM question WHERE type='COMPREHENSIVE' LIMIT 5")
for row in cur.fetchall():
    print(f'  [{row[0]}] {row[1]}: {row[2][:80]}...')

cur.close()
conn.close()
print('Done!')
