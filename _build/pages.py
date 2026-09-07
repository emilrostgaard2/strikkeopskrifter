#!/usr/bin/env python3
"""Genererer alle statiske sider ud fra data/*.json og _build/content.py.
   Kør efter feeds.py:  python3 _build/pages.py
"""
import json, os, re, html, unicodedata, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{ROOT}/_build")
import content as C

OPS  = json.load(open(f"{ROOT}/data/opskrifter.json", encoding="utf-8"))
PRIS = json.load(open(f"{ROOT}/data/priser.json", encoding="utf-8"))
GARN = {g["slug"]: g for g in json.load(open(f"{ROOT}/data/garn.json", encoding="utf-8"))["garn"]}
for g in GARN.values(): g["_re"] = re.compile(g["match"], re.I)
BASE = "https://strikkeopskrifter.dk"
import datetime
try:
    _st = json.load(open(f"{ROOT}/data/feed-status.json", encoding="utf-8")); _gen = datetime.datetime.fromisoformat(_st["generated"])
except Exception:
    _gen = datetime.datetime.now(datetime.timezone.utc)
_gen_dk = _gen + datetime.timedelta(hours=2)
UPDATED = _gen_dk.strftime("%-d. %B %Y kl. %H:%M").replace("January","januar").replace("February","februar").replace("March","marts").replace("April","april").replace("May","maj").replace("June","juni").replace("July","juli").replace("August","august").replace("September","september").replace("October","oktober").replace("November","november").replace("December","december")
TODAY = _gen_dk.strftime("%Y-%m-%d")
DETAILS = {}
try: DETAILS = json.load(open(f"{ROOT}/data/drops-details.json", encoding="utf-8"))
except Exception: pass
HIST = {}
try: HIST = json.load(open(f"{ROOT}/data/prishistorik.json", encoding="utf-8"))
except Exception: pass

def slugify(s):
    s = s.lower().replace("ø","o").replace("æ","ae").replace("å","aa")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")
def e(s): return html.escape(str(s or ""), quote=True)
def kr(n): return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
import hashlib
def img(url):
    """Lokal WebP hvis images.py har hentet den, ellers feed-URL."""
    if not url: return ""
    k = hashlib.md5(url.encode()).hexdigest()[:16]
    return f"/assets/img/cache/{k}.webp" if os.path.exists(f"{ROOT}/assets/img/cache/{k}.webp") else url
def jsonld(obj): return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'

TYPE_LABEL = {"sweater":"Sweatre & bluser","cardigan":"Cardigans","vest":"Veste","hue":"Huer","sjal":"Sjaler & tørklæder","sokker":"Sokker",
              "vanter":"Vanter","baby":"Baby","børn":"Børn","kjole":"Kjoler","hjem":"Hjem","andet":"Andet"}
TARGET_LABEL = {"dame":"damer","herre":"herrer","børn":"børn","baby":"baby"}

HEAD = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Lora:wght@500;600;700&family=Fraunces:opsz,wght,SOFT@9..144,600;9..144,700,100&family=Instrument+Sans:wght@400;500;600&family=Caveat:wght@500;600&display=swap" rel="stylesheet">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/style.css">'''
def nav(current=""):
    def a(href, label, key, extra=""): return f'<a href="{href}"{" aria-current=page" if key==current else ""}{extra}>{label}</a>'
    return f'''<header class="site"><div class="wrap nav"><a class="logo" href="/">strikke<span>opskrifter</span>.dk</a>
<button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="mainnav"><span></span><span></span><span></span></button>
<nav id="mainnav"><ul>
<li class="has-sub">{a("/opskrifter/","Opskrifter","opskrifter",' aria-haspopup="true"')}<button class="sub-toggle" aria-label="Vis undermenu">▾</button>
<div class="sub"><div class="sub-col"><b>Til hvem</b><a href="/opskrifter/dame/">Damer</a><a href="/opskrifter/boern/">Børn</a><a href="/opskrifter/baby/">Baby</a><a href="/opskrifter/herre/">Herrer</a><a href="/opskrifter/begynder/">Begyndere</a></div>
<div class="sub-col"><b>Type</b><a href="/opskrifter/sweater/">Sweatre & bluser</a><a href="/opskrifter/cardigan/">Cardigans</a><a href="/opskrifter/vest/">Veste</a><a href="/opskrifter/hue/">Huer</a><a href="/opskrifter/sjal/">Sjaler & tørklæder</a><a href="/opskrifter/sokker/">Sokker</a></div>
<div class="sub-col"><b>Pind</b><a href="/opskrifter/pind-3/">Pind 3</a><a href="/opskrifter/pind-4/">Pind 4</a><a href="/opskrifter/pind-5/">Pind 5</a><a href="/opskrifter/pind-7/">Pind 7</a><a href="/opskrifter/pind-8/">Pind 8</a></div></div></li>
<li>{a("/gratis/","Gratis","gratis")}</li><li>{a("/garn/","Garn","garn")}</li><li>{a("/garn/drops/","DROPS","drops")}</li><li>{a("/guides/","Guides","guides")}</li>
</ul></nav></div></header>'''
FOOT = '''<footer class="site"><div class="wrap foot-grid">
<div class="foot-brand"><a class="logo" href="/">strikke<span>opskrifter</span>.dk</a><p>Find opskriften, regn garnet ud, og køb det hvor det er billigst. Priser hentes hver nat fra danske garnbutikker.</p>
<form class="foot-news" action="#" onsubmit="return false"><input type="email" placeholder="din@mail.dk" aria-label="E-mail"><button class="btn btn-primary btn-sm" type="submit">Få prisfald</button></form></div>
<div><b>Opskrifter</b><a href="/opskrifter/dame/">Til damer</a><a href="/opskrifter/boern/">Til børn</a><a href="/opskrifter/baby/">Til baby</a><a href="/opskrifter/herre/">Til herrer</a><a href="/opskrifter/begynder/">Begyndere</a><a href="/gratis/">Gratis opskrifter</a><a href="/garn/drops/">DROPS-opskrifter</a></div>
<div><b>Typer</b><a href="/opskrifter/sweater/">Sweatre & bluser</a><a href="/opskrifter/cardigan/">Cardigans</a><a href="/opskrifter/vest/">Veste</a><a href="/opskrifter/hue/">Huer</a><a href="/opskrifter/sjal/">Sjaler</a><a href="/opskrifter/sokker/">Sokker</a></div>
<div><b>Garn & guides</b><a href="/garn/">Sammenlign garnpriser</a><a href="/garn/drops-baby-merino/">Drops Baby Merino</a><a href="/garn/drops-air/">Drops Air</a><a href="/guides/vaelg-alternativt-garn/">Vælg alternativt garn</a><a href="/guides/hvor-mange-noegler/">Hvor mange nøgler?</a><a href="/guides/alternativer-onling-no-1/">Alternativer til Önling No 1</a></div>
<div><b>Pinde</b><a href="/opskrifter/pind-3/">Pind 3</a><a href="/opskrifter/pind-4/">Pind 4</a><a href="/opskrifter/pind-5/">Pind 5</a><a href="/opskrifter/pind-7/">Pind 7</a><a href="/opskrifter/pind-8/">Pind 8</a></div>
<div><b>Om</b><a href="/om/">Om siden</a><a href="/om/#provision">Sådan tjener vi penge</a><a href="/om/#kontakt">Kontakt</a></div>
</div><div class="wrap foot-bottom">© strikkeopskrifter.dk · Opskrifterne tilhører designerne og butikkerne. Vi linker til dem og får provision ved køb – det ændrer ikke din pris.</div></footer>'''
def breadcrumbs(items):
    html_ = " / ".join(f'<a href="{u}">{e(l)}</a>' if u else e(l) for l, u in items)
    ld = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
          {"@type":"ListItem","position":i+1,"name":l, **({"item":BASE+u} if u else {})} for i,(l,u) in enumerate(items)]}
    return f'<div class="crumbs">{html_}</div>', ld

def faq_block(faq, h="Ofte stillede spørgsmål"):
    if not faq: return "", None
    items = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)
    ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
    return f'<section class="sec faq"><h2>{e(h)}</h2>{items}</section>', ld

EXPLORE = {
 "opskrifter": [
  "Leder du efter noget bestemt? Vi har samlet <a href='/opskrifter/dame/'>strikkeopskrifter til damer</a>, <a href='/opskrifter/boern/'>til børn</a>, <a href='/opskrifter/baby/'>til baby</a> og <a href='/opskrifter/herre/'>til herrer</a> – og er du ny i strik, så start med <a href='/opskrifter/begynder/'>de nemme opskrifter til begyndere</a>. Alle <a href='/gratis/'>gratis strikkeopskrifter</a> ligger på én side, og <a href='/garn/drops/'>DROPS' opskrifter</a> har deres egen, fordi de er så mange.",
  "Efter type: <a href='/opskrifter/sweater/'>sweatre og bluser</a>, <a href='/opskrifter/cardigan/'>cardigans</a>, <a href='/opskrifter/vest/'>veste og slipovers</a>, <a href='/opskrifter/hue/'>huer</a>, <a href='/opskrifter/sjal/'>sjaler og tørklæder</a> og <a href='/opskrifter/sokker/'>sokker</a>. Strikker du helst på en bestemt pind, så se opskrifter til <a href='/opskrifter/pind-3/'>pind 3</a>, <a href='/opskrifter/pind-4/'>pind 4</a>, <a href='/opskrifter/pind-5/'>pind 5</a>, <a href='/opskrifter/pind-7/'>pind 7</a> eller <a href='/opskrifter/pind-8/'>pind 8</a>.",
  "Garnet betyder mere for prisen end opskriften. På <a href='/garn/'>garnsiderne</a> sammenligner vi prisen pr. nøgle hos danske butikker – fx <a href='/garn/drops-baby-merino/'>Drops Baby Merino</a>, <a href='/garn/drops-air/'>Drops Air</a> og <a href='/garn/onling-no-1/'>Önling No 1</a> – og i guiderne kan du læse, <a href='/guides/hvor-mange-noegler/'>hvor mange nøgler du skal bruge</a>, og <a href='/guides/vaelg-alternativt-garn/'>hvordan du vælger et billigere garn</a>.",
 ],
 "garn": [
  "Skal garnet bruges til noget bestemt? Find opskrifter til <a href='/opskrifter/dame/'>damer</a>, <a href='/opskrifter/boern/'>børn</a>, <a href='/opskrifter/baby/'>baby</a> og <a href='/opskrifter/herre/'>herrer</a>, eller gå efter type: <a href='/opskrifter/sweater/'>sweatre</a>, <a href='/opskrifter/cardigan/'>cardigans</a>, <a href='/opskrifter/hue/'>huer</a>, <a href='/opskrifter/sjal/'>sjaler</a> og <a href='/opskrifter/sokker/'>sokker</a>.",
  "Over 900 af opskrifterne er <a href='/gratis/'>gratis</a> – de fleste fra <a href='/garn/drops/'>DROPS Design</a>, hvor du kun betaler for garnet. Er du usikker på mængden, så læs <a href='/guides/hvor-mange-noegler/'>hvor mange nøgler du skal bruge</a>; skal du erstatte et garn, så se <a href='/guides/vaelg-alternativt-garn/'>guiden til alternativt garn</a> eller <a href='/guides/alternativer-onling-no-1/'>alternativerne til Önling No 1</a>.",
 ],
 "drops": [
  "DROPS' opskrifter er gratis, og garnet fås hos flere danske butikker – derfor kan du sammenligne. Se <a href='/garn/drops-baby-merino/'>Baby Merino</a>, <a href='/garn/drops-merino-extra-fine/'>Merino Extra Fine</a>, <a href='/garn/drops-air/'>Air</a>, <a href='/garn/drops-alpaca/'>Alpaca</a> og <a href='/garn/drops-kid-silk/'>Kid-Silk</a> med dagens priser, eller alle <a href='/garn/'>garner</a> samlet.",
  "Flere gratis opskrifter: <a href='/gratis/'>alle gratis strikkeopskrifter</a>, <a href='/opskrifter/dame/'>til damer</a>, <a href='/opskrifter/boern/'>til børn</a>, <a href='/opskrifter/baby/'>til baby</a> og <a href='/opskrifter/herre/'>til herrer</a>. Nye strikkere finder de nemme på <a href='/opskrifter/begynder/'>begyndersiden</a>, og på <a href='/opskrifter/pind-4/'>pind 4</a> og <a href='/opskrifter/pind-5/'>pind 5</a> ligger de hurtigste projekter.",
 ],
 "gratis": [
  "Gratis strikkeopskrifter efter hvem de er til: <a href='/opskrifter/dame/'>damer</a>, <a href='/opskrifter/boern/'>børn</a>, <a href='/opskrifter/baby/'>baby</a> og <a href='/opskrifter/herre/'>herrer</a> – vælg 'Kun gratis' i filteret på hver side. Næsten alle kommer fra <a href='/garn/drops/'>DROPS Design</a>, og <a href='/opskrifter/begynder/'>begyndersiden</a> viser dem, der ikke kræver erfaring.",
  "Gratis opskrift, men ikke gratis garn: på <a href='/garn/'>garnsiderne</a> ser du, hvor <a href='/garn/drops-baby-merino/'>Baby Merino</a>, <a href='/garn/drops-belle/'>Belle</a>, <a href='/garn/drops-air/'>Air</a> og de andre er billigst i dag. Og bruger opskriften et garn, du ikke kan få, så læs <a href='/guides/vaelg-alternativt-garn/'>hvordan du vælger et andet</a>.",
 ],
 "guides": [
  "Guiderne hænger sammen med resten af siden: find <a href='/opskrifter/'>opskrifter</a> til <a href='/opskrifter/dame/'>damer</a>, <a href='/opskrifter/boern/'>børn</a>, <a href='/opskrifter/baby/'>baby</a> og <a href='/opskrifter/herre/'>herrer</a>, se <a href='/gratis/'>de gratis</a> eller <a href='/garn/drops/'>DROPS' opskrifter</a>, og sammenlign <a href='/garn/'>garnpriser</a> pr. nøgle hos danske butikker.",
 ],
}
def explore_html(current, exclude=None):
    key = current if current in EXPLORE else "opskrifter"
    paras = "".join(f"<p>{t}</p>" for t in EXPLORE[key])
    return f'<section class="sec explore"><h2>Udforsk mere</h2>{paras}</section>'

def shell(title, meta, path, body, lds, current="", og_image=None):
    ld_html = "".join(jsonld(x) for x in lds if x)
    og = f'<meta property="og:image" content="{e(og_image)}"><link rel="preload" as="image" href="{e(img(og_image))}">' if og_image else ""
    return f'''<!DOCTYPE html>
