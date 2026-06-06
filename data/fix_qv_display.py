import os

file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "src", "views", "paper", "QuestionViewPage.vue"))
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix: use year and questionNumber from API, not id
# The card header shows question number tag + label
old_header = '''          <div class="qv-card-num">
            <span class="qv-card-num-tag">{{ question.questionNumber || question.question_number }}</span>
            <span class="qv-card-num-label">第 {{ question.questionNumber || question.question_number }} 题</span>
            <span class="qv-card-score">2 分</span>
          </div>'''

new_header = '''          <div class="qv-card-num">
            <span class="qv-card-num-tag">{{ question.questionNumber || question.question_number || question.chapterId }}</span>
            <span class="qv-card-num-label">{{ question.year || paperYear }}年 · 第 {{ question.questionNumber || question.question_number || question.chapterId }} 题</span>
            <span class="qv-card-score">2 分</span>
          </div>'''

content = content.replace(old_header, new_header)

# Fix the year display in topbar
old_year = '<span class="qv-year" v-if="question">{{ paperYear }}年真题</span>'
new_year = '<span class="qv-year" v-if="question">{{ question.year || paperYear }}年 · 第 {{ question.questionNumber || question.question_number || question.chapterId }} 题</span>'
content = content.replace(old_year, new_year)

# Fix the questionNumber mapping in loadQuestion
old_map = 'q.questionNumber = q.question_number || q.questionNumber || q.id'
new_map = 'q.questionNumber = q.questionNumber || q.question_number || q.chapterId'
content = content.replace(old_map, new_map)

# Fix paperYear assignment
old_py = 'paperYear.value = q.year || 0'
new_py = 'paperYear.value = q.year || 0'  # keep this
# Actually let's set question.year from API response 
# The API now returns year and questionNumber directly

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed QuestionViewPage display")