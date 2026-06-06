import os, re

file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "src", "views", "papers", "PapersPage.vue"))
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace activeKP with activeNode (supports all levels)
old_active = 'const activeKP = ref<number | null>(null)'
new_active = '''const activeNode = ref<{type: string, id: number} | null>(null)
const activeKP = computed(() => activeNode.value?.type === 'kp' ? activeNode.value.id : null)'''

content = content.replace(old_active, new_active)

# 2. Replace selectKP with selectNode
old_select = '''function selectKP(kpId: number) {
  if (activeKP.value === kpId) {
    activeKP.value = null
    kpMatchSet.value = new Set()
  } else {
    activeKP.value = kpId
    const fastMap = buildKnowledgeMap()
    kpMatchSet.value = fastMap[kpId] || new Set()
  }
}'''

new_select = '''function selectNode(type: string, id: number) {
  if (activeNode.value?.type === type && activeNode.value?.id === id) {
    activeNode.value = null
    kpMatchSet.value = new Set()
  } else {
    activeNode.value = {type, id}
    if (type === 'kp') {
      const fastMap = buildKnowledgeMap()
      kpMatchSet.value = fastMap[id] || new Set()
    }
  }
}
function goPractice() {
  if (!activeNode.value) return
  const {type, id} = activeNode.value
  if (type === 'subject') router.push(`/practice?subjectId=${id}&from=knowledge`)
  else if (type === 'chapter') router.push(`/practice?chapterId=${id}&from=knowledge`)
  else if (type === 'kp') router.push(`/practice?knowledgeId=${id}&subjectId=1&from=knowledge`)
}'''

content = content.replace(old_select, new_select)

# 3. Update L1 (subjects) to be selectable
old_l1 = '''<div class="kp-l1-header" @click="subj._open = !subj._open">
              <span class="kp-arrow">{{ subj._open ? '\u25bc' : '\u25b6' }}</span>
              <span class="kp-l1-icon">{{ subj.icon }}</span>
              <span class="kp-l1-name">{{ subj.name }}</span>
              <span class="kp-l1-badge">{{ subj.totalQuestions }}题</span>
              '''

new_l1 = '''<div class="kp-l1-header" :class="{ selected: activeNode?.type==='subject' && activeNode?.id===subj.id }">
              <span class="kp-arrow" @click="subj._open = !subj._open">{{ subj._open ? '\u25bc' : '\u25b6' }}</span>
              <span class="kp-l1-icon">{{ subj.icon }}</span>
              <span class="kp-l1-name" @click="selectNode('subject', subj.id)">{{ subj.name }}</span>
              <span class="kp-l1-badge">{{ subj.totalQuestions }}题</span>
              <span v-if="activeNode?.type==='subject' && activeNode?.id===subj.id" class="kp-btn" @click.stop="goPractice()">去刷题 &#8594;</span>
              '''

content = content.replace(old_l1, new_l1)

# 4. Update L2 (chapters) to be selectable
old_l2 = '''<div class="kp-l2-header" @click="ch._open = !ch._open">
                  <span class="kp-arrow sm">{{ ch._open ? '\u25bc' : '\u25b6' }}</span>
                  <span class="kp-l2-name">{{ ch.name }}</span>
                  <span class="kp-l2-badge">{{ ch.totalQuestions }}题</span>
                  '''

new_l2 = '''<div class="kp-l2-header" :class="{ selected: activeNode?.type==='chapter' && activeNode?.id===ch.id }">
                  <span class="kp-arrow sm" @click="ch._open = !ch._open">{{ ch._open ? '\u25bc' : '\u25b6' }}</span>
                  <span class="kp-l2-name" @click="selectNode('chapter', ch.id)">{{ ch.name }}</span>
                  <span class="kp-l2-badge">{{ ch.totalQuestions }}题</span>
                  <span v-if="activeNode?.type==='chapter' && activeNode?.id===ch.id" class="kp-btn" @click.stop="goPractice()">去刷题 &#8594;</span>
                  '''

