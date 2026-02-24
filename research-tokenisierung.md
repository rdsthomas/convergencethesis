# Deep Dive: Tokenisierung aller Assets — Research-Report

*Recherche für "Maschinengeld" (Convergence Thesis) | Stand: 24. Februar 2026*

---

## Executive Summary

Tokenisierung — die Umwandlung von Eigentumsrechten an realen Vermögenswerten in digitale Token auf einer Blockchain — ist dabei, die Investmentlandschaft fundamental zu verändern. Der Markt für tokenisierte Real-World Assets (RWA) hat Ende 2025 die **$36-Milliarden-Marke** überschritten (ohne Stablecoins), ein Wachstum von über **2.200% seit 2020**. Die Prognosen für 2030 schwanken dramatisch: **$2–4 Billionen** (McKinsey, konservativ), **$16 Billionen** (BCG), bis hin zu **$30 Billionen** (Standard Chartered, bullish).

Das Thema fehlt als eigenständiger Deep Dive im Buch "Maschinengeld" — und das ist eine **kritische Lücke**, denn Tokenisierung ist das Bindeglied zwischen "Maschinen brauchen Krypto" und "was bedeutet das für den Kleinanleger".

---

## 1. Status Quo: Was wird heute schon tokenisiert?

### 1.1 Marktgröße und Wachstum

| Kennzahl | Wert | Quelle |
|----------|------|--------|
| RWA on-chain (Ende 2025) | **$36 Mrd.** (ex Stablecoins) | RWA.io / Canton Network Report |
| Wachstum seit 2022 | **~380%** (von $5 auf $24 Mrd. bis Mitte 2025) | RedStone / CoinDesk |
| Tokenisierte US-Treasuries | **~$9 Mrd.** | rwa.xyz |
| Tokenisierte Money Market Funds | **$8,6 Mrd.** AUM | AInvest |
| BlackRock BUIDL allein | **$1,8–3 Mrd.** | DL News / BlockInvest |
| Prognose 2030 (McKinsey, base) | **$2–4 Billionen** | McKinsey 2024 |
| Prognose 2030 (BCG, bullish) | **$16 Billionen** | BCG / Ripple Report |
| Prognose 2034 (Std. Chartered) | **$30 Billionen** | Standard Chartered |
| Prognose 2030 (Ark Invest) | **>$11 Billionen** | Ark Invest, Jan 2026 |

### 1.2 Asset-Klassen

**Bereits tokenisiert und skalierend:**
- **Staatsanleihen / Treasuries:** Die Einstiegsdroge der Institutionellen. BlackRock BUIDL, Franklin Templeton BENJI, Ondo Finance USDY. Allein tokenisierte US-Treasuries: ~$9 Mrd.
- **Money Market Funds:** JPMorgan TCN, BlackRock BUIDL, Goldman Sachs GS DAP. AUM verdoppelt auf $8,6 Mrd. in 2025.
- **Private Credit / Lending:** Centrifuge, Maple Finance, Goldfinch. Reale Kredite an Unternehmen, tokenisiert und für DeFi-Investoren zugänglich.
- **Immobilien:** RealT (US-Mietimmobilien ab $50), Prypco Mint (Dubai), Lofty.ai. Globaler tokenisierter Immobilienmarkt: ~$20 Mrd., BCG-Prognose $3,2 Bio. bis 2030.

**Im Aufbau / Pilotphase:**
- **Aktien / Equity:** Nasdaq hat im Januar 2026 bei der SEC beantragt, tokenisierte Aktien auf der Börse handeln zu dürfen. DTCC/DTC betreibt einen 3-Jahres-Pilot.
- **Private Equity / Venture Capital:** Securitize (hat KKR-Fonds tokenisiert), Hamilton Lane (tokenisierte PE-Fonds ab $20.000 statt $5 Mio.)
- **Rohstoffe:** Paxos Gold (PAXG), Tether Gold (XAUt). Tokenisiertes Gold: >$1 Mrd.
- **Intellectual Property:** Royal.io (Musik-Royalties), IPwe (Patente auf IBM-Blockchain)
- **Kunst & Collectibles:** Masterworks (fraktionierte Blue-Chip-Kunst), Otis
- **Infrastruktur & Farmland:** AcreTrader, Lofty (tokenisiertes Farmland)

### 1.3 Die wichtigsten Plattformen

