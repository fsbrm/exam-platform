<template>
  <div class="kg-page">
    <div v-if="loading" class="page-loading">
      <div class="lds-spinner"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
      <p>构建知识森林...</p>
    </div>
    <template v-else>
    <div class="kg-topbar">
      <div class="kg-title-section">
        <h1>🕸️ 408 知识森林</h1>
        <p>{{ totalNodes }} 节点 · {{ totalLinks }} 连线 · 力导向物理引擎</p>
      </div>
      <div class="kg-filters">
        <div
          v-for="cat in categories"
          :key="cat.key"
          class="kg-chip"
          :class="{ active: activeCats.includes(cat.key) }"
          :style="{ '--chip-color': cat.color }"
          @click="toggleCat(cat.key)"
        >
          <span class="chip-dot" :style="{ background: cat.color }"></span>
          {{ cat.name }}
          <span class="chip-count">{{ cat.count }}题</span>
        </div>
      </div>
    </div>

    <div class="kg-layout">
      <div class="kg-chart-container">
        <div ref="chartRef" class="kg-chart"></div>
      </div>

      <div class="kg-sidebar">
        <h3>📌 选中节点</h3>
        <div v-if="selectedNode" class="node-detail">
          <div class="detail-header">
            <span class="detail-cat" :style="{ background: catColorMap[selectedNode.category] || '#999' }">
              {{ selectedNode.level === 'subject' ? '科目' : selectedNode.level === 'chapter' ? '章节' : '知识点' }}
            </span>
            <h4>{{ selectedNode.name }}</h4>
          </div>
          <div class="detail-ring" v-if="selectedNode.level === 'kp'">
            <div class="ring-progress">
              <svg viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" fill="none" stroke="#eee" stroke-width="8"/>
                <circle cx="50" cy="50" r="40" fill="none"
                  :stroke="masteryColor(selectedNode.mastery)"
                  stroke-width="8" stroke-linecap="round"
                  :stroke-dasharray="251.2"
                  :stroke-dashoffset="251.2 * (1 - (selectedNode.mastery || 0) / 100)"
                  transform="rotate(-90 50 50)"/>
              </svg>
              <div class="ring-text">
                <span class="ring-pct">{{ selectedNode.mastery || 0 }}%</span>
                <span class="ring-sub">掌握度</span>
              </div>
            </div>
          </div>
          <div class="detail-stats">
            <div class="ds-item done">
              <span class="ds-val">{{ selectedNode.doneCount || 0 }}</span>
              <span class="ds-label">已做题</span>
            </div>
            <div class="ds-item correct">
              <span class="ds-val">{{ selectedNode.correctCount || 0 }}</span>
              <span class="ds-label">正确数</span>
            </div>
          </div>
          <el-button v-if="selectedNode.level === 'kp'" type="primary" @click="goPractice" style="width:100%; margin-top:8px">练习此知识点</el-button>

          <!-- Sub-node listing for chapter/subject -->
          <div v-if="childNodes.length > 0" class="sub-node-list">
            <h5>
              {{ selectedNode.level === 'subject' ? '📖 章节列表' : '📝 知识点列表' }}
              <span class="sub-count">{{ childNodes.length }}个</span>
            </h5>
            <div v-for="child in childNodes" :key="child.id" class="sub-item"
              @click="focusNode(child.id)"
              :class="{ mastered: child.mastery >= 70, weak: child.mastery > 0 && child.mastery < 40 }">
              <span class="sub-dot" :style="{ background: child.mastery >= 70 ? '#52c41a' : child.mastery > 0 ? '#fa8c16' : '#d9d9d9' }"></span>
              <span class="sub-name">{{ child.name }}</span>
              <span class="sub-pct">{{ child.mastery || 0 }}%</span>
            </div>
          </div>
        </div>
        <div v-else class="detail-empty">
          <div class="empty-icon">👆</div>
          点击节点查看详情<br/>
          <small>拖拽节点 · 滚轮缩放</small>
        </div>

        <h3 style="margin-top: 20px">⚠️ 薄弱知识点</h3>
        <div class="weak-list" v-if="weakPoints.length > 0">
          <div v-for="wp in weakPoints" :key="wp.id" class="weak-item" @click="focusNode(wp.id)">
            <span class="weak-dot" :style="{ background: catColorMap[wp.category || ''] || '#ff4d4f' }"></span>
            <span class="weak-name">{{ wp.name }}</span>
            <span class="weak-stat">
              <span class="ws-ok">{{ wp.correct_count || 0 }}✓</span>
              <span class="ws-total">/{{ wp.done_count || 0 }}</span>
            </span>
          </div>
        </div>
      </div>
    </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import api from '@/api'

