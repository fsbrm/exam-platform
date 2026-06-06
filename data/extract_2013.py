import pdfplumber, os
pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")
with pdfplumber.open(os.path.join(pdf_dir, "2013.pdf")) as pdf:
    text = ""
    for p in pdf.pages:
        t = p.extract_text()
        if t: text += t + "\n"
with open(os.path.join(pdf_dir, "2013.txt"), "w", encoding="utf-8") as f:
    f.write(text)
print(f"Extracted {len(text)} chars")
