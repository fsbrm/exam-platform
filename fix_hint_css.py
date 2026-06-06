filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Update pl-hint CSS
old_pl_hint = '.pl-hint { margin-top: 10px; padding: 10px 14px; background: #fffbe6; border-radius: 8px; border: 1px solid #ffe58f; font-size: 13px; color: #ad6800; line-height: 1.6; }\n.pl-hint-icon { margin-right: 4px; }'
new_pl_hint = '.pl-hint { margin-top: 8px; padding: 10px 14px; background: #fffbe6; border-radius: 8px; border: 1px solid #ffe58f; font-size: 13px; color: #ad6800; line-height: 1.6; }\n.pl-hint-icon { margin-right: 4px; }\n.pl-hint-stage { display: flex; align-items: center; gap: 4px; margin-bottom: 4px; }\n.pl-hint-label { font-size: 11px; font-weight: 700; color: #ad6800; background: #fff1b8; padding: 1px 6px; border-radius: 3px; }\n.pl-hint-text { color: #8c6d00; }'
content = content.replace(old_pl_hint, new_pl_hint)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('CSS updated')
