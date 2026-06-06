import re

file = r"D:\桌面\毕设\exam-platform\frontend\src\views\paper\PaperDetailPage.vue"
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: v-for in left nav grid
content = content.replace(
    'v-for="q in questions" :key="q.id || q.questionNumber"',
    'v-for="(q, idx) in questions" :key="q.id || q.questionNumber"'
)
content = content.replace(
    'active: currentIndex === $index',
    'active: currentIndex === idx'
)
content = content.replace(
    'correct: q.userCorrect === true,\n              wrong: q.userCorrect === false\n            }"\n            @click="currentIndex = $index"',
    'correct: q.userCorrect === true,\n              wrong: q.userCorrect === false\n            }"\n            @click="currentIndex = idx"'
)

# Fix 2: v-for in answer sheet
content = content.replace(
    "v-for=\"q in questions\" :key=\"'s'+q.id\"",
    'v-for="(q2, idx2) in questions" :key="\'s\'+q2.id"'
)

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed all $index references")