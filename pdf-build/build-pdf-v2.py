#!/usr/bin/env python3
"""
Build The AI Species PDF from the Google Docs "Gesamtentwurf v5".
Uses Typst for professional book-quality typesetting.

Usage:
    python3 build-pdf-v2.py
    python3 build-pdf-v2.py --output /path/to/output.pdf
    python3 build-pdf-v2.py --input /path/to/exported.txt  (skip Google Docs fetch)
"""

import os
import re
import sys
import argparse
import subprocess
import typst

# === Paths ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
IMG_DIR = os.path.join(PROJECT_DIR, "epub-build", "images")
OUTPUT_DIR = SCRIPT_DIR
TEMPLATE_FILE = os.path.join(SCRIPT_DIR, "template-v2.typ")
CONTENT_FILE = os.path.join(SCRIPT_DIR, "content-v2.typ")
COVER_IMG = os.path.join(IMG_DIR, "cover.png")

# Google Doc V5
DOC_ID = "1JF7Kei019q0iunIISa-fCq7Y4aLcHWHmkjBOb7MBlms"
GOG_ACCOUNT = "th@consensus.ventures"

# Book metadata
BOOK_TITLE = "The AI Species"
BOOK_SUBTITLE = "Besitze sie. Sonst besitzt sie dich."
BOOK_SHORT_TITLE = "THE AI SPECIES"
AUTHOR = "Thomas Huhn"
PUBLISHER = "Consensus Ventures GmbH"
OUTPUT_BASENAME = "The-AI-Species-Thomas-Huhn.pdf"

# Image mapping: Abbildung number -> file + preferred width
IMAGE_SPECS = {
    1: {"file": "00-konvergenz-venn-color.png", "width": "92%"},
    2: {"file": "01-250-jahre-umbrueche-color.png", "width": "92%"},
    3: {"file": "01b-infrastruktur-vs-anwendung-color.png", "width": "90%"},
    4: {"file": "02a-vier-phasen-ki-color.png", "width": "90%"},
    5: {"file": "02b-ki-landscape-color.png", "width": "94%"},
    6: {"file": "02c-deepseek-kosten-color.png", "width": "90%"},
    7: {"file": "03a-maschine-vs-bank-color.png", "width": "94%"},
    8: {"file": "03b-stablecoin-vs-visa-color.png", "width": "92%"},
    9: {"file": "03c-tokenisierung-flow-color.png", "width": "90%"},
    10: {"file": "03d-wer-tokenisiert-was-color.png", "width": "92%"},
    11: {"file": "03e-dao-anatomie-color.png", "width": "88%"},
    12: {"file": "04a-ki-weltkarte-color.png", "width": "94%"},
    13: {"file": "04b-chip-krieg-tsmc-color.png", "width": "92%"},
    14: {"file": "05a-kraftwerk-kaeufer-color.png", "width": "92%"},
    15: {"file": "05b-energiehunger-ki-color.png", "width": "92%"},
    16: {"file": "06a-jobs-verschwinden-entstehen-color.png", "width": "92%"},
    17: {"file": "06b-geschichte-der-arbeit-color.png", "width": "92%"},
    18: {"file": "07-regulierung-ampel-color.png", "width": "88%"},
    19: {"file": "08-szenario-2026-2035-color.png", "width": "92%"},
    20: {"file": "09-bci-interface-evolution-color.png", "width": "90%"},
    21: {"file": "11-longevity-smart-money-color.png", "width": "90%"},
    22: {"file": "12a-barbell-strategie-color.png", "width": "94%"},
    23: {"file": "12b-portfolio-varianten-color.png", "width": "94%"},
    24: {"file": "13-risiko-matrix-color.png", "width": "90%"},
}

# Literaturverzeichnis subsection headings
LIT_SUBSECTIONS = {
    "Bücher",
    "Wissenschaftliche Arbeiten und Fachaufsätze",
    "Institutionelle Reports und Studien",
    "Datenquellen und On-Chain-Analyse",
    "Nachrichtenquellen und Medienberichte",
    "Weiterbildung und Kurse",
}

# Endnotes chapter headings (these should be sub-headings, NOT new chapters)
ENDNOTE_CHAPTER_RE = re.compile(
    r'^(Vorwort|Kapitel \d+(?:\s*\(Fortsetzung\))?(?::.*)?|Abbildungsverzeichnis)$'
)


def fetch_doc():
    """Fetch the Google Doc text via gog CLI."""
    print("Fetching Google Doc...")
    env = os.environ.copy()
    env["GOG_KEYRING_PASSWORD"] = "jeannie"
    env["HOME"] = "/root"
    result = subprocess.run(
        ["gog", "docs", "read", DOC_ID, "--account", GOG_ACCOUNT],
        capture_output=True, text=True, env=env
    )
    if result.returncode != 0:
        print(f"Error fetching doc: {result.stderr}")
        sys.exit(1)
    text = result.stdout
    if not text.strip():
        print("Error: Empty document received")
        sys.exit(1)
    print(f"  Fetched {len(text)} chars, {text.count(chr(10))} lines")
    return text


