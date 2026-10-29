# -*- coding: utf-8 -*-
"""三档并发下载器，支持断点续传
用法: python download.py [thumb|img|png] [workers]
"""
import json, os, sys, time, threading
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = json.load(open(os.path.join(root, "manifest.json"), encoding="utf-8"))

tier = sys.argv[1] if len(sys.argv) > 1 else "thumb"
workers = int(sys.argv[2]) if len(sys.argv) > 2 else 12

URL_KEY = {"thumb": "thumb_url", "img": "img_url", "png": "png_url"}[tier]
PATH_KEY = {"thumb": "thumb_path", "img": "img_path", "png": "png_path"}[tier]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
lock = threading.Lock()
done = [0]
failed = []
bytes_total = [0]
t0 = time.time()
total = len(rows)


def fetch(r):
    url, rel = r[URL_KEY], r[PATH_KEY]
    dst = os.path.join(root, rel)
    if os.path.exists(dst) and os.path.getsize(dst) > 1024:
        with lock:
            done[0] += 1
            bytes_total[0] += os.path.getsize(dst)
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Referer": "https://ai-costume-gallery.pages.dev/",
            })
            with urllib.request.urlopen(req, timeout=60) as resp:
                blob = resp.read()
            if len(blob) < 512:
                raise IOError("too small: %d" % len(blob))
            tmp = dst + ".part"
            with open(tmp, "wb") as f:
                f.write(blob)
            os.replace(tmp, dst)
            with lock:
                done[0] += 1
                bytes_total[0] += len(blob)
                n = done[0]
            if n % 200 == 0 or n == total:
                el = time.time() - t0
                print("  %d/%d  %.1f MB  %.1f files/s" % (
                    n, total, bytes_total[0] / 1048576, n / el), flush=True)
            return
        except Exception as e:
            last = e
            time.sleep(1.2 * (attempt + 1))
    with lock:
        failed.append((r["id"], str(last)))


print("tier=%s workers=%d total=%d" % (tier, workers, total), flush=True)
with ThreadPoolExecutor(max_workers=workers) as ex:
    futs = [ex.submit(fetch, r) for r in rows]
    for _ in as_completed(futs):
        pass

el = time.time() - t0
print("\n完成 %d/%d, %.1f MB, 用时 %.0fs" % (
    done[0], total, bytes_total[0] / 1048576, el))
if failed:
    print("失败 %d 条:" % len(failed))
    for i, e in failed[:30]:
        print("  ", i, e)
    json.dump(failed, open(os.path.join(root, "failed_%s.json" % tier), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
else:
    print("无失败")


# [deploy-patch] 有失败条目时返回非零退出码，避免自动化流程误判成功
if failed:
    sys.exit(1)
