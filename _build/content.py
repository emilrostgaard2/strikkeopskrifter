# -*- coding: utf-8 -*-
"""Tekster til kategorisider, hubs og guides. Hver side har ét primært søgeord og en unik vinkel,
så siderne ikke konkurrerer med hinanden. Redigér frit – pages.py bygger HTML'en."""

SITE = "strikkeopskrifter.dk"
OWNER = "Emil Rostgaard"
AUTHORS = {
 "emil": dict(slug="emil-rostgaard", name="Emil Rostgaard", role="Grundlægger · data, priser og teknik",
   photo="/assets/img/team/emil-rostgaard.jpg", linkedin="https://www.linkedin.com/in/emil-rostgaard-702809195/",
   bio=("Emil har bygget strikkeopskrifter.dk og står for det, der gør siden anderledes: prisdata fra butikkerne, garntabellen, "
        "beregneren og den natlige opdatering. Han strikker ikke selv – og skriver det åbent – men han har bygget prissammenligninger "
        "før og ved, hvad der skal til, for at tal er til at stole på. Alt, der handler om garn og teknik, bliver tjekket af redaktionens strikker."),
   short="Står for data, priser, SEO og teknik."),
 "mette": dict(slug="mette-hansen", name="Mette Hansen", role="Strikker · hjælper med garn og strik",
   photo="", linkedin="",
   bio=("Mette strikker og hjælper redaktionen, når der er spørgsmål om garn, teknik og hvad der virker i praksis. Hun læser guides "
        "og garntekster igennem, før de udgives, og siger til, hvis noget lyder forkert. Hun er ikke ansat, og hun sælger ikke garn – "
        "hun er den, vi spørger, når banderolen og virkeligheden ikke stemmer overens."),
   short="Læser guides igennem og hjælper med garn- og strikkespørgsmål."),
}
OWNER_BIO = AUTHORS["emil"]["bio"]

