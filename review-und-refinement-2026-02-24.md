# Kritischer Review & Refinement des Überarbeitungsplans

**Datum:** 24. Februar 2026  
**Grundlage:** Überarbeitungsplan vom 24.02.2026 + Analyse aller 18 Kapitel in Google Docs

---

## TEIL 1: KRITISCHER REVIEW

### Wortanzahl-Realität vs. Plan-Annahmen

Der Plan wurde auf Basis des Lektoratsberichts erstellt, ohne die tatsächlichen Wortanzahlen genau zu kennen. Die Realität:

| Kapitel | Ist-Wörter | Soll (BUCHSTRUKTUR) | Delta |
|---------|-----------|-------------------|-------|
| Vorwort | 809 | 2.000 | -1.191 |
| Kap. 1 | 2.391 | 5.000 | -2.609 |
| Kap. 2 | 3.843 | 8.000 | -4.157 |
| Kap. 3 | 1.832 | 8.000 | -6.168 |
| Kap. 3b | 5.135 | (Teil von Kap. 3) | — |
| Kap. 3c | 2.619 | (Teil von Kap. 3) | — |
| Kap. 4 | 3.114 | 7.000 | -3.886 |
| Kap. 5 | 3.151 | 6.000 | -2.849 |
| Kap. 6 | 3.226 | 7.000 | -3.774 |
| Kap. 7 | 2.657 | 5.000 | -2.343 |
| Kap. 8 | 1.978 | 6.000 | -4.022 |
| Kap. 9 | 1.840 | 10.000 | -8.160 |
| Kap. 10 | 1.812 | 5.000 | -3.188 |
| Kap. 10b | 1.995 | (kein Soll) | — |
| Kap. 11 | 3.203 | 10.000 | -6.797 |
| Kap. 12 | 884 | 7.000 | -6.116 |
| Kap. 13 | 1.282 | 4.000 | -2.718 |
| Epilog | 632 | 2.000 | -1.368 |
| **Gesamt** | **~42.400** | **~75.000** | **~-32.600** |

**Kritische Erkenntnis #1:** Das Buch ist 42.400 Wörter lang, soll aber 50.000-55.000 werden (Massenmarkt-Benchmark). Es fehlen also nicht 8.000-13.000 Wörter wie in BUCHSTRUKTUR geschätzt, sondern **die 42.400 sind der Rohtext inklusive Duplikaten.** Wenn wir die Robotik-Duplikate streichen (~800 Wörter), liegt der Nettotext bei ~41.600.

**Kritische Erkenntnis #2:** Der Plan schlägt signifikantes Hinzufügen vor (Glossar, Bankensektor, Bildung, DeFi, Solana, Backtests, Cybersecurity, Day-in-the-Life etc.) — insgesamt geschätzt 15.000-20.000 neue Wörter. Das würde das Buch auf ~57.000-62.000 Wörter bringen. Das ist im Rahmen, wenn man die Straffungen gegenrechnet. **Aber: Es birgt das Risiko, den Fokus zu verwässern.**

### Risiko-Analyse der einzelnen Phasen

#### Phase 1 (Strukturelle Eingriffe) — Bewertung: ✅ SOLID

**1.1 Robotik-Duplikate:** Korrekt identifiziert, gut beschrieben. Habe die Duplikate verifiziert — sie sind tatsächlich zu ~85% identisch. Die Empfehlung (alles in Phase 4 konsolidieren) ist richtig.

**1.2 Kap. 3b aufteilen:** Hier wird es kritisch. Kap. 3b hat 5.135 Wörter — das ist lang, aber nicht "Kurzbuch-Länge". Der Lektoratsbericht hat die Länge überschätzt, weil die Google-Docs-Formatierung ohne Absätze einen dichten Block erzeugt. **Revidierte Empfehlung:** Kap. 3b muss nicht zwingend aufgeteilt werden. Die Tokenisierung und die Stablecoin-Geopolitik hängen thematisch zusammen (Tokenisierung BRAUCHT Stablecoins als Infrastruktur). Stattdessen: bessere Zwischenüberschriften und einen klareren inneren Aufbau.

**1.3 Kapitelnummerierung:** Korrekt. Kap. 10b → Kap. 11 ist sinnvoll. **Aber:** Die neue Nummerierung erzeugt jetzt 3, 3b, 3c, 3d — das ist genauso unschön. **Revidierte Empfehlung:** Entweder alles durchnummerieren (Kap. 3, 4, 5, 6 statt 3, 3b, 3c, 3d) oder die Unter-Kapitel als "3.1, 3.2, 3.3" bezeichnen.

