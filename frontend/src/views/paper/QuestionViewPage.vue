<template>
  <div class="qv-page">
    <!-- Top bar -->
    <div class="qv-topbar">
      <span class="qv-back" @click="goBack">&larr; 返回</span>
      <span class="qv-year" v-if="question">{{ question.year || paperYear }}年 · 第 {{ question.questionNumber || question.question_number }} 题</span>
      <div class="qv-nav">
        <el-button size="small" :disabled="!prevId" @click="goPrev">上一题</el-button>
        <span class="qv-pos">{{ currentIdx }} / {{ totalCount }}</span>
        <el-button size="small" :disabled="!nextId" @click="goNext">下一题</el-button>
      </div>
      <el-button size="small" type="primary" @click="toggleListMode">
        {{ listMode ? '单题模式' : '列表模式' }}
      </el-button>
    </div>

    <!-- List Mode -->
    <div v-if="listMode && allQuestions.length > 0" class="qv-list">
      <div v-for="(q, i) in allQuestions" :key="q.id" v-memo="[q.id, q._done, q._correct, q._mastery]"
        class="qv-list-item"
        :class="{ active: q.id === currentQid }"
        @click="jumpTo(i)">
        <span class="qv-li-num">{{ q.question_number || q.questionNumber || (i+1) }}</span>
        <span class="qv-li-content">{{ q._stripped }}</span>
        <span v-if="q._mastery" class="qv-li-mastery" :class="'m-'+q._mastery">{{ masteryLabel(q._mastery) }}</span>
      </div>
    </div>

    <!-- Single Question Card -->
    <div class="qv-card-wrap" v-if="question">
      <div class="qv-card">

        <!-- Header: number + score + tags -->
        <div class="qv-card-hd">
          <div class="qv-card-num">
            <span class="qv-card-num-tag">{{ question.questionNumber || question.question_number }}</span>
            <span class="qv-card-num-label">{{ question.year || paperYear }}年 · 第 {{ question.questionNumber || question.question_number }} 题</span>
            <span class="qv-card-score">2 分</span>
          </div>
          <div class="qv-card-tags">
            <el-tag :type="diffTag">{{ diffText }}</el-tag>
            <el-tag type="info" effect="plain">{{ typeText }}</el-tag>
            <el-tag v-if="mastery" :type="masteryTag">{{ masteryText }}</el-tag>
          </div>
        </div>

        <!-- Content -->
        <div class="qv-card-body">
          <div class="qv-content"><div v-html="question.content"></div></div>

          <!-- Options -->
          <div class="qv-options" v-if="parsedOptions.length">
            <div v-for="opt in parsedOptions" :key="opt.key"
              class="qv-opt"
              :class="{
                selected: selectedAnswer === opt.key && !showResult,
                correct: showResult && opt.key === question.answer,
                wrong: showResult && selectedAnswer === opt.key && opt.key !== question.answer
              }"
              @click="selectOption(opt.key)">
              <span class="qv-opt-key">{{ opt.key }}</span>
              <span class="qv-opt-val"><span v-html="opt.value"></span></span>
              <span v-if="showResult && opt.key === question.answer" class="qv-opt-mark ok">&#10003;</span>
              <span v-else-if="showResult && selectedAnswer === opt.key && opt.key !== question.answer" class="qv-opt-mark err">&#10007;</span>
            </div>
          </div>

          <!-- Result -->
          <div v-if="showResult" class="qv-result" :class="lastCorrect ? 'ok' : 'err'">
            <p><strong>{{ lastCorrect ? '✅ 回答正确！' : '❌ 回答错误' }}</strong></p>
            <p v-if="!lastCorrect">正确答案：<strong>{{ question.answer }}</strong></p>
            <div v-if="question.analysis" class="qv-analysis">
              <strong>解析：</strong>{{ question.analysis }}
            </div>
          </div>
        </div>

        <!-- Action Bar -->
        <div class="qv-actions">
          <div class="qv-act-left">
            <el-button v-if="!showResult && selectedAnswer" type="primary" @click="submitAnswer">提交答案</el-button>
            <el-button v-if="showResult" @click="resetQuestion">重做</el-button>
          </div>

          <div class="qv-act-right">
            <!-- Hint -->
            <el-button text @click="showHint = !showHint">💡 提示</el-button>
            <!-- Video -->
            <el-button text @click="showVideo = !showVideo">🎬 视频</el-button>
            <!-- Note -->
            <el-button text @click="showNote = !showNote">📝 笔记</el-button>
          </div>
        </div>

        <!-- Hint Panel -->
        <div v-if="showHint" class="qv-panel hint">
          <div class="qv-panel-hd">💡 解题提示</div>
          <p>本题考察{{ getKpNames() }}相关知识点。建议回顾教材对应章节，注意常见易错点。</p>
          <p class="qv-hint-more">（后续将接入AI智能提示）</p>
        </div>

        <!-- Video Panel -->
        <div v-if="showVideo" class="qv-panel video">
          <div class="qv-panel-hd">🎬 相关视频</div>
          <div class="qv-video-placeholder">
            <div class="qv-video-icon">▶</div>
            <p>408考研 · {{ getKpNames() }} · 知识点讲解</p>
            <el-button type="primary" size="small" round>
              <a :href="videoSearchUrl" target="_blank" style="color:white;text-decoration:none">前往B站观看</a>
            </el-button>
          </div>
        </div>

        <!-- Note Panel -->
        <div v-if="showNote" class="qv-panel note">
          <div class="qv-panel-hd">📝 笔记</div>
          <el-input v-model="noteContent" type="textarea" :rows="3" placeholder="记录你的解题思路、易错点..." />
          <div class="qv-note-actions">
            <el-button size="small" type="primary" @click="saveNote" :loading="noteSaving">保存笔记</el-button>
          </div>
        </div>

        <!-- Mastery Buttons -->
        <div class="qv-mastery">
          <span class="qv-mastery-label">掌握程度：</span>
          <el-button
            :type="mastery === 'mastered' ? 'success' : 'default'"
            size="small" round @click="setMastery('mastered')">
            ✅ 掌握
          </el-button>
          <el-button
            :type="mastery === 'unfamiliar' ? 'warning' : 'default'"
            size="small" round @click="setMastery('unfamiliar')">
            🤔 不熟
          </el-button>
          <el-button
            :type="mastery === 'dontknow' ? 'danger' : 'default'"
            size="small" round @click="setMastery('dontknow')">
            ❌ 不会
          </el-button>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="qv-loading">
      <p>加载中...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const question = ref<any>(null)
