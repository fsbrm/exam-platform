import re, os, json

# Load page counts (from rendered images)
img_dir = r"D:\桌面\毕设\exam-platform\frontend\public\images\questions"
page_counts = {}
for f in os.listdir(img_dir):
    if f.endswith('.png') and '_p' in f and not f.startswith('test'):
        year = int(f[:4])
        page = int(f.split('_p')[1].split('.')[0])
        if year not in page_counts or page > page_counts[year]:
            page_counts[year] = page

# Sort and show
for y in sorted(page_counts):
    print(f"{y}: {page_counts[y]} pages")

# Read seed-v6.sql
with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed-v6.sql", "r", encoding="utf-8") as f:
    seed = f.read()

total_fixed = 0

for year in range(2009, 2026):
    if year not in page_counts:
        continue
    
    total_pages = page_counts[year]
    single_pages = total_pages - 7  # last 7 pages for comprehensive
    
    # === Process SINGLE questions (Q1-Q40) ===
    pattern = rf"(\(\d+,\d+,\d+,'SINGLE','[^']*',')([^']*)('.*?,{year}\))"
    matches = list(re.finditer(pattern, seed))
    year_singles = matches[:40]
    
    fixed_s = 0
    for i, m in enumerate(year_singles):
        # Map Q1-Q40 to pages 1 through single_pages
        # ~5 questions per page
        page = min((i // 5) + 1, single_pages)
        
        # Verify image exists
        img_file = os.path.join(img_dir, f"{year}_p{page:02d}.png")
        if not os.path.exists(img_file):
            continue
        
        img_tag = f'<img src="/images/questions/{year}_p{page:02d}.png" style="max-width:100%;margin:8px 0;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.1)" loading="lazy" />'
        
        old = m.group(0)
        # Remove any existing img tag in content
        clean_content = re.sub(r'<img[^>]+>', '', m.group(2))
        # Add image before cleaned content
        new = m.group(1) + img_tag + m.group(3)
        
        if old in seed:
            seed = seed.replace(old, new, 1)
            fixed_s += 1
            total_fixed += 1
    
    # === Process MULTI questions (Q41-Q47) ===
    pattern_m = rf"(\(\d+,\d+,\d+,'MULTI','HARD',')([^']*)('"
    matches_m = list(re.finditer(pattern_m, seed))
    
    # Filter to this year
    year_multis = []
    for m in matches_m:
        rest = seed[m.end():m.end()+15]
        if f",{year})" in rest:
            year_multis.append(m)
    year_multis = year_multis[:7]
    
    fixed_m = 0
    for i, m in enumerate(year_multis):
        page = single_pages + i + 1
        if page > total_pages:
            page = total_pages
        
        img_file = os.path.join(img_dir, f"{year}_p{page:02d}.png")
        if not os.path.exists(img_file):
            continue
        
        img_tag = f'<img src="/images/questions/{year}_p{page:02d}.png" style="max-width:100%;margin:8px 0;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.1)" loading="lazy" /><br/>'
        
        old = m.group(0)
        clean_content = re.sub(r'<img[^>]+>', '', m.group(2))
        new = m.group(1) + img_tag + clean_content + m.group(3)
        
        if old in seed:
            seed = seed.replace(old, new, 1)
            fixed_m += 1
            total_fixed += 1
    
    print(f"{year}: SINGLE {fixed_s}/40, MULTI {fixed_m}/7")

print(f"\nTotal fixed: {total_fixed}")

with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed-v6.sql", "w", encoding="utf-8") as f:
    f.write(seed)
print("seed-v6.sql updated")
