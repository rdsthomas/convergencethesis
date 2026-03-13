# Überarbeitungsplan: "Maschinengeld"

**Erstellt:** 24. Februar 2026  
**Grundlage:** Lektorats- und Qualitätsbericht vom 24.02.2026  
**Ziel:** Alle identifizierten Schwächen beseitigen, alle vier Personas stärker bedienen

---

## Phase 1: Strukturelle Eingriffe (KRITISCH)

Diese Änderungen betreffen die Architektur des Buches und sollten zuerst umgesetzt werden, da sie die Grundlage für alle weiteren Verbesserungen bilden.

### 1.1 Robotik-Duplikate in Kap. 2 bereinigen
**Problem:** Boston Dynamics, Figure AI, 1X, Unitree, NVIDIA werden dreimal nahezu wörtlich beschrieben (KI-Landschaft, Robotik-Landschaft, Phase 4).  
**Maßnahme:**
- Die ausführliche Beschreibung der Robotik-Player in **Phase 4** belassen (dort gehört sie hin)
- In "KI-Landschaft" nur kurz erwähnen: "Die wichtigsten Robotik-Player — von Boston Dynamics bis Figure AI — behandle ich ausführlich in Phase 4"
- Den separaten "Robotik-Landschaft"-Abschnitt **komplett streichen** und Inhalte in Phase 4 integrieren
- **Geschätzter Umfang:** 3-5 Seiten Kürzung

### 1.2 Kapitel 3b aufteilen
**Problem:** Kap. 3b hat die Länge eines Kurzbuches und mischt Tokenisierung mit Stablecoin-Geopolitik und Schuldenthemen.  
**Maßnahme:**
- **Neues Kap. 3b:** "Tokenisierung — Wenn alles handelbar wird" (Was es ist, RWA-Beispiele, Demokratisierung vs. Gatekeeper, Maschinen als Investoren)
- **Neues Kap. 3c:** "Stablecoins und das Schuldenparadox" (Dollar-Dominanz, BRICS, US-Schuldenkrise, drei Szenarien)
- **Bisheriges Kap. 3c (DAOs)** wird zu **Kap. 3d**
- **Geschätzter Umfang:** Keine Kürzung, aber bessere Verdaulichkeit

### 1.3 Kapitelnummerierung bereinigen
**Problem:** "Kap. 10b" wirkt wie ein Nachtrag.  
**Maßnahme:**
- Kap. 10 → Kap. 10 (Ethik)
- Kap. 10b → Kap. 11 (Longevity)
- Bisheriges Kap. 11 → Kap. 12 (Barbell-Strategie)
- Bisheriges Kap. 12 → Kap. 13 (Risiken)
- Bisheriges Kap. 13 → Kap. 14 (Warum jetzt)
- **Alle Querverweise im gesamten Buch prüfen und aktualisieren!**

### 1.4 Überlappungen Kap. 4 ↔ Kap. 7 auflösen
**Problem:** EU-Regulierungskritik wird in beiden Kapiteln redundant behandelt.  
**Maßnahme:**
- **Kap. 4 (Geopolitik):** Behält die drei persönlichen Regulierungserfahrungen und den Europa-Kontext. Fokus: "Wie Regulierung die geopolitische Machtverteilung verschiebt"
- **Kap. 7 (Regulierung):** Streicht wiederholte Europa-Kritik, stärkt stattdessen: Robotersteuer, Waffen-Regulierung, konkrete Handlungsempfehlungen für europäische Leser
- Autonome-Waffen-Abschnitt von Kap. 7 nach Kap. 10 (Ethik) verschieben — dort passt er thematisch besser
- **Geschätzter Umfang:** 2-3 Seiten Kürzung in Kap. 7

---

## Phase 2: Humanizer-Überarbeitung

Gezieltes Entfernen von AI-Writing-Patterns, ohne den Stil zu verändern.

### 2.1 Erstens/Zweitens/Drittens-Pattern auflösen
**Betroffene Kapitel:** 1, 2, 3b (neu), 4, 7  
**Maßnahme:**
- Jedes Vorkommen identifizieren (ca. 12-15 Stellen)
- **Mindestens 8 davon** in Fließtext umwandeln
- Erlaubt: Maximal 2-3 bewusste Erstens/Zweitens/Drittens im gesamten Buch, wo die Nummerierung echten Mehrwert hat
- **Beispiel-Transformation:**
  - Vorher: "Erstens: Die Technologie ist real. Zweitens: Die meisten Investments scheitern. Drittens: Das Geld fließt zur Infrastruktur."
  - Nachher: "Die Technologie war in jedem dieser Zyklen real — das war nie das Problem. Das Problem war, dass die meisten frühen Investments trotzdem scheiterten. Was überlebte, war die Infrastruktur: nicht die Dotcom-Startups, sondern die Glasfaserkabel."