def escape_typst(text):
    """Escape special Typst characters in text."""
    text = text.replace("\\", "\\\\")
    text = text.replace("#", "\\#")
    text = text.replace("$", "\\$")
    text = text.replace("@", "\\@")
    text = text.replace("*", "\\*")
    text = text.replace("_", "\\_")
    text = text.replace("<", "\\<")
    text = text.replace(">", "\\>")
    text = text.replace("~", "\\~")
    text = text.replace("^", "\\^")
    return text


def find_content_start(lines):
    """Find where actual content starts (3rd occurrence of 'Vorwort', confirmed by 'Es ist zwei Uhr nachts')."""
    vorwort_count = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "Vorwort":
            vorwort_count += 1
            if vorwort_count == 3:
                return i

    # Fallback
    for i, line in enumerate(lines):
        if "Es ist zwei Uhr nachts" in line:
            return i - 1

    print("ERROR: Could not find content start")
    sys.exit(1)


def extract_impressum(lines, content_start):
    """Extract impressum text between 'Impressum' and 'Inhaltsverzeichnis'."""
    imp_start = None
    imp_end = None
    for i, line in enumerate(lines[:content_start]):
        stripped = line.strip()
        if stripped == "Impressum" and imp_start is None:
            imp_start = i + 1
        elif stripped == "Inhaltsverzeichnis" and imp_start is not None:
            imp_end = i
            break

    if imp_start and imp_end:
        return "\n".join(lines[imp_start:imp_end]).strip()
    return ""


def parse_document(raw_text):
    """Parse the Google Docs text into structured sections."""
    lines = raw_text.split("\n")
    content_start = find_content_start(lines)
    print(f"  Content starts at line {content_start}")

    impressum_text = extract_impressum(lines, content_start)

    sections = []
    current_section = None
    in_endnotes = False
    skip_klappentext = False

    i = content_start
    while i < len(lines):
        stripped = lines[i].strip()

        # Skip Klappentext entirely
        if skip_klappentext:
            i += 1
            continue

        # Handle Endnotes mode — chapter headings here are sub-headings
        if in_endnotes:
            if stripped in ("Abbildungsverzeichnis", "Stichwortverzeichnis",
                           "Über den Autor", "Klappentext"):
                in_endnotes = False
                # Fall through to normal detection
            else:
                if current_section is not None:
                    current_section["lines"].append(lines[i])
                i += 1
                continue

        # Detect section types

        # Strip inline "Abbildung X:" that Google Docs concatenates onto headings
        clean_stripped = re.sub(r'Abbildung \d+:.*$', '', stripped).strip()

        if stripped == "Vorwort" and not any(s["title"] == "Vorwort" for s in sections):
            current_section = {"type": "chapter", "title": "Vorwort", "lines": [], "chapter_num": None}
            sections.append(current_section)

        elif re.match(r'^TEIL [IVX]+:', clean_stripped):
            sections.append({"type": "teil", "title": clean_stripped, "lines": []})
            current_section = None
            # If there's an Abbildung concatenated, save for next section
            abb_match = re.search(r'(Abbildung \d+:.+)$', stripped)
            if abb_match:
                pass

        elif re.match(r'^Kapitel \d+:', clean_stripped):
            m = re.match(r'^Kapitel (\d+):\s*(.*)$', clean_stripped)
            if m:
                ch_num = m.group(1)
                ch_title = m.group(2).strip()
                current_section = {
                    "type": "chapter",
                    "title": f"Kapitel {ch_num}: {ch_title}",
                    "chapter_num": ch_num,
                    "lines": []
                }
                sections.append(current_section)
                # Handle concatenated Abbildung on same line
                abb_match = re.search(r'(Abbildung \d+:.+)$', stripped)
                if abb_match and clean_stripped != stripped:
                    current_section["lines"].append(abb_match.group(1))

        elif re.match(r'^Epilog:', stripped):
            current_section = {"type": "chapter", "title": stripped, "lines": [], "chapter_num": None}
            sections.append(current_section)

        elif stripped == "Danksagung":
            current_section = {"type": "backmatter", "title": "Danksagung", "lines": []}
            sections.append(current_section)

        elif re.match(r'^Anhang [A-E]', stripped):
            current_section = {"type": "appendix", "title": stripped, "lines": []}
            sections.append(current_section)

        elif stripped == "Endnotes":
            current_section = {"type": "endnotes", "title": "Endnotes", "lines": []}
            sections.append(current_section)
            in_endnotes = True

        elif stripped == "Abbildungsverzeichnis" and i > content_start + 100:
            current_section = {"type": "backmatter", "title": "Abbildungsverzeichnis", "lines": []}
            sections.append(current_section)

        elif stripped == "Stichwortverzeichnis" and i > content_start + 100:
            current_section = {"type": "backmatter", "title": "Stichwortverzeichnis", "lines": []}
            sections.append(current_section)

        elif stripped == "Über den Autor" and i > content_start + 100:
            current_section = {"type": "backmatter", "title": "Über den Autor", "lines": []}
            sections.append(current_section)

        elif stripped == "Klappentext":
            skip_klappentext = True

        elif current_section is not None:
            current_section["lines"].append(lines[i])

        i += 1

    return impressum_text, sections


