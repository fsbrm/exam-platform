<template>
  <div class="practice-page">
    <div v-if="loading" class="loading-box">
      <el-icon class="is-loading" :size="40"><Loading /></el-icon>
      <p>加载题目中...</p>
    </div>
    <div v-else-if="questions.length === 0" class="empty-box">
      <el-empty description="暂无题目" />
      <el-button type="primary" @click="goBack">返回</el-button>
    </div>
    <template v-else>
        <!-- List filters as floating card -->
        <div v-if="viewMode === 'list'" class="pp-float-filters">
          <div class="pff-title">筛选</div>
          <el-select v-model="listFilterSubjectId" placeholder="科目" clearable size="small" @change="listFilterChapterId = null">
            <el-option v-for="s in SUBJECTS" :key="s.id" :label="s.name" :value="s.id" />
          </el-select>
          <el-select v-if="listFilterSubjectId" v-model="listFilterChapterId" placeholder="章节" clearable size="small">
            <el-option v-for="ch in availableChapters" :key="ch.id" :label="ch.name" :value="ch.id" />
          </el-select>
          <el-select v-model="listFilterYear" placeholder="年份" clearable size="small">
            <el-option v-for="y in availableYears" :key="y" :label="y+''" :value="y" />
          </el-select>
          <el-select v-model="listFilterType" size="small">
            <el-option label="全部" value="ALL" /><el-option label="选择题" value="CHOICE" /><el-option label="大题" value="BIG" />
          </el-select>
          <el-input v-model="listSearchText" placeholder="搜索..." size="small" clearable />
          <el-select v-model="listQuickJump" placeholder="跳转题目" size="small" filterable @change="jumpToListQuestion">
            <el-option v-for="(q, idx) in filteredListQuestions" :key="q.id" :label="(q.year||'')+'年'+(q.questionNumber||idx+1)+'题'" :value="idx" />
          </el-select>
        </div>
      <!-- Floating nav toggle (top-right, only when nav closed) -->
      <button v-if="viewMode==='single' && !navOpen" class="pp-float-nav-btn" @click="navOpen=true">☰ {{ questions.length }}题</button>
      <!-- Floating mode switch -->
      <div class="pp-float-mode">
        <button :class="{active:viewMode==='list'}" @click="viewMode='list'">☰ 列表</button>
        <button :class="{active:viewMode==='single'}" @click="viewMode='single'">▦ 单题</button>
      </div>
      <div class="pp-scroll">
        <div v-if="viewMode === 'list'" class="pp-list-wrap">
          <div v-if="filteredListQuestions.length === 0" class="pp-empty">无匹配题目</div>
          <div v-for="(q, qi) in filteredListQuestions" :key="q.id" class="pl-card" :id="'q-'+q.id">
            <div class="pl-card-hd">
              <span class="pl-num">{{ q.year ? q.year+'年第'+(q.questionNumber||qi+1)+'题' : '第'+(qi+1)+' 题' }}</span>
              <el-tag size="small">{{ q.difficulty==='EASY' ? '简单' : q.difficulty==='MEDIUM' ? '中等' : '困难' }}</el-tag>
              <span class="pl-type-tag">{{ q.type==='SINGLE' ? '单选' : '多选' }}</span>
              <span v-if="q._submitted" class="pl-result" :class="q._correct ? 'ok' : 'err'">{{ q._correct ? '对' : '错' }}</span>
              <div class="pl-mastery">
                <el-button :type="q._mastery==='mastered' ? 'success' : ''" size="small" plain @click.stop="markListMastery(q,'mastered')">掌握</el-button>
                <el-button :type="q._mastery==='unfamiliar' ? 'warning' : ''" size="small" plain @click.stop="markListMastery(q,'unfamiliar')">不熟</el-button>
                <el-button :type="q._mastery==='dontknow' ? 'danger' : ''" size="small" plain @click.stop="markListMastery(q,'dontknow')">不会</el-button>
                <el-button size="small" plain @click.stop="markListMastery(q,'careless')" :style="q._mastery==='careless' ? {color:'#7c3aed',borderColor:'#7c3aed',background:'#f5f3ff'} : {}">粗心</el-button>
              </div>
            </div>
            <div class="pl-content">
              <div v-if="q.image"><img :src="q.image" style="max-width:100%;border-radius:6px;margin-bottom:10px" loading="lazy" /></div>
              <div class="pl-text" v-html="formatListContent(q)"></div>
            </div>
            <div class="pl-options" v-if="parsedListOptions(q).length">
              <div v-for="opt in parsedListOptions(q)" :key="opt.key" class="pl-opt" :class="{ selected: q._selected===opt.key && !q._submitted, correct: q._submitted && (opt.key===(q._answer||q.answer)), wrong: q._submitted && q._selected===opt.key && opt.key!==q.answer }" @click="selectListOption(q, opt.key)">
                <span class="pl-opt-key">{{ opt.key }}</span>
                <span class="pl-opt-val" v-html="opt.value"></span>
                <span class="pl-opt-icon" v-if="q._submitted && opt.key===(q._answer||q.answer)">OK</span>
                <span class="pl-opt-icon err" v-if="q._submitted && q._selected===opt.key && opt.key!==(q._answer||q.answer)">NO</span>
              </div>
            </div>
            <div v-if="q._submitted" class="pl-answer">
            <div class="pl-answer-hd"><span v-if="q._showAnswer" style="color:#4f7cff;font-weight:700">答案：{{ q._answer || q.answer }}</span><span v-else :style="{color: q._correct ? '#52c41a' : '#ff4d4f', fontWeight:700}">{{ q._correct ? '正确' : '错误' }}</span></div>
              <div class="pl-answer-body" v-if="q.analysis" v-html="q.analysis"></div>
            </div>
            <div v-if="q._hintLevel >= 1" class="pl-hint"><div class="pl-hint-stage">提示一</div><div class="pl-hint-text">请仔细审题，回忆相关知识点。</div></div>
            <div v-if="q._hintLevel >= 2" class="pl-hint" style="background:#fff0f6;border-color:#ffadd2"><div class="pl-hint-stage">提示一</div><div class="pl-hint-text">{{ getDetailedHint(q) }}</div></div>
            <div v-if="q._showNote" class="pl-note-box"><el-input v-model="q._note" type="textarea" :rows="2" placeholder="笔记..." size="small" /></div>
            <div class="pl-actions">
              <el-button v-if="!q._submitted && q._selected" type="primary" size="small" @click="submitListAnswer(q, qi)">提交</el-button>
              <el-button v-if="q._submitted" size="small" @click="resetListQuestion(q)">重做</el-button>
              <el-button v-if="!q._submitted" size="small" plain @click="cycleHint(q)">提示</el-button>
              <el-button size="small" plain @click="q._showNote=!q._showNote">笔记</el-button>
              <el-button size="small" plain @click="openVideoSearch(q)">视频</el-button>
              <el-button size="small" plain @click="openListAiChat(q)">AI</el-button>
              <el-button v-if="!q._submitted" size="small" type="warning" plain @click="showListAnswer(q)">答案</el-button>
              <el-button size="small" plain @click="toggleListFavorite(q)">{{ q._favorited ? '☆' : '★' }}</el-button>
            </div>
          </div>
          <div class="pl-nav-bar">
            <el-button @click="scrollToListPrev" :disabled="listScrollIdx <= 0"><el-icon><ArrowLeft /></el-icon>上一题</el-button>
            <span>{{ listScrollIdx + 1 }} / {{ filteredListQuestions.length }}</span>
            <el-button @click="scrollToListNext" :disabled="listScrollIdx >= filteredListQuestions.length - 1">下一题<el-icon><ArrowRight /></el-icon></el-button>
          </div>
        </div>
        <div v-if="viewMode === 'single' && currentQuestion" class="pp-single-wrap">
          <!-- Left arrow -->
          <button class="side-arrow side-arrow-left" @click="prevQuestion" :disabled="currentIndex===0" :style="{visibility: currentIndex===0 ? 'hidden' : 'visible'}">
            <el-icon :size="28"><ArrowLeft /></el-icon>
          </button>
          <main class="pps-main">
            <div class="sl-q-card">
              <div class="sl-q-header">
                <el-tag :type="typeTagType">{{ typeLabel }}</el-tag>
                <el-tag :type="diffTagType" effect="plain">{{ diffLabel }}</el-tag>
                <span class="sl-q-num">{{ currentQuestion?.year ? currentQuestion.year+'年第'+(currentQuestion.questionNumber||currentIndex+1)+'题' : '第'+(currentIndex+1)+'/'+questions.length+' 题' }}</span>
                <div class="mastery-btns">
                  <el-button :type="currentMastery==='mastered' ? 'success' : ''" size="small" plain @click="markMastery('mastered')">掌握</el-button>
                  <el-button :type="currentMastery==='unfamiliar' ? 'warning' : ''" size="small" plain @click="markMastery('unfamiliar')">不熟</el-button>
                  <el-button :type="currentMastery==='dontknow' ? 'danger' : ''" size="small" plain @click="markMastery('dontknow')">不会</el-button>
                  <el-button size="small" plain @click="markMastery('careless')" :style="currentMastery==='careless' ? {color:'#7c3aed',borderColor:'#7c3aed',background:'#f5f3ff'} : {}">粗心</el-button>
                </div>
                <el-button text :icon="isFavorited ? 'StarFilled' : 'Star'" @click="toggleFavorite">{{ isFavorited ? '已收藏' : '收藏' }}</el-button>
              </div>
              <div class="sl-q-content">
                <div v-if="currentQuestion?.image"><img :src="currentQuestion.image" style="max-width:100%;border-radius:8px;margin-bottom:16px" loading="lazy" /></div>
                <div class="q-text" v-html="formattedContent"></div>
              </div>
              <div class="sl-options" v-if="['SINGLE','MULTI'].includes(currentQuestion.type)">
                <div v-for="opt in parsedOptions" :key="opt.key" class="sl-opt" :class="{ selected: isSelected(opt.key), correct: showResult && opt.key===correctAnswer, wrong: showResult && isSelected(opt.key) && opt.key!==correctAnswer, disabled: showResult }" @click="selectOption(opt.key)">
                  <span class="sl-opt-key">{{ opt.key }}</span>
                  <span class="sl-opt-val" v-html="opt.value"></span>
                </div>
              </div>
              <div v-if="isBigQuestion" class="sl-result ok">
                <div class="sl-result-hd">参考答案</div>
              <div class="sl-result-body" v-html="currentQuestion.answer || currentQuestion.analysis"></div>
              </div>
              <div v-if="showResult" class="sl-result" :class="{ ok: lastCorrect, err: !lastCorrect }">
                <div class="sl-result-hd"><span v-if="currentQuestion?._showAnswer" style="color:#4f7cff">答案：{{ correctAnswer }}</span><span v-else-if="lastCorrect">正确！</span><span v-else>错误！答案：{{ correctAnswer }}</span></div>
                <div class="sl-result-body" v-if="currentQuestion.analysis" v-html="renderText(currentQuestion.analysis)"></div>
              </div>
              <div v-if="singleHintLevel >= 1" class="sl-hint">提示一：{{ getHintStage1(currentQuestion) }}</div>
              <div v-if="singleHintLevel >= 2" class="sl-hint" style="background:#fff0f6">提示二：{{ getHintStage2(currentQuestion) }}</div>
              <div class="sl-actions">
                <el-button @click="prevQuestion" :disabled="currentIndex === 0" size="large"><el-icon><ArrowLeft /></el-icon>上一题</el-button>
                <el-button v-if="!showResult && canSubmit" type="primary" size="large" @click="submitAnswer">提交</el-button>
                <el-button v-if="!showResult" size="large" type="warning" plain @click="viewSingleAnswer">答案</el-button>
                <el-button @click="nextQuestion" :disabled="currentIndex >= questions.length - 1" size="large">下一题<el-icon><ArrowRight /></el-icon></el-button>
                <el-button v-if="!showResult" size="large" plain @click="cycleSingleHint">提示</el-button>
                <el-button size="large" plain @click="openVideoSearch(currentQuestion)">视频</el-button>
                <el-button size="large" plain @click="toggleNotePanel">笔记</el-button>
              </div>
              <div v-if="showNotePanel" class="sl-note-panel">
                <el-input v-model="currentNote" type="textarea" :rows="3" placeholder="记录解题思路..." />
                <div style="margin-top:8px;display:flex;gap:8px"><el-button size="small" type="primary" @click="saveNote">保存</el-button><el-button size="small" @click="showNotePanel=false">取消</el-button></div>
              </div>
              <div v-if="showVideos" class="video-overlay" @click.self="showVideos=false">
                <div class="video-modal"><div class="vm-header"><h3>视频学习</h3><button class="vm-close" @click="showVideos=false">X</button></div><div class="vm-body"><div class="vm-section"><div class="vm-section-title">题目讲解</div><div v-for="v in questionVideos" :key="v.url" class="vm-video-card" @click="openVideoUrl(v.url)"><div class="vm-card-icon">▶</div><div class="vm-card-info"><div class="vm-card-title">{{ v.title }}</div><div class="vm-card-source">{{ v.source }}</div></div></div></div><div class="vm-section" v-if="knowledgeVideos.length"><div class="vm-section-title">知识点</div><div v-for="v in knowledgeVideos" :key="v.url" class="vm-video-card" @click="openVideoUrl(v.url)"><div class="vm-card-icon">▶</div><div class="vm-card-info"><div class="vm-card-title">{{ v.title }}</div><div class="vm-card-source">{{ v.source }}</div></div></div></div></div></div>
              </div>
            </div>
          </main>
          <!-- Right arrow -->
          <button class="side-arrow side-arrow-right" @click="nextQuestion" :disabled="currentIndex>=questions.length-1" :style="{visibility: currentIndex>=questions.length-1 ? 'hidden' : 'visible'}">
            <el-icon :size="28"><ArrowRight /></el-icon>
          </button>
          <aside class="pps-nav" v-show="navOpen">
            <div class="pps-nav-title">
              <span>题号 · {{ questions.length }}题</span>
              <button class="pps-nav-close" @click="navOpen=false">✕</button>
            </div>
            <div class="pps-nav-grid">
              <div v-for="(q, idx) in paginatedNavQuestions" :key="'sn'+q.id" class="pps-nav-num"
                :class="{ active: currentIndex===navPage*NAV_PAGE_SIZE+idx, correct: q._correct===true, wrong: q._correct===false, done: q._submitted }"
                @click="loadAnswer(navPage*NAV_PAGE_SIZE+idx)">
                {{ navPage * NAV_PAGE_SIZE + idx + 1 }}
              </div>
            </div>
            <div class="pps-nav-pager">
              <button :disabled="navPage===0" @click="navPage--">◀</button>
              <input class="pps-nav-pinp" :value="navPage+1" @keydown.enter="jumpNavPage($event)" @blur="jumpNavPage($event)" />
              <span>/ {{ navTotalPages }}</span>
              <button :disabled="navPage>=navTotalPages-1" @click="navPage++">▶</button>
            </div>
            <div class="pps-nav-legend"><span><i class="pnl-dot active"></i>当前</span><span><i class="pnl-dot done"></i>已答</span><span><i class="pnl-dot correct"></i>正确</span><span><i class="pnl-dot wrong"></i>错误</span></div>
          </aside>
        </div>
      </div>
    </template>
  </div>
