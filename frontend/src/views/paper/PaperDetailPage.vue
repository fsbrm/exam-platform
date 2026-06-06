<template>
  <div class="paper-detail">
    <!-- Top Bar -->
    <div class="pd-topbar">
      <div class="pd-back" @click="$router.back()">
        <span>&larr;</span> 返回总览
      </div>
      <div class="pd-title">
        <h2>{{ paperInfo.year }}年408计算机基础综合真题</h2>
        <span class="pd-total">{{ questions.length }}道题目（含选择题和综合题）</span>
      </div>
      <div class="pd-progress" v-if="questions.length > 0">
        已完成 {{ answeredCount }} / {{ questions.length }}
      </div>
    </div>

    <!-- Content Area -->
    <div class="pd-body" v-if="questions.length > 0">
      <!-- Left: Question Number Navigator -->
      <nav class="pd-nav">
        <div class="pd-nav-header">题号导航</div>
        <div class="pd-nav-grid">
          <div v-for="(q, idx) in questions" :key="q.id || q.questionNumber"
            class="pd-nav-num"
            :class="{
              active: currentIndex === idx,
              correct: q.userCorrect === true,
              wrong: q.userCorrect === false
            }"
            @click="currentIndex = idx">
            {{ q.questionNumber || q.question_number }}
          </div>
        </div>
      </nav>

      <!-- Center: Question & Options -->
      <main class="pd-main">
        <div class="pd-question-card" v-if="currentQuestion">
          <!-- Question Header -->
          <div class="pd-q-header">
            <span class="pd-q-num">第 {{ currentQuestion.questionNumber || currentQuestion.question_number }} 题</span>
            <el-tag :type="diffTagType" size="small">{{ diffLabel }}</el-tag>
            <el-tag :type="typeTagType" size="small" effect="plain">{{ typeLabel }}</el-tag>
            <span class="pd-q-year">{{ paperInfo.year }}年真题</span>
          </div>

          <!-- Question Content -->
          <div class="pd-q-content">
            <div v-html="currentQuestion.content" class="pd-q-html"></div>
          </div>

          <!-- Options -->
          <div class="pd-options" v-if="parsedOptions.length > 0 && !isComprehensive">
            <div v-for="opt in parsedOptions" :key="opt.key"
              class="pd-option"
              :class="{
                selected: selectedAnswer === opt.key && !showResult,
                correct: showResult && opt.key === currentQuestion.answer,
                wrong: showResult && selectedAnswer === opt.key && opt.key !== currentQuestion.answer
              }"
              @click="selectOption(opt.key)">
              <span class="pd-opt-key">{{ opt.key }}</span>
              <span class="pd-opt-val">{{ opt.value }}</span>
              <span class="pd-opt-icon" v-if="showResult && opt.key === currentQuestion.answer">&#10003;</span>
              <span class="pd-opt-icon err" v-if="showResult && selectedAnswer === opt.key && opt.key !== currentQuestion.answer">&#10007;</span>
            </div>
          </div>

          <!-- Comprehensive Answer -->
          <div v-if="isComprehensive" class="pd-result ok">
            <div class="pd-result-header">📝 参考答案</div>
            <div class="pd-result-analysis" v-html="currentQuestion.answer"></div>
            <div class="pd-result-analysis" v-if="currentQuestion.analysis" style="margin-top:12px">
              <strong>解析：</strong>{{ currentQuestion.analysis }}
            </div>
          </div>

          <!-- Result -->
          <div v-if="showResult" class="pd-result" :class="{ ok: lastCorrect, err: !lastCorrect }">
            <div class="pd-result-header">
              {{ lastCorrect ? '✅ 回答正确' : '❌ 回答错误' }}
              <span v-if="!lastCorrect">，正确答案：{{ currentQuestion.answer }}</span>
            </div>
            <div class="pd-result-analysis" v-if="currentQuestion.analysis">
              <strong>解析：</strong>{{ currentQuestion.analysis }}
            </div>
          </div>

          <!-- Actions -->
          <div class="pd-actions">
            <el-button v-if="!showResult && selectedAnswer && !isComprehensive" type="primary" @click="submitAnswer">
              提交答案
            </el-button>
            <div class="pd-nav-btns">
              <el-button :disabled="currentIndex === 0" @click="prevQuestion">上一题</el-button>
              <span class="pd-nav-info">{{ currentIndex + 1 }} / {{ questions.length }}</span>
              <el-button :disabled="currentIndex >= questions.length - 1" @click="nextQuestion">下一题</el-button>
            </div>
          </div>
        </div>

        <!-- Empty state when no question selected -->
        <div v-else class="pd-empty">
          请从左侧题号开始答题
        </div>
      </main>

      <!-- Right: Answer Sheet Summary -->
      <aside class="pd-summary">
        <h4>答题卡</h4>
        <div class="pd-summary-grid">
          <div v-for="(q2, idx2) in questions" :key="'s'+q2.id"
            class="pd-s-cell"
            :class="{
              done: q2.userAnswer,
              correct: q2.userCorrect === true,
              wrong: q2.userCorrect === false
            }">
            {{ q2.questionNumber || q2.question_number }}
          </div>
        </div>
        <div class="pd-legend">
          <span><i class="pd-ld done"></i>已答</span>
          <span><i class="pd-ld correct"></i>正确</span>
          <span><i class="pd-ld wrong"></i>错误</span>
        </div>
      </aside>
    </div>

    <!-- Loading -->
    <div v-else-if="loading" class="pd-loading">
      <p>加载题目中...</p>
    </div>

    <!-- Empty -->
    <div v-else class="pd-empty-state">
      <el-empty description="该年份暂无题目数据" />
      <el-button @click="$router.back()">返回</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api'

