fp = r'D:\桌面\毕设\exam-platform\frontend\src\views\paper\QuestionViewPage.vue'
with open(fp, 'r', encoding='utf-8') as f:
    c = f.read()

old = '''function masteryLabel(m: string) {'''
new = '''function stripQvContent(html: string) {
  if (!html) return ''
  return html.replace(/<[^>]*>/g, '').substring(0, 50)
}

function masteryLabel(m: string) {'''
c = c.replace(old, new)
with open(fp, 'w', encoding='utf-8') as f:
    f.write(c)
print('stripQvContent added')
