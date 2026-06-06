filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\papers\PapersPage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Tooltip should use v-html or strip HTML
# Change {{ tooltip.content }} to use stripped text
old_tt = '<div class="tt-content">{{ tooltip.content }}</div>'
new_tt = '<div class="tt-content" v-html="stripHtml(tooltip.content)"></div>'
content = content.replace(old_tt, new_tt)

# Add stripHtml function
old_func = 'function goTooltip() {'
new_func = """function stripHtml(html: string) {
  if (!html) return ''
  // If has img tag, keep it; otherwise strip all HTML
  if (html.includes('<img')) return html
  return html.replace(/<[^>]*>/g, '')
}

function goTooltip() {"""
content = content.replace(old_func, new_func)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('PapersPage tooltip fixed')
