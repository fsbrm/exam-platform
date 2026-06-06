filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the list mode cards
old_list_card = '''        <div v-for="(q, qi) in questions.filter(q => q.type !== 'COMPREHENSIVE')" :key="q.id" class="pl-card" :id="'q-'+q.id">
          <div class="pl-card-hd">
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
          </div>
          <div class="pl-content" v-html="q.content"></div>
          <div class="pl-options" v-if="parsedListOptions(q).length">
            <div v-for="opt in parsedListOptions(q)" :key="opt.key"
              class="pl-opt"
              :class="{
                selected: q._selected === opt.key && !q._submitted,
                correct: q._submitted && (opt.key === q.answer || q._answer),
                wrong: q._submitted && q._selected === opt.key && opt.key !== q.answer
              }"
              @click="selectListOption(q, opt.key)">
              <span class="pl-opt-key">{{ opt.key }}</span>
              <span class="pl-opt-val">{{ opt.value }}</span>
            </div>
          </div>
          <div class="pl-actions">
            <el-button v-if="!q._submitted && q._selected" type="primary" size="small" @click="submitListAnswer(q, qi)">提交</el-button>
            <el-button v-if="q._submitted" size="small" @click="resetListQuestion(q)">重做</el-button>
          </div>
        </div>'''

new_list_card = '''        <div v-for="(q, qi) in questions.filter(q => q.type !== 'COMPREHENSIVE')" :key="q.id" class="pl-card" :id="'q-'+q.id">
          <div class="pl-card-hd">
            <span class="pl-num">第{{ qi+1 }} 题</span>
            <el-tag size="small">{{ q.difficulty === 'EASY' ? '简单' : q.difficulty === 'MEDIUM' ? '中等' : '困难' }}</el-tag>
            <span class="pl-type-tag">{{ q.type === 'SINGLE' ? '单选' : '多选' }}</span>
            <span v-if="q._submitted" class="pl-result" :class="q._correct ? 'ok' : 'err'">
              {{ q._correct ? '✓ 做对' : '✗ 做错' }}
            </span>
            <div class="pl-mastery">
              <el-button :type="q._mastery === 'mastered' ? 'success' : ''" size="small" plain @click.stop="markListMastery(q, 'mastered')">掌握</el-button>
              <el-button :type="q._mastery === 'unfamiliar' ? 'warning' : ''" size="small" plain @click.stop="markListMastery(q, 'unfamiliar')">不熟</el-button>
              <el-button :type="q._mastery === 'dontknow' ? 'danger' : ''" size="small" plain @click.stop="markListMastery(q, 'dontknow')">不会</el-button>
            </div>
          </div>
          <div class="pl-content" v-html="q.content"></div>
          <div class="pl-options" v-if="parsedListOptions(q).length">
            <div v-for="opt in parsedListOptions(q)" :key="opt.key"
              class="pl-opt"
              :class="{
                selected: q._selected === opt.key && !q._submitted,
                correct: q._submitted && (opt.key === q.answer || q._answer),
                wrong: q._submitted && q._selected === opt.key && opt.key !== q.answer
              }"
              @click="selectListOption(q, opt.key)">
              <span class="pl-opt-key">{{ opt.key }}</span>
              <span class="pl-opt-val">{{ opt.value }}</span>
              <span class="pl-opt-icon" v-if="q._submitted && opt.key === (q._answer || q.answer)">✓</span>
              <span class="pl-opt-icon err" v-if="q._submitted && q._selected === opt.key && opt.key !== (q._answer || q.answer)">✗</span>
            </div>
          </div>
          <!-- Answer & Analysis after submission -->
          <div v-if="q._submitted" class="pl-answer">
            <div class="pl-answer-hd">
              <span :style="{color: q._correct ? '#52c41a' : '#ff4d4f', fontWeight:700}">
                {{ q._correct ? '✅ 回答正确' : '❌ 回答错误' }}
              </span>
              <span v-if="!q._correct" style="margin-left:8px">正确答案：<strong>{{ q._answer || q.answer }}</strong></span>
            </div>
            <div class="pl-answer-body" v-if="q.analysis" v-html="q.analysis"></div>
            <div class="pl-answer-body" v-else style="color:#9ca3af;font-style:italic">暂无解析</div>
          </div>
          <!-- Hint -->
          <div v-if="q._showHint" class="pl-hint">
            <span class="pl-hint-icon">💡</span> {{ q._hint || '请仔细审题，注意排除干扰选项，结合知识点分析。' }}
          </div>
          <!-- Notes -->
          <div v-if="q._showNote" class="pl-note-box">
            <el-input v-model="q._note" type="textarea" :rows="2" placeholder="记录你的思路或笔记..." size="small" />
          </div>
          <!-- Action bar -->
          <div class="pl-actions">
            <el-button v-if="!q._submitted && q._selected" type="primary" size="small" @click="submitListAnswer(q, qi)">提交答案</el-button>
            <el-button v-if="q._submitted" size="small" @click="resetListQuestion(q)">重做</el-button>
            <el-button v-if="!q._submitted" size="small" plain @click="q._showHint = !q._showHint; if(!q._hint) q._hint='请仔细审题，注意排除干扰选项，结合知识点分析。'">💡 {{ q._showHint ? '隐藏提示' : '提示' }}</el-button>
            <el-button size="small" plain @click="q._showNote = !q._showNote">📝 {{ q._showNote ? '收起笔记' : '笔记' }}</el-button>
            <el-button size="small" plain @click="openVideoSearch(q)">🎬 相关视频</el-button>
            <el-button size="small" plain @click="openListAiChat(q)">🤖 AI分析</el-button>
            <el-button size="small" plain @click="toggleListFavorite(q)">
              {{ q._favorited ? '⭐ 已收藏' : '☆ 收藏' }}
            </el-button>
          </div>
        </div>'''