<html lang="da"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | strikkeopskrifter.dk</title><meta name="description" content="{e(meta)}">
<link rel="canonical" href="{BASE}{path}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(meta)}">{og}
{HEAD}{ld_html}</head><body>{nav(current)}<main class="wrap">{body}{explore_html(current)}<p class="small muted byauthor">Redigeret af <a href="/om/">{e(C.OWNER)}</a> · priser opdateret {UPDATED} · <a href="/om/#kontakt">Fandt du en fejl?</a></p></main>{FOOT}<button class="totop" aria-label="Til toppen" hidden>↑</button><script src="/assets/site.js"></script></body></html>'''

# ---------------- Drops-opskriftssider ----------------
def find_yarns(text):
    out, seen = [], set()
    for m in re.finditer(r"Drops\s+([A-ZÆØÅ][\w-]*(?:\s+[A-ZÆØÅ][\w-]*){0,2})", text):
        name = "Drops " + m.group(1).strip(" .,")
        name = re.sub(r"\s+(garn|og|eller|som|der|i|Design)$", "", name, flags=re.I)
        if name.lower() in seen or len(name) < 8 or name == "Drops Design": continue
        seen.add(name.lower())
        out.append((name, next((s for s, g in GARN.items() if g["_re"].search(name)), None)))
    return out

def shop_rows(slug, qty=1):
    g = PRIS.get(slug); rows = []
    if not g: return ""
    for i, s in enumerate(v for v in g["shops"].values() if v["price"]):
        note = " · ".join(x for x in [f"Fri fragt over {s['free_shipping_from']} kr." if s.get("free_shipping_from") else "", f"{s.get('colors_in_stock',0)} farver på lager"] if x)
        v = next((v for v in s["variants"] if v["stock"]=="in_stock" and v.get("cart")), None)
        if v and qty > 1:
            v = dict(v)
            v["cart"] = re.sub(r"(%3A|:)1(?=(&|$))", lambda m: m.group(1) + str(qty), v["cart"])
            v["cart"] = re.sub(r"quantity(%3D|=)1(?=(%26|&|$))", lambda m: "quantity" + m.group(1) + str(qty), v["cart"])
        logo = f'<img class="slogo" src="{e(s["logo"])}" alt="" width="40" height="40">' if s.get("logo") else '<span class="slogo logo-txt">' + e(s["shop"][:1]) + '</span>'
        rows.append(f'''<div class="shop {'best' if i==0 else ''}">{logo}<div class="name">{e(s['shop'])}<small>{e(note)}</small></div>
<div class="price">{kr(s['price'])} kr.<small>pr. nøgle</small></div><a class="go" href="{e(v['cart'] if v else s['url'])}" rel="sponsored nofollow" target="_blank">{f'Læg {qty} i kurven' if v and qty>1 else ('Læg i kurven' if v else 'Gå til butik')}</a></div>''')
    return "".join(rows)

TYPE_SENT = {
 "sweater":"En sweater eller bluse er det mest strikkede projekt i Danmark – og det, hvor garnprisen betyder mest, fordi du skal bruge flest nøgler.",
 "cardigan":"Cardigans kræver 10–15 % mere garn end en tilsvarende sweater på grund af knapkanterne, så tjek prisen pr. nøgle en ekstra gang.",
 "vest":"En vest er et hurtigt projekt med lavt garnforbrug – ofte 4–6 nøgler – og et godt sted at prøve et lidt dyrere garn.",
 "hue":"En hue bruger typisk ét nøgle. Det gør den til et perfekt restegarns- eller begynderprojekt.",
 "sjal":"Sjaler og tørklæder strikkes ofte i tyndt garn med stor løbelængde, så få nøgler rækker langt.",
 "sokker":"Sokker kræver et slidstærkt garn med nylon – tjek at alternativet også har det, ellers holder hælen ikke.",
 "vanter":"Vanter bruger under 100 g og strikkes færdig på en aften eller to.",
 "baby":"Babystrik skal tåle vask og være blødt mod huden – vælg superwash-merino eller bomuld.",
 "børn":"Børnetøj bliver vasket ofte – vælg et garn, der tåler maskinvask på uldprogram.",
 "kjole":"En strikket kjole bruger mere garn end en sweater – regn med 12–18 nøgler til en voksenstørrelse.",
 "hjem":"Tæpper og puder tilgiver ujævn strikkefasthed og er gode projekter til restegarn.",
 "andet":"",
}

def needles(text):
    found = sorted({m.group(1).replace(",", ".") for m in re.finditer(r"(?:rund)?pind(?:e)?\s*(?:nr\.?\s*)?(\d+(?:[.,]\d)?)\s*(?:mm)?", text, re.I)}, key=float)
    return found

def materials_panel(o, yarns):
    """Rigtige mængder fra DROPS når de findes, ellers estimat ud fra garnpakkens pris."""
    rows = []
    det = DETAILS.get(o.get("page"))
    if det and det.get("yarns"):
        for y in det["yarns"]:
            slug = next((s_ for s_, g in GARN.items() if g["_re"].search(y["name"])), None); g = GARN.get(slug); p = PRIS.get(slug) if slug else None
            gr = y["grams"]; sizes = det.get("sizes") or []
            per = " · ".join(f"{sz}: {gm} g" for sz, gm in zip(sizes, gr)) if sizes and len(sizes)==len(gr) else " – ".join(str(x) for x in gr) + " g"
            ch = next((v for v in p["shops"].values() if v["price"]), None) if p else None
            cost = f"<br><span class='small muted'>{-(-gr[0]//g['grams'])}–{-(-gr[-1]//g['grams'])} nøgler à {g['grams']} g · fra {kr(-(-gr[0]//g['grams'])*ch['price'])} kr. hos {e(ch['shop'])}</span>" if g and ch else ""
            rows.append(f"<tr><th>{e(y['name'])}</th><td>{e(per)}{cost}</td></tr>")
        n = det.get("needles") or []
        rows.append(f"<tr><th>Pinde</th><td>{'Rundpind ' + ' og '.join(x+' mm' for x in n) if n else 'Se opskriften'}</td></tr>")
        if det.get("gauge"): rows.append(f"<tr><th>Strikkefasthed</th><td>{e(det['gauge'])}</td></tr>")
        rows.append(f"<tr><th>Størrelser</th><td>{e(' – '.join(det.get('sizes') or []) or o.get('sizes') or 'Se opskriften')}</td></tr>")
        rows.append("<tr><th>Opskrift</th><td>Gratis PDF fra DROPS Design (dansk) – <a href='#beregner'>brug beregneren</a> til din størrelse</td></tr>")
        return f"<section class='panel' style='margin-bottom:22px'><h3 style='margin-bottom:10px'>Det skal du bruge</h3><table>{''.join(rows)}</table><p class='small muted' style='margin:10px 0 0'>Mængder pr. størrelse er DROPS Designs egne angivelser.</p></section>"
    for name, slug in yarns:
        g = GARN.get(slug); p = PRIS.get(slug)
        if not (g and p and p.get("shops")): 
            rows.append(f"<tr><th>{e(name)}</th><td>mængde pr. størrelse står i opskriften</td></tr>"); continue
        ref = p["shops"].get("rito") or next(iter(p["shops"].values()))
        balls = max(1, round(o["price"] / ref["price"])) if ref.get("price") and len(yarns) == 1 else None
        cheapest = next((v for v in p["shops"].values() if v["price"]), None)
        if balls:
            rows.append(f"<tr><th>{e(name)}</th><td>ca. <b>{balls} nøgler</b> à {g['grams']} g til mindste størrelse ({balls*g['grams']} g / {balls*g['meters']} m)"
                        f"<br><span class='small muted'>{balls} × {kr(cheapest['price'])} kr. = <b>{kr(balls*cheapest['price'])} kr.</b> hos {e(cheapest['shop'])} (billigst)</span></td></tr>")
        else:
            rows.append(f"<tr><th>{e(name)}</th><td>fra {kr(cheapest['price'])} kr. pr. nøgle hos {e(cheapest['shop'])} – mængde pr. størrelse står i opskriften</td></tr>")
    n = needles(o.get("desc",""))
    rows.append(f"<tr><th>Pinde</th><td>{'Rundpind ' + ' og '.join(x+' mm' for x in n) if n else 'Se opskriften'}</td></tr>")
    rows.append(f"<tr><th>Størrelser</th><td>{e(o.get('sizes') or 'Se opskriften')}</td></tr>")
    rows.append("<tr><th>Opskrift</th><td>Gratis PDF fra DROPS Design (dansk)</td></tr>")
    note = "<p class='small muted' style='margin:10px 0 0'>Nøgleantallet er beregnet ud fra garnpakkens pris og gælder mindste størrelse – større størrelser bruger mere. Den præcise mængde pr. størrelse står i opskriften.</p>" if len(yarns)==1 else ""
    return f"<section class='panel' style='margin-bottom:22px'><h3 style='margin-bottom:10px'>Det skal du bruge</h3><table>{''.join(rows)}</table>{note}</section>"

def alternatives_html(yarns):
    """2 garner i samme strikkefasthed (±1 m) med priser – automatisk fra garntabellen."""
    if not yarns or not yarns[0][1] or not GARN.get(yarns[0][1]): return ""
    g0 = GARN[yarns[0][1]]; out = []
    cands = [g for s_, g in GARN.items() if s_ != g0["slug"] and abs(g["gauge"] - g0["gauge"]) <= 1 and PRIS.get(s_, {}).get("from_price")]
    cands.sort(key=lambda g: PRIS[g["slug"]]["from_price"])
    for g in cands[:3]:
        p = PRIS[g["slug"]]; ch = next((v for v in p["shops"].values() if v["price"]), None)
        save = ""
        if PRIS.get(g0["slug"], {}).get("from_price"):
            d = PRIS[g0["slug"]]["from_price"] - p["from_price"]
            save = f'<span class="tag save">spar {kr(d)} kr./nøgle</span>' if d >= 2 else ""
        out.append(f'''<div class="shop"><span class="slogo logo-txt">{e(g["name"][6:7] if g["name"].startswith("Drops ") else g["name"][:1])}</span><div class="name"><a href="/garn/{g["slug"]}/">{e(g["name"])}</a> {save}<small>{e(g["fiber"])} · {g["meters"]} m/{g["grams"]} g · {g["gauge"]} m på 10 cm</small></div>
