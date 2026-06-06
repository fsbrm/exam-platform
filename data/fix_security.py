import os

file = r"D:\桌面\毕设\exam-platform\backend\src\main\java\com\exam\security\SecurityConfig.java"
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

old = '.requestMatchers("/api/questions/random").permitAll()'
new = '.requestMatchers("/api/questions/random").permitAll()\n                .requestMatchers(HttpMethod.GET, "/api/questions/*").permitAll()'

# Add HttpMethod import if not present
if 'import org.springframework.http.HttpMethod;' not in content:
    content = content.replace(
        'import org.springframework.security.config.annotation.web.builders.HttpSecurity;',
        'import org.springframework.http.HttpMethod;\nimport org.springframework.security.config.annotation.web.builders.HttpSecurity;'
    )

content = content.replace(old, new)

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)

print("SecurityConfig updated")