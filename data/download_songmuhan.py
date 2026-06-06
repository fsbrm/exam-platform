import urllib.request, os

# songmuhan/408 has 2009-2021 individual PDFs
base = "https://raw.githubusercontent.com/songmuhan/408/master/"
out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs2")
os.makedirs(out_dir, exist_ok=True)

for year in range(2009, 2022):
    url = f"{base}{year}408.pdf"
    fname = os.path.join(out_dir, f"{year}.pdf")
    if os.path.exists(fname):
        print(f"[SKIP] {year}.pdf exists")
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