| Plattform | Fokus | Volumen/Status |
|-----------|-------|----------------|
| **Securitize** | Security Tokens, PE-Fonds | KKR, Hamilton Lane, BlackRock-Partner |
| **Ondo Finance** | Tokenisierte Treasuries (USDY, OUSG) | >$600 Mio. TVL |
| **Centrifuge** | Private Credit / RWA | >$500 Mio. finanziert |
| **RealT** | Tokenisierte US-Immobilien | Ab $50 pro Token, >$100 Mio. |
| **Maple Finance** | Institutionelle Kreditvergabe | >$3 Mrd. kumuliert |
| **Franklin Templeton** | BENJI (tokenisierter Money Fund) | On Stellar & Polygon |
| **Figure Technologies** | HELOC-Verbriefung auf Blockchain | >$13 Mrd. Origination |
| **Mavryk** | UAE Premium Real Estate | $10 Mrd. Pipeline (MAG) |

---

## 2. Die TradFi-Giganten steigen ein

### BlackRock
- **BUIDL** (USD Institutional Digital Liquidity Fund): Gestartet März 2024 auf Ethereum, gewachsen auf **~$3 Mrd.** AUM bis Ende 2025
- Auf 7 Blockchains expandiert (Ethereum, Polygon, Arbitrum, Avalanche, Optimism, Aptos, Solana)
- **Februar 2026:** BUIDL wird auf Uniswap (DeFi-Börse) gelistet — ein historischer Moment: der größte Vermögensverwalter der Welt betritt DeFi
- Larry Fink: *"Tokenisierung wird die nächste Generation der Märkte sein"*

### JPMorgan
- **Onyx Digital Assets:** Hauseigene Blockchain-Plattform
- **TCN (Tokenized Collateral Network):** Tokenisierte Money-Market-Fund-Anteile als Echtzeit-Sicherheiten
- Dezember 2025: Ethereum-basierter tokenisierter Money Fund angekündigt
- Kinexys (ehemals JPM Coin): >$2 Mrd. tägliches Transaktionsvolumen

### Goldman Sachs
- **GS DAP (Digital Asset Platform):** Tokenisierte Anleihen und strukturierte Produkte
- Juli 2025: Partnerschaft mit Bank of New York Mellon für tokenisierte Money-Market-Fund-Anteile
- EIB (Europäische Investitionsbank): Mehrere digitale Bond-Emissionen über GS DAP

### Weitere
- **HSBC:** 24/7 tokenisierte Gold-Token live
- **Franklin Templeton:** BENJI Fund auf Stellar und Polygon
- **Fidelity:** Tokenisierte Money-Market-Produkte in Entwicklung
- **Citibank:** Prognose: Tokenisierung erreicht $4–5 Bio. bis 2030

### Was bedeutet das?
Wenn BlackRock auf Uniswap geht und Nasdaq tokenisierte Aktien handeln will, ist Tokenisierung keine Nische mehr. Die Frage ist nicht ob, sondern wie schnell. Die TradFi-Giganten bringen Legitimität, Kapital und — entscheidend — **regulatorische Zugkraft** mit.

---

## 3. Gesetzgebung: Der entscheidende Faktor

### Die zentrale Erkenntnis

Tokenisierung kann nur funktionieren, wenn sie **gesetzlich durchsetzbare Eigentumsrechte** schafft. Ein Token, der nicht vor Gericht als Eigentumsnachweis anerkannt wird, ist nichts als ein hübsches JPEG. Die regulatorische Landschaft 2025/2026 zeigt ein **Drei-Geschwindigkeiten-Modell:**

### 3.1 USA unter Trump: Vom Feind zum Förderer

Die Kehrtwende unter der Trump-Administration ist dramatisch:

**GENIUS Act (Juli 2025 unterzeichnet)**
- Erstes umfassendes Bundesgesetz für Stablecoins
- Bundesweites Regulierungsframework für Stablecoin-Emittenten
- Anforderungen: Reserven, Audits, finanzielle Integrität
- Schafft Rechtssicherheit für die "Zahlungsschicht" der Tokenisierung

