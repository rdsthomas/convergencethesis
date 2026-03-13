# Research: Kapitel 5 — Energie-Ergänzungen

> **Recherche-Datum:** 24. Februar 2026
> **Quellen:** Deloitte, IEA, Lazard, World Nuclear Association, Cameco, EESI, UC Riverside, OPB, u.a.

---

## Thema 1: Erneuerbare vs. Nuklear für KI-Rechenzentren

### 1.1 Kapazitätsfaktor — Was bedeutet das praktisch?

Der Kapazitätsfaktor gibt an, wie viel Prozent der theoretisch möglichen Stromerzeugung eine Anlage tatsächlich liefert:

| Energiequelle | Kapazitätsfaktor | Praktische Bedeutung |
|--------------|-----------------|---------------------|
| **Nuklear** | **~92,5%** | Liefert >22 Stunden/Tag, 340+ Tage/Jahr |
| Erdgas (CCGT) | ~56% | Flexibel, aber fossil |
| Onshore-Wind | ~33–35% | Liefert nur wenn Wind weht |
| Solar PV | ~23–25% | Liefert nur tagsüber, wetterabhängig |

**Quelle:** EIA, Deloitte Research Center for Energy & Industrials (Dezember 2024)

**Was das praktisch bedeutet:** Ein 1-GW-Kernkraftwerk erzeugt pro Jahr ca. 8.100 GWh Strom. Um dieselbe Energiemenge mit Solar zu erzeugen, bräuchte man 3,3–4 GW installierte Solarkapazität — aber selbst dann nicht zur richtigen Zeit. Nuklear ist 2–4× so zuverlässig wie Wind oder Solar.

### 1.2 Das Intermittenz-Problem

KI-Rechenzentren brauchen **24/7/365 Strom mit 99,99% Zuverlässigkeit**. Das ist der Kern des Problems:

- **Solar** liefert Strom nur ca. 6–10 Stunden pro Tag (je nach Standort und Jahreszeit). Nachts: null.
- **Wind** ist fundamental unberechenbar. Es gibt Perioden von Tagen oder Wochen mit Windstille ("Dunkelflauten").
- **KI-Training** ist besonders energieintensiv und kann nicht einfach unterbrochen werden. Ein Trainingsrun über Wochen muss durchgehend mit Strom versorgt werden.

Google hat selbst festgestellt: **Keines seiner Rechenzentren weltweit war 2017 rund um die Uhr zu 100% mit kohlenstofffreier Energie versorgt** — obwohl Google der weltweit größte Corporate-Käufer erneuerbarer Energien ist.

### 1.3 Das Speicher-Problem — Kosten für 1 GW Rechenzentrum

Die Schlüsselanalyse kommt von Gordon Hughes (Energieökonom, ehemaliger Weltbank-Berater):

**Szenario: 1 GW Rechenzentrum mit 99,99% Zuverlässigkeit rein erneuerbar versorgen:**

| Komponente | Benötigte Kapazität | Kapitalkosten |
|-----------|--------------------:|-------------:|
| Offshore-Wind | ≥1,8 GW | ~$7 Mrd. |
| Solar PV | ≥1,5 GW | ~$1,5 Mrd. |
| Batteriespeicher (8h) | 1 GW / 8 GWh | ~$4,8 Mrd. |
| **Gesamt (erneuerbar)** | | **~$13,3 Mrd.** |

**Zum Vergleich — Nuklear-Optionen für dasselbe 1 GW Rechenzentrum:**

| Option | Beschreibung | Kapitalkosten |
|--------|-------------|-------------:|
| **Konventionelles AKW** (z.B. Korean APR-1400) + Gas-Backup | 1 GW Nuklear + 1 GW Gasturbinen-Backup für Wartung | **~$9,85 Mrd.** |
| **4 × 300 MW SMR** + Gas-Backup | Modulare Reaktoren + 300 MW Gasturbinen | **~$10,6 Mrd.** |
| **Erneuerbar + Gas-Backup** (statt Batterie) | Wind+Solar + Gasturbinen statt Batterien | **~$10,9 Mrd.** |
| **Reines Gas** (4 × 300 MW CCGT + Backup) | Billigste Option, aber CO₂-intensiv | **~$1,7 Mrd.** |

