import os, re

# Read current file
file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "src", "views", "papers", "PapersPage.vue"))
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the entire left panel section
# Find start: <!-- Left: Knowledge Tree -->
# Find end: </aside> (first one after that marker)
start_marker = '<!-- Left: Knowledge Tree -->'
end_marker = '</aside>'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx) + len(end_marker)

new_panel = '''      <!-- Left: 3-Level Knowledge Tree -->
      <aside class="kp-panel">
        <h3>知识点目录</h3>
        <el-input v-model="kpSearch" placeholder="搜索知识点..." size="small" clearable class="kp-search" />

        <div class="kp-tree">
          <!-- Level 1: Subjects -->
          <div v-for="subj in treeData" :key="'s'+subj.id" class="kp-l1">
            <div class="kp-l1-header" @click="subj._open = !subj._open">
              <span class="kp-arrow">{{ subj._open ? '\u25bc' : '\u25b6' }}</span>
              <span class="kp-l1-icon">{{ subj.icon }}</span>
              <span class="kp-l1-name">{{ subj.name }}</span>
              <span class="kp-l1-badge">{{ subj.totalQuestions }}题</span>
              <span class="kp-l1-action" @click.stop="goPracticeBySubject(subj.id)">去刷题</span>
            </div>

            <!-- Level 2: Chapters -->
            <div v-show="subj._open" class="kp-l2-wrap">
              <div v-for="ch in subj.chapters" :key="'c'+ch.id" class="kp-l2">
                <div class="kp-l2-header" @click="ch._open = !ch._open">
                  <span class="kp-arrow sm">{{ ch._open ? '\u25bc' : '\u25b6' }}</span>
                  <span class="kp-l2-name">{{ ch.name }}</span>
                  <span class="kp-l2-badge">{{ ch.totalQuestions }}题</span>
                  <span class="kp-l2-action" @click.stop="goPracticeByChapter(ch.id)">刷题</span>
                </div>

                <!-- Level 3: Knowledge Points -->
                <div v-show="ch._open" class="kp-l3-wrap">
                  <div v-for="kp in ch.knowledgePoints" :key="'k'+kp.id" class="kp-l3"
                    :class="{ active: activeKP === kp.id }"
                    @click="toggleKP(kp.id)">
                    <span class="kp-l3-dot" :style="{background: activeKP === kp.id ? '#4f7cff' : '#d1d5db'}"></span>
                    <span class="kp-l3-name">{{ kp.name }}</span>
                    <span class="kp-l3-action" @click.stop="goPracticeByKP(kp.id)">刷</span>
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
          <div v-for="subj in treeData" :key="'pg'+subj.id" class="kp-pg-subject">
            <div class="kp-pg-subj-name">{{ subj.icon }} {{ subj.name }}</div>
            <el-progress :percentage="subj._pct || 0" :stroke-width="6" :color="'#4f7cff'" />
          </div>
        </div>

        <!-- Legend -->
        <div class="kp-legend">
          <span class="leg-title">图例</span>
          <span><i class="leg-dot" style="background:#dbeafe;border:1px solid #93c5fd"></i>未做</span>
          <span><i class="leg-dot" style="background:#c8e6c9;border:1px solid #81c784"></i>掌握</span>
          <span><i class="leg-dot" style="background:#fff3e0;border:1px solid #ffb74d"></i>不熟</span>
          <span><i class="leg-dot" style="background:#ffebee;border:1px solid #ef9a9a"></i>不会</span>
          <span><i class="leg-dot" style="background:#ffeb3b;border:2px solid #4f7cff"></i>匹配</span>
        </div>
      </aside>'''

content = content[:start_idx] + new_panel + content[end_idx:]

# Now update the script section to add treeData ref and new functions
# Replace tree-related variables
old_tree_vars = 'const matrixData = ref<any[]>([])\nconst knowledgeTree = ref<any[]>([])\nconst knowledgeMap = ref<Record<number, number[]>>({}) // kpId -> Set of "year-qnum" keys\nconst tooltip = reactive({'

new_tree_vars = 'const matrixData = ref<any[]>([])\nconst treeData = ref<any[]>([])\nconst showProgress = ref(false)\nconst knowledgeTree = ref<any[]>([])\nconst knowledgeMap = ref<Record<number, number[]>>({}) // kpId -> Set of "year-qnum" keys\nconst tooltip = reactive({'

content = content.replace(old_tree_vars, new_tree_vars)

# Replace filteredTree computed with treeData
old_filtered = '''const filteredTree = computed(() => {
  if (!kpSearch.value) return knowledgeTree.value
  return knowledgeTree.value.map((cat: any) => ({
    ...cat,
    open: true,
    children: cat.children.filter((kp: any) => kp.name.includes(kpSearch.value))
  })).filter((cat: any) => cat.children.length > 0)
})'''

new_filtered = '''const filteredTree = computed(() => {
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
})'''

