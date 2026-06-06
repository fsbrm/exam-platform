filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\paper\PaperDetailPage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure the paper detail page also shows clean text
# The v-html should work fine for text content
# But let's update the title to properly count question types
content = content.replace(
    '<span class="pd-total">{{ questions.length }}道题目</span>',
    '<span class="pd-total">{{ questions.length }}道题目（含选择题和综合题）</span>'
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('PaperDetailPage updated')
