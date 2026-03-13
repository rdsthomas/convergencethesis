#!/usr/bin/env python3
"""Build Maschinengeld EPUB from chapter text files + images."""

import os
import re
import subprocess

BUILD_DIR = "/root/clawd/projects/convergencethesis/epub-build"
IMG_DIR = os.path.join(BUILD_DIR, "images")
OUTPUT_MD = os.path.join(BUILD_DIR, "maschinengeld-gesamt.md")
OUTPUT_EPUB = os.path.join(BUILD_DIR, "Maschinengeld-Thomas-Huhn.epub")

# Chapter order with Teil-headers
STRUCTURE = [
    # (teil_header, filename)
    (None, "00-vorwort.txt"),
    ("TEIL I: DIE THESE", None),
    (None, "01-transformation.txt"),
    (None, "02-ki-revolution.txt"),
    (None, "03-maschinen-krypto.txt"),
    (None, "03b-tokenisierung.txt"),
    (None, "03c-daos.txt"),
    ("TEIL II: DIE LANDSCHAFT", None),
    (None, "04-geopolitik.txt"),
    (None, "05-energie.txt"),
    (None, "06-menschlicher-preis.txt"),
    (None, "07-regulierung.txt"),
    ("TEIL III: DIE ZUKUNFT", None),
    (None, "08-szenario.txt"),
    (None, "09-interface.txt"),
    (None, "10-ethik.txt"),
    (None, "11-longevity.txt"),
    ("TEIL IV: DAS PLAYBOOK", None),
    (None, "12-barbell.txt"),
    (None, "13-risiken.txt"),
    (None, "14-warum-jetzt.txt"),
    (None, "15-epilog.txt"),
    (None, "16-anhang-a-glossar.txt"),
    (None, "17-anhang-bcd.txt"),
]

# Image placement: (image_filename, after_text_pattern, caption)
# We'll insert images into the markdown based on chapter prefix matching
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


def convert_chapter_to_markdown(text, filename):
    """Convert plain text chapter to markdown with proper heading levels."""
    lines = text.strip().split('\n')
    md_lines = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            md_lines.append('')
            continue
        
        # First non-empty line of a chapter file is typically the chapter title
        # We'll detect section headers by heuristics
        md_lines.append(stripped)
    
    return '\n'.join(md_lines)


def add_images_to_chapter(text, filename):
    """Append images at the end of the chapter section (simple approach)."""
    images = IMAGE_MAP.get(filename, [])
    if not images:
        return text
    
    result = text
    for img_file, caption in images:
        img_path = os.path.join(IMG_DIR, img_file)
        if os.path.exists(img_path):
            # Add image at the end of chapter with caption
            result += f"\n\n![{caption}](images/{img_file})\n\n*{caption}*\n"
    
    return result


def build_markdown():
    """Build the complete markdown document."""
    parts = []
    
    # Title page
    parts.append("---")
    parts.append("title: 'Maschinengeld'")
    parts.append("subtitle: 'Warum KI, Roboter und Krypto eine Ökonomie ohne Menschen erschaffen'")
    parts.append("author: 'Thomas Huhn'")
    parts.append("date: 'März 2026'")
    parts.append("lang: de-DE")
    parts.append("cover-image: images/cover.png")
    parts.append("---")
    parts.append("")
    
    for teil_header, filename in STRUCTURE:
        if teil_header and not filename:
            # Teil header
            parts.append(f"\n\n# {teil_header}\n\n")
            continue
        
        if filename:
            filepath = os.path.join(BUILD_DIR, filename)
            if not os.path.exists(filepath):
                print(f"WARNING: {filename} not found, skipping")
                continue
            
            with open(filepath, 'r') as f:
                text = f.read().strip()
            
            if not text:
                print(f"WARNING: {filename} is empty, skipping")
                continue
            
            # Add images
            text = add_images_to_chapter(text, filename)
            
            # Add separator
            parts.append(f"\n\n{text}\n")
    
    return '\n'.join(parts)


def main():
    print("Building Maschinengeld EPUB...")
    
    # 1. Build markdown
    md_content = build_markdown()
    with open(OUTPUT_MD, 'w') as f:
        f.write(md_content)
    print(f"Markdown written: {len(md_content)} chars")
    
    # 2. Convert to EPUB with pandoc
    cover_path = os.path.join(IMG_DIR, "cover.png")
    cmd = [
        "pandoc",
        OUTPUT_MD,
        "-o", OUTPUT_EPUB,
        "--epub-cover-image", cover_path,
        "--toc",
        "--toc-depth=2",
        f"--resource-path={BUILD_DIR}",
        "--metadata", "title=Maschinengeld",
        "--metadata", "creator=Thomas Huhn",
        "--metadata", "language=de-DE",
        "--metadata", "subject=KI, Kryptowährungen, Robotik, Investment",
        "--metadata", "description=Warum KI, Roboter und Krypto eine Ökonomie ohne Menschen erschaffen",
    ]
    
    print(f"Running pandoc...")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=BUILD_DIR)
    
    if result.returncode != 0:
        print(f"PANDOC ERROR: {result.stderr}")
        return False
    
    if result.stderr:
        print(f"Pandoc warnings: {result.stderr[:500]}")
    
    size = os.path.getsize(OUTPUT_EPUB)
    print(f"EPUB created: {OUTPUT_EPUB} ({size/1024/1024:.1f} MB)")
    return True


if __name__ == "__main__":
    main()