**SEC unter Chairman Paul Atkins (seit 2025)**
- **Paradigmenwechsel:** Von "Regulation by Enforcement" (Gensler) zu proaktiver Regelgebung
- **28. Januar 2026:** SEC veröffentlicht gemeinsame Erklärung dreier Abteilungen zu tokenisierten Wertpapieren — ein de-facto "Playbook" für die Industrie
- Kernaussage: *"Neue Schienen, gleiche Regeln"* — solange Token echte Wertpapiere repräsentieren und Anlegerrechte klar sind, ist die SEC offen für innovative Buchführung via DLT
- **DTC No-Action Letter (Dezember 2025):** Die SEC erlaubt der Depository Trust Company einen **3-Jahres-Pilot**, um Wertpapier-Custody auf Blockchains abzubilden — das Herz der US-Wertpapierabwicklung geht on-chain
- **Nasdaq (Januar 2026):** Beantragt bei der SEC, tokenisierte Aktien auf der Börse handeln zu dürfen

**Market Infrastructure Bill (in Arbeit)**
- Umfassendes Gesetz für digitale Asset-Broker, -Dealer und -Börsen
- Soll klären, wann Krypto-Transaktionen als Wertpapiergeschäfte gelten
- SEC vs. CFTC Zuständigkeit wird definiert
- **Token-Taxonomie:** Digitale Rohstoffe/Netzwerk-Token, Collectibles, Tools (keine Wertpapiere) und tokenisierte Wertpapiere

**Kritische Einschränkung: Accredited Investor Rules**
- Die SEC hat bisher **nicht** angedeutet, die Accredited-Investor-Regeln zu lockern
- Viele tokenisierte Wertpapiere in den USA bleiben auf "akkreditierte Investoren" beschränkt (Einkommen >$200K/Jahr oder Vermögen >$1 Mio.)
- **Das ist der größte Haken für die Demokratisierungs-These in den USA**

### 3.2 Europa: Gründlich, aber langsam

**MiCA (Markets in Crypto-Assets Regulation)**
- Seit 30. Dezember 2024 vollständig in Kraft
- Einheitliche Regeln für alle 27 EU-Staaten
- Drei Kategorien: Asset-Referenced Tokens (ARTs), E-Money Tokens (EMTs), sonstige Crypto-Assets
- **Aber:** MiCA reguliert primär Krypto-Assets, NICHT tokenisierte Wertpapiere — dafür gelten weiterhin MiFID II, Prospektverordnung etc.
- Erste MiCA-Lizenzen: Dezember 2024 (NL), Deutschland führt mit 18 lizenzierten CASPs

**DLT Pilot Regime (EU 2022/858)**
- Sandbox für DLT-basierte Wertpapierabwicklung, **verlängert bis 2026**
- Erlaubt regulierte Piloten für tokenisierte Aktien, Anleihen, Derivate
- **Dezember 2025:** EU-Kommission schlägt **massives Upgrade** vor — größere Volumenlimits, mehr Asset-Klassen, Weg von der Sandbox zur permanenten Infrastruktur

**Deutsches eWpG (Gesetz über elektronische Wertpapiere)**
- Seit Juni 2021 in Kraft — Deutschland war EU-Vorreiter
- Ermöglicht rein digitale Wertpapiere (Schuldverschreibungen, Fondsanteile) ohne physische Urkunde
- Kryptowertpapiere auf DLT möglich
- BaFin reguliert, Roadmap 2025: Digitalisierung der Regulierung
- **2026 Standard:** Viele RWA-Deals werden als elektronische/DLT-Wertpapiere auf lizenzierter Infrastruktur strukturiert

**Schweiz & Liechtenstein**
- **Schweiz:** DLT-Gesetz seit 2021, "Registerwertrechte" direkt on-chain durchsetzbar, SDX (SIX Digital Exchange) operativ
- **Liechtenstein:** Token-Container-Modell (TVTG) — eines der fortschrittlichsten Tokenisierungs-Gesetze weltweit
- Beide: Token issuance möglich, aber **Sekundärmarkt/Listing** problematisch (Liquidität fehlt)

**Luxemburg**
- Traditioneller Fondsstandort, aktiv bei tokenisierten Fonds
- Société Générale / Forge: Tokenisierte Bonds unter luxemburgischem Recht

### 3.3 Asien: Das pragmatische Laboratorium

**Singapur (MAS / Project Guardian)**
- **Project Guardian:** Das wichtigste öffentlich-private Tokenisierungs-Projekt weltweit
- Partnerschaft MAS + JPMorgan, DBS, HSBC, BlackRock, Goldman u.a.
- Bis 2025: **>15 Tokenisierungs-Trials** über 6 Währungen (Fixed Income, FX, Fund Management)
- November 2025: MAS und **Deutsche Bundesbank** unterzeichnen MoU für Cross-Border Tokenisierung
- November 2025: UK Investment Association schließt sich Project Guardian an
- Dezember 2025: Roadmap für operationelle Tokenisierung von Fonds veröffentlicht
- **Stablecoin-Framework** etabliert (vor Hongkong)
- Singapur positioniert sich als *"Global Hub for Tokenization"*

