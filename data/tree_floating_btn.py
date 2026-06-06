import os

file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "src", "views", "papers", "PapersPage.vue"))
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Make L3 nodes radio-style selectable, show floating button on selected row
old_l3 = '''<div v-for="kp in ch.knowledgePoints" :key="'k'+kp.id" class="kp-l3"
                    :class="{ active: activeKP === kp.id }"
                    @click="toggleKP(kp.id)">
                    <span class="kp-l3-dot" :style="{background: activeKP === kp.id ? '#4f7cff' : '#d1d5db'}"></span>
                    <span class="kp-l3-name">{{ kp.name }}</span>
                    <span class="kp-l3-action" @click.stop="goPracticeByKP(kp.id)">刷</span>
                  </div>'''

new_l3 = '''<div v-for="kp in ch.knowledgePoints" :key="'k'+kp.id" class="kp-l3"
                    :class="{ active: activeKP === kp.id }"
                    @click="selectKP(kp.id)">
                    <span class="kp-l3-radio" :class="{ checked: activeKP === kp.id }"></span>
                    <span class="kp-l3-name">{{ kp.name }}</span>
                    <span v-if="activeKP === kp.id" class="kp-l3-btn" @click.stop="goPracticeByKP(kp.id)">去刷题 &#8594;</span>
                  </div>'''

content = content.replace(old_l3, new_l3)

# 2. Remove the old action bar
old_bar = '''<!-- Contextual Action -->
        <div v-if="activeKP" class="kp-action-bar">
          <el-button type="primary" size="small" @click="goPracticeByKP(activeKP)" style="width:100%">
            去刷题 → 该知识点题目
          </el-button>
        </div>

        <!-- Progress Toggle -->'''

new_bar = '''<!-- Progress Toggle -->'''
content = content.replace(old_bar, new_bar)

# 3. Rename toggleKP to selectKP (single select, not toggle)
content = content.replace('function toggleKP(kpId: number) {', 'function selectKP(kpId: number) {')
# Fix the function body - remove toggle logic, just select
old_toggle_body = '''function selectKP(kpId: number) {
  if (activeKP.value === kpId) {
    activeKP.value = null
    kpMatchSet.value = new Set()
  } else {
    activeKP.value = kpId
    const fastMap = buildKnowledgeMap()
    kpMatchSet.value = fastMap[kpId] || new Set()
  }
}'''

new_select_body = '''function selectKP(kpId: number) {
  if (activeKP.value === kpId) {
    activeKP.value = null
    kpMatchSet.value = new Set()
  } else {
    activeKP.value = kpId
    const fastMap = buildKnowledgeMap()
    kpMatchSet.value = fastMap[kpId] || new Set()
  }
}'''

content = content.replace(old_toggle_body, new_select_body)

# 4. Update CSS - radio style dots + floating button
old_l3_css = '''.kp-l3-dot { width: 5px; height: 5px; border-radius: 50%; flex-shrink: 0; }
.kp-l3-name { flex: 1; color: #6b7280; }
.kp-l3.active .kp-l3-name { color: #4f7cff; }'''

new_l3_css = '''.kp-l3-radio {
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
.kp-l3-btn:hover { background: #3b6de6; }'''

content = content.replace(old_l3_css, new_l3_css)

# 5. Clean up unused action-bar CSS
content = content.replace('''/* Action bar */
.kp-action-bar { margin-top: 8px; padding: 8px; border-top: 1px solid #e5e7eb; }

/* Progress toggle */''', '/* Progress toggle */')

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Tree: radio select + floating button on selected row")