</template>
<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import api from '@/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(true)
const viewMode = ref('single')
const questions = ref<any[]>([])
const currentIndex = ref(0)
const selectedAnswer = ref('')
const showResult = ref(false)
const lastCorrect = ref(false)
const correctAnswer = ref('')
const answeredCount = ref(0)
const correctCount = ref(0)
const isFavorited = ref(false)
const currentMastery = ref('')
const submittedMap = ref(new Set())
const listScrollIdx = ref(0)
const navOpen = ref(true)
const navPage = ref(0)
const NAV_PAGE_SIZE = 25
const navTotalPages = computed(() => Math.ceil(questions.value.length / NAV_PAGE_SIZE))
const paginatedNavQuestions = computed(() => {
  const start = navPage.value * NAV_PAGE_SIZE
  return questions.value.slice(start, start + NAV_PAGE_SIZE)
})
function jumpNavPage(e: Event) {
  const v = parseInt((e.target as HTMLInputElement).value)
  if (v >= 1 && v <= navTotalPages.value) navPage.value = v - 1
  else (e.target as HTMLInputElement).value = String(navPage.value + 1)
}
// Auto-sync nav page to current question
watch(currentIndex, (idx) => { navPage.value = Math.floor(idx / NAV_PAGE_SIZE) })
const listFilterYear = ref(null)
const listFilterType = ref('ALL')
const listFilterSubjectId = ref(null)
const listFilterChapterId = ref(null)
const listQuickJump = ref(null)
const listSearchText = ref('')
const singleHintLevel = ref(0)
const showNotePanel = ref(false)
const currentNote = ref('')
const showVideos = ref(false)
const feedbackEnabled = () => localStorage.getItem('practice_feedback') === 'true'

