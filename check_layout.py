with open(r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue', 'r', encoding='utf-8') as f:
    content = f.read()

# Check for the single layout structure
if 'single-layout' in content:
    idx = content.index('single-layout')
    print(content[idx:idx+200])
    print('---')
    
# Check media query
if '@media' in content:
    idx2 = content.index('@media')
    print(content[idx2:idx2+200])
    
# Check for common issues
print(f'\nContains viewMode=: {"viewMode===" in content}')
print(f'Contains single: {"single" in content}')
