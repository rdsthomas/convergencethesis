# Strukturplan: Zwei Websites, zwei Missionen

## theaispecies.world — Das Buch verkaufen

**Mission:** Jeder Besucher soll das Buch kaufen wollen. Jede Seite führt zum Kauf-Button.

### Seitenstruktur

```
theaispecies.world/
├── / (Landing Page)                    ← Hero + Buch-Pitch + CTA "Jetzt kaufen"
├── /buch                               ← Kapitelübersicht, Leseprobe, Rezensionen
├── /leser                              ← Companion-Bereich (Zugangscode aus dem Buch)
│   ├── /leser/musterportfolio          ← Das AI-Species-Musterportfolio (live aktualisiert)
│   ├── /leser/watchlist                ← Firmen-Watchlist aus dem Buch
│   └── /leser/tools                    ← Rechner, Checklisten, Downloads
├── /newsletter                         ← AI Species Weekly Signup
├── /autor                              ← Thomas Huhn — kurz, persönlich, Skin in the Game
├── /presse                             ← Presskit, Cover-Download, Zitate, Pressetext
└── /datenschutz + /impressum
```

### Landing Page — Aufbau

1. **Hero:** Buchtitel + Cover + ein Satz ("Die Investment-Blaupause für den KI-Tsunami") + Kauf-Button
2. **Das Problem:** 3 Sätze — warum die meisten Anleger die größte Vermögensverschiebung der Geschichte verpassen werden
3. **Die These:** Convergence Thesis in 50 Wörtern — mit Link zu convergencethesis.com für die tiefe Analyse
4. **Was im Buch steht:** 5-6 Kapitel-Highlights als Appetithäppchen
5. **Für wen:** "Dieses Buch ist für..." (kein "für alle" — klare Zielgruppe)
6. **Über den Autor:** Foto, 3 Sätze, "Skin in the Game"
7. **Social Proof:** Erste Rezensionen, Pressezitate
8. **CTA:** Kauf-Buttons (Amazon, eBook, Buchhandel)
9. **Newsletter-Teaser:** "Bleib dran — AI Species Weekly"

### Ton & Design
- Verkaufsorientiert, aber nicht marktschreierisch
- Dunkel, professionell, etwas Editorial-Magazin-Feeling
- Große Typographie, wenig Ablenkung
- Mobil-first (die meisten kommen über Social/Newsletter)

---

## convergencethesis.com — Die Autorität aufbauen

**Mission:** Thomas Huhn als **die** deutschsprachige Stimme für die Konvergenz von KI, Robotik und Krypto positionieren. Akademischer Anspruch, aber zugänglich.

### Seitenstruktur

```
convergencethesis.com/
├── / (Hub)                             ← "Die Convergence Thesis" — Kurzfassung + Einladung zum Diskurs
├── /thesis                             ← Die vollständige These (bestehendes Thesis-Essay, erweitert)
├── /research                           ← Wöchentliche Deep-Research-Artikel (aus Weekly Research)
│   ├── /research/kw10-2026             ← Einzelne Research-Posts
│   └── ...
├── /forum                              ← Diskussionsforum (Disqus, Discourse, oder eigene Lösung)
├── /daten                              ← Live-Dashboards, Charts, Marktdaten
│   ├── /daten/crypto-tracker           ← Token-Preise der Buch-Picks
│   └── /daten/macro                    ← Makro-Indikatoren (Liquidität, DXY, M2)
├── /autor                              ← Ausführlicheres Profil, Veröffentlichungen, Vorträge
├── /buch                               ← Cross-Link: "Das Buch zur These → theaispecies.world"
└── /datenschutz + /impressum
```

### Hub-Seite (/) — Aufbau

1. **Die These in einem Satz:** "KI, Robotik und Krypto konvergieren zur Maschinenökonomie — wer das versteht, investiert richtig."
2. **Die Kurzfassung:** 500 Wörter — die These als intellektuelles Framework
3. **Neueste Research-Artikel:** 3 Karten mit den letzten Deep-Dives
4. **Forum-Teaser:** "Diskutiere die These"
5. **Das Buch:** "Die vollständige Analyse → theaispecies.world" (1 Box, dezent)
6. **Über den Autor:** Akademisch/beruflicher Fokus