const router = useRouter()
const loading = ref(true)
const chartRef = ref<HTMLElement | null>(null)
const selectedNode = ref<any>(null)
const weakPoints = ref<any[]>([])
const allNodes = ref<any[]>([])
const allLinks = ref<any[]>([])
const activeCats = ref<string[]>(['数据结构','计算机组成原理','操作系统','计算机网络'])

const categories = [
  { key: '数据结构', name: '数据结构', color: '#4f7cff', count: 0 },
  { key: '计算机组成原理', name: '组成原理', color: '#fa8c16', count: 0 },
  { key: '操作系统', name: '操作系统', color: '#52c41a', count: 0 },
  { key: '计算机网络', name: '计算机网络', color: '#9c27b0', count: 0 },
]

const catColorMap: Record<string, string> = {
  '数据结构': '#4f7cff', '计算机组成原理': '#fa8c16', '操作系统': '#52c41a', '计算机网络': '#9c27b0'
}

const totalNodes = computed(() => allNodes.value.length)
const totalLinks = computed(() => allLinks.value.length)

const childNodes = computed(() => {
  const sel = selectedNode.value
  if (!sel) return []
  const isSubject = sel.level === 'subject'
  const isChapter = sel.level === 'chapter'
  if (!isSubject && !isChapter) return []
  if (isSubject) {
    return allNodes.value.filter(n => n.level === 'chapter' && n.category === sel.category)
  }
  return allNodes.value.filter(n => n.level === 'kp' && n.chapterId === sel.id)
})

function masteryColor(pct: number) {
  if (!pct || pct === 0) return '#d9d9d9'
  if (pct >= 70) return '#52c41a'
  if (pct >= 40) return '#fa8c16'
  return '#ff4d4f'
}

function toggleCat(key: string) {
  const idx = activeCats.value.indexOf(key)
  if (idx >= 0) activeCats.value.splice(idx, 1)
  else activeCats.value.push(key)
  renderChart()
}

function focusNode(id: number) {
  selectedNode.value = allNodes.value.find(n => n.id === id) || null
}

function goPractice() {
  if (!selectedNode.value || selectedNode.value.level !== 'kp') return
  const kpId = selectedNode.value.id
  router.push(`/practice?knowledgeId=${kpId}&from=knowledge`)
}

onMounted(async () => {
  const subjectIds = [10, 20, 30, 40]
  const results = await Promise.allSettled(
    subjectIds.map(id => api.get('/knowledge/graph', { params: { subjectId: id } }))
  )
  const mergedNodes: any[] = []
  const mergedLinks: any[] = []
  for (const r of results) {
    if (r.status === 'fulfilled' && (r.value as any)?.code === 200) {
      const data = (r.value as any).data
      mergedNodes.push(...(data.nodes || []))
      mergedLinks.push(...(data.links || []))
    }
  }
  allNodes.value = mergedNodes
  allLinks.value = mergedLinks

  for (const c of categories) {
    c.count = mergedNodes.filter(n => n.level === 'kp' && n.category === c.key).length
  }

  const weakResults = await Promise.allSettled(
    subjectIds.map(id => api.get('/knowledge/weakness', { params: { subjectId: id } }))
  )
  const allWeak: any[] = []
  for (const r of weakResults) {
    if (r.status === 'fulfilled' && (r.value as any)?.code === 200) {
      allWeak.push(...((r.value as any).data || []))
    }
  }
  weakPoints.value = allWeak.sort((a: any, b: any) =>
    ((b.done_count || 0) - (b.correct_count || 0)) - ((a.done_count || 0) - (a.correct_count || 0))
  ).slice(0, 8)

  await nextTick()
  renderChart()
  window.addEventListener('resize', () => chart?.resize())
  loading.value = false
})

let chart: any = null