**1.4 Kap. 4/7 Überlappung:** Korrekt identifiziert. Kap. 4 hat 3.114 Wörter, Kap. 7 hat 2.657. Beide sind unter dem Soll. Die Überlappung zu eliminieren und Kap. 7 mit neuem Material zu füllen ist richtig.

#### Phase 2 (Humanizer) — Bewertung: ⚠️ TEILWEISE PROBLEMATISCH

**2.1 Erstens/Zweitens/Drittens:** Korrekt identifiziert, gute Lösung. **Aber:** Der Plan nennt "ca. 12-15 Stellen" — ich habe in Kap. 2 (dem längsten Kapitel) nachgezählt: Es gibt dort genau 3 Vorkommen (bei DeepSeek: "Erstens, dass US-Exportkontrollen... Zweitens, dass Open Source... Drittens, und das ist die wichtigste Lektion..."). Das ist weniger als vermutet. **Risiko:** Übereifrig aufzulösen, wo es gar nicht stört. Die DeepSeek-Passage z.B. funktioniert mit der Nummerierung.

**2.2 Em-Dash-Reduktion:** Der Plan empfiehlt "maximal einen pro Absatz". Das ist zu restriktiv für den Stil des Buches. Thomas schreibt mit Gedankenstrichen — das ist seine Stimme, kein AI-Artifact. **Revidierte Empfehlung:** Nur dort eingreifen, wo 3+ Gedankenstriche in einem Absatz sind. Nicht flächendeckend.

**2.3 "Fundamental/transformativ":** Richtig identifiziert. **Aber:** 15x "fundamental" in 42.400 Wörtern ist 0,035% — nicht dramatisch. Auf 5 zu reduzieren ist sinnvoll, aber kein Notfall.

**2.4 Generische Schlussabsätze:** Korrekt. Aber: Kap. 2 endet bereits mit einer starken Überleitung ("Oder, und hier kommen wir zum nächsten Kapitel, das Geld, mit dem die Maschinen bezahlen?"). Nicht alle Schlüsse sind generisch.

#### Phase 3 (Übergänge) — Bewertung: ✅ GUT, ABER TEILS ÜBERFLÜSSIG

Die vorgeschlagenen Übergänge sind solide. **Aber:** Einige Kapitel haben bereits Übergänge (Kap. 2 → Kap. 3 ist schon vorhanden). Der Plan sollte prüfen, welche Übergänge fehlen und welche schon existieren, statt blind alle zu schreiben.

#### Phase 4 (Personas) — Bewertung: ⚠️ GRÖSSTES RISIKO

**4.1.1 Barbell-Portfolio backtesten:** Gute Idee, aber **praktisch schwierig**. Die Barbell-Strategie enthält Token (OLAS, PEAQ, FET) und Private Equity (Neuralink, Figure AI), die keinen historischen Track Record als Portfolio haben. Ein seriöser Backtest ist nur für die "sichere Seite" (NVIDIA, Big Tech, ETFs) möglich. **Revidierte Empfehlung:** Vereinfachter Backtest nur der liquiden Positionen, plus ehrliche Aussage: "Die asymmetrische Seite ist per Definition nicht backtestbar — das ist ja der Punkt."

**4.1.2 Regulierte Produkte:** Gute Idee, **aber mit Verfallsdatum.** ETF-ISINs und WKNs können sich ändern, ETFs geschlossen werden. **Revidierte Empfehlung:** In einen Anhang auslagern, mit Hinweis "Stand: März 2026, aktuelle Liste auf [Website]".

**4.2.1 Gründer-Perspektive:** 2-3 Seiten Gründer-Content in einem Investmentbuch? **Risiko: Zielgruppen-Verwässerung.** Das Buch ist ein Investmentbuch, kein Gründer-Handbuch. Lena ist eine von vier Personas. **Revidierte Empfehlung:** Maximal 1 Seite als Exkurs-Box, nicht als eigener Abschnitt.

**4.3.2 Bankensektor-Abschnitt:** 3-4 Seiten über "Was passiert mit Banken?" ist gut, gehört aber in Kap. 6 (Menschlicher Preis), nicht in Kap. 8. **UND:** Der Plan schlägt zeitgleich Bildung/Umschulung (4.3.3) vor — zusammen mit Bankensektor wären das 7-8 Seiten neuer Content in Kap. 6, das aktuell nur 3.226 Wörter hat. Das verdoppelt das Kapitel. **Revidierte Empfehlung:** Bankensektor + Bildung zusammen als EINEN Abschnitt in Kap. 6, max. 2.000 Wörter.