**Quelle:** Gordon Hughes, "Assessing electricity generation costs: Supplying a 1-GW data centre" (November 2024)

**Kernaussage:** Batterie allein reicht nicht. Selbst 8-Stunden-Batterie kostet ~$4,8 Mrd. und deckt nur eine Nacht ab. Für eine 35-tägige Wartungsperiode eines Reaktors würde Batteriespeicher **über $60 Mrd.** kosten. Ohne Gas-Backup geht es praktisch nicht.

**Aktuelle Batteriekosten (Stand Ende 2025):**
- Utility-Scale (4h+): ~$125/kWh (Ember, Oktober 2025)
- Installiert (kommerziell): $280–580/kWh
- Saudi-Arabien (Tabuk/Hail-Projekte, August 2025): Rekordtief $73–75/kWh nur für Zellen

### 1.4 Flächenverbrauch

| Energiequelle | Fläche für 1 GW (equivalent output) |
|--------------|-------------------------------------|
| **Kernkraftwerk** | **~1,3 Quadratmeilen** (~3,4 km²) |
| **Solarpark** | **45–75 Quadratmeilen** (~115–195 km²) |
| **Windpark** | **260–360 Quadratmeilen** (~670–930 km²) |

**Quelle:** NEI (Nuclear Energy Institute), DOE

Nuklear braucht also **35–60× weniger Fläche als Solar** und **200–280× weniger als Wind** für dieselbe Energieproduktion. Das ist besonders relevant für dicht besiedelte Regionen.

In Bezug auf Landintensität pro Energieeinheit:
- **Nuklear:** 7,1 ha/TWh/Jahr (Median)
- **Solar:** ~400 ha/TWh/Jahr
- **Wind:** ~700+ ha/TWh/Jahr (wenn man Gesamtfläche zählt)

**Quelle:** The Breakthrough Institute (Juli 2022)

### 1.5 Die großen Tech-Deals — Warum Solar/Wind allein nicht reicht

Die Hyperscaler haben massiv in Erneuerbare investiert — und wenden sich trotzdem Nuklear zu:

| Unternehmen | Erneuerbare-Deals | Nuklear-Deals |
|------------|------------------|---------------|
| **Google** | Weltgrößter Corporate-PPA-Käufer; zuletzt 1,2 GW Clearway-Deal (Jan. 2026), TotalEnergies-PPA | Kairos Power SMR-Flottenvertrag: 500 MW, ab 2030+; Intersect Power-Übernahme (Dez. 2025) |
| **Microsoft** | Massiver Wind/Solar-PPA-Bestand | **Three Mile Island Restart:** 20-jähriger PPA, 835 MW, $16 Mrd., Ziel 2027; $1 Mrd. DOE-Darlehen (Nov. 2025) |
| **Amazon** | Größter Corporate-Käufer erneuerbarer Energien weltweit | $20+ Mrd. Investment in Susquehanna-Nuklear-Campus; $650 Mio. Rechenzentrum neben AKW |
| **Meta** | Große Solar/Wind-PPAs | Nuclearisierung zunehmend in Diskussion |

**Warum reichen die Erneuerbaren-Deals nicht?**
- PPAs für Solar/Wind sind **buchhalterische Übungen**: Die Energie wird physisch nicht zum Rechenzentrum geliefert, sondern ins Netz eingespeist und "verrechnet" (sog. RECs — Renewable Energy Certificates).
- Google gab zu: **90%** carbon-free bis 2025 — aber nicht 100%, und nicht 24/7.
- Die physische Grundlastversorgung kommt weiterhin aus dem Netz (fossil/nuklear).

