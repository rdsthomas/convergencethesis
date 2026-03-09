#!/usr/bin/env python3
"""
Build EPUB from Maschinenwelt v5 Google Doc — with all 9 style elements.

Pipeline: Google Doc → DOCX export → Pandoc Markdown → add style elements → Pandoc EPUB

Style elements:
1. Pull Quotes — one per chapter, centered, larger font
2. Callout Boxes — gray-background info boxes
3. Key Takeaways — end-of-chapter summary boxes
4. Drop Caps — CSS ::first-letter (automatic)
5. Ornamental Breaks — ✦ between sections
6. Epigraphs — chapter-opening quotes
7. Marginalien — skipped (not suited for EPUB)
8. Checklists — action items for investment chapters
9. Chapter Openers — combined: number + title + ornament + epigraph + drop cap
"""

import json
import os
import re
import subprocess
import urllib.request
import urllib.parse

DOC_ID = '1JF7Kei019q0iunIISa-fCq7Y4aLcHWHmkjBOb7MBlms'
BUILD_DIR = '/root/clawd/projects/convergencethesis/epub-build'
COVER = os.path.join(BUILD_DIR, 'images', 'cover.png')
OUTPUT = os.path.join(BUILD_DIR, 'Maschinenwelt-v5-styled.epub')
DOCX_PATH = '/tmp/maschinenwelt-v5.docx'
MD_PATH = '/tmp/maschinenwelt-v5-styled.md'

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA: All style element content
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EPIGRAPHS = {
    'Kapitel 1': ('Die Zukunft ist schon da — sie ist nur ungleich verteilt.', 'William Gibson'),
    'Kapitel 2': ('Wir überschätzen immer die Veränderung der nächsten zwei Jahre und unterschätzen die Veränderung der nächsten zehn.', 'Bill Gates'),
    'Kapitel 3': ('Geld ist nur ein Werkzeug. Es bringt dich überall hin, aber es ersetzt dich nicht als Fahrer.', 'Ayn Rand'),
    'Kapitel 4': ('In der Kryptographie vertrauen wir.', 'Frei nach „In God We Trust"'),
    'Kapitel 5': ('Das Netz kennt keinen Schlaf.', 'Kevin Kelly'),
    'Kapitel 6': ('Wer die Chips kontrolliert, kontrolliert die Zukunft.', 'Frei nach Jensen Huang'),
    'Kapitel 7': ('Zivilisation ist im Wesentlichen ein Wettlauf um Energie.', 'Frederick Soddy'),
    'Kapitel 8': ('Wer einen Sinn zu leben hat, erträgt fast jedes Wie.', 'Viktor Frankl'),
    'Kapitel 9': ('Regulierung ist der Versuch, mit den Werkzeugen von gestern die Probleme von morgen zu lösen.', ''),
    'Kapitel 10': ('Schwerer-als-Luft-Flugmaschinen sind unmöglich.', 'Lord Kelvin, 1895'),
    'Kapitel 11': ('Jede hinreichend fortgeschrittene Technologie ist von Magie nicht zu unterscheiden.', 'Arthur C. Clarke'),
    'Kapitel 12': ('Cogito, ergo sum — aber was, wenn die Maschine auch denkt?', 'Frei nach Descartes'),
    'Kapitel 13': ('Der erste Mensch, der 1.000 Jahre alt wird, lebt möglicherweise bereits.', 'Aubrey de Grey'),
    'Kapitel 14': ('Rule No. 1: Never lose money. Rule No. 2: Never forget Rule No. 1.', 'Warren Buffett'),
    'Kapitel 15': ('Es ist schwer, Vorhersagen zu machen, besonders über die Zukunft.', 'Niels Bohr (zugeschrieben)'),
    'Kapitel 16': ('Die beste Zeit, einen Baum zu pflanzen, war vor zwanzig Jahren. Die zweitbeste Zeit ist jetzt.', 'Chinesisches Sprichwort'),
}

