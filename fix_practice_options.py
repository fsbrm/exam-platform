fp = r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue'
with open(fp, 'r', encoding='utf-8') as f:
    c = f.read()

old = '''const parsedOptions = computed(() => {
  if (!currentQuestion.value?.options) return []
  try {
    const opts = typeof currentQuestion.value.options === 'string'
      ? JSON.parse(currentQuestion.value.options) : currentQuestion.value.options
    return Array.isArray(opts) ? opts : []
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

# Also fix parsedListOptions
old2 = '''function parsedListOptions(q: any) {
  try {
    const opts = typeof q.options === 'string' ? JSON.parse(q.options) : q.options
    return Array.isArray(opts) ? opts : []
  } catch { return [] }
}'''

new2 = '''function parsedListOptions(q: any) {
  try {
    const opts = typeof q.options === 'string' ? JSON.parse(q.options) : q.options
    if (Array.isArray(opts)) return opts
    if (opts && typeof opts === 'object') {
      return Object.entries(opts).map(([key, value]: [string, any]) => ({ key, value }))
    }
    return []
  } catch { return [] }
}'''

c = c.replace(old2, new2)

with open(fp, 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed')