# ---------- kategorisider under /opskrifter/ ----------
# preset = de filtre, siden er låst til. Grid'et viser kun opskrifter der matcher.
CATEGORIES = [
 dict(slug="dame", path="opskrifter/dame", preset=dict(target="dame"),
  kw="strikkeopskrifter dame", title="Strikkeopskrifter til damer – sweatre, cardigans, veste og sjaler",
  meta="Strikkeopskrifter til damer med garnforbrug pr. størrelse og prissammenligning. Gratis og betalte opskrifter fra DROPS, PetiteKnit m.fl. – find den billigste vej til dit næste projekt.",
  h1="Strikkeopskrifter til damer",
  intro=[
   "Her finder du strikkeopskrifter til damer samlet ét sted – oversize sweatre, raglan-cardigans, slipovers, sommertoppe og sjaler – fra danske og nordiske designere som DROPS Design, PetiteKnit og Rikke Jönsson. Det, der adskiller listen fra en almindelig opskriftssamling, er, at vi for hver opskrift viser, hvilket garn den er strikket i, og hvad garnet koster i dag hos de danske butikker, vi sammenligner.",
   "En stor del af opskrifterne er gratis. Det gælder alle DROPS-opskrifter, hvor du henter PDF'en uden beregning og kun betaler for garnet. Vil du hellere have en betalt opskrift fra en dansk designer, kan du filtrere på designer og sortere efter, hvad garnet koster – ofte er forskellen mellem billigste og dyreste butik 100–200 kr. på en sweater.",
  ],
  sections=[
   ("Garn til damestrik: fire typer, du møder igen og igen", "Merino (Baby Merino, Merino Extra Fine, Önling No 3) er det sikre valg – blødt, elastisk, tåler vask. Alpaka (Drops Alpaca, Puna) er varmere og falder tungere. Mohair/silke (Kid-Silk, Önling No 10) holdes sammen med et andet garn og giver den luftige nordiske look. Bomuld og hør (Belle, Safran, Önling No 21) er til sommer. På opskriftssiderne viser vi, hvilken af de fire opskriften bruger, og hvad den koster."),
   ("Sådan bruger du siden til damestrik", "Vælg først, hvad du vil strikke – sweater, cardigan, vest – og om den skal være gratis. Klik ind på opskriften, vælg din størrelse i beregneren, og se prisen hos hver butik. Er originalgarnet dyrt, står alternativerne lige under. Klik 'Læg i kurven', så lander du i butikkens kurv med det rigtige antal nøgler."),

   ("Sådan vælger du den rigtige størrelse", "Danske og nordiske damesweatre strikkes i dag ofte med 10–25 cm positiv ease – altså løsere end din overvidde. Tjek altid opskriftens færdige mål frem for kun bogstavstørrelsen: en M hos én designer kan svare til en L hos en anden. Er du i tvivl, så mål en sweater du allerede er glad for, og vælg den størrelse i opskriften, der kommer tættest på."),
   ("Hvad koster det at strikke en damesweater?", "Regn med 300–600 g garn til en voksensweater afhængigt af tykkelse og pasform. I et budgetgarn som Drops Baby Merino til omkring 23 kr. pr. nøgle lander du på 200–300 kr. I et merino/angora-garn fra Önling eller et Sandnes-garn ligger prisen typisk på 800–1.400 kr. Vores beregner på hver opskriftsside regner det ud for din størrelse og viser, hvor det er billigst."),
   ("Populære teknikker i dameopskrifter lige nu", "Raglan strikket oppefra og ned dominerer, fordi det er nemt at prøve undervejs og kræver ingen sammensyning. Rundt bærestykke med hulmønster eller fair isle er den klassiske nordiske variant. Vendepinde i nakken, italiensk opslagning og dobbeltstrikkede kanter er detaljer, der løfter resultatet – og som vi markerer på opskriftssiden, så du ved, hvad du går ind til."),
  ],
  faq=[
   ("Er strikkeopskrifter til damer gratis?", "Mange er. Alle DROPS Designs opskrifter kan hentes gratis, og flere garnbutikker giver gratis opskrifter med, når du køber garnet. Betalte opskrifter fra danske designere koster typisk 40–80 kr. Brug filteret 'Kun gratis' for kun at se de gratis."),
   ("Hvilket garn er bedst til en damesweater?", "Det afhænger af, om du vil have varme, drapering eller slid. Merino er blødt og alsidigt, alpaka er varmere og tungere, mohair holdt sammen med merino giver den luftige nordiske look. Tjek altid strikkefastheden i opskriften – den er vigtigere end fiberen."),
   ("Kan jeg bruge et andet garn end det, opskriften angiver?", "Ja, hvis du rammer samme strikkefasthed. Find et garn med samme antal masker pr. 10 cm og regn mængden om i meter, ikke gram. På hver opskriftsside foreslår vi 2–3 alternativer i samme fasthed, ofte til en brøkdel af prisen."),
   ("Hvor mange nøgler skal jeg bruge?", "Det står i opskriftens materialeliste pr. størrelse. På vores opskriftssider vælger du din størrelse, og beregneren viser antal nøgler og samlet pris hos hver butik."),
  ]),

 dict(slug="boern", path="opskrifter/boern", preset=dict(target="børn"),
  kw="strikkeopskrifter børn", title="Strikkeopskrifter til børn – sweatre, cardigans, huer og sokker",
  meta="Strikkeopskrifter til børn i alderen 2–14 år. Se garnforbrug pr. størrelse, find gratis DROPS-opskrifter og sammenlign garnpriser hos danske butikker.",
  h1="Strikkeopskrifter til børn",
  intro=[
   "Børnestrik er taknemmeligt: projekterne er små, garnforbruget er lavt, og du ser resultatet hurtigt. Her er strikkeopskrifter til børn fra 2 til 14 år – sweatre, cardigans, huer, vanter, sokker og dukketøj – med garnforbrug pr. størrelse og dagens garnpris, så du kan se, om projektet koster 80 eller 300 kr., før du går i gang.",
   "De fleste børneopskrifter her er gratis DROPS-opskrifter, hvor du kun betaler for garnet. Vi viser også PetiteKnits junior-versioner og andre danske designere, når de findes i en børnestørrelse.",
  ],
  sections=[
   ("Hvor lang tid tager børnestrik?", "En hue: 2–3 timer. En sweater til en 4-årig: 8–12 timer. En cardigan til en 10-årig: 15–20 timer. Det er små projekter, og det er derfor, de er gode til at prøve nye teknikker – hulmønster, striber, raglan – uden at binde 40 timer."),
   ("Restegarn og børnestrik", "Børnestørrelser er oplagte til restegarn: en 2-års sweater kan strikkes af 3 nøgler. Kig efter opskrifter med striber, så du kan blande farver, og brug beregneren til at se, hvor mange meter du reelt skal bruge."),

   ("Vælg et garn, der tåler vask", "Børnetøj bliver vasket ofte. Vælg superwash-behandlet merino (fx Drops Baby Merino eller Merino Extra Fine), en uld/bomuld-blanding eller ren bomuld til sommer. Undgå løst spundet alpaka og mohair til de mindste – det fnugger, og det filter i maskinen."),
   ("Størrelser og vokseplads", "Børnestørrelser angives i alder (2, 4, 6 år …) eller centilong. Strik gerne en størrelse op – et barn på 4 år passer ofte en 5–6-års sweater året ud. Længde er nemmere at justere end vidde, så tag ekstra centimeter på krop og ærmer."),
   ("Nemme projekter at starte med", "Huer, halsrør og en simpel raglan oppefra og ned er de bedste begynderprojekter til børn: få masker, ingen sammensyning, og du kan prøve undervejs. Sokker og vanter kræver lidt mere teknik (hælle, tommelfingre), men garnforbruget er minimalt."),
  ],
  faq=[
   ("Hvor meget garn skal jeg bruge til en børnesweater?", "Typisk 150–300 g afhængigt af alder og garntykkelse. En 4-års sweater i Baby Merino kræver omkring 4 nøgler à 50 g – under 100 kr. i garn."),
   ("Findes der gratis strikkeopskrifter til børn?", "Ja, hundredvis. Alle DROPS-børneopskrifter er gratis at hente. Filtrér på 'Kun gratis', så ser du kun dem."),
   ("Hvilket garn kan tåle maskinvask?", "Superwash-merino, bomuld og de fleste uld/akryl-blandinger. Tjek altid banderolen – og vask på uldprogram, selv om det er superwash."),
   ("Hvad er forskellen på baby- og børneopskrifter?", "Babyopskrifter dækker 0–2 år og har ofte knapper i skulderen og ekstra vidde til bleen. Børneopskrifter fra 2 år og op er skaleret som voksenmodeller. Vi har en separat side til babystrik."),
  ]),

 dict(slug="baby", path="opskrifter/baby", preset=dict(target="baby"),
  kw="strikkeopskrifter baby", title="Strikkeopskrifter til baby – bluser, dragter, huer og tæpper (0–2 år)",
  meta="Strikkeopskrifter til baby 0–2 år, inkl. præmatur. Gratis DROPS-opskrifter, garnforbrug pr. størrelse og garnpriser hos danske butikker.",
  h1="Strikkeopskrifter til baby",
  intro=[
   "Babystrik er ofte det første, man strikker til andre – en lille bluse, en hue til hjemturen fra hospitalet eller et tæppe til barnevognen. Her har vi samlet strikkeopskrifter til baby fra 0 til 2 år, inklusive størrelser til for tidligt fødte. Alle opskrifter viser garnforbrug og dagens pris på garnet, og de fleste er gratis.",
   "Til baby betyder garnvalget mere end noget andet: det skal være blødt mod huden, kunne vaskes, og ikke fnugge. Vi markerer på hver opskrift, hvilket garn den er strikket i, og foreslår alternativer, der opfylder de tre krav.",
  ],
  sections=[
   ("Gaveidéer til nybagte forældre", "Et tæppe (80 × 80 cm) i superwash-merino, en hue med fold og et par futter er de tre klassikere. Tæppet bruger 250–350 g, huen og futterne ét nøgle hver. Vælg lyse, ensfarvede nuancer – de passer til alt, og forældrene kan vaske dem."),
   ("Sikkerhed i babystrik", "Undgå lange bånd og løse knapper til de mindste. Strik hellere knapper i skulderen end i front, og vælg garn uden løse fibre (ingen mohair, ingen angora) til det, der er tæt på ansigtet."),

   ("Garn til baby: det skal du tjekke", "Vælg superwash-merino eller merino/bomuld i tynd til mellemtyk kvalitet (24–28 masker pr. 10 cm). Drops Baby Merino er den klassiske budgetløsning; Sandnes Sunday og Knitting for Olive Merino er blødere og lidt dyrere. Undgå angora, mohair og løst spundet alpaka til nyfødte."),
   ("Størrelser: 0–1 mdr, 1–3 mdr, 6–9 mdr …", "Babyer vokser hurtigt – strik til den størrelse, barnet har om 2–3 måneder, ikke i dag. Til gaver ved fødslen er 3–6 mdr det sikre valg. Præmatur-størrelser (under 50 cm) findes i udvalgte DROPS-opskrifter og bruges også af hospitaler og Mødrehjælpen."),
   ("Nemme babyprojekter", "Tæpper i retstrik, huer med fold og en bluse med knapper i skulderen er de nemmeste. En babydragt tager længere tid, men er et fantastisk gaveprojekt."),
  ],
  faq=[
   ("Hvor meget garn skal jeg bruge til en babybluse?", "50–150 g. Til str. 3–6 mdr rækker 2–3 nøgler à 50 g i de fleste merinogarner – under 75 kr."),
   ("Er strikkeopskrifter til baby gratis?", "De fleste her på siden er. DROPS har hundredvis af gratis babyopskrifter, og du betaler kun for garnet."),
   ("Hvilket garn er blødest til nyfødte?", "Ekstrafin merino i superwash-kvalitet. Det kløer ikke, kan maskinvaskes på uldprogram og er ikke allergent på samme måde som angora eller mohair."),
   ("Kan jeg strikke til for tidligt fødte?", "Ja – flere DROPS-opskrifter har præmatur-størrelser. Brug søgefeltet med ordet 'præmatur'."),
  ]),

 dict(slug="herre", path="opskrifter/herre", preset=dict(target="herre"),
  kw="strikkeopskrifter herre", title="Strikkeopskrifter til herrer og mænd – sweatre, huer og cardigans",
  meta="Strikkeopskrifter til herrer: klassiske sweatre, raglan, huer og cardigans i herrestørrelser S–3XL. Se garnforbrug og garnpriser hos danske butikker.",
  h1="Strikkeopskrifter til herrer",
  intro=[
   "Strikkeopskrifter til mænd er sværere at finde end til damer, og det er ofte de samme fem modeller, der går igen. Her har vi samlet dem, der faktisk findes i rigtige herrestørrelser – klassiske rundhalssweatre, raglan strikket oppefra og ned, huer, halsrør og enkelte cardigans – med garnforbrug pr. størrelse og dagens garnpris.",
   "Herreopskrifter kræver mere garn end dameopskrifter (typisk 500–800 g til en sweater), så prisforskellen mellem butikkerne betyder mere. Vores beregner viser, hvor de 12–16 nøgler er billigst.",
  ],
  sections=[
   ("Herrestrik: de fem modeller, der faktisk bliver brugt", "En enkel rundhalssweater i glatstrik, en raglansweater, en hue i rib, et halsrør og en cardigan med lynlås. Det er dem, mænd tager på. Fair isle-bærestykker er flotte, men ender ofte i skabet. Vi har markeret de enkle modeller nedenfor."),
   ("Garnforbrug og pris til herrestørrelser", "En herresweater i str. L bruger 550–700 g – 11–14 nøgler à 50 g. I Drops Merino Extra Fine (ca. 25 kr.) er det 275–350 kr.; i Önling No 3 (71 kr.) 780–1.000 kr. Beregneren viser tallet for præcis din størrelse."),

   ("Pasform til herrer", "De fleste mænd foretrækker en lige, let afslappet pasform uden markant oversize. Tjek opskriftens færdige overvidde og vælg 8–15 cm mere end brystmålet. Ærmelængde og kroplængde er de to ting, der oftest skal justeres – begge er nemme at rette i en top-down-model."),
   ("Garn, der holder til hverdagsbrug", "Vælg et robust garn: uld/nylon til sokker, kamgarnsspundet merino eller en uld/alpaka-blanding til sweatre. Drops Nepal, Drops Alaska og Merino Extra Fine er gode og billige valg. Undgå meget løst spundne garner, der piller."),
   ("Nemme herreprojekter", "En hue i rib eller perlestrik, et halsrør og en enkel raglansweater i glatstrik. Alle tre findes som gratis DROPS-opskrifter nedenfor."),
  ],
  faq=[
   ("Hvor meget garn skal jeg bruge til en herresweater?", "500–800 g afhængigt af størrelse og garntykkelse. I Drops Merino Extra Fine (105 m/50 g) er det 12–16 nøgler til str. L–XL."),
   ("Findes der gratis strikkeopskrifter til mænd?", "Ja. DROPS har en fast samling herreopskrifter, som alle er gratis. Filtrér på 'Kun gratis'."),
   ("Kan jeg bruge en dameopskrift til en mand?", "Ofte ja, hvis den findes i XL–3XL og er lige i pasformen. Drop hulmønstre og feminine detaljer, og forlæng krop og ærmer."),
  ]),

 dict(slug="begynder", path="opskrifter/begynder", preset=dict(level="begynder"),
  kw="strikkeopskrifter begynder", title="Nemme strikkeopskrifter til begyndere – start her",
  meta="Nemme strikkeopskrifter til begyndere: huer, halsrør, tæpper og simple sweatre uden svære teknikker. Med garnforbrug, garnpris og tips til at komme godt i gang.",
  h1="Nemme strikkeopskrifter til begyndere",
  intro=[
   "Er du ny i strik, er det vigtigste ikke, hvad du strikker, men at det lykkes første gang. Her er strikkeopskrifter til begyndere, som kun bruger ret, vrang, udtagninger og indtagninger – ingen snoninger, ingen hulmønstre, ingen vendepinde. Alle er valgt, fordi de tilgiver små fejl og kan strikkes på en uge eller to.",
   "Vi anbefaler at starte med et garn i mellemtykkelse (pind 4–5), i en lys ensfarvet nuance, så du kan se maskerne. Til hvert projekt viser vi, hvor meget garn du skal bruge og hvor det er billigst – så det første projekt ikke bliver dyrere end nødvendigt.",
  ],
  sections=[
   ("Det skal du købe, før du starter", "Én rundpind 4 mm 80 cm, ét eller to nøgler garn i mellemtykkelse (pind 4–5) i en lys farve, en maskemarkør og en stoppenål. Det er det. Køb ikke et pindesæt – vent, til du ved, at du fortsætter."),
   ("Læs opskriften, før du strikker", "De fleste begynderfejl sker, fordi man læser en linje ad gangen. Læs hele opskriften igennem først, marker hvilken størrelse du strikker (tal i parentes), og tæl masker efter hver udtagning. DROPS har videoer til alle teknikker – linket står i PDF'en."),

   ("Rækkefølgen, der virker", "1) En hue eller et halsrør på rundpind – du lærer at strikke rundt og læse en opskrift. 2) Et tæppe eller tørklæde i retstrik – tålmodighed og jævn strikkefasthed. 3) En raglansweater strikket oppefra og ned i glatstrik – din første 'rigtige' trøje uden sammensyning."),
   ("De tre ting, begyndere oftest gør forkert", "Strikker for stramt (skift til en tykkere pind), springer strikkeprøven over (så passer størrelsen ikke), og vælger mørkt eller fnugget garn (så kan du ikke se, hvad der sker). Alle tre er nemme at undgå."),
   ("Hvilke pinde skal jeg købe?", "En rundpind 4 mm 80 cm og en 5 mm 80 cm dækker 80 % af begynderprojekterne. Køb udskiftelige spidser senere, når du ved, at du fortsætter."),
  ],
  faq=[
   ("Hvad er den nemmeste strikkeopskrift at starte med?", "En hue i rib på rundpind. Den tager 3–4 timer, bruger under 100 g garn og lærer dig at strikke rundt og tage ind."),
   ("Hvor lang tid tager en begyndersweater?", "20–40 timer for en voksenstørrelse i mellemtykt garn. Det er realistisk at nå på to–tre uger med en time om dagen."),
   ("Skal jeg lave en strikkeprøve?", "Ja, altid. 10 minutter nu sparer dig for at trevle en hel sweater op senere. Strik 12 × 12 cm, vask den som det færdige tøj, og mål."),
   ("Hvilket garn er nemmest for begyndere?", "Et glat, ensfarvet uld- eller merinogarn i mellemtykkelse. Drops Nepal, Drops Merino Extra Fine og Drops Alaska er billige og nemme at strikke i."),
  ]),
]