content = content.replace(old_l2, new_l2)

# 5. Update L3 (knowledge points) - remove radio, use highlight + button
old_l3 = '''<div v-for="kp in ch.knowledgePoints" :key="'k'+kp.id" class="kp-l3"
                    :class="{ active: activeKP === kp.id }"
                    @click="selectKP(kp.id)">
                    <span class="kp-l3-radio" :class="{ checked: activeKP === kp.id }"></span>
                    <span class="kp-l3-name">{{ kp.name }}</span>
                    <span v-if="activeKP === kp.id" class="kp-l3-btn" @click.stop="goPracticeByKP(kp.id)">去刷题 &#8594;</span>
                  </div>'''

new_l3 = '''<div v-for="kp in ch.knowledgePoints" :key="'k'+kp.id" class="kp-l3"
                    :class="{ active: activeNode?.type==='kp' && activeNode?.id===kp.id }"
                    @click="selectNode('kp', kp.id)">
                    <span class="kp-l3-name">{{ kp.name }}</span>
                    <span v-if="activeNode?.type==='kp' && activeNode?.id===kp.id" class="kp-btn" @click.stop="goPractice()">去刷题 &#8594;</span>
                  </div>'''

content = content.replace(old_l3, new_l3)

# 6. Remove old individual functions and replace with goPractice
content = content.replace('''function goPracticeBySubject(subjId: number) {
  router.push(`/practice?subjectId=${subjId}&from=knowledge`)
}
function goPracticeByChapter(chId: number) {
  router.push(`/practice?chapterId=${chId}&from=knowledge`)
}
function goPracticeByKP(kpId: number) {
  router.push(`/practice?knowledgeId=${kpId}&subjectId=1&from=knowledge`)
}''', '// goPractice() handles all levels')

# 7. Update CSS - remove radio, add generic kp-btn
# Replace kp-l3-radio + kp-l3-btn with generic kp-btn
content = content.replace('''.kp-l3-radio {
  width: 14px; height: 14px; border-radius: 50%; flex-shrink: 0;
  border: 2px solid #d1d5db; transition: all 0.15s;
}
.kp-l3-radio.checked { border-color: #4f7cff; background: #4f7cff; box-shadow: inset 0 0 0 2px white; }
.kp-l3-name { flex: 1; color: #6b7280; }
.kp-l3.active .kp-l3-name { color: #4f7cff; font-weight: 600; }
.kp-l3-btn {
  font-size: 11px; color: white; background: #4f7cff; padding: 2px 10px;
  border-radius: 10px; cursor: pointer; white-space: nowrap; animation: fadeIn 0.15s;
}
@keyframes fadeIn { from { opacity: 0; transform: translateX(-4px); } to { opacity: 1; transform: translateX(0); } }
.kp-l3-btn:hover { background: #3b6de6; }''', '''.kp-l3-name { flex: 1; color: #6b7280; }
.kp-l3.active .kp-l3-name { color: #4f7cff; font-weight: 600; }

/* Selected state for all levels */
.kp-l1-header.selected, .kp-l2-header.selected { background: #eff6ff; border-radius: 6px; }

/* Floating practice button */
.kp-btn {
  font-size: 11px; color: white; background: #4f7cff; padding: 2px 10px;
  border-radius: 10px; cursor: pointer; white-space: nowrap; animation: fadeIn 0.15s;
  flex-shrink: 0;
}
@keyframes fadeIn { from { opacity: 0; transform: translateX(-4px); } to { opacity: 1; transform: translateX(0); } }
.kp-btn:hover { background: #3b6de6; }''')

# 8. Update computed activeKP to use activeNode
old_kp_computed = ''  # already handled in step 1

# 9. Fix knowledgeMap building - it was using activeKP
# The buildKnowledgeMap and toggleKP functions were already modified

# 10. Remove unused goPracticeByKP, goPracticeBySubject, goPracticeByChapter references in template
# Already done in step 6

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
print("All 3 levels selectable with floating button")