def is_german_quote(line):
    """Check if line is a standalone German-quoted passage suitable for pull-quote."""
    stripped = line.strip()
    open_q = "\u201e"   # „
    close_q = "\u201c"  # "
    close_q2 = "\u201d" # "
    if stripped.startswith(open_q) and (stripped.endswith(close_q) or stripped.endswith(close_q2) or stripped.endswith('"')):
        return True
    if stripped.startswith(open_q) and "\u2014" in stripped:
        return True
    if stripped.startswith('"') and stripped.endswith('"') and len(stripped) > 30:
        return True
    return False


def is_subheading(line, prev_empty, section_type, lines_from_start):
    """Conservative heuristic to detect true sub-headings."""
    stripped = line.strip()
    if not stripped or len(stripped) > 90:
        return False
    if not prev_empty:
        return False
    if lines_from_start < 2:
        return False
    if stripped.endswith(",") or stripped.endswith(";"):
        return False
    if stripped.endswith(".") and len(stripped) > 40:
        return False
    if stripped.startswith("•") or stripped.startswith("- ") or stripped.startswith("["):
        return False
    if re.match(r'^\d+\.\s', stripped):
        return False
    if re.match(r'^Abbildung \d+:', stripped):
        return False
    if stripped.count(":") > 1:
        return False
    # Avoid treating short website/contact lines as headings
    if "." in stripped and " " not in stripped:
        return False
    # Avoid full-sentence lines with common verbs
    if re.search(r'\b(ist|sind|war|wird|hat|haben|kann|können|bleibt|zeigt)\b', stripped, re.IGNORECASE) and len(stripped) > 32:
        return False
    return True


def format_paragraph(text):
    """Format a paragraph for Typst."""
    text = text.strip()
    if not text:
        return ""
    return escape_typst(text)


def format_glossary_section(lines):
    """Format glossary entries into Typst."""
    out = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Glossary entries: "Term: Definition" or "Term (Abbreviation): Definition"
        m = re.match(r'^([^:]+):\s+(.+)$', line)
        if m:
            term = m.group(1).strip()
            definition_parts = [m.group(2).strip()]
            # Collect continuation lines
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r'^[A-Z].*:\s+', lines[i + 1].strip()):
                i += 1
                definition_parts.append(lines[i].strip())
            definition = " ".join(definition_parts)

            term_esc = escape_typst(term)
            def_esc = escape_typst(definition)
            out.append(f'\n#glossary-entry[{term_esc}][{def_esc}]\n')
        else:
            escaped = escape_typst(line)
            out.append(f'\n{escaped}\n')

        i += 1
    return "\n".join(out)


def format_abbildungsverzeichnis(lines):
    """Format the figure index with cleaner hierarchy."""
    out = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("[Die Seitenzahlen"):
            i += 1
            continue
        m = re.match(r'^Abbildung (\d+):\s*(.+)$', line)
        if m:
            fig_num = m.group(1)
            caption = escape_typst(m.group(2))
            out.append(f'''\n#block(below: 5pt)[
  #text(weight: "semibold", font: "Source Sans 3")[Abbildung {fig_num}]
  #h(6pt)
  {caption}
]\n''')
            if i + 1 < len(lines) and lines[i + 1].strip():
                detail = escape_typst(lines[i + 1].strip())
                out.append(f'#text(size: 8.2pt, fill: rgb("#666"))[{detail}]\n#v(4pt)\n')
                i += 1
        else:
            escaped = escape_typst(line)
            if not line.startswith("    "):
                out.append(f'\n{escaped}\n')
        i += 1
    return "\n".join(out)


def format_stichwortverzeichnis(lines):
    """Format the index (Stichwortverzeichnis)."""
    out = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("[Die Seitenzahlen"):
            continue

        # Single letter heading
        if re.match(r'^[A-Z]$', stripped):
            out.append(f'\n#v(8pt)\n#text(weight: "bold", size: 12pt, fill: gold)[{stripped}]\n#v(2pt)\n')
            continue

        # Index entries
        escaped = escape_typst(stripped)
        out.append(f'\n#text(size: 9pt)[{escaped}]\n')

    return "\n".join(out)


