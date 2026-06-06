import requests, json, pymysql

# Try to get all available data without auth
url = "https://www.408os.cn/api/zt/question/list"
all_questions = []

# Try with pagination
for page in range(1, 20):
    try:
        resp = requests.get(url, params={"page": page, "pageSize": 100}, timeout=10)
        if resp.status_code != 200:
            break
        data = resp.json()
        if data.get("code") == 401:
            print(f"Page {page}: auth required")
            break
        rows = data.get("rows", [])
        if not rows:
            break
        all_questions.extend(rows)
        print(f"Page {page}: got {len(rows)} questions (total so far: {len(all_questions)})")
    except Exception as e:
        print(f"Page {page} error: {e}")
        break

print(f"\nTotal questions from API: {len(all_questions)}")

if all_questions:
    years = set(q.get("year") for q in all_questions)
    print(f"Years: {sorted(years)}")
    
    # Show sample
    for q in all_questions[:5]:
        print(f"  Q{q.get('questionIndex')}: type={q.get('questionType')} answer={q.get('answer')} score={q.get('score')} year={q.get('year')}")

    # Save for reference
    with open(r'D:\桌面\毕设\exam-platform\data\408os_meta.json', 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)
    print("Saved to 408os_meta.json")
