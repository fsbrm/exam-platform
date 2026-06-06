import os

file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "src", "views", "papers", "PapersPage.vue"))
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

old = '.kp-l1-header.selected, .kp-l2-header.selected { background: #eff6ff; border-radius: 6px; }'
new = '.kp-l1-header.selected, .kp-l2-header.selected, .kp-l3.active { background: #eff6ff; border-radius: 6px; }'

content = content.replace(old, new)

# Also fix kp-l3 padding to look better without the radio dot
old_l3 = '''.kp-l3 {
  display: flex; align-items: center; gap: 6px; padding: 3px 6px;'''
new_l3 = '''.kp-l3 {
  display: flex; align-items: center; gap: 6px; padding: 5px 10px;'''

content = content.replace(old_l3, new_l3)

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
print("L3 highlight + padding fixed")