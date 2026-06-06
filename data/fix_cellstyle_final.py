import os

file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "src", "views", "papers", "PapersPage.vue"))
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

old_cellstyle = '''function cellStyle(yd: any, qnum: number) {
  const key = `${yd.year}-${qnum}`
  const q = (yd.questions || []).find((x: any) => x.questionNumber === qnum)
  if (kpMatchSet.value.has(key)) return { background: '#ffeb3b', border: '2px solid #4f7cff' }
  if (!q || !q.done) return { background: '#e5e7eb' }
  return q.correct ? { background: '#c8e6c9' } : { background: '#ffd6d6' }
}'''

new_cellstyle = '''function cellStyle(yd: any, qnum: number) {
  const key = `${yd.year}-${qnum}`
  const q = (yd.questions || []).find((x: any) => x.questionNumber === qnum)
  if (kpMatchSet.value.has(key)) return { background: '#ffeb3b', border: '2px solid #4f7cff' }
  if (!q) return { background: '#f0f0f0', opacity: 0.4 }
  // Mastery colors first
  if (q.mastery === 'mastered') return { background: '#c8e6c9', border: '1px solid #81c784' }
  if (q.mastery === 'unfamiliar') return { background: '#fff3e0', border: '1px solid #ffb74d' }
  if (q.mastery === 'dontknow') return { background: '#ffebee', border: '1px solid #ef9a9a' }
  // Done/correct states
  if (!q.done) return { background: '#dbeafe', border: '1px solid #93c5fd' }
  return q.correct ? { background: '#c8e6c9' } : { background: '#ffd6d6' }
}'''

if old_cellstyle in content:
    content = content.replace(old_cellstyle, new_cellstyle)
    print("cellStyle fixed with mastery colors")
else:
    print("cellStyle pattern not found - searching...")
    idx = content.find('function cellStyle')
    if idx >= 0:
        snippet = content[idx:idx+400]
        print(repr(snippet[:200]))
        # Try with different whitespace
        import re
        # Use regex to replace the function
        pattern = r'function cellStyle\(yd: any, qnum: number\) \{[\s\S]*?^}'
        content = re.sub(pattern, new_cellstyle, content, flags=re.MULTILINE)
        print("Regex replacement done")

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)