<template>
  <div class="page-container">
    <div v-if="loading" class="loading-box"><el-icon class="is-loading" :size="40"><Loading /></el-icon></div>
    <div v-else class="result-content">
      <div class="result-header card">
        <div class="score-circle" :class="scoreClass">
          <span class="score-num">{{ result.score }}</span>
          <span class="score-unit">分</span>
        </div>
        <h2>考试完成！</h2>
        <div class="result-stats">
          <div class="stat"><span class="stat-val">{{ result.correctCount }}/{{ result.totalQuestions }}</span><span class="stat-lbl">正确数</span></div>
          <div class="stat"><span class="stat-val">{{ formatTime(result.duration) }}</span><span class="stat-lbl">用时</span></div>
          <div class="stat"><span class="stat-val">{{ result.status === 'TIMEOUT' ? '超时' : '正常' }}</span><span class="stat-lbl">状态</span></div>
        </div>
      </div>

      <div class="review-section card">
        <h3>题目回顾</h3>
        <div v-for="(q, i) in detailQuestions" :key="i" class="review-item" :class="{ correct: q.isCorrect === 1, wrong: q.isCorrect === 0 }">
          <div class="review-num">{{ i + 1 }}</div>
          <div class="review-body">
            <div class="review-content"><span v-html="q.content"></span></div>
            <div class="review-answer" v-if="q.isCorrect === 0">
              <span>你的答案：<strong class="wrong-text">{{ q.userAnswer || '未作答' }}</strong></span>
              <span>正确答案：<strong class="correct-text">{{ q.answer }}</strong></span>
            </div>
            <div class="review-analysis" v-if="q.analysis">{{ q.analysis }}</div>
          </div>
          <el-icon :size="20"><CircleCheck v-if="q.isCorrect === 1" style="color:var(--success-color)" /><CircleClose v-else style="color:var(--danger-color)" /></el-icon>
        </div>
      </div>

      <div class="result-actions">
        <el-button type="primary" size="large" @click="$router.push('/subjects')">继续刷题</el-button>
        <el-button size="large" @click="$router.push('/analytics')">查看分析</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api'

const route = useRoute()
const loading = ref(true)
const result = ref<any>({})
const detailQuestions = ref<any[]>([])

const scoreClass = computed(() => {
  const s = result.value.score || 0
  if (s >= 80) return 'great'
  if (s >= 60) return 'ok'
  return 'bad'
})

onMounted(async () => {
  const examId = route.params.id
  try {
    const res: any = await api.get(`/practice/exam/${examId}`)
    if (res.code === 200) {
      result.value = res.data.exam
      detailQuestions.value = res.data.questions
    }
  } finally { loading.value = false }
})

function formatTime(s: number) {
  if (!s) return '0秒'
  const m = Math.floor(s / 60)
  const sec = s % 60
  return m > 0 ? `${m}分${sec}秒` : `${sec}秒`
}
</script>

<style scoped>
.loading-box { text-align: center; padding: 120px 0; }
.result-content { max-width: 800px; margin: 0 auto; }

.result-header { text-align: center; padding: 40px; margin-bottom: 24px; }
.score-circle {
  width: 100px; height: 100px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 0 auto 16px; border: 4px solid;
}
.score-circle.great { border-color: var(--success-color); color: var(--success-color); }
.score-circle.ok { border-color: var(--warning-color); color: var(--warning-color); }
.score-circle.bad { border-color: var(--danger-color); color: var(--danger-color); }
.score-num { font-size: 32px; font-weight: 800; line-height: 1; }
.score-unit { font-size: 12px; }

.result-stats { display: flex; justify-content: center; gap: 32px; margin-top: 20px; }
.stat { display: flex; flex-direction: column; }
.stat-val { font-weight: 700; }
.stat-lbl { font-size: 12px; color: var(--text-secondary); }

.review-section { padding: 24px; }
.review-section h3 { margin-bottom: 16px; }
.review-item {
  display: flex; gap: 12px; padding: 16px; border-radius: 8px;
  margin-bottom: 12px; background: var(--bg-color);
}
.review-item.correct { border-left: 3px solid var(--success-color); }
.review-item.wrong { border-left: 3px solid var(--danger-color); }
.review-num { font-weight: 700; font-size: 18px; min-width: 30px; }
.review-body { flex: 1; }
.review-content { font-size: 14px; margin-bottom: 8px; }
.review-answer { display: flex; gap: 16px; font-size: 13px; }
.wrong-text { color: var(--danger-color); }
.correct-text { color: var(--success-color); }
.review-analysis { margin-top: 8px; font-size: 13px; color: var(--text-secondary); padding: 8px; background: white; border-radius: 6px; }
.result-actions { display: flex; gap: 16px; justify-content: center; margin-top: 32px; }
</style>
