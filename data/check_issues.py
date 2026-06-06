import pdfplumber, os, re

pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")

# Check years with answer issues
for year in [2011, 2013, 2020]:
    pdf_path = os.path.join(pdf_dir, f"{year}.pdf")
    print(f"\n{'='*60}")
    print(f"[{year}] Answer section search...")
    
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    
    # Search for answer patterns in last 30% of text
    tail = full_text[-len(full_text)//3:]
    
    # Check for common answer formats
    for pat_name, pat in [
        ("Number.Letter", r'(\d{1,2})\s*[\.\．\、\s]+\s*([A-D])'),
        ("Number答案Letter", r'(\d{1,2})\s*[\.\．\、\s]*答案[：:]*\s*([A-D])'),
        ("Just letters", r'([A-D]{40,})'),
        ("Number.Letter spaced", r'(\d{1,2})\s+([A-D])\s'),
    ]:
        matches = re.findall(pat, tail)
        if matches:
            print(f"  [{pat_name}]: {len(matches)} matches")
            if len(matches) <= 5:
                print(f"    Sample: {matches[:3]}")
    
    # Search for "参考答案" or "答案" sections
    for m in re.finditer(r'(?:参考答案|答案)[\s\S]{0,200}', tail):
        print(f"  Answer section: {m.group()[:200]}")
        break