import re, os

with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed-v6.sql", "r", encoding="utf-8") as f:
    seed = f.read()

page_counts = {2009:17,2010:16,2011:14,2012:18,2013:19,2014:20,2015:13,2016:11,2017:12,2018:12,2019:12,2020:29,2021:18}

fixed = 0
for year in range(2009, 2022):
    total = page_counts.get(year, 15)
    start_page = total - 7
    
    pattern = rf"(\(\d+,\d+,\d+,'MULTI','HARD','[^']*','\[\]','[^']*','[^']*',{year}\))"
    matches = list(re.finditer(pattern, seed))
    
    for i, m in enumerate(matches):
        page = start_page + i
        img_path = f"/images/questions/{year}_p{page:02d}.png"
        img_file = rf"D:\桌面\毕设\exam-platform\frontend\public\images\questions\{year}_p{page:02d}.png"
        
        if not os.path.exists(img_file):
            continue
        
        old = m.group(0)
        new = old.replace(",'[]','", f",'[]','{img_path}','")
        seed = seed.replace(old, new, 1)
        fixed += 1

print(f"Fixed {fixed} comprehensive questions with image paths")
with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed-v6.sql", "w", encoding="utf-8") as f:
    f.write(seed)
print("Done")
