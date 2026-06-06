filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the currentQuestion computed and add choiceQuestions after it
old = 'const currentQuestion = computed(() => questions.value[currentIndex.value] || null)'
new = '''const currentQuestion = computed(() => questions.value[currentIndex.value] || null)

// Only multiple choice questions (排除综合题)
const choiceQuestions = computed(() => questions.value.filter(q => q.type !== 'COMPREHENSIVE'))'''
content = content.replace(old, new)

# Add loadAnswer function before onMounted
old_ma = 'onMounted(async () => {'
new_ma = '''function loadAnswer(idx: number) {
  if (idx < 0 || idx >= questions.value.length) return
  const q = questions.value[idx]
  currentIndex.value = idx
  selectedAnswer.value = q._selected || ''
  showResult.value = !!q._submitted
  if (q._submitted) {
    lastCorrect.value = !!q._correct
    correctAnswer.value = q._answer || q.answer || ''
  }
}

onMounted(async () => {'''
content = content.replace(old_ma, new_ma)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Script updated!')
