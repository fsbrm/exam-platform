filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Update renderedContent to just pass content (already clean text)
old_rc = """const renderedContent = computed(() => {
  const c = currentQuestion.value?.content || ''
  if (currentQuestion.value?.image) {
    const img = <img src="" style="max-width:100%;margin:8px 0;border-radius:6px" />
    return img + c
  }
  return c
})"""

new_rc = """const renderedContent = computed(() => {
  const c = currentQuestion.value?.content || ''
  const img = currentQuestion.value?.image
  // Only add image for comprehensive questions where it helps
  if (img && currentQuestion.value?.type === 'COMPREHENSIVE') {
    return <img src="" style="max-width:100%;margin:8px 0;border-radius:8px;border:1px solid #e5e7eb" /><br/>
  }
  if (img) {
    return <img src="" style="max-width:100%;margin:4px 0;border-radius:6px" /><br/>
  }
  return c
})"""

content = content.replace(old_rc, new_rc)

# Also update the list mode to not filter comprehensive - show all
# Actually keep the filter for now, comprehensive should be separate

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('PracticePage updated')
