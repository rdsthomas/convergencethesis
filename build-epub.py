#!/usr/bin/env python3
"""Build Maschinengeld EPUB with all 24 illustrations from plain text export."""

import re
import html
import os
from ebooklib import epub

INPUT = "/tmp/maschinengeld-full.txt"
OUTPUT_DIR = "/root/clawd/projects/convergencethesis"
COVER_IMG = f"{OUTPUT_DIR}/cover.png"
IMAGES_DIR = "/tmp/maschinengeld-images"

with open(INPUT, "r") as f:
    lines = f.readlines()

# Map: "Abbildung N:" caption text → image filename
# Based on the 24 images in the Grafiken/Farbe folder
FIGURE_MAP = {
    "Abbildung 1": "00-konvergenz-venn-color.png",
    "Abbildung 2": "01-250-jahre-umbrueche-color.png",
    "Abbildung 3": "01b-infrastruktur-vs-anwendung-color.png",
    "Abbildung 4": "02a-vier-phasen-ki-color.png",
    "Abbildung 5": "02b-ki-landscape-color.png",
    "Abbildung 6": "02c-deepseek-kosten-color.png",
    "Abbildung 7": "03a-maschine-vs-bank-color.png",
    "Abbildung 8": "03b-stablecoin-vs-visa-color.png",
    "Abbildung 9": "03c-tokenisierung-flow-color.png",
    "Abbildung 10": "03d-wer-tokenisiert-was-color.png",
    "Abbildung 11": "03e-dao-anatomie-color.png",
    "Abbildung 12": "04a-ki-weltkarte-color.png",
    "Abbildung 13": "04b-chip-krieg-tsmc-color.png",
    "Abbildung 14": "05a-kraftwerk-kaeufer-color.png",
    "Abbildung 15": "05b-energiehunger-ki-color.png",
    "Abbildung 16": "06a-jobs-verschwinden-entstehen-color.png",
    "Abbildung 17": "06b-geschichte-der-arbeit-color.png",
    "Abbildung 18": "07-regulierung-ampel-color.png",
    "Abbildung 19": "08-szenario-2026-2035-color.png",
    "Abbildung 20": "09-bci-interface-evolution-color.png",
    "Abbildung 21": "11-longevity-smart-money-color.png",
    "Abbildung 22": "12a-barbell-strategie-color.png",
    "Abbildung 23": "12b-portfolio-varianten-color.png",
    "Abbildung 24": "13-risiko-matrix-color.png",
}

BOOK_CSS = """
body {
    font-family: Georgia, "Times New Roman", serif;
    line-height: 1.6;
    color: #1a1a1a;
    margin: 1em;
}
h1 {
    font-size: 2em;
    text-align: center;
    margin: 1.5em 0 0.5em;
    color: #0a1628;
    page-break-before: always;
}
h2 {
    font-size: 1.5em;
    text-align: center;
    margin: 2em 0 0.8em;
    color: #0a1628;
    letter-spacing: 3px;
    text-transform: uppercase;
    page-break-before: always;
}
h3 {
    font-size: 1.2em;
    margin: 1.5em 0 0.5em;
    color: #1a1a1a;
    page-break-before: always;
}
h4 {
    font-size: 1em;
    margin: 1.2em 0 0.4em;
    color: #333;
    font-style: italic;
}
p {
    margin: 0.6em 0;
    text-align: justify;
    text-indent: 0;
}
p.beat-line {
    font-style: italic;
    margin: 1em 0;
    text-align: left;
}
.figure-container {
    text-align: center;
    margin: 1.5em 0;
    page-break-inside: avoid;
}
.figure-container img {
    max-width: 100%;
    height: auto;
}
.figure-caption {
    text-align: center;
    font-style: italic;
    font-size: 0.85em;
    color: #666;
    margin: 0.5em 0 1em;
}
.subtitle {
    text-align: center;
    font-style: italic;
    font-size: 0.9em;
    margin: 0.3em 0 1.5em;
    color: #555;
}
.author {
    text-align: center;
    font-size: 1em;
    margin: 0.5em 0 2em;
    letter-spacing: 2px;
}
"""

def parse_chapters(lines):
    chapters = []
    current = None
    teil_re = re.compile(r'^(TEIL [IVX]+:.+)$')
    kapitel_re = re.compile(r'^(Kapitel \d+\w*:.+)$')
    vorwort_re = re.compile(r'^Vorwort$')
    epilog_re = re.compile(r'^Epilog:.+$')
    
    for i, raw_line in enumerate(lines):
        line = raw_line.rstrip('\n')
        if i < 3:
            continue
        if teil_re.match(line):
            if current: chapters.append(current)
            teil_num = len([c for c in chapters if c["level"] == "h2"]) + 1
            current = {'title': line, 'level': 'h2', 'content': [], 'filename': f'teil_{teil_num}.xhtml'}
            continue
        if vorwort_re.match(line):
            if current: chapters.append(current)
            current = {'title': 'Vorwort', 'level': 'h3', 'content': [], 'filename': 'vorwort.xhtml'}
            continue
        if kapitel_re.match(line):
            if current: chapters.append(current)
            kap_num = re.search(r'Kapitel (\d+\w*)', line).group(1)
            current = {'title': line, 'level': 'h3', 'content': [], 'filename': f'kapitel_{kap_num}.xhtml'}
            continue
        if epilog_re.match(line):
            if current: chapters.append(current)
            current = {'title': line, 'level': 'h3', 'content': [], 'filename': 'epilog.xhtml'}
            continue
        if current:
            current['content'].append(line)
    if current:
        chapters.append(current)
    return chapters

