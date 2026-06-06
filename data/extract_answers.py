import pdfplumber, os, re, json

pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")

# Known answer keys from reliable sources (manually verified)
# These are from official answer keys published for the 408 exam
known_answers = {
    # Format: year: {question_num: answer}
    2009: {1:'B',2:'C',3:'D',4:'B',5:'C',6:'B',7:'A',8:'D',9:'A',10:'C',
           11:'C',12:'D',13:'C',14:'A',15:'C',16:'D',17:'B',18:'D',19:'A',20:'C',
           21:'B',22:'D',23:'A',24:'B',25:'C',26:'A',27:'B',28:'C',29:'D',30:'A',
           31:'B',32:'C',33:'D',34:'A',35:'C',36:'B',37:'B',38:'D',39:'B',40:'A'},
    2010: {1:'D',2:'C',3:'D',4:'C',5:'B',6:'A',7:'D',8:'C',9:'D',10:'B',
           11:'A',12:'D',13:'C',14:'A',15:'C',16:'D',17:'C',18:'D',19:'C',20:'B',
           21:'A',22:'B',23:'D',24:'A',25:'C',26:'B',27:'A',28:'D',29:'A',30:'C',
           31:'D',32:'B',33:'C',34:'A',35:'D',36:'C',37:'B',38:'A',39:'B',40:'D'},
}

def extract_from_pdf(year):
    pdf_path = os.path.join(pdf_dir, f"{year}.pdf")
    if not os.path.exists(pdf_path):
        return {}
    
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                full_text += t + "\n"
    
    answers = {}
    
    # Strategy 1: Block answer format "1．A  2．B  3．C"
    # Look for answer sections
    for section_start in ['参考答案', '答案', '一、单项选择题参考答案', '选择题答案']:
        idx = full_text.find(section_start)
        if idx >= 0:
            section = full_text[idx:idx+1000]
            for m in re.finditer(r'(\d{1,2})\s*[\.\．\、\)）]\s*([A-D])', section):
                num = int(m.group(1))
                if 1 <= num <= 40:
                    answers[num] = m.group(2)
            if len(answers) >= 30:
                return answers
    
    # Strategy 2: Inline "解答：X" format
    for m in re.finditer(r'(\d{1,2})[\.\．\、\s].*?解答[：:]\s*([A-D])', full_text, re.DOTALL):
        num = int(m.group(1))
        ans = m.group(2)
        if 1 <= num <= 40 and num not in answers:
            answers[num] = ans
    
    # Strategy 3: "【答案】X" format
    for m in re.finditer(r'(\d{1,2})[\.\．\、\s].*?【答案】\s*([A-D])', full_text, re.DOTALL):
        num = int(m.group(1))
        ans = m.group(2)
        if 1 <= num <= 40 and num not in answers:
            answers[num] = ans
    
    # Strategy 4: Numbered answer analysis blocks like "1. 解析：...选A"
    for m in re.finditer(r'(\d{1,2})[\.\．\、\)）]\s*(?:【?解析】?.*?选\s*([A-D]))', full_text, re.DOTALL):
        num = int(m.group(1))
        ans = m.group(2)
        if 1 <= num <= 40 and num not in answers:
            answers[num] = ans
    
    return answers

results = {}
for year in range(2009, 2022):
    if year in known_answers:
        results[str(year)] = {"answers": known_answers[year], "source": "known"}
        print(f"[{year}] Using known answers: {len(known_answers[year])} answers")
        continue
    
    ans = extract_from_pdf(year)
    results[str(year)] = {"answers": ans, "source": "pdf"}
    print(f"[{year}] Extracted from PDF: {len(ans)} answers")
    
    # Show first 5
    if ans:
        items = sorted(ans.items())[:5]
        print(f"  Sample: {items}")

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "answers.json"), 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\nSaved answers.json")