PULL_QUOTES = {
    'Vorwort': 'Ohne Besitz wirst du nicht glücklich sein. Ohne Besitz hast du keine Sicherheit. Ohne Besitz hast du keine Verhandlungsmacht.',
    'Kapitel 1': 'Und diesmal ist die Transformation radikaler als alles, was wir kennen.',
    'Kapitel 2': 'Wenn ich Klavier übe, werden Sie dadurch nicht besser. Maschinen lernen anders: Jede Instanz teilt ihr Wissen sofort mit allen anderen.',
    'Kapitel 3': 'Maschinengeld. Das Geld, das Maschinen brauchen, um in einer Welt zu funktionieren, die sie selbst miterschaffen.',
    'Kapitel 4': 'Wer sein Geld nicht selbst verwahrt, besitzt es nicht wirklich.',
    'Kapitel 5': 'Was entsteht, wenn man das zusammensetzt? Unternehmen, die keine Menschen brauchen, um zu funktionieren.',
    'Kapitel 6': 'Wir konnten keinen europäischen Hoster finden, der das Modell legal betreiben konnte.',
    'Kapitel 7': 'Wer die Energie kontrolliert, kontrolliert das Tempo der KI-Revolution.',
    'Kapitel 8': 'Die größte Gefahr der Maschinenökonomie ist nicht der Kontrollverlust über KI. Es ist der Verlust des Antriebs bei den Menschen.',
    'Kapitel 9': 'Ob der Roboter besteuert wird oder nicht — er ersetzt trotzdem die Arbeit.',
    'Kapitel 10': 'Unternehmen, die KI nicht adoptieren, verschwinden.',
    'Kapitel 11': 'Die Adoption wird schnell gehen: Menschen müssen keine neue Fähigkeit erlernen, um zu sprechen.',
    'Kapitel 12': 'Wir können nicht einmal bei einem anderen Menschen beweisen, dass er bewusst ist.',
    'Kapitel 13': 'Sam Altman hat 180 Millionen Dollar in Retro Biosciences investiert. Das Ziel: zehn zusätzliche gesunde Lebensjahre für jeden Menschen.',
    'Kapitel 14': 'Wer in einem Crash kein Cash hat, kann nur zuschauen, wie andere die Schnäppchen kaufen.',
    'Kapitel 15': '2011 fiel Bitcoin um 93 Prozent. Jedes Mal schrieben die Medien Nachrufe. Jedes Mal lag er danach höher als je zuvor.',
    'Kapitel 16': 'Die Frage ist nicht: Kann ich es mir leisten, jetzt zu investieren? Die Frage ist: Kann ich es mir leisten, es nicht zu tun?',
    'Epilog': 'Ich werde nicht aufhören, nach der Antwort zu suchen.',
}