<div class="price">{kr(p["from_price"])} kr.<small>pr. nøgle hos {e(ch["shop"])}</small></div><a class="go" href="/garn/{g["slug"]}/">Se priser</a></div>''')
    if not out: return ""
    return f'''<section style="margin-top:26px"><h3 style="margin-bottom:4px">Alternativer i samme strikkefasthed</h3><p class="small muted" style="margin:0 0 10px">Garner med {g0["gauge"]}±1 masker på 10 cm – strik en prøve, og regn mængden om i meter. <a href="/guides/vaelg-alternativt-garn/">Sådan gør du</a>.</p>{"".join(out)}</section>'''

def calc_html(o, det):
    """Rigtig beregner (som Rikke Cozy) når DROPS-mængder pr. størrelse findes."""
    if not det or "yarns" not in det: return "", ""
    sizes = det.get("sizes") or []
    n = max(len(y["grams"]) for y in det["yarns"])
    if not sizes or len(sizes) != n: sizes = [f"Str. {i+1}" for i in range(n)]
    yconf = {}; opts = ""
    for i, y in enumerate(det["yarns"]):
        slug = next((s_ for s_, g in GARN.items() if g["_re"].search(y["name"])), None)
        g = GARN.get(slug); p = PRIS.get(slug) if slug else None
        if not g: continue
        key = f"y{i}"
        grams = (y["grams"] + [y["grams"][-1]]*n)[:n]
        yconf[key] = {"name": y["name"], "garn": slug, "perBall": g["grams"], "grams": grams, "shops": []}
        opts += f'''<label class="yarn"><input type="radio" name="yarn" value="{key}" {'checked' if not opts else ''}><div><h3>{e(y["name"])} <span class="tag orig">Originalgarn</span></h3><p>{e(g["fiber"])} · {g["grams"]} g / {g["meters"]} m{' · <a href="/garn/'+slug+'/">se priser</a>' if p and p.get("shops") else ''}</p></div><div class="amt" data-amt="{key}"></div></label>'''
    if not yconf: return "", ""
    default = min(len(sizes)-1, 2)
    buttons = "".join(f'<button aria-pressed="{"true" if i==default else "false"}" data-i="{i}">{e(sz)}</button>' for i, sz in enumerate(sizes))
    gauge = f'<p class="small muted" style="margin:8px 0 0">Strikkefasthed: {e(det["gauge"])}</p>' if det.get("gauge") else ""
    html_ = f'''<section class="calc" id="beregner"><div class="calc-head"><div><h2>Hvor meget garn skal du bruge?</h2><p>Vælg din størrelse. Mængderne er DROPS' egne tal pr. størrelse – vi regner nøgler og pris ud hos hver butik.</p>{gauge}</div>
