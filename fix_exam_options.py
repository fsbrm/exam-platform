fp = r'D:\桌面\毕设\exam-platform\frontend\src\views\exam\ExamPage.vue'
with open(fp, 'r', encoding='utf-8') as f:
    c = f.read()

old = '''const parsedOptions = computed(() => {
    if (!currentQuestion.value?.options) return []
    try {
      return typeof currentQuestion.value.options === 'string'
        ? JSON.parse(currentQuestion.value.options) : currentQuestion.value.options
    } catch { return [] }
  })'''

new = '''const parsedOptions = computed(() => {
    if (!currentQuestion.value?.options) return []
    try {
      const opts = typeof currentQuestion.value.options === 'string'
        ? JSON.parse(currentQuestion.value.options) : currentQuestion.value.options
      if (Array.isArray(opts)) return opts
      if (opts && typeof opts === 'object') {
        return Object.entries(opts).map(([key, value]) => ({ key, value }))
      }
      return []
    } catch { return [] }
  })'''

c = c.replace(old, new)
with open(fp, 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed')
