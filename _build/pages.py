#!/usr/bin/env python3
"""Genererer statiske opskriftssider ud fra data/opskrifter.json + data/priser.json.
   /opskrifter/drops/<slug>/index.html  for hver Drops-garnpakke
   Kør efter feeds.py:  python3 _build/pages.py
"""
import json, os, re, html, unicodedata
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPS  = json.load(open(f"{ROOT}/data/opskrifter.json", encoding="utf-8"))
PRIS = json.load(open(f"{ROOT}/data/priser.json", encoding="utf-8"))
GARN = {g["slug"]: g for g in json.load(open(f"{ROOT}/data/garn.json", encoding="utf-8"))["garn"]}
for g in GARN.values(): g["_re"] = re.compile(g["match"], re.I)

def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = s.replace("ø","o").replace("æ","ae").replace("å","aa")
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")
def e(s): return html.escape(s or "", quote=True)
def kr(n): return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

TYPE_LABEL = {"sweater":"Sweatre & bluser","cardigan":"Cardigans","vest":"Veste","hue":"Huer","sjal":"Sjaler & tørklæder","sokker":"Sokker",
              "vanter":"Vanter","baby":"Baby","børn":"Børn","kjole":"Kjoler","hjem":"Hjem","andet":"Andet"}

HEAD = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT@9..144,400;9..144,600;9..144,700,100&family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">'''
NAV = '''<header class="site"><div class="wrap nav"><a class="logo" href="/">strikke<span>opskrifter</span>.dk</a>
<ul><li><a href="/opskrifter/" aria-current="page">Opskrifter</a></li><li><a href="/garn/">Garn</a></li><li><a href="/designere/">Designere</a></li><li><a href="/guides/">Guides</a></li></ul></div></header>'''
FOOT = '''<footer class="site"><div class="wrap"><div>strikkeopskrifter.dk · Find opskriften, regn garnet ud, og køb det hvor det er billigst.</div>
<div><a href="/om/">Om siden</a> · <a href="/om/#provision">Sådan tjener vi penge</a> · <a href="/om/#kontakt">Kontakt</a></div></div></footer>'''

def find_yarns(text):
    """Finder 'Drops Belle', 'Drops Kid-Silk' m.m. i beskrivelsen. Returnerer [(navn, slug|None)]"""
    out, seen = [], set()
    for m in re.finditer(r"Drops\s+([A-ZÆØÅ][\w-]*(?:\s+[A-ZÆØÅ][\w-]*){0,2})", text):
        name = "Drops " + m.group(1).strip(" .,")
        name = re.sub(r"\s+(garn|og|eller|som|der|i)$", "", name, flags=re.I)
        if name.lower() in seen or len(name) < 8: continue
        seen.add(name.lower())
        slug = next((s for s, g in GARN.items() if g["_re"].search(name)), None)
        out.append((name, slug))
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

