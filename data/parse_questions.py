import pdfplumber, os, re, json

pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")
output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "questions_raw.json")

all_questions = {}

for year in range(2009, 2022):
    pdf_path = os.path.join(pdf_dir, f"{year}.pdf")
    if not os.path.exists(pdf_path):
        print(f"[{year}] PDF not found, skipping")
        continue
    
    print(f"\n{'='*60}")
    print(f"[{year}] Processing...")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            
            # Find answer key - typically a block of "1. A  2. B  3. C..." or similar
            # Look for patterns like "1．A" or "1.A" or "1、A"  
            answer_lines = []
            answer_patterns = [
                r'(?:参考答案|答案)[\s\S]*?((?:\d{1,2}[\.\．\、\s]+[A-D]{1,4}\s*)+)',
                r'一、单项选择题\s*(?:参考答案|答案)[\s\S]*?((?:\d{1,2}[\.\．\、\s]+[A-D]{1,4}\s*)+)',
            ]
            
            for pat in answer_patterns:
                m = re.search(pat, full_text)
                if m:
                    answer_text = m.group(1)
                    # Parse individual answers
                    for am in re.finditer(r'(\d{1,2})[\.\．\、\s]+([A-D]{1,4})', answer_text):
                        num, ans = int(am.group(1)), am.group(2).strip()
                        if num <= 40:  # Only multiple choice
                            answer_lines.append((num, ans))
                    if answer_lines:
                        break
            
            answers = {num: ans for num, ans in answer_lines}
            print(f"  Found {len(answers)} answers")
            
            # Now extract questions
            questions = []
            # Pattern: question number + content + options
            # Question starts with number followed by . or 、or ．
            q_pattern = r'(?:^|\n)\s*(\d{1,2})[\.\．\、\)）]\s*((?:(?!\n\s*\d{1,2}[\.\．\、\)）])[\s\S])+?)(?=\n\s*\d{1,2}[\.\．\、\)）]|\Z)'
            
            for m in re.finditer(q_pattern, full_text, re.MULTILINE):
                num = int(m.group(1))
                if num > 40:  # Skip big questions
                    break
                content = m.group(2).strip()
                
                # Extract options A/B/C/D
                options = {}
                opt_pattern = r'[A-D][\.\．\、\s）\)]\s*([^\n]{1,200}?)(?=\s*[A-D][\.\．\、\s）\)]|\s*\n\s*(?:\d{1,2}[\.\．\、\)）]|$))'
                for om in re.finditer(opt_pattern, content):
                    options[om.group(0)[0]] = om.group(1).strip()
                
                # Clean content (remove options)
                clean_content = re.sub(r'[A-D][\.\．\、\s）\)][^\n]+', '', content).strip()
                clean_content = ' '.join(clean_content.split())  # Normalize whitespace
                
                questions.append({
                    "num": num,
                    "content": clean_content[:500],
                    "options": {k: v[:200] for k, v in options.items()},
                    "answer": answers.get(num, "")
                })
            
            all_questions[str(year)] = questions
            print(f"  Parsed {len(questions)} questions")
            
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()

# Save raw data
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_questions, f, ensure_ascii=False, indent=2)

total = sum(len(qs) for qs in all_questions.values())
print(f"\n{'='*60}")
print(f"Total questions extracted: {total}")
print(f"Saved to: {output_file}")