KEY_TAKEAWAYS = {
    'Kapitel 1': [
        'KI, Robotik und Kryptowährungen konvergieren zur größten wirtschaftlichen Transformation seit der Dampfmaschine.',
        'Anders als frühere Transformationen laufen alle drei gleichzeitig und beschleunigen sich gegenseitig.',
        'Infrastruktur-Investoren profitieren historisch am stärksten — nicht die Anwendungs-Hypes.',
    ],
    'Kapitel 2': [
        'Vier Phasen: Werkzeug → Mitarbeiter → Agent → Roboter.',
        'Jede Phase vergrößert den adressierbaren Markt um eine Größenordnung.',
        'Null-Marginalkosten und exponentielles Lernen schaffen disruptive Kostenvorteile.',
    ],
    'Kapitel 3': [
        'Maschinen brauchen eigenes Geld, weil das traditionelle Bankensystem sie ausschließt.',
        'Krypto und Smart Contracts sind der native Zahlungskanal für autonome Agenten.',
        'Die Machine-to-Machine Economy funktioniert bereits heute (x402, autonome Fahrzeuge).',
    ],
    'Kapitel 4': [
        'Tokenisierung demokratisiert den Zugang zu bisher illiquiden Assets.',
        'BlackRock, JPMorgan und Goldman Sachs sind bereits aktiv — das ist kein Krypto-Hype mehr.',
        'Self-Custody wird in einer CBDC-Welt zum Menschenrecht.',
    ],
    'Kapitel 5': [
        'DAOs ermöglichen Unternehmen ohne menschliche Führung.',
        'Smart Contracts + KI-Agenten = autonome Wirtschaftseinheiten.',
        'Token-Halter profitieren — aber die Zugangsfrage verschärft die Ungleichheit.',
    ],
    'Kapitel 6': [
        'Die USA dominieren das KI-Ökosystem: Hardware, Cloud, Venture Capital.',
        'China holt auf, Europa reguliert sich ins Abseits.',
        'TSMC in Taiwan ist das geopolitische Nadelöhr der gesamten KI-Revolution.',
    ],
    'Kapitel 7': [
        'Der Energieverbrauch von KI wächst exponentiell.',
        'Kernenergie ist die einzige skalierbare Lösung für den Baseload-Bedarf.',
        'Tech-Giganten kaufen Kernkraftwerke — Uran wird zum strategischen Asset.',
    ],
    'Kapitel 8': [
        '30 bis 50 Prozent der Wissensarbeit könnten automatisiert werden.',
        'Die Sinnkrise ist das größere Risiko als der reine Jobverlust.',
        'Anpassungsfähigkeit und KI-Kompetenz werden zu Überlebensfähigkeiten.',
    ],
    'Kapitel 9': [
        'Der EU AI Act bremst europäische KI-Innovation.',
        'Die Roboter-Steuer-Debatte greift zu kurz.',
        'Regulierung kann die Transformation verlangsamen, aber nicht aufhalten.',
    ],
    'Kapitel 10': [
        '2026–2028: Stille Revolution — KI-Agenten senken Kosten um 90 Prozent.',
        '2028–2031: Der Wendepunkt — physische Robotik erreicht die Massenproduktion.',
        '2031–2035: Neue Normalität — die autonome Wirtschaft ist Realität.',
    ],
    'Kapitel 11': [
        'Voice und Gesten ersetzen Tastatur und Maus als primäre Interfaces.',
        'Brain-Computer Interfaces erreichen in den 2030ern klinische Reife.',
        'Synthetische Realität (BCI + KI-generierte Welten) wird die nächste Plattform.',
    ],
    'Kapitel 12': [
        'Bewusstsein ist wissenschaftlich nicht definiert — weder bei Menschen noch bei Maschinen.',
        'Eigentumsfragen bei KI-generierten Werken sind rechtlich ungelöst.',
        'Die Grenze zwischen Mensch und Maschine verschwimmt — mit ethischen Konsequenzen.',
    ],
    'Kapitel 13': [
        'Altern ist kein unausweichliches Schicksal, sondern ein biologischer Prozess.',
        'Smart Money investiert Milliarden in Longevity-Forschung.',
        'Senolytika, Epigenetik und KI-beschleunigte Wirkstoffentwicklung sind die Schlüsseltechnologien.',
    ],
    'Kapitel 14': [
        'Barbell-Strategie: 60–70% sicherer Kern plus 30–40% asymmetrische Wetten.',
        'Konkretes Beispiel-Portfolio mit 100.000 Euro Ausgangsbasis.',
        'Regel Nr. 1: Nie mehr riskieren, als man bereit ist zu verlieren.',
    ],
    'Kapitel 15': [
        'Eine KI-Blase ist möglich, aber die Infrastruktur-Investitionen haben reale Gegenwerte.',
        'Bitcoin-Volatilität sinkt historisch mit jeder Marktkapitalisierungsstufe.',
        'Die Barbell-Strategie schützt vor allen Szenarien — auch dem Worst Case.',
    ],
    'Kapitel 16': [
        'Das Zeitfenster für asymmetrische Renditen schließt sich — in Jahren, nicht Jahrzehnten.',
        'Warten bis der „Beweis" da ist bedeutet, die höchsten Preise zu zahlen.',
        'Definiter Optimismus: Aktiv handeln, statt passiv hoffen.',
    ],
}

CHECKLISTS = {
    'Kapitel 14': [
        'Portfolio-Allokation festlegen: Kern / Asymmetrisch / Cash',
        'Krypto-Wallet einrichten — Self-Custody!',
        'Erste Positionen aufbauen: ETFs und Bitcoin',
        'Rebalancing-Termine im Kalender eintragen (quartalsweise)',
    ],
    'Kapitel 15': [
        'Persönliche Risikotoleranz ehrlich definieren',
        'Stop-Loss-Strategie festlegen — und daran halten',
        'Worst-Case-Szenario durchrechnen: Können Sie den Verlust aushalten?',
        'Cash-Reserve sicherstellen (mindestens 6 Monate Lebenshaltung)',
    ],
    'Kapitel 16': [
        'Dieses Buch nicht weglegen — handeln',
        'convergencethesis.com besuchen für laufende Updates',
        'Eigene Recherche starten mit den Quellen im Anhang',
        'Ersten Schritt innerhalb von 48 Stunden machen',
    ],
}

