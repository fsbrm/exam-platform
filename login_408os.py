import requests, json

session = requests.Session()

# Try to find the login endpoint
login_urls = [
    "https://www.408os.cn/api/zt/user/login",
    "https://www.408os.cn/api/login",
    "https://www.408os.cn/api/auth/login",
    "https://www.408os.cn/api/zt/login",
    "https://www.408os.cn/api/user/login",
]

creds = {"email": "1454534408@qq.com", "password": "1454534408@qq.com"}

for url in login_urls:
    try:
        resp = session.post(url, json=creds, timeout=10)
        print(f"{url}: {resp.status_code} - {resp.text[:200]}")
        if resp.status_code == 200 and '"code":200' in resp.text:
            print(f"  LOGIN SUCCESS! Token: {resp.json().get('data', {}).get('token', 'N/A')}")
            # Save session cookies
            break
    except Exception as e:
        print(f"{url}: ERROR - {e}")

# Try with different field names
alt_creds = [
    {"username": "1454534408@qq.com", "password": "1454534408@qq.com"},
    {"account": "1454534408@qq.com", "password": "1454534408@qq.com"},
]

for url in login_urls:
    for creds in alt_creds:
        try:
            resp = session.post(url, json=creds, timeout=10)
            if '"code":200' in resp.text or '"code":0' in resp.text:
                print(f"{url} with {list(creds.keys())}: SUCCESS - {resp.text[:200]}")
                break
        except:
            pass
