fp = r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue'
with open(fp, 'r', encoding='utf-8') as f:
    c = f.read()

# Add "view answer" button in single mode - show when not submitted
old_sl_btn = '''<el-button v-if="!showResult && canSubmit" type="primary" size="large" @click="submitAnswer">提交答案</el-button>'''
new_sl_btn = '''<el-button v-if="!showResult && canSubmit" type="primary" size="large" @click="submitAnswer">提交答案</el-button>
              <el-button v-if="!showResult" size="large" type="warning" plain @click="viewSingleAnswer">🔑 查看答案</el-button>'''

c = c.replace(old_sl_btn, new_sl_btn)

# Add viewSingleAnswer function
old_vs = "function cycleSingleHint() {"
new_vs = """function viewSingleAnswer() {
  const q = questions.value[currentIndex.value]
  correctAnswer.value = q.answer
  showResult.value = true
  lastCorrect.value = false
  q._submitted = true
  q._correct = null
  q._showAnswer = true
}

function cycleSingleHint() {"""
c = c.replace(old_vs, new_vs)

# Update result header to show "view answer" mode
old_rh = '''<span>{{ lastCorrect ? '✅ 回答正确！' : '❌ 回答错误' }}</span>
                <span v-if="!lastCorrect" style="margin-left:8px">正确答案：<strong>{{ correctAnswer }}</strong></span>'''
new_rh = '''<span v-if="currentQuestion?._showAnswer" style="color:#4f7cff">🔑 正确答案：<strong>{{ correctAnswer }}</strong></span>
                <span v-else-if="lastCorrect">✅ 回答正确！</span>
                <span v-else>❌ 回答错误 <span style="margin-left:8px">正确答案：<strong>{{ correctAnswer }}</strong></span></span>'''

c = c.replace(old_rh, new_rh)

with open(fp, 'w', encoding='utf-8') as f:
    f.write(c)
print('Done')
