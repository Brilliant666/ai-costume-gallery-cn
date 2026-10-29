# -*- coding: utf-8 -*-
"""生成 manifest.json / manifest.csv，并把关键词拆成标签"""
import json, os, re, csv

base = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(base)
data = json.load(open(os.path.join(root, "data", "costume.json"), encoding="utf-8"))

BASE_URL = "https://ai-costume-gallery.pages.dev/"

# 分类显示顺序：四季 → 内衣 → 性感 → 泳装 → 派对
CAT_ORDER = ["春", "夏", "秋", "冬", "ランジェリー", "セクシー", "水着", "パーティ"]


def safe(s):
    return re.sub(r'[\\/:*?"<>|]', "_", s).strip().rstrip(".")


rows = []
for d in data:
    cat = safe(d["カテゴリ"])
    pid = safe(d["id"])
    tags = d["キーワード"].split()
    rows.append({
        "id": d["id"],
        "分类": d["カテゴリ"],
        "关键词": d["キーワード"],
        "标签": tags,
        "thumb_url": BASE_URL + d["サムネ"],
        "img_url": BASE_URL + d["画像"],
        "png_url": BASE_URL + d["原寸"],
        "thumb_path": os.path.join("thumbs", cat, pid + ".webp").replace("\\", "/"),
        "img_path": os.path.join("img", cat, pid + ".webp").replace("\\", "/"),
        "png_path": os.path.join("png", cat, pid + ".png").replace("\\", "/"),
    })

rows.sort(key=lambda r: (CAT_ORDER.index(r["分类"]) if r["分类"] in CAT_ORDER else 99, r["id"]))

json.dump(rows, open(os.path.join(root, "manifest.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

with open(os.path.join(root, "manifest.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "分类", "关键词", "标签", "thumb_url", "img_url", "png_url", "thumb_path", "img_path", "png_path"])
    for r in rows:
        w.writerow([r["id"], r["分类"], r["关键词"], " ".join(r["标签"]),
                    r["thumb_url"], r["img_url"], r["png_url"],
                    r["thumb_path"], r["img_path"], r["png_path"]])

from collections import Counter
print("条目:", len(rows))
print("\n分类分布:")
for k, v in Counter(r["分类"] for r in rows).most_common():
    print(f"  {k}: {v}")
toks = Counter(t for r in rows for t in r["标签"])
print(f"\n标签词表: {len(toks)} 个")
print("每件平均标签数: %.1f" % (sum(len(r['标签']) for r in rows) / len(rows)))