### 1.6 Baseload vs. Peakload — Warum Grundlastfähigkeit entscheidend ist

**Grundlast (Baseload):** Die minimale, konstant benötigte Stromleistung rund um die Uhr. Rechenzentren sind das Paradebeispiel:

- KI-Rechenzentren verbrauchen 24/7 nahezu konstant Strom (Load Factor >95%)
- GPU-Cluster für Training laufen Wochen oder Monate ohne Unterbrechung
- Selbst Inference-Workloads haben keinen "Off"-Schalter

**Das Problem mit Erneuerbaren für Grundlast:**
- Solar produziert zur **Mittagszeit das Maximum**, nachts null → komplett asynchron mit 24/7-Bedarf
- Wind ist **statistisch unkorreliert** mit dem Bedarf
- Man kann nicht einfach "4× so viel Solar" installieren — nachts bleibt es dunkel

**Nuklear ist der einzige kohlenstofffreie Grundlastproduzent im großen Maßstab.**

### 1.7 PPAs (Power Purchase Agreements) — Warum sie das Problem nicht lösen

**Wie PPAs funktionieren:**
1. Techkonzern schließt langfristigen Vertrag (10–25 Jahre) mit Strom-Erzeuger
2. Erzeuger baut Solar/Windpark und speist Strom ins Netz ein
3. Techkonzern erhält RECs (Renewable Energy Certificates) in Höhe der eingespeisten Menge
4. Der tatsächliche Strom im Rechenzentrum kommt aus dem lokalen Netz-Mix

**Warum das nicht reicht:**
- **Zeitlicher Mismatch:** Das Rechenzentrum verbraucht nachts Strom, die RECs stammen von mittags erzeugtem Solarstrom → **zeitliche Entkopplung**
- **Geografischer Mismatch:** Der Windpark steht in Texas, das Rechenzentrum in Virginia → **räumliche Entkopplung**
- **Physisch null Effekt:** In der Stunde, in der das Rechenzentrum Strom braucht und kein Wind weht, kommt der Strom aus dem Gaskraftwerk nebenan
- **24/7 Carbon-Free Energy (CFE)** ist das neue Ziel: Google arbeitet an "zeitlich abgeglichenem" CFE, gibt aber zu, dass sie davon weit entfernt sind

**Die IEA prognostiziert:** Ab 2030 werden SMRs in den Energie-Mix für Rechenzentren eintreten. GlobalData erwartet **mindestens 3 GW zusätzliche SMR-Kapazität für Rechenzentren bis 2028**, mit einem Peak zwischen 2031–2035.

---

## Thema 2: Die Ökonomie der Energie — Kosten und Uranpreis

### 2.1 Baukosten für 1 GW Stromerzeugungskapazität

| Technologie | Kapitalkosten pro kW | Kosten für 1 GW | Bauzeit |
|------------|--------------------:|-----------------:|---------|
| **Solar PV (Utility)** | $1.000–1.400/kW | **$1,0–1,4 Mrd.** | 1–2 Jahre |
| **Onshore-Wind** | $1.300–1.600/kW | **$1,3–1,6 Mrd.** | 2–3 Jahre |
| **Offshore-Wind** | $3.500–5.000/kW | **$3,5–5,0 Mrd.** | 3–5 Jahre |
| **Erdgas (CCGT)** | $700–1.100/kW | **$0,7–1,1 Mrd.** | 2–3 Jahre |
| **Konventionelles AKW** (Neubau, USA) | $8.500–14.000/kW | **$8,5–14 Mrd.** | 7–15 Jahre |
| **Konventionelles AKW** (Korean APR-1400) | ~$5.000–7.000/kW | **$5–7 Mrd.** | 5–7 Jahre |
| **SMR** (Projektkost.) | Noch ungewiss, geschätzt $5.000–8.000/kW | **$5–8 Mrd.** | 3–7 Jahre (Ziel) |
| **Vogtle 3&4** (2024, reale Kosten) | ~$16.000/kW | **$35 Mrd. für 2,2 GW** | 14 Jahre |