**4.4.1-4.4.4 (Marco, Krypto-Investor):** Die DeFi-Analyse, Tokenomics und On-Chain-Daten sind inhaltlich wertvoll, aber **veralten am schnellsten.** TVL-Zahlen von Februar 2026 sind bis zur Drucklegung obsolet. **Revidierte Empfehlung:** On-Chain-Daten nur als Momentaufnahme mit deutlichem Datums-Stempel, und Verweis auf Live-Dashboards (DefiLlama, Dune Analytics) im Anhang.

#### Phase 5 (Ergänzungen) — Bewertung: ⚠️ ZU VIEL

**5.1 Persönliche Anekdoten:** Essenziell und richtig. **Aber:** Der Plan schlägt Anekdoten für Kap. 5, 7, 8, 10 vor — alle vier. Thomas muss diese selbst schreiben oder zumindest den Kern liefern. KI kann keine authentischen persönlichen Geschichten erfinden. **Das ist kein Task für die automatisierte Umsetzung.**

**5.2 "Day in the Life 2030":** Gute Idee, aber **riskant.** Zukunftsszenarien in Erzählform können schnell kitschig oder naiv wirken. **Revidierte Empfehlung:** Nur umsetzen, wenn es gelingt, den Ton von Kap. 1 zu halten — konkret, nicht utopisch, mit einer Prise Unbehagen.

**5.3 Cybersecurity + 5.4 Datenschutz + 5.5 Krypto-Risiken:** Das sind drei separate neue Abschnitte à 2-3 Seiten. Zusammen ~6.000-9.000 Wörter. **Das ist fast ein Viertel des aktuellen Buches.** Und sie verteilen sich über verschiedene Kapitel. **Risiko: Thematische Fragmentierung.** **Revidierte Empfehlung:** Cybersecurity und Krypto-Risiken gehören BEIDE in Kap. 12 (Risiken). Datenschutz gehört in Kap. 10 (Ethik). Nicht drei separate Maßnahmen, sondern zwei gezielte Erweiterungen bestehender Kapitel.

#### Phase 6 (Anhang) — Bewertung: ✅ GUT

Glossar, Ressourcen, Abbildungen — alles sinnvoll und risikoarm.

### Meta-Kritik: Was der Plan insgesamt falsch macht

1. **Zu viele gleichzeitige Baustellen.** 6 Phasen, ~40 Einzelmaßnahmen. Das ist für ein Buch von 42.000 Wörtern unverhältnismäßig. Gefahr: Jede Maßnahme einzeln gut, aber in der Summe zerstören sie den bestehenden Fluss.

2. **Keine Priorisierung zwischen Personas.** Klaus, Lena, Markus, Marco werden gleichgewichtig behandelt. Aber: Das Buch ist primär für Investoren geschrieben. Klaus und Marco sind die Kernzielgruppe. Lena und Markus sind Sekundär. Der Plan sollte das widerspiegeln.

3. **Unterschätzung des Schreibaufwands.** "Persönliche Anekdoten einbauen" klingt einfach, ist aber der schwierigste Teil — weil sie authentisch sein müssen. Das kann nur Thomas selbst liefern.

4. **Keine Qualitätskontrolle eingebaut.** Der Plan hat keine Review-Schleifen. Nach Phase 1 sollte geprüft werden, ob die Struktur noch stimmt, bevor Phase 2 beginnt.

---

## TEIL 2: REFINEMENT — DER ÜBERARBEITETE PLAN

### Grundsätze des revidierten Plans

1. **Weniger ist mehr.** Nur Maßnahmen umsetzen, die das Buch messbar verbessern, ohne den Fluss zu zerstören.
2. **Kern-Personas priorisieren:** Klaus (Finanzberater) und Marco (Krypto-Investor) vor Lena und Markus.
3. **Was nur Thomas schreiben kann, kennzeichnen** (persönliche Anekdoten, eigene Erfahrungen).
4. **Review nach jeder Phase.**
5. **Machbar in der tatsächlichen Kapitelstruktur** — keine Umbaumaßnahmen, die das Buch instabil machen.

---

### PHASE 1: Chirurgische Struktureingriffe (KRITISCH)

