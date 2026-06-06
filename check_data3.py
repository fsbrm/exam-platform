import json

data_dir = r'D:\桌面\毕设\exam-platform\data'

# all_comp_q.json details
with open(f'{data_dir}/all_comp_q.json', 'r', encoding='utf-8') as f:
    comp = json.load(f)
print('=== all_comp_q.json detail ===')
for i, c in enumerate(comp[:5]):
    print(f'  [{i}]: {json.dumps(c, ensure_ascii=False)[:200]}')
print('...')
for i in range(max(0,len(comp)-3), len(comp)):
    c = comp[i]
    print(f'  [{i}]: y={c.get("y")}, s={c.get("s")}, ch={c.get("ch")}')

# Check answers detail
with open(f'{data_dir}/answers.json', 'r', encoding='utf-8') as f:
    answers = json.load(f)
print('\n=== answers.json detail ===')
for y in sorted(answers.keys()):
    arr = answers[y]
    for a in arr:
        print(f'  {y}: type={a.get("type")}, answer={str(a.get("answer"))[:80]}')
