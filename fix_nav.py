filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix single mode navigation - always show both buttons
old_actions = '''            <div class="sl-actions">
              <el-button @click="prevQuestion" :disabled="currentIndex === 0" size="large"><el-icon><ArrowLeft /></el-icon>上一题</el-button>
              <el-button v-if="!showResult && canSubmit" type="primary" size="large" @click="submitAnswer">提交答案</el-button>
              <el-button v-if="showResult && currentIndex < questions.length - 1" type="primary" size="large" @click="nextQuestion">下一题<el-icon><ArrowRight /></el-icon></el-button>
              <el-button v-if="showResult && currentIndex === questions.length - 1" type="success" size="large" @click="finishPractice">完成练习</el-button>
              <el-button v-if="showResult" @click="openAiChat">🤖 AI帮我分析</el-button>
            </div>'''

new_actions = '''            <div class="sl-actions">
              <el-button @click="prevQuestion" :disabled="currentIndex === 0" size="large"><el-icon><ArrowLeft /></el-icon>上一题</el-button>
              <el-button v-if="!showResult && canSubmit" type="primary" size="large" @click="submitAnswer">提交答案</el-button>
              <el-button v-if="showResult" type="primary" size="large" @click="goNextOrFinish">{{ currentIndex < questions.length - 1 ? '下一题' : '完成练习' }}<el-icon v-if="currentIndex < questions.length - 1"><ArrowRight /></el-icon></el-button>
              <el-button v-if="showResult" @click="openAiChat">🤖 AI帮我分析</el-button>
            </div>'''

content = content.replace(old_actions, new_actions)

# Add goNextOrFinish function
old_func = "function finishPractice() {"
new_func = """function goNextOrFinish() {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
    resetState()
  } else {
    ElMessage.success(练习完成！正确率 %)
    router.back()
  }
}

function finishPractice() {"""

content = content.replace(old_func, new_func)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Navigation fixed!')