def format_literatur(lines):
    """Format Anhang D — Literaturverzeichnis with subsections."""
    out = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        # Subsection headings
        if line in LIT_SUBSECTIONS or line.startswith("Wissenschaftliche Arbeiten") or line.startswith("Institutionelle Reports") or line.startswith("Datenquellen") or line.startswith("Nachrichtenquellen") or line.startswith("Weiterbildung"):
            escaped = escape_typst(line)
            out.append(f'\n#heading(level: 2)[{escaped}]\n')
            i += 1
            continue

        # Introductory paragraph
        if line.startswith("Die folgende Übersicht"):
            escaped = escape_typst(line)
            out.append(f'\n#text(style: "italic", size: 9.5pt)[{escaped}]\n')
            i += 1
            continue

        # Literature entries
        escaped = escape_typst(line)
        out.append(f'\n#text(size: 9pt)[{escaped}]\n')
        i += 1

    return "\n".join(out)


def section_to_typst(section, img_dir):
    """Convert a parsed section to Typst markup."""
    out = []

    if section["type"] == "teil":
        title = escape_typst(section["title"])
        out.append(f'\n#teil-page[{title}]\n')
        return "\n".join(out)

    if section["type"] == "chapter":
        title = section["title"]
        escaped_title = escape_typst(title)
        out.append(f'\n#pagebreak(to: "odd")\n')
        out.append('#state("running-matter", false).update(true)\n')
        out.append(f'#heading(level: 1)[{escaped_title}]\n')

    elif section["type"] == "appendix":
        escaped_title = escape_typst(section["title"])

        # Special formatting for specific appendices
        if "Glossar" in section["title"]:
            out.append(f'\n#pagebreak()\n')
            out.append(f'#heading(level: 1)[{escaped_title}]\n')
            glossary_content = format_glossary_section(section.get("lines", []))
            out.append(glossary_content)
            return "\n".join(out)

        if "Literaturverzeichnis" in section["title"]:
            out.append(f'\n#pagebreak()\n')
            out.append(f'#heading(level: 1)[{escaped_title}]\n')
            lit_content = format_literatur(section.get("lines", []))
            out.append(lit_content)
            return "\n".join(out)

        out.append(f'\n#pagebreak()\n')
        out.append(f'#heading(level: 1)[{escaped_title}]\n')

    elif section["type"] == "endnotes":
        out.append(f'\n#pagebreak()\n')
        out.append(f'#heading(level: 1)[Endnotes]\n')
        out.append(f'#set text(size: 8pt)\n')
        out.append(f'#set par(leading: 0.5em, spacing: 0.6em)\n')

    elif section["type"] == "backmatter":
        escaped_title = escape_typst(section["title"])

        if section["title"] == "Abbildungsverzeichnis":
            out.append(f'\n#pagebreak()\n')
            out.append(f'#heading(level: 1)[{escaped_title}]\n')
            abb_content = format_abbildungsverzeichnis(section.get("lines", []))
            out.append(abb_content)
            return "\n".join(out)

        if section["title"] == "Stichwortverzeichnis":
            out.append(f'\n#pagebreak()\n')
            out.append(f'#heading(level: 1)[{escaped_title}]\n')
            stw_content = format_stichwortverzeichnis(section.get("lines", []))
            out.append(stw_content)
            return "\n".join(out)

        out.append(f'\n#pagebreak()\n')
        out.append(f'#heading(level: 1)[{escaped_title}]\n')

    # Process lines
    lines = section.get("lines", [])
    in_endnotes = section["type"] == "endnotes"

    i = 0
    prev_empty = True
    lines_from_section_start = 0
    first_para = True  # For drop-cap on chapter openers

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            prev_empty = True
            i += 1
            continue

        lines_from_section_start += 1

        # === Image detection ===
        img_match = re.match(r'^Abbildung (\d+):\s*(.+)$', line)
        if img_match:
            fig_num = int(img_match.group(1))
            caption = escape_typst(img_match.group(2))
            if fig_num in IMAGE_SPECS:
                spec = IMAGE_SPECS[fig_num]
                img_path = os.path.join(img_dir, spec["file"])
                rel_path = os.path.relpath(img_path, SCRIPT_DIR)
                width = spec.get("width", "85%")
                out.append(f'''
#figure(
  image("{rel_path}", width: {width}),
  caption: [Abbildung {fig_num}: {caption}],
) <fig{fig_num}>
''')
            else:
                out.append(f'\n#emph[Abbildung {fig_num}: {caption}]\n')
            prev_empty = False
            first_para = False
            i += 1
            continue

        # Also handle "...textAbbildung X:" concatenated within text
        inline_img = re.search(r'Abbildung (\d+):\s*(.+)$', line)
        if inline_img and not line.startswith("Abbildung"):
            text_before = line[:inline_img.start()].strip()
            if text_before:
                escaped = format_paragraph(text_before)
                out.append(f'\n{escaped}\n')
            fig_num = int(inline_img.group(1))
            caption = escape_typst(inline_img.group(2))
            if fig_num in IMAGE_SPECS:
                spec = IMAGE_SPECS[fig_num]
                img_path = os.path.join(img_dir, spec["file"])
                rel_path = os.path.relpath(img_path, SCRIPT_DIR)
                width = spec.get("width", "85%")
                out.append(f'''
#figure(
  image("{rel_path}", width: {width}),
  caption: [Abbildung {fig_num}: {caption}],
) <fig{fig_num}>
''')
            prev_empty = False
            first_para = False
            i += 1
            continue

        # === Endnotes sub-headings and entries ===
        if in_endnotes:
            if ENDNOTE_CHAPTER_RE.match(line):
                escaped = escape_typst(line)
                out.append(f'\n#v(10pt)\n#text(weight: "bold", size: 9pt, font: "Source Sans 3")[{escaped}]\n#v(4pt)\n')
                prev_empty = False
                i += 1
                continue

            # Endnote entries: "N. text..."
            m_note = re.match(r'^(\d+)\.\s+(.+)', line)
            if m_note:
                num = m_note.group(1)
                note_lines = [m_note.group(2)]
                while (i + 1 < len(lines) and lines[i + 1].strip()
                       and not re.match(r'^\d+\.\s', lines[i + 1].strip())
                       and not ENDNOTE_CHAPTER_RE.match(lines[i + 1].strip())):
                    i += 1
                    note_lines.append(lines[i].strip())
                full_note = " ".join(note_lines)
                escaped_note = escape_typst(full_note)
                out.append(f'\n[{num}.] #h(4pt) {escaped_note}\n')
                prev_empty = False
                i += 1
                continue

            # Other endnote text
            escaped = escape_typst(line)
            out.append(f'\n{escaped}\n')
            prev_empty = False
            i += 1
            continue

        # === "📌 Auf einen Blick" callout box ===
        if line.startswith('\U0001f4cc') and 'Auf einen Blick' in line:
            items = []
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith('◆'):
                item_text = lines[j].strip()[1:].strip()
                items.append(escape_typst(item_text))
                j += 1
            box_items = '\n    '.join(f'#text(fill: gold)[◆] #h(4pt) {it} #linebreak()' for it in items)
            out.append(f'''
#callout-box[
  #text(weight: "bold", font: "Source Sans 3", size: 10pt)[📌 Auf einen Blick]
  #v(6pt)
  #set par(first-line-indent: 0pt, leading: 0.85em, spacing: 0.7em)
    {box_items}
]
''')
            i = j
            prev_empty = False
            first_para = False
            continue

        # === "✅ Was Sie jetzt tun können" action box ===
        if line.startswith('✅') and 'Was Sie' in line:
            items = []
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith('☐'):
                item_text = lines[j].strip()[1:].strip()
                items.append(escape_typst(item_text))
                j += 1
            box_items = '\n    '.join(f'☐ #h(4pt) {it} #linebreak()' for it in items)
            out.append(f'''
#info-box[
  #text(weight: "bold", font: "Source Sans 3", size: 10pt)[✅ Was Sie jetzt tun können]
  #v(6pt)
  #set par(first-line-indent: 0pt, leading: 0.85em, spacing: 0.7em)
    {box_items}
]
''')
            i = j
            prev_empty = False
            first_para = False
            continue

        # === Tab-separated table data (portfolio tables etc.) ===
        # Format in raw text: each row spans multiple lines:
        #   Line 1: first cell (no tab)
        #   Line 2+: \tCell2, \tCell3, etc.
        # Detect: current line is a short label and next line starts with tab
        is_table_start = False
        if prev_empty and '\t' not in lines[i] and len(line) < 40 and i + 1 < len(lines) and lines[i + 1].startswith('\t'):
            is_table_start = True
        if is_table_start:
            # Collect multi-line rows: first cell on its own line, subsequent cells tab-prefixed
            table_rows = []
            j = i
            current_row_cells = []
            while j < len(lines):
                raw_line = lines[j]
                stripped_line = raw_line.strip()
                if not stripped_line:
                    # Flush current row if any
                    if current_row_cells:
                        table_rows.append(current_row_cells)
                        current_row_cells = []
                    # Check if table continues after blank
                    peek = j + 1
                    while peek < len(lines) and not lines[peek].strip():
                        peek += 1
                    if peek < len(lines):
                        peek_stripped = lines[peek].strip()
                        # Table continues if next content is tab-prefixed, section header, or short label + tab
                        if (lines[peek].startswith('\t') or
                            peek_stripped.startswith(('SICHERE SEITE', 'ASYMMETRISCHE SEITE')) or
                            ('\t' not in lines[peek] and len(peek_stripped) < 40 and peek + 1 < len(lines) and lines[peek + 1].startswith('\t'))):
                            j += 1
                            continue
                    break
                elif raw_line.startswith('\t'):
                    # Tab-prefixed continuation cells for current row
                    tab_cells = [c.strip() for c in raw_line.split('\t') if c.strip()]
                    current_row_cells.extend(tab_cells)
                    j += 1
                elif stripped_line.startswith(('SICHERE SEITE', 'ASYMMETRISCHE SEITE')):
                    if current_row_cells:
                        table_rows.append(current_row_cells)
                        current_row_cells = []
                    table_rows.append([stripped_line])
                    j += 1
                else:
                    # New first cell of a row
                    if current_row_cells:
                        table_rows.append(current_row_cells)
                    current_row_cells = [stripped_line]
                    j += 1
            if current_row_cells:
                table_rows.append(current_row_cells)
            if len(table_rows) >= 2:
                # Determine number of columns from max cells in any row
                ncols = max(len(r) for r in table_rows)
                if ncols < 2:
                    ncols = 2
                col_spec = ', '.join(['auto'] * ncols)
                out.append(f'\n#v(0.5em)\n#block(width: 100%, breakable: true)[\n#table(\n  columns: ({col_spec}),\n  stroke: 0.4pt + rgb("#CCC"),\n  inset: 6pt,\n  fill: (col, row) => if row == 0 {{ rgb("#F0EDE4") }} else if calc.odd(row) {{ rgb("#FAFAFA") }} else {{ white }},\n')
                for ri, row in enumerate(table_rows):
                    if len(row) == 1:
                        # Spanning header row (e.g. "SICHERE SEITE (70%)")
                        cell_text = escape_typst(row[0])
                        out.append(f'  table.cell(colspan: {ncols})[#text(weight: "bold", size: 8.5pt, font: "Source Sans 3", fill: navy)[{cell_text}]],\n')
                    else:
                        # Pad row to ncols
                        padded = row + [''] * (ncols - len(row))
                        cells_typst = []
                        for ci, cell in enumerate(padded):
                            cell_esc = escape_typst(cell)
                            if ri == 0:
                                cells_typst.append(f'[#text(weight: "bold", size: 8.5pt, font: "Source Sans 3")[{cell_esc}]]')
                            elif cell.lower() == 'gesamt':
                                cells_typst.append(f'[#text(weight: "bold")[{cell_esc}]]')
                            else:
                                cells_typst.append(f'[{cell_esc}]')
                        out.append('  ' + ', '.join(cells_typst) + ',\n')
                out.append(')\n]\n#v(0.5em)\n')
                i = j
                prev_empty = False
                first_para = False
                continue

        # === Pull quotes — standalone German-quoted lines ===
        if prev_empty and is_german_quote(line) and len(line) > 30 and len(line) < 500:
            escaped = escape_typst(line)
            # Check if next non-empty line is an attribution (— Name)
            attrib = None
            peek = i + 1
            while peek < len(lines) and not lines[peek].strip():
                peek += 1
            if peek < len(lines) and lines[peek].strip().startswith('—'):
                attrib = escape_typst(lines[peek].strip())
            out.append(f'\n#pull-quote[{escaped}]\n')
            if attrib:
                out.append(f'#v(-0.6em)\n#align(left, pad(left: 2em)[#text(size: 9pt, style: "italic", fill: rgb("#666"))[{attrib}]])\n#v(0.6em)\n')
                i = peek + 1
            else:
                i += 1
            prev_empty = False
            first_para = False
            continue

        # === Quote attribution line on its own (— Name) — attach to preceding content ===
        if line.startswith('—') and len(line) < 100 and prev_empty:
            escaped = escape_typst(line)
            out.append(f'#v(-0.4em)\n#align(left, pad(left: 2em)[#text(size: 9pt, style: "italic", fill: rgb("#666"))[{escaped}]])\n#v(0.6em)\n')
            prev_empty = False
            first_para = False
            i += 1
            continue

        # === Sub-headings ===
        if section["type"] in ("chapter", "appendix", "backmatter"):
            if is_subheading(line, prev_empty, section["type"], lines_from_section_start):
                escaped = escape_typst(line)
                out.append(f'\n#heading(level: 2)[{escaped}]\n')
                prev_empty = False
                first_para = False
                i += 1
                continue

        # === Literaturverzeichnis subsection headings in Anhang D ===
        if section["type"] == "appendix" and "Literaturverzeichnis" in section.get("title", ""):
            if line in LIT_SUBSECTIONS:
                escaped = escape_typst(line)
                out.append(f'\n#heading(level: 2)[{escaped}]\n')
                prev_empty = False
                i += 1
                continue

        # === Bullet points ===
        if line.startswith("•") or (line.startswith("- ") and len(line) > 3):
            prefix_len = 1 if line.startswith("•") else 2
            bullet_text = escape_typst(line[prefix_len:].strip())
            out.append(f'\n- {bullet_text}')
            prev_empty = False
            first_para = False
            i += 1
            continue

        # === ◆ diamond bullets (outside callout-box context) ===
        if line.startswith('◆'):
            bullet_text = escape_typst(line[1:].strip())
            out.append(f'\n- {bullet_text}')
            prev_empty = False
            first_para = False
            i += 1
            continue

        # === Stichwortverzeichnis entries ===
        if section["type"] == "backmatter" and section["title"] == "Stichwortverzeichnis":
            if re.match(r'^[A-Z]$', line):
                out.append(f'\n#v(8pt)\n#text(weight: "bold", size: 12pt, fill: gold)[{line}]\n#v(2pt)\n')
                prev_empty = False
                i += 1
                continue

        # === Special handling for author page website/contact ===
        if section["type"] == "backmatter" and section.get("title") == "Über den Autor":
            if "." in line and " " not in line:
                out.append(f'\n#v(6pt)\n#text(font: "Source Sans 3", size: 9.8pt, fill: navy)[{escape_typst(line)}]\n')
                prev_empty = False
                first_para = False
                i += 1
                continue

        # === Drop cap for first paragraph of chapters ===
        if first_para and section["type"] == "chapter" and len(line) > 20:
            first_char = line[0]
            rest_text = line[1:]
            first_char_esc = escape_typst(first_char)
            rest_esc = escape_typst(rest_text)
            out.append(f'\n#drop-cap[{first_char_esc}][{rest_esc}]\n')
            first_para = False
            prev_empty = False
            i += 1
            continue

        # === Regular paragraph ===
        escaped = format_paragraph(line)
        if escaped:
            out.append(f'\n{escaped}\n')
        prev_empty = False
        first_para = False
        i += 1

    return "\n".join(out)


