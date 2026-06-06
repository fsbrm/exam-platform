with open(r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f'Total lines: {len(lines)}')
# Find the style section
for i, line in enumerate(lines):
    if '<style' in line:
        print(f'Style starts at line {i+1}')
        break
