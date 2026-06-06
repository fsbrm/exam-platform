import subprocess

# Read seed.sql as bytes to avoid encoding issues
with open(r"D:\seed_temp.sql", "rb") as f:
    sql_bytes = f.read()

# Remove BOM if present
if sql_bytes.startswith(b"\xef\xbb\xbf"):
    sql_bytes = sql_bytes[3:]

result = subprocess.run(
    [r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
     "--default-character-set=utf8mb4",
     "-u", "root", "-p123456", "exam_platform"],
    input=sql_bytes,
    capture_output=True, timeout=60
)

print("STDOUT:", result.stdout.decode("utf-8", errors="replace")[-300:])
stderr_text = result.stderr.decode("utf-8", errors="replace")
if stderr_text.strip():
    print("STDERR:", stderr_text[-500:])
print("Return:", result.returncode)
