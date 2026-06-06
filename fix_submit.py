filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Update submitListAnswer to store analysis too
old_sub = '''async function submitListAnswer(q: any, qi: number) {
  if (!q._selected) return
  try {
    const res: any = await api.post('/practice/submit', { questionId: q.id, answer: q._selected })
    if (res.code === 200) {
      q._submitted = true
      q._correct = res.data.isCorrect
      q._answer = res.data.answer
      answeredCount.value++
      if (q._correct) correctCount.value++
    }
  } catch {}
}'''

new_sub = '''async function submitListAnswer(q: any, qi: number) {
  if (!q._selected) return
  try {
    const res: any = await api.post('/practice/submit', { questionId: q.id, answer: q._selected })
    if (res.code === 200) {
      q._submitted = true
      q._correct = res.data.isCorrect
      q._answer = res.data.answer || q.answer
      q.analysis = res.data.analysis || q.analysis
      answeredCount.value++
      if (q._correct) correctCount.value++
    }
  } catch {}
}'''

content = content.replace(old_sub, new_sub)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('submitListAnswer updated')
