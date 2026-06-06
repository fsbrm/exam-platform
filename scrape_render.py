import requests

# The site might use SSR (server-side rendering) for exercise pages
resp = requests.get("https://www.408os.cn/exercise?year=2009&questionId=1", timeout=10)
html = resp.text

# Look for question data in the HTML
import re
# Search for JSON data embedded in the page
patterns = [
    r'window\.__INITIAL_STATE__\s*=\s*({.*?});',
    r'__NUXT__\s*=\s*({.*?});',
    r'<script[^>]*id="__NEXT_DATA__"[^>]*>(.*?)</script>',
    r'<script>window\.__DATA__\s*=\s*(.*?)</script>',
]

for p in patterns:
    m = re.search(p, html, re.DOTALL)
    if m:
        print(f"Found data: {m.group(1)[:500]}")

# Also try looking for <script> tags with application/json
scripts = re.findall(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>', html, re.DOTALL)
for s in scripts:
    print(f"JSON script: {s[:300]}")

# Check if the page has any meaningful content
if "question" in html.lower():
    # Find content around "question"
    idx = html.lower().find("question")
    print(f"\nContent around 'question' at {idx}:")
    print(html[max(0,idx-100):idx+300])