const allQuestions = ref<any[]>([])
const listMode = ref(false)
const currentQid = ref(0)
const selectedAnswer = ref('')
const showResult = ref(false)
const lastCorrect = ref(false)
const mastery = ref('')
const showHint = ref(false)
const showVideo = ref(false)
const showNote = ref(false)
const noteContent = ref('')
const noteSaving = ref(false)
const paperYear = ref(0)

const currentIdx = computed(() => {
  if (!allQuestions.value.length) return 0
  return allQuestions.value.findIndex((q: any) => q.id === currentQid.value) + 1
})
const totalCount = computed(() => allQuestions.value.length)
const prevId = computed(() => {
  const idx = allQuestions.value.findIndex((q: any) => q.id === currentQid.value)
  return idx > 0 ? allQuestions.value[idx - 1].id : null
})
const nextId = computed(() => {
  const idx = allQuestions.value.findIndex((q: any) => q.id === currentQid.value)
  return idx < allQuestions.value.length - 1 ? allQuestions.value[idx + 1].id : null
})

const parsedOptions = computed(() => {
  if (!question.value) return []
  try {
    const opts = typeof question.value.options === 'string'
      ? JSON.parse(question.value.options)
      : question.value.options
    return Array.isArray(opts) ? opts : []
  } catch { return [] }
})

const typeText = computed(() => {
  const t = question.value?.type
  return t === 'SINGLE' ? '单选' : t === 'MULTI' ? '多选' : '单选'
})
const diffText = computed(() => {
  const d = question.value?.difficulty
  return d === 'EASY' ? '简单' : d === 'MEDIUM' ? '中等' : '困难'
})
const diffTag = computed(() => {
  const d = question.value?.difficulty
  return d === 'EASY' ? 'success' : d === 'MEDIUM' ? 'warning' : 'danger'
})

const masteryText = computed(() => {
  return mastery.value === 'mastered' ? '已掌握' : mastery.value === 'unfamiliar' ? '不熟' : '不会'
})
const masteryTag = computed(() => {
  return mastery.value === 'mastered' ? 'success' : mastery.value === 'unfamiliar' ? 'warning' : 'danger'
})

const videoSearchUrl = computed(() => {
  const kw = encodeURIComponent('408考研 ' + getKpNames())
  return `https://search.bilibili.com/all?keyword=${kw}`
})

function stripQvContent(html: string) {
  if (!html) return ''
  return html.replace(/<[^>]*>/g, '').substring(0, 50)
}

function masteryLabel(m: string) {
  return m === 'mastered' ? '掌握' : m === 'unfamiliar' ? '不熟' : '不会'
}

function getKpNames(): string {
  try {
    const kp = question.value?._kpNames
    return kp ? kp : '计算机基础'
  } catch { return '计算机基础' }
}

function selectOption(key: string) {
  if (showResult.value) return
  selectedAnswer.value = key
}

