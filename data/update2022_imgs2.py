import re, os

with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed-v6.sql", "r", encoding="utf-8") as f:
    seed = f.read()

page_counts = {2022: 11, 2023: 11, 2024: 12, 2025: 12}
questions_per_page = 5

for year in range(2022, 2026):
    total = page_counts[year]
    single_pages = min(8, total - 3)
    
    # Match pattern WITH year included
    pattern = rf"(\(\d+,\d+,\d+,'SINGLE','[^']*',')([^']*)('.*?,{year}\))"
    all_matches = list(re.finditer(pattern, seed))
    year_matches = all_matches[:40]
    
    if not year_matches:
        print(f"{year}: no SINGLE matches found")
        continue
    
    fixed = 0
    for i, m in enumerate(year_matches):
        page = (i // questions_per_page) + 1
        if page > single_pages:
            page = single_pages
        
        img_file = rf"D:\桌面\毕设\exam-platform\frontend\public\images\questions\{year}_p{page:02d}.png"
        if not os.path.exists(img_file):
            continue
        
        qnum = i + 1
        img_tag = f'<img src="/images/questions/{year}_p{page:02d}.png" style="max-width:100%;margin:8px 0;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.1)" /><br/><small>{year}年408真题 第{qnum}题</small>'
        
        old = m.group(0)
        if "<img" not in m.group(2):
            new = m.group(1) + img_tag + m.group(3)
            if old in seed:
                seed = seed.replace(old, new, 1)
                fixed += 1
    
    print(f"{year}: {fixed}/{len(year_matches)} SINGLE updated with page images")

with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed-v6.sql", "w", encoding="utf-8") as f:
    f.write(seed)
print("Done")
