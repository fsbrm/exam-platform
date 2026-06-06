import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"D:\桌面\毕设\exam-platform\frontend\src\views\admin\QuestionManage.vue"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix the three type errors
content = content.replace(
    "{{ {SINGLE:",
    "{{ ({SINGLE:"
)
content = content.replace(
    ':type="{EASY:',
    ':type="({EASY:'
)
content = content.replace(
    "{{ {EASY:",
    "{{ ({EASY:"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done")
