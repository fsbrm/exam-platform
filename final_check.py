with open(r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue', 'r', encoding='utf-8') as f:
    content = f.read()

checks = [
    ('答题卡', 'sl-sheet'),
    ('题号导航', 'sl-nav'),
    ('掌握按钮', 'markMastery'),
    ('列表模式掌握', 'markListMastery'),
    ('单题模式', "viewMode === 'single'"),
    ('默认单题', "ref('single')"),
    ('选择题筛选', 'choiceQuestions'),
    ('综合题显示', 'COMPREHENSIVE'),
    ('选项区域', 'sl-options'),
    ('进度条', 'progressPercent'),
]

for name, keyword in checks:
    found = keyword in content
    print(f'  {"[OK]" if found else "[MISSING]"} {name}')
