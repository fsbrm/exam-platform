import re, os

with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed-v6.sql", "r", encoding="utf-8") as f:
    seed = f.read()

page_counts = {2009:17,2010:16,2011:14,2012:18,2013:19,2014:20,2015:13,2016:11,2017:12,2018:12,2019:12,2020:29,2021:18}

# First, undo the bad fix: put answer back
print("Step 1: Undo bad changes...")
seed = re.sub(r",'\[\]','/images/questions/([^']+)','", r",'[]',''','", seed)

fixed = 0
for year in range(2009, 2022):
    total = page_counts.get(year, 15)
    start_page = total - 7
    
    pattern = rf"(\(\d+,\d+,\d+,'MULTI','HARD',')([^']*)(')"
    matches = list(re.finditer(pattern, seed))
    
    # Find only matches for this year
    year_prefix = f"({year})"
    for m in matches:
        # Check if this is for our year by looking at the full line
        full_match = m.group(0)
        # Get the full tuple to check year
        context_start = max(0, m.start() - 50)
        context = seed[context_start:m.end() + 50]
        
        if f",{year})" not in context:
            continue
        
        # Only process first 7 matches per year (Q41-Q47)
        year_matches = [x for x in matches if f",{year})" in seed[max(0,x.start()-50):x.end()+50]]
        year_matches = year_matches[:7]
        
        if m not in year_matches:
            continue
        
        i = year_matches.index(m)
        page = start_page + i
        img_file = rf"D:\桌面\毕设\exam-platform\frontend\public\images\questions\{year}_p{page:02d}.png"
        
        if not os.path.exists(img_file):
            continue
        
        img_tag = f'<img src="/images/questions/{year}_p{page:02d}.png" style="max-width:100%;margin:8px 0;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.1)" /><br/>'
        
        content = m.group(2)
        if not content.startswith("<img"):
            new_content = img_tag + content
            old_full = m.group(0)
            new_full = m.group(1) + new_content + m.group(3)
            seed = seed.replace(old_full, new_full, 1)
            fixed += 1
            print(f"{year} Q{41+i}: added page {page} image")

print(f"\nFixed {fixed} comprehensive questions with embedded images")
with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed-v6.sql", "w", encoding="utf-8") as f:
    f.write(seed)
print("Done")