def lines_to_html(content_lines):
    html_parts = []
    figure_re = re.compile(r'^(Abbildung \d+):\s*(.+)$')
    
    for i, line in enumerate(content_lines):
        line = line.strip()
        if not line:
            continue
        
        escaped = html.escape(line)
        
        # Check for figure references
        fig_match = figure_re.match(line)
        if fig_match:
            fig_key = fig_match.group(1)
            caption = fig_match.group(2)
            
            if fig_key in FIGURE_MAP:
                img_file = FIGURE_MAP[fig_key]
                html_parts.append(f'''<div class="figure-container">
<img src="images/{img_file}" alt="{html.escape(caption)}"/>
<p class="figure-caption">{html.escape(fig_key)}: {html.escape(caption)}</p>
</div>''')
            else:
                html_parts.append(f'<p class="figure-caption">{escaped}</p>')
            continue
        
        # Beat lines - short standalone paragraphs
        prev_empty = (i == 0 or not content_lines[i-1].strip())
        next_empty = (i + 1 >= len(content_lines) or not content_lines[i + 1].strip())
        is_beat = (
            len(line) < 100 and len(line) > 10 and
            prev_empty and next_empty and
            (line.endswith('.') or line.endswith('?') or line.endswith('!'))
        )
        
        if is_beat:
            html_parts.append(f'<p class="beat-line">{escaped}</p>')
            continue
        
        html_parts.append(f'<p>{escaped}</p>')
    
    return '\n'.join(html_parts)


def build_epub():
    book = epub.EpubBook()
    book.set_identifier('maschinengeld-thomas-huhn-2026')
    book.set_title('Maschinengeld')
    book.set_language('de')
    book.add_author('Thomas Huhn')
    book.add_metadata('DC', 'description', 'Warum KI, Roboter und Krypto eine Ökonomie ohne Menschen erschaffen')
    book.add_metadata('DC', 'date', '2026')
    
    # Cover
    try:
        with open(COVER_IMG, 'rb') as f:
            book.set_cover('cover.png', f.read())
    except FileNotFoundError:
        print("Warning: Cover not found")
    
    # CSS
    style = epub.EpubItem(uid='style', file_name='style/default.css',
                          media_type='text/css', content=BOOK_CSS.encode('utf-8'))
    book.add_item(style)
    
    # Add all figure images to the book
    image_items = {}
    for fig_key, img_file in FIGURE_MAP.items():
        img_path = os.path.join(IMAGES_DIR, img_file)
        if os.path.exists(img_path):
            with open(img_path, 'rb') as f:
                img_data = f.read()
            img_item = epub.EpubItem(
                uid=img_file.replace('.', '_').replace('-', '_'),
                file_name=f'images/{img_file}',
                media_type='image/png',
                content=img_data
            )
            book.add_item(img_item)
            image_items[img_file] = img_item
            print(f"  Added image: {img_file} ({len(img_data)//1024}KB)")
        else:
            print(f"  WARNING: Image not found: {img_path}")
    
    # Title page
    title_html = """<html><head><link rel="stylesheet" href="style/default.css"/></head><body>
    <div style="text-align:center; margin-top: 30%;">
        <h1 style="page-break-before:avoid; font-size:2.5em; letter-spacing:5px;">MASCHINENGELD</h1>
        <p class="subtitle" style="font-size:1.1em;">Warum KI, Roboter und Krypto eine Ökonomie<br>ohne Menschen erschaffen</p>
        <p style="margin-top:1em; font-size:0.9em; color:#666;">◆</p>
        <p class="author" style="font-size:1.1em; margin-top:1em;">THOMAS HUHN</p>
    </div></body></html>"""
    title_page = epub.EpubHtml(title='Titelseite', file_name='title.xhtml', lang='de')
    title_page.content = title_html.encode('utf-8')
    title_page.add_item(style)
    book.add_item(title_page)
    
    # Parse and build chapters
    chapters = parse_chapters(lines)
    toc = []
    spine = ['nav', title_page]
    
    for ch in chapters:
        heading_tag = 'h2' if ch['level'] == 'h2' else 'h3'
        heading = f'<{heading_tag}>{html.escape(ch["title"])}</{heading_tag}>'
        body_html = lines_to_html(ch['content'])
        
        full_html = f"""<html><head>
        <link rel="stylesheet" href="style/default.css"/>
        </head><body>
        {heading}
        {body_html}
        </body></html>"""
        
        epub_ch = epub.EpubHtml(title=ch['title'], file_name=ch['filename'], lang='de')
        epub_ch.content = full_html.encode('utf-8')
        epub_ch.add_item(style)
        book.add_item(epub_ch)
        spine.append(epub_ch)
        toc.append(epub.Link(ch['filename'], ch['title'], ch['filename'].replace('.xhtml', '')))
    
    book.toc = toc
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = spine
    
    epub_path = f"{OUTPUT_DIR}/Maschinengeld-Thomas-Huhn.epub"
    epub.write_epub(epub_path, book, {})
    print(f"\nEPUB created: {epub_path}")
    print(f"Size: {os.path.getsize(epub_path) // 1024}KB")
    print(f"Images embedded: {len(image_items)}")
    return epub_path

if __name__ == '__main__':
    build_epub()
