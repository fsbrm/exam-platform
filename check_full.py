with open(r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue', 'r', encoding='utf-8') as f:
    content = f.read()
# Check if it ends properly
if '</style>' in content:
    print('Has style section')
else:
    print('NO style section!')
if 'loadAnswer' in content:
    print('Has loadAnswer')
if 'choiceQuestions' in content:
    print('Has choiceQuestions')
if 'single-layout' in content:
    print('Has single-layout')
print(f'File length: {len(content)} chars')
