#!/usr/bin/env python3
"""
Læser Partner-ads produktfeeds, normaliserer dem, matcher garn mod data/garn.json
og skriver:
  data/priser.json        – pris pr. garnkvalitet pr. butik, med alle farvevarianter
  data/drops-pakker.json  – Drops-garnpakker (opskrift + garn) fra Rito
  data/feed-status.json   – hvornår, hvor mange, hvad matchede ikke

Kør:  python3 _build/feeds.py            (bruger feeds/*.xml eller henter fra url/env)
"""
import json, os, re, sys, html, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG  = json.load(open(f"{ROOT}/_build/feeds.json", encoding="utf-8"))
GARN = json.load(open(f"{ROOT}/data/garn.json", encoding="utf-8"))["garn"]
for g in GARN: g["_re"] = re.compile(g["match"], re.I)

# ---------- hjælpere ----------
def clean(s):
    """Feeds er iso-8859-1 med indlejret UTF-8-rod (Â). Ryd op."""
    if not s: return ""
    s = html.unescape(s).replace("\r", " ").replace("\n", " ")
    s = s.replace("Â", "").replace("â€“", "–").replace("â€™", "'")
    return re.sub(r"\s{2,}", " ", s).strip()

def cut(text, n):
    """Klip ved sætningsgrænse i stedet for midt i et ord."""
    text = (text or "").strip()
    if len(text) <= n:
        # Partner-ads klipper beskrivelser ved 255 tegn – fjern en afklippet sidste sætning
        if text and text[-1] not in ".!?" and len(text) >= 200:
            i = max(text.rfind(". "), text.rfind("! "), text.rfind("? "))
            return text[:i+1] if i > len(text)*0.4 else text.rsplit(" ",1)[0] + " …"
        return text
    head = text[:n]
    i = max(head.rfind(". "), head.rfind("! "), head.rfind("? "))
    return (head[:i+1] if i > n*0.5 else head.rsplit(" ",1)[0] + " …").strip()

def num(s):
    try: return round(float((s or "").replace(",", ".")), 2)
    except: return None

def stock(s):
    s = (s or "").lower().replace("_", " ").strip()
    if s.startswith("in") or s in ("på lager", "ja", "true", "1"): return "in_stock"
    if "backorder" in s or "restordre" in s: return "backorder"
    return "out_of_stock"

def target_url(vareurl):
    """Partner-ads-link → den URL kunden lander på (htmlurl=)."""
    q = urllib.parse.urlparse(vareurl).query
    return urllib.parse.parse_qs(q).get("htmlurl", [""])[0]

def with_target(vareurl, new_target):
    """Byt htmlurl= i et Partner-ads-link, behold tracking."""
    u = urllib.parse.urlparse(vareurl)
    q = urllib.parse.parse_qs(u.query)
    q["htmlurl"] = [new_target]
    return u._replace(query=urllib.parse.urlencode(q, doseq=True)).geturl()

COLOR_RE = re.compile(r"(?:unicolor|mix|uni|colour|color)?\s*(\d{2,4})\s+([A-Za-zÆØÅæøåéü'/ -]+?)\s*$", re.I)
def parse_color_field(c):
    """'01 Hvid Unicolour' / 'Off White - 01' / 'Poivre' → (nr, navn)"""
    c = (c or "").strip()
    if not c: return "", ""
    m = re.match(r"^(\d{1,4})\s+(.+?)(?:\s+(?:unicolou?r|mix|uni))?$", c, re.I)
    if m: return m.group(1), m.group(2).strip()
    m = re.match(r"^(.+?)\s*[-–]\s*(\d{1,4})$", c)
    if m: return m.group(2), m.group(1).strip()
    return "", c

def split_color(name, feed_color=None):
    """Finder farvenummer + navn. Feed-felt 'color' vinder, ellers produktnavnet."""
    nr, col = parse_color_field(feed_color)
    if nr: return nr, col
    m = re.search(r"-\s*([^-()]+?)\s*\((\d{2,4})\)\s*$", name)          # 'Önling No 1 - merino og angora garn - Salviegrøn (060)'
    if m: return m.group(2), m.group(1).strip()
    m = COLOR_RE.search(name)
    if m: return m.group(1), m.group(2).strip()
    m = re.search(r"-\s*([^-]+?)\s*-\s*(\d{1,4})\s*$", name)          # 'Ulysse - Poivre - 01' / 'Drops Air - Off White - 01'
    if m: return m.group(2), m.group(1).strip()
    return "", col

