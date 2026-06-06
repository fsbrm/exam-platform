path = r'D:\桌面\毕设\exam-platform\frontend\src\views\knowledge\KnowledgeGraph.vue'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the non-working zoom property we added
content = content.replace('\n      zoom: 0.65,\n      scaleLimit:', '\n      scaleLimit:')

# Add auto-zoom after setOption. Find chart.setOption and add timeout after it
old_pattern = '''  chart.off('click')
  chart.on('click', (params: any) => {'''
new_pattern = '''  // Auto-zoom to fit all nodes after force layout settles
  setTimeout(() => {
    try {
      chart.dispatchAction({ type: 'graphRoam', zoom: 0.6 })
    } catch(e) { /* ignore */ }
  }, 400)
  setTimeout(() => {
    try {
      chart.dispatchAction({ type: 'graphRoam', zoom: 0.55 })
    } catch(e) { /* ignore */ }
  }, 1200)

  chart.off('click')
  chart.on('click', (params: any) => {'''

if old_pattern in content:
    content = content.replace(old_pattern, new_pattern)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Added auto-zoom timeout after render')
else:
    print('Pattern not found')