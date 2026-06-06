fp = r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue'
with open(fp, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Add list mode navigation buttons at the bottom
old_list_end = '''      </div>
      <div class="progress-bar">'''

new_list_end = '''        <!-- List mode navigation -->
        <div class="pl-nav-bar">
          <el-button @click="scrollToListPrev" :disabled="listScrollIdx <= 0" size="default"><el-icon><ArrowLeft /></el-icon>上一题</el-button>
          <span class="pl-nav-info">{{ listScrollIdx + 1 }} / {{ choiceQuestions.length }}</span>
          <el-button @click="scrollToListNext" :disabled="listScrollIdx >= choiceQuestions.length - 1" size="default">下一题<el-icon><ArrowRight /></el-icon></el-button>
        </div>
      </div>
      <div class="progress-bar">'''

c = c.replace(old_list_end, new_list_end)

# 2. Add listScrollIdx ref and functions
old_ref = "const submittedMap = ref<Set<number>>(new Set())"
new_ref = "const submittedMap = ref<Set<number>>(new Set())\nconst listScrollIdx = ref(0)"
c = c.replace(old_ref, new_ref)

# Add scroll functions
old_scroll = "function openVideoSearch(q: any) {"
new_scroll = """function scrollToListNext() {
  if (listScrollIdx.value < choiceQuestions.value.length - 1) {
    listScrollIdx.value++
    const el = document.getElementById('q-' + choiceQuestions.value[listScrollIdx.value]?.id)
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }
}

function scrollToListPrev() {
  if (listScrollIdx.value > 0) {
    listScrollIdx.value--
    const el = document.getElementById('q-' + choiceQuestions.value[listScrollIdx.value]?.id)
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }
}

function openVideoSearch(q: any) {"""

c = c.replace(old_scroll, new_scroll)

# 3. Add "view answer" button for SINGLE/MULTI questions (skip submission, show answer)
old_actions_end = '''            <el-button size="small" plain @click="toggleListFavorite(q)">
              {{ q._favorited ? '⭐ 已收藏' : '☆ 收藏' }}
            </el-button>
          </div>'''

new_actions_end = '''            <el-button v-if="!q._submitted" size="small" type="warning" plain @click="showListAnswer(q)">🔑 查看答案</el-button>
            <el-button size="small" plain @click="toggleListFavorite(q)">
              {{ q._favorited ? '⭐ 已收藏' : '☆ 收藏' }}
            </el-button>
          </div>'''

c = c.replace(old_actions_end, new_actions_end)

# 4. Add showListAnswer function
old_mlm = "async function markListMastery(q: any, level: string) {"
new_mlm = """function showListAnswer(q: any) {
  q._submitted = true
  q._correct = null  // didn't actually answer
  q._answer = q.answer  // show the correct answer
  q._showAnswer = true
}

async function markListMastery(q: any, level: string) {"""

c = c.replace(old_mlm, new_mlm)

# 5. Update answer display to handle "view answer" mode
old_ans_hd = '''            <div class="pl-answer-hd">
              <span :style="{color: q._correct ? '#52c41a' : '#ff4d4f', fontWeight:700}">
                {{ q._correct ? '✅ 回答正确' : '❌ 回答错误' }}
              </span>
              <span v-if="!q._correct" style="margin-left:8px">正确答案：<strong>{{ q._answer || q.answer }}</strong></span>
            </div>'''

new_ans_hd = '''            <div class="pl-answer-hd">
              <span v-if="q._showAnswer" :style="{color:'#4f7cff', fontWeight:700}">
                🔑 正确答案：<strong>{{ q._answer || q.answer }}</strong>
              </span>
              <span v-else :style="{color: q._correct ? '#52c41a' : '#ff4d4f', fontWeight:700}">
                {{ q._correct ? '✅ 回答正确' : '❌ 回答错误' }}
              </span>
              <span v-if="!q._correct && !q._showAnswer" style="margin-left:8px">正确答案：<strong>{{ q._answer || q.answer }}</strong></span>
            </div>'''

c = c.replace(old_ans_hd, new_ans_hd)

# 6. Add CSS for list nav bar
old_css_end = ".pl-actions { margin-top: 12px; display: flex; gap: 6px; flex-wrap: wrap; }"
new_css_end = """.pl-nav-bar { display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 20px; padding: 12px; background: white; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.pl-nav-info { font-size: 14px; font-weight: 600; color: #6b7280; min-width: 60px; text-align: center; }
.pl-actions { margin-top: 12px; display: flex; gap: 6px; flex-wrap: wrap; }"""

c = c.replace(old_css_end, new_css_end)

with open(fp, 'w', encoding='utf-8') as f:
    f.write(c)
print('Done')
