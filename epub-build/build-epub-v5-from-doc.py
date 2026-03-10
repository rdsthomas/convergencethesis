#!/usr/bin/env python3
"""
Build EPUB from Maschinenwelt v5 Google Doc — from pre-styled document.

The Google Doc already contains all style elements as text:
- Epigraphs (italic quotes after chapter headings)
- Pull Quotes (bold+italic centered text)  
- Key Takeaways (📌 Auf einen Blick + ◆ items)
- Checklists (✅ Was Sie jetzt tun können + ☐ items)
- Szenische Trenner (✦)

This script:
1. Exports Google Doc → DOCX → Pandoc Markdown
2. Fixes heading hierarchy
3. Wraps existing style elements in proper HTML divs for CSS
4. Adds CSS-only features (Drop Caps)
5. Builds EPUB with Pandoc

Pipeline: Google Doc v5 → DOCX → Markdown → fix/wrap → EPUB
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

# Known epigraph sources for detection
EPIGRAPH_SOURCES = [
    'William Gibson', 'Bill Gates', 'Ayn Rand', 'In God We Trust',
    'Kevin Kelly', 'Jensen Huang', 'Frederick Soddy', 'Viktor Frankl',
    'Lord Kelvin', 'Arthur C. Clarke', 'Descartes', 'Aubrey de Grey',
    'Warren Buffett', 'Niels Bohr', 'Chinesisches Sprichwort',
]

# Full CSS for all style elements
EPUB_CSS = """
/* Base typography */
body {
    font-family: Georgia, 'Times New Roman', serif;
    line-height: 1.6;
    text-align: justify;
    margin: 1em;
}
h1 { text-align: center; margin-top: 2em; margin-bottom: 1em; page-break-before: always; }
h2 { margin-top: 1.5em; margin-bottom: 0.5em; }
h3 { margin-top: 1.2em; margin-bottom: 0.4em; }
p { text-indent: 1.5em; margin: 0.3em 0; }
p + p { text-indent: 1.5em; }
h1 + p, h2 + p, h3 + p { text-indent: 0; }

/* Images */
img { max-width: 100%; height: auto; display: block; margin: 1em auto; }
p img { text-indent: 0; }

/* Drop Caps */
.drop-cap::first-letter {
    float: left;
    font-size: 3.2em;
    line-height: 0.8;
    padding-right: 0.08em;
    padding-top: 0.07em;
    font-weight: bold;
    color: #1a3a5c;
}

/* Epigraphs */
.epigraph {
    text-align: right;
    font-style: italic;
    color: #666;
    font-size: 0.9em;
    margin: 0.5em 1em 0.2em 2em;
    text-indent: 0;
}
.epigraph-source {
    text-align: right;
    color: #888;
    font-size: 0.85em;
    margin: 0 1em 1.5em 2em;
    text-indent: 0;
}

/* Pull Quotes */
.pull-quote {
    text-align: center;
    font-size: 1.2em;
    font-weight: bold;
    font-style: italic;
    margin: 1.5em 2em;
    padding: 1em 0;
    border-top: 2px solid #ccc;
    border-bottom: 2px solid #ccc;
    text-indent: 0;
    color: #333;
}

/* Key Takeaways */
.key-takeaways {
    background-color: #e8f0fe;
    border-left: 4px solid #1a73e8;
    padding: 0.8em 1em;
    margin: 1.5em 0;
    border-radius: 4px;
}
.key-takeaways .takeaway-title {
    font-weight: bold;
    font-size: 1.05em;
    margin-bottom: 0.5em;
    text-indent: 0;
}
.key-takeaways .takeaway-item {
    font-size: 0.95em;
    margin: 0.3em 0;
    text-indent: 0;
}

/* Checklists */
.checklist-box {
    background-color: #e6f4ea;
    border-left: 4px solid #34a853;
    padding: 0.8em 1em;
    margin: 1.5em 0;
    border-radius: 4px;
}
.checklist-box .checklist-title {
    font-weight: bold;
    font-size: 1.05em;
    margin-bottom: 0.5em;
    text-indent: 0;
}
.checklist-box .checklist-item {
    font-size: 0.95em;
    margin: 0.3em 0;
    text-indent: 0;
}

/* Ornamental Breaks */
.ornamental-break {
    text-align: center;
    font-size: 1.2em;
    color: #999;
    margin: 1.5em 0;
    text-indent: 0;
    letter-spacing: 0.3em;
}

