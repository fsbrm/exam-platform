<template>
  <div class="kg-page">
    <div v-if="loading" class="page-loading">
      <div class="spinner"></div>
      <p>构建知识森林...</p>
    </div>
    <template v-else>
    <div class="kg-topbar">
      <div class="kg-title-section">
        <h1>🌲 408 知识森林</h1>
        <p>{{ totalNodes }} 节点 · {{ totalLinks }} 连线</p>
      </div>
      <div class="kg-filters">
        <div class="kg-chip all-chip" :class="{ active: activeCat === '' }" @click="selectCat('')">
          <span class="chip-dot" style="background:linear-gradient(135deg,#4f7cff,#52c41a,#fa8c16,#9c27b0)"></span>
          全科
        </div>
        <div v-for="cat in categories" :key="cat.key" class="kg-chip"
          :class="{ active: activeCat === cat.key }"
          :style="{ '--chip-color': cat.color }"
          @click="selectCat(cat.key)">
          <span class="chip-dot" :style="{ background: cat.color }"></span>
          {{ cat.name }}
        </div>
      </div>
    </div>

    <div class="kg-layout">
      <div class="kg-chart-container">
        <div ref="chartRef" class="kg-chart"></div>
      </div>

      <div class="kg-sidebar">
        <h3>🎯 选中节点</h3>
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
          <el-button v-if="selectedNode.level === 'kp'" type="primary" @click="goPractice" style="width:100%;margin-top:8px">练习此知识点</el-button>

          <div v-if="childNodes.length > 0" class="sub-node-list">
            <h5>{{ selectedNode.level === 'subject' ? '📉 章节' : '📑 知识点' }} <span class="sub-count">{{ childNodes.length }}个</span></h5>
            <div v-for="child in childNodes" :key="child.id" class="sub-item" @click="focusNode(child.id)">
              <span class="sub-dot" :style="{ background: child.mastery >= 70 ? '#52c41a' : child.mastery > 0 ? '#fa8c16' : '#d9d9d9' }"></span>
              <span class="sub-name">{{ child.name }}</span>
              <span class="sub-pct">{{ child.mastery || 0 }}%</span>
            </div>
          </div>
        </div>
        <div v-else class="detail-empty">
          <div class="empty-icon">👆</div>
          点击节点查看详情
        </div>

        <h3 style="margin-top:20px">⚠️ 薄弱知识点</h3>
        <div class="weak-list" v-if="weakPoints.length > 0">
          <div v-for="wp in weakPoints" :key="wp.id" class="weak-item" @click="focusNode(wp.id)">
            <span class="weak-dot" :style="{ background: catColorMap[wp.category] || '#ff4d4f' }"></span>
            <span class="weak-name">{{ wp.name }}</span>
            <span class="weak-stat">{{ wp.correct_count || 0 }}✓ /{{ wp.done_count || 0 }}</span>
          </div>
        </div>
        <div v-else class="detail-empty"><div class="empty-icon">🎉</div>暂无薄弱知识点</div>
      </div>
    </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue'
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
const activeCat = ref('')

const categories = [
  { key: '数据结构', name: 'DS', color: '#4f7cff', count: 0 },
  { key: '计算机组成原理', name: 'CO', color: '#fa8c16', count: 0 },
  { key: '操作系统', name: 'OS', color: '#52c41a', count: 0 },
  { key: '计算机网络', name: 'CN', color: '#9c27b0', count: 0 },
]

const catColorMap: Record<string, string> = {
  '数据结构': '#4f7cff', '计算机组成原理': '#fa8c16', '操作系统': '#52c41a', '计算机网络': '#9c27b0'
}

const totalNodes = computed(() => allNodes.value.length)
const totalLinks = computed(() => allLinks.value.length)

const childNodes = computed(() => {
  const sel = selectedNode.value
  if (!sel) return []
  if (sel.level === 'subject') {
    return allNodes.value.filter(n => n.level === 'chapter' && n.category === sel.category)
  }
  if (sel.level === 'chapter') {
    return allNodes.value.filter(n => n.level === 'kp' && n.chapterId === sel.id)
  }
  return []
})

