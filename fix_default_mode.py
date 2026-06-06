filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Change default to 'single' mode
content = content.replace(
    "const viewMode = ref('list')",
    "const viewMode = ref('single')"
)

# Also remove the force-list from knowledge
content = content.replace(
    "if (from === 'knowledge') viewMode.value = 'list'",
    "if (from === 'knowledge') viewMode.value = 'single'"
)

# Add mastery buttons to list mode too
old_list_hd = '''          <div class="pl-card-hd">
            <span class="pl-num">第{{ qi+1 }} 题</span>
            <el-tag size="small">{{ q.difficulty === 'EASY' ? '简单' : q.difficulty === 'MEDIUM' ? '中等' : '困难' }}</el-tag>
            <span v-if="q._submitted" class="pl-result" :class="q._correct ? 'ok' : 'err'">
              {{ q._correct ? '✓ 做对' : '✗ 做错' }}
            </span>
          </div>'''

new_list_hd = '''          <div class="pl-card-hd">
            <span class="pl-num">第{{ qi+1 }} 题</span>
            <el-tag size="small">{{ q.difficulty === 'EASY' ? '简单' : q.difficulty === 'MEDIUM' ? '中等' : '困难' }}</el-tag>
            <span v-if="q._submitted" class="pl-result" :class="q._correct ? 'ok' : 'err'">
              {{ q._correct ? '✓ 做对' : '✗ 做错' }}
            </span>
            <div class="pl-mastery">
              <el-button :type="q._mastery === 'mastered' ? 'success' : ''" size="small" plain @click.stop="markListMastery(q, 'mastered')">掌握</el-button>
              <el-button :type="q._mastery === 'unfamiliar' ? 'warning' : ''" size="small" plain @click.stop="markListMastery(q, 'unfamiliar')">不熟</el-button>
              <el-button :type="q._mastery === 'dontknow' ? 'danger' : ''" size="small" plain @click.stop="markListMastery(q, 'dontknow')">不会</el-button>
            </div>
          </div>'''

content = content.replace(old_list_hd, new_list_hd)

# Add markListMastery function
old_func = 'function resetListQuestion(q: any) {'
new_func = '''async function markListMastery(q: any, level: string) {
  try {
    await api.post('/mastery/mark', { questionId: q.id, level })
    q._mastery = level
    const labels: any = { mastered: '已标记为掌握', unfamiliar: '已标记为不熟', dontknow: '已标记为不会' }
    ElMessage.success(labels[level] || '标记成功')
  } catch {}
}

function resetListQuestion(q: any) {'''
content = content.replace(old_func, new_func)

# Add CSS for list mode mastery buttons
old_pl_hd_css = '.pl-card-hd { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }'
new_pl_hd_css = '.pl-card-hd { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; }\n.pl-mastery { display: flex; gap: 4px; margin-left: auto; }'
content = content.replace(old_pl_hd_css, new_pl_hd_css)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated: default=single, mastery buttons in both modes')
