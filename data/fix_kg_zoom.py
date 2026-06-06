path = r'D:\桌面\毕设\exam-platform\frontend\src\views\knowledge\KnowledgeGraph.vue'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '      scaleLimit: { min: 0.3, max: 5 }'
new = '      zoom: 0.65,\n      scaleLimit: { min: 0.3, max: 5 }'

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Added initial zoom: 0.65')
else:
    print('Pattern not found, searching...')
    # Try finding a close match
    import re
    m = re.search(r'scaleLimit.*?min.*?max', content)
    if m:
        print(f'Found near: {m.group()}')
    else:
        print('No match at all')