**Hongkong**
- **Digital Bond Program:** Mehrzählige Multi-Währungs-Anleiheemissionen der HKMA
- **Project Ensemble:** Cross-Border Carbon Credits + tokenisierte Assets
- **Stablecoin-Gesetz:** August 2025 in Kraft, erste Lizenzen Anfang 2026
- Hongkong-Singapur: Stiller Aufbau eines **regulierten Token-Korridors** (Forbes, Sep 2025)
- Positionierung als Gateway zwischen China und globalen Märkten

**Japan**
- Pionier bei Security Token Offerings (STOs)
- SBI Holdings, Nomura, MUFG aktiv
- JFSA (Financial Services Agency) hat klaren Rahmen für tokenisierte Wertpapiere
- Cross-Border-Trials mit Singapur und Schweiz (Project Guardian)
- **Retail-Zugang:** Japan erlaubt tokenisierte Immobilien-STOs für Retail-Investoren ab ~$500

**Dubai / UAE**
- **VARA 2.0:** Dubai's Virtual Assets Regulatory Authority
- August 2025: CMA und VARA einigen sich auf **gesamtnationales Framework**
- **Dubai Land Department:** Real-Estate-Tokenization-Pilot mit Prypco Mint — **ausverkauft**, signalisiert echte Nachfrage
- Ziel: **7% des Dubai-Immobilienmarkts tokenisiert bis 2033** (~$16 Mrd.)
- **DIFC Tokenisation Sandbox 2025:** Für regulierte Finanzinstrumente (Fonds, Bonds, Aktien)
- Mavryk: $10 Mrd. UAE Premium Real Estate Pipeline

**Südkorea**
- Security Token Sandbox seit 2023
- Kookmin Bank, Samsung Securities experimentieren mit tokenisierten Bonds
- Regulierung strenger als Singapur/Hongkong

### 3.4 Regulatorischer Vergleich (Zusammenfassung)

| Dimension | USA | Europa (EU) | Singapur | Hongkong | Japan | UAE/Dubai |
|-----------|-----|-------------|----------|----------|-------|-----------|
| **Stablecoin-Gesetz** | ✅ GENIUS Act (Jul 2025) | ✅ MiCA (Dez 2024) | ✅ MAS Framework | ✅ (Aug 2025) | ✅ | ✅ CBUAE |
| **Tokenisierte Wertpapiere** | 🔄 SEC Playbook + DTC Pilot | 🔄 DLT Pilot + eWpG | ✅ Project Guardian | 🔄 Ensemble | ✅ STOs reguliert | 🔄 DIFC Sandbox |
| **Retail-Zugang** | ❌ Accredited Investor | 🔄 Prospektpflicht | ✅ Möglich | 🔄 Limitiert | ✅ Ab ~$500 | ✅ DLD Pilot |
| **Immobilien-Token** | 🔄 Fragmentiert | 🔄 Länderspezifisch | ✅ | 🔄 | ✅ | ✅ DLD Pilot |
| **DeFi-Integration** | ✅ (BlackRock/Uniswap) | ❌ Unklar | 🔄 Vorsichtig | ❌ | ❌ | 🔄 |
| **Cross-Border** | 🔄 | ✅ EU-Passport | ✅ MoU mit DE, UK | ✅ Korridor mit SG | ✅ Trials | 🔄 |
| **Geschwindigkeit** | 🚀 Beschleunigend | 🐢 Gründlich, langsam | 🚀 Pragmatisch | 🏃 Aufholend | 🏃 Stetig | 🚀 Aggressiv |

*✅ = In Kraft / Klar | 🔄 = In Arbeit / Pilotphase | ❌ = Fehlend / Unklar*

---

## 4. Die Gretchenfrage: Demokratisierung oder neue Exklusivität?

### Das Versprechen

Die Vision ist verlockend: Wenn ein Münchner Wohnhaus mit Wert €5 Mio. in 50.000 Token à €100 aufgeteilt wird, kann jeder mitmachen. Kein Mindestinvestment von €500.000, keine exklusiven Private-Equity-Clubs, keine Wartelisten. Immobilien, Venture Capital, Private Equity, Infrastruktur, Kunst — alles wird investierbar, für jeden, überall, 24/7.