**Quellen:** EIA AEO 2025, Statista, World Nuclear Association, Lazard

**Wichtig:** Die reinen Baukosten täuschen. Solar ist billig zu **bauen**, aber braucht massive Zusatzinvestitionen (Speicher, Netzausbau, Backup), um grundlastfähig zu werden.

### 2.2 LCOE — Levelized Cost of Energy (Lazard 2025)

| Technologie | LCOE (unsubventioniert, $/MWh) |
|------------|-------------------------------|
| **Onshore-Wind** | $27–73 |
| **Solar PV (Utility)** | $38–78 |
| **Erdgas (CCGT)** | $48–107 |
| **Kohle** | $71–173 |
| **Nuklear (Neubau, USA)** | $141–220 |

**Quelle:** Lazard LCOE+ Report, Juni 2025

**Kritische Einordnung:**
- LCOE ist ein **irreführendes Maß** für den Vergleich zwischen dispatchablen (steuerbar) und intermittierenden Quellen.
- LCOE für Solar berücksichtigt **nicht** die Kosten für Speicher, Netzausbau und Backup — die sogenannten "Firming Costs".
- Solar LCOE + Firming (Batterien + Gas-Backup) liegt bei **$90–150/MWh** — vergleichbar mit Nuklear.
- Gordon Hughes (ehemaliger Weltbank-Berater): "Die einzige Verwendung von LCOE-Vergleichen zwischen verschiedenen Technologien ist Lobbyarbeit und PR."
- Die **DOE Liftoff-Studie** berechnete die unsubventionierten Kosten für Vogtle 3/4 auf **$186/MWh** (in 2024-Preisen).

### 2.3 Uranpreis — Aktueller Stand und Entwicklung

**Aktueller Preis (Februar 2026):**
- **Spot-Preis:** ~$88/lb U₃O₈ (10. Februar 2026, Trading Economics)
- **Langfristpreis:** $86,50/lb (14-Jahres-Hoch, Dezember 2025)

**Historischer Verlauf:**

| Jahr | Spot-Preis (Ø $/lb U₃O₈) | Bemerkung |
|------|:-------------------------:|-----------|
| 2020 | $29,96 | COVID-Tief |
| 2021 | $35,28 | Erholung beginnt |
| 2022 | $49,81 | Russland-Ukraine-Krieg |
| 2023 | $62,51 | Angebotssorgen, Niger-Putsch |
| 2024 | $85,14 | Tech-Nachfrage-Rallye |
| 2025 | $73,54 (Ø) / $63–83 (Range) | Volatile Konsolidierung, Langfristpreise steigen |
| Feb 2026 | ~$88 | Erneuter Anstieg |

**Quelle:** Cameco, TradeTech, Trading Economics

**Warum steigt der Uranpreis?**
1. **Tech-Nachfrage:** Microsoft TMI-Restart, Google SMR-Deals, Amazon Nuklear-Campus
2. **Angebotsdefizit:** Primäre Minenproduktion deckt Nachfrage nicht
3. **Kasachstan-Risiko:** Kazatomprom senkt Produktion 2026 um 10%; Schwefelsäure-Engpässe
4. **Cameco-Produktionskürzung:** McArthur River Verzögerungen → 19% Guidance-Reduktion (Aug. 2025)
5. **Niger-Instabilität:** Politische Krise bedroht Orano-Operationen (~50% der Primärproduktion kommen aus Kasachstan + Niger)
6. **Sprott Physical Uranium Trust (SPUT):** Aggressiver physischer Uran-Kauf entzieht dem Spotmarkt Material
7. **COP30-Erklärung:** 33 Länder bekennen sich zur **Verdreifachung der Kernkraftkapazität bis 2050**

