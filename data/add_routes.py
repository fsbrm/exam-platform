import os

# Update router
router_file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "src", "router", "index.ts"))
with open(router_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Add question route  
old = "{ path: '/paper/:paperId', name: 'paperDetail', component: () => import('@/views/paper/PaperDetailPage.vue') },"
new = "{ path: '/paper/:paperId', name: 'paperDetail', component: () => import('@/views/paper/PaperDetailPage.vue') },\n    { path: '/question/:questionId', name: 'questionView', component: () => import('@/views/paper/QuestionViewPage.vue') },"
content = content.replace(old, new)

# Add /question to public prefixes
old2 = "const publicPrefixes = ['/paper']"
new2 = "const publicPrefixes = ['/paper', '/question']"
content = content.replace(old2, new2)

with open(router_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Router updated")

# Update PapersPage - cell click -> /question/:id
papers_file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "src", "views", "papers", "PapersPage.vue"))
with open(papers_file, 'r', encoding='utf-8') as f:
    pc = f.read()

# Fix goTooltip to navigate to single question
old_gt = 'function goTooltip() {\n  tooltip.visible = false\n  const yd = matrixData.value.find((y: any) => y.year === tooltip.year)\n  const paperId = yd ? yd.paperId : 1\n  router.push(`/paper/${paperId}`)\n}'
new_gt = 'function goTooltip() {\n  tooltip.visible = false\n  if (tooltip.questionId) {\n    router.push(`/question/${tooltip.questionId}?from=matrix`)\n  }\n}'
pc = pc.replace(old_gt, new_gt)

with open(papers_file, 'w', encoding='utf-8') as f:
    f.write(pc)
print("PapersPage updated")