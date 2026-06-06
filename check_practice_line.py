with open(r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(105, 115):
    print(f'{i+1}: {lines[i].rstrip()}')
