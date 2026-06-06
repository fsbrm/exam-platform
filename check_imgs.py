import json, os

data_dir = r'D:\桌面\毕设\exam-platform\data'
img_dir = r'D:\桌面\毕设\exam-platform\frontend\public\images\questions'

# List all screenshots
imgs = sorted(os.listdir(img_dir))
print(f'Total screenshots: {len(imgs)}')

# Group by year
from collections import defaultdict
by_year = defaultdict(list)
for img in imgs:
    year = img[:4]
    if year.isdigit():
        by_year[year].append(img)

for y in sorted(by_year.keys()):
    pages = by_year[y]
    # Count unique base names
    print(f'  {y}: {len(pages)} images - {sorted(pages)[:5]}...')

# Check what comprehensive questions need
with open(os.path.join(data_dir, 'all_comp_q.json'), 'r', encoding='utf-8') as f:
    comp = json.load(f)
    
print(f'\nComprehensive questions by year:')
comp_by_year = defaultdict(list)
for c in comp:
    comp_by_year[str(c['y'])].append(c)

for y in sorted(comp_by_year.keys()):
    imgs_for_year = by_year.get(y, [])
    q_count = len(comp_by_year[y])
    subjects = set(str(c.get('s')) for c in comp_by_year[y])
    print(f'  {y}: {q_count} questions, subjects={subjects}, has_imgs={len(imgs_for_year)>0}')
