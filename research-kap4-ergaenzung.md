# Research-Report: Kapitel 4 Ergänzungen — Maschinengeld

**Erstellt:** 24. Februar 2026  
**Themen:** Meta Llama EU-Verbot | MiCA & Stablecoin-Zinsen | MiCA Token-Regulierung | Chip-Krieg Vertiefung | Indien als KI-Player

---

## Thema 1: Meta Llama EU-Verbot — Europa als KI-Wüste zweiter Klasse

### Chronologie der Sperrungen

**Juli 2024 — Die erste Ankündigung:**  
Am 17. Juli 2024 gab Meta in einem Statement gegenüber Axios bekannt, dass es seine kommenden multimodalen KI-Modelle nicht in der EU veröffentlichen werde. Das exakte Zitat:

> *"We will release a multimodal Llama model over the coming months — but not in the EU due to the unpredictable nature of the European regulatory environment."*

Zu diesem Zeitpunkt war Llama 3.1 (nur Text) gerade erschienen und wurde in der EU normal verfügbar gemacht. Die Sperre betraf ausschließlich die geplanten **multimodalen Versionen** — also Modelle, die neben Text auch Bilder verarbeiten können.

**September 2024 — Llama 3.2 erscheint:**  
Mit der Veröffentlichung von Llama 3.2 im September 2024 wurde die Sperre konkret und lizenzrechtlich verankert. Die Llama 3.2 Community License Agreement enthält explizit folgende Klausel:

> *"With respect to any multimodal models included in Llama 3.2, the rights granted under Section 1(a) are not being granted to you if you are an individual domiciled in, or a company with a principal place of business in, the European Union."*

Das bedeutet: Die **textbasierten Modelle** von Llama 3.2 (1B und 3B Parameter) durften von EU-Bürgern genutzt werden. Die **Vision-Modelle** (11B und 90B, die Bilder verarbeiten) waren explizit ausgeschlossen.

**April 2025 — Llama 4 erweitert die Sperre:**  
Als Meta im April 2025 die Llama-4-Familie veröffentlichte — Llama 4 Scout, Llama 4 Maverick — waren **alle Modelle multimodal**. Es gab keine rein textbasierten Versionen mehr. Die gleiche EU-Ausschlussklausel blieb in der Lizenz. Damit war **die gesamte Llama-4-Generation für EU-Bürger und -Unternehmen gesperrt**.

### Welche Modelle sind betroffen — Übersicht

| Modell | Release | Multimodal? | EU-Status |
|--------|---------|-------------|-----------|
| Llama 3.1 (8B/70B/405B) | Juli 2024 | Nein (nur Text) | ✅ Erlaubt |
| Llama 3.2 (1B/3B Text) | Sept. 2024 | Nein | ✅ Erlaubt |
| Llama 3.2 (11B/90B Vision) | Sept. 2024 | Ja | ❌ Gesperrt |
| Llama 3.3 (70B) | Dez. 2024 | Nein (nur Text) | ✅ Erlaubt |
| Llama 4 Scout | April 2025 | Ja (alle) | ❌ Gesperrt |
| Llama 4 Maverick | April 2025 | Ja (alle) | ❌ Gesperrt |

### Offizieller Grund

Meta nannte offiziell die **"unpredictable nature of the European regulatory environment"** als Grund. Im Detail spielen zwei regulatorische Rahmenwerke eine Rolle:

1. **DSGVO (GDPR):** Multimodale Modelle, die Bilder verarbeiten, müssen mit Bilddaten trainiert worden sein. Die DSGVO stellt strenge Anforderungen an die Verarbeitung personenbezogener Daten. Meta hatte bereits 2024 Probleme, als die irische Datenschutzbehörde (DPC) das Training von KI-Modellen mit Facebook- und Instagram-Nutzerdaten stoppte. Die Verwendung von Bildern europäischer Nutzer für das KI-Training wurde als besonders problematisch eingestuft.

2. **EU AI Act:** Der im August 2024 in Kraft getretene AI Act stellt zusätzliche Anforderungen an KI-Systeme, insbesondere an sogenannte "General Purpose AI Models" (GPAI). Multimodale Modelle fallen potenziell in Hochrisiko-Kategorien.

Meta hat nie spezifiziert, welches einzelne Gesetz die Sperre ausgelöst hat. Die Formulierung "regulatory environment" deutet auf eine **Kombination beider Regelwerke** hin — und möglicherweise auch auf eine bewusste politische Botschaft an die EU-Regulierer.

### Auswirkungen auf europäische Unternehmen und Entwickler

Die Sperre trifft besonders hart, weil Llama als **Open-Source-Alternative** zu proprietären Modellen wie GPT-4 oder Claude galt:

- **Startups**, die auf Llama-basierte multimodale Anwendungen setzten, mussten auf andere Modelle ausweichen oder VPN-basierte Workarounds nutzen
- **Unternehmen**, die Vision-Fähigkeiten für Dokumentenverarbeitung, medizinische Bildanalyse oder industrielle Qualitätskontrolle benötigten, verloren Zugang zu einem der leistungsfähigsten offenen Modelle
- **Cloud-Hoster** mit Sitz in der EU können die gesperrten Modelle nicht offiziell anbieten
- Mit Llama 4 verschärft sich das Problem: Da **alle** Llama-4-Modelle multimodal sind, haben EU-Entwickler keinen legalen Zugang zur neuesten Generation

### Workarounds und Grauzone

In der Praxis existieren diverse Workarounds:

- Die Modell-Gewichte sind auf Hugging Face und anderen Plattformen frei herunterladbar. Die Lizenz ist ein **vertraglicher Ausschluss**, keine technische Sperre — es gibt keinen DRM-Schutz
- Viele EU-Entwickler laden die Modelle einfach herunter und nutzen sie trotzdem. Die Durchsetzbarkeit der Lizenzklausel ist rechtlich umstritten
- Einige argumentieren, dass die Klausel gegen EU-Recht (Diskriminierungsverbot im digitalen Binnenmarkt) verstoßen könnte
- Plattformen wie Hugging Face (Sitz in Frankreich!) hosten die Modelle weiterhin

