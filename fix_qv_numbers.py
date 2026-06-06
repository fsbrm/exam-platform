fp = r'D:\桌面\毕设\exam-platform\frontend\src\views\paper\QuestionViewPage.vue'
with open(fp, 'r', encoding='utf-8') as f:
    c = f.read()

# Fix 1: Remove bad fallbacks in display - use question_number only
c = c.replace(
    "{{ question.questionNumber || question.question_number || question.chapterId }}",
    "{{ question.questionNumber || question.question_number }}"
)

# Fix 2: Fix the year label to show proper format
c = c.replace(
    "{{ question.year || paperYear }}骞?路 绗?{{ question.questionNumber || question.question_number || question.chapterId }} 棰?",
    "{{ question.year || paperYear }}骞?路 绗?{{ question.questionNumber || question.question_number }} 棰?"
)

# Fix 3: Remove bad fallback in loadQuestion
c = c.replace(
    "q.questionNumber = q.questionNumber || q.question_number || q.chapterId",
    "q.questionNumber = q.questionNumber || q.question_number || null"
)

# Fix 4: Fix the list item number
c = c.replace(
    "{{ q.questionNumber || (i+1) }}",
    "{{ q.question_number || q.questionNumber || (i+1) }}"
)

# Fix 5: Remove bad fallback in allQuestions mapping
c = c.replace(
    "questionNumber: x.question_number || x.id,",
    "questionNumber: x.question_number || null,"
)

with open(fp, 'w', encoding='utf-8') as f:
    f.write(c)
print('QuestionViewPage fixed')