### 2.2 Em-Dash-Reduktion
**Betroffene Kapitel:** 3b (neu), 4, 5, 7  
**Maßnahme:**
- Pro Absatz maximal einen Gedankenstrich erlauben
- Überzählige ersetzen durch: Punkt + neuer Satz, Komma, Doppelpunkt, oder Klammer
- **Fokus:** Kap. 3b und Kap. 4 zuerst (dort am auffälligsten)

### 2.3 "Fundamental/transformativ"-Inflation reduzieren
**Maßnahme:**
- "fundamental" von >15 auf maximal 5 Vorkommen reduzieren
- "transformativ" von 6 auf maximal 2 reduzieren
- Alternativen: "grundlegend", "tiefgreifend", "einschneidend", "weitreichend", oder die Passage so umschreiben, dass das Adjektiv überflüssig wird
- "entscheidend" ebenfalls prüfen und variieren

### 2.4 Generische Schlussabsätze überarbeiten
**Betroffene Kapitel:** 1, 3, 5, 7  
**Maßnahme:**
- Kapitelschlüsse individualisieren — jedes Kapitel braucht einen eigenen Ausklang
- Kap. 1: "Die Maschinen kommen. Und sie bringen ihr eigenes Geld mit" → spezifischer, weniger slogan-haft
- Den dreifach ähnlichen Schluss (Kap. 13, Vorwort, Epilog) differenzieren: Nur einer darf die "Kann ich es mir leisten, nicht zu handeln?"-Frage stellen

---

## Phase 3: Spannungsbogen & Übergänge

### 3.1 Kapitelübergänge schreiben
**Alle Kapitel betroffen.**  
**Maßnahme:** Am Ende jedes Kapitels 1-2 Sätze ergänzen, die zum nächsten Kapitel überleiten.

**Entwürfe für die kritischsten Übergänge:**
- **Kap. 2 → Kap. 3:** "Maschinen, die denken, handeln und lernen — das ist beeindruckend. Aber eine Frage bleibt offen: Wie bezahlen sie dafür?"
- **Kap. 5 → Kap. 6:** "Energie ist die physische Grundlage der Maschinenökonomie. Aber was ist mit den Menschen, die in dieser neuen Welt leben müssen?"
- **Kap. 7 → Kap. 8:** "Regulierung kann bremsen, lenken oder zerbrechen. Was passiert, wenn wir die nächsten zehn Jahre unter diesen Bedingungen durchspielen?"
- **Kap. 9 → Kap. 10:** "Wenn Maschinen denken, handeln, bezahlen und vielleicht sogar fühlen — dann stehen wir vor Fragen, die kein Business-Plan beantworten kann."

### 3.2 Brücke von Kap. 2 zu Kap. 3 stärken
**Maßnahme:** Kurzweils Technologie-Spirale am Ende von Kap. 2 als explizite Brücke nutzen: "Und in dieser sich beschleunigenden Spirale brauchen die Maschinen eines, das sie bisher nicht haben: Geld."

### 3.3 Robotik-Durchhänger in Kap. 8 beheben
**Problem:** Figure AI/1X werden erneut wiederholt.  
**Maßnahme:** Kap. 8 referenziert die Robotik-Player nur noch per Verweis auf Kap. 2, bringt stattdessen **neue Informationen**: konkrete Einsatzszenarien, Stückzahlen-Prognosen, Kostenentwicklung.

---

## Phase 4: Persona-Befriedigungf

### 4.1 Persona "Klaus" (Finanzberater, 55) stärker bedienen

#### 4.1.1 Barbell-Portfolio backtesten
**Kapitel:** 11 (neu: 12)  
**Maßnahme:**
- Vereinfachten Backtest für 2022-2025 rechnen
- Drei Varianten (Konservativ/Ausgewogen/Aggressiv) vs. MSCI World und 60/40
- Sharpe Ratio, Max Drawdown, Gesamtrendite
- In einer Tabelle darstellen
- **Hinweis:** Historische Performance als Illustration, nicht als Garantie kennzeichnen

