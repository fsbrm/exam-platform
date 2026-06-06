import os

file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "src", "views", "papers", "PapersPage.vue"))
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove per-node action buttons from template
content = content.replace('<span class="kp-l1-action" @click.stop="goPracticeBySubject(subj.id)">去刷题</span>', '')
content = content.replace('<span class="kp-l2-action" @click.stop="goPracticeByChapter(ch.id)">刷题</span>', '')
content = content.replace('<span class="kp-l3-action" @click.stop="goPracticeByKP(kp.id)">刷</span>', '')

# 2. Add a single contextual action button after the tree (before toggle)
old_toggle = '''        </div>

        <!-- Progress Toggle -->'''

new_toggle = '''        </div>

        <!-- Contextual Action -->
        <div v-if="activeKP" class="kp-action-bar">
          <el-button type="primary" size="small" @click="goPracticeByKP(activeKP)" style="width:100%">
            去刷题 → 该知识点题目
          </el-button>
        </div>

        <!-- Progress Toggle -->'''

content = content.replace(old_toggle, new_toggle)

# 3. Clean up unused CSS
content = content.replace('''.kp-l1-action { font-size: 11px; color: #4f7cff; cursor: pointer; padding: 2px 6px; border-radius: 4px; }
.kp-l1-action:hover { background: #dbeafe; }

''', '')

content = content.replace('''.kp-l2-action { font-size: 10px; color: #4f7cff; cursor: pointer; padding: 1px 5px; border-radius: 3px; }
.kp-l2-action:hover { background: #dbeafe; }

''', '')

content = content.replace('''.kp-l3-action { font-size: 10px; color: #4f7cff; cursor: pointer; padding: 0 4px; border-radius: 2px; display: none; }
.kp-l3:hover .kp-l3-action { display: inline; }
.kp-l3-action:hover { background: #dbeafe; }

''', '')

# 4. Add CSS for action bar
old_prog_css = '/* Progress toggle */'
new_bar_css = '''/* Action bar */
.kp-action-bar { margin-top: 8px; padding: 8px; border-top: 1px solid #e5e7eb; }

/* Progress toggle */'''

content = content.replace(old_prog_css, new_bar_css)

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Cleaned up - single contextual action button")