# ---------- hubs ----------
GRATIS = dict(path="gratis", preset=dict(free=True),
  kw="gratis strikkeopskrifter", title="Gratis strikkeopskrifter – hent opskriften, betal kun for garnet",
  meta="Over 900 gratis strikkeopskrifter til dame, børn, baby og herre. Hent PDF'en gratis, se hvor meget garn du skal bruge, og køb garnet hvor det er billigst.",
  h1="Gratis strikkeopskrifter",
  intro=[
   "Her er alle gratis strikkeopskrifter på siden samlet – over 900 modeller, du kan hente som PDF uden at betale. Langt de fleste er fra DROPS Design, der stiller hele deres katalog gratis til rådighed, fordi de tjener på garnet. Det udnytter vi: for hver opskrift viser vi, hvilket garn den er strikket i, hvor mange nøgler du skal bruge til din størrelse, og hvad garnet koster i dag hos de danske butikker, vi sammenligner.",
   "Så 'gratis' betyder ikke gratis at strikke – du skal stadig købe garn. Men det betyder, at hele dit budget går til garnet, og der er ofte 100–200 kr. at spare på en sweater ved at vælge den rigtige butik. Filtrér nedenfor på dame, børn, baby, herre eller type, eller brug søgefeltet til at finde et bestemt garn eller design.",
  ],
  sections=[
   ("Hvorfor er DROPS-opskrifter gratis?", "DROPS/Garnstudio er en norsk garnproducent, der designer opskrifter til sit eget garn og giver dem væk for at sælge garnet. Opskrifterne er oversat til dansk, testet og opdateres løbende. Du henter PDF'en direkte hos DROPS eller hos forhandleren – der er ingen tilmelding eller betaling."),
   ("Andre gratis kilder", "Flere danske garnbutikker giver gratis opskrifter med, når du køber deres garn (fx Permin, Hjertegarn og Filcolana). Designere som PetiteKnit har enkelte gratis opskrifter som smagsprøve. Vi tilføjer dem her, efterhånden som vi får materialelisterne tastet ind."),
   ("Sådan sparer du mest på garnet", "Vælg opskriften først, tjek garnet på opskriftssiden, og sammenlign prisen pr. nøgle mellem butikkerne. Læg mærke til fragtgrænsen: en butik med 2 kr. lavere pris pr. nøgle kan blive dyrere, hvis du ryger under grænsen for fri fragt."),
  ],
  faq=[
   ("Er opskrifterne virkelig gratis?", "Ja. Du henter PDF'en uden at betale eller oprette konto. Du betaler kun for garnet, og det bestemmer du selv, hvor du køber."),
   ("Må jeg sælge det, jeg strikker efter en gratis opskrift?", "DROPS tillader salg af færdige produkter til privat brug i mindre skala, men ikke at du videresælger eller kopierer selve opskriften. Tjek den enkelte designers vilkår."),
   ("Kan jeg bruge et andet garn end DROPS?", "Ja. Ram samme strikkefasthed og regn mængden om i meter. Vi foreslår alternativer på opskriftssiderne."),
   ("Hvorfor viser I en garnpakke?", "Nogle butikker sælger garnet til en bestemt opskrift som færdig pakke i din størrelse. Det er nemt, men ikke altid billigst – derfor viser vi begge dele."),
  ])

DROPS = dict(path="garn/drops", preset=dict(designer="DROPS Design"),
  kw="drops strikkeopskrifter", title="DROPS strikkeopskrifter – alle gratis opskrifter med garnpris",
  meta="Alle DROPS strikkeopskrifter på dansk: gratis opskrifter til dame, herre, børn og baby. Se hvilket DROPS-garn du skal bruge, og sammenlign prisen hos danske butikker.",
  h1="DROPS strikkeopskrifter",
  intro=[
   "DROPS Design er den største kilde til gratis strikkeopskrifter i Danmark – over 900 modeller på dansk, fra sommerbluser i Belle og Muskat til vintersweatre i Nepal og Air. Her er hele samlingen med det, DROPS selv ikke viser: prisen på garnet hos de danske butikker, vi sammenligner, og hvor mange nøgler du skal bruge til din størrelse.",
   "DROPS-garn sælges af næsten alle danske garnbutikker, og priserne svinger mere, end de fleste tror. Baby Merino koster fra 20 til 35 kr. pr. nøgle afhængigt af butik – på en sweater med 10 nøgler er det 150 kr. i forskel. Vælg opskriften, tjek garnet, og køb hvor det er billigst.",
  ],
  sections=[
   ("DROPS-garn: de vigtigste kvaliteter", "Baby Merino (24 m, pind 3) og Merino Extra Fine (21 m, pind 4) er de to alsidige merinogarner. Alpaca (23 m) og Brushed Alpaca Silk bruges til lette, varme modeller. Kid-Silk er mohair/silke til at holde sammen med et andet garn. Nepal og Air er mellemtykke og hurtige at strikke. Snow/Eskimo og Alaska er de tykke vintergarner. Vi har garnsider med priser og alternativer til hver af dem."),
   ("Sådan læser du en DROPS-opskrift", "DROPS angiver garnmængde i gram pr. størrelse og strikkefasthed for hvert garn. Bemærk 'Garngruppe' (A–F): to garner i samme gruppe kan erstatte hinanden, hvis du rammer fastheden. Opskrifterne har videoer til de fleste teknikker – link står i PDF'en."),
   ("Populære DROPS-modeller i Danmark", "Sommerbluser i Belle og Safran, raglansweatre i Air og Nepal, og sokker i Fabel er de mest strikkede herhjemme. Kig under 'Sweatre & bluser' nedenfor, eller sortér efter billigste garnpakke."),
  ],
  faq=[
   ("Er alle DROPS strikkeopskrifter gratis?", "Ja. Hele DROPS' katalog kan hentes gratis som PDF på dansk."),
   ("Hvor køber jeg DROPS-garn billigst?", "Det skifter fra uge til uge. Vi henter priser fra danske butikker hver nat og viser den billigste pr. garn. Se garnsiderne under 'Garn'."),
   ("Kan jeg strikke en DROPS-opskrift i et andet garn?", "Ja, hvis du rammer samme strikkefasthed (masker pr. 10 cm). Regn mængden om i meter – ikke gram – da løbelængden varierer."),
   ("Hvad betyder DROPS' garngrupper?", "A er tyndest (lace/fingering), F er tykkest. Garner i samme gruppe har cirka samme fasthed og kan ofte byttes."),
  ])

