#!/usr/bin/env python3
"""
Henter materialelisten (gram pr. størrelse, strikkefasthed, pinde) fra DROPS' egne opskriftssider
for hver Drops-garnpakke i data/opskrifter.json. Resultatet caches i data/drops-details.json,
så hver opskrift kun hentes én gang. Kør i GitHub Actions (kræver internet):

    python3 _build/drops.py            # henter op til MAX_NEW nye pr. kørsel
    python3 _build/drops.py --max 200

Flow pr. opskrift: Rito-produktside (htmlurl fra affiliate-linket) → link til garnstudio.com
→ opskriftsside → parse "Materialer"-afsnittet. Fejler noget, springes opskriften over og prøves igen næste nat.
"""
import json, os, re, sys, time, html, urllib.request, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = f"{ROOT}/data/drops-details.json"
MAX_NEW = int(sys.argv[sys.argv.index("--max")+1]) if "--max" in sys.argv else 120
UA = {"User-Agent": "Mozilla/5.0 (compatible; strikkeopskrifter.dk/1.0; +https://strikkeopskrifter.dk/om/)"}

def get(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode(r.headers.get_content_charset() or "utf-8", "replace")

def target(vareurl):
    q = urllib.parse.parse_qs(urllib.parse.urlparse(vareurl).query)
    return q.get("htmlurl", [""])[0]

SIZE_RE = re.compile(r"\b(XS|S|M|L|XL|XXL|XXXL|2XL|3XL|4XL|5XL|6XL|\d{1,2}(?:/\d{1,2})?(?:\s*(?:år|mdr|måneder))?)\b")
def parse_garnstudio(htm):
    """Returnerer {sizes:[...], yarns:[{name, grams:[...]}], gauge:'', needles:[...]} eller None"""
    t = html.unescape(re.sub(r"<[^>]+>", " ", htm))
    t = re.sub(r"\s+", " ", t)
    m = re.search(r"(?:Størrelse|Størrelser|STØRRELSE)[^:]*:\s*([^\n]{3,120}?)(?:\s(?:Færdige|Materialer|MATERIALER|Garn|GARN|Overvidde|Bryst))", t, re.I)
    sizes = []
    if m:
        for x in re.split(r"\s*[-–]\s*|\s+", m.group(1).strip()):
            if not x: continue
            if SIZE_RE.fullmatch(x): sizes.append(x)
            else: break
    yarns = []
    for ym in re.finditer(r"(DROPS\s+[A-ZÆØÅ][A-ZÆØÅa-zæøå\- ]{2,30}?)\s+fra\s+Garnstudio[^0-9]{0,60}?((?:\d{2,4}\s*-\s*){1,12}\d{2,4})\s*g", t):
        name = " ".join(w.capitalize() if w.isupper() else w for w in ym.group(1).split())
        grams = [int(x) for x in re.findall(r"\d{2,4}", ym.group(2))]
        yarns.append({"name": name, "grams": grams})
    if not yarns:  # variant uden "fra Garnstudio"
        for ym in re.finditer(r"(DROPS\s+[A-ZÆØÅ][A-Za-zæøåÆØÅ\- ]{2,30})[^0-9]{0,40}?((?:\d{2,4}\s*-\s*){1,12}\d{2,4})\s*g\b", t):
            name = " ".join(w.capitalize() if w.isupper() else w for w in ym.group(1).split())
            yarns.append({"name": name, "grams": [int(x) for x in re.findall(r"\d{2,4}", ym.group(2))]})
    gauge = ""
    gm = re.search(r"(?:STRIKKEFASTHED|Strikkefasthed)[^:]*:\s*([^.]{5,120}\.)", t)
    if gm: gauge = gm.group(1).strip()
    needles = sorted({x.replace(",", ".") for x in re.findall(r"(?:RUNDPIND|PIND|STRØMPEPIND|Rundpind|Pind)[^0-9]{0,30}?(\d{1,2}(?:[.,]5)?)\s*mm", t)}, key=float)
    if not yarns: return None
    return {"sizes": sizes, "yarns": yarns, "gauge": gauge, "needles": needles}

def find_garnstudio_link(htm):
    m = re.search(r'href="(https?://(?:www\.)?garnstudio\.com/pattern\.php\?id=\d+[^"]*)"', htm)
    return html.unescape(m.group(1)) if m else None

def main():
    ops = json.load(open(f"{ROOT}/data/opskrifter.json", encoding="utf-8"))
    try: details = json.load(open(OUT, encoding="utf-8"))
    except Exception: details = {}
    todo = [o for o in ops if o.get("kind") == "pakke" and o.get("page") and o["page"] not in details]
    print(f"{len(details)} cached, {len(todo)} mangler – henter op til {MAX_NEW}")
    n = ok = 0
    for o in todo[:MAX_NEW]:
        n += 1
        try:
            page = get(target(o["url"]))
            gs = find_garnstudio_link(page)
            if not gs:
                details[o["page"]] = {"error": "no_garnstudio_link"}; continue
            gs = re.sub(r"cid=\d+", "cid=17", gs) if "cid=" in gs else gs + "&cid=17"   # cid=17 = dansk
            d = parse_garnstudio(get(gs))
            if not d:
                details[o["page"]] = {"error": "parse_failed", "src": gs}; continue
            d["src"] = gs; details[o["page"]] = d; ok += 1
            time.sleep(1.2)   # vær flink ved DROPS' server
        except Exception as ex:
            details[o["page"]] = {"error": str(ex)[:120]}
        if n % 20 == 0:
            json.dump(details, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(details, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Hentet {n}, parsede {ok}. I alt {sum(1 for v in details.values() if 'yarns' in v)} opskrifter med mængder.")

if __name__ == "__main__":
    main()
