fp = r"D:\桌面\毕设\exam-platform\frontend\src\views\paper\PaperDetailPage.vue"
with open(fp, "r", encoding="utf-8") as f:
    c = f.read()

old = """    if (!currentQuestion.value) return []
    try {
      const opts = typeof currentQuestion.value.options === 'string'
        ? JSON.parse(currentQuestion.value.options)
        : currentQuestion.value.options
      return Array.isArray(opts) ? opts : []
    } catch { return [] }
  })"""

new = """    if (!currentQuestion.value) return []
    try {
      const opts = typeof currentQuestion.value.options === 'string'
        ? JSON.parse(currentQuestion.value.options)
        : currentQuestion.value.options
      if (Array.isArray(opts)) return opts
      if (opts && typeof opts === 'object') {
        return Object.entries(opts).map(([key, value]) => ({ key, value }))
      }
      return []
    } catch { return [] }
  })"""

if old in c:
    c = c.replace(old, new)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(c)
    print("FIXED!")
else:
    print("PATTERN NOT FOUND")
    # Try to find the actual text
    idx = c.find("if (!currentQuestion.value) return []")
    if idx > 0:
        print("Found at", idx)
        print(repr(c[idx:idx+300]))