/* Callout boxes */
.callout-box {
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    border-left: 4px solid #666;
    padding: 0.8em 1em;
    margin: 1.5em 0;
    border-radius: 4px;
    font-size: 0.95em;
}

/* Warning callout box (Wichtiger Hinweis) */
.callout-warning {
    background-color: #fff8e1;
    border: 1px solid #ffcc02;
    border-left: 4px solid #ff8f00;
    padding: 1em 1.2em;
    margin: 1.5em 0;
    border-radius: 4px;
    font-size: 0.95em;
    text-indent: 0;
}
.callout-warning .callout-warning-title {
    font-weight: bold;
    font-size: 1.05em;
    margin-bottom: 0.5em;
    text-indent: 0;
    color: #e65100;
}
.callout-warning p {
    text-indent: 0;
    margin: 0.3em 0;
}

/* Glossary entries */
.glossary-entry {
    text-indent: 0 !important;
    margin: 0.6em 0;
    line-height: 1.5;
}
.glossary-entry strong {
    color: #1a3a5c;
}

/* Bibliography / Literaturverzeichnis */
.bib-section p, .bib-entry {
    text-indent: 0 !important;
    margin: 0.4em 0;
    line-height: 1.5;
}
.bib-section h3, .bib-section h4 {
    margin-top: 1.2em;
    margin-bottom: 0.3em;
}

/* Portfolio tables */
.portfolio-table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0 1.5em 0;
    font-size: 0.88em;
    line-height: 1.4;
}
.portfolio-table caption {
    font-weight: bold;
    font-size: 1em;
    margin-bottom: 0.5em;
    text-align: left;
    color: #1a3a5c;
}
.portfolio-table th {
    background-color: #1a3a5c;
    color: #fff;
    padding: 0.5em 0.6em;
    text-align: left;
    font-weight: bold;
    border: 1px solid #13304d;
}
.portfolio-table td {
    padding: 0.4em 0.6em;
    border: 1px solid #ccc;
    vertical-align: top;
}
.portfolio-table tr:nth-child(even) td {
    background-color: #f5f8fc;
}
.portfolio-table .section-header td {
    background-color: #e8f0fe;
    font-weight: bold;
    color: #1a3a5c;
    border-top: 2px solid #1a3a5c;
}
.portfolio-table .total-row td {
    font-weight: bold;
    border-top: 2px solid #1a3a5c;
    background-color: #f0f4f8;
}