async function submitAnswer() {
  if (!question.value || !selectedAnswer.value) return
  try {
    const res: any = await api.post('/practice/submit', {
      questionId: question.value.id,
      answer: selectedAnswer.value
    })
    if (res.code === 200) {
      lastCorrect.value = res.data.isCorrect
      showResult.value = true
      // Update list item
      const item = allQuestions.value.find((q: any) => q.id === question.value.id)
      if (item) {
        item._done = true
        item._correct = res.data.isCorrect
      }
    }
  } catch { ElMessage.error('提交失败，请先登录') }
}

function resetQuestion() {
  selectedAnswer.value = ''
  showResult.value = false
}

async function setMastery(level: string) {
  mastery.value = level
  if (question.value) {
    question.value._mastery = level
    const item = allQuestions.value.find((q: any) => q.id === question.value.id)
    if (item) item._mastery = level
  }
  try {
    await api.post(`/user/mastery/${question.value.id}`, { mastery: level })
  } catch {}
  ElMessage.success(`已标记为：${masteryLabel(level)}`)
}

async function saveNote() {
  if (!noteContent.value.trim()) return
  noteSaving.value = true
  try {
    await api.post(`/user/note/${question.value.id}`, {
      content: noteContent.value
    })
    ElMessage.success('笔记已保存')
  } catch {
    ElMessage.error('保存失败，请先登录')
  } finally { noteSaving.value = false }
}

function goPrev() {
  if (prevId.value) router.replace(`/question/${prevId.value}`)
}
function goNext() {
  if (nextId.value) router.replace(`/question/${nextId.value}`)
}
function jumpTo(idx: number) {
  const q = allQuestions.value[idx]
  if (q) router.replace(`/question/${q.id}`)
}
function toggleListMode() {
  listMode.value = !listMode.value
}
function goBack() {
  if (route.query.from === 'matrix') {
    router.push('/papers')
  } else if (route.query.from === 'knowledge') {
    router.push('/knowledge')
  } else {
    router.back()
  }
}