Ein Blogpost von Sara Zan (Mai 2025) fasst die Situation pointiert zusammen: Die Sperre sei primär eine **Lizenz-Einschränkung**, keine technische Barriere. Wer die Modelle herunterlädt und in der EU nutzt, verstößt zwar gegen die Lizenzbedingungen, aber ob Meta dies je durchsetzen würde (oder könnte), ist fraglich.

### Andere US-Unternehmen mit EU-Einschränkungen

Meta ist kein Einzelfall:

- **Apple:** Verzögerte den Launch von Apple Intelligence in der EU zunächst komplett (Juni 2024), unter Berufung auf den Digital Markets Act (DMA). Features wie iPhone Mirroring und SharePlay Screen Sharing wurden für EU-Nutzer gesperrt. Apple argumentierte, der DMA zwinge sie, Features auf Nicht-Apple-Geräten funktionsfähig zu machen, bevor sie sie launchen dürfen. Bis Februar 2026 sind einige Apple-Intelligence-Features wie Live Activities und bestimmte Siri-Funktionen in der EU immer noch eingeschränkt.
- **Google:** Verzögerte ebenfalls einige KI-Features für die EU
- **OpenAI:** Hat bestimmte Features wie das Gedächtnis-Feature von ChatGPT in der EU später ausgerollt

### Bedeutung für die Convergence Thesis

Die Meta-Llama-Sperre ist ein Paradebeispiel für die **regulatorische Divergenz**, die Europa im KI-Wettlauf zurückwirft. Während US-Entwickler Zugang zu den neuesten offenen Modellen haben und chinesische Entwickler mit DeepSeek und Qwen eigene Alternativen besitzen, werden europäische Entwickler durch eine Kombination aus Regulierung und vorauseilendem Gehorsam der Tech-Konzerne systematisch benachteiligt.

---

## Thema 2: MiCA und Stablecoin-Zinsen — Wie die EU Rendite verbietet

### Was MiCA zu Stablecoins und Zinsen sagt

MiCA (Markets in Crypto-Assets Regulation) klassifiziert Stablecoins in zwei Kategorien:
- **Asset-Referenced Tokens (ARTs):** An einen Korb von Vermögenswerten gebunden
- **E-Money Tokens (EMTs):** An eine einzelne Fiat-Währung gebunden (z.B. USDC, USDT)

**Artikel 50 MiCA** enthält das entscheidende Verbot: Emittenten von E-Money-Tokens und Krypto-Asset-Dienstleister dürfen den Haltern dieser Token **keine Zinsen gewähren**. Dieses Verbot gilt auch für Asset-Referenced Tokens (Artikel 40).

Die Logik dahinter: E-Money-Tokens sollen als **Zahlungsmittel** dienen, nicht als Sparanlage. Sie sollen keine Einlagen im bankaufsichtsrechtlichen Sinne sein. Ein Zinsverbot soll verhindern, dass Stablecoins zu unregulierten Bankprodukten werden.

### Coinbase beendet USDC Rewards für EU-Bürger

**28. November 2024:** Coinbase schickte eine E-Mail an alle EEA-Kunden (Europäischer Wirtschaftsraum), die besagte, dass das **USDC Rewards Program ab dem 1. Dezember 2024 eingestellt** wird.

Ein Coinbase-Sprecher erklärte gegenüber DL News:

> *"Under MiCA, Coinbase is required to terminate the USDC rewards programme for EEA customers beginning December 1, 2024."*

Bemerkenswert: Coinbase konnte (oder wollte) nicht spezifizieren, welche **exakte MiCA-Regelung** die Einstellung erzwingt. Kritiker bemerkten, dass Coinbase pauschal auf "MiCA" verwies, ohne Artikel 50 direkt zu benennen.

### Zinssätze: Was US-Bürger erhalten, was EU-Bürgern verwehrt wird

| Plattform | Produkt | US-Rate (APY) | EU-Rate (APY) |
|-----------|---------|---------------|---------------|
| Coinbase | USDC Rewards | 4,35–5,2% | **0%** (seit 1. Dez. 2024) |
| Coinbase Wallet | USDC on Base | 4,7% | **Nicht verfügbar für EEA** |

Zum Zeitpunkt der Einstellung bot Coinbase US-Kunden eine Rendite von ca. **4,7–5,2% APY** auf USDC-Bestände. EU-Kunden erhielten von einem Tag auf den anderen **null**. Bei einem USDC-Bestand von 10.000 USD bedeutet das einen jährlichen Verlust von 470–520 USD an passivem Einkommen.

### Tether (USDT) — Das größere MiCA-Problem

Während Coinbase die Zinsen einstellte, traf es Tether/USDT noch härter:

- **Tether hat keine MiCA-Lizenz beantragt** und keine Autorisierung als E-Money-Token-Emittent in der EU erhalten
- Mehrere europäische Börsen haben USDT **delistet**:
  - **OKX** war die erste große Börse, die USDT-Handelspaare in der EU einstellte
  - **Crypto.com** delistete USDT und 9 weitere Tokens bis zum 31. Januar 2025
  - **Coinbase** delistete ebenfalls nicht-MiCA-konforme Stablecoins
- Tether stellte sogar seinen eigenen **Euro-Stablecoin (EUR€) Ende 2024 ein** — offenbar wollte man sich nicht dem MiCA-Regime unterwerfen
- Ab **1. Juli 2025** ist USDT auf regulierten europäischen Börsen und für Unternehmenstransaktionen de facto verboten

Dies ist bemerkenswert, weil USDT **der mit Abstand größte Stablecoin der Welt** ist (Marktkapitalisierung über 139 Mrd. USD). In Europa, wo Stablecoins über 58% des Krypto-Transaktionsvolumens ausmachten, entsteht eine massive Liquiditätslücke.