# Pull quote trigger phrases (to find the right paragraph and insert after it)
PULL_QUOTE_TRIGGERS = {
    'Vorwort': 'Ohne Besitz wirst du nicht glücklich sein',
    'Kapitel 1': 'Und diesmal ist die Transformation radikaler',
    'Kapitel 2': 'Wenn ich Klavier übe',
    'Kapitel 3': 'Maschinengeld. Das Geld, das Maschinen brauchen',
    'Kapitel 4': 'Wer sein Geld nicht selbst verwahrt',
    'Kapitel 5': 'Unternehmen, die keine Menschen brauchen',
    'Kapitel 6': 'keinen europäischen Hoster finden',
    'Kapitel 7': 'Wer die Energie kontrolliert',
    'Kapitel 8': 'nicht der Kontrollverlust über KI',
    'Kapitel 9': 'Ob der Roboter besteuert wird',
    'Kapitel 10': 'die KI nicht adoptieren, verschwinden',
    'Kapitel 11': 'keine neue Fähigkeit erlernen, um zu sprechen',
    'Kapitel 12': 'nicht einmal bei einem anderen Menschen beweisen',
    'Kapitel 13': '180 Millionen Dollar in Retro Biosciences',
    'Kapitel 14': 'kein Cash hat, kann nur zuschauen',
    'Kapitel 15': '2011 fiel Bitcoin um 93 Prozent',
    'Kapitel 16': 'Kann ich es mir leisten, es nicht zu tun',
    'Epilog': 'nicht aufhören, nach der Antwort zu suchen',
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EPUB_CSS = """
/* ===== BASE ===== */
body {
    font-family: Georgia, "Times New Roman", serif;
    line-height: 1.6;
    margin: 1em;
    color: #1a1a1a;
}

/* ===== HEADINGS ===== */
h1 {
    font-size: 1.8em;
    text-align: center;
    margin-top: 3em;
    margin-bottom: 0.5em;
    page-break-before: always;
    letter-spacing: 0.05em;
}
h2 {
    font-size: 1.4em;
    margin-top: 2em;
    margin-bottom: 0.8em;
    page-break-before: always;
}
h3 {
    font-size: 1.15em;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}

/* ===== BODY TEXT ===== */
p {
    text-indent: 1.5em;
    margin-top: 0;
    margin-bottom: 0.3em;
    text-align: justify;
}
h1 + p, h2 + p, h3 + p, hr + p, blockquote + p,
.epigraph + p, .pull-quote + p, .callout-box + p,
.key-takeaways + p, .checklist-box + p {
    text-indent: 0;
}

/* ===== DROP CAPS (Element 4) ===== */
.chapter-start::first-letter {
    font-size: 3.2em;
    float: left;
    line-height: 0.8;
    margin-right: 0.08em;
    margin-top: 0.05em;
    font-weight: bold;
    color: #2c3e50;
}

/* ===== IMAGES ===== */
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1em auto;
}
.caption, figcaption, p em:only-child {
    text-align: center;
    font-style: italic;
    font-size: 0.9em;
    margin-top: 0.5em;
    margin-bottom: 1em;
    text-indent: 0;
}

/* ===== EPIGRAPH (Element 6) ===== */
.epigraph {
    text-align: right;
    font-style: italic;
    font-size: 0.95em;
    margin: 1.5em 1em 0.5em 2em;
    padding: 0;
    color: #555;
    text-indent: 0;
}
.epigraph-source {
    text-align: right;
    font-size: 0.85em;
    color: #777;
    margin: 0 1em 2em 2em;
    text-indent: 0;
}

/* ===== PULL QUOTE (Element 1) ===== */
.pull-quote {
    text-align: center;
    font-size: 1.2em;
    font-style: italic;
    font-weight: bold;
    color: #2c3e50;
    margin: 2em 1.5em;
    padding: 1em 0;
    border-top: 2px solid #bdc3c7;
    border-bottom: 2px solid #bdc3c7;
    text-indent: 0;
    line-height: 1.4;
}

/* ===== CALLOUT BOX (Element 2) ===== */
.callout-box {
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    border-left: 4px solid #2c3e50;
    padding: 1em 1.2em;
    margin: 1.5em 0;
    font-size: 0.95em;
    line-height: 1.5;
    text-indent: 0;
}
.callout-box p {
    text-indent: 0;
    margin-bottom: 0.4em;
}
.callout-title {
    font-weight: bold;
    font-size: 1em;
    margin-bottom: 0.5em;
    color: #2c3e50;
    text-indent: 0;
}

/* ===== KEY TAKEAWAYS (Element 3) ===== */
.key-takeaways {
    background-color: #eef3f7;
    border: 1px solid #c8d6e0;
    border-radius: 4px;
    padding: 1em 1.2em;
    margin: 2em 0;
    text-indent: 0;
}
.key-takeaways p {
    text-indent: 0;
}
.takeaway-title {
    font-weight: bold;
    font-size: 1.05em;
    color: #2c3e50;
    margin-bottom: 0.5em;
    text-indent: 0;
}
.takeaway-item {
    margin-bottom: 0.4em;
    padding-left: 1.5em;
    text-indent: -1.2em;
    text-align: left;
}

/* ===== CHECKLIST (Element 8) ===== */
.checklist-box {
    background-color: #f0f7f0;
    border: 1px solid #b8d4b8;
    border-radius: 4px;
    padding: 1em 1.2em;
    margin: 2em 0;
    text-indent: 0;
}
.checklist-box p {
    text-indent: 0;
}
.checklist-title {
    font-weight: bold;
    font-size: 1.05em;
    color: #2d572c;
    margin-bottom: 0.5em;
    text-indent: 0;
}
.checklist-item {
    margin-bottom: 0.4em;
    padding-left: 1.5em;
    text-indent: 0;
    text-align: left;
}

/* ===== ORNAMENTAL BREAK (Element 5) ===== */
.ornamental-break {
    text-align: center;
    margin: 2em 0;
    font-size: 1.2em;
    color: #888;
    letter-spacing: 0.5em;
    text-indent: 0;
}
hr.ornamental {
    border: none;
    text-align: center;
    margin: 2em 0;
}
hr.ornamental::after {
    content: "✦";
    color: #888;
    font-size: 1.2em;
    letter-spacing: 0.5em;
}

/* ===== BLOCKQUOTES ===== */
blockquote {
    margin: 1em 2em;
    font-style: italic;
    border-left: 3px solid #ccc;
    padding-left: 1em;
}

/* ===== IMPRESSUM ===== */
.impressum { font-size: 0.85em; line-height: 1.4; }

/* ===== LISTS ===== */
ul, ol { margin: 0.5em 0 0.5em 2em; }
li { margin-bottom: 0.3em; }
"""


def get_access_token():
    with open('/tmp/gog-token.json') as f:
        tok = json.load(f)
    with open('/root/.config/gogcli/credentials.json') as f:
        creds = json.load(f)
    data = urllib.parse.urlencode({
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'refresh_token': tok['refresh_token'],
        'grant_type': 'refresh_token'
    }).encode()
    req = urllib.request.Request('https://oauth2.googleapis.com/token', data=data)
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())['access_token']


