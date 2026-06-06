with open(r'D:\桌面\毕设\exam-platform\frontend\src\views\paper\PaperDetailPage.vue', 'r', encoding='utf-8') as f:
    content = f.read()

# Check for common syntax issues
import re
# Check for unmatched template expressions
open_braces = content.count('{{')
close_braces = content.count('}}')
print(f'Template braces: {{ = {open_braces}, }} = {close_braces}')
if open_braces != close_braces:
    print('WARNING: mismatched braces!')

# Check for v-html usage
vhtml_count = content.count('v-html')
print(f'v-html directives: {vhtml_count}')

# Check for COMPREHENSIVE handling
comp_count = content.count('COMPREHENSIVE')
print(f'COMPREHENSIVE refs: {comp_count}')

with open(r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue', 'r', encoding='utf-8') as f:
    content2 = f.read()
open2 = content2.count('{{')
close2 = content2.count('}}')
print(f'\nPracticePage braces: {{ = {open2}, }} = {close2}')
if open2 != close2:
    # Find mismatched lines
    lines = content2.split('\n')
    depth = 0
    for i, line in enumerate(lines):
        depth += line.count('{{') - line.count('}}')
        if depth < 0:
            print(f'  Issue line {i+1}: {line.strip()[:80]}')
            depth = 0