# ---------- guides ----------
GUIDES = [
 dict(slug="vaelg-alternativt-garn", title="Sådan vælger du et alternativt garn til en strikkeopskrift",
  meta="Guide: sådan erstatter du garnet i en strikkeopskrift med et billigere eller blødere alternativ – strikkefasthed, løbelængde, fiber og omregning af mængde.",
  h1="Sådan vælger du et alternativt garn",
  body=[
   ("Hvorfor skifte garn?", "Fordi det anbefalede garn er udsolgt, for dyrt, klør, eller bare ikke findes i den farve, du vil have. Det er helt normalt – og det går fint, hvis du tjekker tre ting."),
   ("1. Strikkefasthed er det vigtigste", "Opskriften angiver fx 22 masker × 30 pinde = 10 × 10 cm. Dit alternativ skal kunne strikkes til samme fasthed på nogenlunde samme pind. Kig på banderolen: står der 21–23 masker på pind 3,5–4, er du tæt på. Står der 26 masker, er garnet for tyndt – medmindre du holder to tråde sammen."),
   ("2. Regn mængden om i meter, ikke gram", "50 g merino er ikke 50 g alpaka. Gang antal nøgler i opskriften med løbelængden pr. nøgle for det oprindelige garn – det giver det samlede antal meter. Divider med løbelængden på dit alternativ, og rund op. Eksempel: 9 nøgler à 180 m = 1.620 m. I et garn med 175 m/50 g skal du bruge 1.620 / 175 = 9,3 → 10 nøgler."),
   ("3. Fiberen bestemmer faldet", "Merino er elastisk og glat. Alpaka er tungere og falder mere. Bomuld har ingen elasticitet og bliver længere med tiden. Mohair/silke giver luft og glød. Et hulmønster i merino ser anderledes ud i bomuld – ikke nødvendigvis dårligere, men anderledes. Strik en prøve, vask den, og se."),
   ("Typiske erstatninger", "Önling No 1 (180 m/50 g, 21 m) → Drops Baby Merino holdt lidt løst, Sandnes Sunday eller Knitting for Olive Merino (dobbelt). Sandnes Double Sunday (108 m/50 g) → Drops Merino Extra Fine. Isager Silk Mohair / KFO Soft Silk Mohair → Drops Kid-Silk. Vi viser konkrete alternativer med pris på hver opskriftsside."),
   ("Den ene ting, du ikke må springe over", "Strikkeprøven. Strik 12 × 12 cm i mønsteret, vask den som det færdige tøj, lad den tørre fladt, og mål de midterste 10 cm. Passer det ikke, skift pind – ikke garn."),
  ],
  faq=[
   ("Kan jeg altid erstatte et garn?", "Næsten. Undtagelsen er specialgarner med effekt (tweed, farveskift, bouclé), hvor udtrykket er hele pointen."),
   ("Hvad gør jeg, hvis løbelængden er meget forskellig?", "Regn i meter og rund op til nærmeste hele nøgle. Køb gerne et nøgle ekstra – de fleste butikker tager uåbnede nøgler retur."),
  ]),
 dict(slug="alternativer-onling-no-1", title="Alternativer til Önling No 1 – 5 garner i samme strikkefasthed",
  meta="Billigere alternativer til Önling No 1 (merino/angora, 180 m/50 g, 21 m): Drops Baby Merino, Drops Alpaca, Sandnes Sunday, Knitting for Olive Merino og Drops Lima – med pris og forskelle.",
  h1="Alternativer til Önling No 1",
  body=[
   ("Hvad er Önling No 1?", "Önling No 1 er 75 % merino og 25 % angora, 50 g / 180 m, strikkefasthed 21 masker på pind 3,5–4. Det er garnet bag Rikke Cozy Sweater og de fleste af Önlings egne modeller – blødt, let, med en svag angora-glød. Prisen er omkring 139 kr. pr. nøgle, så en sweater lander på 1.100–1.400 kr."),
   ("1. Drops Baby Merino (fra ca. 23 kr.)", "100 % merino, 175 m/50 g. Lidt tyndere (24 m på pind 3), så strik løsere på pind 4 eller hold den sammen med en tynd mohairtråd for at ramme 21 masker. Ingen angora-fnug, kan maskinvaskes. Sparer 800–1.000 kr. på en sweater."),
   ("2. Drops Alpaca (fra ca. 24 kr.)", "100 % alpaka, 167 m/50 g, 23 m. Tættest på No 1 i fald og varme – alpaka giver samme bløde glød som angora. Lidt tungere. Strik en prøve på pind 4."),
   ("3. Drops Lima (fra ca. 25 kr.)", "65 % uld, 35 % alpaka, 100 m/50 g, 21 m på pind 4. Rammer strikkefastheden præcist, men er tykkere og mere rustik. God til de tættere modeller."),
   ("4. Sandnes Sunday (ca. 60 kr.)", "100 % merino, 235 m/50 g, 27 m. Skal holdes dobbelt eller sammen med mohair for at ramme No 1. Blødere end Drops, dyrere – men stadig halv pris af No 1."),
   ("5. Knitting for Olive Merino + Soft Silk Mohair (ca. 65 + 75 kr.)", "Det 'danske' alternativ: KFO Merino (250 m/50 g) holdt sammen med Soft Silk Mohair giver 21 m på pind 4 og et look, der ligger tæt på No 1. Dyrere end Drops, men billigere end Önling."),
   ("Sådan regner du om", "Önling No 1: 9 nøgler à 180 m = 1.620 m til en sweater i M. Baby Merino (175 m): 1.620 / 175 = 9,3 → 10 nøgler. Alpaca (167 m): 10 nøgler. Lima (100 m): 17 nøgler. Regn i meter, aldrig i gram."),
  ],
  faq=[
   ("Mister jeg noget ved at skifte fra No 1?", "Angora-gløden og den helt lette vægt. Alpaka kommer tættest på. Merino er glattere og mere 'ren' i udtrykket."),
   ("Kan jeg bruge alternativet til alle Önling-opskrifter?", "Til dem, der er strikket i No 1, ja. Önling No 3 og No 4 + mohair har andre fastheder – tjek opskriftens angivelse."),
  ]),
 dict(slug="hvor-mange-noegler", title="Hvor mange nøgler garn skal jeg bruge? Sådan regner du det ud",
  meta="Guide: sådan beregner du garnforbrug til sweater, cardigan, hue og sokker – i gram og meter – og hvorfor du altid skal købe ét nøgle ekstra.",
  h1="Hvor mange nøgler garn skal jeg bruge?",
  body=[
   ("Kort svar", "Det står i opskriften pr. størrelse. Men opskriften er skrevet til ét bestemt garn – bruger du et andet, skal du regne om. Og har du ingen opskrift, kan du bruge tommelfingerreglerne nedenfor."),
   ("Tommelfingerregler i meter (voksen str. M)", "Sweater i tyndt garn (26–28 m): 1.500–1.800 m. Sweater i mellemtykt garn (20–22 m): 1.000–1.300 m. Sweater i tykt garn (14–16 m): 700–900 m. Cardigan: læg 10–15 % til. Hue: 100–150 m. Halsrør: 150–250 m. Sokker: 350–450 m. Til herre XL: læg 25–30 % til. Til børn 6 år: cirka 40 % af voksen M."),
   ("Fra meter til nøgler", "Del det samlede antal meter med løbelængden pr. nøgle (står på banderolen, fx 175 m/50 g), og rund op. 1.200 m / 175 m = 6,9 → 7 nøgler."),
   ("Hvorfor gram ikke er nok", "50 g alpaka indeholder færre meter end 50 g merino, fordi fiberen er tungere. To garner med samme vægt kan have 100 m forskel pr. nøgle. Regn derfor altid i meter, når du skifter garn."),
   ("Køb ét nøgle ekstra – altid", "Farvepartier (dye lots) varierer, og du kan ikke altid få det samme parti igen. Et ekstra nøgle koster 20–70 kr.; en sweater, der mangler de sidste 30 gram, koster dig et nyt projekt. Uåbnede nøgler kan ofte returneres."),
   ("Mønster æder garn", "Snoninger bruger 15–25 % mere end glatstrik. Fair isle med flere farver bruger 20–30 % mere samlet, fordi trådene løber bagpå. Rib og perlestrik ligger tæt på glatstrik."),
  ],
  faq=[
   ("Hvor mange nøgler til en sweater?", "6–10 nøgler à 50 g i mellemtykt garn til en voksen M. 10–14 i tyndt garn. Tjek opskriften – vores beregner regner det ud pr. størrelse."),
   ("Hvor mange nøgler til en hue?", "Ét nøgle à 50 g i de fleste garner. Til tykke huer eller huer med fold: to."),
   ("Hvad gør jeg, hvis jeg løber tør?", "Tjek butikken for samme dye lot først. Ellers: strik rib, kanter eller ærmer i det nye parti, så overgangen ikke ses midt på kroppen."),
  ]),
]

