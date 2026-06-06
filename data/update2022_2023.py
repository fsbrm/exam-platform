import json, re, os

# Load existing answers
with open(r"D:\桌面\毕设\exam-platform\data\answers.json", "r", encoding="utf-8") as f:
    answers = json.load(f)

# 2022 answers (from pyPDF2 extraction + pdftotext cross-ref)
answers["2022"] = {
    "source": "pdf_extracted",
    "answers": {
        "1":"B","2":"D","3":"B","4":"C","5":"D","6":"D","7":"B","8":"D","9":"D","10":"A",
        "11":"D","12":"A","13":"B","14":"A","15":"C","16":"A","17":"C","18":"B","19":"D","20":"A",
        "21":"C","22":"C","23":"D","24":"A","25":"C","26":"B","27":"C","28":"D","29":"A","30":"D",
        "31":"B","32":"A","33":"B","34":"C","35":"B","36":"D","37":"B","38":"C","39":"D","40":"B"
    }
}

# 2023 answers (from pdftotext)
answers["2023"] = {
    "source": "pdf_extracted",
    "answers": {
        "1":"D","2":"C","3":"A","4":"B","5":"A","6":"B","7":"B","8":"B","9":"C","10":"C",
        "11":"D","12":"C","13":"A","14":"A","15":"C","16":"B","17":"A","18":"B","19":"C","20":"D",
        "21":"D","22":"C","23":"D","24":"A","25":"C","26":"D","27":"C","28":"D","29":"B","30":"C",
        "31":"B","32":"D","33":"D","34":"C","35":"B","36":"C","37":"D","38":"A","39":"B","40":"D"
    }
}

# Save updated answers
with open(r"D:\桌面\毕设\exam-platform\data\answers.json", "w", encoding="utf-8") as f:
    json.dump(answers, f, ensure_ascii=False, indent=2)
print("answers.json updated with 2022-2023")

# Now update seed-v6.sql SINGLE questions for 2022-2023 with correct answers
with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed-v6.sql", "r", encoding="utf-8") as f:
    seed = f.read()

for year in [2022, 2023]:
    known = answers[str(year)]["answers"]
    # Find SINGLE questions for this year
    pattern = rf"(\(\d+,\d+,\d+,'SINGLE','[^']*','[^']*','\[[^\]]*\]',')([A-D])('[^']*'{year}\))"
    matches = list(re.finditer(pattern, seed))
    
    fixed = 0
    for i, m in enumerate(matches):
        qnum = i + 1
        if qnum > 40: break
        correct = known.get(str(qnum))
        if not correct: continue
        
        current = m.group(2)
        if current != correct:
            old = m.group(0)
            new = m.group(1) + correct + m.group(3)
            seed = seed.replace(old, new, 1)
            fixed += 1
    
    print(f"{year}: fixed {fixed} answers")

with open(r"D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed-v6.sql", "w", encoding="utf-8") as f:
    f.write(seed)
print("seed-v6.sql updated")
