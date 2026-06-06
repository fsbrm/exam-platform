import pdfplumber, os, re

pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")

for year in [2011, 2021]:
    pdf_path = os.path.join(pdf_dir, f"{year}.pdf")
    print(f"\n{'='*60}")
    print(f"[{year}]")
    
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    
    # Show first 3000 chars  
    print(full_text[:3000])
    print("\n...")
    # Show answer patterns
    ans_matches = list(re.finditer(r'(\d{1,2})\s*[\.\．\、\s]+([A-D])\b', full_text))
    print(f"\nTotal 'num.letter' patterns: {len(ans_matches)}")
    if ans_matches:
        print(f"First 10: {[(m.group(1), m.group(2)) for m in ans_matches[:10]]}")