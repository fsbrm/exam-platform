import requests, re

resp = requests.get("https://www.408os.cn/assets/index-Q0E05wSr.js", timeout=10)
js = resp.text

# Search for login-related config
patterns = [
    r'clientId["\s:]+["\']([^"\']+)["\']',
    r'client_id["\s:]+["\']([^"\']+)["\']',
    r'CLIENT_ID["\s:]+["\']([^"\']+)["\']',
    r'client-id["\s:]+["\']([^"\']+)["\']',
    r'grant_type["\s:]+["\']([^"\']+)["\']',
    r'password["\s:]+["\']([^"\']+)["\']',
    r'login\b.{0,200}client',
]

for p in patterns:
    matches = re.findall(p, js, re.IGNORECASE)
    if matches:
        print(f"Pattern '{p}': {matches[:5]}")

# Also look for login function
idx = js.find('login')
if idx > 0:
    print(f"\nLogin context at {idx}:")
    print(js[max(0,idx-100):idx+300])
