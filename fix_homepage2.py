filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\home\HomePage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken line
content = content.replace(
    "@click=\".push('/practice?subjectId=10')\"",
    "@click=\"$router.push('/practice?subjectId=10')\""
)

# Also handle non-backtick version
content = content.replace(
    '@click=".push(\'/practice?subjectId=10\')"',
    '@click=".push(\'/practice?subjectId=10\')"'
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
import re
match = re.search(r'@click="[^"]*practice[^"]*"', content)
if match:
    print(f'Practice link: {match.group()}')
