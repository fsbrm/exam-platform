filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old = 'ElMessage.success(\u7ec3\u4e60\u5b8c\u6210\uff01\u6b63\u786e\u7387 %)'
new = 'ElMessage.success(`\u7ec3\u4e60\u5b8c\u6210\uff01\u6b63\u786e\u7387 ${correctPercent.value}%`)'

if old in content:
    content = content.replace(old, new)
    print('Replaced!')
else:
    # Try to find the actual line
    for line in content.split('\n'):
        if 'ElMessage.success' in line and '练习' in line:
            print(f'Found: {repr(line)}')
            break

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
