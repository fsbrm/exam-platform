import os

file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "src", "views", "papers", "PapersPage.vue"))
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# New cellStyle with mastery colors
old_style = '''function cellStyle(yd: any, qnum: number) {
  const key = `${yd.year}-${qnum}`
  const q = (yd.questions || []).find((x: any) => x.questionNumber === qnum)
  if (kpMatchSet.value.has(key)) return { background: '#ffeb3b', border: '2px solid #4f7cff' }
  if (!q) return { background: '#f0f0f0', opacity: 0.4 }
  if (!q.done) return { background: '#dbeafe', border: '1px solid #93c5fd' }
  return q.correct ? { background: '#c8e6c9' } : { background: '#ffd6d6' }
}'''

new_style = '''function cellStyle(yd: any, qnum: number) {
  const key = `${yd.year}-${qnum}`
  const q = (yd.questions || []).find((x: any) => x.questionNumber === qnum)
  if (kpMatchSet.value.has(key)) return { background: '#ffeb3b', border: '2px solid #4f7cff' }
  if (!q) return { background: '#f0f0f0', opacity: 0.4 }
  // Mastery takes priority over done/correct
  if (q.mastery === 'mastered') return { background: '#c8e6c9', border: '1px solid #81c784' }
  if (q.mastery === 'unfamiliar') return { background: '#fff3e0', border: '1px solid #ffb74d' }
  if (q.mastery === 'dontknow') return { background: '#ffebee', border: '1px solid #ef9a9a' }
  // Normal done/correct states
  if (!q.done) return { background: '#dbeafe', border: '1px solid #93c5fd' }
  return q.correct ? { background: '#c8e6c9' } : { background: '#ffd6d6' }
}'''

content = content.replace(old_style, new_style)

# Update legend
old_legend = '''<div class="kp-legend">
          <span class="leg-title">图例</span>
          <span><i class="leg-dot" style="background:#e5e7eb"></i>未做</span>
          <span><i class="leg-dot" style="background:#ffd6d6"></i>做错</span>
          <span><i class="leg-dot" style="background:#c8e6c9"></i>做对</span>
          <span><i class="leg-dot" style="background:#ffeb3b;border:2px solid #4f7cff"></i>匹配知识点</span>
        </div>'''

new_legend = '''<div class="kp-legend">
          <span class="leg-title">图例</span>
          <span><i class="leg-dot" style="background:#dbeafe;border:1px solid #93c5fd"></i>未做</span>
          <span><i class="leg-dot" style="background:#c8e6c9;border:1px solid #81c784"></i>掌握/做对</span>
          <span><i class="leg-dot" style="background:#fff3e0;border:1px solid #ffb74d"></i>不熟</span>
          <span><i class="leg-dot" style="background:#ffebee;border:1px solid #ef9a9a"></i>不会/做错</span>
          <span><i class="leg-dot" style="background:#ffeb3b;border:2px solid #4f7cff"></i>匹配</span>
        </div>'''

content = content.replace(old_legend, new_legend)

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Cell colors updated with mastery support")