**Gewinner:** Circle (USDC-Emittent) hat eine MiCA-Lizenz erhalten und bietet auch den Euro-Stablecoin EURC an, der bereits über 287 Mio. EUR in Umlauf hat — mehr als die Hälfte des gesamten Euro-Stablecoin-Marktes.

### Kritik und Reaktionen

Der sarkastische Tweet eines europäischen Krypto-Entwicklers (Mikko Ohtamaa, @moo9000) nach der Coinbase-Ankündigung:

> *"I feel protected"*

Marina Markezic, eine bekannte europäische Krypto-Lobbyistin, kommentierte die Entscheidung mit dem Hinweis, MiCA führe dazu, dass europäische Nutzer systematisch schlechter gestellt werden als ihre amerikanischen Counterparts.

**Robert Kopitsch**, Mitgründer von Blockchain for Europe (zu dessen Vorstand Vertreter von Coinbase, Binance und Ripple gehören), kritisierte im Dezember 2024:

> *"The implementation of MiCA into national law is not going the way it should."*

### Vergleich: Was US-Bürger können, was EU-Bürger nicht können

| Feature | USA | EU (nach MiCA) |
|---------|-----|-----------------|
| USDC-Zinsen (Coinbase) | ✅ 4,35–5,2% APY | ❌ Verboten |
| USDT halten/handeln | ✅ Auf allen Börsen | ❌ Von regulierten Börsen delistet |
| Stablecoin-Lending (DeFi) | ✅ Weitgehend unreguliert | ⚠️ Regulatorische Grauzone |
| Stablecoin-Vielfalt | ✅ USDC, USDT, DAI, etc. | ⚠️ Nur MiCA-konforme (USDC, EURC) |
| Yield Farming | ✅ Frei verfügbar | ⚠️ Rechtlich unsicher |

---

## Thema 3: MiCA Token-Regulierung und Innovation

### Konkrete Anforderungen für Token-Issuance unter MiCA

MiCA unterscheidet drei Kategorien von Crypto-Assets mit unterschiedlichen Anforderungen:

#### 1. "Other Crypto-Assets" (Utility Tokens, Governance Tokens etc.)
- **Whitepaper-Pflicht:** Jeder Token-Emittent muss ein detailliertes Krypto-Asset-Whitepaper gemäß Artikel 6 MiCA erstellen und veröffentlichen
- **Inhaltspflichten des Whitepapers:**
  - Beschreibung des Emittenten und des Projekts
  - Beschreibung des Crypto-Assets und seiner Technologie
  - Rechte und Pflichten der Halter
  - Risikobeschreibung
  - Angaben zur zugrunde liegenden Technologie (Blockchain, Konsensmechanismus)
- **Notifizierung:** Das Whitepaper muss der zuständigen nationalen Aufsichtsbehörde (z.B. BaFin in Deutschland) **20 Tage vor Veröffentlichung** vorgelegt werden
- **Haftung:** Der Emittent haftet für die Richtigkeit der Angaben im Whitepaper
- **Keine Zulassungspflicht**, aber Registrierungspflicht

#### 2. Asset-Referenced Tokens (ARTs)
- **Autorisierungspflicht:** Emittenten müssen eine regulatorische Lizenz in einem EU-Mitgliedsstaat erhalten
- **Kapitalanforderungen:** Eigenmittel von mindestens 350.000 EUR oder 2% des durchschnittlichen Reservenvermögens (je nachdem, was höher ist)
- **Reserve-Anforderungen:** Vollständige Unterlegung mit liquiden Vermögenswerten
- **Regelmäßige Audits** der Reserven
- **Transparenzberichte**
- Bei **"signifikanten" ARTs** (über 5 Mrd. EUR oder 10 Mio. Nutzer): Zusätzliche strengere Anforderungen, Beaufsichtigung durch die Europäische Bankenaufsichtsbehörde (EBA)

#### 3. E-Money Tokens (EMTs / Stablecoins)
- **Autorisierung als Kreditinstitut oder E-Geld-Institut** erforderlich
- **Vollständige 1:1-Besicherung** mit Fiat-Währungsreserven
- **Zinsverbot** (Artikel 50)
- **Transaktionslimits** für Nicht-Euro-Stablecoins
- Regelmäßige Audits

### Wie betrifft das innovative Modelle?

#### Open-Source-Contribution-Tokens
Tokens, die als Belohnung für Beiträge zu Open-Source-Projekten ausgegeben werden (ähnlich Gitcoin):
- Fallen unter die Kategorie "Other Crypto-Assets"
- **Whitepaper-Pflicht** für jedes Projekt, das Tokens emittiert — selbst wenn es ein kleines Open-Source-Projekt ist
- Der Whitepaper-Erstellungsprozess erfordert juristische Expertise, die für ehrenamtliche Open-Source-Projekte oft nicht vorhanden oder finanzierbar ist
- **Haftungsrisiko** für den Emittenten

#### Community Tokens / Governance Tokens
- Governance-Tokens, die Stimmrechte in DAOs verleihen, fallen unter MiCA, wenn sie **übertragbar** und auf einem Handelsplatz **handelbar** sind
- Die Whitepaper-Pflicht gilt auch hier
- Problematisch: Viele Governance-Token-Modelle basieren darauf, dass Tokens an Community-Mitglieder **kostenlos verteilt** werden (Airdrops). Unter MiCA muss trotzdem ein Whitepaper erstellt werden.

#### Utility Tokens für Plattformen
- Auch Utility Tokens (z.B. Zugangs-Tokens für eine Plattform) unterliegen MiCA, sofern sie übertragbar sind
- **Ausnahme:** Tokens, die ausschließlich zur Nutzung eines Dienstes berechtigen und **nicht übertragbar** sind, fallen nicht unter MiCA
- In der Praxis sind die meisten Utility Tokens aber auf Blockchains implementiert und damit inhärent übertragbar