### 2.4 Uranium Supply Gap — Die strukturelle Lücke

**Nachfrage vs. Angebot:**

| Kennzahl | Menge |
|----------|-------|
| **Globale Reaktor-Nachfrage (2025)** | ~68.920 tU/Jahr (~179 Mio. lbs U₃O₈) |
| **Primäre Minenproduktion (2024)** | ~54.345 tU (~140–150 Mio. lbs U₃O₈) |
| **Strukturelle Lücke** | **~25.000–30.000 tU/Jahr** (~30–40 Mio. lbs) |
| **Sekundäre Quellen (2025)** | ~27 Mio. lbs (14% des Angebots, fallend) |
| **Sekundäre Quellen (2030, Prognose)** | ~17 Mio. lbs (8% des Angebots) |

**Quelle:** World Nuclear Association 2025 Fuel Report, UxC, IAEA

Die Lücke wird heute durch Lagerbestände, wiederaufbereitetes Material und Unterversorgung geschlossen. Diese sekundären Quellen **schrumpfen jedoch stetig** — von 14% auf geschätzt 8% bis 2030.

**Langfristig:** 116 Mio. lbs wurden 2025 unter Langfristvertrag gestellt — aber das lag **unter der Replacement Rate**, was die kumulativen ungedeckten Anforderungen in der Zukunft erhöht.

### 2.5 Cameco und Kazatomprom — Marktführer unter Druck

| Produzent | Marktanteil | Produktion 2025 | Situation |
|-----------|:-----------:|:--------------:|-----------|
| **Kazatomprom** (Kasachstan) | ~24% der Weltproduktion | Reduziert | 10% Produktionskürzung 2026; Schwefelsäure-Engpass; 12–17% Kürzung in 2025 |
| **Cameco** (Kanada) | ~14–20% der Weltproduktion | Reduziert | 19% Guidance-Reduktion wg. McArthur River-Verzögerungen (Aug. 2025) |
| **Orano** (Frankreich/Niger) | ~8% | Bedroht | Niger-Putsch 2023 → politische Instabilität |

Die beiden größten Produzenten liefern zusammen **~40% der Weltproduktion** — und beide kürzen gerade die Produktion.

### 2.6 Enrichment Bottleneck — Der Engpass bei der Urananreicherung

Die Urananreicherung ist ein **noch kritischerer Engpass** als die Minenproduktion:

**Globale Anreicherungskapazität (in Mio. SWU/Jahr):**

| Anbieter | Kapazität (Mio. SWU) | Marktanteil |
|----------|---------------------:|:-----------:|
| **Rosatom (Russland)** | 27 | ~40% |
| **Urenco (UK/NL/DE)** | 18 | ~21% |
| **CNNC (China)** | 12,5 | ~14% |
| **Orano (Frankreich)** | 7,5 | ~13% |
| Andere | 12 | ~12% |
| **Gesamt (nominell)** | **~77** | |

**Quelle:** World Nuclear Association, Discovery Alert (Oktober 2025)

**Das geopolitische Problem:**
- **Russland kontrolliert ~40% der globalen Anreicherung** — vergleichbar mit Europas früherer Abhängigkeit von russischem Gas
- Die USA bezogen ~24% ihrer Anreicherungsdienste aus Russland
- Biden unterzeichnete im Mai 2024 das **"Prohibiting Russian Uranium Imports Act"**
- **Effektive westliche Kapazität ohne Russland:** Nur ~37–40 Mio. SWU/Jahr

**Prognosen:**
- **Referenz-Szenario:** Globales Anreicherungsdefizit ab **2034**
- **Oberes Szenario:** Defizit bereits **2030–2032**
- ARK Invest: "SWUs werden **bis 2030** knapp"
- HALEU (High-Assay Low-Enriched Uranium) für SMRs benötigt **5–6× mehr SWU pro kg** als konventioneller Brennstoff