#### 1.1 Robotik-Duplikate in Kap. 2 eliminieren
- Den Abschnitt "Die Robotik-Landschaft: Mehr als Tesla und Boston Dynamics" **komplett streichen** (ca. 580 Wörter)
- In "Phase 4: Verkörperte KI" den konsolidierten Robotik-Text belassen
- Im KI-Labore-Abschnitt Robotik nur kurz andeuten: "Die Robotik-Player behandle ich in Phase 4"
- **Netto-Effekt:** -580 Wörter, keine Duplikate mehr, Phase 4 bleibt ausführlich

#### 1.2 Kap. 3b: Innere Struktur verbessern (NICHT aufteilen)
- 3 klare Zwischenüberschriften setzen:
  1. "Was Tokenisierung ist und warum sie diesmal funktioniert"
  2. "Die Stablecoin-Revolution: Warum Dollar auf der Blockchain die Welt verändern"
  3. "Demokratisierung oder neue Gatekeeper? Die Robinhood-Lektion"
- Die drei Szenarien (40%/45%/15%) als "subjektive Einschätzung des Autors" kennzeichnen
- **Kein Splitting** — der thematische Zusammenhang (Tokenisierung braucht Stablecoins) ist zu stark

#### 1.3 Kapitelnummerierung bereinigen
- Kap. 10b → Kap. 11 (Longevity)
- Alle folgenden Kapitel um 1 hochzählen: Kap. 11→12, 12→13, 13→14
- Kap. 3b und 3c bleiben als Unterkapitel (sie gehören thematisch zu "Krypto")
- Alle Querverweise im gesamten Buch prüfen und aktualisieren

#### 1.4 Kap. 4/7 Überlappung auflösen
- In Kap. 7 die wiederholte EU-AI-Act-Kritik streichen (stattdessen: Verweis auf Kap. 4)
- Autonome-Waffen-Abschnitt von Kap. 7 nach Kap. 10 (Ethik) verschieben
- Kap. 7 stärken mit: konkreten regulatorischen Handlungsempfehlungen für europäische Leser ("Was können Sie trotz MiCA tun?")

**Review-Checkpoint nach Phase 1:** Alle Kapitel durchlesen, prüfen ob die Struktur stimmt.

---

### PHASE 2: Humanizer-Pass (GEZIELT)

#### 2.1 Erstens/Zweitens/Drittens — nur wo es stört
- Jedes Vorkommen identifizieren
- **Regel:** Auflösen, wo die Nummerierung formelhaft wirkt und keinen Mehrwert hat. Belassen, wo sie den Lesefluss unterstützt (z.B. "DeepSeek bewies drei Dinge gleichzeitig" in Kap. 2 ist gut)
- Ziel: Maximal 3-4 bewusste Erstens/Zweitens/Drittens im gesamten Buch

#### 2.2 Em-Dashes — nur Ausreißer
- Nur eingreifen bei 3+ Gedankenstrichen pro Absatz
- Thomas' Grundstil mit Gedankenstrichen respektieren
- Fokus: Kap. 3b und Kap. 4

#### 2.3 Wortwiederholungen
- "fundamental" auf max. 8 reduzieren (statt 5 — in 42.000 Wörtern ist 8 akzeptabel)
- "transformativ" auf max. 3
- "entscheidend" variieren

#### 2.4 Schlussabsätze individualisieren
- Nur die Kapitel überarbeiten, deren Schlüsse tatsächlich generisch sind (Kap. 1, 5, 7)
- Kap. 2 hat bereits einen starken Schluss → nicht ändern
- Den dreifach ähnlichen "Kann ich es mir leisten?"-Schluss (Kap. 13/Vorwort/Epilog) differenzieren

---

### PHASE 3: Übergänge & Spannungsbogen

#### 3.1 Fehlende Kapitelübergänge ergänzen
Nur dort schreiben, wo der Übergang tatsächlich fehlt:
- Kap. 3c → Kap. 4 (fehlt)
- Kap. 5 → Kap. 6 (fehlt)
- Kap. 7 → Kap. 8 (fehlt)
- Kap. 9 → Kap. 10 (fehlt)
- Kap. 10 → Kap. 11/Longevity (fehlt)
- Kap. 2 → Kap. 3 (existiert bereits — nicht doppeln!)

#### 3.2 Robotik-Verweise in Kap. 8 bereinigen
- Wiederholte Figure AI/1X-Details durch Verweise auf Kap. 2 ersetzen
- Stattdessen: neue Zukunfts-Inhalte (Stückzahlen-Prognosen, Kostenverläufe)

---

