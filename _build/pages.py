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

def slugify(s):
    s = s.lower().replace("ø","o").replace("æ","ae").replace("å","aa")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")
def e(s): return html.escape(str(s or ""), quote=True)
def kr(n): return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def jsonld(obj): return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'

TYPE_LABEL = {"sweater":"Sweatre & bluser","cardigan":"Cardigans","vest":"Veste","hue":"Huer","sjal":"Sjaler & tørklæder","sokker":"Sokker",
              "vanter":"Vanter","baby":"Baby","børn":"Børn","kjole":"Kjoler","hjem":"Hjem","andet":"Andet"}
TARGET_LABEL = {"dame":"damer","herre":"herrer","børn":"børn","baby":"baby"}

HEAD = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT@9..144,400;9..144,600;9..144,700,100&family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">'''
def nav(current=""):
    def a(href, label, key): return f'<li><a href="{href}"{" aria-current=page" if key==current else ""}>{label}</a></li>'
    return f'''<header class="site"><div class="wrap nav"><a class="logo" href="/">strikke<span>opskrifter</span>.dk</a>
<ul>{a("/opskrifter/","Opskrifter","opskrifter")}{a("/gratis/","Gratis","gratis")}{a("/garn/","Garn","garn")}{a("/garn/drops/","DROPS","drops")}{a("/guides/","Guides","guides")}</ul></div></header>'''
FOOT = f'''<footer class="site"><div class="wrap"><div>strikkeopskrifter.dk · Find opskriften, regn garnet ud, og køb det hvor det er billigst.<br><span style="opacity:.7">Opskrifter: <a href="/opskrifter/dame/">Damer</a> · <a href="/opskrifter/boern/">Børn</a> · <a href="/opskrifter/baby/">Baby</a> · <a href="/opskrifter/herre/">Herrer</a> · <a href="/opskrifter/begynder/">Begyndere</a> · <a href="/gratis/">Gratis</a> · <a href="/garn/drops/">DROPS</a></span></div>
<div><a href="/om/">Om siden</a> · <a href="/om/#provision">Sådan tjener vi penge</a> · <a href="/om/#kontakt">Kontakt</a></div></div></footer>'''

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

def shell(title, meta, path, body, lds, current="", og_image=None):
    ld_html = "".join(jsonld(x) for x in lds if x)
    og = f'<meta property="og:image" content="{e(og_image)}">' if og_image else ""
    return f'''<!DOCTYPE html>
<html lang="da"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | strikkeopskrifter.dk</title><meta name="description" content="{e(meta)}">
<link rel="canonical" href="{BASE}{path}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(meta)}">{og}
{HEAD}{ld_html}</head><body>{nav(current)}<main class="wrap">{body}</main>{FOOT}<script src="/assets/site.js"></script></body></html>'''

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

def shop_rows(slug):
    g = PRIS.get(slug); rows = []
    if not g: return ""
    for i, s in enumerate(v for v in g["shops"].values() if v["price"]):
        note = " · ".join(x for x in [f"Fri fragt over {s['free_shipping_from']} kr." if s.get("free_shipping_from") else "", f"{s.get('colors_in_stock',0)} farver på lager"] if x)
        v = next((v for v in s["variants"] if v["stock"]=="in_stock" and v.get("cart")), None)
        rows.append(f'''<div class="shop {'best' if i==0 else ''}"><div class="name">{e(s['shop'])}<small>{e(note)}</small></div>
<div class="price">{kr(s['price'])} kr.<small>pr. nøgle</small></div><a class="go" href="{e(v['cart'] if v else s['url'])}" rel="sponsored nofollow" target="_blank">{'Læg i kurven' if v else 'Gå til butik'}</a></div>''')
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

