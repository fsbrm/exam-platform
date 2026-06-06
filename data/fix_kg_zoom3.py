path = r'D:\桌面\毕设\exam-platform\frontend\src\views\knowledge\KnowledgeGraph.vue'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the dispatchAction approach with a more reliable setOption approach
old_block = '''  // Auto-zoom to fit all nodes after force layout settles
  setTimeout(() => {
    try {
      chart.dispatchAction({ type: 'graphRoam', zoom: 0.6 })
    } catch(e) { /* ignore */ }
  }, 400)
  setTimeout(() => {
    try {
      chart.dispatchAction({ type: 'graphRoam', zoom: 0.55 })
    } catch(e) { /* ignore */ }
  }, 1200)'''

new_block = '''  // Auto-zoom to fit all nodes after force layout settles
  setTimeout(() => {
    chart.setOption({ series: [{ zoom: 0.52 }] })
  }, 600)
  setTimeout(() => {
    chart.setOption({ series: [{ zoom: 0.52 }] })
  }, 1800)'''

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated to use setOption zoom')
else:
    print('Old block not found, checking...')
    if 'graphRoam' in content:
        print('Found graphRoam reference')
    else:
        print('No graphRoam found')