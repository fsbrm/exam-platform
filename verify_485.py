with open(r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f.readlines()):
        if 'ElMessage.success' in line and '练习' in line:
            print(f'Line {i+1}: {repr(line.rstrip())}')