def download_docx(token):
    if os.path.exists(DOCX_PATH) and os.path.getsize(DOCX_PATH) > 1000000:
        print(f"  Using cached DOCX: {os.path.getsize(DOCX_PATH)/1024/1024:.1f} MB")
        return
    export_url = f'https://docs.google.com/document/d/{DOC_ID}/export?format=docx'
    req = urllib.request.Request(export_url, headers={'Authorization': f'Bearer {token}'})
    resp = urllib.request.urlopen(req)
    docx_data = resp.read()
    with open(DOCX_PATH, 'wb') as f:
        f.write(docx_data)
    print(f"  DOCX downloaded: {len(docx_data)/1024/1024:.1f} MB")


def docx_to_markdown():
    result = subprocess.run(
        ['pandoc', DOCX_PATH, '-t', 'markdown', '--wrap=none', '--extract-media=/tmp/epub-media'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr}")
        return None
    return result.stdout


def get_chapter_key(heading_text):
    """Extract chapter key from heading text for lookup in our data dicts."""
    # "Kapitel 1: Am Anfang..." -> "Kapitel 1"
    m = re.match(r'(Kapitel \d+)', heading_text)
    if m:
        return m.group(1)
    if 'Vorwort' in heading_text:
        return 'Vorwort'
    if 'Epilog' in heading_text:
        return 'Epilog'
    return None


def make_epigraph_md(chapter_key):
    """Generate markdown for an epigraph."""
    if chapter_key not in EPIGRAPHS:
        return ''
    quote, source = EPIGRAPHS[chapter_key]
    lines = []
    lines.append('')
    lines.append(f'<div class="epigraph">„{quote}"</div>')
    if source:
        lines.append(f'<div class="epigraph-source">— {source}</div>')
    else:
        lines.append(f'<div class="epigraph-source"></div>')
    lines.append('')
    return '\n'.join(lines)


def make_pull_quote_md(chapter_key):
    """Generate markdown for a pull quote."""
    if chapter_key not in PULL_QUOTES:
        return ''
    quote = PULL_QUOTES[chapter_key]
    return f'\n<div class="pull-quote">„{quote}"</div>\n'


def make_key_takeaways_md(chapter_key):
    """Generate markdown for key takeaways box."""
    if chapter_key not in KEY_TAKEAWAYS:
        return ''
    items = KEY_TAKEAWAYS[chapter_key]
    lines = ['', '<div class="key-takeaways">', '<p class="takeaway-title">📌 Auf einen Blick</p>']
    for item in items:
        lines.append(f'<p class="takeaway-item">◆ {item}</p>')
    lines.append('</div>')
    lines.append('')
    return '\n'.join(lines)


def make_checklist_md(chapter_key):
    """Generate markdown for a checklist box."""
    if chapter_key not in CHECKLISTS:
        return ''
    items = CHECKLISTS[chapter_key]
    lines = ['', '<div class="checklist-box">', '<p class="checklist-title">✅ Was Sie jetzt tun können</p>']
    for item in items:
        lines.append(f'<p class="checklist-item">☐ {item}</p>')
    lines.append('</div>')
    lines.append('')
    return '\n'.join(lines)


def fix_markdown(md):
    """
    Fix markdown for proper EPUB structure and add all 9 style elements.
    """
    lines = md.split('\n')
    output = []

    # Add YAML front matter
    output.append('---')
    output.append('title: "Maschinenwelt"')
    output.append('subtitle: "Besitze sie, oder sie besitzen dich"')
    output.append('author: "Thomas Huhn"')
    output.append('date: "2026"')
    output.append('lang: de-DE')
    output.append('rights: "© 2026 Thomas Huhn. Alle Rechte vorbehalten."')
    output.append('---')
    output.append('')

    skip_toc = False
    skip_title = True
    current_chapter_key = None
    pull_quote_inserted = {}  # Track which chapters got their pull quote
    first_para_after_heading = False  # For drop cap class
    chapter_start_pending = False
    in_backmatter = False  # Set to True after Danksagung/Endnotes

    i = 0
    while i < len(lines):
        line = lines[i]

        # Skip raw title/cover lines at the very beginning (before Impressum)
        if skip_title:
            if line.startswith('#'):
                skip_title = False
            else:
                i += 1
                continue

        # Skip Google Docs TOC section (appears between Impressum and Vorwort)
        # The TOC consists of indented links like "> [[Kapitel 1...]{.underline}]"
        # or "## **Inhaltsverzeichnis**" in some exports
        if re.match(r'^##\s+\*\*Inhaltsverzeichnis\*\*', line):
            skip_toc = True
            i += 1
            continue
        if skip_toc:
            if re.match(r'^##\s+\*\*(?!Inhaltsverzeichnis)', line):
                skip_toc = False
            else:
                i += 1
                continue
        # Also skip TOC-like lines (indented links to chapters)
        if re.match(r'^>\s*\[?\[', line) or re.match(r'^\[?\[\[', line):
            i += 1
            continue

        # === IMAGE + CAPTION FIX ===
        img_caption_pattern = r'^(!\[[^\]]*\]\([^)]+\))\{[^}]*\}\*(.+?)\*\s*$'
        img_only_pattern = r'^(!\[[^\]]*\]\([^)]+\))\{[^}]*\}\s*$'

        m = re.match(img_caption_pattern, line)
        if m:
            img_part = m.group(1)
            caption_text = m.group(2)
            output.append('')
            output.append(img_part)
            output.append('')
            output.append(f'*{caption_text}*')
            output.append('')
            i += 1
            continue

        m2 = re.match(img_only_pattern, line)
        if m2:
            output.append('')
            output.append(m2.group(1))
            output.append('')
            i += 1
            continue

        m3 = re.match(r'^(!\[[^\]]*\]\([^)]+\))\*(.+?)\*\s*$', line)
        if m3:
            output.append('')
            output.append(m3.group(1))
            output.append('')
            output.append(f'*{m3.group(2)}*')
            output.append('')
            i += 1
            continue

        # === DETECT CHAPTER HEADINGS ===
        # Fresh DOCX export gives: ### **Kapitel N: ...** or ## **Vorwort** or ### **Epilog: ...**
        # Also handle: ## Kapitel N: ... (from cached markdown)
        heading_clean = re.sub(r'\*\*', '', line.lstrip('#').strip())
        is_chapter_heading = (
            re.match(r'^#{2,3}\s+\*?\*?(Kapitel \d+|Vorwort|Epilog)', line) or
            re.match(r'^#{2,3}\s+\*\*(Kapitel \d+|Vorwort|Epilog)', line)
        )

        if is_chapter_heading:
            # Before emitting the new chapter, add key takeaways + checklist for PREVIOUS chapter
            if current_chapter_key:
                takeaways = make_key_takeaways_md(current_chapter_key)
                if takeaways:
                    output.append(takeaways)
                checklist = make_checklist_md(current_chapter_key)
                if checklist:
                    output.append(checklist)

            # Determine new chapter key
            current_chapter_key = get_chapter_key(heading_clean)

            # Build clean heading at H1 level
            line = f'# {heading_clean}'

            output.append(line)

            # Add epigraph after chapter heading (Element 6 + 9)
            epigraph = make_epigraph_md(current_chapter_key)
            if epigraph:
                output.append(epigraph)

            chapter_start_pending = True  # Next paragraph gets drop cap
            i += 1
            continue

        # === DETECT TEIL HEADINGS (## **TEIL I: ...**) ===
        is_teil_heading = re.match(r'^##\s+\*\*TEIL\s+', line)
        if is_teil_heading:
            teil_text = re.sub(r'\*\*', '', line.lstrip('#').strip())
            output.append(f'# {teil_text}')
            i += 1
            continue

        # === DETECT BACKMATTER (Danksagung, Endnotes, etc.) ===
        if re.match(r'^##\s+\*\*Danksagung\*\*', line) or re.match(r'^##\s+\*\*Endnotes\*\*', line) or re.match(r'^#\s+Danksagung', line) or re.match(r'^#\s+Endnotes', line):
            in_backmatter = True

        # === H3/H4 SUBHEADINGS → ORNAMENTAL BREAK (Element 5) ===
        if line.startswith('####'):
            # H4 subheadings: shift to ### and add ornamental break in main content
            if not in_backmatter:
                output.append('')
                output.append('<p class="ornamental-break">✦</p>')
                output.append('')
            clean = re.sub(r'\*\*(.+?)\*\*', r'\1', line.lstrip('#').strip())
            output.append(f'### {clean}')
            i += 1
            continue

        if line.startswith('### '):
            # H3 subheadings that are NOT chapter headings (already caught above)
            if not in_backmatter:
                output.append('')
                output.append('<p class="ornamental-break">✦</p>')
                output.append('')
            clean = re.sub(r'\*\*(.+?)\*\*', r'\1', line.lstrip('#').strip())
            output.append(f'## {clean}')
            i += 1
            continue

        # === SHIFT OTHER HEADINGS ===
        if line.startswith('##'):
            clean = re.sub(r'\*\*(.+?)\*\*', r'\1', line.lstrip('#').strip())
            line = f'# {clean}'

        # Clean up any remaining bold in headings
        if line.startswith('#'):
            line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)

        # Clean up escaped brackets and dashes
        line = line.replace('\\[', '[').replace('\\]', ']')
        line = line.replace(' --- ', ' — ')
        line = line.replace('---', '—')
        line = re.sub(r'(\d)--(\d)', r'\1–\2', line)

        # === INSERT PULL QUOTE (Element 1) ===
        if current_chapter_key and current_chapter_key not in pull_quote_inserted:
            trigger = PULL_QUOTE_TRIGGERS.get(current_chapter_key, '')
            if trigger and trigger in line:
                output.append(line)
                output.append(make_pull_quote_md(current_chapter_key))
                pull_quote_inserted[current_chapter_key] = True
                i += 1
                continue

        # === DROP CAP for first paragraph (Element 4 + 9) ===
        if chapter_start_pending and line.strip() and not line.startswith('#') and not line.startswith('<') and not line.startswith('!') and not line.startswith('*Abbildung'):
            # Add drop cap class to first paragraph
            output.append(f'<p class="chapter-start">{line.strip()}</p>')
            chapter_start_pending = False
            i += 1
            continue

        output.append(line)
        i += 1

    # Add takeaways for the last chapter (Epilog)
    if current_chapter_key:
        takeaways = make_key_takeaways_md(current_chapter_key)
        if takeaways:
            output.append(takeaways)
        checklist = make_checklist_md(current_chapter_key)
        if checklist:
            output.append(checklist)

    return '\n'.join(output)