**Konkretes Beispiel:** Hamilton Lane — einer der größten Private-Equity-Verwalter der Welt (~$920 Mrd. AUM) — hat über Securitize Fonds tokenisiert und das Mindestinvestment von **$5 Mio. auf $20.000** gesenkt. RealT verkauft Anteile an US-Mietimmobilien ab **$50 pro Token** mit wöchentlichen Mietausschüttungen.

### Die Realität (kritische Perspektive)

**1. Accredited Investor Problem (USA)**
In den USA dürfen die meisten tokenisierten Wertpapiere weiterhin nur an "akkreditierte Investoren" verkauft werden (Vermögen >$1 Mio. oder Einkommen >$200K). Solange sich das nicht ändert, bleibt die Demokratisierung in den USA eine Illusion. Die Trump-SEC hat hier bisher **keine Lockerung signalisiert**.

**2. Prospektpflicht (Europa)**
In der EU erfordern tokenisierte Wertpapiere über bestimmten Schwellwerten einen vollständigen Prospekt — teuer und aufwändig. Für kleine Emissionen (unter €8 Mio.) gibt es Ausnahmen, aber diese limitieren die Skalierung.

**3. Liquiditätsproblem**
Tokenisierung schafft nicht automatisch Liquidität. Ein Token für ein Nischen-Immobilienprojekt kann genau so illiquide sein wie die Immobilie selbst. Sekundärmärkte sind fragmentiert — der Canton Network Report 2026 dokumentiert **1–3% Preisunterschiede** für identische Assets auf verschiedenen Chains und **2–5% Friktionskosten** bei Cross-Chain-Transfers.

**4. Neue Gatekeeping-Mechanismen**
- BlackRock BUIDL erfordert weiterhin KYC/AML und akkreditierte Investoren
- Viele institutionelle Plattformen haben Mindestinvestments ($100K+)
- Die "permissioned DeFi" Bewegung (Aave Arc, Compound Treasury) schafft separate Pools nur für Institutionelle
- **Risk:** Die gleichen TradFi-Gatekeepers, die die alten Barrieren gebaut haben, bauen jetzt die neuen

**5. Historische Parallele: Robinhood**
Die "Demokratisierung" des Aktienhandels durch Robinhood hat gezeigt: Zugang allein reicht nicht. Ohne finanzielle Bildung und regulatorischen Schutz können Kleinanleger durch Fractional Investing und 24/7-Handel *mehr* verlieren als zuvor. Payment for Order Flow, Gamification, Meme-Stocks.

### Ehrliche Einschätzung

Die Wahrheit liegt in der Mitte:

**Für Kleinanleger wird sich vieles verbessern:**
- Zugang zu bisher verschlossenen Asset-Klassen (Private Credit, Infrastruktur, Immobilien in anderen Ländern)
- Niedrigere Mindestinvestments (von $5 Mio. auf $20K bei PE, von $500K auf $50 bei Immobilien)
- 24/7-Handel und schnellere Settlement-Zeiten
- Automatische Dividenden via Smart Contracts
- Bessere Diversifikation über Asset-Klassen

**Aber die Reichen werden weiterhin Vorteile haben:**
- Erstallokationen und beste Deals fließen zuerst an institutionelle Investoren
- Regulatorische Hürden (Accredited Investor) bleiben in den USA
- Liquiditätsprämien gehen an die, die große Volumes handeln
- Die "ertragreichsten" Investments (Tier-1 VC, Trophy Assets) werden tokenisiert, aber zu Konditionen, die weiterhin bevorzugt die Großen bedienen

**Die bessere Metapher:** Tokenisierung ist nicht die Revolution, die Reichtum umverteilt. Sie ist wie die Erfindung des Buchdrucks: Das Wissen wurde zugänglicher, aber wer die Druckpressen besaß, wurde noch mächtiger. Mehr Menschen können teilhaben — aber die Architekten des Systems werden überproportional profitieren.

---

## 5. Tokenisierung × Maschinenökonomie: Die Convergence-Thesis-Dimension

Hier wird es für das Buch besonders relevant:

