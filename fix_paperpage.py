import re

filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\paper\PaperDetailPage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Change content rendering to v-html
content = content.replace(
    '<img v-if="currentQuestion.image" :src="currentQuestion.image" style="max-width:100%;margin:8px 0;border-radius:4px" />{{ currentQuestion.content }}',
    '<div v-html="currentQuestion.content" class="pd-q-html"></div>'
)

# Fix 2: Update typeLabel to handle COMPREHENSIVE
content = content.replace(
    "return t === 'SINGLE' ? '单选题' : t === 'MULTI' ? '多选题' : t || '单选题'",
    "return t === 'SINGLE' ? '单选题' : t === 'MULTI' ? '多选题' : t === 'COMPREHENSIVE' ? '综合题' : t || '单选题'"
)

# Fix 3: Update title to be more generic  
content = content.replace(
    '<span class="pd-total">{{ questions.length }}道选择题</span>',
    '<span class="pd-total">{{ questions.length }}道题目</span>'
)

# Fix 4: Update empty prompt
content = content.replace(
    '请从左侧选择题号开始答题',
    '请从左侧题号开始答题'
)

# Fix 5: For COMPREHENSIVE questions, show answer directly
# Add computed property for isComprehensive
old_computed = "const diffLabel = computed(() => {"
new_computed = """const isComprehensive = computed(() => currentQuestion.value?.type === 'COMPREHENSIVE')

const diffLabel = computed(() => {"""
content = content.replace(old_computed, new_computed)

# Fix 6: For comprehensive questions, show answer panel instead of options
# Change the options section to hide for comprehensive questions
content = content.replace(
    '<div class="pd-options" v-if="parsedOptions.length > 0">',
    '<div class="pd-options" v-if="parsedOptions.length > 0 && !isComprehensive">'
)

# Fix 7: Add comprehensive answer display before the result section
old_result_section = '<!-- Result -->'
new_comp_section = """<!-- Comprehensive Answer -->'
          <div v-if="isComprehensive" class="pd-result ok">
            <div class="pd-result-header">📝 参考答案</div>
            <div class="pd-result-analysis" v-html="currentQuestion.answer"></div>
            <div class="pd-result-analysis" v-if="currentQuestion.analysis" style="margin-top:12px">
              <strong>解析：</strong>{{ currentQuestion.analysis }}
            </div>
          </div>

          <!-- Result -->"""
# Need to use the actual HTML comment
content = content.replace(
    '          <!-- Result -->',
    """          <!-- Comprehensive Answer -->
          <div v-if="isComprehensive" class="pd-result ok">
            <div class="pd-result-header">📝 参考答案</div>
            <div class="pd-result-analysis" v-html="currentQuestion.answer"></div>
            <div class="pd-result-analysis" v-if="currentQuestion.analysis" style="margin-top:12px">
              <strong>解析：</strong>{{ currentQuestion.analysis }}
            </div>
          </div>

          <!-- Result -->"""
)

# Fix 8: Hide submit button for comprehensive questions
content = content.replace(
    '<el-button v-if="!showResult && selectedAnswer" type="primary" @click="submitAnswer">',
    '<el-button v-if="!showResult && selectedAnswer && !isComprehensive" type="primary" @click="submitAnswer">'
)

# Add CSS for v-html content
content = content.replace(
    '.pd-q-content {',
    '.pd-q-html :deep(img) { max-width: 100%; height: auto; border-radius: 8px; margin: 8px 0; }\n.pd-q-content {'
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('PaperDetailPage.vue updated!')
