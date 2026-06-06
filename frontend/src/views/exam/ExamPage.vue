<template>
  <div class="exam-page">
    <!-- Setup -->
    <div v-if="!started" class="exam-setup card">
      <h2>模拟考试</h2>
      <el-form :model="form" label-width="100px">
        <el-form-item label="选择科目">
          <el-select v-model="form.subjectId" placeholder="选择科目" size="large" style="width:100%">
            <el-option v-for="s in subjects" :key="s.id" :label="s.name" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="题目数量">
          <el-slider v-model="form.questionCount" :min="10" :max="50" :step="5" show-input />
        </el-form-item>
        <el-form-item label="考试时长">
          <el-select v-model="form.timeLimit" size="large" style="width:100%">
            <el-option label="30 分钟" :value="30" />
            <el-option label="45 分钟" :value="45" />
            <el-option label="60 分钟" :value="60" />
            <el-option label="90 分钟" :value="90" />
            <el-option label="120 分钟" :value="120" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="large" @click="startExam" :loading="starting">
            开始考试
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- Exam In Progress -->
    <div v-else class="exam-container">
      <div class="exam-header">
        <div class="timer" :class="{ warning: remainingTime < 300 }">
          ⏱️ {{ formatTime(remainingTime) }}
        </div>
        <div class="progress-text">
          {{ currentIndex + 1 }} / {{ questions.length }}
        </div>
        <el-button type="danger" @click="submitExam" :loading="submitting">交卷</el-button>
      </div>

      <div class="question-card card">
        <el-tag>{{ typeLabel }}</el-tag>
        <div class="q-content"><img v-if="currentQuestion?.image" :src="currentQuestion.image" style="max-width:100%;margin:8px 0;border-radius:6px" /><div v-html="currentQuestion?.content"></div></div>

        <div class="q-options" v-if="['SINGLE', 'MULTI'].includes(currentQuestion?.type)">
          <div v-for="opt in parsedOptions" :key="opt.key"
            class="option-item" :class="{ selected: isSelected(opt.key) }"
            @click="selectOption(opt.key)">
            <span class="option-key">{{ opt.key }}</span>
            <span class="option-value"><span v-html="opt.value"></span></span>
          </div>
        </div>

        <div class="q-options" v-if="currentQuestion?.type === 'JUDGE'">
          <div v-for="opt in [{key:'T',value:'正确'},{key:'F',value:'错误'}]" :key="opt.key"
            class="option-item" :class="{ selected: selectedAnswer === opt.key }"
            @click="selectOption(opt.key)">
            <span class="option-key">{{ opt.key === 'T' ? '✓' : '✗' }}</span>
            <span class="option-value"><span v-html="opt.value"></span></span>
          </div>
        </div>

        <div v-if="currentQuestion?.type === 'FILL'" class="fill-input">
          <el-input v-model="selectedAnswer" placeholder="请输入答案" size="large" />
        </div>

        <div class="nav-buttons">
          <el-button v-if="currentIndex > 0" @click="prevQuestion">上一题</el-button>
          <el-button type="primary" v-if="currentIndex < questions.length - 1" @click="nextQuestion">下一题</el-button>
          <el-button type="success" v-if="currentIndex === questions.length - 1" @click="submitExam" :loading="submitting">交卷</el-button>
        </div>
      </div>

      <div class="question-nav">
        <div v-for="(q, i) in questions" :key="i"
          class="q-dot"
          :class="{ active: i === currentIndex, answered: answers[i] !== undefined }"
          @click="currentIndex = i; loadAnswer(i)">
          {{ i + 1 }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const subjects = ref<any[]>([])
const started = ref(false)
const starting = ref(false)
const submitting = ref(false)
const form = ref({ subjectId: 1, questionCount: 20, timeLimit: 60 })

const questions = ref<any[]>([])
const answers = ref<Record<number, string>>({})
const currentIndex = ref(0)
const examId = ref(0)
const remainingTime = ref(0)
let timer: any = null

const currentQuestion = computed(() => questions.value[currentIndex.value] || null)

const typeLabel = computed(() => {
  const map: any = { SINGLE: '单选题', MULTI: '多选题', JUDGE: '判断题', FILL: '填空题', COMPREHENSIVE: '综合题' }
  return map[currentQuestion.value?.type] || ''
})

const parsedOptions = computed(() => {
  if (!currentQuestion.value?.options) return []
  try {
    return typeof currentQuestion.value.options === 'string'
      ? JSON.parse(currentQuestion.value.options) : currentQuestion.value.options
  } catch { return [] }
})

const selectedAnswer = computed({
  get: () => answers.value[currentIndex.value] || '',
  set: (val) => { answers.value[currentIndex.value] = val }
})

onMounted(async () => {
  const res: any = await api.get('/subjects')
  if (res.code === 200) subjects.value = res.data
})

async function startExam() {
  starting.value = true
  try {
    const res: any = await api.post('/practice/exam/start', form.value)
    if (res.code === 200) {
      examId.value = res.data.examId
      questions.value = res.data.questions
      remainingTime.value = form.value.timeLimit * 60
      started.value = true
      startTimer()
    }
  } catch {} finally { starting.value = false }
}

function startTimer() {
  timer = setInterval(() => {
    remainingTime.value--
    if (remainingTime.value <= 0) {
      clearInterval(timer)
      ElMessage.warning('考试时间到，自动交卷')
      handleTimeout()
    }
  }, 1000)
}

async function handleTimeout() {
  try {
    await api.post(`/practice/exam/${examId.value}/timeout`)
  } catch {}
  router.push(`/exam/result/${examId.value}`)
}

function isSelected(key: string) {
  const cur = answers.value[currentIndex.value] || ''
  if (currentQuestion.value?.type === 'MULTI') return cur.split(',').includes(key)
  return cur === key
}

function selectOption(key: string) {
  const cur = answers.value[currentIndex.value] || ''
  if (currentQuestion.value?.type === 'MULTI') {
    const sel = cur ? cur.split(',').filter((s: string) => s) : []
    const idx = sel.indexOf(key)
    if (idx >= 0) sel.splice(idx, 1)
    else sel.push(key)
    answers.value[currentIndex.value] = sel.sort().join(',')
  } else {
    answers.value[currentIndex.value] = key
  }
}

function loadAnswer(i: number) {
  // just switch view
}

function prevQuestion() {
  if (currentIndex.value > 0) currentIndex.value--
}

function nextQuestion() {
  if (currentIndex.value < questions.value.length - 1) currentIndex.value++
}

async function submitExam() {
  await ElMessageBox.confirm('确定要交卷吗？', '确认交卷', { confirmButtonText: '确定', cancelButtonText: '继续答题' })
  submitting.value = true
  try {
    // Submit all answers
    for (const q of questions.value) {
      const ans = answers.value[questions.value.indexOf(q)]
      if (ans !== undefined) {
        await api.post(`/practice/exam/${examId.value}/answer`, { questionId: q.id, answer: ans })
      }
    }
    await api.post(`/practice/exam/${examId.value}/submit`)
    clearInterval(timer)
    router.push(`/exam/result/${examId.value}`)
  } catch {} finally { submitting.value = false }
}

function formatTime(s: number) {
  const m = Math.floor(s / 60)
  const sec = s % 60
  return `${m.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`
}

onUnmounted(() => { if (timer) clearInterval(timer) })
</script>

<style scoped>
.exam-page { min-height: 100vh; background: var(--bg-color); }
.exam-setup { max-width: 500px; margin: 80px auto 0; padding: 32px; }
.exam-setup h2 { margin-bottom: 24px; }

.exam-container { max-width: 800px; margin: 0 auto; padding: 80px 20px 40px; }
.exam-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 20px; background: var(--card-bg); border-radius: 10px;
  margin-bottom: 20px; box-shadow: var(--shadow); position: sticky; top: 60px; z-index: 10;
}
.timer { font-size: 24px; font-weight: 700; font-variant-numeric: tabular-nums; }
.timer.warning { color: var(--danger-color); animation: pulse 1s infinite; }
@keyframes pulse { 50% { opacity: 0.5; } }

