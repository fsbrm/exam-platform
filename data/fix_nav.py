import os

# Use relative path approach
script_dir = os.path.dirname(os.path.abspath(__file__))
file = os.path.normpath(os.path.join(script_dir, "..", "frontend", "src", "views", "papers", "PapersPage.vue"))

with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

old1 = 'function goTooltip() {\n  tooltip.visible = false\n  router.push(`/practice?questionId=${tooltip.questionId}&subjectId=1`)\n}'
new1 = 'function goTooltip() {\n  tooltip.visible = false\n  const yd = matrixData.value.find((y: any) => y.year === tooltip.year)\n  const paperId = yd ? yd.paperId : 1\n  router.push(`/paper/${paperId}`)\n}'

old2 = 'function selectYear(year: number) {\n  // Find paper ID and navigate\n  const yd = matrixData.value.find((y: any) => y.year === year)\n  if (yd) {\n    router.push(`/exam?subjectId=1&paperId=${yd.paperId}`)\n  }\n}'
new2 = 'function selectYear(year: number) {\n  const yd = matrixData.value.find((y: any) => y.year === year)\n  if (yd) {\n    router.push(`/paper/${yd.paperId}`)\n  }\n}'

if old1 in content:
    content = content.replace(old1, new1)
    print("Fixed goTooltip")
else:
    print("old1 not found!")
    # Try to find it
    idx = content.find('function goTooltip')
    if idx >= 0:
        print("goTooltip at", idx)
        print(repr(content[idx:idx+200]))

if old2 in content:
    content = content.replace(old2, new2)
    print("Fixed selectYear")
else:
    print("old2 not found!")

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
print("File saved")