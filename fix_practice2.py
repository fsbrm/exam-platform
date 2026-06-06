# Fix PracticePage.vue - two issues
filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Bug 1: Missing closing ) in template line 57
content = content.replace(
    '<span>正确率{{ correctPercent }}%（{{ correctCount }}/{{ answeredCount }}题</span>',
    '<span>正确率{{ correctPercent }}%（{{ correctCount }}/{{ answeredCount }}）题</span>'
)

# Bug 2: renderedContent still using renderText - fix it properly
# Find the exact line
import re
pattern = r"const renderedContent = computed\(\(\) => \{ const img = currentQuestion\.value\?\.image \? <img src=\\\"\\\" style=\\\"max-width:100%;margin:8px 0;border-radius:6px\\\" /> : ''; return img \+ renderText\(currentQuestion\.value\?\.content \|\| ''\) \}\)"
new_rc = "const renderedContent = computed(() => { const img = currentQuestion.value?.image ? <img src=\"\" style=\"max-width:100%;margin:8px 0;border-radius:6px\" /> : ''; return img + (currentQuestion.value?.content || '') })"

# Try a simpler approach - just find and replace the line containing renderText in renderedContent
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'renderedContent' in line and 'renderText' in line:
        print(f'Fixing line {i+1}: {line[:80]}...')
        lines[i] = "const renderedContent = computed(() => { const img = currentQuestion.value?.image ? <img src=\"\" style=\"max-width:100%;margin:8px 0;border-radius:6px\" /> : ''; return img + (currentQuestion.value?.content || '') })"
        break

content = '\n'.join(lines)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed!')