// Floating feedback animation
function showFeedback(isCorrect: boolean) {
  if (!feedbackEnabled()) return
  const main = isCorrect ? 'Niceeee~~~ 🎉' : '我真受不了嘞！ 😤'
  const extras = isCorrect
    ? ['太棒了！✨', '真厉害！🔥', '稳准狠！💯']
    : ['又错了... 💔', '再想想！🤔', '差一点！😭']
  const username = userStore.user?.nickname || userStore.user?.username || '大佬'
  const rareBonus = isCorrect && Math.random() < 0.4 ? "Let's gou ! ! ! 🚀" : null
  const godBonus = isCorrect && Math.random() < 0.3 ? '都是同龄人，我原本没想降维打击！！！ 👽' : null
  const nameBonus = isCorrect && Math.random() < 0.5 ? `流水的天才，铁打的 ${username} ！ 👑` : null
  const count = 1 + (Math.random() < 0.6 ? Math.floor(Math.random() * 2) + 1 : 0) + (rareBonus ? 1 : 0) + (godBonus ? 1 : 0) + (nameBonus ? 1 : 0)
  let allTexts = [main, ...extras].slice(0, count)
  if (rareBonus) allTexts.splice(1, 0, rareBonus)
  if (godBonus) allTexts.splice(1, 0, godBonus)
  if (nameBonus) allTexts.splice(1, 0, nameBonus)
  for (let i = 0; i < allTexts.length; i++) {
    const el = document.createElement('div')
    el.className = 'feedback-float ' + (isCorrect ? 'fb-correct' : 'fb-wrong')
    el.textContent = allTexts[i]
    // Random speed: 4-7 seconds, random delay
    el.style.animationDuration = (4 + Math.random() * 3) + 's'
    el.style.top = (25 + Math.random() * 35) + '%'
    el.style.animationDelay = (i * 0.3) + 's'
    document.body.appendChild(el)
    setTimeout(() => el.remove(), 8000)
  }
}
const questionVideos = ref([])
const knowledgeVideos = ref([])
const videoDataCache = {}