#### 4.1.2 Regulierte Produkte nennen
**Kapitel:** 11 (neu: 12)  
**Maßnahme:**
- Bei jeder Asset-Klasse mindestens ein reguliertes Produkt nennen (ETF-ISIN, WKN)
- Beispiele: iShares Global Clean Energy ETF, VanEck Bitcoin ETN, CoinShares Ethereum ETP
- "Wie ein deutscher Anleger mit Depot bei einer Direktbank investieren kann" — 1 Seite Praxis

#### 4.1.3 DAO-Kapitel besser einordnen
**Kapitel:** 3d (neu)  
**Maßnahme:**
- Abschnitt ergänzen: "Was das für die Fondsstrukturierung der Zukunft bedeutet"
- Brücke bauen: "Wenn Sie heute einen Fonds auflegen, brauchen Sie eine KVG, eine Depotbank, einen Administrator. Eine DAO kann das in einem Smart Contract abbilden."

#### 4.1.4 Worst-Case-Szenario durchrechnen
**Kapitel:** 12 (neu: 13)  
**Maßnahme:**
- Konkretes Szenario: NVIDIA -60%, Bitcoin -80%, KI-feindliche EU-Regulierung, Krypto-Winter
- Zeigen: Was bleibt vom Barbell-Portfolio übrig?
- Die "sichere Seite" (70-80%) als Rettungsanker demonstrieren

### 4.2 Persona "Lena" (Gründerin, 32) stärker bedienen

#### 4.2.1 Gründer-Perspektive ergänzen
**Kapitel:** 4 oder neuer Abschnitt  
**Maßnahme:**
- 2-3 Seiten: "Was die Convergence Thesis für Gründer bedeutet"
- Sollte mein SaaS on-chain laufen? (Nein, aber hier ist, wann es Sinn macht…)
- Token-Emission für Startups: Wann ja, wann nein?
- Europäische Gründer trotz AI Act: Wie positionieren?
- Kann als eigener Kasten/Exkurs in Kap. 4 oder Kap. 11 eingebaut werden

#### 4.2.2 Open-Source-Implikationen vertiefen
**Kapitel:** 2  
**Maßnahme:**
- DeepSeek-Abschnitt ausbauen: Was bedeutet Open Source für die Machtverteilung?
- Llama, Mistral, Open-Source-Ökosystem → Chancen für Startups
- "Warum ein Berliner Startup mit einem Open-Source-Modell gegen OpenAI antreten kann"

#### 4.2.3 Wiederholungen eliminieren
Ergibt sich automatisch aus Phase 1 (Robotik-Duplikate, Kap. 4/7 Überlappung).

### 4.3 Persona "Markus" (Bankangestellter, 42) stärker bedienen

#### 4.3.1 Glossar erstellen
**Neuer Anhang**  
**Maßnahme:**
- Alphabetisches Glossar: 40-60 Begriffe
- Jeder Begriff: 1-2 Sätze, alltagstaugliche Erklärung
- Beispiel: "DeFi (Decentralized Finance): Finanzdienstleistungen ohne Bank. Statt dass eine Sparkasse Ihren Kredit verwaltet, macht das ein Computerprogramm auf einer Blockchain."
- Im Text: Bei Erstverwendung jedes Begriffs Seitenverweis auf Glossar

#### 4.3.2 Bankensektor-Abschnitt ergänzen
**Kapitel:** 6 oder 8  
**Maßnahme:**
- 3-4 Seiten: "Was passiert mit Banken in der Maschinenökonomie?"
- Konkret: Welche Bankjobs verschwinden? Welche verändern sich? Welche entstehen?
- Referenz auf JPMorgan-AI-Investitionen, DBS-Bank-Tokenisierung
- "Wenn Sie bei einer Bank arbeiten: Was Sie jetzt lernen sollten"

#### 4.3.3 Bildungs- und Umschulungskapitel
**Kapitel:** 6  
**Maßnahme:**
- Den "Das ist eine Debatte für ein anderes Buch"-Verweis ersetzen durch 3-4 Seiten konkreter Empfehlungen
- Welche Fähigkeiten werden wertvoll? (Prompt Engineering, KI-Aufsicht, ethische KI-Governance, Datenqualität)
- Welche werden wertlos? (Routine-Datenverarbeitung, Standard-Programmierung, einfache Analyse)
- Konkrete Weiterbildungsressourcen (Coursera, LinkedIn Learning, etc.)

