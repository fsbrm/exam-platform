<template>
  <div class="analytics-page">
    <h1 class="page-title">学习数据分析</h1>
    <div v-if="loading" class="page-loading">
      <div class="spinner"></div>
      <p>加载分析数据...</p>
    </div>
    <template v-else>
    <!-- 概览卡片 -->
    <div class="overview-cards">
      <div class="ov-card"><div class="ov-icon">📝</div><div class="ov-val">{{ overview.totalQuestions || 0 }}</div><div class="ov-label">总刷题数</div></div>
      <div class="ov-card"><div class="ov-icon">✅</div><div class="ov-val">{{ overview.accuracy || 0 }}%</div><div class="ov-label">正确率</div></div>
      <div class="ov-card"><div class="ov-icon">🔥</div><div class="ov-val">{{ overview.streakDays || 0 }}天</div><div class="ov-label">连续打卡</div></div>
      <div class="ov-card"><div class="ov-icon">📮</div><div class="ov-val">{{ overview.studyDays || 0 }}天</div><div class="ov-label">学习天数</div></div>
    </div>

    <!-- 今日统计 -->
    <div class="section-card" v-if="todayCount > 0">
      <div class="section-hd"><h3>📌 今日概览</h3></div>
      <div class="today-stats">
        <span>今日答题 <strong>{{ todayCount }}</strong> 道，正确 <strong>{{ todayCorrect }}</strong> 道</span>
      </div>
    </div>

    <!-- 刷题日历热力图 -->
    <div class="section-card">
      <div class="section-hd"><h3>📮 刷题日历</h3></div>
      <div ref="heatmapRef" class="heatmap-chart"></div>
    </div>

    <!-- 科目对比 + 近10天趋势 -->
    <div class="charts-row">
      <div class="section-card half"><h3>📱 科目正确率对比</h3><div ref="subjectRef" class="chart-box"></div></div>
      <div class="section-card half"><h3>📲 近10天刷题趋势</h3><div ref="trendRef" class="chart-box"></div></div>
    </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import api from '@/api'

const loading = ref(true)
const overview = ref<any>({})
const todayCount = ref(0)
const todayCorrect = ref(0)
const heatmapData = ref<Record<string, number>>({})
const subjectStats = ref<any[]>([])
const weeklyStats = ref<any[]>([])

const heatmapRef = ref()
const subjectRef = ref()
const trendRef = ref()

onMounted(async () => {
  try {
    const [dashRes, weeklyRes]: any[] = await Promise.all([
      api.get('/dashboard'),
      api.get('/dashboard/weekly')
    ])

    if (dashRes.code === 200) {
      const d = dashRes.data
      overview.value = d.overview || {}
      todayCount.value = d.todayCount || 0
      todayCorrect.value = d.todayCorrect || 0
      heatmapData.value = d.heatmap || {}
      subjectStats.value = d.subjectStats || []
    }

    if (weeklyRes.code === 200) {
      weeklyStats.value = weeklyRes.data?.dailyStats || []
    }
  } catch {}

  await nextTick()
  renderHeatmap()
  renderSubjectChart()
  renderTrendChart()
  loading.value = false
})