def build_epub(md_path):
    css_path = '/tmp/epub-kindle-styled.css'
    with open(css_path, 'w') as f:
        f.write(EPUB_CSS)

    cmd = [
        'pandoc', md_path,
        '-o', OUTPUT,
        '--epub-cover-image', COVER,
        '--css', css_path,
        '--toc',
        '--toc-depth=2',
        '--epub-chapter-level=2',
        '--metadata', 'title=Maschinenwelt',
        '--metadata', 'subtitle=Besitze sie, oder sie besitzen dich',
        '--metadata', 'creator=Thomas Huhn',
        '--metadata', 'language=de-DE',
        '--metadata', 'date=2026',
        '--metadata', 'subject=KI, Kryptowährungen, Robotik, Investment, Blockchain',
        '--metadata', 'description=Das beste und letzte Investment deines Lebens.',
        f'--resource-path=/tmp/epub-media:{BUILD_DIR}',
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  PANDOC ERROR: {result.stderr}")
        return False
    if result.stderr:
        warnings = [w for w in result.stderr.strip().split('\n') if w and 'Could not' not in w]
        if warnings:
            print(f"  Warnings: {len(warnings)}")
            for w in warnings[:5]:
                print(f"    {w[:100]}")

    size = os.path.getsize(OUTPUT)
    print(f"  EPUB: {OUTPUT}")
    print(f"  Size: {size/1024/1024:.1f} MB")
    return True


def verify_epub():
    import zipfile
    z = zipfile.ZipFile(OUTPUT)

    chapters = [f for f in z.namelist() if f.startswith('EPUB/text/ch') and f.endswith('.xhtml')]
    images = [f for f in z.namelist() if f.startswith('EPUB/media/') and 'cover' not in f.lower()]

    # Count style elements in XHTML
    pullquotes = 0
    callouts = 0
    takeaways = 0
    checklists = 0
    ornaments = 0
    epigraphs = 0
    dropcaps = 0

    for ch in chapters:
        content = z.read(ch).decode('utf-8')
        pullquotes += content.count('pull-quote')
        callouts += content.count('callout-box')
        takeaways += content.count('key-takeaways')
        checklists += content.count('checklist-box')
        ornaments += content.count('ornamental-break')
        epigraphs += content.count('epigraph"')
        dropcaps += content.count('chapter-start')

    nav = z.read('EPUB/nav.xhtml').decode('utf-8')
    toc_entries = re.findall(r'<a[^>]*>([^<]+)</a>', nav)

    print(f"\n  📊 Style Elements:")
    print(f"    Pull Quotes:     {pullquotes}")
    print(f"    Callout Boxes:   {callouts}")
    print(f"    Key Takeaways:   {takeaways}")
    print(f"    Checklists:      {checklists}")
    print(f"    Ornamental Breaks: {ornaments}")
    print(f"    Epigraphs:       {epigraphs}")
    print(f"    Drop Caps:       {dropcaps}")

    print(f"\n  📖 Structure:")
    print(f"    Chapters: {len(chapters)}")
    print(f"    Images: {len(images)} (+ cover)")
    print(f"    TOC entries: {len(toc_entries)}")

    z.close()


def main():
    print("=" * 60)
    print("  MASCHINENWELT v5 — STYLED EPUB Build")
    print("  (9 Design Elements)")
    print("=" * 60)

    print("\n1. Export OAuth token...")
    subprocess.run(
        ['bash', '-c', 'export GOG_KEYRING_PASSWORD=jeannie HOME=/root; gog auth tokens export th@consensus.ventures --out /tmp/gog-token.json'],
        capture_output=True
    )

    print("\n2. Download DOCX from Google Docs...")
    token = get_access_token()
    download_docx(token)

    print("\n3. Convert DOCX → Markdown...")
    md = docx_to_markdown()
    if not md:
        return
    print(f"  Raw markdown: {len(md)/1024:.0f} KB")

    print("\n4. Fix markdown + add style elements...")
    fixed_md = fix_markdown(md)
    with open(MD_PATH, 'w') as f:
        f.write(fixed_md)
    print(f"  Styled markdown: {len(fixed_md)/1024:.0f} KB")

    h1 = len(re.findall(r'^# ', fixed_md, re.MULTILINE))
    h2 = len(re.findall(r'^## ', fixed_md, re.MULTILINE))
    print(f"  Headings: H1={h1}, H2={h2}")

    print("\n5. Build EPUB...")
    if build_epub(MD_PATH):
        print("\n6. Verify EPUB...")
        verify_epub()

    print("\n" + "=" * 60)
    print("  ✅ STYLED EPUB BUILD COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
