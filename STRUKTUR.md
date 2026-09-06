# strikkeopskrifter.dk – struktur

Statisk site. Hver side er en mappe med index.html, så URL'erne er rene uden serverkonfiguration.

```
/
├── index.html                          Forside: søg, "sådan virker det", populære opskrifter, garn på tilbud, guides
├── opskrifter/
│   ├── index.html                      Alle opskrifter (filter: kategori, niveau, gratis/betalt, garn)
│   └── <opskrift-slug>/index.html      Opskriftsside = kernen. Beregner + prissammenligning + køb
├── garn/
│   ├── index.html                      Alle garner (filter: fiber, strikkefasthed, pris)
│   └── <garn-slug>/index.html          Garnside: pris hos alle butikker, specs, "passer til opskrifter med"
├── designere/<slug>/index.html         Designerside: alle opskrifter fra én designer (senere)
├── guides/<slug>/index.html            Artikler: alternativt garn, nøgleberegning, alternativer til X (senere)
├── om/index.html                       Om siden + provisionsforklaring (lovpligtig) (senere)
├── assets/style.css                    Fælles stil – ét sted
├── assets/site.js                      Garnberegner (læser window.OPSKRIFT fra opskriftssiden)
└── _build/  data/                      Senere: JSON med opskrifter, garn, priser → genererer siderne
```

## Sammenhængen
- Opskriftsside linker til garnsider (originalgarn + alternativer) og designer.
- Garnside linker tilbage til alle opskrifter, der bruger eller kan bruge garnet.
- Guides linker ind i begge dele. Det er den interne linkstruktur, Google skal se.

## Slugs
Små bogstaver, bindestreg, ingen æøå: `rikke-cozy-sweater`, `drops-baby-merino`, `onling-no-1`.

## Data på opskriftssiden
`window.OPSKRIFT` nederst i hver opskriftsside indeholder størrelser, gram pr. størrelse pr. garn og butikker med pris + affiliate-URL. `cart:true` betyder at deeplinket lander i forudfyldt kurv (Shopify/WooCommerce). Når der er >20 opskrifter, flyttes dette til `data/` og siderne genereres af `_build/build.py`.