### Gibt es Ausnahmen für kleine Token-Emissionen?

MiCA sieht einige Ausnahmen vor:
- **Kostenlose Tokens:** Krypto-Assets, die automatisch als Belohnung für die Aufrechterhaltung eines DLT-Netzwerks oder die Validierung von Transaktionen generiert werden (z.B. Mining-Rewards), sind ausgenommen
- **Kleine Angebote:** Angebote, die sich an weniger als 150 Personen pro Mitgliedsstaat richten, sind teilweise ausgenommen
- **Angebote unter 1 Million EUR** in einem 12-Monats-Zeitraum sind von einigen Anforderungen befreit
- **NFTs:** Echte, einzigartige Non-Fungible Tokens sind von MiCA ausgenommen, aber NFTs, die "in großen Serien oder Sammlungen" herausgegeben werden, gelten als fungibel und fallen unter MiCA

### Projekte, die die EU verlassen oder Token-Pläne aufgegeben haben

Konkrete Beispiele für einen "Krypto-Exodus" aus der EU:

- **Estland**, das jahrelang als europäisches Krypto-Paradies galt (mit über 1.000 Krypto-Lizenzen), hat die meisten davon widerrufen. Viele Firmen sind in die Schweiz, nach Dubai oder in die Karibik abgewandert
- Laut einem Bericht von eestifirma.ee ist Europa als Standort für Blockchain-Entwicklung bis 2024 "signifikant zurückgegangen"
- Mehrere DeFi-Projekte haben angekündigt, EU-Nutzer von bestimmten Funktionen auszuschließen, anstatt MiCA-Compliance-Kosten zu tragen
- Die **Übergangsfristen** (bis Juli 2026 für bestehende Dienstleister) sorgen für zusätzliche Unsicherheit

### Vergleich mit USA

Die USA haben **kein einheitliches Krypto-Regulierungsrahmenwerk** wie MiCA. Die Situation:

| Aspekt | EU (MiCA) | USA |
|--------|-----------|-----|
| Einheitliches Rahmenwerk | ✅ Ja (seit Dez. 2024) | ❌ Nein (fragmentiert, SEC/CFTC/Staaten) |
| Whitepaper-Pflicht | ✅ Obligatorisch | ❌ Nicht vorgeschrieben |
| Token-Emittenten-Lizenz | ✅ Für ARTs und EMTs | ⚠️ Fallweise (SEC-Registrierung möglich) |
| Zinsverbot auf Stablecoins | ✅ Ja (Art. 50) | ❌ Nein |
| Stablecoin-Emittenten | Nur lizenzierte E-Geld-Institute | Noch nicht reguliert (Stablecoin-Gesetz in Arbeit) |
| Kosten für Compliance | Hoch (350.000 EUR+ für ARTs) | Variabel, oft geringer |
| Regulatorische Klarheit | ✅ Hoch | ❌ Gering (ständige Gerichtsverfahren) |

**Paradox:** MiCA bietet mehr Rechtssicherheit als die USA, aber die Kosten und Einschränkungen sind so hoch, dass viele innovative Projekte lieber in der regulatorischen Grauzone der USA operieren, wo sie de facto mehr Freiheiten haben.

### Kritik aus der europäischen Blockchain-Community

- **Blockchain for Europe** kritisiert die uneinheitliche Umsetzung in den Mitgliedsstaaten
- Viele Branchenteilnehmer bemängeln, dass MiCA **zu strenge prudentielle Standards** setzt, die über vergleichbare Regulierungen in den USA und UK hinausgehen
- Die **Whitepaper-Pflicht** wird als unverhältnismäßige Bürde für kleine Projekte kritisiert
- Das **Zinsverbot** für Stablecoins wird als innovationsfeindlich angesehen — es bestraft europäische Nutzer, ohne einen erkennbaren Sicherheitsgewinn
- ESMA und EBA werden für **langsame und widersprüchliche technische Standards** kritisiert

---

## Thema 4: Chip-Krieg — Vertiefung

### TSMC Arizona: Die teuerste Fabrik der Welt

#### Aktuelle Zahlen
- **Gesamtinvestition:** 165 Milliarden USD (ursprünglich 12 Mrd., dann 40 Mrd., dann 65 Mrd., jetzt 165 Mrd.)
- **CHIPS-Act-Förderung:** 6,6 Milliarden USD direkte Zuschüsse, finalisiert im November 2024 unter Biden
- **Zusätzlich:** Milliarden in zinsgünstigen Krediten und Steuervorteilen

#### Die drei (jetzt sechs) Fabs
| Fab | Technologie | Produktionsstart | Status |
|-----|-------------|------------------|--------|
| Fab 21 (erste) | 4nm (urspr. 5nm) | H1 2025 | In Produktion |
| Fab 2 | 2nm / 3nm | 2028 | Im Bau |
| Fab 3 | 2nm oder kleiner | Ende Dekade | Im Bau (seit April 2025) |
| Fabs 4-6 | Fortschrittlich | Nach 2030 | Angekündigt (März 2025) |

#### Die 100-Milliarden-Expansion (März 2025)
Am 4. März 2025 kündigte TSMC eine zusätzliche Investition von **100 Milliarden USD** an — die größte ausländische Direktinvestition in der US-Geschichte. Damit sollen drei weitere Fabs, zwei Packaging-Anlagen und ein Forschungszentrum in Arizona entstehen. Trump inszenierte die Ankündigung als persönlichen Verhandlungserfolg.

Die Expansion wurde teilweise durch die **Zolldrohungen** der Trump-Administration motiviert: TSMC-Chips, die in den USA produziert werden, wären von Importzöllen auf taiwanische Halbleiter nicht betroffen. TSMC schätzt, dass bis zu **30% der Produktion auf 2nm und fortschrittlicheren Nodes** in den USA stattfinden wird.

