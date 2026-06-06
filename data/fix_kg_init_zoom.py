path = r'D:\桌面\毕设\exam-platform\frontend\src\views\knowledge\KnowledgeGraph.vue'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the timeout-based zoom attempts 
old_timeout = '''  // Auto-zoom to fit all nodes after force layout settles
  setTimeout(() => {
    chart.setOption({ series: [{ zoom: 0.52 }] })
  }, 600)
  setTimeout(() => {
    chart.setOption({ series: [{ zoom: 0.52 }] })
  }, 1800)'''

if old_timeout in content:
    content = content.replace(old_timeout, '')
    print('Removed timeout zoom attempts')

# Add zoom directly in the initial series config
old_limit = '      scaleLimit: { min: 0.3, max: 5 }'
new_config = '''      zoom: 0.5,
      scaleLimit: { min: 0.2, max: 5 }'''

if old_limit in content:
    content = content.replace(old_limit, new_config)
    print('Added zoom: 0.5 to initial config')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')