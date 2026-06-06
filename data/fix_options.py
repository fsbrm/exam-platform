import re, json

sql_file = r"D:\桌面\毕设\exam-platform\data\real_questions.sql"
with open(sql_file, 'r', encoding='utf-8') as f:
    content = f.read()

def fix_options(match):
    """Fix inline options that were merged together"""
    options_str = match.group(0)
    # Already properly formatted as JSON array? Check
    try:
        opts = json.loads(options_str)
        if len(opts) == 4:
            return options_str
    except:
        pass
    
    # Try to parse merged options like "A．xxx B．yyy C．zzz D．www"
    # First unescape any SQL escaping
    clean = options_str.replace("''", "'")
    
    # Split by option markers
    parts = re.split(r'(?=[A-D][\.\．\、\s）\)])', clean)
    opts = []
    for part in parts:
        m = re.match(r'([A-D])[\.\．\、\s）\)]\s*(.+)', part)
        if m:
            key = m.group(1)
            val = m.group(2).strip()
            # Remove trailing numbers or other option markers
            val = re.sub(r'\s*[B-D][\.\．\、\s）\)].*$', '', val)
            opts.append({"key": key, "value": val[:200]})
    
    if opts and len(opts) >= 2:
        return json.dumps(opts, ensure_ascii=False).replace("'", "''")
    return options_str

# Find all options JSON in the SQL
fixed = re.sub(r"'\[.*?\]'", fix_options, content)

with open(sql_file, 'w', encoding='utf-8') as f:
    f.write(fixed)

print("Options fixed!")