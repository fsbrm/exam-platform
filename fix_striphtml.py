filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\papers\PapersPage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_strip = """function stripHtml(html: string) {
  if (!html) return ''
  // If has img tag, keep it; otherwise strip all HTML
  if (html.includes('<img')) return html
  return html.replace(/<[^>]*>/g, '')
}"""

new_strip = """function stripHtml(html: string) {
  if (!html) return '(暂无内容)'
  // If it's just an image, show description instead
  const textOnly = html.replace(/<[^>]*>/g, '').trim()
  if (!textOnly && html.includes('<img')) return '📷 查看原题截图'
  // Strip HTML tags for clean text display
  if (html.includes('<img')) {
    return textOnly || '📷 查看原题截图'
  }
  return textOnly
}"""

content = content.replace(old_strip, new_strip)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('stripHtml updated')