### Ton & Design
- Sachlich, datengetrieben, nüchtern
- Hell, clean, viel Weißraum — denke an academic papers, nicht an Verlagswerbung
- Visualisierungen und Charts statt Marketing-Buzzwords
- Einladung zum Diskurs ("Ich kann falsch liegen. Sagen Sie mir wo.")

---

## Content-Zuordnung: Was gehört wohin?

| Content | theaispecies.world | convergencethesis.com |
|---------|:------------------:|:---------------------:|
| Buchverkauf, Kauf-CTAs | ✅ Hauptzweck | ❌ Nur Cross-Link |
| Musterportfolio (Leser) | ✅ /leser/ (mit Code) | ❌ |
| Watchlist (Leser) | ✅ /leser/ (mit Code) | ❌ |
| Newsletter (AI Species Weekly) | ✅ Signup hier | Verweis → theaispecies.world |
| Wöchentliche Research-Artikel | Teaser/Zusammenfassung | ✅ Volltext |
| Diskussionsforum | ❌ | ✅ /forum/ |
| Die These (Essay) | Kurzversion im Pitch | ✅ Volltext /thesis/ |
| Pressematerial | ✅ /presse/ | ❌ |
| Autor-Profil | Kurz + persönlich | Ausführlich + akademisch |
| Live-Daten/Charts | ❌ | ✅ /daten/ |
| Leseprobe | ✅ /buch/ | ❌ |
| Rezensionen | ✅ / (Social Proof) | ❌ |

---

## Cross-Linking-Strategie

**theaispecies.world → convergencethesis.com:**
- "Die These hinter dem Buch: convergencethesis.com"
- Footer-Link: "Zur Research-Plattform"
- Im Leser-Bereich: "Diskutiere auf convergencethesis.com/forum"

**convergencethesis.com → theaispecies.world:**
- Dezenter Banner: "Die vollständige Analyse: The AI Species — Jetzt bestellen"
- In Research-Artikeln: "Mehr dazu in Kapitel X → theaispecies.world/buch"
- Autor-Seite: Buch als prominenteste Veröffentlichung

---

## Newsletter — Wo lebt er?

**AI Species Weekly** lebt auf **theaispecies.world/newsletter**.

**Begründung:** Der Newsletter ist das direkte Kommunikationsmittel des Autors an seine Leser. Er verkauft Bücher, bindet Leser, baut Community. Das ist Buch-Welt, nicht Theorie-Welt.

Die Research-Artikel auf convergencethesis.com sind davon getrennt — sie werden als Blog-Posts veröffentlicht (öffentlich, indexierbar, SEO-relevant). Der Newsletter kann auf die besten Research-Posts verlinken, aber der Newsletter selbst gehört zum Buch.

**Buttondown:** Username von `convergencethesis` auf `theaispecies` ändern (oder neuen Account).

---

## Technische Umsetzung

| Aspekt | theaispecies.world | convergencethesis.com |
|--------|-------------------|----------------------|
| Framework | Hugo (neu) | Hugo (bestehend, anpassen) |
| Hosting | Cloudflare Pages | Cloudflare Pages (bleibt) |
| Newsletter | Buttondown (neuer Handle) | — |
| Forum | — | Discourse / Disqus / Giscus |
| Analytics | Plausible oder CF Web Analytics | Plausible oder CF Web Analytics |
| E-Mail | thomas@theaispecies.world | thomas@convergencethesis.com |

---

## Prioritäten

1. **Sofort:** theaispecies.world als Buch-Landing aufsetzen (das Buch geht bald live)
2. **Parallel:** convergencethesis.com anpassen (Buch-spezifische Inhalte rausnehmen, Research rein)
3. **Woche 1-2:** Forum auf convergencethesis.com einrichten
4. **Laufend:** Wöchentliche Research-Posts auf convergencethesis.com, Newsletter auf theaispecies.world
