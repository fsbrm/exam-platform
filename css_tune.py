filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Update the CSS for better text readability
# Find and enhance the sl-q-content and pl-content styles
old_pl_content = '.pl-content { font-size: 15px; line-height: 1.8; margin-bottom: 16px; padding: 12px; background: #f9fafb; border-radius: 8px; }'
new_pl_content = '.pl-content { font-size: 15px; line-height: 2; margin-bottom: 16px; padding: 16px; background: #fafbfc; border-radius: 8px; color: #1f2937; }'

content = content.replace(old_pl_content, new_pl_content)

old_sl_content = '.sl-q-content { font-size: 16px; line-height: 1.8; margin-bottom: 20px; padding: 16px; background: #f9fafb; border-radius: 8px; }'
new_sl_content = '.sl-q-content { font-size: 16px; line-height: 2.2; margin-bottom: 20px; padding: 20px; background: #fafbfc; border-radius: 10px; color: #1f2937; border: 1px solid #f3f4f6; }'

content = content.replace(old_sl_content, new_sl_content)

# Better option styling
old_opt = '.sl-opt { display: flex; align-items: center; gap: 12px; padding: 12px 16px; border: 2px solid #e5e7eb; border-radius: 10px; cursor: pointer; transition: all 0.15s; background: white; }'
new_opt = '.sl-opt { display: flex; align-items: center; gap: 14px; padding: 14px 18px; border: 2px solid #e5e7eb; border-radius: 10px; cursor: pointer; transition: all 0.2s; background: white; font-size: 15px; }'

content = content.replace(old_opt, new_opt)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('CSS updated for better readability')
