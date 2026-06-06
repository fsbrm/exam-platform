import re

with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed.sql", "r", encoding="utf-8-sig") as f:
    content = f.read()

# Replace all img tags with minimal format (no quotes needed in content)
# <img src='/images/...' style='...' loading='lazy' />
# -> <img src=/images/... style=max-width:100%;margin:8px 0;border-radius:6px loading=lazy />
old_img = re.compile(
    r"<img\s+src='(/images/questions/\d{4}_p\d+\.png)'\s+"
    r"style='max-width:100%;margin:8px\s+0;border-radius:6px;box-shadow:0\s+2px\s+8px\s+rgba\(0,0,0,0\.1\)'\s+"
    r"loading='lazy'\s*/>"
)

def replace_img(m):
    path = m.group(1)
    return f'<img src={path} style=max-width:100%;margin:8px 0;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.1) loading=lazy />'

count = len(old_img.findall(content))
content = old_img.sub(replace_img, content)

# Also fix <br/> tags that are inside content - should be fine without quotes
# Remove any remaining single quotes in img tags
content = content.replace("src='", "src=")
content = content.replace("style='", "style=")
content = content.replace("loading='lazy'", "loading=lazy")
# Fix the closing: style=...'/>  -> style=...'/> 
# Actually fix: ' /> - remove trailing quote
content = re.sub(r"'(/>)", r"\1", content)
content = re.sub(r"'( />)", r"\1", content)

print(f"Fixed {count} img tags to quoteless format")

with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed.sql", "w", encoding="utf-8") as f:
    f.write(content)
print("Done. Ready for import.")
