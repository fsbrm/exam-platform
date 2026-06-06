import os

file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend", "src", "main", "java", "com", "exam", "controller", "KnowledgeController.java"))
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# Ensure HashMap and Map are imported
if 'import java.util.HashMap;' not in content:
    content = content.replace('import java.util.*;', 'import java.util.*;\nimport java.util.HashMap;\nimport java.util.LinkedHashMap;\nimport java.util.Map;')

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed KnowledgeController imports")