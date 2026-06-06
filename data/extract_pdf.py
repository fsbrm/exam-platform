import pdfplumber
import os
import glob

pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")
pdfs = glob.glob(os.path.join(pdf_dir, "*.pdf"))
print(f"Found PDFs: {pdfs}")

for pdf_path in pdfs:
    print(f"\n{'='*60}")
    print(f"File: {os.path.basename(pdf_path)}")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Pages: {len(pdf.pages)}")
            for i, page in enumerate(pdf.pages[:3]):
                text = page.extract_text()
                if text:
                    print(f"\n--- Page {i+1} ---")
                    print(text[:1500])
    except Exception as e:
        print(f"Error: {e}")