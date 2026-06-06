filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix line 225 with proper JS template literal
for i, line in enumerate(lines):
    if 'renderedContent' in line and 'computed' in line:
        # Write the JS code directly - use format to avoid issues
        lines[i] = 'const renderedContent = computed(() => {\n'
        lines.insert(i+1, '  const content = currentQuestion.value?.content || \'\'\n')
        lines.insert(i+2, '  const img = currentQuestion.value?.image\n')
        lines.insert(i+3, '    ? <img src="" style="max-width:100%;margin:8px 0;border-radius:6px" />\n')
        lines.insert(i+4, '    : \'\'\n')
        lines.insert(i+5, '  return img + content\n')
        lines.insert(i+6, '})\n')
        # Remove old lines that were part of the original
        break

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Fixed!')

# Verify
with open(filepath, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f.readlines()):
        if 'renderedContent' in line:
            print(f'Line {i+1}: {line.rstrip()}')
        elif i >= 223 and i <= 233:
            print(f'Line {i+1}: {line.rstrip()}')