<div class="sizes" role="group" aria-label="Vælg størrelse">{buttons}</div></div>
<div class="calc-body"><div class="yarn-opts" role="radiogroup" aria-label="Vælg garn">{opts}<div style="padding:14px 34px;font-size:13.5px;color:var(--ink-2)">Skal du bruge flere garner (fx mohair holdt sammen), vælg dem én ad gangen.</div></div>
<div class="compare"><h3 id="cmp-title"></h3><p class="sub">Priser opdateret {UPDATED}. Fragt er ikke medregnet.</p><div id="shops"></div></div></div></section>'''
    js = f'<script>window.OPSKRIFT={json.dumps({"sizes": sizes, "defaultSize": default, "yarns": yconf}, ensure_ascii=False)};</script>'
    return html_, js

def _pick(name, pool, salt=0):
    return pool[(sum(ord(c) for c in name) + salt) % len(pool)]

def gen_desc(o, yarns, det=None, kits=None):
    """Unik beskrivelse ud fra data – ikke feed-tekst. Formuleringer roterer ud fra navnet."""
    n = o["name"]; tl = TYPE_LABEL.get(o["type"], "andet").lower(); tgt = TARGET_LABEL.get(o.get("target","dame"), "damer")
    singular = {"sweatre & bluser":"en sweater", "cardigans":"en cardigan", "veste":"en vest", "huer":"en hue", "sjaler & tørklæder":"et sjal", "sokker":"et par sokker", "vanter":"et par vanter", "baby":"babystrik", "børn":"børnestrik", "kjoler":"en kjole", "hjem":"strik til hjemmet", "andet":"et strikkeprojekt"}.get(tl, "et strikkeprojekt")
    yn = [nm for nm, _ in yarns]; g0 = next((GARN[sl] for _, sl in yarns if sl and GARN.get(sl)), None)
    p0 = next((PRIS[sl] for _, sl in yarns if sl and PRIS.get(sl, {}).get("shops")), None)
    parts = []
    parts.append(_pick(n, [
        f"{n} er {singular} fra {o['designer']} til {tgt}",
        f"{n} af {o['designer']} er {singular} designet til {tgt}",
        f"Fra {o['designer']} kommer {n} – {singular} til {tgt}",
    ]) + (f" i størrelserne {o['sizes']}." if o.get("sizes") else "."))
    if yn:
        fib = f" ({g0['fiber'].lower()})" if g0 else ""
        parts.append(_pick(n, [
            f"Opskriften er strikket i {' og '.join(yn)}{fib}.",
            f"Garnet er {' holdt sammen med '.join(yn) if len(yn)>1 else yn[0]}{fib}.",
            f"Du skal bruge {' og '.join(yn)}{fib}.",
        ], 1))
    if g0:
        parts.append(_pick(n, [
            f"Det giver {g0['gauge']} masker på 10 cm på pind {g0['needle']} – {'et fint, tæt maskebillede' if g0['gauge']>=24 else ('den klassiske mellemtykkelse' if g0['gauge']>=19 else 'et tykt, hurtigt strik')}.",
            f"Strikkefastheden er {g0['gauge']} masker pr. 10 cm (pind {g0['needle']}), så {'regn med lidt flere timer, men få gram' if g0['gauge']>=24 else ('det er hurtigt nok til at holde motivationen' if g0['gauge']>=19 else 'det er færdigt på få dage')}.",
        ], 2))
    if det and det.get("yarns") and det["yarns"][0].get("grams"):
        gr = det["yarns"][0]["grams"]; parts.append(f"DROPS angiver {gr[0]}–{gr[-1]} g til de {len(gr)} størrelser.")
    if p0:
        shops = [v for v in p0["shops"].values() if v["price"]]
        if len(shops) >= 2:
            parts.append(_pick(n, [
                f"Vi sammenligner prisen hos {len(shops)} butikker – billigst er {shops[0]['shop']} med {kr(shops[0]['price'])} kr. pr. nøgle mod {kr(shops[-1]['price'])} kr. hos {shops[-1]['shop']}.",
                f"Garnet fås hos {len(shops)} af de butikker, vi følger, fra {kr(shops[0]['price'])} kr. pr. nøgle ({shops[0]['shop']}) til {kr(shops[-1]['price'])} kr.",
            ], 3))
        elif shops:
            parts.append(f"Garnet koster {kr(shops[0]['price'])} kr. pr. nøgle hos {shops[0]['shop']}.")
    if o.get("free"):
        parts.append(_pick(n, ["Opskriften er gratis – du betaler kun for garnet.", "Selve opskriften henter du gratis som PDF.", "Opskriften koster ikke noget; det gør garnet."], 4))
    elif kits:
        ks = sorted([k for k in kits if k.get("price")], key=lambda k: k["price"])
        if ks: parts.append(f"Opskriften koster {kr(o['price'])} kr., og et strikkekit med alt garnet fra {kr(ks[0]['price'])} kr.")
    lvl = o.get("level")
    if lvl: parts.append(_pick(n, {"begynder":["Teknisk er den enkel og egner sig til nye strikkere.","Ingen svære teknikker – et godt første projekt."],"let øvet":["Niveauet er let øvet: kan du strikke ret, vrang og tage ind, kan du strikke den.","Den kræver lidt erfaring, men ingen specielle teknikker."],"øvet":["Der er teknikker, der kræver lidt øvelse – se opskriftens beskrivelse.","Den er til dig, der har strikket et par projekter før."]}.get(lvl, [""]), 5))
    return " ".join(x for x in parts if x)

def drops_page(o, related):
    det = DETAILS.get(o.get("page"))
    calc, calc_js = calc_html(o, det)
    yarns = find_yarns(o.get("desc",""))
    if det and det.get("yarns"):
        yarns = [(y["name"], next((s_ for s_, g in GARN.items() if g["_re"].search(y["name"])), None)) for y in det["yarns"]] or yarns
    tl = TYPE_LABEL.get(o["type"], "andet").lower()
    tgt = TARGET_LABEL.get(o.get("target","dame"), "damer")
    title = f"{o['name']} – gratis strikkeopskrift fra DROPS ({tl}, {tgt})"
    meta = f"{o['name']} by DROPS Design: gratis strikkeopskrift til {tgt}{(' i str. '+o['sizes']) if o.get('sizes') else ''}. {('Strikket i ' + ', '.join(n for n,_ in yarns) + '. ') if yarns else ''}Sammenlign garnprisen hos danske butikker, eller køb garnpakken samlet."
    path = o["page"]
    yarn_html = ""
    for name, slug in yarns:
        g = GARN.get(slug); p = PRIS.get(slug)
        spec = f"{g['fiber']} · {g['grams']} g / {g['meters']} m · {g['gauge']} m på 10 cm · pind {g['needle']}" if g else ""
        link = f'<a href="/garn/{slug}/">{e(name)}</a>' if slug and p and p.get("shops") else e(name)
        qty = 1
        if g and p and p.get("shops") and len(yarns) == 1:
            ref = p["shops"].get("rito") or next(iter(p["shops"].values()))
            if ref.get("price"): qty = max(1, round(o["price"] / ref["price"]))
        rows = shop_rows(slug, qty) if slug else ""
        yarn_html += f'''<section class="panel" style="margin-bottom:20px"><h3 style="margin-bottom:4px">{link}</h3><p class="muted small" style="margin:0 0 12px">{e(spec)}</p>
{rows if rows else '<p class="muted small">Vi har ikke priser på dette garn endnu – brug garnpakken, eller se <a href="/guides/vaelg-alternativt-garn/">alternativer i samme strikkefasthed</a>.</p>'}</section>'''
    if not yarns:
        yarn_html = '<p class="muted">Garnet fremgår ikke af beskrivelsen – materialelisten står i opskriften. Garnpakken til højre indeholder det hele.</p>'
    yarn_names = ", ".join(n for n, _ in yarns) or "det garn, DROPS anbefaler"
    faq = [
     (f"Er opskriften til {o['name']} gratis?", f"Ja. {o['name']} er designet af DROPS Design, og hele deres katalog er gratis. Du henter PDF'en på dansk via linket øverst og betaler kun for garnet."),
     (f"Hvilket garn skal jeg bruge til {o['name']}?", f"Opskriften er strikket i {yarn_names}. Den præcise mængde pr. størrelse står i opskriftens materialeliste – og garnpakken fra {o['shop_name']} indeholder garnet til den størrelse, du vælger."),
     (f"Kan jeg strikke {o['name']} i et andet garn?", f"Ja, hvis du rammer samme strikkefasthed som opskriften angiver. Regn mængden om i meter frem for gram. Se vores guide til at vælge alternativt garn."),
     (f"Hvad koster det at strikke {o['name']}?", f"Garnpakken med alt garn koster {kr(o['price'])} kr. hos {o['shop_name']}. Køber du nøglerne enkeltvis, kan det være billigere – sammenlign priserne ovenfor."),
    ]
    lead = gen_desc(o, yarns, det)
    # Prisboks: billigste samlede garnpris vs. garnpakke
    cheapest_total = o["price"]; save = 0
    if len(yarns) == 1 and yarns[0][1] and PRIS.get(yarns[0][1], {}).get("shops"):
        p1 = PRIS[yarns[0][1]]; ref = p1["shops"].get("rito") or next(iter(p1["shops"].values()))
        if ref.get("price"):
            b = max(1, round(o["price"] / ref["price"])); ch = next((v for v in p1["shops"].values() if v["price"]), None)
            if ch: cheapest_total = round(b * ch["price"], 2); save = round(o["price"] - cheapest_total, 2)
    pricebox = f'<div class="pricebox"><span class="big">{kr(cheapest_total)} kr.</span><span class="from">garn til mindste str., billigste butik</span>' + (f'<span class="save">spar {kr(save)} kr. vs. pakken</span>' if save >= 5 else '') + '</div>'
    # Farvekort fra billigste butik (mere billedmateriale + CRO)
    colors_html = ""
    if len(yarns) == 1 and yarns[0][1] and PRIS.get(yarns[0][1], {}).get("shops"):
        ch = next((v for v in PRIS[yarns[0][1]]["shops"].values() if v["price"]), None)
        sw = [v for v in ch["variants"] if v.get("image")][:24] if ch else []
        if sw:
            colors_html = f'<p class="small muted" style="margin:14px 0 0">Farver hos {e(ch["shop"])} – klik på en farve for at gå direkte til den:</p><div class="colors">' + "".join(
                f'<a href="{e(v.get("cart") or v["url"])}" rel="sponsored nofollow" target="_blank" title="{e(v["nr"])} {e(v["color"])}{"" if v["stock"]=="in_stock" else " (udsolgt)"}" class="{"" if v["stock"]=="in_stock" else "out"}" style="background-image:url(\'{e(v["image"])}\')"></a>' for v in sw) + "</div>"
    faq_html, faq_ld = faq_block(faq, f"Spørgsmål om {o['name']}")
    crumbs, crumb_ld = breadcrumbs([("Forside","/"),("Opskrifter","/opskrifter/"),("DROPS","/garn/drops/"),(TYPE_LABEL.get(o['type'],'Andet'), f"/opskrifter/?kategori={o['type']}"),(o['name'],None)])
    rel_html = "".join(f'''<a class="card" href="{r['page']}"><div class="img" style="background:center/cover url('{e(img(r['image']))}')"></div><b>{e(r['name'])}</b><span>DROPS Design · gratis · {TARGET_LABEL.get(r.get('target',''),'')}</span><em class="price">Garnpakke {kr(r['price'])} kr.</em></a>''' for r in related)
    product_ld = {"@context":"https://schema.org","@type":"Product","name":f"{o['name']} – garnpakke","image":o["image"],"description":lead,
                  "brand":{"@type":"Brand","name":"DROPS Design"},"offers":{"@type":"Offer","priceCurrency":"DKK","price":o["price"],"availability":"https://schema.org/InStock" if o.get("stock")=="in_stock" else "https://schema.org/BackOrder","seller":{"@type":"Organization","name":o["shop_name"]}}}
    body = f'''{crumbs}