### PHASE 4: Persona-gezielte Ergänzungen (PRIORISIERT)

#### Priorität A — Klaus (Finanzberater): höchster ROI

**4A.1 Vereinfachter Backtest (nur liquide Positionen)**
- Kap. 12 (Barbell): Backtest für die "sichere Seite" (NVIDIA, Big Tech ETFs, Bitcoin ETF) für 2022-2025
- Ehrlich: "Die asymmetrische Seite ist per Definition nicht backtestbar"
- 1 Tabelle, 1 Absatz Interpretation
- ~500 Wörter

**4A.2 Regulierte Produkte im Anhang**
- Anhang: "Umsetzung für deutsche Anleger" mit ETF-ISINs, ETPs, Depotbanken
- Stand-Datum prominent
- Verweis auf Website/Companion für aktuelle Daten
- ~800 Wörter

**4A.3 Worst-Case-Szenario**
- Kap. 13 (Risiken): Konkretes Drawdown-Szenario durchrechnen
- NVIDIA -60%, Bitcoin -80%, EU-Regulierung → Portfolioeffekt zeigen
- Demonstrieren, dass die sichere Seite den Drawdown abfängt
- ~600 Wörter

#### Priorität B — Marco (Krypto-Investor): spezifischer Mehrwert

**4B.1 Tokenomics-Tabelle**
- Anhang oder Kap. 12 (Barbell): OLAS, PEAQ, FET, RENDER
- Je 1 Zeile: Supply, Staking, Governance, Inflation, Revenue Share
- Stand-Datum, Verweis auf Live-Daten
- ~400 Wörter + Tabelle

**4B.2 Solana als komplementärer Layer**
- Kap. 3: Kurzer Absatz Solana neben Ethereum
- Nicht als Konkurrenz, sondern als komplementär (Mikrotransaktionen, DePIN)
- ~300 Wörter

**4B.3 On-Chain-Daten als Datenpunkte**
- Kap. 3: Stablecoin-Transaktionsvolumen (Visa-Vergleich)
- Kap. 3b: TVL in RWA-Protokollen
- Als Einzelzahlen in Fließtext, nicht als eigener Abschnitt
- ~200 Wörter verteilt

#### Priorität C — Markus (Bankangestellter): Zugänglichkeit

**4C.1 Glossar**
- Neuer Anhang: 40-50 Begriffe
- Alltagssprache, Analogien
- ~2.000 Wörter

**4C.2 Bankensektor + Bildung (kombiniert)**
- Kap. 6 (Menschlicher Preis): EIN Abschnitt "Was das für Berufe bedeutet — am Beispiel Banken"
- Inkl. Weiterbildungsempfehlungen (kurz)
- Max. 1.500 Wörter

**4C.3 Krypto-Analogien bei Erstverwendung**
- Kap. 3 und 3b: 5-6 Schlüsselbegriffe mit Alltagsanalogie ergänzen
- Im Fließtext, nicht als Fußnoten
- ~200 Wörter

#### Priorität D — Lena (Gründerin): minimal, da Sekundärzielgruppe

**4D.1 Open-Source-Absatz in Kap. 2 stärken**
- DeepSeek-Abschnitt: 2-3 Sätze zu "Was das für Startups bedeutet"
- ~100 Wörter

**4D.2 Gründer-Exkurs: GESTRICHEN**
- Risiko der Zielgruppen-Verwässerung zu hoch
- Lena holt bereits viel aus Kap. 5, 6, 11 — das Buch muss nicht alles für jeden sein

---

### PHASE 5: Inhaltliche Ergänzungen (REDUZIERT)

#### 5.1 Persönliche Anekdoten — NUR mit Thomas' Input
- **Markierung im Text:** An 3-4 Stellen einen Platzhalter setzen: "[PERSÖNLICHE ANEKDOTE: Thomas, hier wäre eine Geschichte aus deiner accessibleAI-Erfahrung perfekt — z.B. über Rechenkosten / Regulierungsfrust / KI-Ethik-Dilemma]"
- **Nicht selbst erfinden.** Thomas muss den Kern liefern. Wir können polieren.

#### 5.2 "Day in the Life 2030": VERSCHOBEN
- Zu riskant als KI-generierter Text (Kitsch-Gefahr)
- Besser: Thomas als separates Schreibprojekt vorschlagen

#### 5.3 Cybersecurity + Krypto-Risiken → Kap. 13 (Risiken)
- EINEN kombinierten Abschnitt: "Technische Risiken der Maschinenökonomie"
- Smart-Contract-Bugs, Hacks, Depegging, KI-Cyberangriffe
- ~800 Wörter

