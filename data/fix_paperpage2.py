file = r"D:\桌面\毕设\exam-platform\frontend\src\views\paper\PaperDetailPage.vue"
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# The answer sheet section: replace q. with q2. inside its block
# But we need to be careful - replace only the answer sheet v-for block
# Let me find the exact section and fix it

old_answer_sheet = '''          <div v-for="(q2, idx2) in questions" :key="'s'+q2.id"
            class="pd-s-cell"
            :class="{
              done: q.userAnswer,
              correct: q.userCorrect === true,
              wrong: q.userCorrect === false
            }">
            {{ q.questionNumber || q.question_number }}
          </div>'''

new_answer_sheet = '''          <div v-for="(q2, idx2) in questions" :key="'s'+q2.id"
            class="pd-s-cell"
            :class="{
              done: q2.userAnswer,
              correct: q2.userCorrect === true,
              wrong: q2.userCorrect === false
            }">
            {{ q2.questionNumber || q2.question_number }}
          </div>'''

content = content.replace(old_answer_sheet, new_answer_sheet)

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed answer sheet variable references")