### 2.7 Uranverbrauch eines typischen Kernkraftwerks

| Kennzahl | Wert |
|----------|------|
| Jährlicher Verbrauch (1 GW Reaktor) | **~25 t angereichertes Uran** |
| Äquivalent in Natururan | **~163–250 t Natururan** |
| Brennstoff-Beladung (1 GW LWR) | ~27 t Brennstoff alle 1,5 Jahre |
| SWU-Bedarf pro 1 GW Reaktor | ~100.000–120.000 SWU/Jahr |
| Globaler Bedarf (436 Reaktoren, ~400 GWe) | ~67.000–69.000 tU/Jahr |

**Zum Vergleich:** Ein Uranbrennstoff-Pellet (Fingerkuppe groß) erzeugt so viel Energie wie **1 Tonne Kohle**, 149 Gallonen Öl oder 17.000 Kubikfuß Erdgas.

---

## Thema 3: Der Wasserverbrauch von Rechenzentren

### 3.1 Wie viel Wasser verbraucht ein Rechenzentrum?

**Typische Verbrauchswerte:**
- **Durchschnittliche WUE (Water Usage Effectiveness):** 1,9 Liter pro kWh
- **Hyperscale-Rechenzentrum:** ~550.000 Gallonen (~2,1 Mio. Liter) **pro Tag**
- **Pro Facility und Jahr:** ~200 Mio. Gallonen (~760 Mio. Liter)
- **Mittelgroßes Rechenzentrum:** ~110 Mio. Gallonen/Jahr (= Jahresverbrauch von ~1.000 Haushalten)
- **Großes Rechenzentrum:** Bis zu 5 Mio. Gallonen/Tag (~1,8 Mrd. Gallonen/Jahr)

**Quelle:** EESI, CloudComputing News (2025)

### 3.2 Warum brauchen Rechenzentren so viel Wasser?

**Verdunstungskühlung** ist der Haupttreiber:

1. **Server erzeugen Hitze:** GPUs/CPUs laufen unter Volllast bei 70–90°C
2. **Luft muss gekühlt werden:** Kühltürme nutzen Verdunstung von Wasser, um heiße Luft abzukühlen
3. **Verdunstung = Wasserverbrauch:** Das Wasser verdampft und ist "verbraucht" (nicht recycelbar)
4. **Stromversorgung verbraucht auch Wasser:** Thermische Kraftwerke (Gas, Kohle) nutzen ebenfalls Wasser zur Kühlung → "indirekter" Wasserverbrauch

Der gesamte Wasserverbrauch umfasst:
- **On-site:** Wasser für die Kühlung im Rechenzentrum selbst
- **Off-site:** Wasser für die Stromerzeugung (Kraftwerke)
- Verhältnis: ca. **1,3–2,0 ml pro Wh** Gesamtverbrauch (direkt + indirekt)

### 3.3 Wasserverbrauch der Big Tech — Konkrete Zahlen

| Unternehmen | Wasserverbrauch (2023/2024) | Trend |
|------------|---------------------------|-------|
| **Google** | **6,1 Mrd. Gallonen** (23,1 Mrd. Liter) für Rechenzentren (2023); **8,1 Mrd. Gallonen** (2024, inkl. Büros) | ↑ Stark steigend |
| **Microsoft** | **~1,69 Mrd. Gallonen** (6,4 Mio. m³) gesamt; **+34% ggü. Vorjahr** | ↑↑ Rapide steigend |
| **Meta** | **813 Mio. Gallonen** (3,1 Mrd. Liter) gesamt (2023); 95% davon (776 Mio. Gallonen) für Rechenzentren | ↑ Steigend |

**Extrembeispiel:** Googles Rechenzentrum in **Council Bluffs, Iowa** verbrauchte 2024 allein **1 Milliarde Gallonen** (3,8 Mrd. Liter) — genug, um den gesamten Trinkwasserbedarf aller Haushalte in Iowa zu decken.

