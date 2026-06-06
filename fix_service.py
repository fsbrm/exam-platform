fp = r'D:\桌面\毕设\exam-platform\backend\src\main\java\com\exam\service\impl\QuestionServiceImpl.java'
with open(fp, 'r', encoding='utf-8') as f:
    c = f.read()

# Fix the questionNumber assignment
old_line = 'vo.setQuestionNumber(q.getChapterId() != null ? q.getChapterId().intValue() : null);'
new_line = 'vo.setQuestionNumber(questionMapper.selectQuestionNumber(questionId));'
c = c.replace(old_line, new_line)
with open(fp, 'w', encoding='utf-8') as f:
    f.write(c)
print('QuestionServiceImpl updated')
