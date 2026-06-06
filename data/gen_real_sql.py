import pdfplumber, os, re, json

pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")
output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "real_questions.sql")

# Known verified answer keys
known_answers = {
    2009: {1:'B',2:'C',3:'D',4:'B',5:'C',6:'B',7:'A',8:'D',9:'A',10:'C',
           11:'C',12:'D',13:'C',14:'A',15:'C',16:'D',17:'B',18:'D',19:'A',20:'C',
           21:'B',22:'D',23:'A',24:'B',25:'C',26:'A',27:'B',28:'C',29:'D',30:'A',
           31:'B',32:'C',33:'D',34:'A',35:'C',36:'B',37:'B',38:'D',39:'B',40:'A'},
    2010: {1:'D',2:'C',3:'D',4:'C',5:'B',6:'A',7:'D',8:'C',9:'D',10:'B',
           11:'A',12:'D',13:'C',14:'A',15:'C',16:'D',17:'C',18:'D',19:'C',20:'B',
           21:'A',22:'B',23:'D',24:'A',25:'C',26:'B',27:'A',28:'D',29:'A',30:'C',
           31:'D',32:'B',33:'C',34:'A',35:'D',36:'C',37:'B',38:'A',39:'B',40:'D'},
    # PDF extracted answers that are mostly complete
    2012: {},
    2014: {},
    2015: {},
    2016: {},
    2017: {},
    2018: {},
    2019: {},
    2021: {},
}

# Extract answers from PDFs for years that worked
def extract_answers_from_pdf(year):
    pdf_path = os.path.join(pdf_dir, f"{year}.pdf")
    if not os.path.exists(pdf_path):
        return {}
    
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            t = page.extract_text()
            if t: text += t + "\n"
    
    answers = {}
    # Look for answer section
    for start in ['参考答案', '一、单项选择题参考答案', '答案']:
        idx = text.find(start)
        if idx >= 0:
            section = text[idx:idx+1500]
            for m in re.finditer(r'(\d{1,2})\s*[.\．\、\)〉]\s*([A-D])', section):
                num = int(m.group(1))
                if 1 <= num <= 40 and num not in answers:
                    answers[num] = m.group(2)
            if len(answers) >= 35:
                return answers
    
    # Inline answers
    for m in re.finditer(r'(\d{1,2})[.\．\、\s].*?解答[：:]\s*([A-D])', text):
        num = int(m.group(1))
        if 1 <= num <= 40 and num not in answers:
            answers[num] = m.group(2)
    
    return answers

def extract_questions_from_pdf(year):
    """Extract question text from PDF"""
    pdf_path = os.path.join(pdf_dir, f"{year}.pdf")
    if not os.path.exists(pdf_path):
        return []
    
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            t = page.extract_text()
            if t: text += t + "\n"
    
    # Find the question section (everything before "二、综合应用题" or Q41)
    q_end = text.find('二、综合应用题')
    if q_end < 0:
        q_end = text.find('41．')
    if q_end < 0:
        q_end = len(text)
    
    q_section = text[:q_end]
    
    questions = []
    
    # Better regex: match question number + content + options  
    # Pattern: "\n1．content\nA．...\nB．...\nC．...\nD．..."
    q_pattern = r'\n\s*(\d{1,2})[\.\．\、\)）]\s*((?:(?!\n\s*\d{1,2}[\.\．\、\)）])[\s\S])+?)(?=\n\s*\d{1,2}[\.\．\、\)）]|\n\s*二[、\.,]|\Z)'
    
    for m in re.finditer(q_pattern, q_section):
        num = int(m.group(1))
        if num < 1 or num > 40:
            continue
        
        content = m.group(2).strip()
        
        # Extract options - handle both inline and multi-line formats
        options = {}
        # Try multi-line first
        opt_pat = r'(?:^|\n)\s*([A-D])[\.\．\、\s）\)]\s*((?:(?!\n\s*[A-D][\.\．\、\s）\)])[\s\S])+?)(?=\n\s*[A-D][\.\．\、\s）\)]|\n\s*\d{1,2}[\.\．\、\)）]|\n\s*解答|\Z)'
        for om in re.finditer(opt_pat, content):
            options[om.group(1)] = ' '.join(om.group(2).split())[:200]
        
        # If no multi-line options, try inline
        if not options:
            inline_pat = r'([A-D])[\.\．\、\s）\)]\s*([^\s]+(?:\s+[^\s]+){0,20}?)(?=\s*[A-D][\.\．\、\s）\)]|$)'
            for om in re.finditer(inline_pat, content):
                options[om.group(1)] = om.group(2).strip()[:200]
        
        # Clean content
        clean = content
        clean = re.sub(r'\n?\s*[A-D][\.\．\、\s）\)][\s\S]*?(?=\n\s*[A-D][\.\．\、\s）\)]|\n\s*\d{1,2}[\.\．\、\)）]|\n\s*解答|\Z)', '', clean)
        clean = re.sub(r'解答[：:]\s*[A-D]', '', clean)
        clean = ' '.join(clean.split())
        
        if len(clean) > 10:  # Minimum content length
            questions.append({
                "num": num,
                "content": clean[:600],
                "options": options
            })
    
    return questions