content = content.replace(old_filtered, new_filtered)

# Add new functions before goPracticeByKP
old_gop = 'function goPracticeByKP() {\n  if (activeKP.value) {\n    router.push(`/practice?knowledgeId=${activeKP.value}&subjectId=1&from=knowledge`)\n  }\n}'

new_gop = '''function goPracticeBySubject(subjId: number) {
  router.push(`/practice?subjectId=${subjId}&from=knowledge`)
}
function goPracticeByChapter(chId: number) {
  router.push(`/practice?chapterId=${chId}&from=knowledge`)
}
function goPracticeByKP(kpId: number) {
  router.push(`/practice?knowledgeId=${kpId}&subjectId=1&from=knowledge`)
}'''

# Actually the old one is goPracticeByKP() with a different body, let me handle separately
# Let's search for both patterns
# First, find the existing goPracticeByKP
idx_gop = content.find('function goPracticeByKP')
idx_end_gop = content.find('\nfunction goTooltip', idx_gop)
if idx_gop >= 0 and idx_end_gop > idx_gop:
    content = content[:idx_gop] + new_gop + '\n\n' + content[idx_end_gop+1:]

# Update onMounted to load treeData
old_mounted = '''onMounted(async () => {
  try {
    const res: any = await api.get('/papers/matrix?subjectId=1')
    if (res.code === 200) {
      matrixData.value = res.data.years || []
      knowledgeTree.value = (res.data.knowledgeTree || []).map((c: any) => ({...c, open: false}))
    }
  } catch {}
})'''

new_mounted = '''onMounted(async () => {
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
    }
  } catch {}
})'''

content = content.replace(old_mounted, new_mounted)

# Add CSS for new 3-level tree
old_css_end = '.kp-legend { margin-top: 12px;'
new_css_start = '''/* 3-Level Tree */
.kp-l1 { margin-bottom: 2px; }
.kp-l1-header {
  display: flex; align-items: center; gap: 6px; padding: 8px 8px;
  cursor: pointer; border-radius: 6px; font-size: 13px; font-weight: 600;
  transition: all 0.15s;
}
.kp-l1-header:hover { background: #e8f0ff; }
.kp-l1-icon { font-size: 14px; color: #4f7cff; }
.kp-l1-name { flex: 1; color: #1f2937; }
.kp-l1-badge { font-size: 11px; color: #9ca3af; }
.kp-l1-action { font-size: 11px; color: #4f7cff; cursor: pointer; padding: 2px 6px; border-radius: 4px; }
.kp-l1-action:hover { background: #dbeafe; }

.kp-l2-wrap { padding-left: 8px; }
.kp-l2 { }
.kp-l2-header {
  display: flex; align-items: center; gap: 4px; padding: 5px 6px;
  cursor: pointer; border-radius: 4px; font-size: 12px;
}
.kp-l2-header:hover { background: #f0f4ff; }
.kp-arrow.sm { font-size: 9px; width: 10px; color: #9ca3af; }
.kp-l2-name { flex: 1; color: #374151; font-weight: 500; }
.kp-l2-badge { font-size: 10px; color: #9ca3af; }
.kp-l2-action { font-size: 10px; color: #4f7cff; cursor: pointer; padding: 1px 5px; border-radius: 3px; }
.kp-l2-action:hover { background: #dbeafe; }

.kp-l3-wrap { padding-left: 10px; }
.kp-l3 {
  display: flex; align-items: center; gap: 6px; padding: 3px 6px;
  cursor: pointer; border-radius: 3px; font-size: 11px;
}
.kp-l3:hover { background: #f0f4ff; }
.kp-l3.active { background: #e8f0ff; }
.kp-l3-dot { width: 5px; height: 5px; border-radius: 50%; flex-shrink: 0; }
.kp-l3-name { flex: 1; color: #6b7280; }
.kp-l3.active .kp-l3-name { color: #4f7cff; }
.kp-l3-action { font-size: 10px; color: #4f7cff; cursor: pointer; padding: 0 4px; border-radius: 2px; display: none; }
.kp-l3:hover .kp-l3-action { display: inline; }
.kp-l3-action:hover { background: #dbeafe; }

/* Progress toggle */
.kp-toggle { margin-top: 10px; padding: 8px; border-top: 1px solid #e5e7eb; }
.kp-progress { padding: 8px; max-height: 200px; overflow-y: auto; }
.kp-pg-title { font-size: 12px; font-weight: 600; color: #6b7280; margin-bottom: 8px; }
.kp-pg-subject { margin-bottom: 10px; }
.kp-pg-subj-name { font-size: 11px; color: #374151; margin-bottom: 3px; }

'''

# Find the .kp-legend CSS and prepend the new CSS
css_idx = content.find('.kp-legend { margin-top: 12px;')
if css_idx >= 0:
    content = content[:css_idx] + new_css_start + content[css_idx:]

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
print("PapersPage completely rewritten with 3-level tree")