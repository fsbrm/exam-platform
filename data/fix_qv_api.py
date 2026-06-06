import os

file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "src", "views", "paper", "QuestionViewPage.vue"))
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix saveNote to use correct endpoint
old_note = "await api.post('/note', {\n      questionId: question.value.id,\n      content: noteContent.value\n    })"
new_note = "await api.post(`/user/note/${question.value.id}`, {\n      content: noteContent.value\n    })"
content = content.replace(old_note, new_note)

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed note API endpoint")