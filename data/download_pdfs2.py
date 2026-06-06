import urllib.request
import os

pdfs = {
    2020: "https://raw.githubusercontent.com/songmuhan/408/master/2020408.pdf",
    2021: "https://raw.githubusercontent.com/songmuhan/408/master/2021408.pdf",
}

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")
os.makedirs(out_dir, exist_ok=True)

for year, url in pdfs.items():
    fname = os.path.join(out_dir, f"{year}.pdf")
    if os.path.exists(fname):
        print(f"[SKIP] {year}.pdf - already exists")
        continue
    try:
        print(f"Downloading {year}...")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            with open(fname, "wb") as f:
                f.write(data)
            print(f"[OK] {year}.pdf ({len(data)} bytes)")
    except Exception as e:
        print(f"[FAIL] {year}: {e}")

print("Done!")