with open(r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and fix line 485
for i, line in enumerate(lines):
    if 'ElMessage.success(练习完成' in line:
        print(f'Line {i+1} BEFORE: {line.rstrip()}')
        lines[i] = '      ElMessage.success(练习完成！正确率 %)\n'
        print(f'Line {i+1} AFTER:  {lines[i].rstrip()}')

with open(r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Fixed!')