<style>.hero{{display:grid;grid-template-columns:5fr 6fr;gap:48px;padding:24px 0 40px;align-items:start}}.swatch{{aspect-ratio:4/5;background:var(--oat-2) center/cover;border-radius:var(--r);box-shadow:var(--shadow)}}
.byline{{color:var(--ink-2);margin:10px 0 18px}}.lead{{font-size:17px;max-width:56ch;margin:0 0 24px}}.cta-row{{display:flex;gap:12px;flex-wrap:wrap}}.two{{display:grid;grid-template-columns:7fr 4fr;gap:40px;margin-bottom:48px;align-items:start}}@media(max-width:860px){{.hero,.two{{grid-template-columns:1fr}}}}</style>
<section class="hero"><div class="swatch" role="img" aria-label="{e(o['name'])}" style="background-image:url('{e(img(o['image']))}')"></div>
<div><span class="eyebrow">Gratis opskrift · til {tgt}</span><h1>{e(o['name'])}</h1><p class="byline">Design af DROPS Design{(' · Str. '+e(o['sizes'])) if o.get('sizes') else ''} · Niveau: {e(o.get('level','let øvet'))}</p>
{pricebox}
<p class="lead">{e(lead)}</p>
<div class="cta-row"><a class="btn btn-primary" href="#garn">Se garn og pris</a><a class="btn btn-ghost" href="{e(o['url'])}" rel="sponsored nofollow" target="_blank">Hent opskriften gratis</a></div>
<p class="small muted" style="margin-top:12px">Opskriften er gratis hos DROPS. Garnet køber du hvor det er billigst – eller som samlet pakke.</p></div></section>
<div class="sticky-cta"><div><div class="small muted">Garn fra</div><div class="big">{kr(cheapest_total)} kr.</div></div><a class="btn btn-primary btn-sm" href="#garn">Se garn og pris</a></div>
{calc}
<section id="garn" class="two"><div><h2 style="margin-bottom:8px">Garnet til {e(o['name'])}</h2><p class="muted" style="margin:0 0 18px;max-width:60ch">{e(TYPE_SENT.get(o['type'],''))} Priser opdateret {UPDATED}.</p>{materials_panel(o, yarns)}{yarn_html}{colors_html}{alternatives_html(yarns)}
<p class="disclose">Vi får en lille provision, hvis du køber via vores links. Det ændrer ikke prisen for dig, og det påvirker ikke, hvilken butik vi viser som billigst.</p></div>
<aside class="panel"><h3 style="margin-bottom:6px">Alt garnet i én pakke</h3><p class="muted small" style="margin:0 0 14px">{e(o['shop_name'])} sælger garnet til {e(o['name'])} som samlet pakke i din størrelse{(' ('+e(o['sizes'])+')') if o.get('sizes') else ''}. Opskriften henter du gratis.</p>
<div style="font-family:var(--serif);font-size:30px;font-weight:600;margin-bottom:12px">{kr(o['price'])} kr.</div>
<a class="btn btn-primary" style="display:block" href="{e(o['url'])}" rel="sponsored nofollow" target="_blank">Se garnpakken hos {e(o['shop_name'])}</a>
<p class="small muted" style="margin:16px 0 0">Ny i strik? Læs <a href="/guides/hvor-mange-noegler/">hvor mange nøgler du skal bruge</a> og <a href="/guides/vaelg-alternativt-garn/">hvordan du vælger et andet garn</a>.</p></aside></section>
{faq_html}
<section class="sec"><div class="sec-head"><h2>Flere gratis DROPS-opskrifter – {e(tl)} til {e(tgt)}</h2><a href="/opskrifter/?kategori={o['type']}">Se alle →</a></div><div class="grid">{rel_html}</div></section>'''
    return shell(title, meta, path, body + calc_js, [crumb_ld, faq_ld, product_ld], "drops", o["image"])

# ---------------- kvalitetsregel: kun sider der fortjener at findes ----------------
MIN_DESC = 150
def has_priced_yarn(names):
    return any(slug and PRIS.get(slug, {}).get("shops") for _, slug in names)
def qualifies(o, yarns):
    return bool(o.get("image")) and len(o.get("desc","")) >= MIN_DESC and has_priced_yarn(yarns)

# ---------------- betalte opskrifter (Önling, Broen Garn …) ----------------
def kit_yarns(o):
    """'No 1', 'No 3 + silk mohair' → [(navn, slug)]"""
    names = []
    for k in o.get("kits", []):
        for part in re.split(r"\s*\+\s*", k.get("yarn","")):
            part = part.strip()
            if not part: continue
            full = ("Önling " + part) if re.match(r"(?i)no\.?\s*\d", part) else ("Önling No 10" if "mohair" in part.lower() else part)
            if full not in names: names.append(full)
    if not names:
        for m in re.finditer(r"(?:Önling\s+)?No\.?\s*(\d{1,2})\b", o.get("name","") + " " + o.get("desc","")):
            full = "Önling No " + m.group(1)
            if full not in names: names.append(full)
    return [(n, next((s_ for s_, g in GARN.items() if g["_re"].search(n)), None)) for n in names]

def pattern_page(o, related):
    ds = slugify(o.get("designer") or "designer")
    yarns = kit_yarns(o); tgt = TARGET_LABEL.get(o.get("target","dame"), "damer"); tl = TYPE_LABEL.get(o["type"],"Andet")
    kits = sorted([k for k in o.get("kits", []) if k.get("price")], key=lambda k: k["price"])
    kit_min = kits[0]["price"] if kits else None
    is_kit_only = o.get("kind") == "kit"
    title = f"{o['name']} af {o['designer']} – strikkeopskrift, garn og pris"
    meta = f"{o['name']} af {o['designer']}: {'opskrift ' + kr(o['price']) + ' kr.' if not is_kit_only else 'strikkekit'}{(', garnpakke fra ' + kr(kit_min) + ' kr.') if kit_min and not is_kit_only else ''}. Se hvilket garn den er strikket i, hvad garnet koster, og køb opskrift og garn samlet hos {o['shop_name']}."
    path = o["page"]
    lead = gen_desc(o, yarns, None, kits)
    # garn-blokke
    yarn_html = ""
    for name, slug in yarns:
        g = GARN.get(slug); pr = PRIS.get(slug)
        spec = f"{g['fiber']} · {g['grams']} g / {g['meters']} m · {g['gauge']} m på 10 cm · pind {g['needle']}" if g else ""
        link = f'<a href="/garn/{slug}/">{e(name)}</a>' if slug and pr and pr.get("shops") else e(name)
        rows = shop_rows(slug) if slug else ""
        yarn_html += f'''<section class="panel" style="margin-bottom:20px"><h3 style="margin-bottom:4px">{link}</h3><p class="muted small" style="margin:0 0 12px">{e(spec)}</p>{rows or '<p class="muted small">Ingen løse priser endnu.</p>'}</section>'''
    # kits pr. størrelse
    kit_rows = "".join(f'''<div class="shop"><span class="slogo logo-txt">Ö</span><div class="name">Str. {e(k['size'] or '–')}<small>{e(k['yarn'])}{' · udsolgt' if k['stock']!='in_stock' else ''}</small></div><div class="price">{kr(k['price'])} kr.<small>garn{'' if is_kit_only else ' + opskrift'}</small></div><a class="go" href="{e(k.get('cart') or k['url'])}" rel="sponsored nofollow" target="_blank">{'Læg i kurven' if k.get('cart') else 'Se kittet'}</a></div>''' for i, k in enumerate(o.get("kits", [])) if k.get("price"))
    kits_html = f'''<section class="panel" style="margin-bottom:20px"><h3 style="margin-bottom:4px">Strikkekit i din størrelse</h3><p class="muted small" style="margin:0 0 12px">{e(o['shop_name'])} sælger garnet til {e(o['name'])} pakket efter størrelse{'' if is_kit_only else ' – opskriften følger med'}. Vælg din størrelse og læg direkte i kurven.</p>{kit_rows}</section>''' if kits else ""
    pricebox = f'<div class="pricebox">' + (f'<span class="big">{kr(o["price"])} kr.</span><span class="from">opskrift (PDF)</span>' if not is_kit_only else f'<span class="big">fra {kr(o["price"])} kr.</span><span class="from">strikkekit</span>') + (f'<span class="from">· kit med garn fra <b>{kr(kit_min)} kr.</b></span>' if kit_min and not is_kit_only else '') + '</div>'
    faq = [
     (f"Hvad koster opskriften til {o['name']}?", f"Opskriften koster {kr(o['price'])} kr. som PDF hos {o['shop_name']}." if not is_kit_only else f"{o['name']} sælges som strikkekit med garn fra {kr(o['price'])} kr. hos {o['shop_name']}."),
     (f"Hvilket garn skal jeg bruge til {o['name']}?", f"Opskriften er strikket i {', '.join(n for n,_ in yarns) or 'det garn, designeren anbefaler'}. Mængden pr. størrelse står i opskriften – eller køb kittet, hvor garnet er pakket til din størrelse."),
     (f"Kan jeg strikke {o['name']} i et andet garn?", "Ja, hvis du rammer samme strikkefasthed. Se alternativerne herunder og vores guide til at vælge alternativt garn."),
    ]
    if kit_min and not is_kit_only: faq.append((f"Hvad koster det samlet at strikke {o['name']}?", f"Med strikkekit inkl. opskrift: fra {kr(kit_min)} kr. afhængigt af størrelse. Køber du garnet løst, kan det være billigere – sammenlign priserne ovenfor."))
    faq_html, faq_ld = faq_block(faq, f"Spørgsmål om {o['name']}")
    crumbs, crumb_ld = breadcrumbs([("Forside","/"),("Opskrifter","/opskrifter/"),(o["designer"], f"/designere/{ds}/"),(o["name"],None)])
    rel_html = "".join(f'''<a class="card" href="{r['page']}"><div class="img" style="background:center/cover url('{e(img(r['image']))}')"></div><b>{e(r['name'])}</b><span>{e(r['designer'])}</span><em class="price">{'Opskrift ' if r.get('kind')=='opskrift' else 'Kit fra '}{kr(r['price'])} kr.</em></a>''' for r in related)
    product_ld = {"@context":"https://schema.org","@type":"Product","name":o["name"],"image":o["image"],"description":lead,"brand":{"@type":"Brand","name":o["designer"]},
                  "offers":{"@type":"AggregateOffer","priceCurrency":"DKK","lowPrice":o["price"],"highPrice":max([o["price"]]+[k["price"] for k in kits]),"offerCount":1+len(kits),"seller":{"@type":"Organization","name":o["shop_name"]}}}
    body = f'''{crumbs}
