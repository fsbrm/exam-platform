filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: List mode - change text interpolation to v-html
content = content.replace(
    '<div class="pl-content">{{ q.content }}</div>',
    '<div class="pl-content" v-html="q.content"></div>'
)

# Fix 2: Single mode - don't escape HTML in content since it has <img> tags
# Change renderedContent to use content directly (already has <img> tags)
old_rc = "const renderedContent = computed(() => { const img = currentQuestion.value?.image ? <img src=\"\" style=\"max-width:100%;margin:8px 0;border-radius:6px\" /> : ''; return img + renderText(currentQuestion.value?.content || '') })"
new_rc = "const renderedContent = computed(() => { const img = currentQuestion.value?.image ? <img src=\"\" style=\"max-width:100%;margin:8px 0;border-radius:6px\" /> : ''; return img + (currentQuestion.value?.content || '') })"

content = content.replace(old_rc, new_rc)

# Fix 3: Add COMPREHENSIVE to type label
old_type = "const map: any = { SINGLE: '单选题', MULTI: '多选题', JUDGE: '判断题', FILL: '填空题' }"
new_type = "const map: any = { SINGLE: '单选题', MULTI: '多选题', JUDGE: '判断题', FILL: '填空题', COMPREHENSIVE: '综合题' }"
content = content.replace(old_type, new_type)

# Fix 4: Add COMPREHENSIVE to type tag type
old_type_tag = "const map: any = { SINGLE: '', MULTI: 'warning', JUDGE: 'info', FILL: 'success' }"
new_type_tag = "const map: any = { SINGLE: '', MULTI: 'warning', JUDGE: 'info', FILL: 'success', COMPREHENSIVE: 'danger' }"
content = content.replace(old_type_tag, new_type_tag)

# Fix 5: Handle comprehensive questions - show answer directly, no options needed
# Add a comprehensive answer display section
# Find the result box section and add comprehensive handling
old_result_start = '        <div v-if="showResult" class="result-box"'
new_comp_handle = """        <!-- Comprehensive answer display -->
        <div v-if="currentQuestion?.type === 'COMPREHENSIVE'" class="result-box correct" style="margin-bottom:24px">
          <div class="result-header">
            <span>📝 参考答案</span>
          </div>
          <div class="result-answer" style="margin-top:8px">
            <div v-html="currentQuestion.answer"></div>
          </div>
          <div class="result-analysis" v-if="currentQuestion.analysis" v-html="currentQuestion.analysis" style="margin-top:12px"></div>
        </div>

        <div v-if="showResult" class="result-box" """
content = content.replace(old_result_start, new_comp_handle)

# Fix 6: Hide option selection for comprehensive questions
old_q_opts = '<div class="q-options" v-if="[\'SINGLE\', \'MULTI\'].includes(currentQuestion.type)">'
# Already correct - it only shows for SINGLE and MULTI

# Fix 7: Make the submit button logic handle COMPREHENSIVE
# Find canSubmit and add comprehensive check
content = content.replace(
    "if (currentQuestion.value.type === 'FILL') return selectedAnswer.value.trim().length > 0",
    "if (currentQuestion.value.type === 'COMPREHENSIVE') return false\n  if (currentQuestion.value.type === 'FILL') return selectedAnswer.value.trim().length > 0"
)

# Fix 8: The result analysis using renderText should also use v-html properly
# Actually the renderText for analysis is fine since we want to preserve analysis text formatting
# But for the analysis, we should use v-html to support any HTML in analysis too
# Leave as is for now

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('PracticePage.vue updated!')
