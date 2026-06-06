filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old = """const renderedContent = computed(() => {
  const content = currentQuestion.value?.content || ''
  const img = currentQuestion.value?.image
    ? <img src="" style="max-width:100%;margin:8px 0;border-radius:6px" />
    : ''
  return img + content
})"""

new = """const renderedContent = computed(() => {
  const c = currentQuestion.value?.content || ''
  if (currentQuestion.value?.image) {
    const img = `<img src="${currentQuestion.value.image}" style="max-width:100%;margin:8px 0;border-radius:6px" />`
    return img + c
  }
  return c
})"""

content = content.replace(old, new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open(filepath, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f.readlines()):
        if 'renderedContent' in line or (i >= 224 and i <= 234):
            print(f'Line {i+1}: {line.rstrip()}')
