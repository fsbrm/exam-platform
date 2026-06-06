with open(r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue', 'r', encoding='utf-8') as f:
    content = f.read()

# Find list mode section
start = content.find('<!-- LIST MODE')
end = content.find('<!-- SINGLE MODE')
list_section = content[start:end]
print(list_section)