async function loadQuestion(qid: number) {
  loading.value = true
  showResult.value = false
  selectedAnswer.value = ''
  mastery.value = ''
  showHint.value = false
  showVideo.value = false
  showNote.value = false
  noteContent.value = ''

  try {
    const res: any = await api.get(`/questions/${qid}`)
    if (res.code === 200) {
      const q = res.data || res
      q.questionNumber = q.questionNumber || q.question_number || null
      question.value = q
      currentQid.value = q.id
      paperYear.value = q.year || 0

      // Load mastery
      // Load mastery from question data
      if (q._mastery) mastery.value = q._mastery
      // Try loading from backend
      try {
        const mres: any = await api.get('/user/mastery')
        if (mres.code === 200 && mres.data[q.id]) {
          mastery.value = mres.data[q.id]
          q._mastery = mres.data[q.id]
        }
      } catch {}

      // Load all questions for navigation context
      const pres: any = await api.get(`/papers?subjectId=1`)
      if (pres.code === 200) {
        const papers = pres.data || []
        const paper = papers.find((p: any) => p.year === q.year)
        if (paper) {
          const qres: any = await api.get(`/papers/${paper.id}/questions`)
          if (qres.code === 200) {
            allQuestions.value = (qres.data || []).map((x: any) => ({ ...x, questionNumber: x.question_number || null, _done: false, _correct: false, _mastery: null, _stripped: (x.content || "").replace(/<[^>]*>/g, "").substring(0, 60) }))
          }
        }
      }
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

// Watch route param changes
watch(() => route.params.questionId, (newId) => {
  if (newId) loadQuestion(Number(newId))
})

onMounted(() => {
  const qid = Number(route.params.questionId)
  if (qid) loadQuestion(qid)
})
</script>

<style scoped>
.qv-page { min-height: calc(100vh - 56px); background: #f5f7fa; display: flex; flex-direction: column; }
.qv-topbar {
  background: white; border-bottom: 1px solid #e5e7eb; padding: 10px 24px;
  display: flex; align-items: center; gap: 16px; position: sticky; top: 56px; z-index: 50;
}
.qv-back { cursor: pointer; color: #4f7cff; font-size: 14px; font-weight: 500; }
.qv-year { font-size: 14px; color: #6b7280; }
.qv-nav { display: flex; align-items: center; gap: 8px; margin-left: auto; }
.qv-pos { font-size: 13px; color: #9ca3af; min-width: 60px; text-align: center; }

/* List Mode */
.qv-list { max-width: 800px; margin: 16px auto; display: flex; flex-direction: column; gap: 4px; padding: 0 16px; }
.qv-list-item { content-visibility: auto; contain-intrinsic-size: 52px;
  display: flex; align-items: center; gap: 12px; padding: 10px 16px;
  background: white; border-radius: 8px; cursor: pointer; transition: all 0.15s;
  border: 2px solid transparent;
}
.qv-list-item:hover { border-color: #93c5fd; }
.qv-list-item.active { border-color: #4f7cff; background: #eff6ff; }
.qv-li-num {
  width: 32px; height: 32px; border-radius: 50%; background: #f3f4f6;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 13px; flex-shrink: 0;
}
.qv-list-item.active .qv-li-num { background: #4f7cff; color: white; }
.qv-li-content { flex: 1; font-size: 14px; color: #374151; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.qv-li-mastery { font-size: 11px; padding: 2px 8px; border-radius: 10px; }
.m-mastered { background: #e8f5e9; color: #2e7d32; }
.m-unfamiliar { background: #fff3e0; color: #e65100; }
.m-dontknow { background: #ffebee; color: #c62828; }

/* Card */
.qv-card-wrap { max-width: 800px; width: 100%; margin: auto; padding: 24px 16px; flex: 1; display: flex; align-items: center; justify-content: center; }
.qv-card { background: white; border-radius: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); overflow: hidden; width: 100%; }
.qv-card-hd {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 24px; border-bottom: 1px solid #f0f0f0; background: #fafbfc;
}
.qv-card-num { display: flex; align-items: center; gap: 10px; }
.qv-card-num-tag {
  width: 36px; height: 36px; border-radius: 10px; background: #4f7cff;
  color: white; display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 16px;
}
.qv-card-num-label { font-size: 16px; font-weight: 600; color: #1f2937; }
.qv-card-score { font-size: 13px; color: #9ca3af; background: #f3f4f6; padding: 2px 10px; border-radius: 10px; }
.qv-card-tags { display: flex; gap: 6px; }

.qv-card-body { padding: 24px; }
.qv-content { font-size: 16px; line-height: 1.9; color: #1f2937; margin-bottom: 24px; }

/* Options */
.qv-options { display: flex; flex-direction: column; gap: 10px; }
.qv-opt {
  display: flex; align-items: center; gap: 14px; padding: 14px 18px;
  border: 2px solid #e5e7eb; border-radius: 12px; cursor: pointer;
  transition: all 0.2s; position: relative;
}
.qv-opt:hover:not(.correct):not(.wrong) { border-color: #93c5fd; background: #f8faff; }
.qv-opt.selected { border-color: #4f7cff; background: #eff6ff; }
.qv-opt.correct { border-color: #52c41a; background: #f6ffed; }
.qv-opt.wrong { border-color: #ff4d4f; background: #fff2f0; }
.qv-opt-key {
  width: 36px; height: 36px; border-radius: 50%; background: #f3f4f6;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 16px; flex-shrink: 0;
}
.qv-opt.correct .qv-opt-key { background: #52c41a; color: white; }
.qv-opt.wrong .qv-opt-key { background: #ff4d4f; color: white; }
.qv-opt-val { font-size: 15px; flex: 1; }
.qv-opt-mark { font-size: 20px; }
.qv-opt-mark.ok { color: #52c41a; }
.qv-opt-mark.err { color: #ff4d4f; }

/* Result */
.qv-result { margin-top: 20px; padding: 16px 20px; border-radius: 10px; }
.qv-result.ok { background: #f6ffed; border: 1px solid #b7eb8f; }
.qv-result.err { background: #fff2f0; border: 1px solid #ffccc7; }
.qv-result p { margin: 0 0 4px; }
.qv-analysis { margin-top: 10px; font-size: 14px; line-height: 1.7; color: #374151; }

/* Actions */
.qv-actions {
  display: flex; justify-content: space-between; align-items: center;
  padding: 12px 24px; border-top: 1px solid #f0f0f0;
}
.qv-act-left, .qv-act-right { display: flex; gap: 8px; align-items: center; }

/* Panels */
.qv-panel { margin: 0 24px 12px; padding: 16px 20px; border-radius: 10px; }
.qv-panel.hint { background: #fffbe6; border: 1px solid #ffe58f; }
.qv-panel.video { background: #f0f5ff; border: 1px solid #adc6ff; }
.qv-panel.note { background: #f9f0ff; border: 1px solid #d3adf7; }
.qv-panel-hd { font-size: 14px; font-weight: 600; margin-bottom: 8px; }
.qv-hint-more { font-size: 12px; color: #9ca3af; margin-top: 8px; }
.qv-video-placeholder {
  display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 16px;
}
.qv-video-icon { font-size: 48px; opacity: 0.3; }
.qv-note-actions { margin-top: 10px; }

/* Mastery */
.qv-mastery {
  display: flex; align-items: center; gap: 8px;
  padding: 12px 24px; border-top: 1px solid #f0f0f0;
}
.qv-mastery-label { font-size: 13px; color: #6b7280; }

/* States */
.qv-loading { display: flex; justify-content: center; padding: 120px 0; color: #9ca3af; }
</style>