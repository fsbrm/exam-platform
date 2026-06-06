import pdfplumber, os, re, json

pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")
output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "real_questions_v2.sql")

known_answers = {
    2009: {1:'B',2:'C',3:'D',4:'B',5:'C',6:'B',7:'A',8:'D',9:'A',10:'C',
           11:'C',12:'D',13:'C',14:'A',15:'C',16:'D',17:'B',18:'D',19:'A',20:'C',
           21:'B',22:'D',23:'A',24:'B',25:'C',26:'A',27:'B',28:'C',29:'D',30:'A',
           31:'B',32:'C',33:'D',34:'A',35:'C',36:'B',37:'B',38:'D',39:'B',40:'A'},
    2010: {1:'D',2:'C',3:'D',4:'C',5:'B',6:'A',7:'D',8:'C',9:'D',10:'B',
           11:'A',12:'D',13:'C',14:'A',15:'C',16:'D',17:'C',18:'D',19:'C',20:'B',
           21:'A',22:'B',23:'D',24:'A',25:'C',26:'B',27:'A',28:'D',29:'A',30:'C',
           31:'D',32:'B',33:'C',34:'A',35:'D',36:'C',37:'B',38:'A',39:'B',40:'D'},
}

def extract_answers_from_pdf(year):
    pdf_path = os.path.join(pdf_dir, f"{year}.pdf")
    if not os.path.exists(pdf_path): return {}
    with pdfplumber.open(pdf_path) as pdf:
        text = "".join((p.extract_text() or "") + "\n" for p in pdf.pages)
    answers = {}
    for start in ['参考答案', '一、单项选择题参考答案', '答案']:
        idx = text.find(start)
        if idx >= 0:
            for m in re.finditer(r'(\d{1,2})\s*[.\．\、\)〉]\s*([A-D])', text[idx:idx+1500]):
                num = int(m.group(1))
                if 1 <= num <= 40 and num not in answers:
                    answers[num] = m.group(2)
            if len(answers) >= 35: return answers
    for m in re.finditer(r'(\d{1,2})[.\．\、\s].*?解答[：:]\s*([A-D])', text):
        num = int(m.group(1))
        if 1 <= num <= 40 and num not in answers:
            answers[num] = m.group(2)
    return answers

def parse_options(content):
    """Parse A．xxx B．yyy C．zzz D．www format (inline or multi-line)"""
    options = {}
    # Remove answer notes
    content = re.sub(r'解答[：:]\s*[A-D]', '', content)
    
    # Try to find standard pattern: A．text B．text C．text D．text
    # This handles both inline and multi-line
    pat = r'([A-D])\s*[\.\．\、\s）\)]\s*((?:(?!\s*[A-D]\s*[\.\．\、\s）\)])[\s\S])*?)(?=\s*[A-D]\s*[\.\．\、\s）\)]|\s*\d{1,2}\s*[\.\．\、\)）]|\s*$|$)'
    
    matches = list(re.finditer(pat, content))
    for m in matches:
        key = m.group(1)
        val = m.group(2).strip()
        # Clean trailing question numbers or other noise
        val = re.sub(r'\s+\d{1,2}\s*[\.\．\、\)）].*$', '', val)
        val = ' '.join(val.split())[:200]
        if val and key not in options:
            options[key] = val
    
    return options

def extract_questions(year):
    pdf_path = os.path.join(pdf_dir, f"{year}.pdf")
    if not os.path.exists(pdf_path): return []
    
    with pdfplumber.open(pdf_path) as pdf:
        text = "".join((p.extract_text() or "") + "\n" for p in pdf.pages)
    
    # Find question section
    q_end = text.find('二、综合应用题')
    if q_end < 0: q_end = text.find('41．')
    if q_end < 0: q_end = len(text)
    q_section = text[:q_end]
    
    questions = []
    # Split by question numbers
    blocks = re.split(r'\n\s*(?=\d{1,2}[\.\．\、\)）])', q_section)
    
    for block in blocks:
        m = re.match(r'\s*(\d{1,2})[\.\．\、\)）]\s*(.+)', block, re.DOTALL)
        if not m:
            continue
        num = int(m.group(1))
        if num < 1 or num > 40:
            continue
        
        content = m.group(2).strip()
        
        # Clean content - remove everything after the options
        # and keep only question text
        options = parse_options(content)
        
        # Extract question content (remove options part)
        q_content = content
        # Remove from first A. to end
        opt_start = re.search(r'\s*[A-D]\s*[\.\．\、\s）\)]', q_content)
        if opt_start:
            q_content = q_content[:opt_start.start()].strip()
        q_content = ' '.join(q_content.split())
        
        if len(q_content) > 5:
            questions.append({
                "num": num,
                "content": q_content[:600],
                "options": options
            })
    
    return questions

# Generate SQL
sql = ["USE exam_platform;",
       "",
       "-- Clear existing questions",
       "DELETE FROM question_knowledge;",
       "DELETE FROM user_answer; DELETE FROM wrong_question;",
       "DELETE FROM favorite; DELETE FROM note;",
       "DELETE FROM paper_question; DELETE FROM exam_question;",
       "DELETE FROM exam_record; DELETE FROM question;",
       "",
       "INSERT INTO question (id, chapter_id, subject_id, type, difficulty, content, options, answer, analysis, year) VALUES"]

q_id = 1
total = 0
rows = []

for year in range(2009, 2022):
    questions = extract_questions(year)
    answers = known_answers.get(year) or extract_answers_from_pdf(year)
    
    if not questions:
        print(f"[{year}] No questions, skipping")
        continue
    
    yr_count = 0
    for q in questions:
        ans = answers.get(q['num'], '')
        opts = q.get('options', {})
        
        # Only include if we have at least 2 options
        if len(opts) < 2:
            continue
        
        options_json = json.dumps([{"key": k, "value": v} for k, v in sorted(opts.items())], ensure_ascii=False)
        content_sql = q['content'].replace("\\", "\\\\").replace("'", "''")
        options_sql = options_json.replace("\\", "\\\\").replace("'", "''")
        
        ch_id = q['num']  # Use question number as chapter_id for simplicity
        diff = 'EASY' if q['num'] <= 10 else ('MEDIUM' if q['num'] <= 30 else 'HARD')
        
        row = f"({q_id},{ch_id},1,'SINGLE','{diff}','{content_sql}','{options_sql}','{ans}','{year}年408真题第{q['num']}题',{year})"
        rows.append(row)
        q_id += 1
        yr_count += 1
        total += 1
    
    print(f"[{year}] {yr_count} questions with options, {len(answers)} answers")

sql.append(",\n".join(rows) + ";")

with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql))

print(f"\nTotal: {total} questions")
print(f"Saved to: {output_file}")