def cart_url(shop, product_id, vareurl, qty=1):
    p = shop.get("platform")
    if p == "shopify" and product_id.isdigit() and len(product_id) >= 12:
        return with_target(vareurl, f"{shop['cart_base']}/cart/{product_id}:{qty}")
    if p == "woocommerce" and product_id.isdigit():
        return with_target(vareurl, f"{shop['cart_base']}?add-to-cart={product_id}&quantity={qty}")
    return None

# ---------- indlæsning ----------
def load_feed(shop):
    url = shop.get("url") or os.environ.get(f"FEED_{shop['key'].upper()}", "")
    path = f"{ROOT}/{shop.get('file','')}"
    if url:
        raw = urllib.request.urlopen(url, timeout=120).read()
    elif shop.get("file") and os.path.exists(path):
        raw = open(path, "rb").read()
    else:
        raise FileNotFoundError(f"intet feed: sæt secret FEED_{shop['key'].upper()} eller læg {shop.get('file')}")
    text = raw.decode("iso-8859-1")
    text = re.sub(r'encoding="[^"]+"', 'encoding="utf-8"', text, count=1)
    root = ET.fromstring(text.encode("utf-8"))
    for p in root.iter("produkt"):
        yield {c.tag: clean(c.text) for c in p}

def is_garn(item):
    k = ((item.get("kategorinavn") or "") + " " + (item.get("produktnavn") or "")).lower()
    if any(w in k for w in ("strikkekit", "garnpakke", "opskrift", "gavekort", "strikkebox")): return False
    if not item.get("kategorinavn") and any(g["_re"].search(item.get("produktnavn","")) for g in GARN): return True
    if any(w in k for w in ("opskrift", "bog", "pinde", "hæklenål", "tilbehør", "broderi", "pensel", "knap", "garnkit", "maskemark")): return False
    return "garn" in k

# ---------- kørsel ----------
priser   = {g["slug"]: {"name": g["name"], "brand": g["brand"], "grams": g["grams"], "meters": g["meters"],
                         "gauge": g["gauge"], "needle": g["needle"], "fiber": g["fiber"], "shops": {}} for g in GARN}
pakker   = []
opskrifter = []
onling_ops = {}
seen_pakke = set()
TYPES = [("sweater",r"sweater|trøje|bluse|genser|pullover|tee\b|top\b"),("cardigan",r"cardigan|jakke|bolero"),("vest",r"vest|slipover"),
         ("hue",r"hue|pandebånd|balaclava"),("sjal",r"sjal|tørklæde|halsrør|poncho"),("sokker",r"strømpe|sok"),("vanter",r"vante|luffe|handske"),
         ("baby",r"baby|dåb|body|dragt"),("børn",r"junior|børn|barn"),("kjole",r"kjole|nederdel"),("hjem",r"pude|tæppe|plaid|dukke")]
def find_needles(text):
    return sorted({m.group(1).replace(",", ".").rstrip(".0") if m.group(1) not in ("10",) else "10" for m in re.finditer(r"(?:rund)?pind(?:e)?\s*(?:nr\.?\s*)?(\d{1,2}(?:[.,]5)?)\s*(?:mm)?\b", text, re.I)}, key=float)

def guess_target(text):
    t=text.lower()
    if re.search(r"\bbaby\b|0-3 mdr|1-3 mdr|præmatur|dåb", t): return "baby"
    if re.search(r"børn|barn\b|junior|\b(2|4|6|8|10|12|14) år", t): return "børn"
    if re.search(r"\bherre|\bmand\b|\bmænd|\bmen'?s\b|\bhr\b", t): return "herre"
    return "dame"
def guess_level(text):
    t=text.lower()
    if re.search(r"\bnem\b|nemt|enkel|begynder|let at strikke|simpel", t): return "begynder"
    if re.search(r"fair isle|flerfarvet|snoning|hulmønster|lace|vendepinde|kortrækker|intarsia", t): return "øvet"
    return "let øvet"
def guess_type(text):
    t=text.lower()
    for k,rx in TYPES:
        if re.search(rx,t): return k
    return "andet"
status   = {"generated": datetime.now(timezone.utc).isoformat(timespec="minutes"), "shops": {}}
unmatched = defaultdict(lambda: defaultdict(int))

