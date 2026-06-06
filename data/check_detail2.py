import pdfplumber, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

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
    
    # Save to file
    txt_file = os.path.join(pdf_dir, f"{year}.txt")
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    print(f"  Saved text to {txt_file}")
    print(f"  Total chars: {len(full_text)}")
    
    # Find all number.letter patterns
    ans_matches = list(re.finditer(r'(\d{1,2})\s*[.\．\、\s]+([A-D])\b', full_text))
    filtered = [(int(m.group(1)), m.group(2)) for m in ans_matches if 1 <= int(m.group(1)) <= 40]
    print(f"  Q1-40 answer patterns: {len(filtered)}")
    if filtered:
        print(f"  First 10: {filtered[:10]}")