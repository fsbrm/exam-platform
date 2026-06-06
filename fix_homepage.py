filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\home\HomePage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix practice button subjectId
content = content.replace(
    "@click=\"$router.push('/practice?subjectId=1')\"",
    "@click=\".push('/practice?subjectId=10')\""
)

# Also check if there are other subjectId=1 references
import re
matches = re.findall(r'subjectId[=:]\s*[\"\']?1[\"\']?', content)
if matches:
    print(f'Other subjectId=1 found: {matches}')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('HomePage.vue updated!')
