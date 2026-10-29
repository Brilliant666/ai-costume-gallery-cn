# -*- coding: utf-8 -*-
"""从 raw/index.html（原站存档）解析内嵌数据 → data/costume.json"""
import json, os, re

base = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(base)
# 原站存档不随仓库分发，只在本地产物里保留
html = open(os.path.join(root, "raw", "index.html"), encoding="utf-8").read()

i = html.find("const D=[")
j = html.index("[", i)
depth = 0
in_str = False
esc = False
quote = ""
arr = None
for k in range(j, len(html)):
    ch = html[k]
    if in_str:
        if esc:
            esc = False
        elif ch == "\\":
            esc = True
        elif ch == quote:
            in_str = False
        continue
    if ch in "\"'":
        in_str = True
        quote = ch
    elif ch == "[":
        depth += 1
    elif ch == "]":
        depth -= 1
        if depth == 0:
            arr = html[j:k+1]
            break

if arr is None:
    raise SystemExit("未找到数据数组")

arr = re.sub(r'([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:', r'\1"\2":', arr)
data = json.loads(arr)

os.makedirs(os.path.join(root, "data"), exist_ok=True)
json.dump(data, open(os.path.join(root, "data", "costume.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

from collections import Counter
print("条目数:", len(data))
print("分类:", dict(Counter(d["カテゴリ"] for d in data)))
print("id 前缀:", dict(Counter(d["id"].split("-")[0] for d in data)))
print("字段:", list(data[0].keys()))