<style>.hero{{display:grid;grid-template-columns:5fr 6fr;gap:48px;padding:24px 0 40px;align-items:start}}.swatch{{aspect-ratio:4/5;background:var(--oat-2) center/cover;border-radius:var(--r);box-shadow:var(--shadow)}}
.byline{{color:var(--ink-2);margin:10px 0 18px}}.lead{{font-size:17px;max-width:56ch;margin:0 0 24px}}.cta-row{{display:flex;gap:12px;flex-wrap:wrap}}.two{{display:grid;grid-template-columns:7fr 4fr;gap:40px;margin-bottom:48px;align-items:start}}@media(max-width:860px){{.hero,.two{{grid-template-columns:1fr}}}}</style>
<section class="hero"><div class="swatch" role="img" aria-label="{e(o['name'])}" style="background-image:url('{e(img(o['image']))}')"></div>
<div><span class="eyebrow">Opskrift · {e(o['designer'])}</span><h1>{e(o['name'])}</h1><p class="byline">Design af <a href="/designere/{ds}/">{e(o['designer'])}</a> · Til {tgt} · {e(tl)}{(' · Niveau: '+e(o['level'])) if o.get('level') else ''}</p>
{pricebox}<p class="lead">{e(lead)}</p>
<div class="cta-row"><a class="btn btn-primary" href="#garn">Se garn og pris</a><a class="btn btn-ghost" href="{e(o['url'])}" rel="sponsored nofollow" target="_blank">{'Køb opskriften · ' + kr(o['price']) + ' kr.' if not is_kit_only else 'Se kittet hos ' + e(o['shop_name'])}</a></div>
<p class="small muted" style="margin-top:12px">Opskriften sælges af {e(o['shop_name'])}. Garnet kan købes samme sted – eller løst, hvor det er billigst.</p></div></section>
<div class="sticky-cta"><div><div class="small muted">{'Opskrift' if not is_kit_only else 'Kit fra'}</div><div class="big">{kr(o['price'])} kr.</div></div><a class="btn btn-primary btn-sm" href="#garn">Se garn og pris</a></div>
<section id="garn" class="two"><div><h2 style="margin-bottom:8px">Garnet til {e(o['name'])}</h2><p class="muted" style="margin:0 0 18px;max-width:60ch">{e(TYPE_SENT.get(o['type'],''))} Priser opdateret {UPDATED}.</p>{kits_html}{yarn_html}{alternatives_html(yarns)}
<p class="disclose">Vi får en lille provision, hvis du køber via vores links. Det ændrer ikke prisen for dig.</p></div>
<aside class="panel"><h3 style="margin-bottom:6px">Opskriften</h3><p class="muted small" style="margin:0 0 14px">PDF på dansk{', svensk og norsk' if 'SE' in (o.get('name','') + ' ' + o.get('desc','')) else ''} fra {e(o['shop_name'])}. Sendes på mail efter køb.</p>
<div style="font-family:var(--serif);font-size:30px;font-weight:600;margin-bottom:12px">{kr(o['price'])} kr.</div>
<a class="btn btn-primary" style="display:block" href="{e(o['url'])}" rel="sponsored nofollow" target="_blank">{'Køb opskriften' if not is_kit_only else 'Se kittet'} hos {e(o['shop_name'])}</a>
<p class="small muted" style="margin:16px 0 0">Ny i strik? Læs <a href="/guides/hvor-mange-noegler/">hvor mange nøgler du skal bruge</a> og <a href="/guides/vaelg-alternativt-garn/">hvordan du vælger et andet garn</a>.</p></aside></section>
{faq_html}
<section class="sec"><div class="sec-head"><h2>Flere opskrifter fra {e(o['designer'])}</h2><a href="/designere/{ds}/">Se alle →</a></div><div class="grid">{rel_html}</div></section>'''
    return shell(title, meta, path, body, [crumb_ld, faq_ld, product_ld], "opskrifter", o["image"])

def designer_page(name, items):
    ds = slugify(name); path = f"/designere/{ds}/"
    free = sum(1 for o in items if o.get("free")); paid = len(items) - free
    title = f"{name} strikkeopskrifter – alle {len(items)} opskrifter med garn og pris"
    meta = f"Alle strikkeopskrifter fra {name} samlet: {len(items)} opskrifter{(' ('+str(free)+' gratis)') if free else ''} til dame, børn og baby. Se hvilket garn de er strikket i, og hvad garnet koster i dag."
    crumbs, crumb_ld = breadcrumbs([("Forside","/"),("Designere","/designere/"),(name,None)])
    types = {}
    for o in items: types[o["type"]] = types.get(o["type"], 0) + 1
    tlist = ", ".join(f"{TYPE_LABEL.get(t,t).lower()} ({n})" for t, n in sorted(types.items(), key=lambda x: -x[1])[:6])
    prices = sorted(o["price"] for o in items if o.get("price"))
    intro = f"<p>Her er alle {len(items)} opskrifter fra {e(name)}, vi har med: {e(tlist)}. {'Alle er gratis at hente.' if free==len(items) else ('Opskrifterne koster ' + kr(prices[0]) + '–' + kr(prices[-1]) + ' kr.' if prices else '')} Til hver viser vi garnet, opskriften er strikket i, og hvad det koster i dag hos de butikker, vi sammenligner – så du kan se den samlede pris, før du køber.</p>"
    grid = "".join(card(o) for o in items)
    coll_ld = {"@context":"https://schema.org","@type":"CollectionPage","name":title,"url":BASE+path}
    body = f'''{crumbs}<span class="eyebrow" style="margin-top:14px">Designer</span><h1>{e(name)} strikkeopskrifter</h1><div class="prose intro">{intro}</div><div class="grid" style="margin-top:22px">{grid}</div>'''
    return shell(title, meta, path, body, [crumb_ld, coll_ld], "opskrifter")

def designers_index(groups):
    crumbs, crumb_ld = breadcrumbs([("Forside","/"),("Designere",None)])
    cards = "".join(f'<a class="card" href="/designere/{slugify(n)}/"><div class="img" style="background:center/cover url(\'{e(img(items[0]["image"]))}\')"></div><b>{e(n)}</b><span>{len(items)} opskrifter</span></a>' for n, items in groups)
    body = f'{crumbs}<h1 style="margin:12px 0 8px">Designere</h1><p class="muted" style="max-width:60ch">Strikkeopskrifter samlet pr. designer – med garn og pris til hver opskrift.</p><div class="grid" style="margin-top:24px">{cards}</div>'
    return shell("Strikkedesignere – opskrifter fra DROPS, PetiteKnit, Önling, Hanne Falkenberg m.fl.", "Find strikkeopskrifter pr. designer: DROPS Design, PetiteKnit, Katrine Hannibal (Önling), Hanne Falkenberg, Rikke Jönsson og flere – med garnpris.", "/designere/", body, [crumb_ld], "opskrifter")

# ---------------- garnsider (statisk HTML) ----------------
def garn_page(slug, g):
    name = g["name"]; path = f"/garn/{slug}/"
    shops = [v for v in g["shops"].values() if v["price"]]
    ch = shops[0] if shops else None
    rows = shop_rows(slug)
    colors = ""
    if ch:
        sw = [v for v in ch["variants"] if v.get("image")][:36]
        colors = '<div class="colors" style="grid-template-columns:repeat(9,1fr)">' + "".join(f'<a href="{e(v.get("cart") or v["url"])}" rel="sponsored nofollow" target="_blank" title="{e(v["nr"])} {e(v["color"])}{"" if v["stock"]=="in_stock" else " (udsolgt)"}" class="{"" if v["stock"]=="in_stock" else "out"}" style="background-image:url(\'{e(img(v["image"]))}\')"></a>' for v in sw) + '</div>'
    # opskrifter i dette garn
    using = [o for o in OPS if o.get("page") and any(sl == slug for _, sl in (find_yarns(o.get("desc","")) if o.get("kind")=="pakke" else kit_yarns(o)))][:8]
    alt = [(s_, GARN[s_]) for s_ in GARN if s_ != slug and abs(GARN[s_]["gauge"] - g["gauge"]) <= 1 and PRIS.get(s_, {}).get("from_price")]
    alt.sort(key=lambda x: PRIS[x[0]]["from_price"])
    alt_html = "".join(f'<li><a href="/garn/{s_}/">{e(a["name"])}</a> <span class="muted small">– {e(a["fiber"])}, {a["meters"]} m/{a["grams"]} g, fra {kr(PRIS[s_]["from_price"])} kr.</span></li>' for s_, a in alt[:5])
    title = f"{name} – pris hos {len(shops)} butik{'ker' if len(shops)!=1 else ''}, strikkefasthed og opskrifter"
    meta = f"{name}: {e(g['fiber'])}, {g['meters']} m/{g['grams']} g, {g['gauge']} masker på pind {g['needle']}. Sammenlign prisen pr. nøgle{(' – fra ' + kr(g['from_price']) + ' kr.') if g.get('from_price') else ''} hos danske garnbutikker, og se opskrifter garnet passer til."
    lead = _pick(name, [
        f"{name} er {g['fiber'].lower()} med {g['meters']} m på {g['grams']} g. Strikkefastheden er {g['gauge']} masker pr. 10 cm på pind {g['needle']} – {'en tynd kvalitet til fint strik' if g['gauge']>=24 else ('en mellemtykkelse, der passer til de fleste sweatre' if g['gauge']>=19 else 'en tyk kvalitet til hurtigt strik og huer')}.",
        f"Med {g['meters']} m pr. {g['grams']} g og {g['gauge']} masker på pind {g['needle']} er {name} {'et tyndt garn' if g['gauge']>=24 else ('et mellemtykt garn' if g['gauge']>=19 else 'et tykt garn')} i {g['fiber'].lower()}.",
    ])
    if len(shops) >= 2: lead += f" Vi følger prisen hos {len(shops)} butikker: i dag fra {kr(shops[0]['price'])} kr. pr. nøgle hos {shops[0]['shop']} til {kr(shops[-1]['price'])} kr. hos {shops[-1]['shop']} – en forskel på {kr(shops[-1]['price']-shops[0]['price'])} kr. pr. nøgle, eller {kr((shops[-1]['price']-shops[0]['price'])*10)} kr. på en sweater med 10 nøgler."
    elif ch: lead += f" Garnet koster {kr(ch['price'])} kr. pr. nøgle hos {ch['shop']}, som er den eneste af de butikker, vi følger, der fører det."
    faq = [
     (f"Hvor er {name} billigst?", f"I dag hos {ch['shop']} til {kr(ch['price'])} kr. pr. nøgle." if ch else "Vi har ingen priser endnu."),
     (f"Hvor mange nøgler {name} skal jeg bruge til en sweater?", f"Til en voksen M i mellemtykkelse skal du bruge cirka {round(1200/g['meters'])}–{round(1500/g['meters'])} nøgler à {g['grams']} g (1.200–1.500 m). Tjek opskriftens materialeliste – eller brug beregneren på opskriftssiderne."),
     (f"Hvad kan erstatte {name}?", f"Garner med {g['gauge']}±1 masker på 10 cm: " + ", ".join(a["name"] for _, a in alt[:3]) + ". Regn mængden om i meter." if alt else "Find et garn med samme strikkefasthed og regn mængden om i meter."),
     (f"Kan {name} maskinvaskes?", "Tjek banderolen. Superwash-merino og bomuld tåler uldprogram ved 30 grader; alpaka, mohair og ubehandlet uld vaskes i hånden."),
    ]
    faq_html, faq_ld = faq_block(faq, f"Spørgsmål om {name}")
    crumbs, crumb_ld = breadcrumbs([("Forside","/"),("Garn","/garn/"),(name,None)])
    prod_ld = {"@context":"https://schema.org","@type":"Product","name":name,"brand":{"@type":"Brand","name":g["brand"]},"image":img(ch["image"]) if ch and ch.get("image") else None,
               "offers":{"@type":"AggregateOffer","priceCurrency":"DKK","lowPrice":g.get("from_price"),"highPrice":shops[-1]["price"] if shops else None,"offerCount":len(shops)}}
    body = f'''{crumbs}