#### Verzögerungen und Probleme
- Die erste Fab (Fab 21) war **ursprünglich für Ende 2024** geplant, wurde auf H1 2025 verschoben
- **Hauptgrund:** Mangel an qualifizierten Arbeitskräften. TSMC-Mitarbeiter aus Taiwan berichteten, dass amerikanische Techniker deutlich weniger Erfahrung mit den komplexen Fertigungsprozessen hatten
- Kulturelle Konflikte: TSMCs berüchtigte 12-Stunden-Schichten und Wochenendarbeit stießen bei amerikanischen Arbeitern auf Widerstand
- **Kosten:** Die Chipproduktion in Arizona ist schätzungsweise **30-50% teurer** als in Taiwan

### Intel: Vom Giganten zum Patienten

#### Die Krise in Zahlen
- **Aktienkurs:** Fiel unter Gelsinger um über 60%, während Nvidia um über 200% stieg
- **Foundry-Verluste:** Die Intel Foundry Division verzeichnete im Q3 2024 einen operativen Verlust von **5,8 Milliarden USD** — bei Umsatzrückgängen von 8%
- **Massenentlassungen:** Im August 2024 kündigte Gelsinger die Streichung von **15.000 Arbeitsplätzen** (15% der Belegschaft) an
- **Marktkapitalisierung:** Sank auf einen Bruchteil von Nvidia (Nvidia: 3,35 Billionen USD)

#### Pat Gelsingers Abgang
Am **1. Dezember 2024** gab Intel bekannt, dass CEO Pat Gelsinger "in den Ruhestand tritt" — effektiv sofort. Tatsächlich wurde er vom Board **zum Rücktritt gedrängt**, nachdem das Vertrauen in seinen Turnaround-Plan schwand.

**Ironie:** Gelsinger ging nur **eine Woche** nachdem Intel eine CHIPS-Act-Förderung von **7,86 Milliarden USD** zugesichert bekommen hatte — die größte Einzelförderung des Programms.

#### Der neue CEO: Lip-Bu Tan
**Lip-Bu Tan**, ehemaliger CEO von Cadence Design Systems und langjähriges Intel-Boardmitglied, übernahm als CEO. Seine bisherige Bilanz:
- **Weitere Entlassungen:** Unter Tan wurden nochmals über **20% der Belegschaft** abgebaut, darunter 10.000 Foundry-Arbeiter im Juli 2025 — ohne Abfindung
- **Foundry-Krise:** Tan signalisierte im Juli 2025, dass Intel die Foundry-Sparte möglicherweise aufgeben könnte, wenn keine externen Kunden gewonnen werden. Der Aktienkurs fiel daraufhin um 8%
- **18A-Prozess:** Intels kommender 18A-Prozessknoten (vergleichbar mit TSMCs 2nm) steht unter Druck. Tan erklärte, man brauche externe Kundenaufträge, um die Entwicklung fortzusetzen
- **Intel Foundry 2025:** Die Sparte generierte 4,5 Mrd. USD Umsatz bei 2,5 Mrd. USD operativem Verlust

#### CHIPS Act Geld für Intel
Intel ist der **größte Einzelempfänger** des CHIPS Act:
- **7,86–7,9 Milliarden USD** direkte Förderung
- **Bis zu 11 Milliarden USD** in zinsgünstigen Krediten
- Für Fabriken in Arizona, New Mexico, Ohio und Oregon
- Bis September 2025 waren 5,7 Mrd. USD tatsächlich ausgezahlt

### Samsung: Der strauchelnde Zweite

#### Das Yield-Problem
Samsung war einer der **ersten Hersteller**, die 3nm-Chips in Massenproduktion brachten (2022, mit Gate-All-Around / GAA-Transistoren). Aber die Ausbeute (Yield) bleibt katastrophal:

- **Samsungs 3nm Yield (2025): ~50%** — nach drei Jahren Massenproduktion
- **TSMCs 3nm Yield: >90%**

Das bedeutet: Von einem Wafer voller Samsung-3nm-Chips ist jeder zweite defekt. Bei TSMC sind 9 von 10 funktionsfähig.

#### Kundenverluste
Die niedrigen Yields haben Samsung massiv Kunden gekostet:
- **Qualcomm** wechselte für Flaggschiff-Chips zu TSMC
- **Nvidia** nutzt ausschließlich TSMC
- **Google** wechselte für die Tensor-Chips von Samsung zu TSMC
- Samsung konnte seinen eigenen Exynos 2500 (für Galaxy-Phones) 2025 nur in limitierter Stückzahl produzieren
- **Samsungs Foundry-Marktanteil: 9,3% (Q3 2024)** — gegenüber TSMCs ~60%

#### 2nm-Hoffnung
Samsung kündigte an, Ende 2025 mit der Massenproduktion von **2nm-Chips** zu beginnen, vorerst für eigene Produkte (Exynos-Prozessoren). Der Ausgang ist ungewiss — ob Samsung die Yield-Probleme auf 2nm lösen kann, wird über die Zukunft der Foundry-Sparte entscheiden.

#### Überraschung: Elon Musk setzt auf Samsung
Im November 2025 sicherte sich **xAI/Tesla** einen 16,5-Milliarden-USD-Vertrag mit Samsung für KI-Chip-Fertigung — vermutlich, weil Musks Unternehmen bei TSMC nicht die gewünschte Priorität und Kontrolle erhielten. Musk will direkt in den Fertigungsprozess eingebunden sein, was TSMC (wo Nvidia und Apple über 40% des Umsatzes ausmachen) nicht bietet.

### US CHIPS Act: Das Gesamtbild

Der CHIPS and Science Act wurde im August 2022 von Biden unterzeichnet und autorisiert **280 Milliarden USD** an Gesamtförderung:
- **39 Milliarden USD** für Fab-Bau
- **11 Milliarden USD** für Forschung
- **2 Milliarden USD** speziell für reife Prozesstechnologien (Legacy Chips)
- Steuervorteile: **25% Investment Tax Credit** für Chip-Anlagen

#### Die größten Empfänger