def build_typst_document(impressum_text, sections, img_dir):
    """Generate the complete Typst document."""
    parts = []

    # Import template
    parts.append('#import "template-v2.typ": *\n')
    parts.append(f'#show: doc => book(doc, short-title: [{BOOK_SHORT_TITLE}], author: [{AUTHOR}])\n')

    # === FRONT MATTER ===

    # Full title page
    parts.append(f"""
// Volltitel
#pagebreak(to: "odd")
#page(header: none, footer: none)[
  #v(0.9fr)
  #align(center)[
    #text(size: 30pt, weight: "bold", font: "Source Sans 3", fill: navy)[{BOOK_TITLE.upper()}]
    #v(10pt)
    #line(length: 68pt, stroke: 2.6pt + gold)
    #v(16pt)
    #text(size: 12.2pt, style: "italic", fill: rgb("#444"))[{BOOK_SUBTITLE}]
    #v(44pt)
    #text(size: 14pt, font: "Source Sans 3", weight: "medium")[{AUTHOR}]
    #v(1fr)
    #text(size: 9pt, fill: rgb("#888"))[{PUBLISHER}]
  ]
]
""")

    # Impressum
    imp_escaped = escape_typst(impressum_text).replace("[", "(").replace("]", ")")
    imp_lines = [l.strip() for l in imp_escaped.split("\n") if l.strip()]
    meta_rows = []
    legal_rows = []
    for line in imp_lines:
        if re.match(r'^(©|Alle Rechte|1\. Auflage|Verlag:|Autor:|ISBN|Begleitwebsite:|Kontakt:)', line):
            meta_rows.append(line)
        else:
            legal_rows.append(line)
    meta_block = ('\n      #linebreak()\n      ').join(meta_rows)
    legal_block = ('\n\n      ').join(legal_rows)

    parts.append(f"""
// Impressum / Copyright
#page(header: none, footer: none)[
  #v(0.62fr)
  #block(width: 100%)[
    #text(font: "Source Sans 3", size: 9.2pt, weight: "semibold", fill: navy)[{BOOK_TITLE}]
    #v(3pt)
    #text(size: 8.6pt, style: "italic", fill: rgb("#555"))[{BOOK_SUBTITLE}]
    #v(10pt)
    #line(length: 46pt, stroke: 1.5pt + gold)
    #v(14pt)
    #set text(size: 8.3pt)
    #set par(first-line-indent: 0pt, leading: 0.72em, spacing: 0.34em)
    {meta_block}
  ]
  #v(0.9fr)
  #block(width: 100%)[
    #set text(size: 7.95pt, fill: rgb("#444"))
    #set par(first-line-indent: 0pt, leading: 0.77em, spacing: 0.5em)
    {legal_block}
    #v(14pt)
    #set text(size: 8.15pt, font: "Source Sans 3", fill: rgb("#666"))
    theaispecies.world
    #linebreak()
    thomas\@theaispecies.world
  ]
]
""")

    # Inhaltsverzeichnis
    parts.append("""
// Inhaltsverzeichnis
#pagebreak(to: "odd")
#page(header: none, footer: none)[
  #v(1cm)
  #align(center)[
    #text(size: 16pt, weight: "bold", font: "Source Sans 3", fill: navy)[Inhaltsverzeichnis]
    #v(6pt)
    #line(length: 60pt, stroke: 2pt + gold)
  ]
  #v(14pt)
  #set text(size: 8.9pt, hyphenate: false)
  #set par(leading: 0.7em)
  #outline(
    title: none,
    indent: 1.1em,
    depth: 1,
  )
]
""")

    # === MAIN CONTENT ===
    fig1_inserted = False
    for section in sections:
        typst_content = section_to_typst(section, img_dir)
        if typst_content.strip():
            # Insert Abbildung 1 into Kapitel 1 if not referenced in body text
            if not fig1_inserted and section.get("chapter_num") == "1" and 1 in IMAGE_SPECS:
                spec = IMAGE_SPECS[1]
                img_path = os.path.join(img_dir, spec["file"])
                rel_path = os.path.relpath(img_path, SCRIPT_DIR)
                width = spec.get("width", "85%")
                fig1_markup = f'''
#figure(
  image("{rel_path}", width: {width}),
  caption: [Abbildung 1: Die Konvergenz-These — KI, Robotik und Krypto verschmelzen zur Maschinenökonomie],
) <fig1>
'''
                # Insert after the drop-cap (first paragraph)
                lines_tc = typst_content.split("\n")
                insert_idx = None
                for li, tl in enumerate(lines_tc):
                    if "#drop-cap" in tl:
                        insert_idx = li + 1
                        break
                if insert_idx:
                    lines_tc.insert(insert_idx, fig1_markup)
                    typst_content = "\n".join(lines_tc)
                fig1_inserted = True
            parts.append(typst_content)

    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Build The AI Species PDF from Google Doc V5")
    parser.add_argument("--output", "-o", default=os.path.join(OUTPUT_DIR, OUTPUT_BASENAME))
    parser.add_argument("--input", "-i", help="Use local text file instead of fetching from Google Docs")
    parser.add_argument("--keep-typ", action="store_true", help="Keep intermediate .typ files")
    args = parser.parse_args()

    # 1. Get document text
    if args.input:
        print(f"Reading from {args.input}...")
        with open(args.input, "r") as f:
            raw_text = f.read()
    else:
        raw_text = fetch_doc()

    # Save raw text for debugging
    raw_path = os.path.join(SCRIPT_DIR, "raw-v5.txt")
    with open(raw_path, "w") as f:
        f.write(raw_text)
    print(f"  Raw text saved to {raw_path}")

    # 2. Parse document
    print("Parsing document structure...")
    impressum_text, sections = parse_document(raw_text)

    print(f"  Found {len(sections)} sections:")
    for s in sections:
        stype = s["type"]
        title = s.get("title", "?")
        nlines = len(s.get("lines", []))
        print(f"    [{stype}] {title} ({nlines} lines)")

    # 3. Generate Typst content
    print("Generating Typst content...")
    typst_content = build_typst_document(impressum_text, sections, IMG_DIR)

    with open(CONTENT_FILE, "w") as f:
        f.write(typst_content)
    print(f"  Written {len(typst_content)} chars to {CONTENT_FILE}")

    # 4. Compile PDF
    print("Compiling PDF...")
    try:
        pdf_bytes = typst.compile(CONTENT_FILE, root=PROJECT_DIR)
        with open(args.output, "wb") as f:
            f.write(pdf_bytes)

        size_mb = os.path.getsize(args.output) / (1024 * 1024)
        print(f"\n✅ PDF built: {args.output} ({size_mb:.1f} MB)")

        page_breaks = typst_content.count("#pagebreak")
        print(f"   Estimated {page_breaks}+ pages")

    except Exception as e:
        print(f"\n❌ Typst compilation failed: {e}")
        print(f"   Content file preserved at: {CONTENT_FILE}")
        print(f"   Template expected at: {TEMPLATE_FILE}")
        sys.exit(1)


if __name__ == "__main__":
    main()
