import os

file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "src", "views", "papers", "PapersPage.vue"))
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# Add "开始刷题" button after the knowledge tree, before the legend
old_section = '''        </div>
        <div class="kp-legend">'''

new_section = '''        </div>
        <div v-if="activeKP" class="kp-action">
          <el-button type="primary" size="small" @click="goPracticeByKP">
            去刷题 → 相关题目
          </el-button>
        </div>
        <div class="kp-legend">'''

content = content.replace(old_section, new_section)

# Add the goPracticeByKP function
old_func = 'function goTooltip() {'
new_func = '''function goPracticeByKP() {
  if (activeKP.value) {
    router.push(`/practice?knowledgeId=${activeKP.value}&subjectId=1&from=knowledge`)
  }
}

function goTooltip() {'''
content = content.replace(old_func, new_func)

# Add CSS for kp-action
old_css = '.kp-legend { margin-top: 12px;'
new_css = '.kp-action { margin-top: 8px; padding: 8px 0; border-top: 1px solid #e5e7eb; }\n.kp-legend { margin-top: 12px;'
content = content.replace(old_css, new_css)

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Knowledge practice entry added")