const route = useRoute()
const loading = ref(true)
const questions = ref<any[]>([])
const currentIndex = ref(0)
const selectedAnswer = ref('')
const showResult = ref(false)
const lastCorrect = ref(false)
const answeredCount = ref(0)

const paperInfo = reactive({ year: 0, name: '' })

const currentQuestion = computed(() => questions.value[currentIndex.value] || null)

const parsedOptions = computed(() => {
  if (!currentQuestion.value) return []
  try {
    const opts = typeof currentQuestion.value.options === 'string'
      ? JSON.parse(currentQuestion.value.options)
      : currentQuestion.value.options
    if (Array.isArray(opts)) return opts
      if (opts && typeof opts === 'object') {
        return Object.entries(opts).map(([key, value]) => ({ key, value }))
      }
      return []
  } catch { return [] }
})

const typeLabel = computed(() => {
  const t = currentQuestion.value?.type
  return t === 'SINGLE' ? '单选题' : t === 'MULTI' ? '多选题' : t === 'COMPREHENSIVE' ? '综合题' : t || '单选题'
})

const typeTagType = computed(() => 'primary')
const diffTagType = computed(() => {
  const d = currentQuestion.value?.difficulty
  return d === 'EASY' ? 'success' : d === 'MEDIUM' ? 'warning' : 'danger'
})

const isComprehensive = computed(() => currentQuestion.value?.type === 'COMPREHENSIVE')

const diffLabel = computed(() => {
  const d = currentQuestion.value?.difficulty
  return d === 'EASY' ? '简单' : d === 'MEDIUM' ? '中等' : '困难'
})

