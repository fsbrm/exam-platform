import requests

session = requests.Session()

headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic MTQ1NDUzNDQwOEBxcS5jb206MTQ1NDUzNDQwOEBxcS5jb20=",  # base64 of email:password
    "clientId": "e5cd7a2d8f6b4c1a9e3f0d8c7b6a5e4d",  # random guess
}

# Try with the dromara standard auth
resp = session.post(
    "https://www.408os.cn/api/zt/user/login",
    json={
        "email": "1454534408@qq.com",
        "password": "1454534408@qq.com"
    },
    headers=headers,
    timeout=10
)
print(f"With clientId header: {resp.status_code}")
print(resp.text[:500])
print()

# Try without but add clientId in body
resp2 = session.post(
    "https://www.408os.cn/api/zt/user/login",
    json={
        "email": "1454534408@qq.com", 
        "password": "1454534408@qq.com",
        "clientId": "e5cd7a2d8f6b4c1a9e3f0d8c7b6a5e4d"
    },
    timeout=10
)
print(f"With clientId in body: {resp2.status_code}")
print(resp2.text[:500])

# Try the auth/login with password grant
resp3 = session.post(
    "https://www.408os.cn/api/zt/auth/login",
    json={
        "grant_type": "password",
        "username": "1454534408@qq.com",
        "password": "1454534408@qq.com"
    },
    timeout=10
)
print(f"\nAuth login: {resp3.status_code}")
print(resp3.text[:500])
