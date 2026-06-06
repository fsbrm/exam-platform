import json, os

data_dir = r'D:\桌面\毕设\exam-platform\data'

# all_comp_q.json
cp = os.path.join(data_dir, 'all_comp_q.json')
with open(cp, 'r', encoding='utf-8') as f:
    comp = json.load(f)
print('=== all_comp_q.json ===')
print(f'Type: {type(comp).__name__}, len: {len(comp)}')
if isinstance(comp, list):
    years = sorted(set(c.get('year') for c in comp if c.get('year')))
    print(f'Years: {years}')
    for y in years:
        cnt = sum(1 for c in comp if c.get('year') == y)
        print(f'  {y}: {cnt}')
    if comp:
        c = comp[0]
        print(f'First keys: {list(c.keys())}')
        print(f'Has content: {bool(c.get("content"))}')
        print(f'Has answer: {bool(c.get("answer"))}')

# answers.json
ap = os.path.join(data_dir, 'answers.json')
with open(ap, 'r', encoding='utf-8') as f:
    answers = json.load(f)
print('\n=== answers.json ===')
print(f'Type: {type(answers).__name__}')
if isinstance(answers, list):
    print(f'Total: {len(answers)}')
    types = set(a.get('type') for a in answers)
    print(f'Types: {types}')
    for a in answers[:3]:
        print(f'  year={a.get("year")}, type={a.get("type")}')
elif isinstance(answers, dict):
    print(f'Keys: {sorted(answers.keys())}')
    for k in sorted(answers.keys()):
        print(f'  {k}: {len(answers[k])} items')
