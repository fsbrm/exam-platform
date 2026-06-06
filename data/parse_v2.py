import pdfplumber, os, re, json

pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")
output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "questions_v2.json")

all_data = {}

def extract_answers_separate(text):
    """Try to find a separate answer key block like '1. A  2. B  3. C...'"""
    answers = {}
    # Various answer key formats
    patterns = [
        # Standard: "1．A  2．B" format (common in later years)
        r'(?:参考答案|答案|一.*?选择题.*?答案)[\s\S]{0,100}?((?:\d{1,2}[\.\．\、\)）]\s*[A-D]{1,4}\s+)+)',
        # Compact: "1-5: ABCDD" etc
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            ans_text = m.group(1)
            for am in re.finditer(r'(\d{1,2})[\.\．\、\)）]\s*([A-D]{1,4})', ans_text):
                num = int(am.group(1))
                if 1 <= num <= 40:
                    answers[num] = am.group(2)
            if len(answers) >= 30:
                return answers
    return answers

def extract_answers_inline(text):
    """Extract answers from inline patterns like '解答：B' or '【答案】A'"""
    answers = {}
    patterns = [
        r'(\d{1,2})[\.\．\、\s]+.*?(?:解答|答案|【答案】|【解析】)[：:]\s*([A-D])',
        r'(?:解答|答案)[：:]\s*([A-D]).*?(?:解析|$)',  # More general
    ]
    for pat in patterns:
        for m in re.finditer(pat, text):
            if pat.startswith(r'(\d{1,2})'):
                num = int(m.group(1))
                ans = m.group(2)
            else:
                # Need to find which question this answer belongs to
                # Look backwards for the nearest question number
                before = text[:m.start()]
                q_match = re.findall(r'(\d{1,2})[\.\．\、\)）]', before)
                if not q_match:
                    continue
                num = int(q_match[-1])
                ans = m.group(1)
            if 1 <= num <= 40:
                answers[num] = ans
    return answers

def extract_questions(text):
    """Extract multiple choice questions (Q1-Q40)"""
    questions = []
    # Split text into question blocks
    # Question starts with number. content until next number.
    q_pattern = r'(?:^|\n)\s*(\d{1,2})[\.\．\、\)）]\s*((?:(?!\n\s*\d{1,2}[\.\．\、\)）])[\s\S])+?)' + \
                r'(?=\n\s*\d{1,2}[\.\．\、\)）]\s*\S{5,}|\n\s*二[、\.,]|\Z)'
    
    for m in re.finditer(q_pattern, text):
        num = int(m.group(1))
        if num < 1 or num > 40:
            continue
        content = m.group(2).strip()
        
        # Extract options
        options = {}
        opt_pat = r'\n\s*([A-D])[\.\．\、\s）\)]\s*((?:(?!\n\s*[A-D][\.\．\、\s）\)])[\s\S])+?)(?=\n\s*[A-D][\.\．\、\s）\)]|\n\s*(?:\d{1,2}[\.\．\、\)）]|解答|答案|$))'
        
        for om in re.finditer(opt_pat, content):
            key = om.group(1)
            val = om.group(2).strip()
            options[key] = ' '.join(val.split())[:200]
        
        # Clean content - remove options and answer markers
        clean = content
        clean = re.sub(r'\n\s*[A-D][\.\．\、\s）\)][\s\S]*?(?=\n\s*[A-D][\.\．\、\s）\)]|\n\s*(?:\d{1,2}[\.\．\、\)）]|解答|答案|$))', '', clean)
        clean = re.sub(r'(?:解答|答案)[：:]\s*[A-D]\s*', '', clean)
        clean = ' '.join(clean.split())
        
        questions.append({
            "num": num,
            "content": clean[:600],
            "options": options
        })
    
    return questions

for year in range(2009, 2022):
    pdf_path = os.path.join(pdf_dir, f"{year}.pdf")
    if not os.path.exists(pdf_path):
        print(f"[{year}] PDF not found")
        continue
    
    print(f"[{year}] Processing...", end=" ")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    full_text += t + "\n"
        
        # Try separate answer section first, then inline
        answers = extract_answers_separate(full_text)
        method = "separate"
        if len(answers) < 30:
            answers2 = extract_answers_inline(full_text)
            if len(answers2) > len(answers):
                answers = answers2
                method = "inline"
        
        questions = extract_questions(full_text)
        
        # Merge answers into questions
        for q in questions:
            q["answer"] = answers.get(q["num"], "")
        
        year_data = {
            "year": year,
            "method": method,
            "total": len(questions),
            "with_answer": sum(1 for q in questions if q.get("answer")),
            "questions": questions
        }
        all_data[str(year)] = year_data
        
        print(f"{len(questions)} questions, {year_data['with_answer']} with answers ({method})")
        
    except Exception as e:
        print(f"ERROR: {e}")

# Stats
total_q = sum(d["total"] for d in all_data.values())
total_ans = sum(d["with_answer"] for d in all_data.values())
print(f"\nTotal: {total_q} questions, {total_ans} with answers")

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)
print(f"Saved to {output_file}")