def drops_page(o, related):
    yarns = find_yarns(o.get("desc",""))
    tl = TYPE_LABEL.get(o["type"], "andet").lower()
    tgt = TARGET_LABEL.get(o.get("target","dame"), "damer")
    title = f"{o['name']} – gratis strikkeopskrift fra DROPS ({tl}, {tgt})"
    meta = f"{o['name']} by DROPS Design: gratis strikkeopskrift til {tgt}{(' i str. '+o['sizes']) if o.get('sizes') else ''}. Se hvilket garn du skal bruge, sammenlign prisen, eller køb garnpakken samlet."
    path = o["page"]
    yarn_html = ""
    for name, slug in yarns:
        g = GARN.get(slug); p = PRIS.get(slug)
        spec = f"{g['fiber']} · {g['grams']} g / {g['meters']} m · {g['gauge']} m på 10 cm · pind {g['needle']}" if g else ""
        link = f'<a href="/garn/{slug}/">{e(name)}</a>' if slug and p and p.get("shops") else e(name)
        rows = shop_rows(slug) if slug else ""
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
    faq_html, faq_ld = faq_block(faq, f"Spørgsmål om {o['name']}")
    crumbs, crumb_ld = breadcrumbs([("Forside","/"),("Opskrifter","/opskrifter/"),("DROPS","/garn/drops/"),(TYPE_LABEL.get(o['type'],'Andet'), f"/opskrifter/?kategori={o['type']}"),(o['name'],None)])
    rel_html = "".join(f'''<a class="card" href="{r['page']}"><div class="img" style="background:center/cover url('{e(r['image'])}')"></div><b>{e(r['name'])}</b><span>DROPS Design · gratis · {TARGET_LABEL.get(r.get('target',''),'')}</span><em class="price">Garnpakke {kr(r['price'])} kr.</em></a>''' for r in related)
    product_ld = {"@context":"https://schema.org","@type":"Product","name":f"{o['name']} – garnpakke","image":o["image"],"description":o.get("desc",""),
                  "brand":{"@type":"Brand","name":"DROPS Design"},"offers":{"@type":"Offer","priceCurrency":"DKK","price":o["price"],"availability":"https://schema.org/InStock" if o.get("stock")=="in_stock" else "https://schema.org/BackOrder","seller":{"@type":"Organization","name":o["shop_name"]}}}
    body = f'''{crumbs}
<style>.hero{{display:grid;grid-template-columns:5fr 6fr;gap:48px;padding:24px 0 40px;align-items:start}}.swatch{{aspect-ratio:4/5;background:var(--stone-2) center/cover;border:1px solid var(--line)}}
.byline{{color:var(--ink-2);margin:10px 0 18px}}.lead{{font-size:17px;max-width:56ch;margin:0 0 24px}}.cta-row{{display:flex;gap:12px;flex-wrap:wrap}}.two{{display:grid;grid-template-columns:7fr 4fr;gap:40px;margin-bottom:48px}}@media(max-width:860px){{.hero,.two{{grid-template-columns:1fr}}}}</style>
<section class="hero"><div class="swatch" role="img" aria-label="{e(o['name'])}" style="background-image:url('{e(o['image'])}')"></div>
<div><h1>{e(o['name'])}</h1><p class="byline">Design af DROPS Design · Gratis opskrift · Til {tgt}{(' · Str. '+e(o['sizes'])) if o.get('sizes') else ''} · Niveau: {e(o.get('level','let øvet'))}</p>
<p class="lead">{e(o.get('desc',''))}</p>
<div class="cta-row"><a class="btn btn-primary" href="#garn">Se garn og pris</a><a class="btn btn-ghost" href="{e(o['url'])}" rel="sponsored nofollow" target="_blank">Hent opskriften gratis</a></div>
<p class="small muted" style="margin-top:12px">Opskriften er gratis hos DROPS. Garnet køber du hvor det er billigst – eller som samlet pakke.</p></div></section>
<section id="garn" class="two"><div><h2 style="margin-bottom:8px">Garnet til {e(o['name'])}</h2><p class="muted" style="margin:0 0 18px;max-width:60ch">{e(TYPE_SENT.get(o['type'],''))} Priserne herunder hentes hver nat fra butikkernes egne feeds.</p>{yarn_html}
<p class="disclose">Vi får en lille provision, hvis du køber via vores links. Det ændrer ikke prisen for dig, og det påvirker ikke, hvilken butik vi viser som billigst.</p></div>
<aside class="panel"><h3 style="margin-bottom:6px">Alt garnet i én pakke</h3><p class="muted small" style="margin:0 0 14px">{e(o['shop_name'])} sælger garnet til {e(o['name'])} som samlet pakke i din størrelse{(' ('+e(o['sizes'])+')') if o.get('sizes') else ''}. Opskriften henter du gratis.</p>
<div style="font-family:var(--serif);font-size:30px;font-weight:600;margin-bottom:12px">{kr(o['price'])} kr.</div>
<a class="btn btn-primary" style="display:block" href="{e(o['url'])}" rel="sponsored nofollow" target="_blank">Se garnpakken hos {e(o['shop_name'])}</a>
<p class="small muted" style="margin:16px 0 0">Ny i strik? Læs <a href="/guides/hvor-mange-noegler/">hvor mange nøgler du skal bruge</a> og <a href="/guides/vaelg-alternativt-garn/">hvordan du vælger et andet garn</a>.</p></aside></section>
{faq_html}
<section class="sec"><div class="sec-head"><h2>Flere gratis DROPS-opskrifter – {e(tl)} til {e(tgt)}</h2><a href="/opskrifter/?kategori={o['type']}">Se alle →</a></div><div class="grid">{rel_html}</div></section>'''
    return shell(title, meta, path, body, [crumb_ld, faq_ld, product_ld], "drops", o["image"])

