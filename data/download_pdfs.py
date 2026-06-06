import urllib.request
import os
import time

# PDF URLs from CodePanda66/CSPostgraduate-408
pdfs = {
    2009: "https://raw.githubusercontent.com/CodePanda66/CSPostgraduate-408/master/408Exam/2009%E5%B9%B4408%E7%9C%9F%E9%A2%98%E5%8F%8A%E7%AD%94%E6%A1%88%E8%A7%A3%E6%9E%90.pdf",
    2010: "https://raw.githubusercontent.com/CodePanda66/CSPostgraduate-408/master/408Exam/2010%E5%B9%B4408%E7%9C%9F%E9%A2%98%E5%8F%8A%E7%AD%94%E6%A1%88%E8%A7%A3%E6%9E%90.pdf",
    2011: "https://raw.githubusercontent.com/CodePanda66/CSPostgraduate-408/master/408Exam/2011%E5%B9%B4%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%80%83%E7%A0%94408%E7%BB%9F%E8%80%83%E7%9C%9F%E9%A2%98%E5%8F%8A%E7%AD%94%E6%A1%88.pdf",
    2012: "https://raw.githubusercontent.com/CodePanda66/CSPostgraduate-408/master/408Exam/2012%E5%B9%B4%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BB%9F%E8%80%83%E7%9C%9F%E9%A2%98%E5%8F%8A%E7%AD%94%E6%A1%88%E8%A7%A3%E6%9E%90.pdf",
    2013: "https://raw.githubusercontent.com/CodePanda66/CSPostgraduate-408/master/408Exam/2013%E5%B9%B4%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%80%83%E7%A0%94408%E7%BB%9F%E8%80%83%E7%9C%9F%E9%A2%98%E5%8F%8A%E7%AD%94%E6%A1%88.pdf",
    2014: "https://raw.githubusercontent.com/CodePanda66/CSPostgraduate-408/master/408Exam/2014%E5%B9%B4%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BB%9F%E8%80%83%E7%9C%9F%E9%A2%98%E5%8F%8A%E8%A7%A3%E6%9E%90.pdf",
    2015: "https://raw.githubusercontent.com/CodePanda66/CSPostgraduate-408/master/408Exam/2015%E5%B9%B4%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%80%83%E7%A0%94408%E7%BB%9F%E8%80%83%E7%9C%9F%E9%A2%98%E5%8F%8A%E7%AD%94%E6%A1%88.pdf",
    2016: "https://raw.githubusercontent.com/CodePanda66/CSPostgraduate-408/master/408Exam/2016%E5%B9%B4%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BB%9F%E8%80%83408%E7%AD%94%E6%A1%88%E5%8F%8A%E8%A7%A3%E6%9E%90.pdf",
    2017: "https://raw.githubusercontent.com/CodePanda66/CSPostgraduate-408/master/408Exam/2017%E5%B9%B4%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BB%9F%E8%80%83408%E7%AD%94%E6%A1%88%E5%8F%8A%E8%A7%A3%E6%9E%90.pdf",
    2018: "https://raw.githubusercontent.com/CodePanda66/CSPostgraduate-408/master/408Exam/2018%E5%B9%B4%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%80%83%E7%A0%94%E7%9C%9F%E9%A2%98%E5%8F%8A%E5%8F%82%E8%80%83%E7%AD%94%E6%A1%88%EF%BC%88%E7%8E%8B%E9%81%93%EF%BC%89.pdf",
    2019: "https://raw.githubusercontent.com/CodePanda66/CSPostgraduate-408/master/408Exam/2019%E5%B9%B4408%E7%BB%9F%E8%80%83%E7%9C%9F%E9%A2%98%E5%8F%8A%E7%AD%94%E6%A1%88%EF%BC%88%E5%90%AB%E7%BB%BC%E5%90%88%E9%A2%98%E8%AF%A6%E7%BB%86%E8%A7%A3%E6%9E%90%EF%BC%89.pdf",
}

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")
os.makedirs(out_dir, exist_ok=True)

for year, url in pdfs.items():
    fname = os.path.join(out_dir, f"{year}.pdf")
    if os.path.exists(fname):
        size = os.path.getsize(fname)
        print(f"[SKIP] {year}.pdf ({size} bytes) - already exists")
        continue
    try:
        print(f"Downloading {year}...")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            with open(fname, "wb") as f:
                f.write(data)
            print(f"[OK] {year}.pdf ({len(data)} bytes)")
        time.sleep(1)
    except Exception as e:
        print(f"[FAIL] {year}: {e}")

print("\nDone!")