const SUBJECTS = [
  { id: null, name: '全部科目' },
  { id: 10, name: '数据结构' },
    { id: 20, name: '计算机组成原理' },
  { id: 30, name: '操作系统' },
    { id: 40, name: '计算机网络' },
]

function getChapterName(chId) {
  const names = {
      101: '线性表', 102: '栈和队列', 103: '树与二叉树', 104: '图', 105: '查找', 106: '排序',
    201: '概述', 202: '数据表示', 203: '存储系统', 204: '指令系统', 205: 'CPU', 206: '总线与IO',
    301: '概述', 302: '进程管理', 303: '内存管理', 304: '文件系统', 305: 'IO管理',
      401: '体系结构', 402: '物理层', 403: '数据链路层', 404: '网络层', 405: '传输层及应用层',
  }
  return names[chId] || ('章节' + chId)
}

const currentQuestion = computed(() => questions.value[currentIndex.value] || null)
const choiceQuestions = computed(() => questions.value.filter(q => q.options && q.options !== '[]' && q.type !== 'COMPREHENSIVE'))
const availableYears = computed(() => {
  const years = new Set()
  for (const q of questions.value) if (q.year) years.add(q.year)
  return Array.from(years).sort((a, b) => b - a)
})

const availableChapters = computed(() => {
  const map = new Map()
  const sid = listFilterSubjectId.value
  for (const q of questions.value) {
    const chId = q.chapterId
    if (chId && !map.has(chId)) {
      if (!sid || Math.floor(chId / 100) * 10 === sid) map.set(chId, getChapterName(chId))
    }
  }
  const entries = Array.from(map.entries()).sort((a, b) => a[0] - b[0])
  return [{ id: null, name: '全部章节' }, ...entries.map(([id, name]) => ({ id, name }))]
})

const filteredListQuestions = computed(() => {
  let qs = [...questions.value]
  if (listFilterYear.value) qs = qs.filter(q => q.year === listFilterYear.value)
  if (listFilterSubjectId.value) qs = qs.filter(q => {
    const chId = q.chapterId
    return chId && Math.floor(chId / 100) * 10 === listFilterSubjectId.value
  })
  if (listFilterChapterId.value) qs = qs.filter(q => q.chapterId === listFilterChapterId.value)
  if (listFilterType.value === 'CHOICE') qs = qs.filter(q => q.type === 'SINGLE' || q.type === 'MULTI')
  if (listFilterType.value === 'CHOICE') qs = qs.filter(q => { try { const o = typeof q.options === 'string' ? JSON.parse(q.options) : q.options; return o && o.length > 0 } catch { return false } })
  else if (listFilterType.value === 'BIG') qs = qs.filter(q => { const opts = typeof q.options === 'string' ? q.options : JSON.stringify(q.options || []); return opts === '[]' || opts === '' || !opts })
  if (listSearchText.value) {
    const kw = listSearchText.value.toLowerCase()
    qs = qs.filter(q => (q.content || '').toLowerCase().includes(kw))
  }
  return qs
})

const canSubmit = computed(() => {
  if (!currentQuestion.value) return false
  if (!currentQuestion.value?.options || currentQuestion.value.options === '[]') return false
  return selectedAnswer.value.length > 0
})
const isBigQuestion = computed(() => currentQuestion.value?.type === 'COMPREHENSIVE' || currentQuestion.value?.options === '[]')
const typeLabel = computed(() => ({ SINGLE: '单选', MULTI: '多选', COMPREHENSIVE: '综合' })[currentQuestion.value?.type] || '')
const typeTagType = computed(() => ({ SINGLE: '', MULTI: 'warning', COMPREHENSIVE: 'danger' })[currentQuestion.value?.type] || '')
  const diffLabel = computed(() => ({ EASY: '简单', MEDIUM: '中等', HARD: '困难' })[currentQuestion.value?.difficulty] || '')
const diffTagType = computed(() => ({ EASY: 'success', MEDIUM: 'warning', HARD: 'danger' })[currentQuestion.value?.difficulty] || 'info')
const parsedOptions = computed(() => {
  if (!currentQuestion.value?.options) return []
  try {
    const opts = typeof currentQuestion.value.options === 'string' ? JSON.parse(currentQuestion.value.options) : currentQuestion.value.options
    if (Array.isArray(opts)) return opts
    if (opts && typeof opts === 'object') return Object.entries(opts).map(([key, value]) => ({ key, value }))
    return []
  } catch { return [] }
})
const formattedContent = computed(() => currentQuestion.value?.content || '')