# ---------------- kategorisider / hubs ----------------
def grid_html(preset):
    attrs = " ".join(f'data-{k}="{e(v)}"' for k, v in preset.items())
    return f'''<div class="filters" role="group" aria-label="Filtrér">
    <input type="search" id="f-q" placeholder="Søg opskrift, garn …" aria-label="Søg">
    <select id="f-kat" aria-label="Kategori" {'hidden' if 'type' in preset else ''}><option value="">Alle kategorier</option>{''.join(f'<option value="{k}">{v}</option>' for k,v in TYPE_LABEL.items() if k!='andet')}</select>
    <select id="f-target" aria-label="Til" {'hidden' if 'target' in preset else ''}><option value="">Alle</option><option value="dame">Damer</option><option value="herre">Herrer</option><option value="børn">Børn</option><option value="baby">Baby</option></select>
    <select id="f-des" aria-label="Designer" {'hidden' if 'designer' in preset else ''}><option value="">Alle designere</option></select>
    <select id="f-free" aria-label="Pris" {'hidden' if 'free' in preset else ''}><option value="">Betalt og gratis</option><option value="1">Kun gratis</option></select>
    <select id="f-sort" aria-label="Sortering"><option value="">Nyeste</option><option value="pris">Billigste garn</option><option value="navn">A–Å</option></select>
    <span id="f-count" class="muted small" style="align-self:center"></span></div>
  <div class="grid" id="opskrift-grid" {attrs}></div>'''

def cat_page(c, current="opskrifter"):
    path = "/" + c["path"] + "/"
    intro = "".join(f"<p>{e(p)}</p>" for p in c["intro"])
    secs = "".join(f'<section class="sec"><h2>{e(h)}</h2><p>{e(t)}</p></section>' for h, t in c["sections"])
    faq_html, faq_ld = faq_block(c["faq"])
    crumbs, crumb_ld = breadcrumbs([("Forside","/"),("Opskrifter","/opskrifter/"),(c["h1"],None)] if c["path"].startswith("opskrifter") else [("Forside","/"),(c["h1"],None)])
    coll_ld = {"@context":"https://schema.org","@type":"CollectionPage","name":c["title"],"description":c["meta"],"url":BASE+path,"isPartOf":{"@type":"WebSite","name":"strikkeopskrifter.dk","url":BASE}}
    body = f'''{crumbs}<h1 style="margin-top:12px">{e(c['h1'])}</h1><div class="prose intro">{intro}</div>
{grid_html(c['preset'])}
<div class="prose">{secs}</div>{faq_html}'''
    return shell(c["title"], c["meta"], path, body, [crumb_ld, coll_ld, faq_ld], current)