### KI-Agenten als Investoren
Wenn autonome KI-Agenten Portfolios managen (was bereits geschieht — siehe Autonolas, Virtuals Protocol), brauchen sie programmatisch handelbare Assets. Tokenisierte Wertpapiere sind die einzige Asset-Klasse, die ein Agent ohne menschliche Intermediäre kaufen, halten und verkaufen kann.

### Machine-to-Machine Commerce
Ein selbstfahrendes Taxi, das seine eigene Wartung bezahlt, seine Versicherung tokenisiert und Anteile an seinem Umsatz als Token verkauft — das ist die logische Verlängerung von "Maschinen brauchen Maschinengeld".

### Smart Contracts als automatische Compliance
KI + Smart Contracts = automatische regulatorische Compliance. Die KI prüft, ob ein Investor die Voraussetzungen erfüllt, der Smart Contract vollstreckt die Regeln, die Blockchain dokumentiert alles unveränderlich.

### Das fehlende Kapitel
Tokenisierung ist das **Bindeglied** zwischen:
- Kapitel 3 (Warum Maschinen Krypto brauchen) → Tokenisierung macht *alle* Assets maschinenlesbar
- Kapitel 7 (Regulierung) → Tokenisierung ist der regulatorische Frontline-Konflikt
- Kapitel 11 (Barbell-Strategie) → Tokenisierung eröffnet völlig neue Allokationsmöglichkeiten

---

## 6. Empfehlung für "Maschinengeld"

### Option A: Eigenes Kapitel (EMPFOHLEN)

**Kapitel 3b: "Wenn alles ein Token wird — Die Demokratisierung (und ihre Grenzen)"**

Platzierung: zwischen Kapitel 3 (Warum Maschinen Krypto brauchen) und Kapitel 4 (Geopolitik). Es wäre die natürliche Brücke: Kapitel 3 erklärt *warum* Maschinen Krypto brauchen, Kapitel 3b erklärt *wie* die reale Welt auf die Blockchain kommt.

**Vorgeschlagene Struktur (~7.000 Wörter):**
1. Die Vision: Wenn alles tokenisiert ist
2. Was heute schon passiert (Zahlen, Beispiele)
3. Die TradFi-Invasion: Wenn BlackRock DeFi betritt
4. Gesetzgebung: Der Drei-Geschwindigkeiten-Wettlauf (USA/Europa/Asien)
5. Demokratisierung oder Illusion? — Eine ehrliche Analyse
6. Tokenisierung × Maschinenökonomie: Die Synthese
7. Was das für Investoren bedeutet

### Option B: Verteilung auf bestehende Kapitel

- **Kapitel 3** (3.4 oder 3.5): RWA-Tokenisierung als Erweiterung der Krypto-These
- **Kapitel 7** (7.4): Tokenisierungs-Regulierung als Teil des Regulierungskapitels
- **Kapitel 11** (11.3.5): Tokenisierte Assets als Investmentkategorie

**Empfehlung: Option A.** Das Thema ist zu groß und zu zentral für die Gesamtthese, um es auf Unterkapitel zu verteilen. Es verdient seinen eigenen Raum.

---

## Quellen (Auswahl)

- Canton Network / RWA.io: "State of RWA Tokenization 2026" (Dez 2025)
- CoinDesk: "RWA Tokenization Market Has Grown Almost Fivefold" (Jun 2025)
- Chainalysis: "2025 Crypto Regulatory Round-Up" (Dez 2025)
- Sidley Austin: "SEC Staff Unveils a Playbook for Tokenized Securities" (Jan 2026)
- The Block: "Crypto regulation in 2026: SEC's ambitious agenda" (Dez 2025)
- Cleary Gottlieb: "2026 Digital Assets Regulatory Update" (Jan 2026)
- Fireblocks: "5 Key Digital Asset Policy Changes in 2025" (Dez 2025)
- Forbes: "Hong Kong-Singapore Are Quietly Building A Regulated Token Corridor" (Sep 2025)
- Deloitte: "Digital Dividends: Tokenized Real Estate" (Dez 2025)
- BDO: "Tokenization Trends for Real-World Assets in 2026" (Feb 2026)
- Federal Register: Nasdaq Proposed Rule Change for Tokenized Securities (Jan 2026)
- CoinTelegraph: "How crypto laws changed in 2025" (Jan 2026)
- Ledger Insights: "EU Commission floats major DLT Pilot Regime upgrade" (Dez 2025)
- Kroll: "Crypto Comes of Age in 2025" (Jan 2026)