function parsedListOptions(q) {
  try {
    const opts = typeof q.options === 'string' ? JSON.parse(q.options) : q.options
    if (Array.isArray(opts)) return opts
    if (opts && typeof opts === 'object') return Object.entries(opts).map(([key, value]) => ({ key, value }))
    return []
  } catch { return [] }
}
function formatListContent(q) { return q.content || '' }
function selectListOption(q, key) { if (!q._submitted) q._selected = key }
function renderText(text) { if (!text) return ''; return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\n/g, '<br>') }
function isSelected(key) { return currentQuestion.value?.type === 'MULTI' ? selectedAnswer.value.split(',').includes(key) : selectedAnswer.value === key }
  function getHintStage1(q) { return '请仔细审题，回忆相关知识点，先排除明显不符合题意的选项。' }
  function getHintStage2(q) { return '核心考点，请关注题目中的关键条件，用排除法确认最终答案。' }
function getDetailedHint(q) { return getHintStage2(q) }

async function submitListAnswer(q, qi) {
  if (!q._selected) return
  try {
    const res = await api.post('/practice/submit', { questionId: q.id, answer: q._selected })
    if (res.code === 200) {
      q._submitted = true; q._correct = res.data.isCorrect
      q._answer = res.data.answer || q.answer
      answeredCount.value++; if (q._correct) correctCount.value++
      // Auto-mark mastery: 答对→掌握, 答错→不会
      q._mastery = res.data.isCorrect ? 'mastered' : 'dontknow'
      if (viewMode.value === 'single') currentMastery.value = q._mastery
      await markMasteryForQuestion(q, q._mastery)
      showFeedback(res.data.isCorrect)
    }
  } catch {}
}
function showListAnswer(q) { q._submitted = true; q._correct = null; q._answer = q.answer; q._showAnswer = true }
function resetListQuestion(q) { q._selected = null; q._submitted = false; q._correct = null; q._answer = null; q._showAnswer = false; q._hintLevel = 0 }
function cycleHint(q) { if (!q._hintLevel) q._hintLevel = 0; q._hintLevel = (q._hintLevel + 1) % 3 }
function viewSingleAnswer() {
  const q = questions.value[currentIndex.value]
  correctAnswer.value = q.answer; showResult.value = true; lastCorrect.value = false
  q._submitted = true; q._correct = null; q._showAnswer = true
}
function cycleSingleHint() { singleHintLevel.value = (singleHintLevel.value + 1) % 3 }
function selectOption(key) {
  if (showResult.value) return
  if (currentQuestion.value?.type === 'MULTI') {
    const s = selectedAnswer.value ? selectedAnswer.value.split(',').filter(x => x) : []
    const idx = s.indexOf(key); if (idx >= 0) s.splice(idx, 1); else s.push(key)
    selectedAnswer.value = s.join(',')
  } else { selectedAnswer.value = key }
}
async function submitAnswer() {
  if (!currentQuestion.value || !selectedAnswer.value) return
  try {
    const res = await api.post('/practice/submit', { questionId: currentQuestion.value.id, answer: selectedAnswer.value })
    if (res.code === 200) {
      lastCorrect.value = res.data.isCorrect
      correctAnswer.value = res.data.answer || currentQuestion.value.answer
      showResult.value = true
      const q = questions.value[currentIndex.value]
      q._submitted = true; q._correct = res.data.isCorrect; q._selected = selectedAnswer.value; q._answer = res.data.answer
      answeredCount.value++; if (res.data.isCorrect) correctCount.value++
      q._mastery = res.data.isCorrect ? 'mastered' : 'dontknow'
      currentMastery.value = q._mastery
      await markMasteryForQuestion(q, q._mastery)
      showFeedback(res.data.isCorrect)
    }
  } catch {}
}
function prevQuestion() { if (currentIndex.value > 0) { currentIndex.value--; resetState() } }
function nextQuestion() { if (currentIndex.value < questions.value.length - 1) { currentIndex.value++; resetState() } }
function goNextOrFinish() {
  if (currentIndex.value < questions.value.length - 1) { currentIndex.value++; resetState() }
    else { ElMessage.success('练习完成！'); router.back() }
}
function resetState() {
  selectedAnswer.value = ''; showResult.value = false; singleHintLevel.value = 0
  // Sync mastery for the new current question
  const q = questions.value[currentIndex.value]
  if (q) currentMastery.value = q._mastery || ''
}
function goBack() { router.back() }
function openAiChat() { router.push('/ai?question=' + encodeURIComponent(currentQuestion.value?.content || '') + '&id=' + currentQuestion.value?.id) }
function openListAiChat(q) { router.push('/ai?question=' + encodeURIComponent(q.content || '') + '&id=' + q.id) }
function loadAnswer(idx) {
  if (idx < 0 || idx >= questions.value.length) return
  viewMode.value = 'single'
  const q = questions.value[idx]; currentIndex.value = idx
  selectedAnswer.value = q._selected || ''; showResult.value = !!q._submitted
  if (q._submitted) { correctAnswer.value = q._answer || q.answer; lastCorrect.value = q._correct }
  currentMastery.value = q._mastery || ''
}
function openVideoSearch(q) {
  if (showVideos.value) { showVideos.value = false; return }
  const keyword = encodeURIComponent((q.content || '').substring(0, 30))
    knowledgeVideos.value = [{ url: 'https://search.bilibili.com/video?keyword=' + encodeURIComponent('408考研'), title: 'B站搜索', source: 'bilibili.com' }]
  questionVideos.value = [{ url: 'https://search.bilibili.com/video?keyword=' + keyword, title: '相关讲解', source: 'bilibili.com' }]
  showVideos.value = true
}
function openBilibiliSearch() { window.open('https://search.bilibili.com/video?keyword=408考研', '_blank') }
function openVideoUrl(url) { window.open(url, '_blank') }
async function toggleNotePanel() {
  showNotePanel.value = !showNotePanel.value
  if (showNotePanel.value && currentQuestion.value) {
    try {
      const res: any = await api.get('/user/note/' + currentQuestion.value.id)
      if (res.code === 200 && res.data) currentNote.value = res.data.content || ''
      else currentNote.value = ''
    } catch { currentNote.value = '' }
  }
}
async function saveNote() {
  if (!currentQuestion.value) return
  try { await api.post('/user/note/' + currentQuestion.value.id, { content: currentNote.value }); currentQuestion.value._note = currentNote.value; ElMessage.success('已保存'); showNotePanel.value = false } catch { ElMessage.error('保存失败') }
}
async function toggleFavorite() {
  if (!currentQuestion.value) return
  try {
    const res: any = await api.post('/user/favorite/' + currentQuestion.value.id)
    if (res.code === 200) { isFavorited.value = res.data.isFavorited; currentQuestion.value._favorited = res.data.isFavorited }
  } catch {}
}
async function toggleListFavorite(q) {
  try {
    const res: any = await api.post('/user/favorite/' + q.id)
    if (res.code === 200) q._favorited = res.data.isFavorited
  } catch {}
}
async function markListMastery(q, level) {
  try {
    await api.post('/user/mastery/' + q.id, { mastery: level })
    q._mastery = level
    ElMessage.success({ mastered: '已标记为掌握', unfamiliar: '已标记为不熟', dontknow: '已标记为不会', careless: '已标记为粗心' }[level] || '标记成功')
  } catch {}
}
async function markMastery(level) {
  if (!currentQuestion.value) return
  try {
    await api.post('/user/mastery/' + currentQuestion.value.id, { mastery: level })
    currentMastery.value = level
    const q = questions.value[currentIndex.value]; q._mastery = level
    ElMessage.success({ mastered: '已标记为掌握', unfamiliar: '已标记为不熟', dontknow: '已标记为不会', careless: '已标记为粗心' }[level] || '标记成功')
  } catch {}
}
async function markMasteryForQuestion(q, level) {
  try { await api.post('/user/mastery/' + q.id, { mastery: level }) } catch {}
}
async function loadMastery() {
  if (!questions.value.length) return
  try {
    const res = await api.get('/user/mastery')
    if (res.code === 200 && res.data) {
      const data = res.data
      for (const q of questions.value) q._mastery = data[q.id] || ''
    }
  } catch {}
  if (questions.value[currentIndex.value]) currentMastery.value = questions.value[currentIndex.value]._mastery || ''
}
function jumpToListQuestion(idx) {
  listScrollIdx.value = idx; listQuickJump.value = null
  nextTick(() => {
    const el = document.getElementById('q-' + filteredListQuestions.value[idx]?.id)
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  })
}
async function scrollToListNext() {
  if (listScrollIdx.value < filteredListQuestions.value.length - 1) {
    listScrollIdx.value++
    const el = document.getElementById('q-' + filteredListQuestions.value[listScrollIdx.value]?.id)
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }
}
function scrollToListPrev() {
  if (listScrollIdx.value > 0) {
    listScrollIdx.value--
    const el = document.getElementById('q-' + filteredListQuestions.value[listScrollIdx.value]?.id)
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }
}
function initState(data) {
  return (data || []).map(q => ({ ...q, _selected: null, _submitted: false, _correct: null, _hintLevel: 0, _showNote: false, _note: '', _favorited: false }))
}