#### 5.4 Datenschutz → Kap. 10 (Ethik)
- In bestehenden Abschnitt zur Eigentumsfrage integrieren
- "Wem gehören die Daten einer Maschinen-DAO?" + BCI-Datenrisiken
- ~500 Wörter

---

### PHASE 6: Anhang

#### 6.1 Glossar (~2.000 Wörter)
#### 6.2 Regulierte Produkte für deutsche Anleger (~800 Wörter)
#### 6.3 Tokenomics-Vergleichstabelle (~400 Wörter)
#### 6.4 Weiterführende Ressourcen (~500 Wörter)

---

## Wortbilanz des revidierten Plans

| Maßnahme | Wörter-Effekt |
|----------|--------------|
| Robotik-Duplikate streichen | -580 |
| Kap. 7 Überlappung streichen | -300 |
| Humanizer-Pass (Kürzungen) | -200 |
| Backtest (Klaus) | +500 |
| Worst-Case (Klaus) | +600 |
| Solana (Marco) | +300 |
| On-Chain-Daten (Marco) | +200 |
| Bankensektor + Bildung (Markus) | +1.500 |
| Krypto-Analogien (Markus) | +200 |
| Open-Source Startup-Bezug (Lena) | +100 |
| Cybersecurity/Krypto-Risiken (Kap. 13) | +800 |
| Datenschutz (Kap. 10) | +500 |
| Kapitelübergänge (5 Stück) | +250 |
| Glossar (Anhang) | +2.000 |
| Regulierte Produkte (Anhang) | +800 |
| Tokenomics-Tabelle (Anhang) | +400 |
| Weiterführende Ressourcen (Anhang) | +500 |
| **Netto** | **+~7.070** |

**Neuer Gesamtumfang:** ~49.500 Wörter → im Zielkorridor 50.000-55.000 (Kap. 12 Risiken muss ohnehin noch ausgebaut werden, +2.000-3.000 Wörter auf die 884 aktuell)

---

## Umsetzungsreihenfolge

| Schritt | Was | Abhängigkeiten |
|---------|-----|---------------|
| 1 | Phase 1.1: Robotik-Duplikate streichen | Keine |
| 2 | Phase 1.3: Kapitelnummerierung (10b→11, Folgenummern) | Keine |
| 3 | Phase 1.4: Kap. 4/7 Überlappung auflösen | Keine |
| 4 | Phase 1.2: Kap. 3b Zwischenüberschriften | Keine |
| **REVIEW-CHECKPOINT** | Alle Kapitel durchlesen | 1-4 abgeschlossen |
| 5 | Phase 2: Humanizer-Pass (alle Kapitel) | Phase 1 abgeschlossen |
| 6 | Phase 3: Kapitelübergänge | Phase 1+2 abgeschlossen |
| 7 | Phase 4A: Klaus (Backtest, Worst-Case) | Phase 1 abgeschlossen |
| 8 | Phase 4B: Marco (Solana, Tokenomics, On-Chain) | Phase 1 abgeschlossen |
| 9 | Phase 4C: Markus (Krypto-Analogien, Bankensektor) | Phase 1 abgeschlossen |
| 10 | Phase 4D: Lena (Open-Source-Absatz) | Phase 1 abgeschlossen |
| 11 | Phase 5.3+5.4: Cybersecurity + Datenschutz | Phase 1 abgeschlossen |
| 12 | Phase 5.1: Anekdoten-Platzhalter setzen | Keine |
| 13 | Phase 6: Anhang (Glossar, Produkte, Tokenomics, Ressourcen) | Phase 4 abgeschlossen |
| **FINAL REVIEW** | Gesamtes Buch durchlesen | Alles abgeschlossen |

---

## Was ich NICHT automatisiert umsetzen kann/sollte

1. **Persönliche Anekdoten** — nur Thomas kann authentische Geschichten liefern
2. **"Day in the Life 2030"** — zu riskant als KI-generierter Erzähltext
3. **Barbell-Backtest mit echten Zahlen** — erfordert Finanzmarktdaten-Recherche und sorgfältige Berechnung
4. **Gründer-Perspektive** — gestrichen (Zielgruppen-Verwässerung)

---

*Dieser revidierte Plan reduziert die Maßnahmen von ~40 auf ~20, priorisiert nach Persona-Relevanz, und hält das Buch im Zielkorridor von 50.000-55.000 Wörtern.*
