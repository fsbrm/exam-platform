with open(r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue', 'r', encoding='utf-8') as f:
    current = f.read()

# The current file has template but no script/style
# I need to append the script and style

script = '''
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const viewMode = ref('list')
const questions = ref<any[]>([])
const currentIndex = ref(0)
const selectedAnswer = ref('')
const showResult = ref(false)
const lastCorrect = ref(false)
const correctAnswer = ref('')
const answeredCount = ref(0)
const correctCount = ref(0)
const isFavorited = ref(false)
const currentMastery = ref<'' | 'mastered' | 'unfamiliar' | 'dontknow'>('')
const submittedMap = ref<Set<number>>(new Set())

const currentQuestion = computed(() => questions.value[currentIndex.value] || null)

const choiceQuestions = computed(() => questions.value.filter((q: any) => q.type !== 'COMPREHENSIVE'))

const progressPercent = computed(() =>
  questions.value.length > 0 ? Math.round((currentIndex.value + 1) / questions.value.length * 100) : 0
)

const correctPercent = computed(() =>
  answeredCount.value > 0 ? Math.round(correctCount.value / answeredCount.value * 100) : 0
)

const progressColor = computed(() => {
  if (correctPercent.value >= 80) return '#67c23a'
  if (correctPercent.value >= 60) return '#e6a23c'
  return '#f56c6c'
})

const canSubmit = computed(() => {
  if (!currentQuestion.value) return false
  if (currentQuestion.value.type === 'COMPREHENSIVE') return false
  if (currentQuestion.value.type === 'FILL') return selectedAnswer.value.trim().length > 0
  return selectedAnswer.value.length > 0
})

const typeLabel = computed(() => {
  const map: any = { SINGLE: '单选题', MULTI: '多选题', JUDGE: '判断题', FILL: '填空题', COMPREHENSIVE: '综合题' }
  return map[currentQuestion.value?.type] || ''
})

const typeTagType = computed(() => {
  const map: any = { SINGLE: '', MULTI: 'warning', JUDGE: 'info', FILL: 'success', COMPREHENSIVE: 'danger' }
  return map[currentQuestion.value?.type] || ''
})

const diffLabel = computed(() => {
  const map: any = { EASY: '简单', MEDIUM: '中等', HARD: '困难' }
  return map[currentQuestion.value?.difficulty] || ''
})

const diffTagType = computed(() => {
  const map: any = { EASY: 'success', MEDIUM: 'warning', HARD: 'danger' }
  return map[currentQuestion.value?.difficulty] || 'info'
})

const parsedOptions = computed(() => {
  if (!currentQuestion.value?.options) return []
  try {
    const opts = typeof currentQuestion.value.options === 'string'
      ? JSON.parse(currentQuestion.value.options) : currentQuestion.value.options
    return Array.isArray(opts) ? opts : []
  } catch { return [] }
})

const renderedContent = computed(() => {
  const c = currentQuestion.value?.content || ''
  if (currentQuestion.value?.image) {
    const img = `<img src="${currentQuestion.value.image}" style="max-width:100%;margin:8px 0;border-radius:6px" />`
    return img + c
  }
  return c
})

function renderText(text: string) {
  if (!text) return ''
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\\n/g, '<br>')
}

function parsedListOptions(q: any) {
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

function loadAnswer(idx: number) {
  if (idx < 0 || idx >= questions.value.length) return
  const q = questions.value[idx]
  currentIndex.value = idx
  selectedAnswer.value = q._selected || ''
  showResult.value = !!q._submitted
  if (q._submitted) {
    lastCorrect.value = !!q._correct
    correctAnswer.value = q._answer || q.answer || ''
  }
}

onMounted(async () => {
  const chapterId = route.query.chapterId
  const subjectId = route.query.subjectId
  const knowledgeId = route.query.knowledgeId
  const random = route.query.random
  const from = route.query.from

  if (from === 'knowledge') viewMode.value = 'list'

  try {
    if (knowledgeId) {
      const res: any = await api.get('/questions/practice', { params: { knowledgeId, count: 50 } })
      if (res.code === 200) questions.value = initState(res.data)
    } else if (chapterId) {
      const res: any = await api.get('/questions/practice', { params: { chapterId, count: 50 } })
      if (res.code === 200) questions.value = initState(res.data)
    } else if (subjectId) {
      const res: any = await api.get('/questions/practice', { params: { subjectId, count: 50 } })
      if (res.code === 200) questions.value = initState(res.data)
    } else if (random === 'true' && subjectId) {
      const res: any = await api.get('/questions/random', { params: { subjectId, count: 20 } })
      if (res.code === 200) questions.value = initState(res.data)
    }
  } catch (e) {
    ElMessage.error('加载题目失败')
  } finally {
    loading.value = false
  }
  loadMastery()
})

function initState(data: any[]) {
  return (data || []).map((q: any) => ({
    ...q,
    _selected: null,
    _submitted: false,
    _correct: null
  }))
}

function isSelected(key: string) {
  if (currentQuestion.value?.type === 'MULTI') {
    return selectedAnswer.value.split(',').includes(key)
  }
  return selectedAnswer.value === key
}

function selectOption(key: string) {
  if (showResult.value) return
  if (currentQuestion.value?.type === 'MULTI') {
    const selected = selectedAnswer.value ? selectedAnswer.value.split(',').filter((s: string) => s) : []
    const idx = selected.indexOf(key)
    if (idx >= 0) selected.splice(idx, 1)
    else selected.push(key)
    selectedAnswer.value = selected.join(',')
  } else {
    selectedAnswer.value = key
  }
}

async function submitAnswer() {
  if (!currentQuestion.value || !selectedAnswer.value) return
  try {
    const res: any = await api.post('/practice/submit', {
      questionId: currentQuestion.value.id,
      answer: selectedAnswer.value
    })
    if (res.code === 200) {
      lastCorrect.value = res.data.isCorrect
      correctAnswer.value = res.data.answer || currentQuestion.value.answer
      showResult.value = true
      const q = questions.value[currentIndex.value]
      q._submitted = true
      q._correct = res.data.isCorrect
      q._selected = selectedAnswer.value
      q._answer = res.data.answer
      answeredCount.value++
      if (res.data.isCorrect) correctCount.value++
    }
  } catch {}
}

function prevQuestion() {
  if (currentIndex.value > 0) {
    currentIndex.value--
    resetState()
  }
}

function nextQuestion() {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
    resetState()
  }
}

function resetState() {
  selectedAnswer.value = ''
  showResult.value = false
}

function finishPractice() {
  ElMessage.success(`练习完成！正确率 ${correctPercent.value}%`)
  router.back()
}

function openAiChat() {
  router.push(`/ai?question=${encodeURIComponent(currentQuestion.value.content)}&id=${currentQuestion.value.id}`)
}

async function loadMastery() {
  if (!questions.value.length) return
  const qids = questions.value.map((q: any) => q.id)
  try {
    const res: any = await api.post('/mastery/batch', { questionIds: qids })
    if (res.code === 200 && res.data) {
      const map: any = {}
      for (const m of res.data) map[m.questionId] = m.level
      for (const q of questions.value) {
        q._mastery = map[q.id] || ''
      }
    }
  } catch {}
  if (questions.value[currentIndex.value]) {
    currentMastery.value = questions.value[currentIndex.value]._mastery || ''
  }
}

async function markMastery(level: 'mastered' | 'unfamiliar' | 'dontknow') {
  if (!currentQuestion.value) return
  try {
    await api.post('/mastery/mark', { questionId: currentQuestion.value.id, level })
    currentMastery.value = level
    const q = questions.value[currentIndex.value]
    q._mastery = level
    const labels: any = { mastered: '已标记为掌握', unfamiliar: '已标记为不熟', dontknow: '已标记为不会' }
    ElMessage.success(labels[level] || '标记成功')
  } catch {}
}

async function toggleFavorite() {
  if (!currentQuestion.value) return
  try {
    if (isFavorited.value) {
      await api.delete(`/favorites/${currentQuestion.value.id}`)
      isFavorited.value = false
      ElMessage.success('已取消收藏')
    } else {
      await api.post('/favorites', { questionId: currentQuestion.value.id })
      isFavorited.value = true
      ElMessage.success('已收藏')
    }
  } catch {}
}

function goBack() {
  router.back()
}
</script>

<style scoped>
.practice-page { min-height: 100vh; background: #f5f7fa; }
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
.pl-content :deep(img) { max-width: 100%; height: auto; border-radius: 6px; }
.pl-options { display: flex; flex-direction: column; gap: 8px; }
.pl-opt { display: flex; align-items: center; gap: 12px; padding: 10px 14px; border: 2px solid #e5e7eb; border-radius: 8px; cursor: pointer; transition: all 0.15s; }
.pl-opt:hover:not(.correct):not(.wrong) { border-color: #93c5fd; }
.pl-opt.selected { border-color: #4f7cff !important; }
.pl-opt.correct { border-color: #52c41a; background: #f6ffed; }
.pl-opt.wrong { border-color: #ff4d4f; background: #fff2f0; }
.pl-opt-key { width: 28px; height: 28px; border-radius: 50%; background: #f3f4f6; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px; }
.pl-opt.correct .pl-opt-key { background: #52c41a; color: white; }
.pl-opt.wrong .pl-opt-key { background: #ff4d4f; color: white; }
.pl-opt-val { font-size: 14px; }
.pl-actions { margin-top: 12px; display: flex; gap: 8px; }

.loading-box { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 120px 0; }
.loading-box p { margin-top: 16px; color: #9ca3af; }
.empty-box { max-width: 400px; margin: 80px auto; text-align: center; }
.practice-container { max-width: 1200px; margin: 0 auto; padding: 24px 20px 40px; }
.progress-bar { margin-bottom: 24px; }
.progress-info { display: flex; justify-content: space-between; margin-top: 8px; font-size: 13px; color: #9ca3af; }

/* 3-Column Single Mode Layout */
.single-layout { display: grid; grid-template-columns: 180px 1fr 180px; gap: 16px; height: calc(100vh - 100px); }

/* Left Nav */
.sl-nav { background: white; border-radius: 12px; padding: 16px; overflow-y: auto; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.sl-nav-title { font-size: 13px; font-weight: 600; color: #6b7280; margin-bottom: 12px; }
.sl-nav-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 5px; }
.sl-nav-num { width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; background: #f3f4f6; color: #6b7280; transition: all 0.15s; }
.sl-nav-num:hover { background: #e0e7ff; color: #4f7cff; }
.sl-nav-num.active { background: #4f7cff; color: white; }
.sl-nav-num.done { background: #dbeafe; color: #4f7cff; }
.sl-nav-num.correct { background: #c8e6c9; color: #2e7d32; }
.sl-nav-num.wrong { background: #ffd6d6; color: #c62828; }
.sl-nav-legend { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 6px; font-size: 10px; color: #9ca3af; }
.sln-dot { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 2px; vertical-align: middle; }
.sln-dot.done { background: #dbeafe; }
.sln-dot.correct { background: #c8e6c9; }
.sln-dot.wrong { background: #ffd6d6; }

/* Center */
.sl-main { overflow-y: auto; }
.sl-q-card { background: white; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.sl-q-header { display: flex; align-items: center; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
.sl-q-num { font-size: 13px; color: #6b7280; font-weight: 500; margin: 0 8px; }
.back-btn { flex-shrink: 0; }
.mastery-btns { display: flex; gap: 4px; margin-left: auto; }
.fav-btn { margin-left: auto; }

.sl-q-content { font-size: 16px; line-height: 1.8; margin-bottom: 20px; padding: 16px; background: #f9fafb; border-radius: 8px; }
.sl-q-content :deep(img) { max-width: 100%; height: auto; border-radius: 8px; }

.sl-options { display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; }
.sl-opt { display: flex; align-items: center; gap: 12px; padding: 12px 16px; border: 2px solid #e5e7eb; border-radius: 10px; cursor: pointer; transition: all 0.15s; background: white; }
.sl-opt:hover:not(.disabled) { border-color: #93c5fd; background: #eff6ff; }
.sl-opt.selected { border-color: #4f7cff; background: #eff6ff; }
.sl-opt.correct { border-color: #52c41a; background: #f6ffed; }
.sl-opt.wrong { border-color: #ff4d4f; background: #fff2f0; }
.sl-opt.disabled { cursor: default; }
.sl-opt-key { width: 30px; height: 30px; border-radius: 50%; background: #f3f4f6; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px; flex-shrink: 0; }
.sl-opt.correct .sl-opt-key { background: #52c41a; color: white; }
.sl-opt.wrong .sl-opt-key { background: #ff4d4f; color: white; }
.sl-opt-val { font-size: 15px; }
.sl-fill { margin-bottom: 20px; }

.sl-result { padding: 16px; border-radius: 10px; margin-bottom: 20px; }
.sl-result.ok { background: #f6ffed; border: 1px solid #b7eb8f; }
.sl-result.err { background: #fff2f0; border: 1px solid #ffccc7; }
.sl-result-hd { font-size: 16px; font-weight: 600; margin-bottom: 6px; }
.sl-result-body { font-size: 14px; line-height: 1.7; color: #374151; }

.sl-actions { display: flex; gap: 12px; justify-content: center; }

/* Right Sheet */
.sl-sheet { background: white; border-radius: 12px; padding: 16px; overflow-y: auto; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.sl-sheet-title { font-size: 13px; font-weight: 600; color: #6b7280; margin-bottom: 12px; }
.sl-sheet-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 5px; }
.sl-sheet-cell { width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; border-radius: 4px; font-size: 11px; font-weight: 600; cursor: pointer; background: #f3f4f6; color: #9ca3af; transition: all 0.15s; }
.sl-sheet-cell:hover { background: #e0e7ff; color: #4f7cff; }
.sl-sheet-cell.active { border: 2px solid #4f7cff; color: #4f7cff; background: white; }
.sl-sheet-cell.done { background: #dbeafe; color: #4f7cff; }
.sl-sheet-cell.correct { background: #c8e6c9; color: #2e7d32; }
.sl-sheet-cell.wrong { background: #ffd6d6; color: #c62828; }
.sl-sheet-legend { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 6px; font-size: 10px; color: #9ca3af; }
.ssl-dot { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 2px; vertical-align: middle; }
.ssl-dot.active { border: 2px solid #4f7cff; background: white; }
.ssl-dot.done { background: #dbeafe; }
.ssl-dot.correct { background: #c8e6c9; }
.ssl-dot.wrong { background: #ffd6d6; }

@media (max-width: 900px) {
  .single-layout { grid-template-columns: 1fr; }
  .sl-nav, .sl-sheet { display: none; }
}
</style>
'''

# Write the complete file
with open(r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue', 'w', encoding='utf-8') as f:
    f.write(current + script)

print('Full file rebuilt!')
print(f'Total chars: {len(current + script)}')
