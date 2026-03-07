#!/usr/bin/env python3
"""
Build Maschinengeld PDF from chapter text files + images.
Uses Typst for professional book-quality typesetting.

Usage:
    python3 build-pdf.py
    python3 build-pdf.py --output /path/to/output.pdf
"""

import os
import re
import sys
import argparse
import typst

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
EPUB_BUILD_DIR = os.path.join(PROJECT_DIR, "epub-build")
IMG_DIR = os.path.join(EPUB_BUILD_DIR, "images")
OUTPUT_DIR = SCRIPT_DIR
TEMPLATE_FILE = os.path.join(SCRIPT_DIR, "template.typ")
CONTENT_FILE = os.path.join(SCRIPT_DIR, "content.typ")

# Chapter order — mirrors EPUB build
STRUCTURE = [
    # (teil_header, filename, chapter_num)
    (None, "00-vorwort.txt", None),
    ("TEIL I: DIE THESE", None, None),
    (None, "01-transformation.txt", "1"),
    (None, "02-ki-revolution.txt", "2"),
    (None, "03-maschinen-krypto.txt", "3"),
    (None, "03b-tokenisierung.txt", "3b"),
    (None, "03c-daos.txt", "3c"),
    ("TEIL II: DIE LANDSCHAFT", None, None),
    (None, "04-geopolitik.txt", "4"),
    (None, "05-energie.txt", "5"),
    (None, "06-menschlicher-preis.txt", "6"),
    (None, "07-regulierung.txt", "7"),
    ("TEIL III: DIE ZUKUNFT", None, None),
    (None, "08-szenario.txt", "8"),
    (None, "09-interface.txt", "9"),
    (None, "10-ethik.txt", "10"),
    (None, "11-longevity.txt", "11"),
    ("TEIL IV: DAS PLAYBOOK", None, None),
    (None, "12-barbell.txt", "12"),
    (None, "13-risiken.txt", "13"),
    (None, "14-warum-jetzt.txt", "14"),
    (None, "15-epilog.txt", None),
    (None, "16-anhang-a-glossar.txt", None),
    (None, "17-anhang-bcd.txt", None),
]

# Image placement (same as EPUB build)
IMAGE_MAP = {
    "00-vorwort.txt": [
        ("00-konvergenz-venn-color.png", "Abbildung 1: Die Konvergenz-These — KI, Robotik und Krypto verschmelzen zur Maschinenökonomie"),
    ],
    "01-transformation.txt": [
        ("01-250-jahre-umbrueche-color.png", "Abbildung 2: 250 Jahre technologische Umbrüche — Gewinner und Verlierer jeder Revolution"),
        ("01b-infrastruktur-vs-anwendung-color.png", "Abbildung 3: Infrastruktur schlägt Anwendung — das gleiche Muster in vier Revolutionen"),
    ],
    "02-ki-revolution.txt": [
        ("02a-vier-phasen-ki-color.png", "Abbildung 4: Die vier Phasen der KI — vom Werkzeug zur autonomen Maschine"),
        ("02b-ki-landscape-color.png", "Abbildung 5: Das KI-Ökosystem — Labore, Hyperscaler und ihre Verflechtungen"),
        ("02c-deepseek-kosten-color.png", "Abbildung 6: DeepSeek — Der Sputnik-Moment der KI (Trainingskosten im Vergleich)"),
    ],
    "03-maschinen-krypto.txt": [
        ("03a-maschine-vs-bank-color.png", "Abbildung 7: Maschine vs. Bankensystem — warum Krypto die Antwort ist"),
        ("03b-stablecoin-vs-visa-color.png", "Abbildung 8: Stablecoin-Volumen überholt Visa (2024: $27.6 Billionen)"),
    ],
    "03b-tokenisierung.txt": [
        ("03c-tokenisierung-flow-color.png", "Abbildung 9: Von der physischen zur tokenisierten Welt"),
        ("03d-wer-tokenisiert-was-color.png", "Abbildung 10: Wer tokenisiert was? Die Wall-Street-Giganten steigen ein"),
    ],
    "03c-daos.txt": [
        ("03e-dao-anatomie-color.png", "Abbildung 11: Anatomie einer Maschinen-Firma (DAO) — vom Auto zur autonomen Wirtschaftseinheit"),
    ],
    "04-geopolitik.txt": [
        ("04a-ki-weltkarte-color.png", "Abbildung 12: Die KI-Weltkarte — USA dominiert, China rivalisiert, Europa reguliert"),
        ("04b-chip-krieg-tsmc-color.png", "Abbildung 13: Der Chip-Krieg — TSMCs Nadelöhr in der globalen KI-Lieferkette"),
    ],
    "05-energie.txt": [
        ("05a-kraftwerk-kaeufer-color.png", "Abbildung 14: Tech-Giganten werden Energiekonzerne — die größten Kraftwerk-Deals der KI-Ära"),
        ("05b-energiehunger-ki-color.png", "Abbildung 15: Energiehunger der KI — US-Rechenzentren fressen 12% des Stromnetzes bis 2030"),
    ],
    "06-menschlicher-preis.txt": [
        ("06a-jobs-verschwinden-entstehen-color.png", "Abbildung 16: Welche Jobs verschwinden, welche entstehen (WEF Future of Jobs Report)"),
        ("06b-geschichte-der-arbeit-color.png", "Abbildung 17: Die Geschichte der Arbeit — vier Epochen und der aktuelle Umbruch"),
    ],
    "07-regulierung.txt": [
        ("07-regulierung-ampel-color.png", "Abbildung 18: Regulierungs-Geschwindigkeiten — USA, China und Europa im Vergleich"),
    ],
    "08-szenario.txt": [
        ("08-szenario-2026-2035-color.png", "Abbildung 19: Die Zeitleiste 2026–2035 — vom KI-Agenten zum Roboter-Haushalt"),
    ],
    "09-interface.txt": [
        ("09-bci-interface-evolution-color.png", "Abbildung 20: Die Evolution der Interfaces — von der Lochkarte zum Gedanken"),
    ],
    "11-longevity.txt": [
        ("11-longevity-smart-money-color.png", "Abbildung 21: Das Smart Money wettet auf Unsterblichkeit — die größten Longevity-Investments"),
    ],
    "12-barbell.txt": [
        ("12a-barbell-strategie-color.png", "Abbildung 22: Die Barbell-Strategie — Kern (60–70%) vs. asymmetrische Wetten (30–40%)"),
        ("12b-portfolio-varianten-color.png", "Abbildung 23: Drei Portfolio-Varianten — konservativ, ausgewogen, aggressiv"),
    ],
    "13-risiken.txt": [
        ("13-risiko-matrix-color.png", "Abbildung 24: Risiko-Matrix — Wahrscheinlichkeit vs. Impact der größten Risiken"),
    ],
}