content = content.replace(old_list_card, new_list_card)

# Add new functions for list mode
old_func_end = 'function goBack() {'
new_funcs = '''async function openVideoSearch(q: any) {
  const keyword = encodeURIComponent((q.content || '').substring(0, 30))
  window.open(`https://www.bilibili.com/search?keyword=${keyword}%20%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%80%83%E7%A0%94`, '_blank')
}

function openListAiChat(q: any) {
  router.push(`/ai?question=${encodeURIComponent(q.content || '')}&id=${q.id}`)
}

async function toggleListFavorite(q: any) {
  try {
    if (q._favorited) {
      await api.delete(`/favorites/${q.id}`)
      q._favorited = false
      ElMessage.success('已取消收藏')
    } else {
      await api.post('/favorites', { questionId: q.id })
      q._favorited = true
      ElMessage.success('已收藏')
    }
  } catch {}
}

function goBack() {'''

content = content.replace(old_func_end, new_funcs)

# Update initState to include new fields
old_init = '''function initState(data: any[]) {
  return (data || []).map((q: any) => ({
    ...q,
    _selected: null,
    _submitted: false,
    _correct: null
  }))
}'''

new_init = '''function initState(data: any[]) {
  return (data || []).map((q: any) => ({
    ...q,
    _selected: null,
    _submitted: false,
    _correct: null,
    _showHint: false,
    _hint: null,
    _showNote: false,
    _note: '',
    _favorited: false
  }))
}'''

content = content.replace(old_init, new_init)

# Now add the CSS for new elements
old_css_end = '@media (max-width: 900px) {'
new_css = '''/* List Mode Enhancements */
.pl-type-tag { font-size: 11px; padding: 1px 6px; border-radius: 3px; background: #f0f4ff; color: #4f7cff; }
.pl-opt-icon { color: #52c41a; font-size: 16px; margin-left: auto; }
.pl-opt-icon.err { color: #ff4d4f; }

.pl-answer { margin-top: 12px; padding: 14px; background: #f9fafb; border-radius: 8px; border-left: 3px solid #4f7cff; }
.pl-answer-hd { font-size: 14px; margin-bottom: 6px; }
.pl-answer-body { font-size: 13px; line-height: 1.7; color: #6b7280; margin-top: 6px; }

.pl-hint { margin-top: 10px; padding: 10px 14px; background: #fffbe6; border-radius: 8px; border: 1px solid #ffe58f; font-size: 13px; color: #ad6800; line-height: 1.6; }
.pl-hint-icon { margin-right: 4px; }

.pl-note-box { margin-top: 10px; }

.pl-actions { margin-top: 12px; display: flex; gap: 6px; flex-wrap: wrap; }

@media (max-width: 900px) {'''

content = content.replace(old_css_end, new_css)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('List mode fully enhanced!')
