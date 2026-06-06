fp = r'D:\桌面\毕设\exam-platform\frontend\src\views\paper\PaperDetailPage.vue'
with open(fp, 'r', encoding='utf-8') as f:
    c = f.read()

# Fix parsedOptions - the whitespace is different, use simpler replacement
c = c.replace(
    'return Array.isArray(opts) ? opts : []\n  } catch { return [] }\n})\n\nconst typeLabel',
    'if (Array.isArray(opts)) return opts\n      if (opts && typeof opts === '"'"'object'"'"') {\n        return Object.entries(opts).map(([key, value]) => ({ key, value }))\n      }\n      return []\n  } catch { return [] }\n})\n\nconst typeLabel'
)

with open(fp, 'w', encoding='utf-8') as f:
    f.write(c)
print('PaperDetailPage fixed')