/* Endnotes: hanging indent — number flush left, text indented */
.endnote-entry {
    text-indent: 0 !important;
    padding-left: 2.5em;
    text-indent: -2.5em !important;
    margin: 0.4em 0;
    line-height: 1.5;
    font-size: 0.9em;
}
"""


# Portfolio tables for Kapitel 14 — Paperback-optimized
PORTFOLIO_TABLE_A = """
<table class="portfolio-table">
<caption>Variante A — Der Konservative (100K–500K €)</caption>
<tr><th>Seite</th><th>Allokation</th><th>Anteil</th></tr>
<tr class="section-header"><td colspan="3">Sichere Seite (70 %)</td></tr>
<tr><td>Aktien</td><td>Globaler ETF (MSCI World), Tech-Übergewichtung</td><td>30 %</td></tr>
<tr><td>Big Tech</td><td>NVIDIA, Microsoft, Apple, Alphabet</td><td>15 %</td></tr>
<tr><td>Energie</td><td>Cameco, Constellation Energy, NextEra</td><td>10 %</td></tr>
<tr><td>Robotik</td><td>Intuitive Surgical, ABB, Fanuc</td><td>10 %</td></tr>
<tr><td>Cash</td><td>Tagesgeld / Geldmarkt</td><td>5 %</td></tr>
<tr class="section-header"><td colspan="3">Asymmetrische Seite (30 %)</td></tr>
<tr><td>Bitcoin</td><td>DCA über 6–12 Monate</td><td>15 %</td></tr>
<tr><td>Ethereum</td><td>Layer-2-Ökosystem, Agent-TAM</td><td>5 %</td></tr>
<tr><td>RWA</td><td>BUIDL, Ondo Finance (Tokenisierte Treasuries)</td><td>5 %</td></tr>
<tr><td>Infrastruktur</td><td>Coinbase, OLAS, PEAQ, Agent-Payment-Rails</td><td>5 %</td></tr>
<tr class="total-row"><td colspan="2">Gesamt</td><td>100 %</td></tr>
</table>
"""

PORTFOLIO_TABLE_B = """
<table class="portfolio-table">
<caption>Variante B — Der Ausgewogene (500K–2M €)</caption>
<tr><th>Seite</th><th>Allokation</th><th>Anteil</th></tr>
<tr class="section-header"><td colspan="3">Sichere Seite (60 %)</td></tr>
<tr><td>Aktien</td><td>Globaler ETF mit KI-Tilt</td><td>20 %</td></tr>
<tr><td>Big Tech</td><td>NVIDIA, Microsoft, Apple, Alphabet, Amazon, Meta</td><td>15 %</td></tr>
<tr><td>Robotik</td><td>Tesla, Intuitive Surgical, ABB, Figure AI</td><td>10 %</td></tr>
<tr><td>Energie</td><td>Cameco, Constellation, NuScale, Oklo, Uran-ETF</td><td>10 %</td></tr>
<tr><td>Cash</td><td>Cash-Reserve</td><td>5 %</td></tr>
<tr class="section-header"><td colspan="3">Asymmetrische Seite (40 %)</td></tr>
<tr><td>Bitcoin</td><td>DCA über 12 Monate</td><td>15 %</td></tr>
<tr><td>Ethereum</td><td>Staking, Layer-2-Exposure</td><td>8 %</td></tr>
<tr><td>DeFi</td><td>Circle (IPO), Aave, Uniswap</td><td>7 %</td></tr>
<tr><td>RWA</td><td>Maple, Centrifuge, Hamilton Lane tokenisiert</td><td>5 %</td></tr>
<tr><td>Machine Economy</td><td>Olas, peaq, Fetch.ai/ASI, Render Network</td><td>5 %</td></tr>
<tr class="total-row"><td colspan="2">Gesamt</td><td>100 %</td></tr>
</table>
"""

PORTFOLIO_TABLE_C = """
<table class="portfolio-table">
<caption>Variante C — Der Aggressive (2M €+, hohe Risikotoleranz)</caption>
<tr><th>Seite</th><th>Allokation</th><th>Anteil</th></tr>
<tr class="section-header"><td colspan="3">Sichere Seite (50 %)</td></tr>
<tr><td>Big Tech</td><td>NVIDIA, Microsoft, Apple</td><td>15 %</td></tr>
<tr><td>Energie</td><td>Nuklear &amp; Energie breit diversifiziert</td><td>15 %</td></tr>
<tr><td>Robotik</td><td>Tesla, Intuitive Surgical + Venture-Positionen</td><td>10 %</td></tr>
<tr><td>Cash / Treasuries</td><td>Tokenisierte Treasuries, yield-generierend</td><td>10 %</td></tr>
<tr class="section-header"><td colspan="3">Asymmetrische Seite (50 %)</td></tr>
<tr><td>Bitcoin</td><td>Kernposition</td><td>20 %</td></tr>
<tr><td>Ethereum</td><td>Smart-Contract-Plattform</td><td>10 %</td></tr>
<tr><td>KI-Token / DeFi</td><td>Render, Filecoin, Olas, ASI Alliance, Aave</td><td>8 %</td></tr>
<tr><td>RWA</td><td>Private Equity, Immobilien, Private Credit</td><td>7 %</td></tr>
<tr><td>Venture / Angel</td><td>peaq-Ökosystem, Robotik-DAOs, BCI-nahe Firmen</td><td>5 %</td></tr>
<tr class="total-row"><td colspan="2">Gesamt</td><td>100 %</td></tr>
</table>
"""


# Kinderportfolio tables for Anhang E
KINDER_TABLE_A = """
<table class="portfolio-table">
<caption>Variante A — Der einfache Weg (200 €/Monat, 1 ETF)</caption>
<tr><th>Asset</th><th>Produkt / ISIN</th><th>Anteil</th><th>Betrag</th></tr>
<tr><td>MSCI World ETF</td><td>IE00B4L5Y983 (TER 0,20 %)</td><td>100 %</td><td>200 €</td></tr>
<tr><td colspan="4" style="text-align:right; font-style:italic; border-top: 2px solid #1a3a5c;">Erwartung bei 8 % p.a., 18 Jahre: ca. 96.000 € (eingezahlt: 43.200 €)</td></tr>
</table>
"""

KINDER_TABLE_B = """
<table class="portfolio-table">
<caption>Variante B — Mit KI-Tilt (200 €/Monat, 3 ETFs)</caption>
<tr><th>Asset</th><th>Produkt / ISIN</th><th>Anteil</th><th>Betrag</th></tr>
<tr><td>MSCI World ETF</td><td>IE00B4L5Y983</td><td>60 %</td><td>120 €</td></tr>
<tr><td>Nasdaq-100 ETF</td><td>IE00BFZXGZ54</td><td>25 %</td><td>50 €</td></tr>
<tr><td>Robotik-ETF</td><td>IE00BYZK4552</td><td>15 %</td><td>30 €</td></tr>
<tr class="total-row"><td colspan="2">Gesamt</td><td>100 %</td><td>200 €</td></tr>
<tr><td colspan="4" style="text-align:right; font-style:italic; border-top: 2px solid #1a3a5c;">Erwartung bei 10 % p.a., 18 Jahre: ca. 120.000 €</td></tr>
</table>
"""

KINDER_TABLE_C = """
<table class="portfolio-table">
<caption>Variante C — Die aggressive Kinderbarbell (200 €/Monat)</caption>
<tr><th>Asset</th><th>Produkt / ISIN</th><th>Anteil</th><th>Betrag</th></tr>
<tr><td>MSCI World ETF</td><td>IE00B4L5Y983</td><td>50 %</td><td>100 €</td></tr>
<tr><td>Nasdaq-100 ETF</td><td>IE00BFZXGZ54</td><td>20 %</td><td>40 €</td></tr>
<tr><td>Robotik-ETF</td><td>IE00BYZK4552</td><td>10 %</td><td>20 €</td></tr>
<tr><td>Bitcoin*</td><td>Im eigenen Depot</td><td>15 %</td><td>30 €</td></tr>
<tr><td>Ethereum*</td><td>Im eigenen Depot</td><td>5 %</td><td>10 €</td></tr>
<tr class="total-row"><td colspan="2">Gesamt</td><td>100 %</td><td>200 €</td></tr>
<tr><td colspan="4" style="text-align:right; font-style:italic; font-size:0.85em; border-top: 2px solid #1a3a5c;">* Krypto nicht im Junior-Depot möglich — Kauf im eigenen Namen, Übertrag zum 18. Geburtstag<br/>Konservativ: ca. 141.000 € · Optimistisch: bis zu 195.000 €</td></tr>
</table>
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
    """Always download fresh DOCX."""
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