# ---------- forside ----------
HOME_FAQ = [
 ("Hvad er strikkeopskrifter.dk?", "En samling af danske og nordiske strikkeopskrifter, hvor hver opskrift viser garnforbrug pr. størrelse og dagens garnpris hos danske butikker. Målet er, at du kan vælge opskrift, regne garnet ud og købe det billigst – på ét sted."),
 ("Koster det noget at bruge siden?", "Nej. Vi får en lille provision fra butikken, hvis du køber garn via vores links. Det ændrer ikke din pris, og det påvirker ikke, hvilken butik vi viser som billigst."),
 ("Hvor kommer priserne fra?", "Fra butikkernes egne produktfeeds, som vi henter hver nat. Ser du en pris, der ikke passer, så skriv til os – så retter vi det."),
 ("Er opskrifterne jeres egne?", "Nej. Opskrifterne tilhører designerne og butikkerne, og vi linker til dem. Vores eget bidrag er garndata, beregneren, prissammenligningen og guides."),
]

# ---------- typesider (/opskrifter/<type>/) ----------
TYPES = [
 dict(slug="sweater", type="sweater", kw="strikkeopskrifter sweater", h1="Strikkeopskrifter til sweatre og bluser",
  title="Strikkeopskrifter sweater – raglan, rundt bærestykke og oversize",
  meta="Strikkeopskrifter til sweatre og bluser: raglan oppefra og ned, rundt bærestykke, hulmønster og oversize. Gratis og betalte, med garnforbrug og garnpris.",
  intro=["Sweateren er det projekt, de fleste strikker mest – og det, hvor garnvalget betyder mest for prisen. Her er alle sweater- og bluseopskrifter på siden: raglan strikket oppefra og ned, rundt bærestykke med mønster, lette sommerbluser i bomuld og hør, og tykke vintersweatre i uld og alpaka.",
         "Til hver opskrift viser vi garnet, ca. antal nøgler og dagens pris hos de butikker, vi sammenligner. Filtrér på gratis, hvem den er til, eller sortér efter billigste garn."],
  sections=[
   ("Top-down eller bottom-up?", "Strikket oppefra og ned kan du prøve sweateren undervejs og justere længden – det er derfor, næsten alle nye danske opskrifter er top-down. Bottom-up giver mere kontrol over mønstre i bærestykket og var normen indtil for ti år siden."),
   ("Vask og opspænding", "Merino og uld skal vaskes i hånden eller på uldprogram, presses i et håndklæde og tørres fladt i form. Første vask afgør, om sweateren passer – strik prøven, vask den, og mål først derefter."),
("Raglan eller rundt bærestykke?","Raglan er hurtigst og nemmest at tilpasse undervejs; rundt bærestykke giver plads til mønster og fair isle. Begge strikkes typisk oppefra og ned uden sammensyning, så du kan prøve sweateren, mens du strikker."),
            ("Garnforbrug til en sweater","300–450 g i tyndt garn (pind 3), 400–600 g i mellemtykt (pind 4–5) og 500–800 g i tykt garn (pind 7–8) til en voksen M. Skal den være oversize, læg 15–20 % til.")],
  faq=[("Hvad er den nemmeste sweateropskrift?","En raglan i glatstrik strikket oppefra og ned i mellemtykt garn. Ingen sammensyning, ingen mønster – og du kan prøve den undervejs."),
       ("Hvor lang tid tager en sweater?","20–40 timer i mellemtykt garn, 40–60 i tyndt. En tyk sweater på pind 8 kan strikkes på en weekend."),
       ("Hvilket garn holder bedst til en sweater?","Kamgarnsspundet merino eller en uld/alpaka-blanding. Undgå meget løst spundet garn til ærmer og albuer.")]),
 dict(slug="cardigan", type="cardigan", kw="strikkeopskrifter cardigan", h1="Strikkeopskrifter til cardigans",
  title="Strikkeopskrifter cardigan – med knapper, lynlås eller åben front",
  meta="Strikkeopskrifter til cardigans og jakker til dame, herre og børn. Se garnforbrug, knapkant-teknik og dagens garnpris hos danske butikker.",
  intro=["En cardigan er sweaterens praktiske søster: den kan tages på over alt, og den passer altid. Her er cardigan- og jakkeopskrifter fra korte, kropsnære modeller til lange, oversize kofter – med og uden knapper.",
         "Cardigans bruger 10–15 % mere garn end en sweater på grund af knapkanterne, så prisen pr. nøgle betyder ekstra meget. Vi viser billigste butik for hvert garn."],
  sections=[
   ("Knapper: køb dem sidst", "Vent med knapper til knapkanten er strikket, så du kan måle afstanden. Keramik og træ passer til uld; perlemor til bomuld. Vi linker til knapper hos butikkerne, hvor de findes."),
   ("Cardigan til børn", "Børnecardigans bruger 150–300 g og strikkes ofte med knapper hele vejen, så de er nemme at få på. Se børnesiden for opskrifter i alderen 2–14."),
("Knapkanter uden bøvl","Strik knapkanterne sammen med kroppen (i-cord eller rib) i stedet for at samle op bagefter – det giver et pænere resultat og sparer en time. Knaphuller placeres jævnt, første og sidste 1–2 cm fra kanten."),
            ("Stål eller steek?","Nordiske cardigans strikkes ofte rundt som en sweater og klippes op (steek). Det lyder farligt, men er nemt i uld, der filter let. I superwash og bomuld skal du sy to gange før du klipper.")],
  faq=[("Hvor mange knapper skal jeg bruge?","6–8 på en voksencardigan, 4–5 på en børne. Køb dem, når du har strikket knapkanten, så du kan måle afstanden."),
       ("Kan jeg lave en sweateropskrift om til cardigan?","Ja – strik kroppen frem og tilbage i stedet for rundt, og læg 8–12 masker til knapkanter. Læg 10–15 % garn til.")]),
 dict(slug="hue", type="hue", kw="strikkeopskrifter hue", h1="Strikkeopskrifter til huer",
  title="Strikkeopskrifter hue – rib, perlestrik, fold og pompon",
  meta="Strikkeopskrifter til huer til voksne, børn og baby. Nemme opskrifter i rib og perlestrik, med garnforbrug (typisk ét nøgle) og garnpris.",
  intro=["En hue er det perfekte projekt til en aften: ét nøgle garn, et par timer, og du har noget færdigt. Her er hueopskrifter til voksne, børn og baby – klassisk rib med fold, perlestrik, slouchy modeller og huer med pompon.",
         "De fleste bruger under 100 g, så det er også det oplagte sted at prøve et dyrere garn eller bruge et restenøgle. Vi viser prisen pr. nøgle, så du kan se, om huen koster 25 eller 90 kr."],
  sections=[
   ("Restegarnsprojekt nummer ét", "En hue bruger 40–90 g. Har du et nøgle tilovers fra en sweater, har du en hue. Kig efter huer i samme garn som din sidste sweater – så matcher de."),
   ("Huer til hele familien", "De fleste hueopskrifter findes i 3–4 størrelser fra baby til voksen. Strik dem alle i samme garn og forskellige farver – det er den nemmeste julegave."),
("Størrelse: mål hovedet","Voksen: 54–58 cm hovedomkreds → strik 50–52 cm i omkreds (huen skal sidde stramt). Barn 2–6 år: 48–52 cm. Baby: 38–44 cm. Strik den 2–4 cm mindre end hovedet, ribben giver."),
            ("Garn til huer","Uld eller uld/alpaka holder varmen og formen. Ren alpaka bliver slap. Til baby: superwash-merino, der tåler vask.")],
  faq=[("Hvor meget garn skal jeg bruge til en hue?","50 g i de fleste garner – ét nøgle. Til en hue med fold eller i tykt garn: to."),
       ("Hvilken pind til en hue?","Rundpind 40 cm i den størrelse garnet anbefaler, plus strømpepinde eller magic loop til toppen.")]),
 dict(slug="sjal", type="sjal", kw="strikkeopskrifter sjal", h1="Strikkeopskrifter til sjaler og tørklæder",
  title="Strikkeopskrifter sjal og tørklæde – hulmønster, retstrik og halsrør",
  meta="Strikkeopskrifter til sjaler, tørklæder og halsrør. Fra nemme retstrik-tørklæder til trekantsjaler i hulmønster – med garnforbrug og pris.",
  intro=["Sjaler og tørklæder har ingen størrelser at ramme, ingen ærmer at sy i, og de bruger lidt garn i forhold til, hvor meget strik du får. Her er opskrifter på trekantsjaler, halvmånesjaler, klassiske tørklæder og halsrør – i alt fra tyndt mohair til tykt uld.",
         "Sjaler strikkes ofte i tyndt garn med stor løbelængde, så to-tre nøgler rækker langt. Vi viser garnet og prisen ved hver opskrift."],
  sections=[
   ("Hvor stort skal et sjal være?", "Et trekantsjal til at slå om halsen: 150–180 cm i spændvidde. Et sjal til at have over skuldrene: 200+ cm. Et tørklæde: 20–30 cm bredt og 150–200 cm langt. Garnforbruget følger med – tjek beregneren."),
   ("Sjaler i mohair", "Kid-Silk og Önling No 10 holdt dobbelt giver et sjal, der vejer under 100 g og varmer som uld. Det er det bedste sted at prøve mohair første gang."),
("Fasthed betyder mindre her","I et sjal er strikkefastheden ikke afgørende – bliver det lidt større, er det bare et større sjal. Det gør sjaler til det bedste sted at afprøve et nyt garn."),
            ("Opspænding gør forskellen","Et sjal i hulmønster ser klemt ud, indtil det er vasket og spændt ud. Brug opspændingstråd eller nåle, lad det tørre fladt – og mønsteret åbner sig.")],
  faq=[("Hvor meget garn til et sjal?","300–600 m til et mellemstort trekantsjal, 200–350 m til et tørklæde, 150–250 m til et halsrør."),
       ("Hvilket garn er bedst til sjaler?","Mohair/silke eller tynd merino til lette sjaler; uld/alpaka til varme tørklæder.")]),
 dict(slug="sokker", type="sokker", kw="strikkeopskrifter sokker", h1="Strikkeopskrifter til sokker og strømper",
  title="Strikkeopskrifter sokker – hælle, tåer og strømpegarn der holder",
  meta="Strikkeopskrifter til sokker og strømper til voksne og børn. Se hvilket strømpegarn der holder, hvor meget du skal bruge, og hvor det er billigst.",
  intro=["Strikkede sokker er den gave, alle bliver glade for – og det projekt, der lærer dig mest på kortest tid: rundstrik, hæl, indtagninger til tå. Her er sokkeopskrifter fra enkle raggsokker til mønstrede knæstrømper.",
         "Det vigtigste valg er garnet: det skal indeholde nylon (typisk 25 %), ellers holder hælen ikke. Vi markerer strømpegarn på siden og viser prisen pr. nøgle."],
  sections=[
   ("Strømpegarn: hvad skal du kigge efter?", "75 % uld / 25 % nylon, 100 g / ca. 400 m, pind 2,5–3. Drops Fabel og Önling No 18 er standarden. Uden nylon slides hælen igennem på en sæson."),
   ("Sokker til begyndere", "Start med en hælflap-hæl – den er nemmest at forstå – og strik på magic loop, så du slipper for strømpepinde. DROPS har video til hver del."),
("Hæl-typer","Hælflap er klassisk og slidstærk. Kort-række-hæl (short row) er hurtigere og passer bedre til smalle fødder. Begge findes i DROPS' opskrifter med video."),
            ("Størrelse","Sokker strikkes 1–2 cm kortere end foden – de strækker sig. Mål fodlængde og gang med 0,9.")],
  faq=[("Hvor meget garn skal jeg bruge til et par sokker?","Et nøgle à 100 g (ca. 400 m) rækker til et par voksensokker. Til knæstrømper: to."),
       ("Kan jeg vaske uldsokker i maskinen?","Ja, hvis garnet er superwash med nylon – uldprogram, 30 grader, ingen tørretumbler.")]),
 dict(slug="vest", type="vest", kw="strikkeopskrifter vest", h1="Strikkeopskrifter til veste og slipovers",
  title="Strikkeopskrifter vest – slipover, V-hals og mønstrede veste",
  meta="Strikkeopskrifter til veste og slipovers til dame og herre. Hurtige projekter med lavt garnforbrug – se garn, nøgler og pris.",
  intro=["Vesten er kommet tilbage: slipoveren i rib eller mønster over en skjorte er blevet et fast indslag i garderoben. Den er også et taknemmeligt projekt – ingen ærmer, 4–6 nøgler, og færdig på en uge.",
         "Her er veste- og slipoveropskrifter til dame, herre og børn, med garn og pris. Netop fordi garnforbruget er lavt, er en vest et godt sted at vælge et lidt dyrere garn."],
  sections=[
   ("Vesten som lag", "En vest i tyndt garn (pind 3) fungerer over skjorte; en tyk vest (pind 6–8) som ydre lag. Vælg efter, hvornår du vil bruge den."),
   ("Ribvest eller mønstervest?", "Ribvesten er hurtig og sidder tæt. Mønsterveste (fair isle, snoninger) tager længere, men bruger stadig kun 4–6 nøgler – så det er stedet at prøve en dyrere kvalitet."),
("V-hals eller rund hals?","V-hals er den klassiske slipover og kræver lidt mere teknik i halskanten. Rund hals er nemmere og passer bedre til børn."),
            ("Pasform","Veste strikkes ofte tættere end sweatre – 0–10 cm ease. Tjek opskriftens færdige mål.")],
  faq=[("Hvor meget garn til en vest?","200–350 g til en voksen M i mellemtykt garn – omtrent halvdelen af en sweater."),
       ("Er en vest et begynderprojekt?","Ja, hvis den er i glatstrik eller rib. Mønstrede veste kræver lidt erfaring.")]),
]