**Quellen:** Google Environmental Report 2024, Microsoft Environmental Sustainability Report 2025, Meta Sustainability Report 2024, Fast Company (August 2025)

### 3.4 Wasserknappheit und Konflikte mit lokalen Gemeinden

#### The Dalles, Oregon (Google)

Der bekannteste Fall weltweit:

- **Bevölkerung:** ~16.000 Einwohner
- Google betreibt seit 2006 mehrere Rechenzentren in der Kleinstadt
- Google **versuchte aktiv, seinen Wasserverbrauch geheim zu halten** — bezahlte $100.000 für die Klage der Stadt gegen die Zeitung "The Oregonian"
- Bewohner nennen Google inzwischen **"Voldemort"** (Fortune, Juni 2023)
- Google plant **weitere Rechenzentren** in der Region → erhöhter Wasserbedarf
- Die Stadt will nun **Wasser aus dem Mount-Hood-Nationalwald** beziehen, um den wachsenden Bedarf zu decken
- **Umweltschützer befürchten:** Das Wasser wird primär für Google benötigt, nicht für die Bevölkerung
- OPB (Oregon Public Broadcasting) investigierte im Januar 2026 die Verbindung zwischen Google und der Wasserplanung — der Bürgermeister reagierte empört

**Quellen:** OPB (Januar 2026), Fortune (2023), AP News (2022), Stanford (April 2025)

#### Weitere Konflikte:
- **Mesa/Goodyear, Arizona:** Wüstenstandorte mit bereits bestehender Wasserknappheit, neue Rechenzentren erhöhen den Druck
- **Morrow County, Oregon:** Weitere Google-Expansion in wasserarmem Gebiet
- **Bloomberg (Mai 2025):** Investigativ-Bericht "How AI Demand is Draining Local Water Supplies"

### 3.5 Wasserverbrauch von KI vs. normale Cloud-Workloads

KI-Workloads verbrauchen **deutlich mehr** Energie und damit auch Wasser:

- **KI-Training** (LLM) verwendet exponentiell mehr Rechenleistung als klassische Cloud-Dienste
- **GPU-Dichte** in KI-Rechenzentren ist **10–20× höher** als in normalen Cloud-Rechenzentren → mehr Wärme → mehr Kühlung → mehr Wasser
- US-Rechenzentren verbrauchen nun **~4,4% des nationalen Stromverbrauchs**, gegenüber ~1,9% in 2018 — hauptsächlich wegen KI
- IEA (November 2025): Globaler Strombedarf wächst bis 2035 um mindestens ein Drittel, getrieben durch Digitalisierung und KI

**Hochrechnungen:**
- Die Rack-Dichte steigt von typischerweise 6–10 kW/Rack (Cloud) auf **40–100+ kW/Rack** (KI-Training mit NVIDIA H100/B200)
- Wasser-Verbrauch skaliert **überproportional**, da Verdunstungskühlung bei höherer Leistungsdichte weniger effizient ist

### 3.6 Wasserverbrauch pro ChatGPT-Anfrage

**Die Forschungslage (nuanciert):**

| Quelle | Zahl | Kontext |
|--------|------|---------|
| **UC Riverside Studie (2023)** | ~500 ml pro 5–50 Prompts | On-site + Off-site (Kraftwerke), GPT-3 |
| **Washington Post + UC Riverside (2025)** | **519 ml** für eine 100-Wort-E-Mail (GPT-4) | Inkl. indirektem Wasserverbrauch der Stromerzeugung |
| **IE Business School (2025)** | **10–25 ml pro einzelnem Prompt** | Konservativere Schätzung pro Einzelanfrage |
| **OpenAI (offiziell, Juni 2025)** | **0,32 ml pro Query** | Nur on-site Wasser, ohne Stromerzeugung |