def is_epigraph_quote(text):
    """Check if a line looks like an epigraph quote (starts with „ and is italic)."""
    clean = text.strip().lstrip('*').rstrip('*').strip()
    return clean.startswith('„') and clean.endswith('"')


def is_epigraph_source(text):
    """Check if a line is an epigraph source attribution."""
    clean = text.strip().lstrip('*').rstrip('*').strip()
    if not clean.startswith('—'):
        return False
    return any(src in clean for src in EPIGRAPH_SOURCES)


def fix_markdown(md):
    """
    Fix markdown structure and wrap existing style elements in HTML divs.
    """
    lines = md.split('\n')
    output = []
    
    # YAML front matter
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
    in_backmatter = False
    just_saw_chapter_heading = False
    in_epigraph = False
    in_takeaway = False
    in_checklist = False
    chapter_start_pending = False  # Next content paragraph gets drop-cap
    in_glossar = False
    in_literatur = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip raw title lines at the very beginning
        if skip_title:
            if line.startswith('#'):
                skip_title = False
            else:
                i += 1
                continue
        
        # Skip Google Docs TOC
        if re.match(r'^#{2,3}\s+\*?\*?Inhaltsverzeichnis', line):
            skip_toc = True
            i += 1
            continue
        if skip_toc:
            if re.match(r'^#{2,3}\s+\*?\*?(?!Inhaltsverzeichnis)', line):
                skip_toc = False
            else:
                i += 1
                continue
        # Skip TOC-like lines
        if re.match(r'^>\s*\[?\[', line) or re.match(r'^\[?\[\[', line):
            i += 1
            continue
        
        # === IMAGE + CAPTION FIX ===
        img_caption = re.match(r'^(!\[[^\]]*\]\([^)]+\))\{[^}]*\}\*(.+?)\*\s*$', line)
        if img_caption:
            output.append('')
            output.append(img_caption.group(1))
            output.append('')
            output.append(f'*{img_caption.group(2)}*')
            output.append('')
            i += 1
            continue
        
        img_only = re.match(r'^(!\[[^\]]*\]\([^)]+\))\{[^}]*\}\s*$', line)
        if img_only:
            output.append('')
            output.append(img_only.group(1))
            output.append('')
            i += 1
            continue
        
        img_cap_no_attr = re.match(r'^(!\[[^\]]*\]\([^)]+\))\*(.+?)\*\s*$', line)
        if img_cap_no_attr:
            output.append('')
            output.append(img_cap_no_attr.group(1))
            output.append('')
            output.append(f'*{img_cap_no_attr.group(2)}*')
            output.append('')
            i += 1
            continue
        
        # === DETECT CHAPTER HEADINGS ===
        heading_clean = re.sub(r'\*\*', '', line.lstrip('#').strip())
        is_chapter = re.match(r'^#{2,3}\s+\*?\*?(Kapitel \d+|Vorwort|Epilog)', line)
        
        if is_chapter and not in_backmatter:
            output.append(f'# {heading_clean}')
            just_saw_chapter_heading = True
            chapter_start_pending = True
            i += 1
            continue
        elif is_chapter and in_backmatter:
            # Endnotes chapter headings — keep as H2, no drop cap
            output.append(f'## {heading_clean}')
            i += 1
            continue
        
        # === DETECT TEIL HEADINGS ===
        if re.match(r'^##\s+\*?\*?TEIL\s+', line):
            teil_text = re.sub(r'\*\*', '', line.lstrip('#').strip())
            output.append(f'# {teil_text}')
            i += 1
            continue
        
        # === DETECT BACKMATTER ===
        if re.match(r'^#{1,3}\s+\*?\*?Danksagung', line) or re.match(r'^#{1,3}\s+\*?\*?Endnotes', line):
            in_backmatter = True
            chapter_start_pending = False
        
        # === DETECT AND WRAP EPIGRAPHS ===
        # Epigraphs appear right after chapter headings as italic text starting with „
        if just_saw_chapter_heading:
            stripped = line.strip()
            # Check for empty lines after heading
            if stripped == '':
                output.append(line)
                i += 1
                continue
            
            # Check if this is an epigraph quote
            clean_text = stripped.lstrip('*').rstrip('*').strip()
            if clean_text.startswith('„') and (clean_text.endswith('"') or clean_text.endswith('"')):
                # This is an epigraph quote
                quote_text = clean_text
                output.append(f'<div class="epigraph">{quote_text}</div>')
                
                # Check if next non-empty line is attribution
                j = i + 1
                while j < len(lines) and lines[j].strip() == '':
                    j += 1
                if j < len(lines):
                    attr_clean = lines[j].strip().lstrip('*').rstrip('*').strip()
                    # DOCX export uses --- (em-dash via pandoc), also handle — and – 
                    if attr_clean.startswith('—') or attr_clean.startswith('– ') or attr_clean.startswith('--- ') or attr_clean.startswith('-- '):
                        # Convert --- to — for clean display
                        attr_display = attr_clean.replace('--- ', '— ').replace('-- ', '— ')
                        output.append(f'<div class="epigraph-source">{attr_display}</div>')
                        output.append('')
                        i = j + 1
                        # Don't set chapter_start_pending false yet — drop cap comes after epigraph
                        continue
                
                output.append('')
                i += 1
                continue
            
            # Check if this is an epigraph source line without a preceding quote
            # (some DOCX exports put --- Author on its own)
            if clean_text.startswith('--- ') or clean_text.startswith('-- '):
                if any(src in clean_text for src in EPIGRAPH_SOURCES):
                    attr_display = clean_text.replace('--- ', '— ').replace('-- ', '— ')
                    output.append(f'<div class="epigraph-source">{attr_display}</div>')
                    output.append('')
                    i += 1
                    continue
            
            # Not an epigraph — this is the first content paragraph
            just_saw_chapter_heading = False
        
        # === DETECT AND WRAP ✦ TRENNER ===
        if line.strip() == '✦' or line.strip() == '**✦**':
            output.append('')
            output.append('<p class="ornamental-break">✦</p>')
            output.append('')
            i += 1
            continue
        
        # === DETECT AND WRAP KEY TAKEAWAYS ===
        stripped = line.strip()
        stripped_clean = re.sub(r'\*\*', '', stripped).strip()
        # Detect "📌 Auf einen Blick" or bold version (DOCX export breaks bold mid-word: "**📌 Auf einen Blic**k")
        takeaway_match = ('📌' in stripped and ('Auf einen Blick' in stripped_clean or 'Auf einen Blic' in stripped))
        if takeaway_match:
            # Start collecting takeaway items
            output.append('')
            output.append('<div class="key-takeaways">')
            output.append('<p class="takeaway-title">📌 Auf einen Blick</p>')
            i += 1
            # Collect ◆ items
            while i < len(lines):
                item_line = lines[i].strip()
                item_clean = re.sub(r'\*\*', '', item_line).strip()
                if item_clean.startswith('◆'):
                    output.append(f'<p class="takeaway-item">{item_clean}</p>')
                    i += 1
                elif item_clean == '':
                    # Could be spacing between items — check if next line has ◆
                    if i + 1 < len(lines) and lines[i+1].strip().startswith('◆'):
                        i += 1
                        continue
                    else:
                        break
                else:
                    break
            output.append('</div>')
            output.append('')
            continue
        
        # === DETECT AND WRAP CHECKLISTS ===
        if '✅' in stripped and 'Was Sie jetzt tun können' in stripped:
            output.append('')
            output.append('<div class="checklist-box">')
            output.append('<p class="checklist-title">✅ Was Sie jetzt tun können</p>')
            i += 1
            while i < len(lines):
                item_line = lines[i].strip()
                item_clean = re.sub(r'\*\*', '', item_line).strip()
                if item_clean.startswith('☐'):
                    output.append(f'<p class="checklist-item">{item_clean}</p>')
                    i += 1
                elif item_clean == '':
                    if i + 1 < len(lines) and lines[i+1].strip().startswith('☐'):
                        i += 1
                        continue
                    else:
                        break
                else:
                    break
            output.append('</div>')
            output.append('')
            continue
        
        # === H4 SUBHEADINGS ===
        if line.startswith('####'):
            clean = re.sub(r'\*+', '', line.lstrip('#').strip()).strip()
            
            # Check if this H4 is actually an epigraph quote (starts with „)
            if clean.startswith('„') and (clean.endswith('"') or clean.endswith('\\"')):
                clean = clean.rstrip('\\').rstrip('"').rstrip('\\') + '"'
                output.append(f'<div class="epigraph">{clean}</div>')
                i += 1
                continue
            
            # Check if this H4 is an epigraph source (--- Author)
            if clean.startswith('---') or clean.startswith('—'):
                if any(src in clean for src in EPIGRAPH_SOURCES) or clean.startswith('--- Frei nach'):
                    attr_display = clean.replace('--- ', '— ').replace('--', '—').strip()
                    output.append(f'<div class="epigraph-source">{attr_display}</div>')
                    output.append('')
                    i += 1
                    continue
            
            # Skip empty H4s (like #### with no text)
            if not clean:
                i += 1
                continue
            
            # Regular H4 subheading — add ornamental break before if not in backmatter
            if not in_backmatter:
                last_non_empty = ''
                for prev in reversed(output):
                    if prev.strip():
                        last_non_empty = prev.strip()
                        break
                if '✦' not in last_non_empty and 'epigraph' not in last_non_empty:
                    output.append('')
                    output.append('<p class="ornamental-break">✦</p>')
                    output.append('')
            output.append(f'### {clean}')
            i += 1
            continue
        
        # === H3 → H2 ===
        if line.startswith('### ') and not line.startswith('#### '):
            clean = re.sub(r'\*\*(.+?)\*\*', r'\1', line[4:].strip())
            # Don't add ornamental break for H3s that are chapter headings
            if not re.match(r'(Kapitel \d+|Vorwort|Epilog)', clean):
                if not in_backmatter:
                    last_non_empty = ''
                    for prev in reversed(output):
                        if prev.strip():
                            last_non_empty = prev.strip()
                            break
                    if '✦' not in last_non_empty:
                        output.append('')
                        output.append('<p class="ornamental-break">✦</p>')
                        output.append('')
                output.append(f'## {clean}')
            else:
                output.append(f'## {clean}')
            i += 1
            continue
        
        # === H2 → H1 (for non-TEIL, non-chapter H2s like Impressum, Danksagung) ===
        if line.startswith('## ') and not line.startswith('### '):
            clean = re.sub(r'\*\*(.+?)\*\*', r'\1', line[3:].strip())
            if not re.match(r'(TEIL\s+|Kapitel \d+|Vorwort|Epilog)', clean):
                output.append(f'# {clean}')
            else:
                output.append(f'# {clean}')
            i += 1
            continue
        
        # === DROP CAP for first paragraph after chapter heading ===
        if chapter_start_pending and line.strip() and not line.startswith('#') and not line.startswith('<') and not line.startswith('!'):
            # This is the first content paragraph — add drop-cap class
            # But skip if it's an epigraph or empty
            clean = line.strip()
            if clean and not clean.startswith('✦') and not clean.startswith('📌') and not clean.startswith('✅'):
                # Check it's not an epigraph (already handled above) 
                if not (clean.lstrip('*').startswith('„') or clean.startswith('—')):
                    output.append(f'<p class="drop-cap">{clean}</p>')
                    output.append('')
                    chapter_start_pending = False
                    i += 1
                    continue
        
        # === DETECT ANHANG HEADINGS (plain text "Anhang X --- ...") ===
        anhang_match = re.match(r'^Anhang\s+([A-E])\s+---\s+(.+)$', line.strip())
        if anhang_match:
            anhang_letter = anhang_match.group(1)
            anhang_title = anhang_match.group(2)
            # Close any open bib-section div BEFORE the new heading
            if in_literatur:
                output.append('</div>')
                output.append('')
                in_literatur = False
            in_glossar = False
            output.append(f'# Anhang {anhang_letter} — {anhang_title}')
            just_saw_chapter_heading = True
            chapter_start_pending = True
            # Track which anhang we're in for special formatting
            if anhang_letter == 'A':
                in_glossar = True
            elif anhang_letter == 'D':
                in_literatur = True
                output.append('')
                output.append('<div class="bib-section">')
            i += 1
            continue

        # === DETECT "Wichtiger Hinweis" CALLOUT BOX ===
        if line.strip() == 'Wichtiger Hinweis':
            # Collect the hint text (next non-empty lines)
            hint_lines = []
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            while j < len(lines) and lines[j].strip() != '' and not lines[j].strip().startswith('Anhang'):
                hint_lines.append(lines[j].strip())
                j += 1
            hint_text = ' '.join(hint_lines)
            output.append('')
            output.append('<div class="callout-warning">')
            output.append('<p class="callout-warning-title">⚠️ Wichtiger Hinweis</p>')
            output.append(f'<p>{hint_text}</p>')
            output.append('</div>')
            output.append('')
            i = j
            continue

        # === GLOSSAR ENTRIES: "Begriff (optional): Erklärung" → bold term ===
        if in_glossar and line.strip() and not line.startswith('#') and not line.startswith('<'):
            glossar_match = re.match(r'^([A-ZÄÖÜ][^:]+?):\s+(.+)$', line.strip())
            if glossar_match:
                term = glossar_match.group(1)
                explanation = glossar_match.group(2)
                output.append(f'<p class="glossary-entry"><strong>{term}:</strong> {explanation}</p>')
                i += 1
                continue

        # === PORTFOLIO TABLES for Kapitel 14 ===
        stripped_for_table = re.sub(r'\*+', '', line.strip())
        if stripped_for_table.startswith('Variante A: Der Konservative'):
            # Insert table after the heading
            output.append(f'### {stripped_for_table}')
            output.append('')
            output.append(PORTFOLIO_TABLE_A)
            output.append('')
            i += 1
            continue
        if stripped_for_table.startswith('Variante B: Der Ausgewogene'):
            output.append(f'### {stripped_for_table}')
            output.append('')
            output.append(PORTFOLIO_TABLE_B)
            output.append('')
            i += 1
            continue
        if stripped_for_table.startswith('Variante C: Der Aggressive') and 'Kinderbarbell' not in stripped_for_table and 'Kinder' not in line:
            output.append(f'### {stripped_for_table}')
            output.append('')
            output.append(PORTFOLIO_TABLE_C)
            output.append('')
            i += 1
            continue

        # === KINDERPORTFOLIO TABLES (Anhang E) ===
        if 'Variante A' in line and 'einfache Weg' in line and '1 ETF' in line:
            output.append(KINDER_TABLE_A)
            output.append('')
            output.append(line)
            i += 1
            continue
        if 'Variante B' in line and 'KI-Tilt' in line and '3 ETF' in line:
            output.append(KINDER_TABLE_B)
            output.append('')
            output.append(line)
            i += 1
            continue
        if 'Variante C' in line and 'aggressive Kinderbarbell' in line:
            output.append(KINDER_TABLE_C)
            output.append('')
            output.append(line)
            i += 1
            continue

        # === ENDNOTES: Hanging indent for numbered entries ===
        endnote_match = re.match(r'^(\d+)\\\.\s+(.+)', line.strip())
        if in_backmatter and endnote_match:
            num = endnote_match.group(1)
            text = endnote_match.group(2)
            output.append(f'<p class="endnote-entry">{num}. {text}</p>')
            i += 1
            continue

        # Default: pass through
        output.append(line)
        i += 1
    
    # Close any open bib-section div
    if in_literatur:
        output.append('</div>')
    
    return '\n'.join(output)