function masteryColor(pct: number) {
  if (!pct || pct === 0) return '#d9d9d9'
  if (pct >= 70) return '#52c41a'
  if (pct >= 40) return '#fa8c16'
  return '#ff4d4f'
}

function selectCat(key: string) {
  if (activeCat.value === key) return
  activeCat.value = key
  selectedNode.value = null
  nextTick(() => renderChart())
}

function focusNode(id: number) {
  selectedNode.value = allNodes.value.find(n => n.id === id) || null
}

function goPractice() {
  if (!selectedNode.value || selectedNode.value.level !== 'kp') return
  router.push('/practice?knowledgeId=' + selectedNode.value.id + '&from=knowledge')
}

onMounted(async () => {
  // Fetch subjects dynamically to get correct IDs
  const subjectsRes: any = await api.get('/subjects')
  const subjectIds: number[] = (subjectsRes?.data || []).map((s: any) => s.id)
  if (subjectIds.length === 0) {
    loading.value = false
    return
  }
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
  weakPoints.value = allWeak.sort((a, b) =>
    ((b.done_count || 0) - (b.correct_count || 0)) - ((a.done_count || 0) - (a.correct_count || 0))
  ).slice(0, 8)

  window.addEventListener('resize', () => chart?.resize())
  loading.value = false
  await nextTick()
  renderChart()
})

let chart: any = null

watch(loading, async (val) => {
  if (!val) {
    await nextTick()
    renderChart()
  }
})

function buildRadialLayout(
  nodes: any[], links: any[], catSet: Set<string>, catCenters: Record<string, [number, number]>,
  w: number, h: number
) {
  const showAll = activeCat.value === ''
  const echartsNodes: any[] = []
  const activeList = showAll ? categories.map(c => c.key) : [activeCat.value]

  for (const catKey of activeList) {
    const group = nodes.filter(n => n.category === catKey)
    const center = catCenters[catKey] || [0.5, 0.5]
    const cx = center[0] * w
    const cy = center[1] * h

    const subjNode = group.find(n => n.level === 'subject')
    const chapters = group.filter(n => n.level === 'chapter')
    const kps = group.filter(n => n.level === 'kp')

    if (subjNode) {
      echartsNodes.push({
        id: subjNode.id, name: subjNode.name, fixed: true,
        symbolSize: showAll ? 40 : 56,
        x: cx, y: cy,
        category: catKey,
        itemStyle: {
          color: catColorMap[catKey] || '#999',
          borderColor: '#fff',
          borderWidth: 3,
          shadowBlur: 12,
          shadowColor: 'rgba(0,0,0,0.15)'
        },
        label: { show: true, fontSize: showAll ? 14 : 16, fontWeight: 'bold', color: '#1f2937' },
        data: subjNode
      })
    }

    const chR = showAll ? 120 : 180
    chapters.forEach((ch, idx) => {
      const angle = (idx / chapters.length) * Math.PI * 2 - Math.PI / 2
      echartsNodes.push({
        id: ch.id, name: ch.name,
        symbolSize: showAll ? 20 : 30,
        x: cx + Math.cos(angle) * chR,
        y: cy + Math.sin(angle) * chR,
        category: catKey,
        itemStyle: {
          color: catColorMap[catKey] || '#999',
          borderColor: '#fff',
          borderWidth: 2,
          opacity: 0.85
        },
        label: { show: !showAll || chapters.length <= 8, fontSize: 11, color: '#4b5563' },
        data: ch
      })
    })

    const kpR = showAll ? 50 : 70
    const chPositions = new Map<number, { x: number; y: number }>()
    for (let i = 0; i < chapters.length; i++) {
      const angle = (i / chapters.length) * Math.PI * 2 - Math.PI / 2
      chPositions.set(chapters[i].id, { x: cx + Math.cos(angle) * chR, y: cy + Math.sin(angle) * chR })
    }

    for (const ch of chapters) {
      const chKps = kps.filter(kp => kp.chapterId === ch.id)
      const cp = chPositions.get(ch.id)!
      chKps.forEach((kp, idx) => {
        const angle = (idx / Math.max(chKps.length, 1)) * Math.PI * 2 - Math.PI / 2
        echartsNodes.push({
          id: kp.id, name: kp.name,
          symbolSize: showAll ? 5 : 9,
          x: cp.x + Math.cos(angle) * kpR,
          y: cp.y + Math.sin(angle) * kpR,
          category: catKey,
          itemStyle: { color: catColorMap[catKey] || '#999', opacity: 0.7 },
          label: { show: !showAll, fontSize: 9, color: '#6b7280' },
          data: kp
        })
      })
    }
  }

  // Links
  const nodeIdSet = new Set(echartsNodes.map(n => n.id))
  const echartsLinks = links
    .filter(l => nodeIdSet.has(l.source) && nodeIdSet.has(l.target))
    .map(l => {
      const si = echartsNodes.findIndex(n => n.id === l.source)
      const ti = echartsNodes.findIndex(n => n.id === l.target)
      const isMain = l.style === 'solid'
      return {
        source: si, target: ti,
        lineStyle: {
          color: isMain ? '#c4c4c4' : '#e5e5e5',
          width: isMain ? 1.8 : 0.6,
          curveness: 0.1,
          opacity: isMain ? 0.45 : 0.18
        }
      }
    })

  return { nodes: echartsNodes, links: echartsLinks }
}