def page(o, related):
    yarns = find_yarns(o.get("desc",""))
    title = f"{o['name']} – gratis strikkeopskrift fra DROPS ({TYPE_LABEL.get(o['type'],'').lower() or o.get('type_label','')})"
    desc = f"{o['name']} by DROPS Design: gratis strikkeopskrift{(' i str. '+o['sizes']) if o.get('sizes') else ''}. Se hvilket garn du skal bruge, sammenlign prisen, eller køb garnpakken samlet."
    yarn_html = ""
    for name, slug in yarns:
        g = GARN.get(slug); p = PRIS.get(slug)
        spec = f"{g['fiber']} · {g['grams']} g / {g['meters']} m · {g['gauge']} m på 10 cm" if g else ""
        link = f'<a href="/garn/{slug}/">{e(name)}</a>' if slug and p and p.get("shops") else e(name)
        rows = shop_rows(slug) if slug else ""
        yarn_html += f'''<section class="panel" style="margin-bottom:20px"><h3 style="margin-bottom:4px">{link}</h3><p class="muted small" style="margin:0 0 12px">{e(spec)}</p>
{rows if rows else '<p class="muted small">Vi har ikke priser på dette garn endnu – brug garnpakken herunder.</p>'}</section>'''
    if not yarns:
        yarn_html = '<p class="muted">Garnet fremgår ikke af beskrivelsen – se opskriften for materialeliste.</p>'
    rel_html = "".join(f'''<a class="card" href="/opskrifter/drops/{r['slug']}/"><div class="img" style="background:center/cover url('{e(r['image'])}')"></div><b>{e(r['name'])}</b><span>DROPS Design · gratis</span><em class="price">Garnpakke {kr(r['price'])} kr.</em></a>''' for r in related)
    return f'''<!DOCTYPE html>
<html lang="da"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | strikkeopskrifter.dk</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="https://strikkeopskrifter.dk/opskrifter/drops/{o['slug']}/">
<meta property="og:image" content="{e(o['image'])}">{HEAD}
<style>.hero{{display:grid;grid-template-columns:5fr 6fr;gap:48px;padding:24px 0 40px;align-items:start}}.swatch{{aspect-ratio:4/5;background:var(--stone-2) center/cover;border:1px solid var(--line)}}
.byline{{color:var(--ink-2);margin:10px 0 18px}}.lead{{font-size:17px;max-width:56ch;margin:0 0 24px}}.cta-row{{display:flex;gap:12px;flex-wrap:wrap}}@media(max-width:860px){{.hero{{grid-template-columns:1fr}}}}</style>
</head><body>{NAV}<main class="wrap">
<div class="crumbs"><a href="/">Forside</a> / <a href="/opskrifter/">Opskrifter</a> / <a href="/opskrifter/?des=DROPS+Design">DROPS Design</a> / <a href="/opskrifter/?kategori={o['type']}">{e(TYPE_LABEL.get(o['type'],'Andet'))}</a></div>
<section class="hero"><div class="swatch" role="img" aria-label="{e(o['name'])}" style="background-image:url('{e(o['image'])}')"></div>
<div><h1>{e(o['name'])}</h1><p class="byline">Design af DROPS Design · Gratis opskrift{(' · Str. '+e(o['sizes'])) if o.get('sizes') else ''}</p>
<p class="lead">{e(o.get('desc',''))}</p>
<div class="cta-row"><a class="btn btn-primary" href="#garn">Se garn og pris</a><a class="btn btn-ghost" href="{e(o['url'])}" rel="sponsored nofollow" target="_blank">Hent opskriften gratis</a></div>
<p class="small muted" style="margin-top:12px">Opskriften er gratis hos DROPS. Garnet køber du hvor det er billigst – eller som samlet pakke.</p></div></section>
<section id="garn" style="display:grid;grid-template-columns:7fr 4fr;gap:40px;margin-bottom:56px">
<div><h2 style="margin-bottom:16px">Garnet til {e(o['name'])}</h2>{yarn_html}
<p class="disclose">Vi får en lille provision, hvis du køber via vores links. Det ændrer ikke prisen for dig.</p></div>
<aside class="panel"><h3 style="margin-bottom:6px">Alt garnet i én pakke</h3><p class="muted small" style="margin:0 0 14px">{e(o['shop_name'])} sælger garnet til {e(o['name'])} som samlet pakke i din størrelse{(' ('+e(o['sizes'])+')') if o.get('sizes') else ''}. Opskriften henter du gratis.</p>
<div class="from" style="font-family:var(--serif);font-size:30px;font-weight:600;margin-bottom:12px">{kr(o['price'])} kr.</div>
<a class="btn btn-primary" style="display:block" href="{e(o['url'])}" rel="sponsored nofollow" target="_blank">Se garnpakken hos {e(o['shop_name'])}</a></aside></section>
<section class="sec" style="margin-top:0"><div class="sec-head"><h2>Flere gratis DROPS-opskrifter – {e(TYPE_LABEL.get(o['type'],'andet').lower())}</h2><a href="/opskrifter/?kategori={o['type']}">Se alle →</a></div><div class="grid">{rel_html}</div></section>
</main>{FOOT}</body></html>'''

# ---- kør ----
pakker = [o for o in OPS if o.get("kind") == "pakke" and o.get("image")]
seen = {}
for o in pakker:
    s = slugify(o["name"]); n = seen.get(s, 0); seen[s] = n + 1
    o["slug"] = s if n == 0 else f"{s}-{n+1}"
by_type = {}
for o in pakker: by_type.setdefault(o["type"], []).append(o)
count = 0
for o in pakker:
    rel = [r for r in by_type[o["type"]] if r is not o][:4]
    d = f"{ROOT}/opskrifter/drops/{o['slug']}"; os.makedirs(d, exist_ok=True)
    open(f"{d}/index.html", "w", encoding="utf-8").write(page(o, rel)); count += 1
    o["page"] = f"/opskrifter/drops/{o['slug']}/"
json.dump(OPS, open(f"{ROOT}/data/opskrifter.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# sitemap
urls = ["https://strikkeopskrifter.dk/", "https://strikkeopskrifter.dk/opskrifter/", "https://strikkeopskrifter.dk/garn/"] + \
       [f"https://strikkeopskrifter.dk{o['page']}" for o in pakker] + [f"https://strikkeopskrifter.dk/garn/{s}/" for s, g in PRIS.items() if g.get("shops") and os.path.exists(f"{ROOT}/garn/{s}")]
open(f"{ROOT}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
print(f"Skrev {count} opskriftssider + sitemap.xml ({len(urls)} URL'er)")