def guide_page(g):
    path = f"/guides/{g['slug']}/"
    body_html = "".join(f"<h2>{e(h)}</h2><p>{e(t)}</p>" for h, t in g["body"])
    faq_html, faq_ld = faq_block(g["faq"])
    crumbs, crumb_ld = breadcrumbs([("Forside","/"),("Guides","/guides/"),(g["h1"],None)])
    art_ld = {"@context":"https://schema.org","@type":"Article","headline":g["title"],"description":g["meta"],"author":{"@type":"Person","name":C.OWNER},"publisher":{"@type":"Organization","name":"strikkeopskrifter.dk"},"url":BASE+path}
    body = f'''{crumbs}<article class="prose" style="max-width:68ch"><h1 style="margin:12px 0 8px">{e(g['h1'])}</h1><p class="muted small">Af {e(C.OWNER)} · strikkeopskrifter.dk</p>{body_html}</article>{faq_html}'''
    return shell(g["title"], g["meta"], path, body, [crumb_ld, art_ld, faq_ld], "guides")

def guides_index():
    cards = "".join(f'<a class="card" href="/guides/{g["slug"]}/"><div class="img wide" style="background:var(--stone-2)"></div><b>{e(g["h1"])}</b><span>{e(g["meta"][:90])}…</span></a>' for g in C.GUIDES)
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

pakker = [o for o in OPS if o.get("kind") == "pakke" and o.get("image")]
seen = {}
for o in pakker:
    s = slugify(o["name"]); n = seen.get(s, 0); seen[s] = n + 1
    o["slug"] = s if n == 0 else f"{s}-{n+1}"; o["page"] = f"/opskrifter/drops/{o['slug']}/"
by_key = {}
for o in pakker: by_key.setdefault((o["type"], o.get("target")), []).append(o)
for o in pakker:
    rel = [r for r in by_key[(o["type"], o.get("target"))] if r is not o][:4]
    if len(rel) < 4: rel += [r for r in pakker if r["type"] == o["type"] and r not in rel and r is not o][:4-len(rel)]
    write(o["page"], drops_page(o, rel))
json.dump(OPS, open(f"{ROOT}/data/opskrifter.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for c in C.CATEGORIES: write("/"+c["path"]+"/", cat_page(c))
write("/gratis/", cat_page(C.GRATIS, "gratis"))
write("/garn/drops/", cat_page(C.DROPS, "drops"))
for g in C.GUIDES: write(f"/guides/{g['slug']}/", guide_page(g))
write("/guides/", guides_index())
write("/om/", om_page())

urls = ["/", "/opskrifter/", "/gratis/", "/garn/", "/garn/drops/", "/guides/", "/om/"] + [f"/{c['path']}/" for c in C.CATEGORIES] + \
       [f"/guides/{g['slug']}/" for g in C.GUIDES] + [o["page"] for o in pakker] + \
       [f"/garn/{s}/" for s, g in PRIS.items() if g.get("shops") and os.path.exists(f"{ROOT}/garn/{s}")]
open(f"{ROOT}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{BASE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
open(f"{ROOT}/robots.txt", "w").write(f"User-agent: *\nAllow: /\nDisallow: /data/\nSitemap: {BASE}/sitemap.xml\n")
print(f"Skrev {len(pakker)} opskriftssider, {len(C.CATEGORIES)+2} kategorisider, {len(C.GUIDES)} guides, om-side, sitemap ({len(urls)} URL'er)")