def build_epub(md_path):
    css_path = os.path.join(BUILD_DIR, 'epub-style.css')
    with open(css_path, 'w') as f:
        f.write(EPUB_CSS)
    
    cmd = [
        'pandoc', md_path,
        '-o', OUTPUT,
        '--epub-cover-image', COVER,
        '--css', css_path,
        '--toc', '--toc-depth=2',
        '--epub-chapter-level=2',
        '-f', 'markdown+raw_html',
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr}")
        return False
    
    size = os.path.getsize(OUTPUT)
    print(f"  EPUB built: {size/1024/1024:.1f} MB")
    return True


def upload_to_drive(token, file_path):
    """Upload EPUB to Google Drive and return file ID."""
    folder_id = '1NCcMZTw2tpKh--Up-moGPjoZCZrNnDwm'
    file_name = 'Maschinenwelt-v5-styled.epub'
    
    # Check if file already exists in folder and update it
    search_url = f"https://www.googleapis.com/drive/v3/files?q=name='{file_name}'+and+'{folder_id}'+in+parents+and+trashed=false&fields=files(id)"
    req = urllib.request.Request(search_url, headers={'Authorization': f'Bearer {token}'})
    resp = urllib.request.urlopen(req)
    results = json.loads(resp.read())
    
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    if results.get('files'):
        # Update existing file
        file_id = results['files'][0]['id']
        upload_url = f'https://www.googleapis.com/upload/drive/v3/files/{file_id}?uploadType=media'
        req = urllib.request.Request(upload_url, data=file_data, method='PATCH', headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/epub+zip',
        })
    else:
        # Create new file
        metadata = json.dumps({'name': file_name, 'parents': [folder_id]}).encode()
        boundary = '----MultipartBoundary'
        body = (
            f'--{boundary}\r\n'
            f'Content-Type: application/json; charset=UTF-8\r\n\r\n'
        ).encode() + metadata + (
            f'\r\n--{boundary}\r\n'
            f'Content-Type: application/epub+zip\r\n\r\n'
        ).encode() + file_data + f'\r\n--{boundary}--'.encode()
        
        upload_url = 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart'
        req = urllib.request.Request(upload_url, data=body, headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': f'multipart/related; boundary={boundary}',
        })
    
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    file_id = result.get('id', file_id if results.get('files') else 'unknown')
    return file_id