| Unternehmen | Förderung | Projekt |
|-------------|-----------|---------|
| Intel | 7,86 Mrd. USD | Fabs in AZ, NM, OH, OR |
| TSMC | 6,6 Mrd. USD | 3 Fabs in Arizona |
| Samsung | 6,4 Mrd. USD | Fab in Taylor, Texas |
| Micron | 6,1 Mrd. USD | Fabs in NY und ID |
| GlobalFoundries | 1,5 Mrd. USD | Fab in Malta, NY |
| Amkor | 407 Mio. USD | Packaging in AZ |

**Gesamt bis November 2024:** 33,7 Milliarden USD in Zuschüssen und bis zu 28,8 Milliarden USD in Krediten an 20 Unternehmen für 32 Projekte in 20 Bundesstaaten.

**Die drei größten Profiteur-Staaten:** Arizona, Texas, New York (jeweils 5–10 Mrd. USD).

#### Zukunft unter Trump
Trump hat Skepsis gegenüber dem CHIPS Act geäußert ("Why are we paying companies to do what they should do anyway?"), aber die bereits abgeschlossenen Verträge sind bindend. Die finalisierte TSMC-Förderung wurde noch unter Biden im November 2024 unterschrieben.

### Chinas Chip-Gegenoffensive: SMIC, Huawei und die 7nm-Mauer

#### Huawei Kirin: Langsamer Fortschritt
Die Timeline der Huawei/SMIC-Chipentwicklung:

| Chip | Prozess (SMIC) | Gerät | Jahr |
|------|----------------|-------|------|
| Kirin 9000S | N+2 (7nm) | Mate 60 Pro | 2023 |
| Kirin 9010 | N+2 (7nm) | Pura 70 | 2024 |
| Kirin 9020 | N+2 (7nm) | Mate 70 Pro | 2024 |
| Kirin 9030 | N+3 (verbesserte 7nm) | Mate 80 Pro Max | 2025 |
| Kirin X90 | N+2 (7nm) | MatBook Fold | 2025 |

**Die Realität:** Trotz der Namensgebung "N+3" handelt es sich beim Kirin 9030 immer noch um eine **verbesserte Version von 7nm** — nicht um echtes 5nm. TechInsights bestätigte im Dezember 2025, dass SMIC zwar "meaningful density improvements" erzielt hat, aber technologisch immer noch **hinter TSMC und Samsung** liegt.

#### Das EUV-Problem
Der Schlüssel: SMIC hat **keinen Zugang zu EUV-Lithographie-Maschinen** (Extreme Ultraviolet) von ASML, die für Prozessknoten unter 7nm essentiell sind. SMIC nutzt stattdessen **DUV-Multi-Patterning** — eine Methode, die:
- **Deutlich langsamer** ist (weniger Wafer pro Stunde)
- **Geringere Yields** produziert
- **Höhere Kosten pro Chip** verursacht
- **Physikalische Grenzen** bei etwa 5nm hat

#### Wie weit ist China wirklich?
- **Auf dem Papier:** 3-5 Jahre hinter TSMC (7nm vs. 3nm/2nm)
- **In der Praxis:** Die Lücke ist größer, weil SMIC keine EUV-Maschinen hat und die Yields bei fortschrittlichen Nodes deutlich schlechter sind
- **Bei KI-Chips:** Huaweis Ascend 910C (für KI-Training, vergleichbar mit Nvidias A100) nutzt SMICs N+3-Prozess (6nm-Klasse). Die Leistung liegt **deutlich unter** den neuesten Nvidia-Chips (H100, H200, B200)
- **Quantität vs. Qualität:** China kompensiert den Technologierückstand teilweise durch schiere Masse — über 1 Million A100-äquivalente Chips wurden vor den verschärften Sanktionen importiert
- **5nm-Sprung:** SMIC arbeitet an einem echten 5nm-äquivalenten Prozess, aber die Massenproduktion wird frühestens 2026 erwartet — und selbst dann wird der Yield fraglich sein

---

## Thema 5: Indien als KI-Player

### Indiens KI-Strategie: Die IndiaAI Mission

Im **März 2024** startete die indische Regierung die **IndiaAI Mission** mit einem Budget von **₹10.371,92 Crore** (ca. 1,24 Milliarden USD) über fünf Jahre. Das Motto: *"Making AI in India and Making AI work for India"*.

#### Die sieben Säulen der IndiaAI Mission:
1. **IndiaAI Compute Capacity** — Aufbau einer nationalen KI-Recheninfrastruktur (10.000+ GPUs)
2. **IndiaAI Innovation Centre** — Entwicklung indischer Foundation Models
3. **IndiaAI Datasets Platform** — Aufbau indischer KI-Datensätze (in 22 offiziellen Sprachen)
4. **IndiaAI Application Development** — KI-Anwendungen für indische Herausforderungen (Gesundheit, Landwirtschaft, Klimawandel, Governance). Bis Juli 2025 wurden 30 Anwendungen genehmigt
5. **IndiaAI FutureSkills** — KI-Ausbildungsprogramme
6. **IndiaAI Startup Financing** — Finanzierung von KI-Startups
7. **Safe & Trusted AI** — Ethik und Sicherheitsrahmen

#### BharatGen
Das weltweit erste **staatlich finanzierte multimodale LLM-Projekt**: Ein Konsortium aus IIT Bombay, IIT Kanpur, IIT Hyderabad, IIT Mandi, IIT Madras und anderen Institutionen entwickelt Foundation Models für Sprache, Bild und Ton — speziell für indische Sprachen. Stand Februar 2025: 50-60 Forscher und zahlreiche studentische Mitarbeiter.

#### Budget im Kontext
Die IndiaAI Mission klingt ambitioniert, aber im globalen Vergleich:
- **USA:** CHIPS Act allein 280 Mrd. USD; einzelne Unternehmen (Microsoft, Google, Amazon) investieren jeweils 50-100 Mrd. USD jährlich in KI-Infrastruktur
- **China:** Schätzungsweise 30-50 Mrd. USD jährlich an staatlichen und privaten KI-Investitionen
- **Indien:** ~250 Mio. USD pro Jahr (die Centres of Excellence erhielten 2024-25 nur Rs. 255 Crore / ~28 Mio. USD)