for shop in CFG["shops"]:
    n = matched = 0
    try:
        items = list(load_feed(shop))
    except Exception as e:
        status["shops"][shop["key"]] = {"error": str(e)}; print("FEJL", shop["key"], e); continue

    for it in items:
        name = it.get("produktnavn", "")
        # Drops-garnpakker (Rito): opskrift + garn i én pakke
        if ("drops" in it.get("brand", "").lower() and "strikkeopskrift" in it.get("kategorinavn", "").lower()) or \
           (it.get("kategorinavn","").lower().startswith("drops") and "opskrift" in it.get("kategorinavn","").lower()):
            if it.get("produktid") in seen_pakke: continue
            seen_pakke.add(it.get("produktid"))
            m = re.match(r"(.+?) by DROPS Design\s*-\s*(.+?)\s+Strikkeopskrift\s*(?:str\.?\s*(.+))?$", name, re.I)
            pakker.append({"shop": shop["key"], "shop_name": shop["name"], "kind": "pakke", "designer": "DROPS Design",
                           "name": m.group(1) if m else name, "type": guess_type(m.group(2) if m else name), "type_label": m.group(2) if m else "",
                           "target": guess_target(name+" "+it.get("kategorinavn","")+" "+it.get("beskrivelse","")[:300]), "level": guess_level(it.get("beskrivelse","")), "free": True, "needles": find_needles(it.get("beskrivelse","")),
                           "sizes": (m.group(3) or "").strip() if m else "", "price": num(it.get("nypris")),
                           "stock": stock(it.get("lagerantal")), "image": it.get("billedurl"),
                           "url": it.get("vareurl"), "desc": cut(it.get("beskrivelse"), 700)})
            continue
        # Önling: "X af Y, strikkeopskrift (DK, SE, NO)" + "X, strikkekit i No 1" pr. størrelse
        nl = name.lower()
        if shop["key"] == "onling" and ("strikkeopskrift" in nl or "strikkekit" in nl or "garnpakke" in nl):
            base = re.sub(r",?\s*(strikkeopskrift|strikkekit|garnpakke).*$", "", name, flags=re.I).strip()
            base = re.sub(r"\s+af\s+.+$", "", base).strip().rstrip(",")
            key = base.lower()
            rec = onling_ops.setdefault(key, {"shop": shop["key"], "shop_name": shop["name"], "kind": "opskrift", "name": base,
                   "designer": it.get("brand") or "Önling", "type": guess_type(name), "target": guess_target(name+" "+it.get("beskrivelse","")),
                   "level": guess_level(it.get("beskrivelse","")), "free": False, "needles": [], "image": it.get("billedurl"), "url": it.get("vareurl"),
                   "price": None, "kits": [], "desc": cut(it.get("beskrivelse"), 700), "stock": stock(it.get("lagerantal"))})
            if "strikkeopskrift" in nl and "kit" not in nl:
                rec["price"] = num(it.get("nypris")); rec["url"] = it.get("vareurl"); rec["opskrift_id"] = it.get("produktid")
                if it.get("billedurl"): rec["image"] = it.get("billedurl")
            else:
                ym = re.search(r"(?:kit|garnpakke)\s+i\s+(.+?)(?:\s*\(|$)", name, re.I)
                rec["kits"].append({"yarn": ym.group(1).strip() if ym else "", "size": it.get("size") or "", "price": num(it.get("nypris")),
                                    "url": it.get("vareurl"), "cart": cart_url(shop, it.get("produktid",""), it.get("vareurl")), "stock": stock(it.get("lagerantal"))})
            continue
        # Løsopskrifter (fx PetiteKnit hos Broen Garn)
        if "strikkeopskrift" in it.get("kategorinavn","").lower() and not is_garn(it):
            opskrifter.append({"shop": shop["key"], "shop_name": shop["name"], "kind": "opskrift",
                               "name": re.sub(r"\s*-\s*(dansk|engelsk|english)\s*$","",name,flags=re.I),
                               "designer": it.get("brand") or "", "type": guess_type(name), "target": guess_target(name+" "+it.get("beskrivelse","")), "level": guess_level(it.get("beskrivelse","")), "free": False, "needles": find_needles(it.get("beskrivelse","")),
                               "price": num(it.get("nypris")), "stock": stock(it.get("lagerantal")),
                               "image": it.get("billedurl"), "url": it.get("vareurl")})
            continue
        if not is_garn(it): continue
        n += 1
        g = next((g for g in GARN if g["_re"].search(name)), None)
        if not g:
            key = re.sub(r"\s+\d.*$", "", name)[:40]
            unmatched[shop["key"]][key] += 1
            continue
        matched += 1
        nr, color = split_color(name, it.get("color"))
        price = num(it.get("nypris")); old = num(it.get("glpris"))
        if price is None or price > g["grams"] * 4:   # frasortér pakker/kg-priser (fx 229,50 for 10 nøgler)
            continue
        entry = priser[g["slug"]]["shops"].setdefault(shop["key"], {
            "shop": shop["name"], "logo": shop.get("logo",""), "platform": shop.get("platform"), "shipping": num(it.get("fragtomk")),
            "free_shipping_from": shop.get("free_shipping_from"), "delivery": it.get("leveringstid"),
            "price": None, "old_price": None, "url": it.get("vareurl"), "image": it.get("billedurl"), "variants": []})
        entry["variants"].append({"nr": nr, "color": color, "price": price, "old_price": old if old and old > price else None,
                                  "stock": stock(it.get("lagerantal")), "ean": re.sub(r"\D","",it.get("ean") or "") or None,
                                  "url": it.get("vareurl"), "cart": cart_url(shop, it.get("produktid", ""), it.get("vareurl")),
                                  "image": it.get("billedurl")})
    status["shops"][shop["key"]] = {"garn_items": n, "matched": matched}
    print(f"{shop['name']:<16} garn: {n:>6}  matchede: {matched:>5}")

