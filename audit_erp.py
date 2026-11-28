import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("="*60)
print("AUDITING INDEX.HTML (FRONTEND MODULES)")
print("="*60)

# Nav items
nav_matches = re.findall(r'<button[^>]*class="[^"]*nav-item[^"]*"[^>]*data-tab="([^"]+)"[^>]*>([\s\S]*?)</button>', html)
for tab_id, inner in nav_matches:
    clean_text = re.sub(r'<[^>]+>', '', inner).strip()
    print(f"Nav Tab: {tab_id} -> {clean_text}")

# Sections
sections = re.findall(r'<section[^>]*id="([^"]+)"[^>]*class="([^"]*tab-pane[^"]*)"[^>]*>', html)
print("\nSection Panes:")
for sec_id, cls in sections:
    print(f"Section ID: {sec_id} (class: {cls})")

# Tables
tables = re.findall(r'<table[^>]*id="([^"]+)"[^>]*>', html)
print(f"\nTables with IDs ({len(tables)}):")
for t in tables:
    print(f" - #{t}")

print("\n" + "="*60)
print("AUDITING SRC/API/MAIN.PY (BACKEND ENDPOINTS)")
print("="*60)

with open('src/api/main.py', 'r', encoding='utf-8') as f:
    api_code = f.read()

routes = re.findall(r'@app\.(get|post|put|delete)\("([^"]+)"', api_code)
print(f"Total API Routes Found: {len(routes)}")
categories = {}
for method, path in routes:
    prefix = path.split('/')[1] if len(path.split('/')) > 1 else 'root'
    categories.setdefault(prefix, []).append(f"{method.upper()} {path}")

for cat, endpoints in categories.items():
    print(f"\n--- Module: /{cat} ({len(endpoints)} endpoints) ---")
    for ep in endpoints[:8]:
        print(f"  {ep}")
    if len(endpoints) > 8:
        print(f"  ... and {len(endpoints) - 8} more")

print("\n" + "="*60)
print("AUDITING GET APIS AND PARAMETERS")
print("="*60)

with open('src/api/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.strip().startswith('@app.get("/api/'):
        path = line.strip().split('"')[1]
        # find the function definition
        func_def = ""
        for j in range(i+1, min(i+10, len(lines))):
            if lines[j].strip().startswith("def "):
                func_def = lines[j].strip()
                break
        print(f"GET {path} -> {func_def}")
