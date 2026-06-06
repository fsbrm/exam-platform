import requests

session = requests.Session()

# Try more login patterns
endpoints = [
    ("https://www.408os.cn/api/zt/user/login", {"email": "1454534408@qq.com", "password": "1454534408@qq.com"}),
    ("https://www.408os.cn/api/zt/user/login", {"username": "1454534408@qq.com", "password": "1454534408@qq.com"}),
    ("https://www.408os.cn/api/zt/user/login", {"phonenumber": "1454534408@qq.com", "password": "1454534408@qq.com"}),
    ("https://www.408os.cn/login", {"email": "1454534408@qq.com", "password": "1454534408@qq.com"}),
    ("https://www.408os.cn/api/login", {"email": "1454534408@qq.com", "password": "1454534408@qq.com"}),
]

headers = {"Content-Type": "application/json"}

for url, data in endpoints:
    try:
        resp = session.post(url, json=data, headers=headers, timeout=10)
        print(f"POST {url}: {resp.status_code}")
        print(f"  {resp.text[:300]}")
        print()
    except Exception as e:
        print(f"POST {url}: ERROR {e}")
        print()

# Try form-encoded
resp2 = session.post("https://www.408os.cn/api/zt/user/login", 
    data={"email": "1454534408@qq.com", "password": "1454534408@qq.com"},
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    timeout=10)
print(f"Form POST: {resp2.status_code}")
print(f"  {resp2.text[:300]}")