function renderChart() {
  if (!chartRef.value) return

  const showAll = activeCat.value === ''
  const activeList = showAll ? categories.map(c => c.key) : [activeCat.value]
  const catSet = new Set(activeList)

  const filteredNodes = allNodes.value.filter(n => catSet.has(n.category))

  const catCenters: Record<string, [number, number]> = {}
  const count = activeList.length
  if (count === 1) {
    catCenters[activeList[0]] = [0.5, 0.5]
  } else if (count === 2) {
    catCenters[activeList[0]] = [0.25, 0.5]
    catCenters[activeList[1]] = [0.75, 0.5]
  } else if (count === 3) {
    catCenters[activeList[0]] = [0.18, 0.5]
    catCenters[activeList[1]] = [0.5, 0.5]
    catCenters[activeList[2]] = [0.82, 0.5]
  } else {
    catCenters[activeList[0]] = [0.22, 0.22]
    catCenters[activeList[1]] = [0.78, 0.22]
    catCenters[activeList[2]] = [0.22, 0.78]
    catCenters[activeList[3]] = [0.78, 0.78]
  }

  const w = chartRef.value.clientWidth || 1000
  const h = chartRef.value.clientHeight || 720

  const layout = buildRadialLayout(filteredNodes, allLinks.value, catSet, catCenters, w, h)

  const echartsCats = activeList.map(key => {
    const c = categories.find(x => x.key === key)!
    return { name: key, itemStyle: { color: c.color } }
  })

  if (!chart) {
    chart = echarts.init(chartRef.value)
    chart.on('click', (p: any) => {
      if (p.data?.data) selectedNode.value = p.data.data
    })
  }

  chart.setOption({
    tooltip: {
      trigger: 'item',
      formatter: (p: any) => {
        const d = p.data?.data
        if (!d) return ''
        return '<b>' + d.name + '</b><br/>' + d.category +
          (d.level === 'kp' ? '<br/>掌握: ' + (d.mastery || 0) + '%' : '')
      }
    },
    legend: {
      bottom: 10,
      textStyle: { fontSize: 11 },
      selected: Object.fromEntries(categories.map(c => [c.key, catSet.has(c.key)]))
    },
    series: [{
      type: 'graph',
      layout: 'force',
      roam: true,
      draggable: true,
      categories: echartsCats,
      data: layout.nodes,
      links: layout.links,
      force: {
        initIterations: 80,
        repulsion: 60,
        gravity: 0.05,
        edgeLength: [30, 80],
        friction: 0.9
      },
      emphasis: { focus: 'adjacency', lineStyle: { width: 3 } }
    }]
  }, true)
}
</script>