.question-card { padding: 28px; }
.q-content { font-size: 16px; line-height: 1.8; margin: 20px 0; padding: 16px; background: var(--bg-color); border-radius: 8px; }

.q-options { display: flex; flex-direction: column; gap: 10px; margin-bottom: 24px; }
.option-item {
  display: flex; align-items: center; gap: 12px; padding: 12px 16px;
  border: 2px solid var(--border-color); border-radius: 8px; cursor: pointer; transition: all 0.2s;
  background: #fff !important;
}
.option-item:hover { border-color: var(--primary-color); }
.option-item.selected { border-color: var(--primary-color) !important; background: #fff !important; }
.option-key { width: 30px; height: 30px; border-radius: 50%; background: var(--bg-color); display: flex; align-items: center; justify-content: center; font-weight: 700; flex-shrink: 0; }

.fill-input { margin-bottom: 24px; }

.nav-buttons { display: flex; gap: 12px; justify-content: center; }

.question-nav { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 20px; padding: 16px; background: var(--card-bg); border-radius: 10px; }
.q-dot {
  width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 600; cursor: pointer; border: 2px solid var(--border-color);
  background: var(--bg-color); transition: all 0.2s;
}
.q-dot.active { border-color: var(--primary-color); background: var(--primary-light); }
.q-dot.answered { border-color: var(--success-color); background: #f0f9eb; }
</style>
