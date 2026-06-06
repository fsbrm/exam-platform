import json, os

# Use the current directory
data_dir = r'D:\桌面\毕设\exam-platform\data'
print(f'Data dir exists: {os.path.exists(data_dir)}')
files = os.listdir(data_dir)
print(f'Files: {len(files)}')

# Read questions_raw
qp = os.path.join(data_dir, 'questions_raw.json')
print(f'Reading: {qp}')
print(f'File exists: {os.path.exists(qp)}')
with open(qp, 'r', encoding='utf-8') as f:
    raw = json.load(f)
print(f'Type: {type(raw).__name__}, keys: {sorted(raw.keys()) if isinstance(raw, dict) else "N/A"}')
if isinstance(raw, dict):
    total = sum(len(v) for v in raw.values())
    print(f'Total questions: {total}')
    for y in sorted(raw.keys()):
        arr = raw[y]
        print(f'  {y}: {len(arr)}')