def count_elements(md_text):
    """Count style elements in the output markdown."""
    counts = {
        'Epigraphs': md_text.count('class="epigraph"'),
        'Pull Quotes': md_text.count('class="pull-quote"'),
        'Key Takeaways': md_text.count('class="key-takeaways"'),
        'Checklists': md_text.count('class="checklist-box"'),
        'Ornamental Breaks': md_text.count('class="ornamental-break"'),
        'Drop Caps': md_text.count('class="drop-cap"'),
    }
    return counts


def main():
    print("=" * 60)
    print("  MASCHINENWELT v5 — EPUB Build (from pre-styled Doc)")
    print("=" * 60)
    
    print("\n📥 Step 1: Download fresh DOCX from Google Doc v5...")
    token = get_access_token()
    download_docx(token)
    
    print("\n📝 Step 2: Convert DOCX to Markdown...")
    md = docx_to_markdown()
    if not md:
        print("FAILED")
        return
    print(f"  {len(md.split(chr(10)))} lines, {len(md.split())} words")
    
    print("\n🔧 Step 3: Fix markdown and wrap style elements...")
    fixed_md = fix_markdown(md)
    with open(MD_PATH, 'w') as f:
        f.write(fixed_md)
    
    counts = count_elements(fixed_md)
    for name, count in counts.items():
        print(f"  {name}: {count}")
    
    print("\n📖 Step 4: Build EPUB...")
    success = build_epub(MD_PATH)
    if not success:
        print("FAILED")
        return
    
    # Quick EPUB analysis
    import zipfile
    with zipfile.ZipFile(OUTPUT) as z:
        xhtml_count = sum(1 for f in z.namelist() if f.endswith('.xhtml'))
        image_count = sum(1 for f in z.namelist() if f.endswith('.png') or f.endswith('.jpg'))
    print(f"  Chapters: {xhtml_count}")
    print(f"  Images: {image_count}")
    
    print("\n☁️ Step 5: Upload to Google Drive...")
    token = get_access_token()  # refresh
    file_id = upload_to_drive(token, OUTPUT)
    print(f"  File ID: {file_id}")
    print(f"  URL: https://drive.google.com/file/d/{file_id}/view?usp=drivesdk")
    
    print("\n" + "=" * 60)
    print("  ✅ DONE")
    print("=" * 60)


if __name__ == '__main__':
    main()