#### 4.3.4 Krypto-Sprache vereinfachen
**Kapitel:** 3, 3b, 3c (neu)  
**Maßnahme:**
- Jeden Fachbegriff bei Erstverwendung mit Alltagsanalogie erklären
- "Layer-2" → "Stellen Sie sich die Blockchain als Autobahn vor. Layer-2 ist die Entlastungsstraße daneben."
- "Smart Contract" → "Ein digitaler Vertrag, der sich selbst ausführt — wie ein Getränkeautomat: Geld rein, Flasche raus, kein Mensch nötig."

### 4.4 Persona "Marco" (Krypto-Investor, 28) stärker bedienen

#### 4.4.1 DeFi-Protokoll-Analyse
**Kapitel:** 3b oder 11 (neu: 12)  
**Maßnahme:**
- Deep Dive: Welche DeFi-Protokolle profitieren von der Machine Economy?
- Uniswap v4 Hooks, Agent-Wallets, autonome Liquiditätspools
- TVL-Entwicklung in RWA-Protokollen (Centrifuge, Maple, Goldfinch)
- On-Chain-Metriken als Tabelle

#### 4.4.2 Solana ernst nehmen
**Kapitel:** 3  
**Maßnahme:**
- Abschnitt "Bitcoin als Anker, Ethereum als Betriebssystem" um Solana erweitern
- "Solana als Hochfrequenz-Layer": Mikrotransaktionen, Agent-Payments, Compressed NFTs
- Nicht als Konkurrenz zu Ethereum framen, sondern als komplementär
- Blinktrade, DePIN auf Solana (Helium, Render)

#### 4.4.3 Tokenomics analysieren
**Kapitel:** 11 (neu: 12)  
**Maßnahme:**
- Für jeden genannten Token (OLAS, PEAQ, FET, RENDER) 1 Absatz Tokenomics:
  - Supply-Mechanik (inflationär/deflationär?)
  - Staking/Governance-Rechte
  - Token-Unlock-Schedule
  - Revenue-Share-Mechanismus
- Alternative: Als Tabelle im Anhang

#### 4.4.4 On-Chain-Daten einbauen
**Kapitel:** Verschiedene  
**Maßnahme:**
- Stablecoin-Transaktionsvolumen (Visa-Vergleich) → Kap. 3
- TVL in DeFi und RWA-Protokollen → Kap. 3b
- Agent-Transaktionsvolumen auf Ethereum/Solana → Kap. 3c
- Bitcoin-ETF-Flows → Kap. 11
- "Stand: [Monat 2026]" kennzeichnen

---

## Phase 5: Inhaltliche Ergänzungen

### 5.1 Persönliche Anekdoten einbauen
**Betroffene Kapitel:** 5, 7, 8, 10  
**Maßnahme:** In jedem Kapitel mindestens eine persönliche Geschichte aus dem Unternehmertum.

**Vorschläge:**
- **Kap. 5 (Energie):** Wie viel Cloud-Compute kostet accessibleAI monatlich? Was zahlt ein KI-Startup für GPU-Zeit? Persönliche Erfahrung mit Rechenkosten.
- **Kap. 7 (Regulierung):** Eine weitere Regulierungserfahrung aus accessibleAI — z.B. BFSG-Compliance-Aufwand für Kunden, oder wie absurd bestimmte Anforderungen sind.
- **Kap. 8 (Szenario):** "Als ich 2025 anfing, einen KI-Assistenten in mein Unternehmen zu integrieren…" — was funktioniert, was nicht, was überrascht hat.
- **Kap. 10 (Ethik):** Eigene ethische Dilemmas beim Einsatz von KI — z.B. Entscheidungen über Datenschutz bei accessibleAI, oder wie KI-generierte Barrierefreiheits-Audits menschliche Prüfer ersetzen.

### 5.2 "Day in the Life 2030"-Szenario
**Kapitel:** 8  
**Maßnahme:**
- 2-3 Seiten Erzählung: Ein Tag im Leben eines normalen Menschen 2030
- Morgens: KI-Assistent hat Termine organisiert und Einkauf bestellt
- Tagsüber: Arbeit mit KI-Copilot, Besprechung mit KI-Übersetzung
- Abends: Autonomes Auto, tokenisiertes Restaurant-Trinkgeld, KI-personalisierte Unterhaltung
- Stil: Nah, realistisch, nicht dystopisch — aber mit Spannungsmomenten