<style>.top{{display:grid;grid-template-columns:4fr 7fr;gap:48px;padding:24px 0 40px;align-items:start}}.gimg{{aspect-ratio:1;background:var(--oat-2) center/cover;border-radius:var(--r);box-shadow:var(--shadow)}}
.specs{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:18px 0}}.specs div{{padding:12px 14px;background:var(--paper);border-radius:12px;box-shadow:var(--shadow)}}.specs b{{display:block;font-family:var(--serif);font-size:19px;font-weight:600}}.specs small{{color:var(--ink-2);font-size:13px}}
.two{{display:grid;grid-template-columns:7fr 4fr;gap:40px}}@media(max-width:860px){{.top,.two{{grid-template-columns:1fr}}.specs{{grid-template-columns:1fr 1fr}}}}</style>
<section class="top"><div><div class="gimg" role="img" aria-label="{e(name)}" style="background-image:url('{e(img(ch['image'])) if ch and ch.get('image') else ''}')"></div>{colors}</div>
<div><span class="eyebrow">Garn · {e(g['brand'])}</span><h1>{e(name)}</h1><p class="byline">{e(g['fiber'])}</p>
<div class="pricebox"><span class="big">{('fra ' + kr(g['from_price']) + ' kr.') if g.get('from_price') else '–'}</span><span class="from">pr. nøgle · {len(shops)} butik{'ker' if len(shops)!=1 else ''}</span></div>
<div class="specs"><div><b>{g['grams']} g</b><small>{g['meters']} m</small></div><div><b>{g['gauge']} m</b><small>på 10 cm</small></div><div><b>Pind {e(g['needle'])}</b><small>anbefalet</small></div><div><b>{len(using) if using else '–'}</b><small>opskrifter her</small></div></div>
<p class="lead">{e(lead)}</p></div></section>
<section class="two"><div><h2 style="margin-bottom:6px">Pris pr. nøgle hos danske butikker</h2><p class="small muted" style="margin:0 0 10px">Priser opdateret {UPDATED}. Fragt ikke medregnet.</p>{rows or '<p class="muted">Ingen priser endnu.</p>'}
<div class="panel" id="garn-hist" data-garn="{slug}" style="margin:14px 0;padding:16px 20px"><b>Prishistorik</b> <span class="small muted">– vises når vi har fulgt prisen i nogle dage.</span></div>
<p class="disclose">Vi får en lille provision ved køb via vores links. Det ændrer ikke prisen, og det påvirker ikke rækkefølgen.</p>
{('<h2 style="margin:36px 0 10px">Alternativer i samme strikkefasthed</h2><ul class="toplist">' + alt_html + '</ul><p class="small muted">Regn mængden om i meter – se <a href="/guides/vaelg-alternativt-garn/">guiden</a>.</p>') if alt_html else ''}</div>
<aside class="panel"><h3 style="margin-bottom:6px">Følg prisen</h3><p class="muted small" style="margin:0 0 14px">Få en mail, når {e(name)} falder i pris hos en af butikkerne.</p><form class="foot-news" action="#" onsubmit="return false"><input type="email" placeholder="din@mail.dk" aria-label="E-mail"><button class="btn btn-primary btn-sm" type="submit">Prisalarm</button></form>
<p class="small muted" style="margin:16px 0 0"><a href="/guides/hvor-mange-noegler/">Hvor mange nøgler skal jeg bruge?</a><br><a href="/guides/vaelg-alternativt-garn/">Sådan vælger du et alternativt garn</a></p></aside></section>
{('<section class="sec"><div class="sec-head"><h2>Opskrifter i ' + e(name) + '</h2><a href="/opskrifter/?q=' + e(name.split()[-1]) + '">Se alle →</a></div><div class="grid">' + "".join(card(o) for o in using) + '</div></section>') if using else ''}
{faq_html}'''
    return shell(title, meta, path, body, [crumb_ld, faq_ld, prod_ld], "garn", img(ch["image"]) if ch and ch.get("image") else None)

# ---------------- kategorisider / hubs ----------------
def card(o):
    sub = f"{e(o.get('designer',''))}{(' · '+e(o['sizes'])) if o.get('sizes') else ''}{' · gratis opskrift' if o.get('free') else ''}"
    price = f"Garnpakke {kr(o['price'])} kr." if o.get("kind")=="pakke" else (f"Kit fra {kr(o['price'])} kr." if o.get("kind")=="kit" else f"Opskrift {kr(o['price'])} kr.")
    return f'''<a class="card" href="{e(o.get('page') or o['url'])}"{'' if o.get('page') else ' rel="sponsored nofollow" target="_blank"'}><div class="img" role="img" aria-label="{e(o['name'])}" style="background-image:url('{e(img(o['image']))}')">{'<span class="badge">gratis</span>' if o.get('free') else ''}</div><b>{e(o['name'])}</b><span>{sub}</span><em class="price">{price}</em></a>'''

def match_preset(o, preset):
    if preset.get("type") and o.get("type") != preset["type"]: return False
    if preset.get("target") and o.get("target") != preset["target"]: return False
    if preset.get("designer") and o.get("designer") != preset["designer"]: return False
    if preset.get("free") and not o.get("free"): return False
    if preset.get("level") and o.get("level") != preset["level"]: return False
    if preset.get("needle") and preset["needle"] not in (o.get("needles") or []): return False
    return bool(o.get("image"))

def stats_html(items, what):
    """Genereret prisspænd + top-10 – unikt pr. side, baseret på data."""
    prices = sorted(o["price"] for o in items if o.get("kind")=="pakke" and o.get("price"))
    if len(prices) < 5: return ""
    lo, hi = prices[0], prices[-1]; q1, q3 = prices[len(prices)//4], prices[3*len(prices)//4]
    top = items[:10]
    lis = "".join(f'<li><a href="{e(o.get("page") or o["url"])}">{e(o["name"])}</a> <span class="muted small">– {e(o.get("designer",""))}, garn {kr(o["price"])} kr.</span></li>' for o in top)
    return f'''<section class="sec"><h2>Hvad koster garnet til {e(what)}?</h2><p>Blandt de {len(prices)} opskrifter her, hvor en butik sælger garnet som samlet pakke, koster garnet fra <b>{kr(lo)} kr.</b> til <b>{kr(hi)} kr.</b> – de fleste ligger mellem {kr(q1)} og {kr(q3)} kr. Prisen afhænger af garntykkelse, størrelse og om du køber løst eller som pakke; på hver opskriftsside kan du se, hvor garnet er billigst i dag.</p>
<h3 style="margin:22px 0 10px">De 10 nyeste {e(what)}</h3><ol class="toplist">{lis}</ol></section>'''

def grid_html(preset, items=None):
    attrs = " ".join(f'data-{k}="{e(v)}"' for k, v in preset.items())
    return f'''<div class="filters" role="group" aria-label="Filtrér">
    <input type="search" id="f-q" placeholder="Søg opskrift, garn …" aria-label="Søg">
    <select id="f-kat" aria-label="Kategori" {'hidden' if 'type' in preset else ''}><option value="">Alle kategorier</option>{''.join(f'<option value="{k}">{v}</option>' for k,v in TYPE_LABEL.items() if k!='andet')}</select>
    <select id="f-target" aria-label="Til" {'hidden' if 'target' in preset else ''}><option value="">Alle</option><option value="dame">Damer</option><option value="herre">Herrer</option><option value="børn">Børn</option><option value="baby">Baby</option></select>
    <select id="f-des" aria-label="Designer" {'hidden' if 'designer' in preset else ''}><option value="">Alle designere</option></select>
    <select id="f-free" aria-label="Pris" {'hidden' if 'free' in preset else ''}><option value="">Betalt og gratis</option><option value="1">Kun gratis</option></select>
    <select id="f-sort" aria-label="Sortering"><option value="">Nyeste</option><option value="pris">Billigste garn</option><option value="navn">A–Å</option></select>
    <span id="f-count" class="muted small" style="align-self:center"></span></div>
  <div class="grid" id="opskrift-grid" {attrs}>{''.join(card(o) for o in (items or [])[:24])}</div>'''

def cat_page(c, current="opskrifter"):
    path = "/" + c["path"] + "/"
    intro = "".join(f"<p>{e(p)}</p>" for p in c["intro"])
    secs = "".join(f'<section class="sec"><h2>{e(h)}</h2><p>{e(t)}</p></section>' for h, t in c["sections"])
    faq_html, faq_ld = faq_block(c["faq"])
    crumbs, crumb_ld = breadcrumbs([("Forside","/"),("Opskrifter","/opskrifter/"),(c["h1"],None)] if c["path"].startswith("opskrifter") else [("Forside","/"),(c["h1"],None)])
    coll_ld = {"@context":"https://schema.org","@type":"CollectionPage","name":c["title"],"description":c["meta"],"url":BASE+path,"isPartOf":{"@type":"WebSite","name":"strikkeopskrifter.dk","url":BASE}}
    items = [o for o in OPS if match_preset(o, c["preset"])]
    what = c["h1"].replace("Strikkeopskrifter til ", "").replace("Nemme strikkeopskrifter til ", "opskrifter til ").replace("Strikkeopskrifter", "opskrifter").lower()
    upd = f'<p class="small muted" style="margin:-6px 0 10px">{len(items)} opskrifter · priser opdateret {UPDATED}</p>'
    body = f'''{crumbs}<h1 style="margin-top:12px">{e(c['h1'])}</h1><div class="prose intro">{intro}</div>{upd}
{grid_html(c['preset'], items)}
<div class="prose">{secs}</div>{stats_html(items, what)}{faq_html}'''
    return shell(c["title"], c["meta"], path, body, [crumb_ld, coll_ld, faq_ld], current)

def guide_page(g):
    path = f"/guides/{g['slug']}/"
    body_html = "".join(f"<h2>{e(h)}</h2><p>{e(t)}</p>" for h, t in g["body"])
    faq_html, faq_ld = faq_block(g["faq"])
    crumbs, crumb_ld = breadcrumbs([("Forside","/"),("Guides","/guides/"),(g["h1"],None)])
    art_ld = {"@context":"https://schema.org","@type":"Article","headline":g["title"],"description":g["meta"],"author":{"@type":"Person","name":C.OWNER},"publisher":{"@type":"Organization","name":"strikkeopskrifter.dk"},"url":BASE+path}
    img = f"/assets/img/guides/{g['slug']}.jpg" if os.path.exists(f"{ROOT}/assets/img/guides/{g['slug']}.jpg") else None
    hero = f'<div style="aspect-ratio:16/8;background:var(--oat-2) center/cover url({img});border-radius:20px;box-shadow:var(--shadow);margin:20px 0 28px" role="img" aria-label="{e(g["h1"])}"></div>' if img else ""
    body = f'''{crumbs}<article class="prose" style="max-width:76ch"><span class="eyebrow" style="margin-top:14px">Guide</span><h1 style="margin:0 0 8px">{e(g['h1'])}</h1><p class="muted small">Af {e(C.OWNER)} · strikkeopskrifter.dk</p>{hero}{body_html}</article>{faq_html}'''
    art_ld["image"] = BASE + img if img else None
    return shell(g["title"], g["meta"], path, body, [crumb_ld, art_ld, faq_ld], "guides", BASE + img if img else None)

def guides_index():
    cards = "".join(f'<a class="card" href="/guides/{g["slug"]}/"><div class="img wide" style="background-image:url(/assets/img/guides/{g["slug"]}.jpg)"></div><b>{e(g["h1"])}</b><span>{e(g["meta"][:90])}…</span></a>' for g in C.GUIDES)
    crumbs, crumb_ld = breadcrumbs([("Forside","/"),("Guides",None)])
    body = f'{crumbs}<h1 style="margin:12px 0 8px">Guides til garn og strik</h1><p class="muted" style="max-width:60ch">Korte, praktiske guides om det, folk oftest spørger om: garnvalg, mængder og omregning.</p><div class="grid grid-3" style="margin-top:24px">{cards}</div>'
    return shell("Guides: garnvalg, garnforbrug og alternativer", "Praktiske guides om at vælge garn, regne garnforbrug ud og erstatte garnet i en strikkeopskrift.", "/guides/", body, [crumb_ld], "guides")

def om_page():
    crumbs, crumb_ld = breadcrumbs([("Forside","/"),("Om siden",None)])
    org_ld = {"@context":"https://schema.org","@type":"Organization","name":"strikkeopskrifter.dk","url":BASE,"founder":{"@type":"Person","name":C.OWNER}}
    body = f'''{crumbs}<article class="prose" style="max-width:68ch"><h1 style="margin:12px 0 16px">Om strikkeopskrifter.dk</h1>
