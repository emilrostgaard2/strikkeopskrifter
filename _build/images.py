#!/usr/bin/env python3
"""Downloader opskrifts- og garnbilleder fra feeds til assets/img/cache/<md5>.webp (max 900 px),
så sitet ikke hotlinker og Core Web Vitals bliver bedre. Kør i GitHub Actions (kræver internet + pillow).
Filer der allerede findes, springes over. Kør før pages.py."""
import json, os, hashlib, sys, urllib.request, io
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/assets/img/cache"; os.makedirs(OUT, exist_ok=True)
MAX_NEW = int(sys.argv[sys.argv.index("--max")+1]) if "--max" in sys.argv else 400
try:
    from PIL import Image
except ImportError:
    print("pillow mangler – spring over"); sys.exit(0)
def key(url): return hashlib.md5(url.encode()).hexdigest()[:16]
urls = []
ops = json.load(open(f"{ROOT}/data/opskrifter.json", encoding="utf-8"))
urls += [o["image"] for o in ops if o.get("image") and o.get("kind") == "pakke"]
pris = json.load(open(f"{ROOT}/data/priser.json", encoding="utf-8"))
urls += [s["image"] for g in pris.values() for s in g["shops"].values() if s.get("image")]
n = 0
for u in dict.fromkeys(urls):
    dst = f"{OUT}/{key(u)}.webp"
    if os.path.exists(dst): continue
    if n >= MAX_NEW: break
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 strikkeopskrifter.dk"})
        data = urllib.request.urlopen(req, timeout=20).read()
        im = Image.open(io.BytesIO(data)).convert("RGB"); im.thumbnail((900, 900))
        im.save(dst, "WEBP", quality=80, method=4); n += 1
    except Exception as ex:
        print("fejl", u[:80], ex)
print(f"Hentede {n} nye billeder, {len(os.listdir(OUT))} i cache")