TYPES += [
 dict(slug="karklude", type="karklud", kw="strikkeopskrifter karklude", h1="Strikkeopskrifter til karklude",
  title="Strikkede karklude – gratis opskrifter, garn og mønstre",
  meta="Gratis strikkeopskrifter til karklude og grydelapper i bomuld. Se hvilket garn der holder til opvask, hvor meget du skal bruge (ét nøgle), og hvor bomuldsgarnet er billigst.",
  intro=["Karkluden er Danmarks mest strikkede genstand. Den bruger ét nøgle bomuld, tager en time, og den er det første, de fleste strikker – og det, mange bliver ved med, fordi den kan strikkes uden at tænke. Her er opskrifter på karklude i retstrik, perlestrik, med hulmønster og med relief, plus grydelapper og vaskeklude.",
         "Garnet er 8/4-bomuld eller tilsvarende (Drops Paris, Safran, Muskat). Det tåler kogevask og bliver blødere med tiden. Vi viser prisen pr. nøgle hos butikkerne – på karklude er det den eneste udgift."],
  sections=[("Hvilket garn til karklude?","100 % bomuld i mellemtykkelse (8/4 eller 8/8). Drops Paris (50 g/75 m, pind 5) giver en tyk, solid klud; Safran (50 g/160 m, pind 3) en tyndere og finere. Undgå bomuld/akryl-blandinger – de suger dårligt."),
            ("Størrelse og mønster","20–25 cm i firkant er standard. Retstrik er hurtigst; perlestrik giver bedre skurevirkning; hulmønster tørrer hurtigst. Strik en kant på 3–4 masker i retstrik, så kluden ikke ruller.")],
  faq=[("Hvor meget garn skal jeg bruge til en karklud?","Et nøgle à 50 g rækker til 1–2 klude afhængigt af tykkelse."),("Kan strikkede karklude vaskes ved 60 grader?","Ja, ren bomuld tåler 60–90 grader. De krymper lidt første gang – strik dem 2 cm større.")]),
 dict(slug="taepper", type="taeppe", kw="strikkeopskrifter tæppe", h1="Strikkeopskrifter til tæpper og plaider",
  title="Strikkede tæpper – opskrifter til babytæpper, plaider og patchwork",
  meta="Strikkeopskrifter til tæpper: babytæpper, sofaplaider og patchworktæpper. Se garnforbrug (typisk 300–1.400 g), garnpriser og nemme mønstre.",
  intro=["Et strikket tæppe er det projekt, hvor garnprisen betyder mest – et sofatæppe bruger 1.000–1.400 g, et babytæppe 250–400 g. Til gengæld kræver det ingen teknik: retstrik, perlestrik eller simple firkanter, der sys sammen. Her er tæppeopskrifter fra små babytæpper til store plaider, med garn og pris.",
         "Vælg garn efter brug: superwash-merino eller bomuld til baby (kan vaskes), uld eller uld/alpaka til sofaen (varmt, holder formen), og tykt garn på pind 8 hvis det skal gå hurtigt."],
  sections=[("Hvor meget garn til et tæppe?","Babytæppe 70 × 90 cm: 300–400 g i mellemtykt garn. Plaid 120 × 150 cm: 900–1.400 g. Regn i meter: et babytæppe kræver ca. 800–1.000 m, en plaid 2.500–3.500 m."),
            ("Patchwork eller ét stykke?","Firkanter er nemme at have med i tasken og gode til restegarn, men skal sys sammen. Ét stykke på lang rundpind er hurtigere og giver et jævnere resultat.")],
  faq=[("Hvad er det nemmeste tæppe at strikke?","Et retstrikket tæppe på rundpind 8 i tykt garn – ingen mønster, ingen syning."),("Kan jeg strikke et tæppe af restegarn?","Ja, i firkanter eller striber. Hold dig til samme tykkelse, så tæppet ikke trækker skævt.")]),
 dict(slug="hjemmesko", type="hjemmesko", kw="strikkeopskrifter hjemmesko", h1="Strikkeopskrifter til hjemmesko og sutsko",
  title="Strikkede hjemmesko og sutsko – opskrifter, filtning og garn",
  meta="Strikkeopskrifter til hjemmesko, sutsko og futter til voksne og børn. Filtede eller ufiltede, med garnforbrug og pris på garnet.",
  intro=["Hjemmesko er et weekendprojekt: tykt garn, store pinde, og ofte en tur i vaskemaskinen til sidst, så de filter og bliver tætte. Her er opskrifter på filtede tøfler, strikkede sutsko med såler, og futter til baby og børn.",
         "Skal de filtes, skal garnet være ren uld *uden* superwash – ellers filter det ikke. Drops Snow/Eskimo og Alaska er de klassiske valg. Til ufiltede sutsko passer strømpegarn eller uld/nylon, der tåler slid."],
  sections=[("Filtning i maskinen","Strik dem 30–40 % for store, vask ved 40–60 grader med lidt vaskemiddel og et par håndklæder til at give gnidning. Form dem, mens de er våde, og lad dem tørre på fødderne eller i en form."),
            ("Skridsikre såler","Sy læder- eller gummisåler under, eller påfør latex-skridsikring. Det gør hjemmeskoene sikre på trægulve og forlænger levetiden.")],
  faq=[("Hvor meget garn til et par hjemmesko?","100–150 g tykt garn til voksne, 50–100 g til børn."),("Hvorfor filter mine hjemmesko ikke?","Garnet er superwash-behandlet eller indeholder for meget andet end uld. Brug ren, ubehandlet uld.")]),
 dict(slug="bamser-og-legetoj", type="legetoj", kw="strikkeopskrifter bamser", h1="Strikkeopskrifter til bamser og legetøj",
  title="Strikkede bamser, dyr og dukketøj – opskrifter og garn",
  meta="Strikkeopskrifter til bamser, kaniner, dukker og dukketøj. Små projekter i restegarn med garnforbrug og pris.",
  intro=["Strikket legetøj er små projekter med stor glæde: en kanin, en bjørn, en dukke eller tøj til Baby Born. De bruger 20–100 g garn, strikkes på små pinde, og er perfekte til rester. Her er opskrifter på bamser, dyr og dukketøj til baby og børn.",
         "Vælg et glat, tætstrikket garn (merino eller bomuld) og strik på en pind mindre end anbefalet, så fyldet ikke kan ses gennem maskerne."],
  sections=[("Sikkerhed","Broderede øjne frem for sikkerhedsøjne til de mindste. Fyld med polyesterfyld, der kan vaskes, og sy alle dele fast to gange."),
            ("Dukketøj","Opskrifter til Baby Born (43 cm) og andre dukker på 30–45 cm bruger 20–50 g og er hurtigt strikket – en god første opskrift til børn, der vil lære at strikke.")],
  faq=[("Hvor meget garn til en bamse?","50–100 g afhængigt af størrelse. Rester fra andre projekter rækker ofte."),("Kan strikket legetøj vaskes?","Ja, hvis både garn og fyld er vaskbart. Vask i vaskepose ved 30–40 grader.")]),
 dict(slug="julestrik", type="jul", kw="julestrik opskrifter", h1="Julestrik – opskrifter til nissehuer, julesokker og julepynt",
  title="Julestrik – strikkeopskrifter til nissehuer, julesokker, kalendersokker og pynt",
  meta="Strikkeopskrifter til jul: nissehuer, julesokker, kalendersokker, julekugler og pynt. Med garnforbrug og pris – start i oktober, så er det klar til december.",
  intro=["Julestrik er sæsonens hyggeligste projekter: nissehuer til hele familien, julesokker til pejsen, kalendersokker med 24 lommer, julekugler og småpynt til træet. De fleste er små og hurtige – og de er gaver i sig selv.",
         "Rød, hvid og grøn uld er standard, men de bedste julestrik-projekter bruger det, du har. Start i oktober: en nissehue tager en aften, en kalendersok 8–10 timer."],
  sections=[("Hvad skal du strikke først?","Nissehuer er nemmest og bruges mest. Julekugler bruger 10–20 g og er gode til rester. Kalendersokker er det store projekt – begynd tidligt."),
            ("Garn til julestrik","Uld eller uld/akryl i mellemtykkelse til huer og sokker, bomuld til pynt, der skal holde formen. Til julekugler: tyndt garn og et lille styropor- eller vatkugle-indlæg.")],
  faq=[("Hvornår skal jeg starte på julestrik?","Oktober, hvis det er gaver. Nissehuer kan nås i december."),("Hvor meget garn til en nissehue?","Ét nøgle à 50 g til voksne, mindre til børn.")]),
 dict(slug="halsedisser", type="halsedisse", kw="strikkeopskrifter halsedisse", h1="Strikkeopskrifter til halsedisser og halsrør",
  title="Strikkede halsedisser og halsrør – opskrifter til voksne og børn",
  meta="Strikkeopskrifter til halsedisser, halsrør og cowls. 1–3 nøgler garn, færdig på en aften – med garnforbrug og pris på garnet.",
  intro=["Halsedissen er tørklædets praktiske søster: ingen løse ender, sidder tæt, og børn kan selv tage den på. Den bruger 1–3 nøgler og strikkes rundt uden sammensyning. Her er opskrifter til halsedisser og halsrør til voksne, børn og baby – i rib, perlestrik, snoninger og mohair.",
         "Vælg et blødt garn, der ikke kradser mod halsen: merino, alpaka eller mohair/silke. Vi viser prisen pr. nøgle, så du kan se, om projektet koster 30 eller 150 kr."],
  sections=[("Størrelse","Voksen: 55–65 cm i omkreds, 20–30 cm høj. Barn: 40–50 cm. Strik den i rib, så den giver – ellers skal den kunne gå over hovedet."),
            ("Dobbelt eller enkelt?","En dobbeltstrikket halsedisse (strikket som et rør og foldet) er varmere og pænere på begge sider, men bruger dobbelt garn.")],
  faq=[("Hvor meget garn til en halsedisse?","1–2 nøgler à 50 g til voksne, ét til børn."),("Hvilken pind?","Rundpind 40 cm i den størrelse, garnet anbefaler.")]),
 dict(slug="vanter", type="vanter", kw="strikkeopskrifter vanter", h1="Strikkeopskrifter til vanter og luffer",
  title="Strikkede vanter og luffer – opskrifter til voksne, børn og baby",
  meta="Strikkeopskrifter til vanter, luffer og fingervanter. Færdige på en aften, under 100 g garn – med garnforbrug og pris.",
  intro=["Vanter er det lille projekt med den største nytte: under 100 g garn, en aften eller to, og du har noget, der bruges hver dag fra november til marts. Her er opskrifter til luffer, fingervanter og babyvanter uden tommel.",
         "Uld eller uld/alpaka holder varmen; strømpegarn med nylon holder længst. Strik dem på en pind mindre end sweateren i samme garn – tætte masker giver varme vanter."],
  sections=[("Tommelfingeren","Den 'afrikanske' tommel (strikket på hjælpetråd) er nemmest for begyndere. Kilen (udtagninger i siden) sidder bedre. Begge findes i DROPS' opskrifter med video."),
            ("Størrelse","Mål håndens omkreds uden tommel, og strik 1–2 cm mindre – uld giver sig.")],
  faq=[("Hvor meget garn til et par vanter?","50–80 g til voksne, 30–50 g til børn."),("Kan jeg strikke vanter på rundpind?","Ja, med magic loop eller to rundpinde. Strømpepinde er det klassiske.")]),
]