async function renderHeatmap() {
  if (!heatmapRef.value) return
  const chart = echarts.init(heatmapRef.value)

  const dates = Object.keys(heatmapData.value)
  if (dates.length === 0) {
    chart.setOption({
      title: { text: '暂无刷题记录', left: 'center', top: 'center', textStyle: { fontSize: 14, color: '#9ca3af' } }
    })
    return
  }

  // 找日期范围
  const sorted = dates.sort()
  const minDate = new Date(sorted[0])
  const maxDate = new Date(sorted[sorted.length - 1])

  // 生成全年日期范围
  const yearStart = new Date(maxDate.getFullYear(), 0, 1)
  const yearEnd = new Date(maxDate.getFullYear(), 11, 31)
  const start = minDate < yearStart ? minDate : yearStart
  const end = maxDate > yearEnd ? maxDate : yearEnd

  const dayMs = 86400000
  const weeks = Math.ceil((end.getTime() - start.getTime()) / dayMs / 7) + 1

  const data: [number, number, number][] = []
  for (const [dateStr, count] of Object.entries(heatmapData.value)) {
    const d = new Date(dateStr)
    const weekIndex = Math.floor((d.getTime() - start.getTime()) / dayMs / 7)
    const dayIndex = d.getDay()
    data.push([weekIndex, dayIndex, count])
  }

  const maxCount = Math.max(...Object.values(heatmapData.value), 1)

  chart.setOption({
    tooltip: {
      position: 'top',
      formatter: (p: any) => `${p.value[2]} 题`
    },
    grid: { left: 30, right: 20, top: 10, bottom: 10 },
    xAxis: { type: 'category', show: false, splitArea: { show: true } },
    yAxis: {
      type: 'category',
      data: ['日', '一', '二', '三', '四', '五', '六'],
      splitArea: { show: true },
      axisLabel: { fontSize: 10 }
    },
    visualMap: {
      min: 0,
      max: maxCount,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 0,
      inRange: { color: ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39'] },
      textStyle: { fontSize: 10 }
    },
    series: [{
      type: 'heatmap',
      data: data,
      label: { show: false },
      emphasis: { itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0,0,0,0.3)' } },
      itemStyle: { borderWidth: 2, borderColor: '#fff', borderRadius: 3 }
    }]
  })
}

async function renderSubjectChart() {
  if (!subjectRef.value) return
  const chart = echarts.init(subjectRef.value)

  const names = subjectStats.value.map((s: any) => s.name)
  const accuracies = subjectStats.value.map((s: any) => {
    if (s.doneCount > 0) return Math.round((s.correctCount / s.doneCount) * 100)
    return 0
  })
  const totals = subjectStats.value.map((s: any) => s.doneCount)

  chart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { bottom: 0, textStyle: { fontSize: 11 } },
    xAxis: { type: 'category', data: names, axisLabel: { fontSize: 10 } },
    yAxis: { type: 'value', axisLabel: { fontSize: 10 } },
    series: [
      { name: '正确率(%)', type: 'bar', data: accuracies, itemStyle: { color: '#4f7cff', borderRadius: [4,4,0,0] } },
      { name: '答题数', type: 'line', yAxisIndex: 0, data: totals, smooth: true, itemStyle: { color: '#f59e0b' } }
    ]
  })
}

async function renderTrendChart() {
  if (!trendRef.value) return
  const chart = echarts.init(trendRef.value)

  if (weeklyStats.value.length === 0) {
    chart.setOption({
      title: { text: '暂无近一周数据', left: 'center', top: 'center', textStyle: { fontSize: 14, color: '#9ca3af' } }
    })
    return
  }

  const dates = weeklyStats.value.map((s: any) => {
    const d = s.date
    if (!d) return ''
    const str = typeof d === 'string' ? d : d.toString()
    return str.length >= 10 ? str.substring(5, 10) : str
  })
  const counts = weeklyStats.value.map((s: any) => s.total || 0)
  const corrects = weeklyStats.value.map((s: any) => s.correct || 0)

  chart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { bottom: 0, textStyle: { fontSize: 11 } },
    xAxis: { type: 'category', data: dates, axisLabel: { fontSize: 10 } },
    yAxis: { type: 'value', axisLabel: { fontSize: 10 } },
    series: [
      { name: '答题', type: 'line', data: counts, smooth: true, itemStyle: { color: '#4f7cff' }, areaStyle: { color: 'rgba(79,124,255,0.1)' } },
      { name: '正确', type: 'line', data: corrects, smooth: true, itemStyle: { color: '#10b981' }, areaStyle: { color: 'rgba(16,185,129,0.1)' } }
    ]
  })
}
</script>

<style scoped>
.analytics-page { max-width: 1200px; margin: 0 auto; padding: 24px 20px; }
.page-title { font-size: 22px; font-weight: 800; margin-bottom: 24px; }
.overview-cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }
.ov-card { background: white; border-radius: 14px; padding: 20px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,.04); }
.ov-icon { font-size: 28px; margin-bottom: 6px; }
.ov-val { font-size: 28px; font-weight: 800; color: #1f2937; }
.ov-label { font-size: 12px; color: #9ca3af; margin-top: 2px; }
.section-card { background: white; border-radius: 14px; padding: 20px 24px; box-shadow: 0 1px 3px rgba(0,0,0,.04); margin-bottom: 16px; }
.section-card h3 { font-size: 15px; margin-bottom: 14px; color: #1f2937; }
.section-hd { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.today-stats { font-size: 14px; color: #6b7280; }
.today-stats strong { color: #1f2937; }
.heatmap-chart { width: 100%; height: 200px; }
.charts-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.chart-box { width: 100%; height: 280px; }
.page-loading { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 60vh; gap: 16px; }
.page-loading p { color: #9ca3af; font-size: 14px; }
.spinner { width: 40px; height: 40px; border: 3px solid #e5e7eb; border-top-color: #4f7cff; border-radius: 50%; animation: spin .8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
@media (max-width: 768px) {
  .overview-cards { grid-template-columns: repeat(2, 1fr); }
  .charts-row { grid-template-columns: 1fr; }
}
</style>