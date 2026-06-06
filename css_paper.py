filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\paper\PaperDetailPage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Better content styling
old = '.pd-q-content {'
new = '.pd-q-html { font-size: 16px; line-height: 2.2; color: #1f2937; }\n.pd-q-html :deep(img) { max-width: 100%; height: auto; border-radius: 8px; margin: 8px 0; }\n.pd-q-content {'
content = content.replace(old, new)

# Update content padding
old2 = 'font-size: 16px; line-height: 1.9; padding: 20px; background: white;'
new2 = 'font-size: 16px; line-height: 2.2; padding: 24px; background: white; color: #1f2937;'
content = content.replace(old2, new2)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('PaperDetailPage CSS updated')