Wie ein Kommentar von *The Hindu Frontline* (Februar 2026) anmerkt: "The sum is not trivial, but it does not build the kind of research infrastructure capable of shifting" — das Budget reicht nicht, um die Forschungsinfrastruktur fundamental zu verändern.

### Indiens Tech-Talent-Pool

Indien verfügt über einen der **größten Pools an Software-Entwicklern weltweit**:

- **~4,3–5,2 Millionen Software-Ingenieure** (2025), der zweitgrößte nach den USA (4,7 Mio.)
- **Wachstumsrate: 11,2% pro Jahr** (USA: 5,6%) — Indien holt rapide auf und könnte die USA bis ~2027 überholen
- **~500.000 neue IT-Absolventen pro Jahr** — eine halbe Million Software-Ingenieure jedes Jahr
- **650.000 indische Ingenieure** arbeiten remote für internationale Unternehmen
- Indiens IT-Services-Branche (TCS, Infosys, Wipro, HCL) beschäftigt Millionen und generiert über 200 Mrd. USD Umsatz

### Wichtige indische KI-Unternehmen

| Unternehmen | Gründung | Fokus | Status |
|-------------|----------|-------|--------|
| **Krutrim** (Bhavish Aggarwal/Ola) | 2023 | Indisches LLM, 22 Sprachen | Erstes KI-Unicorn Indiens (1 Mrd. USD, Jan. 2024) |
| **Sarvam AI** | 2023 | Open-Source Hindi LLM (OpenHathi) | 41 Mio. USD Finanzierung |
| **Arya.ai** | 2013 | KI für Finanzdienstleistungen | Etabliert |
| **InVideo** | 2019 | KI-Video-Erstellung | Global aktiv |
| **Leena AI** | 2018 | Konversations-KI für HR | Enterprise-Fokus |
| **Cyient** | 1991 | KI für Engineering/Industrie | Börsennotiert (NSE) |

**Krutrim** verdient besondere Beachtung: Gegründet von Ola-Gründer Bhavish Aggarwal, wurde es im Januar 2024 mit 1 Milliarde USD bewertet — nur wenige Wochen nach der Ankündigung. Das Modell soll in **22 indischen Sprachen** funktionieren, was angesichts Indiens sprachlicher Vielfalt ein enormer Vorteil gegenüber westlichen Modellen wäre.

**Sarvam AI** verfolgt einen Open-Source-Ansatz mit dem Modell **OpenHathi** — einem Hindi-optimierten LLM, das auf offenen Modellen aufbaut. Im Februar 2026 sammelte Sarvam eine signifikante Finanzierungsrunde ein.

### Indiens Rolle als Outsourcing-Hub für KI-Training und Annotation

Indien ist ein **globaler Hub für Daten-Annotation** — die oft unsichtbare Arbeit, die KI-Systeme trainierbar macht:

- Hunderte von Unternehmen in Indien bieten Daten-Annotationsdienste an (Learning Spiral, Shaip, und viele mehr)
- Indische Arbeiter labeln Bilder, transkribieren Audio, kategorisieren Text und trainieren Chatbots — für einen Bruchteil westlicher Kosten
- Die Verfügbarkeit von **Englisch-sprechenden Arbeitskräften** in Kombination mit niedrigen Lohnkosten macht Indien zum bevorzugten Standort
- Spezialisierte Annotationen für Bereiche wie Healthcare, Finanzen und Automotive
- Zunehmend auch **RLHF-Training** (Reinforcement Learning from Human Feedback) für große Sprachmodelle

### Krypto-Regulierung in Indien: Drakonisch restriktiv

Indien hat eines der **strengsten Krypto-Steuerregimes der Welt**:

- **30% Flat Tax** auf alle Krypto-Gewinne (seit April 2022, Section 115BBH)
- **4% Health & Education Cess** zusätzlich → effektiv **31,2%**
- **1% TDS (Tax Deducted at Source)** auf jede Krypto-Transaktion über Rs. 50.000 (ca. 600 USD)
- Seit 2025/2026: Zusätzlich **GST (Goods & Services Tax)** auf Krypto-Transaktionen
- **Kein Verlustausgleich:** Verluste aus Krypto können nicht mit Gewinnen verrechnet werden — selbst wenn man bei einem Token Verlust macht und bei einem anderen Gewinn
- **Kein Verlustvortrag:** Krypto-Verluste können nicht in Folgejahre übertragen werden
- Krypto-Exchanges müssen **PMLA (Prevention of Money Laundering Act)** und strenge KYC-Regeln einhalten

**Auswirkungen:**
- Das Handelsvolumen auf indischen Krypto-Börsen ist nach Einführung der 30%-Steuer dramatisch eingebrochen
- Viele indische Krypto-Trader sind auf ausländische Plattformen (Binance) ausgewichen — bis diese ebenfalls blockiert oder reguliert wurden
- Innovation im Krypto/Web3-Bereich findet weitgehend außerhalb Indiens statt

**Vergleich:** Indiens 30% Flat Tax ohne Verlustausgleich ist sogar strenger als die EU (wo Verluste in vielen Ländern zumindest teilweise verrechenbar sind) und deutlich strenger als die USA (wo Krypto als Kapitalanlage mit gestaffelten Steuersätzen behandelt wird).

### OpenAI: 100 Millionen Nutzer in Indien

Im **Februar 2026** — kurz vor dem India AI Impact Summit in Neu-Delhi — verkündete OpenAI-CEO Sam Altman:

> **Indien hat 100 Millionen wöchentlich aktive ChatGPT-Nutzer** — das macht Indien zum **zweitgrößten Markt** nach den USA und zum größten in Asien.

