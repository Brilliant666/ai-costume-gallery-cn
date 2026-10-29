# -*- coding: utf-8 -*-
"""校验三档文件完整性与分辨率"""
import json, os, struct, sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = json.load(open(os.path.join(root, "manifest.json"), encoding="utf-8"))


def webp_dims(path):
    with open(path, "rb") as f:
        d = f.read(64)
    if d[:4] != b"RIFF" or d[8:12] != b"WEBP":
        return None
    fmt = d[12:16]
    if fmt == b"VP8 ":
        w, h = struct.unpack("<HH", d[26:30])
        return w & 0x3FFF, h & 0x3FFF
    if fmt == b"VP8L":
        b = int.from_bytes(d[21:25], "little")
        return (b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1
    if fmt == b"VP8X":
        return int.from_bytes(d[24:27], "little") + 1, int.from_bytes(d[27:30], "little") + 1
    return None


def png_dims(path):
    with open(path, "rb") as f:
        d = f.read(24)
    if d[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", d[16:24])


TIERS = [("thumb", "thumb_path", webp_dims), ("img", "img_path", webp_dims), ("png", "png_path", png_dims)]
report = {k: {"ok": 0, "missing": [], "bad": [], "bytes": 0, "dims": {}} for k, _, _ in TIERS}

for r in rows:
    for tier, key, fn in TIERS:
        p = os.path.join(root, r[key])
        if not os.path.exists(p):
            report[tier]["missing"].append(r[key])
            continue
        sz = os.path.getsize(p)
        if sz < 512:
            report[tier]["bad"].append((r[key], "size %d" % sz))
            continue
        d = fn(p)
        if d is None:
            report[tier]["bad"].append((r[key], "not an image"))
            continue
        report[tier]["ok"] += 1
        report[tier]["bytes"] += sz
        k = "%dx%d" % d
        report[tier]["dims"][k] = report[tier]["dims"].get(k, 0) + 1

print("总条目:", len(rows), "\n")
total = 0
for tier, _, _ in TIERS:
    t = report[tier]
    total += t["bytes"]
    print("[%-5s] 完好 %d / %d  |  %.1f MB" % (tier, t["ok"], len(rows), t["bytes"] / 1048576))
    print("        分辨率:", t["dims"])
    if t["missing"]:
        print("        缺失 %d: %s" % (len(t["missing"]), t["missing"][:5]))
    if t["bad"]:
        print("        损坏 %d: %s" % (len(t["bad"]), t["bad"][:5]))
    print()
print("三档合计: %.1f MB" % (total / 1048576))

total_ok = sum(report[k]["ok"] for k in report)
if total_ok == 0:
    print("提示：所有文件都缺失，说明还没下载素材。请先运行：")
    print("  python scripts/download.py thumb 16    # 缩略图，约 10 MB")
    print("  python scripts/download.py img 14      # 中图，约 114 MB")
    print("  python scripts/download.py png 14      # 原图，约 1.33 GB（可选）")
    print("下载完成后重新运行本脚本即可校验。")


# [deploy-patch] 存在缺失或损坏文件时返回非零退出码
_missing = sum(len(report[k]["missing"]) for k in report)
_bad = sum(len(report[k]["bad"]) for k in report)
if _missing or _bad:
    print()
    print("校验失败：缺失 %d 项，损坏 %d 项" % (_missing, _bad))
    sys.exit(1)
print()
print("校验通过：全部文件存在且可解码")
