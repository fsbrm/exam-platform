import re

# Fix ExamResult.vue
fp = r'D:\桌面\毕设\exam-platform\frontend\src\views\exam\ExamResult.vue'
with open(fp, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('{{ q.content }}', '<span v-html="q.content"></span>')
with open(fp, 'w', encoding='utf-8') as f:
    f.write(c)
print('ExamResult.vue fixed')

# Fix QuestionViewPage.vue  
fp2 = r'D:\桌面\毕设\exam-platform\frontend\src\views\paper\QuestionViewPage.vue'
with open(fp2, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('{{ (q.content || \'\').substring(0, 50) }}', '<span v-html="stripQvContent(q.content)"></span>')
c = c.replace('{{ question.content }}', '<div v-html="question.content"></div>')
with open(fp2, 'w', encoding='utf-8') as f:
    f.write(c)
print('QuestionViewPage.vue fixed')

# Fix WrongPage.vue
fp3 = r'D:\桌面\毕设\exam-platform\frontend\src\views\wrong\WrongPage.vue'
with open(fp3, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('{{ wq.questionContent }}', '<div v-html="wq.questionContent"></div>')
with open(fp3, 'w', encoding='utf-8') as f:
    f.write(c)
print('WrongPage.vue fixed')