watch(viewMode, (newMode) => {
  nextTick(() => {
    if (newMode === 'list' && currentQuestion.value) {
      const targetId = currentQuestion.value.id
      const idx = filteredListQuestions.value.findIndex(q => q.id === targetId)
      if (idx >= 0) {
        listScrollIdx.value = idx
        const el = document.getElementById('q-' + targetId)
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    } else if (newMode === 'single') {
      const target = filteredListQuestions.value[listScrollIdx.value]
      if (target) {
        const idx = questions.value.findIndex(q => q.id === target.id)
        if (idx >= 0) currentIndex.value = idx
      }
    }
  })
})

onMounted(async () => {
  const chapterId = route.query.chapterId
  const subjectId = route.query.subjectId
  const knowledgeId = route.query.knowledgeId
  const questionId = route.query.questionId
  const from = route.query.from

  if (subjectId) listFilterSubjectId.value = Number(subjectId)
  if (chapterId) {
    listFilterChapterId.value = Number(chapterId)
    const cn = Number(chapterId); const sfc = Math.floor(cn / 100)
    if ([1, 2, 3, 4].includes(sfc)) listFilterSubjectId.value = sfc
  }

  if (from === 'knowledge') viewMode.value = 'single'
  else if (from === 'matrix') viewMode.value = 'single'

  try {
    if (questionId) {
      // Load all questions without pre-setting any filter
      const params = {}
      if (subjectId && from !== 'matrix') params.subjectId = Number(subjectId)
      const allRes = await api.get('/questions/practice', { params })
      if (allRes.code === 200 && allRes.data?.length) {
        questions.value = initState(allRes.data)
        const ti = questions.value.findIndex(q => q.id == questionId)
        if (ti >= 0) currentIndex.value = ti
      } else {
        const qRes2 = await api.get('/questions/' + questionId)
        if (qRes2.code === 200) questions.value = initState([qRes2.data])
      }
    } else if (knowledgeId) {
      const res = await api.get('/questions/practice', { params: { knowledgeId } })
      if (res.code === 200) questions.value = initState(res.data)
    } else if (chapterId) {
      const res = await api.get('/questions/practice', { params: { chapterId } })
      if (res.code === 200) questions.value = initState(res.data)
    } else if (subjectId) {
      const res = await api.get('/questions/practice', { params: { subjectId } })
      if (res.code === 200) questions.value = initState(res.data)
    } else {
      const res = await api.get('/questions/practice')
      if (res.code === 200) questions.value = initState(res.data)
    }
  } catch (e) { ElMessage.error('加载题目失败') } finally { loading.value = false }
  loadMastery()
})
</script>

<style scoped>
.pp-fixed-bar { position: fixed; top: 56px; left: 0; right: 0; z-index: 100; background: rgba(255,255,255,0.95); backdrop-filter: blur(8px); border-bottom: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.06); padding: 0 24px; }
.ppfb-row1 { display: flex; align-items: center; justify-content: flex-end; padding: 6px 0; max-width: 1100px; margin: 0 auto; }
.ppfb-count { font-size: 13px; color: #9ca3af; }
.pp-float-nav-btn { position: fixed; right: 40px; top: 76px; z-index: 90; padding: 5px 12px; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; color: #9ca3af; background: rgba(255,255,255,0.6); backdrop-filter: blur(4px); transition: color 0.2s; white-space: nowrap; }
.pp-float-nav-btn:hover { color: #4f7cff; }
.pp-float-mode { position: fixed; left: 40px; top: 76px; z-index: 90; display: flex; flex-direction: column; gap: 6px; }
.pp-float-mode button { padding: 6px 14px; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; color: #9ca3af; background: rgba(255,255,255,0.6); backdrop-filter: blur(4px); transition: color 0.2s; white-space: nowrap; text-align: left; }
.pp-float-mode button.active { color: #374151; font-weight: 500; }
.pp-float-mode button:hover { color: #4b5563; }
.ppfb-nav-btn { padding: 4px 12px; border: 1px solid #d1d5db; border-radius: 6px; background: white; cursor: pointer; font-size: 13px; color: #4f7cff; white-space: nowrap; }
.ppfb-nav-btn:hover { background: #f0f4ff; }
.ppfb-row2 { display: none; }
.pp-float-filters { position: fixed; right: 20px; top: 80px; z-index: 90; background: rgba(255,255,255,0.95); backdrop-filter: blur(8px); border-radius: 12px; padding: 14px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); display: flex; flex-direction: column; gap: 8px; width: 170px; }
.pff-title { font-size: 12px; font-weight: 600; color: #9ca3af; margin-bottom: 2px; }
.pp-scroll { padding-top: 60px; background: #f5f7fa; min-height: 100vh; }

.pp-list-wrap { max-width: 900px; margin: 0 auto; padding: 20px; display: flex; flex-direction: column; gap: 16px; }
.pp-empty { text-align: center; padding: 60px 0; color: #9ca3af; }
.pp-single-wrap { max-width: 1200px; margin: 0 auto; display: flex; align-items: flex-start; min-height: calc(100vh - 160px); position: relative; }
.side-arrow { position: fixed; top: 50%; transform: translateY(-50%); z-index: 10; width: 44px; height: 44px; border-radius: 50%; border: 1px solid #e5e7eb; background: white; cursor: pointer; display: flex; align-items: center; justify-content: center; color: #4b5563; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: all 0.15s; }
.side-arrow:hover:not(:disabled) { background: #4f7cff; color: white; border-color: #4f7cff; box-shadow: 0 4px 12px rgba(79,124,255,0.3); }
.side-arrow:disabled { opacity: 0.15; cursor: default; }
.side-arrow-left { left: 80px; }
.side-arrow-right { right: 80px; }
.pps-main { flex: 1; overflow-y: auto; padding: 8px 40px 20px; }
.pps-nav { width: 200px; flex-shrink: 0; background: white; border-left: 1px solid #e5e7eb; overflow-y: auto; padding: 16px; position: sticky; top: 80px; align-self: flex-start; max-height: calc(100vh - 120px); }
.pps-nav-title { display: flex; justify-content: space-between; align-items: center; font-size: 13px; font-weight: 600; color: #6b7280; margin-bottom: 12px; }
.pps-nav-close { background: none; border: none; cursor: pointer; font-size: 16px; color: #9ca3af; padding: 2px 6px; border-radius: 4px; }
.pps-nav-close:hover { background: #f3f4f6; color: #374151; }
.pps-nav-pager { display: flex; align-items: center; justify-content: center; gap: 6px; margin-top: 8px; }
.pps-nav-pager button { width: 24px; height: 24px; border: 1px solid #e5e7eb; border-radius: 6px; background: white; cursor: pointer; font-size: 10px; color: #6b7280; display: flex; align-items: center; justify-content: center; }
.pps-nav-pager button:hover:not(:disabled) { background: #eef2ff; color: #4f7cff; border-color: #4f7cff; }
.pps-nav-pager button:disabled { opacity: 0.25; cursor: default; }
.pps-nav-pager span { font-size: 11px; color: #6b7280; }
.pps-nav-pinp { width: 28px; height: 22px; text-align: center; border: 1px solid #e5e7eb; border-radius: 4px; font-size: 11px; outline: none; color: #374151; }
.pps-nav-pinp:focus { border-color: #4f7cff; }
.pps-nav-page-ctl { display: flex; align-items: center; justify-content: center; gap: 4px; margin-bottom: 10px; }
.pps-nav-page-sm { border: none; background: #f3f4f6; cursor: pointer; width: 20px; height: 20px; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 9px; color: #6b7280; }
.pps-nav-page-sm:hover:not(:disabled) { background: #eef2ff; color: #4f7cff; }
.pps-nav-page-sm:disabled { opacity: 0.3; cursor: default; }
.pps-nav-page-inp { width: 32px; height: 20px; text-align: center; border: 1px solid #e5e7eb; border-radius: 4px; font-size: 11px; color: #374151; outline: none; }
.pps-nav-page-inp:focus { border-color: #4f7cff; }
.pps-nav-page-spl { font-size: 11px; color: #9ca3af; }
.pps-nav-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 5px; }
.pps-nav-num { width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; background: #f3f4f6; color: #6b7280; transition: all 0.15s; }
.pps-nav-num:hover { background: #e0e7ff; color: #4f7cff; }
.pps-nav-num.active { background: #4f7cff; color: white; }
.pps-nav-num.done { background: #dbeafe; color: #4f7cff; }
.pps-nav-num.correct { background: #c8e6c9; color: #2e7d32; }
.pps-nav-num.wrong { background: #ffd6d6; color: #c62828; }
.pps-nav-legend { margin-top: 12px; display: flex; gap: 6px; font-size: 10px; color: #9ca3af; flex-wrap: wrap; }
.pnl-dot { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 2px; }
.pnl-dot.active { background: #4f7cff; }
.pnl-dot.done { background: #dbeafe; }
.pnl-dot.correct { background: #c8e6c9; }
.pnl-dot.wrong { background: #ffd6d6; }

.pl-card { background: white; border-radius: 10px; padding: 20px 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.pl-card-hd { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; }
.pl-mastery { display: flex; gap: 4px; margin-left: auto; }
.pl-num { font-size: 15px; font-weight: 700; color: #1f2937; }
.pl-type-tag { font-size: 11px; padding: 2px 8px; background: #f0f4ff; color: #4f7cff; border-radius: 4px; }
.pl-result { font-size: 12px; padding: 2px 8px; border-radius: 8px; }
.pl-result.ok { background: #f6ffed; color: #52c41a; }
.pl-result.err { background: #fff2f0; color: #ff4d4f; }
.pl-content { font-size: 15px; line-height: 2; margin-bottom: 16px; padding: 16px; background: #fafbfc; border-radius: 8px; }
.pl-content img { max-width: 100%; height: auto; border-radius: 6px; }
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
.pl-actions { margin-top: 12px; display: flex; gap: 6px; flex-wrap: wrap; }
.pl-answer { margin-top: 12px; padding: 12px 16px; background: #f8faff; border-radius: 8px; border-left: 3px solid #4f7cff; }
.pl-answer-hd { margin-bottom: 8px; font-size: 14px; }
.pl-answer-body { font-size: 14px; line-height: 1.8; color: #4b5563; }
.pl-hint { margin-top: 10px; padding: 10px 14px; background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; font-size: 13px; }
.pl-hint-stage { display: flex; gap: 4px; font-weight: 600; margin-bottom: 4px; }
.pl-hint-text { color: #4b5563; }
.pl-note-box { margin-top: 10px; }
.pl-nav-bar { display: flex; align-items: center; justify-content: center; gap: 16px; padding: 16px 0; }

.sl-q-card { background: white; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.sl-q-header { display: flex; align-items: center; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
.sl-q-num { font-size: 16px; font-weight: 700; }
.mastery-btns { display: flex; gap: 4px; margin-left: auto; }
.sl-q-content { margin-bottom: 20px; }
.q-text { font-size: 16px; line-height: 2; }
.q-text img { max-width: 100%; height: auto; border-radius: 6px; }
.sl-options { display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; }
.sl-opt { display: flex; align-items: center; gap: 14px; padding: 14px 18px; border: 2px solid #e5e7eb; border-radius: 10px; cursor: pointer; transition: all 0.15s; font-size: 15px; }
.sl-opt:hover:not(.disabled) { border-color: #93c5fd; background: #fafcff; }
.sl-opt.selected { border-color: #4f7cff !important; background: #f0f4ff; }
.sl-opt.correct { border-color: #52c41a; background: #f6ffed; }
.sl-opt.wrong { border-color: #ff4d4f; background: #fff2f0; }
.sl-opt.disabled { cursor: default; opacity: 0.7; }
.sl-opt-key { width: 32px; height: 32px; border-radius: 50%; background: #f3f4f6; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px; flex-shrink: 0; }
.sl-opt.correct .sl-opt-key { background: #52c41a; color: white; }
.sl-opt.wrong .sl-opt-key { background: #ff4d4f; color: white; }
.sl-opt-val { flex: 1; }
.sl-result { padding: 16px 20px; border-radius: 10px; margin-bottom: 16px; }
.sl-result.ok { background: #f6ffed; border: 1px solid #b7eb8f; }
.sl-result.err { background: #fff2f0; border: 1px solid #ffccc7; }
.sl-result-hd { font-size: 15px; font-weight: 600; margin-bottom: 8px; }
.sl-result-body { font-size: 14px; line-height: 1.8; color: #4b5563; }
.sl-hint { margin-bottom: 12px; padding: 10px 14px; background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; font-size: 13px; }
.sl-actions { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 16px; }
.sl-note-panel { margin-top: 12px; }

.video-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.3); z-index: 2000; display: flex; align-items: center; justify-content: center; }
.video-modal { background: white; border-radius: 14px; width: 500px; max-height: 70vh; overflow-y: auto; box-shadow: 0 8px 40px rgba(0,0,0,0.15); }
.vm-header { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; border-bottom: 1px solid #e5e7eb; }
.vm-header h3 { font-size: 16px; }
.vm-close { border: none; background: none; font-size: 18px; cursor: pointer; color: #9ca3af; }
.vm-body { padding: 16px 20px; }
.vm-section { margin-bottom: 16px; }
.vm-section-title { font-size: 14px; font-weight: 600; margin-bottom: 8px; }
.vm-video-card { display: flex; align-items: center; gap: 10px; padding: 10px 12px; background: #f7f8fa; border-radius: 8px; cursor: pointer; margin-bottom: 6px; }
.vm-video-card:hover { background: #f0f4ff; }
.vm-card-icon { width: 32px; height: 32px; background: #4f7cff; color: white; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 14px; }
.vm-card-info { flex: 1; }
.vm-card-title { font-size: 13px; font-weight: 500; }
.vm-card-source { font-size: 11px; color: #9ca3af; }

.loading-box { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }
.loading-box p { margin-top: 16px; color: #9ca3af; }
.empty-box { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; gap: 16px; }
</style>

<!-- unscoped: feedback animation -->
<style>
.feedback-float {
  position: fixed; z-index: 9999; top: 35%;
  font-size: 32px; font-weight: 900; pointer-events: none;
  animation: fb-slide 5s linear forwards;
  text-shadow: 0 2px 12px rgba(0,0,0,0.12);
  white-space: nowrap;
}
.fb-correct { color: #10b981; left: -200px; }
.fb-wrong { color: #ef4444; left: -200px; }
@keyframes fb-slide {
  0%   { transform: translateX(0); opacity: 0; }
  5%   { opacity: 1; }
  80%  { opacity: 1; }
  100% { opacity: 0; transform: translateX(calc(100vw + 300px)); }
}
</style>