**Einordnung:**
- Die **519 ml** Zahl ist die bekannteste, aber sie **inkludiert den Wasserverbrauch der Stromerzeugung** (off-site) — das ist methodisch korrekt, aber irreführend im Vergleich.
- Die offizielle OpenAI-Zahl (0,32 ml) misst nur direkten On-site-Verbrauch.
- **Realistischer Bereich:** 10–25 ml pro Anfrage (wenn man On-site + anteiliges Off-site berücksichtigt).
- Bei **200+ Mio. täglichen ChatGPT-Nutzern** summiert sich selbst ein kleiner Pro-Anfrage-Verbrauch enorm.

**Vergleich:** Man bräuchte ~1.500 ChatGPT-Anfragen, um eine Standard-Wasserflasche (500 ml) zu verbrauchen (nur On-site). **Aber:** Training von GPT-4 soll ca. **700.000 Liter** Wasser verbraucht haben (nur Training, nicht Inference).

### 3.7 Lösungsansätze

| Lösung | Beschreibung | Status |
|--------|-------------|--------|
| **Direct Liquid Cooling (DLC)** | Cold Plates direkt auf Chips; entfernt 70–80% der Wärme am Chip | Zunehmend Standard für KI-Racks; **reduziert Kühlenergieaufwand um ~50%** |
| **Immersion Cooling** | Server komplett in dielektrische Flüssigkeit getaucht | LiquidStack: 40 MW Pilotprojekt in Georgien; erhebliche Wasser-Einsparungen |
| **Closed-Loop-Systeme** | Wasser wird im Kreislauf geführt, nicht verdampft | WUE nahe 0 möglich, aber höhere Energiekosten |
| **Luftkühlung** | Nur Außenluft, kein Wasser | Nur in kalten Klimazonen (Skandinavien, Island) wirtschaftlich; WUE = 0 |
| **Standortwahl** | Kühle Regionen mit reichlich Wasser (Skandinavien, Kanada, Irland) | Abwägung gegen Latenz und Netzanbindung |
| **Water Positive-Versprechen** | Google, Microsoft: mehr Wasser zurückgeben als verbraucht wird (bis 2030) | Bisher nicht erreicht; Microsoft: Wasserverbrauch stieg um 34% |

**Google und Microsoft** haben sich zu **"water positive by 2030"** verpflichtet — aber der Wasserverbrauch steigt bei beiden Unternehmen rapide.

---

## Zusammenfassung: Die wichtigsten Zahlen für Kapitel 5

### Energie-Gleichung für KI-Rechenzentren:
- 1 GW Rechenzentrum mit Erneuerbaren + Speicher: **~$13,3 Mrd.**
- 1 GW Rechenzentrum mit Nuklear + Gas-Backup: **~$9,85 Mrd.**
- 1 GW Rechenzentrum rein mit Gas: **~$1,7 Mrd.**
- Nuklear ist der **einzige** skalierbare, kohlenstofffreie 24/7-Grundlastproduzent

### Uranmarkt:
- Spotpreis Feb. 2026: **~$88/lb** (2020: $30)
- Strukturelle Angebots-Lücke: **~30–40 Mio. lbs/Jahr**
- Beide Top-Produzenten (Cameco + Kazatomprom) **kürzen Produktion**
- Anreicherung: Russland kontrolliert **~40%** — geopolitisches Risiko
- COP30: **33 Länder** wollen Kernkraft bis 2050 verdreifachen

### Wasser:
- Google-Rechenzentren verbrauchten 2024: **8,1 Mrd. Gallonen**
- Microsoft: **+34%** Wasserverbrauch-Anstieg
- Pro ChatGPT-Anfrage: **~0,32 ml** (on-site) bis **~10–25 ml** (inkl. Stromerzeugung)
- Konflikte in Oregon, Arizona und weltweit nehmen zu
- Liquid Cooling als Lösung, aber noch nicht flächendeckend
