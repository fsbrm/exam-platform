import os

file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "src", "views", "practice", "PracticePage.vue"))
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# The current PracticePage has one-at-a-time mode. I'll add a stacked list mode.
# Replace the main template to support both modes, defaulting to list mode.

# Look for the practice-container div
old_container = '<div v-else class="practice-container">'

new_container = '''<div v-else class="practice-container">
      <!-- Mode Toggle -->
      <div class="practice-mode-bar">
        <el-radio-group v-model="viewMode" size="small">
          <el-radio-button value="list">列表模式</el-radio-button>
          <el-radio-button value="single">单题模式</el-radio-button>
        </el-radio-group>
        <span class="pm-info">{{ questions.length }} 道题目</span>
      </div>

      <!-- LIST MODE: All questions stacked vertically -->
      <div v-if="viewMode === 'list'" class="practice-list">
        <div v-for="(q, qi) in questions" :key="q.id" class="pl-card" :id="'q-'+q.id">
          <div class="pl-card-hd">
            <span class="pl-num">第 {{ qi+1 }} 题</span>
            <el-tag size="small">{{ q.difficulty === 'EASY' ? '简单' : q.difficulty === 'MEDIUM' ? '中等' : '困难' }}</el-tag>
            <span v-if="q._submitted" class="pl-result" :class="q._correct ? 'ok' : 'err'">
              {{ q._correct ? '✓ 做对' : '✗ 做错' }}
            </span>
          </div>
          <div class="pl-content">{{ q.content }}</div>
          <div class="pl-options" v-if="parsedListOptions(q).length">
            <div v-for="opt in parsedListOptions(q)" :key="opt.key"
              class="pl-opt"
              :class="{
                selected: q._selected === opt.key && !q._submitted,
                correct: q._submitted && (opt.key === q.answer || q._answer),
                wrong: q._submitted && q._selected === opt.key && opt.key !== q.answer
              }"
              @click="selectListOption(q, opt.key)">
              <span class="pl-opt-key">{{ opt.key }}</span>
              <span class="pl-opt-val">{{ opt.value }}</span>
            </div>
          </div>
          <div class="pl-actions">
            <el-button v-if="!q._submitted && q._selected" type="primary" size="small" @click="submitListAnswer(q, qi)">提交</el-button>
            <el-button v-if="q._submitted" size="small" @click="resetListQuestion(q)">重做</el-button>
          </div>
        </div>
      </div>'''

content = content.replace(old_container, new_container)

# Add viewMode ref
old_refs = 'const loading = ref(true)'
new_refs = 'const loading = ref(true)\nconst viewMode = ref(\'list\')'
content = content.replace(old_refs, new_refs)

# Replace old single-mode content section
old_single = '''<div class="question-card card" v-if="currentQuestion">'''

new_single = '''<!-- SINGLE MODE -->
      <div v-if="viewMode === 'single'" class="question-card card" v-if="currentQuestion">'''

content = content.replace(old_single.replace('\\', '\\\\'), new_single)

# Add list mode helper functions before the existing onMounted
old_onmounted = 'onMounted(async () => {'
new_helpers = '''function parsedListOptions(q: any) {
  try {
    const opts = typeof q.options === 'string' ? JSON.parse(q.options) : q.options
    return Array.isArray(opts) ? opts : []
  } catch { return [] }
}

function selectListOption(q: any, key: string) {
  if (q._submitted) return
  q._selected = key
}

async function submitListAnswer(q: any, qi: number) {
  if (!q._selected) return
  try {
    const res: any = await api.post('/practice/submit', { questionId: q.id, answer: q._selected })
    if (res.code === 200) {
      q._submitted = true
      q._correct = res.data.isCorrect
      q._answer = res.data.answer
      answeredCount.value++
      if (q._correct) correctCount.value++
    }
  } catch {}
}

function resetListQuestion(q: any) {
  q._selected = null
  q._submitted = false
  q._correct = null
}

'''
content = content.replace(old_onmounted, new_helpers + old_onmounted)

# Update onMounted to init question state
old_mount_body = '''try {
    if (paperId) {'''
new_mount_body = '''try {
    // Initialize question state
    const initState = (list: any[]) => {
      return list.map((q: any) => ({
        ...q, _selected: null, _submitted: false, _correct: null, _answer: null
      }))
    }
    if (paperId) {'''

content = content.replace(old_mount_body, new_mount_body)

# Apply initState to questions
old_qs_assignment = 'questions.value = qs.map((q: any) => ({...q, id: q.id || q.questionId}))'
new_qs_assignment = 'questions.value = initState(qs.map((q: any) => ({...q, id: q.id || q.questionId})))'
content = content.replace(old_qs_assignment, new_qs_assignment)

# Also init state for other branches
content = content.replace(
  'if (res.code === 200) questions.value = res.data\n    } else if (random',
  'if (res.code === 200) questions.value = initState(res.data)\n    } else if (random'
)

content = content.replace(
  'if (res.code === 200) questions.value = res.data\n    } else if (subjectId) {',
  'if (res.code === 200) questions.value = initState(res.data)\n    } else if (subjectId) {'
)

# Add CSS for list mode
old_style_end = '.practice-page { min-height: 100vh; background: var(--bg-color); }'
new_style = '''.practice-page { min-height: 100vh; background: var(--bg-color); }
.practice-mode-bar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; padding: 0 4px; }
.pm-info { font-size: 13px; color: #9ca3af; }

/* List Mode */
.practice-list { display: flex; flex-direction: column; gap: 16px; }
.pl-card { background: white; border-radius: 12px; padding: 20px 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.pl-card-hd { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
.pl-num { font-size: 15px; font-weight: 700; color: #1f2937; }
.pl-result { font-size: 12px; padding: 2px 8px; border-radius: 8px; margin-left: auto; }
.pl-result.ok { background: #f6ffed; color: #52c41a; }
.pl-result.err { background: #fff2f0; color: #ff4d4f; }
.pl-content { font-size: 15px; line-height: 1.8; margin-bottom: 16px; padding: 12px; background: #f9fafb; border-radius: 8px; }
.pl-options { display: flex; flex-direction: column; gap: 8px; }
.pl-opt {
  display: flex; align-items: center; gap: 12px; padding: 10px 14px;
  border: 2px solid #e5e7eb; border-radius: 8px; cursor: pointer; transition: all 0.15s;
}
.pl-opt:hover:not(.correct):not(.wrong) { border-color: #93c5fd; background: #f8faff; }
.pl-opt.selected { border-color: #4f7cff; background: #eff6ff; }
.pl-opt.correct { border-color: #52c41a; background: #f6ffed; }
.pl-opt.wrong { border-color: #ff4d4f; background: #fff2f0; }
.pl-opt-key {
  width: 28px; height: 28px; border-radius: 50%; background: #f3f4f6;
  display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px;
}
.pl-opt.correct .pl-opt-key { background: #52c41a; color: white; }
.pl-opt.wrong .pl-opt-key { background: #ff4d4f; color: white; }
.pl-opt-val { font-size: 14px; }
.pl-actions { margin-top: 12px; display: flex; gap: 8px; }
'''

content = content.replace(old_style_end, new_style + old_style_end)

# Adjust container max-width for list mode
content = content.replace(
  '.practice-container { max-width: 800px; margin: 0 auto; padding: 80px 20px 40px; }',
  '.practice-container { max-width: 860px; margin: 0 auto; padding: 24px 20px 40px; }'
)

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
print("PracticePage: list + single mode with vertical layout")