function renderChart() {
  if (!chartRef.value) return
  if (!chart) chart = echarts.init(chartRef.value)

  const catSet = new Set(activeCats.value)
  const filteredNodes = allNodes.value.filter(n => catSet.has(n.category))
  const nodeIdSet = new Set(filteredNodes.map(n => n.id))
  const filteredLinks = allLinks.value.filter(
    l => nodeIdSet.has(l.source) && nodeIdSet.has(l.target)
  )

  const catCenters: Record<string, [number, number]> = {
    '数据结构':      [0.25, 0.22],
    '计算机组成原理': [0.75, 0.22],
    '操作系统':      [0.25, 0.72],
    '计算机网络':    [0.75, 0.72]
  }

  const echartsCats = categories.filter(c => catSet.has(c.key)).map(c => ({
    name: c.key,
    itemStyle: { color: c.color }
  }))

  const nodeMap = new Map(filteredNodes.map(n => [n.id, n]))
  const echartsNodes = filteredNodes.map(n => {
    const center = catCenters[n.category] || [0.5, 0.5]
    return {
      id: n.id,
      name: n.name,
      symbolSize: n.symbolSize || 20,
      category: n.category,
      x: center[0] * 800 + (Math.random() - 0.5) * 200,
      y: center[1] * 700 + (Math.random() - 0.5) * 200,
      itemStyle: { color: n.color || '#999' },
      data: n
    }
  })

  const echartsLinks = filteredLinks.map((l: any) => {
    const si = echartsNodes.findIndex((n: any) => n.id === l.source)
    const ti = echartsNodes.findIndex((n: any) => n.id === l.target)
    const isMain = l.style === 'solid'
    return {
      source: si >= 0 ? si : l.source,
      target: ti >= 0 ? ti : l.target,
      lineStyle: {
        color: isMain ? (catColorMap[nodeMap.get(l.source)?.category] || '#ccc') + '40' : '#e8e8e8',
        width: isMain ? 2 : 1,
        curveness: l.style === 'dashed' ? 0.15 : 0.05,
        opacity: isMain ? 0.6 : 0.3
      }
    }
  })

  chart.setOption({
    backgroundColor: 'transparent',
    animationDuration: 800,
    animationEasingUpdate: 'cubicInOut',
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255,255,255,0.96)',
      borderColor: '#e5e7eb',
      textStyle: { color: '#1f2937', fontSize: 13 },
      formatter: (p: any) => {
        const d = p.data?.data
        if (!d) return p.name
        const lvl = d.level === 'subject' ? '📘 科目' : d.level === 'chapter' ? '📖 章节' : '📝 知识点'
        let html = `<b>${d.name}</b><br/><small>${lvl} · ${d.category}</small>`
        if (d.level !== 'subject') {
          html += `<br/>已做: ${d.doneCount || 0} 正确: ${d.correctCount || 0}`
          html += `<br/>掌握度: <b>${d.mastery || 0}%</b>`
        }
        return html
      }
    },
    legend: {
      data: echartsCats.map(c => c.name),
      bottom: 8,
      textStyle: { fontSize: 12 },
      selected: Object.fromEntries(categories.map(c => [c.key, catSet.has(c.key)]))
    },
    series: [{
      type: 'graph',
      layout: 'force',
      roam: true,
      draggable: true,
      categories: echartsCats,
      data: echartsNodes,
      links: echartsLinks,
      force: {
        initIterations: 300,
        repulsion: 300,
        gravity: 0.04,
        edgeLength: [50, 160],
        layoutAnimation: true,
        friction: 0.85
      },
      emphasis: {
        focus: 'adjacency',
        lineStyle: { width: 4 }
      },
      label: {
        show: true,
        position: 'right',
        fontSize: 10,
        color: '#6b7280',
        formatter: (p: any) => p.data?.data?.level === 'kp' ? p.name : ''
      },
      lineStyle: { color: '#ddd', curveness: 0.1, opacity: 0.4 }
    }]
  })

  chart.off('click')
  chart.on('click', (params: any) => {
    if (params.data && params.data.data) {
      selectedNode.value = params.data.data
    }
  })
}
</script>

