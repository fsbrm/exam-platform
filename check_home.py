filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\home\HomePage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f.readlines()):
        if 'practice' in line and 'subjectId' in line:
            print(f'Line {i+1}: {line.rstrip()}')
