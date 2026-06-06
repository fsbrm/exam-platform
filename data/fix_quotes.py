import re

with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed.sql", "r", encoding="utf-8-sig") as f:
    content = f.read()

# Fix: Replace style="..." with style='...' in img tags (to avoid SQL quote conflicts)
# Pattern: style="max-width:100%;..."  -> style='max-width:100%;...'
old_style = 'style="max-width:100%;margin:8px 0;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.1)"'
new_style = "style='max-width:100%;margin:8px 0;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.1)'"

count = content.count(old_style)
content = content.replace(old_style, new_style)

# Also fix loading="lazy"
old_load = ' loading="lazy"'
new_load = " loading='lazy'"
content = content.replace(old_load, new_load)

# Fix src="..."
# We need to handle src="..." carefully since it's inside a SQL string
# Actually src="..." is fine inside SQL '' if the whole content is in ''
# The issue is specifically with " characters inside SQL '...' strings

print(f"Fixed {count} style attributes")

with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed.sql", "w", encoding="utf-8") as f:
    f.write(content)
print("seed.sql updated with single-quoted style attributes")