<style scoped>
.kg-page { max-width: 1480px; margin: 0 auto; padding: 16px 20px; }
.kg-topbar { margin-bottom: 12px; }
.kg-title-section { text-align: center; margin-bottom: 12px; }
.kg-title-section h1 {
  font-size: 24px; font-weight: 800; margin-bottom: 2px;
  background: linear-gradient(135deg, #4f7cff, #9c27b0);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.kg-title-section p { font-size: 12px; color: #9ca3af; }
.kg-filters { display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; }
.kg-chip {
  display: flex; align-items: center; gap: 5px;
  padding: 5px 14px; border-radius: 18px;
  background: #f3f4f6; cursor: pointer;
  font-size: 12px; font-weight: 500; color: #6b7280;
  border: 2px solid transparent; transition: all 0.2s; user-select: none;
}
.kg-chip:hover { background: #e8ecf4; }
.kg-chip.active {
  background: white; color: #1f2937;
  border-color: var(--chip-color);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.chip-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.chip-count { font-size: 10px; color: #9ca3af; }
.kg-layout { display: grid; grid-template-columns: 1fr 280px; gap: 12px; }
.kg-chart-container {
  background: white; border-radius: 14px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.kg-chart { width: 100%; height: 720px; }
.kg-sidebar {
  background: white; border-radius: 14px; padding: 18px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  max-height: 740px; overflow-y: auto;
}
.kg-sidebar h3 { font-size: 13px; margin-bottom: 10px; color: #374151; }
.node-detail {}
.detail-header { display: flex; align-items: center; gap: 6px; margin-bottom: 10px; }
.detail-cat { padding: 2px 8px; border-radius: 8px; font-size: 10px; color: white; flex-shrink: 0; }
.detail-header h4 { font-size: 14px; margin: 0; color: #1f2937; }
.detail-ring { display: flex; justify-content: center; margin-bottom: 10px; }
.ring-progress { position: relative; width: 90px; height: 90px; }
.ring-progress svg { width: 100%; height: 100%; }
.ring-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); text-align: center; }
.ring-pct { display: block; font-size: 18px; font-weight: 800; color: #1f2937; }
.ring-sub { font-size: 9px; color: #9ca3af; }
.detail-stats { display: flex; gap: 10px; margin-bottom: 6px; }
.ds-item {
  flex: 1; text-align: center; padding: 6px; border-radius: 6px; background: #f9fafb;
}
.ds-val { display: block; font-size: 16px; font-weight: 700; }
.ds-label { font-size: 10px; color: #9ca3af; }
.ds-item.done .ds-val { color: #4f7cff; }
.ds-item.correct .ds-val { color: #52c41a; }
.detail-empty { color: #9ca3af; font-size: 12px; text-align: center; padding: 20px 0; }
.empty-icon { font-size: 24px; margin-bottom: 6px; }
.weak-list { display: flex; flex-direction: column; gap: 5px; }
.weak-item {
  display: flex; align-items: center; gap: 6px;
  padding: 6px 10px; background: #fff5f5;
  border-radius: 6px; cursor: pointer; font-size: 11px; transition: background 0.15s;
}
.weak-item:hover { background: #ffe7e5; }
.weak-dot { width: 5px; height: 5px; border-radius: 50%; flex-shrink: 0; }
.weak-name { flex: 1; font-weight: 500; color: #374151; }
.weak-stat { font-size: 10px; }
.ws-ok { color: #52c41a; }
.ws-total { color: #9ca3af; }
.sub-node-list { margin-top: 14px; border-top: 1px solid #f0f0f0; padding-top: 12px; }
.sub-node-list h5 { font-size: 12px; color: #6b7280; margin: 0 0 8px; display: flex; align-items: center; gap: 6px; }
.sub-count { font-size: 10px; background: #f3f4f6; padding: 1px 7px; border-radius: 8px; color: #9ca3af; }
.sub-item {
  display: flex; align-items: center; gap: 6px; padding: 5px 8px;
  border-radius: 4px; cursor: pointer; font-size: 11px; transition: background 0.15s;
}
.sub-item:hover { background: #f0f4ff; }
.sub-item.mastered { border-left: 3px solid #52c41a; }
.sub-item.weak { border-left: 3px solid #ff4d4f; }
.sub-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.sub-name { flex: 1; color: #374151; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.sub-pct { font-size: 10px; font-weight: 600; color: #6b7280; }

/* Loading */
.page-loading { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 60vh; gap: 16px; }
.page-loading p { color: #9ca3af; font-size: 14px; }
.lds-spinner { color: official; display: inline-block; position: relative; width: 80px; height: 80px; }
.lds-spinner div { transform-origin: 40px 40px; animation: lds-spinner 1.2s linear infinite; }
.lds-spinner div:after { content: " "; display: block; position: absolute; top: 3px; left: 37px; width: 6px; height: 18px; border-radius: 20%; background: #4f7cff; }
.lds-spinner div:nth-child(1) { transform: rotate(0deg); animation-delay: -1.1s; }
.lds-spinner div:nth-child(2) { transform: rotate(30deg); animation-delay: -1s; }
.lds-spinner div:nth-child(3) { transform: rotate(60deg); animation-delay: -0.9s; }
.lds-spinner div:nth-child(4) { transform: rotate(90deg); animation-delay: -0.8s; }
.lds-spinner div:nth-child(5) { transform: rotate(120deg); animation-delay: -0.7s; }
.lds-spinner div:nth-child(6) { transform: rotate(150deg); animation-delay: -0.6s; }
.lds-spinner div:nth-child(7) { transform: rotate(180deg); animation-delay: -0.5s; }
.lds-spinner div:nth-child(8) { transform: rotate(210deg); animation-delay: -0.4s; }
.lds-spinner div:nth-child(9) { transform: rotate(240deg); animation-delay: -0.3s; }
.lds-spinner div:nth-child(10) { transform: rotate(270deg); animation-delay: -0.2s; }
.lds-spinner div:nth-child(11) { transform: rotate(300deg); animation-delay: -0.1s; }
.lds-spinner div:nth-child(12) { transform: rotate(330deg); animation-delay: 0s; }
@keyframes lds-spinner { 0%, 20%, 80%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

@media (max-width: 1024px) {
  .kg-layout { grid-template-columns: 1fr; }
  .kg-chart { height: 500px; }
}
</style>