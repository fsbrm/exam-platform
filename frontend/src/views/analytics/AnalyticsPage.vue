<template>
  <div class="analytics-page">
    <h1 class="page-title">学习数据分析</h1>
    <div v-if="loading" class="page-loading">
      <div class="spinner"></div>
      <p>加载分析数据...</p>
    </div>
    <template v-else>
    <div class="overview-cards">
      <div class="ov-card"><div class="ov-icon">📝</div><div class="ov-val">{{ overview.totalQuestions || 0 }}</div><div class="ov-label">总刷题数</div></div>
      <div class="ov-card"><div class="ov-icon">✅</div><div class="ov-val">{{ overview.accuracy || 0 }}%</div><div class="ov-label">正确率</div></div>
      <div class="ov-card"><div class="ov-icon">🔥</div><div class="ov-val">{{ overview.streakDays || 0 }}天</div><div class="ov-label">连续打卡</div></div>
      <div class="ov-card"><div class="ov-icon">📅</div><div class="ov-val">{{ overview.studyDays || 0 }}天</div><div class="ov-label">学习天数</div></div>
    </div>
    <div class="section-card">
      <div class="section-hd"><h3>📅 刷题日历</h3></div>
      <div ref="heatmapRef" class="heatmap-chart"></div>
    </div>
    <div class="charts-row">
      <div class="section-card half"><h3>📈 科目正确率对比</h3><div ref="subjectRef" class="chart-box"></div></div>
      <div class="section-card half"><h3>📉 近30天刷题趋势</h3><div ref="trendRef" class="chart-box"></div></div>
    </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import api from '@/api'

const loading = ref(true)
const overview = ref<any>({})
const heatmapRef = ref()
const subjectRef = ref()
const trendRef = ref()

onMounted(async () => {
  try {
    const res: any = await api.get('/dashboard')
    if (res.code === 200) overview.value = res.data.overview || {}
    await nextTick()
    renderSubjectChart(); renderTrendChart(); renderHeatmapChart()
  } catch {}
  loading.value = false
})

async function renderHeatmapChart() {
  if (!heatmapRef.value) return
  const { default: echarts } = await import('echarts')
  const chart = echarts.init(heatmapRef.value)
  chart.setOption({ title:{text:'刷题热力图',left:'center',textStyle:{fontSize:14}} })
}
async function renderSubjectChart() {
  if (!subjectRef.value) return
  const { default: echarts } = await import('echarts')
  const chart = echarts.init(subjectRef.value)
  chart.setOption({
    xAxis:{type:'category',data:['DS','CO','OS','CN']},
    yAxis:{type:'value'},
    series:[{type:'bar',data:[60,55,70,65],itemStyle:{color:'#4f7cff'}}]
  })
}
async function renderTrendChart() {
  if (!trendRef.value) return
  const { default: echarts } = await import('echarts')
  const chart = echarts.init(trendRef.value)
  chart.setOption({
    xAxis:{type:'category',data:['Mon','Tue','Wed','Thu','Fri','Sat','Sun']},
    yAxis:{type:'value'},
    series:[{type:'line',data:[5,8,3,10,6,12,4],smooth:true,itemStyle:{color:'#4f7cff'}}]
  })
}
</script>

<style scoped>
.analytics-page{max-width:1200px;margin:0 auto;padding:24px 20px}
.page-title{font-size:22px;font-weight:800;margin-bottom:24px}
.overview-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}
.ov-card{background:white;border-radius:14px;padding:20px;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.ov-icon{font-size:28px;margin-bottom:6px}
.ov-val{font-size:28px;font-weight:800;color:#1f2937}
.ov-label{font-size:12px;color:#9ca3af;margin-top:2px}
.section-card{background:white;border-radius:14px;padding:20px 24px;box-shadow:0 1px 3px rgba(0,0,0,.04);margin-bottom:16px}
.section-card h3{font-size:15px;margin-bottom:14px;color:#1f2937}
.section-hd{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.heatmap-chart{width:100%;height:180px}
.charts-row{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.chart-box{width:100%;height:260px}
.page-loading{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:60vh;gap:16px}
.page-loading p{color:#9ca3af;font-size:14px}
.spinner{width:40px;height:40px;border:3px solid #e5e7eb;border-top-color:#4f7cff;border-radius:50%;animation:spin .8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
</style>