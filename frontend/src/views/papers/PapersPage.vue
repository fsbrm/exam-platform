<template>
  <div class="matrix-page">
    <div class="matrix-layout">
            <!-- Left: 3-Level Knowledge Tree -->
      <aside class="kp-panel">
        <h3>知识点目录</h3>
        <el-input v-model="kpSearch" placeholder="搜索知识点..." size="small" clearable class="kp-search" />

        <div class="kp-tree">
          <!-- Level 1: Subjects -->
          <div v-for="subj in filteredTree" :key="'s'+subj.id" class="kp-l1">
            <div class="kp-l1-header" :class="{ selected: activeNode?.type==='subject' && activeNode?.id===subj.id }" @click="selectNode('subject', subj.id)">
              <span class="kp-arrow" @click.stop="subj._open = !subj._open">{{ subj._open ? '▼' : '▶' }}</span>
              <span class="kp-l1-icon">{{ subj.icon }}</span>
              <span class="kp-l1-name">{{ subj.name }}</span>
              <span class="kp-l1-badge">{{ subj.totalQuestions }}题</span>
              <span v-if="activeNode?.type==='subject' && activeNode?.id===subj.id" class="kp-btn" @click.stop="goPractice()">去刷题 &#8594;</span>

            </div>

            <!-- Level 2: Chapters -->
            <div v-show="subj._open" class="kp-l2-wrap">
              <div v-for="ch in subj.chapters" :key="'c'+ch.id" class="kp-l2">
                <div class="kp-l2-header" :class="{ selected: activeNode?.type==='chapter' && activeNode?.id===ch.id }" @click="selectNode('chapter', ch.id)">
                  <span class="kp-arrow sm" @click.stop="ch._open = !ch._open">{{ ch._open ? '▼' : '▶' }}</span>
                  <span class="kp-l2-name">{{ ch.name }}</span>
                  <span class="kp-l2-badge">{{ ch.totalQuestions }}题</span>
                  <span v-if="activeNode?.type==='chapter' && activeNode?.id===ch.id" class="kp-btn" @click.stop="goPractice()">去刷题 &#8594;</span>

                </div>

                <!-- Level 3: Knowledge Points -->
                <div v-show="ch._open" class="kp-l3-wrap">
                  <div v-for="kp in ch.knowledgePoints" :key="'k'+kp.id" class="kp-l3"
                    :class="{ active: activeNode?.type==='kp' && activeNode?.id===kp.id }"
                    @click="selectNode('kp', kp.id)">
                    <span class="kp-l3-name">{{ kp.name }}</span>
                    <span v-if="activeNode?.type==='kp' && activeNode?.id===kp.id" class="kp-btn" @click.stop="goPractice()">去刷题 &#8594;</span>

                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Progress Toggle -->
        <div class="kp-toggle">
          <el-switch v-model="showProgress" active-text="进度" size="small" />
        </div>

        <!-- Progress Panel -->
        <div v-if="showProgress" class="kp-progress">
          <div class="kp-pg-title">学习进度总览</div>
          <div v-for="subj in filteredTree" :key="'pg'+subj.id" class="kp-pg-subject">
            <div class="kp-pg-subj-name">{{ subj.icon }} {{ subj.name }}</div>
            <el-progress :percentage="subj._pct || 0" :stroke-width="6" :color="'#4f7cff'" />
          </div>
        </div>

        <!-- Legend -->
        <div class="kp-legend">
          <span class="leg-title">图例</span>
          <span><i class="leg-dot" style="background:#e5e7eb;border:1px solid #d1d5db"></i>未做</span>
          <span><i class="leg-dot" style="background:#c8e6c9;border:1px solid #81c784"></i>掌握</span>
          <span><i class="leg-dot" style="background:#fff3e0;border:1px solid #ffb74d"></i>不熟</span>
          <span><i class="leg-dot" style="background:#ffebee;border:1px solid #ef9a9a"></i>不会</span>
          <span><i class="leg-dot" style="background:#ede9fe;border:1px solid #a78bfa"></i>粗心</span>
          <span><i class="leg-dot" style="background:#e5e7eb;box-shadow:0 0 0 2px #4f7cff"></i>匹配</span>
        </div>
      </aside>

      <!-- Right: Year x Question Grid -->
      <main class="grid-panel">
        <div class="grid-scroll">
          <!-- Column Headers: Q1-Q40 | Q41-Q47 -->
          <div class="grid-header">
            <div class="gh-year">年份</div>
            <div class="gh-group">
              <div class="gh-group-title">选择题 1-40</div>
              <div class="gh-nums">
                <div v-for="n in 40" :key="'h'+n" class="gh-num">{{ n }}</div>
              </div>
            </div>
            <div class="gh-divider"></div>
            <div class="gh-group">
              <div class="gh-group-title">大题 41-47</div>
              <div class="gh-nums">
                <div v-for="n in 7" :key="'h'+(n+40)" class="gh-num">{{ n+40 }}</div>
              </div>
            </div>
          </div>

          <!-- Year Rows -->
          <div v-for="yearData in matrixData" :key="yearData.year" class="grid-row">
            <div class="gr-year" @click="selectYear(yearData.year)">
              {{ yearData.year }}
            </div>
            <div class="gr-group">
              <div v-for="n in 40" :key="'a'+n" class="gr-cell"
                :class="cellClass(yearData, n)"
                :style="cellStyle(yearData, n)"
                @click="cellClick(yearData, n)"
                :title="cellTitle(yearData, n)">
              </div>
            </div>
            <div class="gr-divider"></div>
            <div class="gr-group">
              <div v-for="n in 7" :key="'b'+(n+40)" class="gr-cell gr-cell-big"
                :class="cellClass(yearData, n+40)"
                :style="cellStyle(yearData, n+40)"
                @click="cellClick(yearData, n+40)"
                :title="cellTitle(yearData, n+40)">
                <span class="gr-cell-num">{{ n+40 }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Tooltip popup -->
        <div v-if="tooltip.visible" class="tt-overlay" @click="tooltip.visible=false"></div>
        <div v-if="tooltip.visible" class="cell-tooltip">
          <div class="tt-close" @click="tooltip.visible=false">✕</div>
          <div class="tt-year">{{ tooltip.year }}年 第{{ tooltip.num }}题</div>
          <div class="tt-content" v-html="stripHtml(tooltip.content)"></div>
          <div class="tt-meta">
            <span v-if="tooltip.difficulty" :class="'diff-tag d-'+tooltip.difficulty">{{ {EASY:'易',MEDIUM:'中',HARD:'难'}[tooltip.difficulty] }}</span>
            <span v-if="tooltip.done" class="done-tag" :class="tooltip.correct ? 'done-ok' : 'done-err'">{{ tooltip.correct ? '做对' : '做错' }}</span>
          </div>
          <el-button size="small" type="primary" @click="goTooltip">去刷题</el-button>
        </div>
      </main>
    </div>
</div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted, watch, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/api'

const router = useRouter()
const route = useRoute()
const kpSearch = ref('')
const activeNode = ref<{type: string, id: number} | null>(null)
const activeKP = computed(() => activeNode.value?.type === 'kp' ? activeNode.value.id : null)
const matrixData = ref<any[]>([])
const treeData = ref<any[]>([])
const showProgress = ref(false)
const knowledgeTree = ref<any[]>([])
const knowledgeMap = ref<Record<number, number[]>>({}) // kpId -> Set of "year-qnum" keys
const tooltip = reactive({ visible: false, x: 0, y: 0, year: 0, num: 0, content: '', difficulty: '', done: false, correct: false, questionId: 0 })

const filteredTree = computed(() => {
  if (!kpSearch.value) return treeData.value
  const kw = kpSearch.value.toLowerCase()
  return treeData.value.map((subj: any) => ({
    ...subj,
    _open: true,
    chapters: subj.chapters.map((ch: any) => ({
      ...ch,
      _open: true,
      knowledgePoints: ch.knowledgePoints.filter((kp: any) => kp.name.toLowerCase().includes(kw))
    })).filter((ch: any) => ch.knowledgePoints.length > 0 || ch.name.toLowerCase().includes(kw))
  })).filter((subj: any) => subj.chapters.length > 0)
})

// Build knowledgeMap: kpId -> ["2024-5", "2024-12", ...]
function buildKnowledgeMap() {
  const map: Record<number, string[]> = {}
  for (const yd of matrixData.value) {
    for (const q of (yd.questions || [])) {
      for (const kid of (q.knowledgeIds || [])) {
        if (!map[kid]) map[kid] = []
        map[kid].push(`${yd.year}-${q.questionNumber}`)
      }
    }
  }
  // Store as Set for fast lookup
  const fastMap: Record<number, Set<string>> = {}
  for (const [k, v] of Object.entries(map)) {
    fastMap[Number(k)] = new Set(v)
  }
  return fastMap
}

const kpMatchSet = ref<Set<string>>(new Set())

function selectNode(type: string, id: number) {
  if (activeNode.value?.type === type && activeNode.value?.id === id) {
    activeNode.value = null
    kpMatchSet.value = new Set()
  } else {
    activeNode.value = {type, id}
    const fastMap = buildKnowledgeMap()
    if (type === 'kp') {
      // Single knowledge point
      kpMatchSet.value = fastMap[id] || new Set()
    } else if (type === 'chapter') {
      // All KPs under this chapter
      const merged = new Set<string>()
      for (const subj of treeData.value) {
        const ch = subj.chapters?.find((c: any) => c.id === id)
        if (ch) {
          for (const kp of (ch.knowledgePoints || [])) {
            const s = fastMap[kp.id]
            if (s) s.forEach((v: string) => merged.add(v))
          }
          break
        }
      }
      kpMatchSet.value = merged
    } else if (type === 'subject') {
      // All KPs under this subject
      const merged = new Set<string>()
      const subj = treeData.value.find((s: any) => s.id === id)
      if (subj) {
        for (const ch of (subj.chapters || [])) {
          for (const kp of (ch.knowledgePoints || [])) {
            const s = fastMap[kp.id]
            if (s) s.forEach((v: string) => merged.add(v))
          }
        }
      }
      kpMatchSet.value = merged
    }
  }
}
function goPractice() {
  if (!activeNode.value) return
  const {type, id} = activeNode.value
  if (type === 'subject') {
    router.push(`/practice?subjectId=${id}&from=knowledge`)
  } else if (type === 'chapter') {
    router.push(`/practice?chapterId=${id}&from=knowledge`)
  } else if (type === 'kp') {
    // Find which subject this KP belongs to
    let subjectId = 10
    for (const subj of treeData.value) {
      for (const ch of subj.chapters) {
        if (ch.knowledgePoints?.some((kp: any) => kp.id === id)) {
          subjectId = subj.id
        }
      }
    }
    router.push(`/practice?knowledgeId=${id}&subjectId=${subjectId}&from=knowledge`)
  }
}

function cellClass(yd: any, qnum: number) {
  const key = `${yd.year}-${qnum}`
  if (kpMatchSet.value.has(key)) return 'cell-match'
  const q = (yd.questions || []).find((x: any) => x.questionNumber === qnum)
  if (!q || !q.done) return ''
  return q.correct ? 'cell-ok' : 'cell-err'
}

function cellStyle(yd: any, qnum: number) {
  const key = `${yd.year}-${qnum}`
  const q = (yd.questions || []).find((x: any) => x.questionNumber === qnum)
  let style: any = {}
  if (!q) { style = { background: '#f0f0f0', opacity: 0.4 } }
  else if (q.mastery === 'mastered') { style = { background: '#c8e6c9', border: '1px solid #81c784' } }
  else if (q.mastery === 'unfamiliar') { style = { background: '#fff3e0', border: '1px solid #ffb74d' } }
  else if (q.mastery === 'dontknow') { style = { background: '#ffebee', border: '1px solid #ef9a9a' } }
  else if (q.mastery === 'careless') { style = { background: '#ede9fe', border: '1px solid #a78bfa' } }
  else if (!q.done) { style = { background: '#e5e7eb', border: '1px solid #d1d5db' } }
  else { style = q.correct ? { background: '#c8e6c9' } : { background: '#ffd6d6' } }
  if (kpMatchSet.value.has(key)) { style.boxShadow = '0 0 0 2px #4f7cff'; style.position = 'relative'; style.zIndex = 2 }
  return style
}

function cellTitle(yd: any, qnum: number) {
  const q = (yd.questions || []).find((x: any) => x.questionNumber === qnum)
  if (!q) return `${yd.year}年 第${qnum}题`
  return `${yd.year}年 第${qnum}题 [${q.difficulty === 'EASY' ? '易' : q.difficulty === 'MEDIUM' ? '中' : '难'}] ${q.content?.substring(0, 40)}`
}

function cellClick(yd: any, qnum: number, event?: MouseEvent) {
  const q = (yd.questions || []).find((x: any) => x.questionNumber === qnum)
  if (!q) return
  tooltip.year = yd.year
  tooltip.num = qnum
  tooltip.content = q.content || '(无内容)'
  tooltip.difficulty = q.difficulty || ''
  tooltip.done = q.done || false
  tooltip.correct = q.correct || false
  tooltip.questionId = q.questionId
  tooltip.x = Math.min((event as any)?.offsetX || 200, 200)
  tooltip.y = Math.min((event as any)?.offsetY || 100, 100)
  tooltip.visible = true
}

// goPractice() handles all levels

function stripHtml(html: string) {
  if (!html) return '(暂无内容)'
  const textOnly = html.replace(/<[^>]*>/g, '').trim()
  if (!textOnly && html.includes('<img')) return '📷 查看原题截图'
  if (html.includes('<img')) return textOnly || '📷 查看原题截图'
  return textOnly.length > 60 ? textOnly.substring(0, 60) + '...' : textOnly
}

function goTooltip() {
  tooltip.visible = false
  if (tooltip.questionId) {
    router.push(`/practice?questionId=${tooltip.questionId}&from=matrix`)
  }
}

function selectYear(year: number) {
  const yd = matrixData.value.find((y: any) => y.year === year)
  if (yd) {
    router.push(`/paper/${yd.paperId}`)
  }
}

onMounted(async () => {
  try {
    const res: any = await api.get('/papers/matrix?subjectId=1')
    if (res.code === 200) {
      matrixData.value = res.data.years || []
      knowledgeTree.value = (res.data.knowledgeTree || []).map((c: any) => ({...c, open: false}))
    }
    // Load 3-level knowledge tree
    const tr: any = await api.get('/knowledge/tree')
    if (tr.code === 200 && tr.data.tree) {
      treeData.value = tr.data.tree.map((s: any) => ({...s, _open: false}))
      // Restore tree expansion state
      try {
        const saved = sessionStorage.getItem('papers_tree_open')
        if (saved) {
          const openSet = new Set(JSON.parse(saved))
          for (const subj of treeData.value) {
            subj._open = openSet.has('s' + subj.id)
            for (const ch of (subj.chapters || [])) {
              ch._open = openSet.has('c' + ch.id)
            }
          }
        }
      } catch {}
    }
  } catch {}
})

// Save tree expansion state before leaving
onBeforeUnmount(() => {
  const openSet: string[] = []
  for (const subj of treeData.value) {
    if (subj._open) openSet.push('s' + subj.id)
    for (const ch of (subj.chapters || [])) {
      if (ch._open) openSet.push('c' + ch.id)
    }
  }
  sessionStorage.setItem('papers_tree_open', JSON.stringify(openSet))
})

// Reload data on navigation
watch(() => route.path, async (newPath) => {
  if (newPath === '/papers') {
    try {
      const res: any = await api.get('/papers/matrix?subjectId=1')
      if (res.code === 200) {
        matrixData.value = res.data.years || []
      }
    } catch {}
  }
})
</script>

<style scoped>
.matrix-page { height: calc(100vh - 56px); overflow: hidden; }
.matrix-layout { display: flex; height: 100%; }

/* Left Panel */
.kp-panel {
  width: 260px; flex-shrink: 0; background: white; border-right: 1px solid #e5e7eb;
  padding: 16px; display: flex; flex-direction: column; overflow: hidden;
}
.kp-panel h3 { font-size: 15px; margin-bottom: 12px; }
.kp-search { margin-bottom: 10px; }
.kp-tree { flex: 1; overflow-y: auto; }
.kp-cat { margin-bottom: 4px; }
.kp-cat-header {
  display: flex; align-items: center; gap: 6px; padding: 6px 6px; cursor: pointer;
  border-radius: 6px; font-size: 13px; font-weight: 600; user-select: none;
}
.kp-cat-header:hover { background: #f0f4ff; }
.kp-arrow { font-size: 10px; width: 12px; color: #9ca3af; }
.kp-cat-name { flex: 1; }
.kp-cat-badge { font-size: 11px; color: #9ca3af; background: #f0f0f0; padding: 1px 7px; border-radius: 10px; }
.kp-children { padding-left: 14px; }
.kp-leaf { display: flex; align-items: center; gap: 8px; padding: 4px 8px; cursor: pointer; border-radius: 4px; font-size: 12px; }
.kp-leaf:hover { background: #f0f4ff; }
.kp-leaf.active { background: #e8f0ff; color: #4f7cff; }
.kp-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.kp-leaf-name { line-height: 1.3; }

.kp-action { margin-top: 8px; padding: 8px 0; border-top: 1px solid #e5e7eb; }
/* 3-Level Tree */
.kp-l1 { margin-bottom: 2px; }
.kp-l1-header {
  display: flex; align-items: center; gap: 6px; padding: 8px 8px;
  cursor: pointer; border-radius: 6px; font-size: 13px; font-weight: 600;
  transition: all 0.15s;
}
.kp-l1-header:hover { background: #e8f0ff; }
.kp-l1-icon { font-size: 14px; color: #4f7cff; }
.kp-l1-name { flex: 1; color: #1f2937; }
.kp-l1-badge { font-size: 11px; color: #6b7280; background: #f3f4f6; padding: 1px 8px; border-radius: 10px; }
.kp-l2-wrap { padding-left: 8px; }
.kp-l2 { }
.kp-l2-header {
  display: flex; align-items: center; gap: 4px; padding: 5px 6px;
  cursor: pointer; border-radius: 4px; font-size: 12px;
}
.kp-l2-header:hover { background: #f0f4ff; }
.kp-arrow.sm { font-size: 9px; width: 10px; color: #9ca3af; }
.kp-l2-name { flex: 1; color: #374151; font-weight: 500; }
.kp-l2-badge { font-size: 10px; color: #6b7280; background: #f3f4f6; padding: 1px 7px; border-radius: 9px; }
.kp-l3-wrap { padding-left: 10px; }
/* kp-l3 active unified above */
.kp-l3 {
  display: flex; align-items: center; gap: 6px; padding: 5px 10px;
  cursor: pointer; border-radius: 3px; font-size: 11px;
}
.kp-l3:hover { background: #f0f4ff; }
/* merged into above */
.kp-l3-name { flex: 1; color: #6b7280; }
/* unified above */

/* Selected state for all levels */
.kp-l1-header.selected, .kp-l2-header.selected, .kp-l3.active { background: #eef2ff; border-radius: 6px; }
.kp-l1-header.selected .kp-l1-name, .kp-l2-header.selected .kp-l2-name, .kp-l3.active .kp-l3-name { color: #4f7cff; font-weight: 600; }
/* Floating practice button */
.kp-btn {
  font-size: 11px; color: white; background: #4f7cff; padding: 2px 10px;
  border-radius: 10px; cursor: pointer; white-space: nowrap; animation: fadeIn 0.15s;
  flex-shrink: 0;
}
@keyframes fadeIn { from { opacity: 0; transform: translateX(-4px); } to { opacity: 1; transform: translateX(0); } }
.kp-btn:hover { background: #3b6de6; }
/* Progress toggle */
.kp-toggle { margin-top: 10px; padding: 8px; border-top: 1px solid #e5e7eb; }
.kp-progress { padding: 8px; max-height: 200px; overflow-y: auto; }
.kp-pg-title { font-size: 12px; font-weight: 600; color: #6b7280; margin-bottom: 8px; }
.kp-pg-subject { margin-bottom: 10px; }
.kp-pg-subj-name { font-size: 11px; color: #374151; margin-bottom: 3px; }

.kp-legend { margin-top: 12px; padding-top: 10px; border-top: 1px solid #e5e7eb; display: flex; flex-wrap: wrap; gap: 6px; font-size: 11px; color: #6b7280; }
.leg-title { width: 100%; font-weight: 600; }
.leg-dot { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 3px; vertical-align: middle; }

/* Right Grid Panel */
.grid-panel { flex: 1; overflow: hidden; display: flex; flex-direction: column; position: relative; }
.grid-scroll { overflow: auto; padding: 8px; }
.grid-header { display: flex; align-items: flex-end; gap: 0; position: sticky; top: 0; background: #f5f7fa; z-index: 10; padding: 4px 0; }
.gh-year { width: 52px; flex-shrink: 0; font-size: 11px; font-weight: 600; color: #9ca3af; text-align: center; }
.gh-group { }
.gh-group-title { font-size: 11px; font-weight: 700; color: #6b7280; text-align: center; margin-bottom: 3px; }
.gh-nums { display: flex; gap: 3px; }
.gh-num { width: 14px; font-size: 9px; color: #9ca3af; text-align: center; }
.gh-divider { width: 8px; flex-shrink: 0; }

.grid-row { display: flex; align-items: center; gap: 0; margin-bottom: 3px; }
.gr-year {
  width: 52px; flex-shrink: 0; font-size: 13px; font-weight: 700; text-align: center;
  cursor: pointer; padding: 8px 0; border-radius: 4px;
}
.gr-year:hover { background: #f0f4ff; color: #4f7cff; }
.gr-group { display: flex; gap: 3px; }
.gr-cell {
  width: 14px; height: 14px; border-radius: 2px; cursor: pointer;
  transition: transform 0.1s; flex-shrink: 0;
}
.gr-cell:hover { transform: scale(1.5); z-index: 5; box-shadow: 0 2px 6px rgba(0,0,0,0.15); }
.gr-cell-big { width: 18px; height: 18px; border-radius: 3px; display: flex; align-items: center; justify-content: center; }
.gr-cell-num { font-size: 8px; font-weight: 600; color: #6b7280; }
.gr-divider { width: 8px; flex-shrink: 0; }

.cell-ok { background: #c8e6c9 !important; }
.cell-err { background: #ffd6d6 !important; }
.cell-new { background: #e5e7eb !important; border: 1px solid #d1d5db !important; }
.cell-none { background: #f0f0f0 !important; opacity: 0.4 !important; }
.cell-match { box-shadow: 0 0 0 2px #4f7cff; z-index: 2; position: relative; }

/* Tooltip */
.cell-tooltip {
  position: absolute; background: white; border-radius: 10px; padding: 16px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.15); z-index: 100; max-width: 300px;
  right: 20px; top: 60px;
}
.tt-close { position: absolute; top: 8px; right: 10px; cursor: pointer; font-size: 14px; color: #9ca3af; }
.tt-year { font-size: 14px; font-weight: 700; margin-bottom: 8px; }
.tt-content { font-size: 13px; color: #374151; margin-bottom: 8px; line-height: 1.5; }
.tt-meta { display: flex; gap: 6px; margin-bottom: 10px; }
.diff-tag { font-size: 11px; padding: 1px 6px; border-radius: 4px; }
.d-EASY { color: #52c41a; background: #f6ffed; }
.d-MEDIUM { color: #fa8c16; background: #fff7e6; }
.d-HARD { color: #ff4d4f; background: #fff2f0; }
.done-tag { font-size: 11px; padding: 1px 6px; border-radius: 4px; }
.done-ok { color: #52c41a; background: #f6ffed; }
.done-err { color: #ff4d4f; background: #fff2f0; }
</style>