# Known inline figure captions in text files (appear as standalone lines)
FIGURE_CAPTION_PATTERN = re.compile(r'^Abbildung \d+[a-z]?:')


def escape_typst(text):
    """Escape special Typst characters in plain text."""
    replacements = [
        ('\\', '\\\\'),
        ('#', '\\#'),
        ('*', '\\*'),
        ('_', '\\_'),
        ('`', '\\`'),
        ('~', '\\~'),
        ('^', '\\^'),
        ('$', '\\$'),
        ('@', '\\@'),
        ('<', '\\<'),
        ('>', '\\>'),
        ('[', '\\['),
        (']', '\\]'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def is_chapter_title(line):
    """Check if a line is a chapter/section title."""
    patterns = [
        r'^Kapitel \d+[a-z]?:',
        r'^Vorwort$',
        r'^Epilog:',
        r'^Anhang [A-Z]\s*[—–-]',
    ]
    for p in patterns:
        if re.match(p, line.strip()):
            return True
    return False


def parse_chapter(text, filename):
    """
    Parse a chapter text file into structured blocks.
    Returns list of (type, content) tuples:
      - ('section', title)
      - ('paragraph', text)
      - ('figure_ref', caption)  -- inline caption reference
      - ('blank', '')
    """
    lines = text.strip().split('\n')
    blocks = []
    
    if not lines:
        return blocks
    
    # Skip first line (chapter title — handled by STRUCTURE)
    i = 0
    first_line = lines[0].strip()
    if is_chapter_title(first_line) or filename == "00-vorwort.txt":
        i = 1
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Empty line
        if not line:
            blocks.append(('blank', ''))
            i += 1
            continue
        
        # Inline figure caption reference
        if FIGURE_CAPTION_PATTERN.match(line):
            blocks.append(('figure_ref', line))
            i += 1
            continue
        
        # Check if this is a section heading:
        # A section heading is a line that:
        # 1. Is preceded by a blank line (or is right after chapter title)
        # 2. Is followed by a line of body text (not empty)
        # 3. Is reasonably short
        # 4. Doesn't end with sentence-ending punctuation
        # 5. Starts with uppercase
        prev_is_boundary = (
            i == 0 or i == 1 or 
            (i > 0 and not lines[i-1].strip())
        )
        
        next_is_text = (
            i + 1 < len(lines) and 
            lines[i + 1].strip() and 
            not FIGURE_CAPTION_PATTERN.match(lines[i + 1].strip())
        )
        
        is_short = len(line) < 100
        no_terminal_punct = not line.endswith(('.', ',', ';', '!', '?', '…', '»', '"'))
        starts_upper = line[0].isupper()
        not_quote_start = not line.startswith(('„', '"', '«', '—', '–', '-', '•'))
        
        if (prev_is_boundary and next_is_text and is_short and 
            no_terminal_punct and starts_upper and not_quote_start):
            blocks.append(('section', line))
            i += 1
            continue
        
        # Regular paragraph text
        blocks.append(('paragraph', line))
        i += 1
    
    return blocks


def blocks_to_typst(blocks, filename):
    """Convert parsed blocks to Typst markup."""
    output = []
    
    for block_type, content in blocks:
        if block_type == 'blank':
            output.append('')
            continue
        
        if block_type == 'section':
            escaped = escape_typst(content)
            output.append(f'=== {escaped}')
            output.append('')
            continue
        
        if block_type == 'figure_ref':
            # Inline figure reference in text — render as centered italic note
            escaped = escape_typst(content)
            output.append(f'#align(center)[#text(size: 9pt, style: "italic", fill: rgb("666666"))[{escaped}]]')
            output.append('')
            continue
        
        if block_type == 'paragraph':
            escaped = escape_typst(content)
            output.append(escaped)
            continue
    
    return '\n'.join(output)


def build_content():
    """Build the complete Typst content file."""
    parts = []
    
    parts.append('// Auto-generated content — do not edit manually')
    parts.append(f'// Generated by build-pdf.py')
    parts.append('')
    
    for teil_header, filename, chapter_num in STRUCTURE:
        if teil_header and not filename:
            # Teil divider page
            teil_escaped = escape_typst(teil_header)
            parts.append(f'''
// --- {teil_header} ---
#pagebreak(to: "odd")
#v(35%)
#align(center)[
  #text(font: "Source Sans 3", size: 24pt, weight: "bold", fill: rgb("1a1a2e"))[
    {teil_escaped}
  ]
]
#pagebreak()
''')
            continue
        
        if not filename:
            continue
        
        filepath = os.path.join(EPUB_BUILD_DIR, filename)
        if not os.path.exists(filepath):
            print(f"WARNING: {filename} not found, skipping")
            continue
        
        with open(filepath, 'r') as f:
            text = f.read().strip()
        
        if not text:
            print(f"WARNING: {filename} is empty, skipping")
            continue
        
        # Extract chapter title from first line
        first_line = text.split('\n')[0].strip()
        title_escaped = escape_typst(first_line)
        
        # Start chapter on odd page (recto)
        parts.append(f'// --- {first_line} ---')
        parts.append('#pagebreak(to: "odd")')
        
        # Chapter heading (== = level 2)
        parts.append(f'== {title_escaped}')
        parts.append('')
        
        # Parse and convert chapter content
        blocks = parse_chapter(text, filename)
        content = blocks_to_typst(blocks, filename)
        parts.append(content)
        
        # Images for this chapter — placed at end of chapter
        images = IMAGE_MAP.get(filename, [])
        for img_file, caption in images:
            img_path = os.path.join(IMG_DIR, img_file)
            if os.path.exists(img_path):
                caption_escaped = escape_typst(caption)
                rel_img_path = os.path.relpath(img_path, SCRIPT_DIR)
                parts.append(f'''
#figure(
  image("{rel_img_path}", width: 85%),
  caption: [{caption_escaped}],
) <fig-{img_file.replace('.png', '').replace('-', '_')}>
''')
        
        parts.append('')
    
    return '\n'.join(parts)


def main():
    parser = argparse.ArgumentParser(description='Build Maschinengeld PDF')
    parser.add_argument('--output', '-o', default=None,
                        help='Output PDF path (default: pdf-build/Maschinengeld-Thomas-Huhn.pdf)')
    args = parser.parse_args()
    
    output_pdf = args.output or os.path.join(OUTPUT_DIR, 'Maschinengeld-Thomas-Huhn.pdf')
    
    print("🔨 Building Maschinengeld PDF...")
    
    # 1. Generate content.typ
    print("  📝 Generating Typst content from chapter files...")
    content = build_content()
    with open(CONTENT_FILE, 'w') as f:
        f.write(content)
    print(f"     → {len(content)} chars written to content.typ")
    
    # 2. Compile with Typst
    print("  📐 Compiling PDF with Typst...")
    try:
        typst.compile(
            TEMPLATE_FILE,
            output=output_pdf,
            root=PROJECT_DIR,
            font_paths=[
                '/usr/share/fonts/truetype/ebgaramond',
                '/usr/share/fonts/truetype/sourcesans',
                '/usr/share/fonts/truetype/',
            ],
        )
    except Exception as e:
        print(f"  ❌ Typst compilation failed: {e}")
        sys.exit(1)
    
    size = os.path.getsize(output_pdf)
    print(f"  ✅ PDF created: {output_pdf} ({size/1024/1024:.1f} MB)")
    return output_pdf


if __name__ == "__main__":
    main()
