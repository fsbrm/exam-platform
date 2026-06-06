with open(r'D:\桌面\毕设\exam-platform\frontend\src\views\paper\QuestionViewPage.vue', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'qv-year' in line or 'qv-card-num-label' in line or ('第' in line and '题' in line):
        print(f'Line {i+1}: {repr(line.rstrip())}')
    if 'qv-card-num-tag' in line:
        # Show surrounding lines
        print(f'Line {i+1}: {repr(line.rstrip())}')