function selectOption(key: string) {
  if (showResult.value) return
  selectedAnswer.value = key
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
      showResult.value = true
      // Update question state
      const q = questions.value[currentIndex.value]
      q.userAnswer = selectedAnswer.value
      q.userCorrect = res.data.isCorrect
      answeredCount.value = questions.value.filter((x: any) => x.userAnswer).length
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

onMounted(async () => {
  const paperId = route.params.paperId || route.query.paperId
  try {
    const res: any = await api.get(`/papers/${paperId}/questions`)
    if (res.code === 200) {
      const list = res.data || []
      // Add tracking fields
      questions.value = list.map((q: any) => ({
        ...q,
        questionNumber: q.question_number || q.questionNumber,
        userAnswer: null,
        userCorrect: null
      }))
    }
    // Get paper info
    const pres: any = await api.get(`/papers?subjectId=1`)
    if (pres.code === 200) {
      const paper = (pres.data || []).find((p: any) => p.id === Number(paperId))
      if (paper) {
        paperInfo.year = paper.year
        paperInfo.name = paper.name
      }
    }
  } catch (e) {
    console.error('Failed to load paper', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.paper-detail { min-height: 100vh; background: #f5f7fa; display: flex; flex-direction: column; }

/* Top Bar */
.pd-topbar {
  background: white; border-bottom: 1px solid #e5e7eb; padding: 12px 24px;
  display: flex; align-items: center; gap: 24px; position: sticky; top: 56px; z-index: 100;
}
.pd-back { cursor: pointer; color: #4f7cff; font-size: 14px; font-weight: 500; }
.pd-back:hover { opacity: 0.8; }
.pd-title h2 { font-size: 18px; margin: 0; display: inline; }
.pd-total { font-size: 13px; color: #9ca3af; margin-left: 10px; }
.pd-progress { margin-left: auto; font-size: 14px; color: #6b7280; }

/* Body */
.pd-body { display: flex; flex: 1; overflow: hidden; }

/* Left Nav */
.pd-nav {
  width: 180px; background: white; border-right: 1px solid #e5e7eb;
  padding: 16px; overflow-y: auto; flex-shrink: 0;
}
.pd-nav-header { font-size: 13px; font-weight: 600; color: #6b7280; margin-bottom: 12px; }
.pd-nav-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; }
.pd-nav-num {
  width: 28px; height: 28px; display: flex; align-items: center; justify-content: center;
  border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer;
  background: #f3f4f6; color: #6b7280; transition: all 0.15s;
}
.pd-nav-num:hover { background: #e0e7ff; color: #4f7cff; }
.pd-nav-num.active { background: #4f7cff; color: white; }
.pd-nav-num.correct { background: #c8e6c9; color: #2e7d32; }
.pd-nav-num.wrong { background: #ffd6d6; color: #c62828; }

/* Main */
.pd-main { flex: 1; overflow-y: auto; padding: 24px; }
.pd-question-card { max-width: 800px; margin: 0 auto; }
.pd-q-header { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
.pd-q-num { font-size: 20px; font-weight: 700; color: #1f2937; }
.pd-q-year { margin-left: auto; font-size: 12px; color: #9ca3af; }
.pd-q-html :deep(img) { max-width: 100%; height: auto; border-radius: 8px; margin: 8px 0; }
.pd-q-html { font-size: 16px; line-height: 2.2; color: #1f2937; }
.pd-q-html :deep(img) { max-width: 100%; height: auto; border-radius: 8px; margin: 8px 0; }
.pd-q-content {
  font-size: 16px; line-height: 2.2; padding: 24px; background: white; color: #1f2937;
  border-radius: 12px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

/* Options */
.pd-options { display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; }
.pd-option {
  display: flex; align-items: center; gap: 12px; padding: 14px 18px;
  background: white; border: 2px solid #e5e7eb; border-radius: 10px;
  cursor: pointer; transition: all 0.2s; position: relative;
}
.pd-option:hover:not(.correct):not(.wrong) { border-color: #93c5fd; background: #eff6ff; }
.pd-option.selected { border-color: #4f7cff; background: #eff6ff; }
.pd-option.correct { border-color: #52c41a; background: #f6ffed; }
.pd-option.wrong { border-color: #ff4d4f; background: #fff2f0; }
.pd-opt-key {
  width: 34px; height: 34px; border-radius: 50%; background: #f3f4f6;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 15px; flex-shrink: 0;
}
.pd-option.correct .pd-opt-key { background: #52c41a; color: white; }
.pd-option.wrong .pd-opt-key { background: #ff4d4f; color: white; }
.pd-opt-val { font-size: 15px; flex: 1; }
.pd-opt-icon { color: #52c41a; font-size: 18px; }
.pd-opt-icon.err { color: #ff4d4f; }

/* Result */
.pd-result { padding: 16px 20px; border-radius: 10px; margin-bottom: 20px; }
.pd-result.ok { background: #f6ffed; border: 1px solid #b7eb8f; }
.pd-result.err { background: #fff2f0; border: 1px solid #ffccc7; }
.pd-result-header { font-size: 16px; font-weight: 600; margin-bottom: 6px; }
.pd-result-analysis { font-size: 14px; line-height: 1.7; color: #374151; }

/* Actions */
.pd-actions { display: flex; justify-content: space-between; align-items: center; margin-top: 12px; }
.pd-nav-btns { display: flex; align-items: center; gap: 12px; }
.pd-nav-info { font-size: 14px; color: #6b7280; font-weight: 500; }

/* Summary */
.pd-summary {
  width: 180px; background: white; border-left: 1px solid #e5e7eb;
  padding: 16px; overflow-y: auto; flex-shrink: 0;
}
.pd-summary h4 { font-size: 13px; font-weight: 600; color: #6b7280; margin-bottom: 12px; }
.pd-summary-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 5px; }
.pd-s-cell {
  width: 28px; height: 28px; display: flex; align-items: center; justify-content: center;
  border-radius: 4px; font-size: 11px; font-weight: 600; background: #f3f4f6; color: #9ca3af;
}
.pd-s-cell.done { background: #dbeafe; color: #4f7cff; }
.pd-s-cell.correct { background: #c8e6c9; color: #2e7d32; }
.pd-s-cell.wrong { background: #ffd6d6; color: #c62828; }
.pd-legend { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 8px; font-size: 11px; color: #9ca3af; }
.pd-ld { display: inline-block; width: 12px; height: 12px; border-radius: 3px; margin-right: 3px; vertical-align: middle; }
.pd-ld.done { background: #dbeafe; }
.pd-ld.correct { background: #c8e6c9; }
.pd-ld.wrong { background: #ffd6d6; }

/* States */
.pd-loading, .pd-empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 120px 0; }
.pd-empty { text-align: center; padding: 80px 0; color: #9ca3af; }
</style>