Schlüsseldaten:
- **18-24-Jährige** senden die Hälfte aller ChatGPT-Nachrichten in Indien
- Hauptnutzer: Studenten, Lehrer, Entwickler, Unternehmer
- Indiens Anteil am globalen ChatGPT-Traffic: **8,71%** (USA: 16,18%)
- Bei einer indischen Bevölkerung von ~1,45 Milliarden nutzen ~7% wöchentlich ChatGPT

Altman bezeichnete Indien als **"potential superpower in AI"** — das Wort "superpower" war bewusst gewählt.

### Könnte Indien zum dritten KI-Pol werden?

**Argumente dafür:**
- **Größter Talent-Pool der Welt:** 4,3+ Mio. Software-Ingenieure, 500.000 neue pro Jahr
- **Riesiger Binnenmarkt:** 1,45 Mrd. Menschen, davon 100 Mio. aktive ChatGPT-Nutzer
- **Sprachliche Vielfalt als Unique Selling Point:** 22 offizielle Sprachen erzwingen Innovation in multilingualen KI-Systemen
- **Jugendliche Demografie:** Medianalter 28 Jahre (USA: 38, China: 39, EU: 44)
- **Regierungsunterstützung:** IndiaAI Mission, Digital India, zunehmende GPU-Infrastruktur
- **Aufstrebendes Startup-Ökosystem:** Krutrim, Sarvam AI und über 170 KI-Startups
- **Geopolitische Positionierung:** Indien ist weder US-Verbündeter noch China-Alliierter, sondern strategisch unabhängig

**Argumente dagegen:**
- **Budget-Realität:** 1,24 Mrd. USD über 5 Jahre vs. einzelne US-Unternehmen, die Hunderte Milliarden investieren
- **Keine eigene Chip-Fertigung:** Indien produziert keine eigenen fortschrittlichen Halbleiter
- **Infrastruktur:** Stromversorgung, Internetqualität und Datencenter-Kapazität hinken hinterher
- **Brain Drain:** Viele der besten indischen KI-Forscher arbeiten bei Google, Microsoft, OpenAI in den USA
- **Kein eigenes Foundation Model von Weltklasse:** Krutrim und Sarvam AI sind vielversprechend, aber (noch) nicht auf dem Niveau von GPT-4, Claude oder DeepSeek
- **Restriktive Krypto-Regulierung** verhindert Innovation an der Schnittstelle KI/Blockchain

**Realistisches Szenario:** Indien wird vermutlich kein "dritter Pol" im Sinne eines eigenständigen KI-Ökosystems auf Augenhöhe mit den USA oder China. Wahrscheinlicher ist, dass Indien zum **größten Anwendungsmarkt und Talent-Exporteur** wird — eine Supermacht der KI-Nutzung und des KI-Dienstleistungssektors, nicht der KI-Grundlagenforschung. Die **217 Milliarden USD**, die Indien laut einer Prognose bis 2030 in KI investieren könnte, würden diese Position als "distinct third pole" untermauern — allerdings mit einem anderen Schwerpunkt als USA (Frontier-Modelle) und China (staatlich gesteuerte KI-Autarkie).

---

## Zusammenfassung der Querschnittsthemen

### Das Europa-Paradox
Alle fünf Themen zeigen ein gemeinsames Muster: **Europäische Regulierung schützt Bürger — und benachteiligt sie gleichzeitig**:
- Meta Llama: EU-Bürger sind "geschützt" vor multimodalen KI-Modellen, die auf ihren Daten trainiert wurden — aber können die leistungsfähigsten offenen Modelle nicht legal nutzen
- MiCA/Stablecoins: EU-Bürger sind "geschützt" vor unregulierten Finanzprodukten — aber verlieren 4-5% Rendite auf ihre Stablecoin-Bestände
- MiCA/Tokens: EU-Bürger sind "geschützt" vor unseriösen Token-Emissionen — aber innovative Projekte wandern ab
- Chip-Krieg: Europa ist abhängig von US- und asiatischer Chip-Fertigung und hat keine eigene führende Foundry
- Indien: Ein Land mit einem Bruchteil des EU-BIPs hat 100 Mio. wöchentliche ChatGPT-Nutzer und baut aktiv eigene KI-Modelle

### Für das Buchprojekt "Maschinengeld"
Diese Recherche stützt die These, dass die Konvergenz von KI und Krypto/Geld primär außerhalb Europas stattfindet — in den USA (Innovation), China (staatliche Kontrolle) und zunehmend in Indien (Massenadoption). Europa reguliert, während andere bauen. Die Frage ist nicht, ob diese Regulierung gute Absichten hat, sondern ob Europa sich mit diesen Absichten aus der Zukunft reguliert.

---

**Quellen:** Axios (17.07.2024), The Verge (18.07.2024), Slator (04.10.2024), Decrypt (29.11.2024), CoinTelegraph (29.11.2024), DL News (29.11.2024), Finance Magnates (2024), Reuters (02.12.2024, 13.12.2025), CNBC (02.12.2024), Fortune (05.12.2024), TrendForce (29.05.2025), Tom's Hardware (12.12.2024, 2025), TechCrunch (26.01.2024, 15.02.2026), PIB India (2024-2025), IEEE Spectrum (27.12.2024), TSMC Pressemitteilungen (08.04.2024, 04.03.2025), ESMA, Paul Hastings LLP, Norton Rose Fulbright, Hacken.io, Sara Zan Blog (16.05.2025), ioplus.nl (07.04.2025), Apple Newsroom (2025), CoinMarketCap (30.01.2025), O2K Tech, Vaultody, COREDO, Bloomberg (11.12.2025), SCMP (15.12.2025), SemiWiki, The Register (23.06.2025), SIA, Manufacturing Dive, Visual Capitalist, NIST CHIPS, Motley Fool (16.02.2026), CNBC (25.07.2025), Unite.ai (Feb. 2026), India Today (16.02.2026), Frontline/The Hindu (24.02.2026)
