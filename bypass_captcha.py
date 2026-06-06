import requests, json

session = requests.Session()

# Step 1: Get captcha info - common dromara captcha endpoints
captcha_urls = [
    "https://www.408os.cn/api/zt/captcha",
    "https://www.408os.cn/api/zt/captcha/get",
    "https://www.408os.cn/api/captcha",
    "https://www.408os.cn/captcha",
    "https://www.408os.cn/api/zt/user/captcha",
    "https://www.408os.cn/code",
]

for url in captcha_urls:
    try:
        resp = session.get(url, timeout=5)
        print(f"{url}: {resp.status_code} - {resp.text[:200]}")
    except:
        pass

# Step 2: Try to get captcha image
resp2 = session.get("https://www.408os.cn/api/zt/captcha/image", timeout=5)
print(f"\nCaptcha image: {resp2.status_code}")
if resp2.status_code == 200:
    print(resp2.headers.get('content-type'))
    print(resp2.text[:200])
