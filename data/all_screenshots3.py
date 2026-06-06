import re, os

img_dir = r"D:\桌面\毕设\exam-platform\frontend\public\images\questions"

page_counts = {}
for f in os.listdir(img_dir):
    m = re.match(r"(\d{4})_p(\d+)\.png", f)
    if m:
        year = int(m.group(1))
        page = int(m.group(2))
        if year not in page_counts or page > page_counts[year]:
            page_counts[year] = page

with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed-v6.sql", "r", encoding="utf-8") as f:
    seed = f.read()

total_fixed = 0

for year in range(2009, 2026):
    if year not in page_counts:
        continue
    
    total_pages = page_counts[year]
    single_pages = max(1, total_pages - 7)
    
    # SINGLE questions
    pattern_s = re.compile(rf"(\(\d+,\d+,\d+,'SINGLE','[^']*',')([^']*)('.*?,{year}\))")
    singles = [m for m in pattern_s.finditer(seed)][:40]
    
    fixed_s = 0
    for i, m in enumerate(singles):
        page = min((i // 5) + 1, single_pages)
        img_file = os.path.join(img_dir, f"{year}_p{page:02d}.png")
        if not os.path.exists(img_file):
            continue
        
        img_tag = f'<img src="/images/questions/{year}_p{page:02d}.png" style="max-width:100%;margin:8px 0;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.1)" loading="lazy" />'
        
        old = m.group(0)
        new = m.group(1) + img_tag + m.group(3)
        
        if old in seed:
            seed = seed.replace(old, new, 1)
            fixed_s += 1
            total_fixed += 1
    
    # MULTI questions - use simpler line-based approach
    lines = seed.split('\n')
    
    fixed_m = 0
    multi_idx = 0
    for li in range(len(lines)):
        line = lines[li]
        if f"MULTI" not in line or f"{year})" not in line:
            continue
        if multi_idx >= 7:
            break
        
        # Extract the line parts
        m2 = re.match(r"(\(\d+,\d+,\d+,'MULTI','HARD',')([^']*)('.*)", line)
        if not m2:
            continue
        
        page = min(single_pages + multi_idx + 1, total_pages)
        img_file = os.path.join(img_dir, f"{year}_p{page:02d}.png")
        if not os.path.exists(img_file):
            multi_idx += 1
            continue
        
        img_tag = f'<img src="/images/questions/{year}_p{page:02d}.png" style="max-width:100%;margin:8px 0;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.1)" loading="lazy" /><br/>'
        
        # Remove existing img tags
        content = re.sub(r'<img[^>]*/?>', '', m2.group(2)).strip()
        lines[li] = m2.group(1) + img_tag + content + m2.group(3)
        fixed_m += 1
        total_fixed += 1
        multi_idx += 1
    
    seed = '\n'.join(lines)
    
    if fixed_s > 0 or fixed_m > 0:
        print(f"{year}: SINGLE {fixed_s}, MULTI {fixed_m}")

print(f"\nTotal: {total_fixed}")
with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed-v6.sql", "w", encoding="utf-8") as f:
    f.write(seed)
print("Done")
