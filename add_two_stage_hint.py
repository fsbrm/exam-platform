filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# =============================================
# 1. Update list mode hint - two stage
# =============================================
old_list_hint = '''          <!-- Hint -->
          <div v-if="q._showHint" class="pl-hint">
            <span class="pl-hint-icon">💡</span> {{ q._hint || '请仔细审题，注意排除干扰选项，结合知识点分析。' }}
          </div>'''

new_list_hint = '''          <!-- Two-stage Hint -->
          <div v-if="q._hintLevel >= 1" class="pl-hint">
            <div class="pl-hint-stage">
              <span class="pl-hint-icon">💡</span>
              <span class="pl-hint-label">提示一</span>
            </div>
            <div class="pl-hint-text">请仔细审题，回忆相关知识点，先排除明显不符合题意的选项。</div>
          </div>
          <div v-if="q._hintLevel >= 2" class="pl-hint" style="background:#fff0f6;border-color:#ffadd2">
            <div class="pl-hint-stage">
              <span class="pl-hint-icon">🔍</span>
              <span class="pl-hint-label">提示二</span>
            </div>
            <div class="pl-hint-text">{{ getDetailedHint(q) }}</div>
          </div>'''

content = content.replace(old_list_hint, new_list_hint)

# =============================================
# 2. Update list mode hint button - cycle through levels
# =============================================
old_list_btn = '''            <el-button v-if="!q._submitted" size="small" plain @click="q._showHint = !q._showHint; if(!q._hint) q._hint='请仔细审题，注意排除干扰选项，结合知识点分析。'">💡 {{ q._showHint ? '隐藏提示' : '提示' }}</el-button>'''

new_list_btn = '''            <el-button v-if="!q._submitted" size="small" plain @click="cycleHint(q)">
              💡 {{ q._hintLevel === 0 ? '提示' : q._hintLevel === 1 ? '详细提示' : '隐藏提示' }}
            </el-button>'''

content = content.replace(old_list_btn, new_list_btn)

# =============================================
# 3. Add hint display + button in single mode
# =============================================
old_sl_actions = '''            <div class="sl-actions">
              <el-button @click="prevQuestion" :disabled="currentIndex === 0" size="large"><el-icon><ArrowLeft /></el-icon>上一题</el-button>
              <el-button v-if="!showResult && canSubmit" type="primary" size="large" @click="submitAnswer">提交答案</el-button>
              <el-button v-if="showResult" type="primary" size="large" @click="goNextOrFinish">{{ currentIndex < questions.length - 1 ? '下一题' : '完成练习' }}<el-icon v-if="currentIndex < questions.length - 1"><ArrowRight /></el-icon></el-button>
              <el-button v-if="showResult" @click="openAiChat">🤖 AI帮我分析</el-button>
            </div>'''

new_sl_actions = '''            <!-- Two-stage hint for single mode -->
            <div v-if="singleHintLevel >= 1" class="sl-hint">
              <div class="sl-hint-row"><span>💡</span> <strong>提示一：</strong>请仔细审题，回忆相关知识点，先排除明显不符合题意的选项。</div>
            </div>
            <div v-if="singleHintLevel >= 2" class="sl-hint" style="background:#fff0f6;border-color:#ffadd2">
              <div class="sl-hint-row"><span>🔍</span> <strong>提示二：</strong>{{ getDetailedHint(currentQuestion) }}</div>
            </div>

            <div class="sl-actions">
              <el-button @click="prevQuestion" :disabled="currentIndex === 0" size="large"><el-icon><ArrowLeft /></el-icon>上一题</el-button>
              <el-button v-if="!showResult && canSubmit" type="primary" size="large" @click="submitAnswer">提交答案</el-button>
              <el-button v-if="showResult" type="primary" size="large" @click="goNextOrFinish">{{ currentIndex < questions.length - 1 ? '下一题' : '完成练习' }}<el-icon v-if="currentIndex < questions.length - 1"><ArrowRight /></el-icon></el-button>
              <el-button v-if="!showResult" size="large" plain @click="cycleSingleHint">💡 {{ singleHintLevel === 0 ? '提示' : singleHintLevel === 1 ? '详细提示' : '隐藏' }}</el-button>
              <el-button v-if="showResult" @click="openAiChat">🤖 AI帮我分析</el-button>
            </div>'''

content = content.replace(old_sl_actions, new_sl_actions)

# =============================================
# 4. Add functions and state
# =============================================
old_ref = "const submittedMap = ref<Set<number>>(new Set())"
new_ref = "const submittedMap = ref<Set<number>>(new Set())\nconst singleHintLevel = ref(0)"

content = content.replace(old_ref, new_ref)

# Add cycleHint function
old_cycle = "function resetListQuestion(q: any) {"
new_cycle = """function cycleHint(q: any) {
  if (!q._hintLevel) q._hintLevel = 0
  q._hintLevel = (q._hintLevel + 1) % 3
}

function cycleSingleHint() {
  singleHintLevel.value = (singleHintLevel.value + 1) % 3
}

function getDetailedHint(q: any) {
  const type = q.type
  if (type === 'SINGLE') return '本题为单选题，只有一个正确选项。请逐一分析每个选项，用排除法缩小范围，找到最符合题意的答案。'
  if (type === 'MULTI') return '本题为多选题，有多个正确选项。请仔细分析每个选项是否符合题意，注意不要遗漏或误选。'
  return '请结合题目中的关键条件和所学知识点，逐步推理得出答案。'
}

function resetListQuestion(q: any) {"""

content = content.replace(old_cycle, new_cycle)

# Update initState to include _hintLevel
old_init_state = "    _showHint: false,\n    _hint: null,"
new_init_state = "    _hintLevel: 0,"

content = content.replace(old_init_state, new_init_state)

# Update resetState to reset hint
old_reset = """function resetState() {
  selectedAnswer.value = ''
  showResult.value = false
}"""

new_reset = """function resetState() {
  selectedAnswer.value = ''
  showResult.value = false
  singleHintLevel.value = 0
}"""

content = content.replace(old_reset, new_reset)

# =============================================
# 5. Add CSS for hint in single mode
# =============================================
old_css = ".sl-actions { display: flex; gap: 12px; justify-content: center; }"
new_css = """.sl-hint { margin-bottom: 12px; padding: 12px 16px; background: #fffbe6; border: 1px solid #ffe58f; border-radius: 10px; font-size: 14px; line-height: 1.7; color: #8c6d00; }
.sl-hint-row { display: flex; align-items: flex-start; gap: 6px; }
.sl-actions { display: flex; gap: 12px; justify-content: center; }"""

content = content.replace(old_css, new_css)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Two-stage hint added!')