<p>strikkeopskrifter.dk samler danske og nordiske strikkeopskrifter og viser det, opskrifterne selv ikke gør: hvad garnet koster i dag, hvor det er billigst, og hvor mange nøgler du skal bruge til din størrelse.</p>
<h2>Hvem står bag</h2><p>{e(C.OWNER)}. {e(C.OWNER_BIO)}</p>
<h2>Sådan arbejder vi</h2><p>Garndata (løbelængde, strikkefasthed, mængde pr. størrelse) tastes ind manuelt fra opskrifternes materialelister og kontrolleres mod producentens banderole. Priser, lager og farver hentes automatisk hver nat fra butikkernes produktfeeds. Vi ændrer aldrig i priserne, og vi viser altid den billigste butik først – uanset hvad vi tjener på den.</p>
<h2 id="provision">Sådan tjener vi penge</h2><p>Når du klikker videre til en butik og køber, får vi en lille provision (typisk 5–10 %). Det koster ikke dig noget ekstra, og det påvirker ikke rækkefølgen af butikkerne. Vi har ingen betalte placeringer og ingen annoncer. Hvis vi ikke har en aftale med en butik, kan den mangle i sammenligningen – det skriver vi, når det er tilfældet.</p>
<h2>Opskrifterne</h2><p>Opskrifterne tilhører designerne og butikkerne. Vi kopierer dem ikke; vi linker til dem, og vi bruger kun billeder, som butikkerne stiller til rådighed i deres produktfeeds. Er du designer og vil have din opskrift tilføjet, rettet eller fjernet, så skriv.</p>
<h2 id="kontakt">Kontakt</h2><p>Fejl i en pris, en mængde eller et link? Skriv til <a href="mailto:hej@strikkeopskrifter.dk">hej@strikkeopskrifter.dk</a>. Vi retter typisk inden for et døgn.</p></article>'''
    return shell("Om strikkeopskrifter.dk – hvem vi er, og hvordan vi tjener penge", "Hvem der står bag strikkeopskrifter.dk, hvordan garndata og priser indsamles, og hvordan siden finansieres.", "/om/", body, [crumb_ld, org_ld])

# ---------------- kør ----------------
def write(path, html_):
    d = f"{ROOT}/{path.strip('/')}"; os.makedirs(d, exist_ok=True)
    open(f"{d}/index.html", "w", encoding="utf-8").write(html_)

for o in OPS: o.pop("page", None); o.pop("slug", None)
skipped = {"drops": 0, "paid": 0}
pakker = []
for o in [o for o in OPS if o.get("kind") == "pakke"]:
    det = DETAILS.get("/opskrifter/drops/" + slugify(o["name"]) + "/")
    yn = [(y["name"], next((s_ for s_, g in GARN.items() if g["_re"].search(y["name"])), None)) for y in det["yarns"]] if det and det.get("yarns") else find_yarns(o.get("desc",""))
    if qualifies(o, yn): pakker.append(o)
    else: skipped["drops"] += 1
seen = {}
for o in pakker:
    s = slugify(o["name"]); n = seen.get(s, 0); seen[s] = n + 1
    o["slug"] = s if n == 0 else f"{s}-{n+1}"; o["page"] = f"/opskrifter/drops/{o['slug']}/"
by_key = {}
for o in pakker: by_key.setdefault((o["type"], o.get("target")), []).append(o)
def yarn_key(o): return tuple(sorted(n for n,_ in find_yarns(o.get("desc",""))))
for o in pakker:
    yk = yarn_key(o)
    rel = [r for r in by_key[(o["type"], o.get("target"))] if r is not o and yk and yarn_key(r) == yk][:4]
    rel += [r for r in by_key[(o["type"], o.get("target"))] if r is not o and r not in rel][:4-len(rel)]
    if len(rel) < 4: rel += [r for r in pakker if r["type"] == o["type"] and r not in rel and r is not o][:4-len(rel)]
    write(o["page"], drops_page(o, rel))
# betalte opskrifter (Önling m.fl.) → /opskrifter/<designer>/<navn>/
def base_name(n):
    n = re.sub(r"\s*[-–,]?\s*(?:i\s+)?No\.?\s*\d{1,2}(\s*\+\s*[\w ]+?(?:mohair|silk|tråd|follow|følgetråd))?\s*$", "", n, flags=re.I).strip(" ,-")
    return n
merged = {}
for o in [o for o in OPS if o.get("kind") in ("opskrift","kit") and o.get("image") and o.get("designer")]:
    key = (o["designer"], base_name(o["name"]).lower())
    m = merged.get(key)
    if not m:
        m = dict(o); m["name"] = base_name(o["name"]); m["kits"] = list(o.get("kits", [])); m["variants"] = [o]; merged[key] = m
    else:
        m["kits"] += o.get("kits", []); m["variants"].append(o)
        if o.get("kind") == "opskrift" and m.get("kind") == "kit": m["kind"] = "opskrift"; m["price"] = o["price"]; m["url"] = o["url"]
        if len(o.get("desc","")) > len(m.get("desc","")): m["desc"] = o["desc"]
paid = []
for m in merged.values():
    if qualifies(m, kit_yarns(m)): paid.append(m)
    else: skipped["paid"] += 1
for m in merged.values():   # alle varianter peger på den samlede side (eller ingen)
    for v in m["variants"]: v["merged_into"] = m
seen_p = {}
for o in paid:
    sl = f"{slugify(o['designer'])}/{slugify(o['name'])}"; n = seen_p.get(sl, 0); seen_p[sl] = n + 1
    o["page"] = f"/opskrifter/{sl}{'' if n==0 else '-'+str(n+1)}/"
    for v in o["variants"]: v["page"] = o["page"]
# listerne skal vise én post pr. samlet model, ikke pr. variant
OPS = [o for o in OPS if not (o.get("kind") in ("opskrift","kit") and o.get("merged_into") and o is not o["merged_into"]["variants"][0])]
for o in OPS:
    m = o.get("merged_into")
    if m: o["name"] = m["name"]; o["price"] = m["price"]; o["kind"] = m["kind"]; o["kits"] = m["kits"]; o["desc"] = m.get("desc",""); o.pop("merged_into", None)
for m in merged.values():
    for v in m["variants"]: v.pop("merged_into", None)
    m.pop("variants", None)
by_des = {}
for o in paid: by_des.setdefault(o["designer"], []).append(o)
for o in paid:
    rel = [r for r in by_des[o["designer"]] if r is not o and r["type"] == o["type"]][:4]
    rel += [r for r in by_des[o["designer"]] if r is not o and r not in rel][:4-len(rel)]
    write(o["page"], pattern_page(o, rel))
# designersider (≥ 4 opskrifter) inkl. DROPS
groups = {}
for o in OPS:
    if o.get("page") and o.get("designer"): groups.setdefault(o["designer"], []).append(o)
groups = sorted([(k, v) for k, v in groups.items() if len(v) >= 4], key=lambda kv: -len(kv[1]))
for name, items in groups: write(f"/designere/{slugify(name)}/", designer_page(name, items))
write("/designere/", designers_index(groups))
json.dump(OPS, open(f"{ROOT}/data/opskrifter.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for slug, g in PRIS.items():
    if g.get("shops"): write(f"/garn/{slug}/", garn_page(slug, g))
for c in C.CATEGORIES: write("/"+c["path"]+"/", cat_page(c))
for t in C.TYPES:
    write(f"/opskrifter/{t['slug']}/", cat_page(dict(t, path=f"opskrifter/{t['slug']}", preset=dict(type=t["type"]), sections=t.get("sections",[]))))
for n in C.NEEDLES:
    slug = "pind-" + n["n"].replace(".", "-")
    write(f"/opskrifter/{slug}/", cat_page(dict(n, path=f"opskrifter/{slug}", preset=dict(needle=n["n"]), sections=n.get("sections",[]))))
write("/gratis/", cat_page(C.GRATIS, "gratis"))
write("/garn/drops/", cat_page(C.DROPS, "drops"))
for g in C.GUIDES: write(f"/guides/{g['slug']}/", guide_page(g))
write("/guides/", guides_index())
write("/om/", om_page())

urls = ["/", "/opskrifter/", "/gratis/", "/garn/", "/garn/drops/", "/guides/", "/om/"] + [f"/{c['path']}/" for c in C.CATEGORIES] + \
       [f"/opskrifter/{t['slug']}/" for t in C.TYPES] + [f"/opskrifter/pind-{n['n'].replace('.','-')}/" for n in C.NEEDLES] + \
       [f"/guides/{g['slug']}/" for g in C.GUIDES] + [o["page"] for o in pakker] + [o["page"] for o in paid] + ["/designere/"] + [f"/designere/{slugify(n)}/" for n, _ in groups] + \
       [f"/garn/{s}/" for s, g in PRIS.items() if g.get("shops") and os.path.exists(f"{ROOT}/garn/{s}")]
open(f"{ROOT}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")
open(f"{ROOT}/robots.txt", "w").write(f"User-agent: *\nAllow: /\nDisallow: /data/\nSitemap: {BASE}/sitemap.xml\n")
print(f"Sprunget over (for tynde): {skipped['drops']} Drops, {skipped['paid']} betalte")
print(f"Skrev {len(pakker)} Drops-sider, {len(paid)} betalte opskriftssider, {len(groups)} designersider, {len(C.CATEGORIES)+2} kategorisider, {len(C.GUIDES)} guides, om-side, sitemap ({len(urls)} URL'er)")

# ---------------- Fælles header/footer på de håndskrevne sider ----------------
STATIC = {"index.html": "", "opskrifter/index.html": "opskrifter", "garn/index.html": "garn"}
def ssr_home(t):
    picks = [next((o for o in OPS if o.get("type")==ty and o.get("image") and o.get("kind")=="pakke" and o.get("page")), None) for ty in ("sweater","cardigan","hue","vest")]
    for i, o in enumerate(picks):
        if not o: continue
        t = re.sub(r'<a class="card" href="[^"]*" data-opskrift="%d">.*?</a>' % i,
                   lambda m: f'<a class="card" href="{o["page"]}" data-opskrift="{i}"><div class="img" role="img" aria-label="{e(o["name"])}" style="background-image:url(\'{e(img(o["image"]))}\')"><span class="badge">gratis</span></div><b>{e(o["name"])}</b><span>{e(o["designer"])} · gratis opskrift</span><em class="price">Garnpakke {kr(o["price"])} kr.</em></a>', t, flags=re.S)
    for m in list(re.finditer(r'<a class="card" href="[^"]*" data-garn="([^"]+)">.*?</a>', t, flags=re.S)):
        g = PRIS.get(m.group(1)); 
        if not g or not g.get("shops"): continue
        ch = next(iter(g["shops"].values())); disc = round((1-ch["price"]/ch["old_price"])*100) if ch.get("old_price") else 0
        t = t.replace(m.group(0), f'<a class="card" href="garn/{m.group(1)}/" data-garn="{m.group(1)}"><div class="img wide" role="img" aria-label="{e(g["name"])}" style="background-image:url(\'{e(img(ch["image"]))}\')"></div><b>{e(g["name"])}</b><span>{e(g["fiber"])} · {g["meters"]} m/{g["grams"]} g</span><em class="price">fra {kr(g["from_price"])} kr.{(" <span class=\"tag save\">−"+str(disc)+" %</span>") if disc>=10 else ""}</em></a>')
    return t
for rel, cur in STATIC.items():
    f = f"{ROOT}/{rel}"
    if not os.path.exists(f): continue
    orig = t = open(f, encoding="utf-8").read()
    if rel == "index.html": t = ssr_home(t)
    if 'class="sec explore"' not in t:
        t = t.replace("</main>", explore_html({"index.html":"opskrifter","opskrifter/index.html":"opskrifter","garn/index.html":"garn"}[rel]) + f'<p class="small muted byauthor">Redigeret af <a href="/om/">{e(C.OWNER)}</a> · priser opdateret {UPDATED}</p></main>', 1)
        t = t.replace("</body>", '<button class="totop" aria-label="Til toppen" hidden>↑</button></body>')
    t2 = re.sub(r"<header class=\"site\">.*?</header>", lambda m: nav(cur), t, flags=re.S)
    t2 = re.sub(r"<footer class=\"site\">.*?</footer>", lambda m: FOOT, t2, flags=re.S)
    if t2 != orig: open(f, "w", encoding="utf-8").write(t2)
print("Header/footer synkroniseret på", len(STATIC), "statiske sider")