# ---------- pindesider (/opskrifter/pind-<n>/) ----------
NEEDLES = [
 dict(n="3", kw="gratis strikkeopskrifter pind 3", h1="Strikkeopskrifter til pind 3", title="Strikkeopskrifter pind 3 – tynde garner, fint maskebillede",
  meta="Strikkeopskrifter til pind 3 (2,5–3,5 mm): sweatre, bluser og babytøj i tyndt garn som Baby Merino, Safran og Flora. Gratis opskrifter med garnpris.",
  intro=["Pind 3 giver et fint, tæt maskebillede og er standard til babytøj, sommerbluser og klassiske sweatre i tyndt garn. Det tager længere tid end tykkere pinde, men resultatet holder formen og ser 'købt' ud.",
         "Her er opskrifter, hvor garnet strikkes på pind 2,5–3,5 – typisk Drops Baby Merino, Safran, Flora, Fabel og Alpaca. Vi viser garnet og prisen ved hver."],
  sections=[
   ("Hvorfor pind 3 er umagen værd", "Tættere masker betyder, at sweateren holder formen efter vask og ikke bliver posset ved albuerne. Det er også den tykkelse, de fleste betalte danske opskrifter er skrevet til."),
   ("Tidsforbrug", "Regn med 25–35 % flere timer end på pind 4 til samme model. Til gengæld bruger du 20–30 % færre gram."),
  ],
  faq=[("Hvilke garner passer til pind 3?","Garner med 24–28 masker pr. 10 cm: Baby Merino, Safran, Flora, Alpaca, Fabel (sokker), Sandnes Sunday, KFO Merino."),("Tager det lang tid?","Ja – regn med 40–60 timer til en voksensweater. Til gengæld bruger du færre gram.")]),
 dict(n="4", kw="strikkeopskrifter pind 4", h1="Strikkeopskrifter til pind 4", title="Strikkeopskrifter pind 4 – den alsidige mellemtykkelse",
  meta="Strikkeopskrifter til pind 4 (3,5–4,5 mm): sweatre, cardigans og huer i mellemtykt garn som Merino Extra Fine, Karisma, Lima og Belle. Med garnpris.",
  intro=["Pind 4 er den mest brugte pindestørrelse i danske opskrifter – hurtig nok til at komme videre, fin nok til pænt strik. Det er også her, udvalget af garn er størst.",
         "Her er alle opskrifter på pind 3,5–4,5: Merino Extra Fine, Karisma, Lima, Belle, Muskat, Cotton Merino og Puna er de typiske garner. Sammenlign prisen pr. nøgle, før du vælger."],
  sections=[
   ("Det største garnudvalg", "Pind 4 er der, hvor næsten alle producenter har en kvalitet: Merino Extra Fine, Karisma, Lima, Belle, Önling No 1 og No 3. Det gør det nemt at finde et alternativ, hvis originalgarnet er udsolgt eller for dyrt."),
   ("Begynderens pind", "Maskerne er store nok til at se fejl, og en sweater tager 20–30 timer. Start her, hvis du er ny."),
  ],
  faq=[("Hvilke garner passer til pind 4?","Garner med 20–23 masker pr. 10 cm – DK-tykkelse. Drops Merino Extra Fine, Karisma, Lima, Belle, Önling No 1."),("Er pind 4 godt til begyndere?","Ja. Maskerne er nemme at se, og en sweater tager 20–30 timer.")]),
 dict(n="5", kw="gratis strikkeopskrifter pind 5", h1="Strikkeopskrifter til pind 5", title="Strikkeopskrifter pind 5 – hurtigt strik i Air, Nepal og Paris",
  meta="Strikkeopskrifter til pind 5 (4,5–5,5 mm): sweatre og huer i Drops Air, Nepal, Big Merino, Paris og Daisy. Gratis opskrifter med garnforbrug og pris.",
  intro=["På pind 5 vokser strikket hurtigt – en sweater på en uge er realistisk. Garnerne er luftige (Air), varme (Nepal) eller bomuld til sommer (Paris).",
         "Her er opskrifter til pind 4,5–5,5 med garn og pris. Air er det populære valg til lette vintersweatre; Nepal og Big Merino til de mere robuste."],
  sections=[
   ("Air, Nepal eller Paris?", "Air (alpaka/uld/polyamid) er let og varm – til vintersweatre. Nepal (uld/alpaka) er tungere og mere robust. Paris (bomuld) er til sommer og til børn. Alle tre strikkes på pind 5 og kan ofte byttes."),
   ("Pind 5 og oversize", "Mange oversize-modeller er skrevet til pind 5 – garnet må ikke være for tungt, ellers falder sweateren. Air er derfor det typiske valg."),
  ],
  faq=[("Hvilke garner passer til pind 5?","17–19 masker pr. 10 cm: Drops Air, Nepal, Big Merino, Paris, Daisy, Soft Tweed."),("Hvor meget garn?","450–600 g til en voksen M – flere gram end på pind 3, men langt færre timer.")]),
 dict(n="7", kw="gratis strikkeopskrifter pind 7", h1="Strikkeopskrifter til pind 7", title="Strikkeopskrifter pind 7 – tykt strik på en weekend",
  meta="Strikkeopskrifter til pind 7 (6–7 mm): tykke sweatre, huer og halsrør i Drops Melody, Alaska og Wish. Hurtige projekter med garnpris.",
  intro=["Pind 7 er weekendprojektet: en hue på en time, et halsrør på to, en sweater på et par dage. Garnerne er tykke og bløde – børstet alpaka som Melody, eller ren uld som Alaska.",
         "Her er opskrifter til pind 6–7 med garn og pris. Bemærk at tykt garn koster mere pr. sweater, fordi løbelængden er kort – sammenlign prisen pr. nøgle."],
  sections=[
   ("Hurtig strik med omtanke", "På pind 7 er en sweater færdig på en weekend, men garnet er tungt. Vælg en let kvalitet (Melody, Air holdt dobbelt) frem for ren uld, hvis den skal bæres indendørs."),
   ("Huer og halsrør", "Det er her, pind 7 skinner: en hue på en time, et halsrør på to. Begge bruger 1–2 nøgler."),
  ],
  faq=[("Hvilke garner til pind 7?","13–16 masker pr. 10 cm: Drops Melody, Alaska, Wish (pind 8), Snow."),("Hvor meget garn?","600–900 g til en voksensweater i tykt garn.")]),
 dict(n="8", kw="gratis strikkeopskrifter pind 8", h1="Strikkeopskrifter til pind 8", title="Strikkeopskrifter pind 8 – chunky sweatre, huer og tæpper",
  meta="Strikkeopskrifter til pind 8 (7–9 mm): chunky sweatre, cardigans, huer og tæpper i Drops Snow, Wish og Polaris. Nemme projekter med garnpris.",
  intro=["Pind 8 er chunky-strik: store masker, hurtigt resultat og et look, der er blevet populært igen. Det er også det mest tilgivende for begyndere – fejl er nemme at se og rette.",
         "Her er opskrifter til pind 7–9 med garn og pris. Snow (tidligere Eskimo), Wish og Polaris er de typiske garner."],
  sections=[
   ("Chunky uden at det bliver tungt", "Snow/Eskimo er ren uld og tung; Wish og Polaris er blandinger med alpaka og er lettere. Til en sweater, du vil bruge, vælg den lette."),
   ("Tæpper på pind 8", "Et tæppe 120 × 150 cm bruger 1.000–1.400 g på pind 8. Det lyder af meget, men det tager kun 10–15 timer."),
  ],
  faq=[("Hvilke garner til pind 8?","10–13 masker pr. 10 cm: Drops Snow, Wish, Polaris, Andes."),("Er chunky-strik dyrt?","Det kan det være – 50 g rækker kun 50–75 m. Regn med 700–1.000 g til en sweater, og sammenlign prisen pr. nøgle.")]),
]