<style scoped>
.kg-page { max-width: 1400px; margin: 0 auto; padding: 16px 20px; }
.page-loading { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 60vh; gap: 16px; }
.page-loading p { color: #9ca3af; font-size: 14px; }
.spinner { width: 40px; height: 40px; border: 3px solid #e5e7eb; border-top-color: #4f7cff; border-radius: 50%; animation: spin .8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.kg-topbar { display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; margin-bottom: 12px; flex-wrap: wrap; }
.kg-title-section h1 { font-size: 20px; font-weight: 800; margin: 0 0 4px; }
.kg-title-section p { font-size: 12px; color: #9ca3af; margin: 0; }

.kg-filters { display: flex; gap: 6px; flex-wrap: wrap; }
.kg-chip {
  display: flex; align-items: center; gap: 5px;
  padding: 6px 12px; border-radius: 20px; cursor: pointer;
  font-size: 12px; font-weight: 500; color: #6b7280;
  background: white; border: 1.5px solid #e5e7eb;
  transition: all 0.15s; user-select: none;
}
.kg-chip:hover { border-color: var(--chip-color, #4f7cff); }
.kg-chip.active { background: #f0f4ff; border-color: var(--chip-color, #4f7cff); color: #1f2937; font-weight: 600; }
.all-chip { border-color: #d1d5db; }
.all-chip.active { background: #f5f3ff; border-color: #7c3aed; }
.chip-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }

.kg-layout { display: grid; grid-template-columns: 1fr 260px; gap: 12px; }
.kg-chart-container { background: white; border-radius: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.kg-chart { width: 100%; height: 680px; }

.kg-sidebar {
  background: white; border-radius: 14px; padding: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  max-height: 700px; overflow-y: auto;
}
.kg-sidebar h3 { font-size: 13px; margin: 0 0 10px; color: #374151; }
.detail-header { display: flex; align-items: center; gap: 6px; margin-bottom: 10px; }
.detail-cat { padding: 2px 8px; border-radius: 8px; font-size: 10px; color: white; }
.detail-header h4 { font-size: 14px; margin: 0; color: #1f2937; }
.detail-ring { display: flex; justify-content: center; margin-bottom: 10px; }
.ring-progress { position: relative; width: 80px; height: 80px; }
.ring-progress svg { width: 100%; height: 100%; }
.ring-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); text-align: center; }
.ring-pct { display: block; font-size: 16px; font-weight: 800; color: #1f2937; }
.ring-sub { font-size: 9px; color: #9ca3af; }
.detail-stats { display: flex; gap: 8px; margin-bottom: 6px; }
.ds-item { flex: 1; text-align: center; padding: 6px; border-radius: 6px; background: #f9fafb; }
.ds-val { display: block; font-size: 15px; font-weight: 700; }
.ds-label { font-size: 10px; color: #9ca3af; }
.ds-item.done .ds-val { color: #4f7cff; }
.ds-item.correct .ds-val { color: #52c41a; }
.detail-empty { color: #9ca3af; font-size: 12px; text-align: center; padding: 20px 0; }
.empty-icon { font-size: 24px; margin-bottom: 6px; }

.weak-list { display: flex; flex-direction: column; gap: 4px; }
.weak-item {
  display: flex; align-items: center; gap: 6px; padding: 5px 8px;
  background: #fff5f5; border-radius: 6px; cursor: pointer; font-size: 11px;
}
.weak-item:hover { background: #ffe7e5; }
.weak-dot { width: 5px; height: 5px; border-radius: 50%; flex-shrink: 0; }
.weak-name { flex: 1; font-weight: 500; color: #374151; }
.weak-stat { font-size: 10px; color: #9ca3af; }

.sub-node-list { margin-top: 12px; border-top: 1px solid #f0f0f0; padding-top: 10px; }
.sub-node-list h5 { font-size: 11px; color: #6b7280; margin: 0 0 6px; }
.sub-count { font-size: 10px; background: #f3f4f6; padding: 1px 6px; border-radius: 8px; color: #9ca3af; }
.sub-item {
  display: flex; align-items: center; gap: 6px; padding: 3px 6px;
  border-radius: 4px; cursor: pointer; font-size: 11px;
}
.sub-item:hover { background: #f0f4ff; }
.sub-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.sub-name { flex: 1; color: #374151; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.sub-pct { font-size: 10px; font-weight: 600; color: #6b7280; }

@media (max-width: 1024px) {
  .kg-layout { grid-template-columns: 1fr; }
  .kg-chart { height: 500px; }
}
</style>