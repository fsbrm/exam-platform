with open(r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f.readlines()):
        if 'single' in line.lower() and ('v-if' in line or 'viewMode' in line):
            print(f'Line {i+1}: {line.rstrip()}')
        if 'v-if' in line and 'single' in line.lower():
            print(f'Line {i+1}: {line.rstrip()}')
