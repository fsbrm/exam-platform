filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\exam\ExamPage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Add COMPREHENSIVE to typeLabel
old_tm = "const map: any = { SINGLE: '单选题', MULTI: '多选题', JUDGE: '判断题', FILL: '填空题' }"
new_tm = "const map: any = { SINGLE: '单选题', MULTI: '多选题', JUDGE: '判断题', FILL: '填空题', COMPREHENSIVE: '综合题' }"
content = content.replace(old_tm, new_tm)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('ExamPage.vue updated!')
