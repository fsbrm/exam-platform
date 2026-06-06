import pdfplumber
import os
import re

pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")

for year in range(2009, 2022):
    pdf_path = os.path.join(pdf_dir, f"{year}.pdf")
    if not os.path.exists(pdf_path):
        print(f"\n{'='*60}")
        print(f"[MISSING] {year}.pdf")
        continue
    
    print(f"\n{'='*60}")
    print(f"[{year}] Analyzing...")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n\n"
            
            # Find answer section
            answer_match = re.search(r'(?:一、单项选择.*?参考答案|参考答案|答案.*?解析|一.*?选择题.*?答案).*?(?=\n\n|\Z)', full_text, re.DOTALL | re.IGNORECASE)
            
            # Count questions found
            q_matches = re.findall(r'(?:^|\n)\s*(\d{1,2})[\.\、\s]\s*([^\n]{10,200}?)(?=\s*(?:A[\.\、\s]|$))', full_text)
            
            print(f"  Pages: {len(pdf.pages)}")
            print(f"  Total chars: {len(full_text)}")
            print(f"  Questions found: {len(q_matches)}")
            
            # Show first 3 questions
            for num, content in q_matches[:3]:
                print(f"  Q{num}: {content[:80]}...")
            
            # Show last 200 chars (usually has answers)
            print(f"\n  --- Last 500 chars ---")
            print(full_text[-500:])
            
    except Exception as e:
        print(f"  ERROR: {e}")