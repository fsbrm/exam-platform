import json

with open(r'D:\桌面\毕设\exam-platform\data\408os_meta.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Check paperId distribution
from collections import Counter
paper_ids = Counter(q['paperId'] for q in data)
print("Paper IDs:", sorted(paper_ids.items()))

# Map paperId to questionIndex range
by_paper = {}
for q in data:
    pid = q['paperId']
    by_paper.setdefault(pid, []).append(q['questionIndex'])

for pid in sorted(by_paper.keys()):
    qis = by_paper[pid]
    print(f"  paperId={pid}: {len(qis)} questions, indices {min(qis)}-{max(qis)}")