### 5.3 Cybersecurity-Abschnitt
**Kapitel:** 12 (neu: 13, Risiken)  
**Maßnahme:**
- 2-3 Seiten: Sicherheitsrisiken der Maschinenökonomie
- DAO-Hack 2016 als Ausgangspunkt (bereits erwähnt, ausbauen)
- Smart-Contract-Bugs, Bridge-Hacks, Oracle-Manipulation
- "Was passiert, wenn eine Maschinen-DAO gehackt wird?"
- KI-gestützte Cyberangriffe vs. KI-gestützte Verteidigung

### 5.4 Datenschutz und Privacy
**Kapitel:** 10 (Ethik) oder 9 (Interface)  
**Maßnahme:**
- 2-3 Seiten: Wenn Maschinen alles sehen, hören, analysieren
- BCI-Daten als intimste Daten überhaupt
- Surveillance Capitalism → Surveillance Economy
- "Wem gehören die Daten einer Maschinen-DAO?"

### 5.5 Konkrete Krypto-Risiken
**Kapitel:** 12 (neu: 13)  
**Maßnahme:**
- Praktische Investorenrisiken: Rug Pulls, Depegging, Smart-Contract-Exploits
- Wie man sich schützt: Cold Storage, Audit-Reports, Versicherungen
- "Die zehn häufigsten Fehler bei Krypto-Investments"

---

## Phase 6: Anhang & Begleitmaterial

### 6.1 Glossar
- 40-60 Begriffe, alphabetisch
- Alltagstaugliche Erklärungen
- Seitenverweise auf erste Verwendung im Text

### 6.2 Weiterführende Ressourcen
- Bücher (Marks, Taleb, Kurzweil, Sinclair — bereits zitiert)
- Podcasts
- Websites/Tools für On-Chain-Daten
- Weiterbildungsplattformen

### 6.3 Abbildungen & Tabellen
- Barbell-Portfolio als Grafik
- Backtest-Ergebnis als Tabelle
- KI-Phasen-Timeline
- Tokenomics-Vergleich (Tabelle)
- Geopolitik-Karte (KI-Regulierung weltweit)

---

## Zeitplan

| Phase | Aufwand (geschätzt) | Priorität |
|-------|-------------------|-----------|
| Phase 1: Strukturelle Eingriffe | 2-3 Tage | KRITISCH |
| Phase 2: Humanizer | 1-2 Tage | HOCH |
| Phase 3: Übergänge | 1 Tag | HOCH |
| Phase 4: Personas | 3-5 Tage | HOCH |
| Phase 5: Ergänzungen | 3-5 Tage | MITTEL |
| Phase 6: Anhang | 1-2 Tage | MITTEL |
| **Gesamt** | **~11-18 Tage** | |

**Empfohlene Reihenfolge:** Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6

Phasen 1-3 können teilweise parallel bearbeitet werden. Phasen 4 und 5 haben Überschneidungen (z.B. Bankensektor-Abschnitt bedient Markus UND füllt eine inhaltliche Lücke).

---

## Checkliste Persona-Abdeckung

| Maßnahme | Klaus | Lena | Markus | Marco |
|----------|:-----:|:----:|:------:|:-----:|
| Backtest Barbell-Portfolio | ✅ | | | |
| ETF-ISINs / regulierte Produkte | ✅ | | ✅ | |
| DAO-Einordnung für Finanzbranche | ✅ | | ✅ | |
| Worst-Case-Szenario | ✅ | | ✅ | |
| Gründer-Perspektive | | ✅ | | |
| Open-Source-Vertiefung | | ✅ | | |
| Glossar | | | ✅ | |
| Bankensektor-Abschnitt | | | ✅ | |
| Bildung & Umschulung | | | ✅ | |
| Krypto-Sprache vereinfachen | | | ✅ | |
| DeFi-Protokoll-Analyse | | | | ✅ |
| Solana-Abschnitt | | | | ✅ |
| Tokenomics | | | | ✅ |
| On-Chain-Daten | | | | ✅ |
| Wiederholungen eliminieren | ✅ | ✅ | | ✅ |
| Persönliche Anekdoten | ✅ | ✅ | ✅ | |
| Kapitelübergänge | ✅ | ✅ | ✅ | ✅ |

---

*Dieser Plan ist die Arbeitsgrundlage für die Überarbeitung des Manuskripts. Die Prioritäten sind so gesetzt, dass die kritischsten Probleme zuerst gelöst werden und jede Phase das Buch messbar verbessert.*