# Generate SQL
sql_lines = [
    "USE exam_platform;",
    "",
    "-- 408 Real Exam Questions (2009-2021)",
    "-- Generated from real exam PDFs",
    "",
    "-- Clear existing questions",
    "DELETE FROM question_knowledge;",
    "DELETE FROM user_answer;",
    "DELETE FROM wrong_question;",
    "DELETE FROM favorite;",
    "DELETE FROM note;",
    "DELETE FROM paper_question;",
    "DELETE FROM exam_question;",
    "DELETE FROM exam_record;",
    "DELETE FROM question;",
    "",
]

q_id = 1
inserts = []

# Subject mapping
# DS: Q1-11, CO: Q12-22, OS: Q23-32, CN: Q33-40
def get_subject_info(q_num):
    if 1 <= q_num <= 11:
        return 1, q_num  # DS, chapter 1-11
    elif 12 <= q_num <= 22:
        return 1, q_num   # CO
    elif 23 <= q_num <= 32:
        return 1, q_num   # OS  
    else:
        return 1, q_num   # CN

total = 0
for year in range(2009, 2022):
    questions = extract_questions_from_pdf(year)
    answers = known_answers.get(year) or extract_answers_from_pdf(year)
    
    if not questions:
        print(f"[{year}] No questions extracted")
        continue
    
    print(f"[{year}] {len(questions)} questions, {len(answers)} answers")
    
    for q in questions:
        ans = answers.get(q['num'], '')
        opts = q.get('options', {})
        options_json = json.dumps([{"key": k, "value": v} for k, v in sorted(opts.items())], ensure_ascii=False)
        content = q['content'].replace("'", "''").replace('\\', '\\\\')
        
        subj_id, ch_id = get_subject_info(q['num'])
        difficulty = 'EASY' if q['num'] <= 10 else ('MEDIUM' if q['num'] <= 30 else 'HARD')
        q_type = 'SINGLE'
        
        insert = f"({q_id},{ch_id},{subj_id},'{q_type}','{difficulty}','{content}','{options_json}','{ans}','{year}年408真题第{q['num']}题',{year})"
        inserts.append(insert)
        q_id += 1
        total += 1

if inserts:
    sql_lines.append("INSERT INTO question (id, chapter_id, subject_id, type, difficulty, content, options, answer, analysis, year) VALUES")
    for i, ins in enumerate(inserts):
        comma = "," if i < len(inserts) - 1 else ";"
        sql_lines.append(ins + comma)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql_lines))

print(f"\nTotal questions generated: {total}")
print(f"SQL saved to: {output_file}")