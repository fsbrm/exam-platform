import os

file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "src", "views", "paper", "QuestionViewPage.vue"))
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

old_mastery = '''function setMastery(level: string) {
  mastery.value = level
  if (question.value) {
    question.value._mastery = level
    const item = allQuestions.value.find((q: any) => q.id === question.value.id)
    if (item) item._mastery = level
  }
  ElMessage.success(`已标记为：${masteryLabel(level)}`)
}'''

new_mastery = '''async function setMastery(level: string) {
  mastery.value = level
  if (question.value) {
    question.value._mastery = level
    const item = allQuestions.value.find((q: any) => q.id === question.value.id)
    if (item) item._mastery = level
  }
  try {
    await api.post(`/user/mastery/${question.value.id}`, { mastery: level })
  } catch {}
  ElMessage.success(`已标记为：${masteryLabel(level)}`)
}'''

content = content.replace(old_mastery, new_mastery)

# Also load mastery on question load
old_load = "if (q._mastery) mastery.value = q._mastery"
new_load = '''// Load mastery from question data
      if (q._mastery) mastery.value = q._mastery
      // Try loading from backend
      try {
        const mres: any = await api.get('/user/mastery')
        if (mres.code === 200 && mres.data[q.id]) {
          mastery.value = mres.data[q.id]
          q._mastery = mres.data[q.id]
        }
      } catch {}'''
content = content.replace(old_load, new_load)

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Mastery save/load updated")