# pris pr. butik = laveste pris blandt varianter på lager; sortér butikker billigst først
for slug, g in priser.items():
    for k, s in g["shops"].items():
        instock = [v for v in s["variants"] if v["stock"] == "in_stock"] or s["variants"]
        s["price"] = min(v["price"] for v in instock) if instock else None
        s["old_price"] = max((v["old_price"] or 0) for v in instock) or None
        s["colors_in_stock"] = sum(1 for v in s["variants"] if v["stock"] == "in_stock")
        s["variants"].sort(key=lambda v: (v["nr"] or "zzz", v["color"]))
    g["shops"] = dict(sorted(g["shops"].items(), key=lambda kv: kv[1]["price"] or 1e9))
    g["from_price"] = min((s["price"] for s in g["shops"].values() if s["price"]), default=None)

loaded = [k for k, v in status["shops"].items() if "error" not in v]
if not loaded:
    print("\nIngen feeds kunne læses – beholder eksisterende data/*.json og fortsætter deploy.")
    sys.exit(0)
status["unmatched_top"] = {k: dict(sorted(v.items(), key=lambda x: -x[1])[:25]) for k, v in unmatched.items()}
os.makedirs(f"{ROOT}/data", exist_ok=True)
# Prishistorik: én linje pr. dag pr. garn pr. butik (laveste pris) – bruges til "laveste 30 dage" og graf
hist_path = f"{ROOT}/data/prishistorik.json"
try: hist = json.load(open(hist_path, encoding="utf-8"))
except Exception: hist = {}
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
for slug, g in priser.items():
    for k, s in g["shops"].items():
        if s.get("price"): hist.setdefault(slug, {}).setdefault(k, {})[today] = s["price"]
cutoff = (datetime.now(timezone.utc).replace(hour=0) - __import__("datetime").timedelta(days=120)).strftime("%Y-%m-%d")
for slug in hist:
    for k in hist[slug]: hist[slug][k] = {d: v for d, v in hist[slug][k].items() if d >= cutoff}
json.dump(hist, open(hist_path, "w", encoding="utf-8"), ensure_ascii=False)
json.dump(priser, open(f"{ROOT}/data/priser.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(pakker, open(f"{ROOT}/data/drops-pakker.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for rec in onling_ops.values():
    if rec["price"] is None and rec["kits"]: rec["price"] = min(k["price"] for k in rec["kits"] if k["price"]); rec["kind"] = "kit"
    if rec["price"] is not None: opskrifter.append(rec)
alle = [o for o in opskrifter + pakker if o.get("stock") != "out_of_stock"]
for o in alle:  # pinde: fra beskrivelsen + fra garntabellen for de garner, opskriften nævner
    ns = set(o.get("needles") or [])
    for m in re.finditer(r"Drops\s+([A-ZÆØÅ][\w-]*(?:\s+[A-ZÆØÅ][\w-]*){0,2})", o.get("desc","")):
        for g in GARN:
            if g["_re"].search("Drops " + m.group(1)):
                ns.update(re.findall(r"\d+(?:\.\d)?", g["needle"].replace(",", ".")))
    o["needles"] = sorted(ns, key=float)
json.dump(alle, open(f"{ROOT}/data/opskrifter.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(status, open(f"{ROOT}/data/feed-status.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\nSkrev {sum(1 for g in priser.values() if g['shops'])} garner med priser, {len(pakker)} Drops-pakker, {len(opskrifter)} løsopskrifter.")
