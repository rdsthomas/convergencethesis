#!/usr/bin/env python3
"""
Build EPUB from English translation of "The AI Species".

Applies the same style elements as the German original:
- Drop Caps at chapter starts
- Key Takeaways boxes (📌 Key Takeaways + ◆ items)
- Checklists (✅ What You Can Do Now + ☐ items)
- Epigraphs (italic quotes + attribution)
- Pull Quotes
- Ornamental Breaks (✦)
- Tables with styling
- Glossary entries with bold terms
"""

import os
import re
import subprocess
import sys

INPUT_MD = '/tmp/translation-en-complete.md'
BUILD_DIR = '/root/clawd/projects/convergencethesis/epub-build'
COVER = os.path.join(BUILD_DIR, 'images', 'cover.png')
OUTPUT = '/tmp/The-AI-Species-EN-v5.epub'
PROCESSED_MD = '/tmp/ai-species-en-processed.md'

# Known epigraph sources for detection
EPIGRAPH_SOURCES = [
    'William Gibson', 'Bill Gates', 'Ayn Rand', 'In God We Trust',
    'Kevin Kelly', 'Jensen Huang', 'Frederick Soddy', 'Viktor Frankl',
    'Lord Kelvin', 'Arthur C. Clarke', 'Descartes', 'Aubrey de Grey',
    'Warren Buffett', 'Niels Bohr', 'Chinese proverb', 'Chinesisches Sprichwort',
    'Freely', 'Free after',
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

/* Warning callout box */
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

/* Bibliography / References */
.bib-section p, .bib-section .bib-entry {
    text-indent: 0 !important;
    padding-left: 0 !important;
    margin-left: 0 !important;
    margin: 0.4em 0;
    line-height: 1.5;
}
.bib-section h2, .bib-section h3, .bib-section h4 {
    text-indent: 0 !important;
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

/* Endnotes: hanging indent */
.endnote-entry {
    text-indent: 0 !important;
    padding-left: 2.5em;
    text-indent: -2.5em !important;
    margin: 0.4em 0;
    line-height: 1.5;
    font-size: 0.9em;
}

/* Figure list */
.figure-entry {
    text-indent: 0 !important;
    margin: 0.3em 0;
}

/* Index */
.index-entry {
    text-indent: 0 !important;
    margin: 0.3em 0;
    line-height: 1.5;
}
.index-letter {
    text-indent: 0 !important;
    font-weight: bold;
    font-size: 1.1em;
    color: #1a3a5c;
    margin: 0.8em 0 0.2em 0;
}

/* Subtitle and metadata on title page */
.subtitle {
    text-align: center;
    font-size: 1.1em;
    font-style: italic;
    color: #666;
    margin-top: 0.5em;
}
.author-name {
    text-align: center;
    font-size: 1.2em;
    margin-top: 1em;
}

/* Horizontal rules — use as section separators */
hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 2em auto;
    width: 40%;
}

/* Tables in markdown (pandoc default) */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 0.9em;
}
th {
    background-color: #1a3a5c;
    color: white;
    padding: 0.5em;
    text-align: left;
    border: 1px solid #13304d;
}
td {
    padding: 0.4em 0.5em;
    border: 1px solid #ccc;
}
tr:nth-child(even) td {
    background-color: #f5f8fc;
}
"""


# Portfolio tables for Chapter 14 — English
PORTFOLIO_TABLE_A = """
<table class="portfolio-table">
<caption>Variant A — The Conservative ($100K–$500K)</caption>
<tr><th>Side</th><th>Allocation</th><th>Share</th></tr>
<tr class="section-header"><td colspan="3">Safe Side (70%)</td></tr>
<tr><td>Equities</td><td>Global ETF (S&amp;P 500 / Total Market), tech-overweight</td><td>30%</td></tr>
<tr><td>Big Tech</td><td>NVIDIA, Microsoft, Apple, Alphabet</td><td>15%</td></tr>
<tr><td>Energy</td><td>Cameco, Constellation Energy, NextEra</td><td>10%</td></tr>
<tr><td>Robotics</td><td>Intuitive Surgical, ABB, Fanuc</td><td>10%</td></tr>
<tr><td>Cash</td><td>Money market / high-yield savings</td><td>5%</td></tr>
<tr class="section-header"><td colspan="3">Asymmetric Side (30%)</td></tr>
<tr><td>Bitcoin</td><td>DCA over 6–12 months</td><td>15%</td></tr>
<tr><td>Ethereum</td><td>Layer-2 ecosystem, Agent TAM</td><td>5%</td></tr>
<tr><td>RWA</td><td>BUIDL, Ondo Finance (Tokenized Treasuries)</td><td>5%</td></tr>
<tr><td>Infrastructure</td><td>Coinbase, OLAS, PEAQ, Agent Payment Rails</td><td>5%</td></tr>
<tr class="total-row"><td colspan="2">Total</td><td>100%</td></tr>
</table>
"""

PORTFOLIO_TABLE_B = """
<table class="portfolio-table">
<caption>Variant B — The Balanced ($500K–$2M)</caption>
<tr><th>Side</th><th>Allocation</th><th>Share</th></tr>
<tr class="section-header"><td colspan="3">Safe Side (60%)</td></tr>
<tr><td>Equities</td><td>Global ETF with AI tilt</td><td>20%</td></tr>
<tr><td>Big Tech</td><td>NVIDIA, Microsoft, Apple, Alphabet, Amazon, Meta</td><td>15%</td></tr>
<tr><td>Robotics</td><td>Tesla, Intuitive Surgical, ABB, Figure AI</td><td>10%</td></tr>
<tr><td>Energy</td><td>Cameco, Constellation, NuScale, Oklo, Uranium ETF</td><td>10%</td></tr>
<tr><td>Cash</td><td>Cash reserve</td><td>5%</td></tr>
<tr class="section-header"><td colspan="3">Asymmetric Side (40%)</td></tr>
<tr><td>Bitcoin</td><td>DCA over 12 months</td><td>15%</td></tr>
<tr><td>Ethereum</td><td>Staking, Layer-2 exposure</td><td>8%</td></tr>
<tr><td>DeFi</td><td>Circle (IPO), Aave, Uniswap</td><td>7%</td></tr>
<tr><td>RWA</td><td>Maple, Centrifuge, Hamilton Lane tokenized</td><td>5%</td></tr>
<tr><td>Machine Economy</td><td>Olas, peaq, Fetch.ai/ASI, Render Network</td><td>5%</td></tr>
<tr class="total-row"><td colspan="2">Total</td><td>100%</td></tr>
</table>
"""

PORTFOLIO_TABLE_C = """
<table class="portfolio-table">
<caption>Variant C — The Aggressive ($2M+, high risk tolerance)</caption>
<tr><th>Side</th><th>Allocation</th><th>Share</th></tr>
<tr class="section-header"><td colspan="3">Safe Side (50%)</td></tr>
<tr><td>Big Tech</td><td>NVIDIA, Microsoft, Apple</td><td>15%</td></tr>
<tr><td>Energy</td><td>Nuclear &amp; energy broadly diversified</td><td>15%</td></tr>
<tr><td>Robotics</td><td>Tesla, Intuitive Surgical + venture positions</td><td>10%</td></tr>
<tr><td>Cash / Treasuries</td><td>Tokenized Treasuries, yield-generating</td><td>10%</td></tr>
<tr class="section-header"><td colspan="3">Asymmetric Side (50%)</td></tr>
<tr><td>Bitcoin</td><td>Core position</td><td>20%</td></tr>
<tr><td>Ethereum</td><td>Smart contract platform</td><td>10%</td></tr>
<tr><td>AI Tokens / DeFi</td><td>Render, Filecoin, Olas, ASI Alliance, Aave</td><td>8%</td></tr>
<tr><td>RWA</td><td>Private equity, real estate, private credit</td><td>7%</td></tr>
<tr><td>Venture / Angel</td><td>peaq ecosystem, Robotics DAOs, BCI-adjacent firms</td><td>5%</td></tr>
<tr class="total-row"><td colspan="2">Total</td><td>100%</td></tr>
</table>
"""


def process_markdown(md_text):
    """Process the English markdown: add YAML front matter, wrap style elements in HTML."""
    lines = md_text.split('\n')
    output = []

    # YAML front matter
    output.append('---')
    output.append('title: "The AI Species — Own Them, or They\'ll Own You"')
    output.append('subtitle: "The Investment Blueprint for the Coming AI Tsunami"')
    output.append('author: "Thomas Huhn"')
    output.append('date: "2026"')
    output.append('lang: en-US')
    output.append('rights: "© 2026 Thomas Huhn. All rights reserved."')
    output.append('---')
    output.append('')

    in_backmatter = False
    just_saw_chapter = False
    chapter_start_pending = False
    in_glossary = False
    in_bibliography = False
    in_toc = False
    skip_initial_title = True
    in_key_takeaways = False
    in_checklist = False
    skip_table_after_variant = False
    variant_skip_count = 0

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip initial title block (# The AI Species..., ## The Investment..., ### Thomas Huhn)
        if skip_initial_title:
            if stripped.startswith('# The AI Species') or stripped.startswith('## The Investment') or stripped.startswith('### Thomas Huhn') or stripped == '' or stripped == '---':
                i += 1
                continue
            if stripped.startswith('## Copyright'):
                skip_initial_title = False
                # Fall through to process this line
            else:
                i += 1
                continue

        # Skip Table of Contents section
        if stripped == '## Table of Contents':
            in_toc = True
            i += 1
            continue
        if in_toc:
            if stripped.startswith('## ') and stripped != '## Table of Contents':
                in_toc = False
                # Fall through
            elif stripped == '---':
                in_toc = False
                i += 1
                continue
            else:
                i += 1
                continue

        # === DETECT PART HEADINGS ===
        if stripped.startswith('# PART '):
            output.append(f'# {stripped[2:]}')
            i += 1
            continue

        # === DETECT CHAPTER HEADINGS ===
        chapter_match = re.match(r'^## (Chapter \d+:.+|Foreword|Epilogue:.+|Acknowledgments|Copyright)$', stripped)
        if chapter_match:
            heading_text = chapter_match.group(1)
            if heading_text in ('Acknowledgments',):
                in_backmatter = True
            if not in_backmatter:
                output.append(f'# {heading_text}')
            else:
                output.append(f'# {heading_text}')
            just_saw_chapter = True
            chapter_start_pending = True
            in_glossary = False
            in_bibliography = False
            i += 1
            continue

        # === DETECT APPENDIX HEADINGS ===
        appendix_match = re.match(r'^## (Appendix [A-E] — .+)$', stripped)
        if appendix_match:
            heading_text = appendix_match.group(1)
            if in_bibliography:
                output.append('</div>')
                output.append('')
                in_bibliography = False
            output.append(f'# {heading_text}')
            just_saw_chapter = True
            chapter_start_pending = True
            if 'Glossary' in heading_text:
                in_glossary = True
            elif 'Bibliography' in heading_text:
                in_bibliography = True
                output.append('')
                output.append('<div class="bib-section">')
            else:
                in_glossary = False
            i += 1
            continue

        # === DETECT BACKMATTER HEADINGS (Endnotes, List of Figures, Index, About the Author, Back Cover) ===
        backmatter_match = re.match(r'^## (Endnotes|List of Figures|Index|About the Author|Back Cover)$', stripped)
        if backmatter_match:
            heading_text = backmatter_match.group(1)
            in_backmatter = True
            if in_bibliography:
                output.append('</div>')
                output.append('')
                in_bibliography = False
            output.append(f'# {heading_text}')
            just_saw_chapter = True
            chapter_start_pending = True
            in_glossary = False
            i += 1
            continue

        # === DETECT AND WRAP EPIGRAPHS ===
        # Pattern: *"quote text"* on one line, followed by — Attribution on next
        # Can appear either directly after chapter heading or after a ✦
        if just_saw_chapter:
            if stripped == '' or stripped == '---':
                output.append(line)
                i += 1
                continue

            # ✦ after chapter heading — don't reset just_saw_chapter, skip
            if stripped == '✦' or stripped == '**✦**':
                # Don't add ornamental break here, it's part of the epigraph framing
                i += 1
                continue

            # Check for epigraph: italic quoted text
            epigraph_match = re.match(r'^\*"(.+?)"\*$', stripped)
            if not epigraph_match:
                # Also try: *"text"* with smart quotes
                epigraph_match = re.match(r'^\*[\u201c"](.+?)[\u201d"]\*$', stripped)
            if epigraph_match:
                quote_text = epigraph_match.group(1)
                output.append(f'<div class="epigraph">\u201c{quote_text}\u201d</div>')

                # Check next non-empty line for attribution (skip ✦ and empty lines)
                j = i + 1
                while j < len(lines) and (lines[j].strip() == '' or lines[j].strip() == '✦'):
                    j += 1
                if j < len(lines) and lines[j].strip().startswith('—'):
                    attr_text = lines[j].strip()
                    output.append(f'<div class="epigraph-source">{attr_text}</div>')
                    output.append('')
                    # Skip any trailing ✦ after the attribution
                    j += 1
                    while j < len(lines) and (lines[j].strip() == '' or lines[j].strip() == '✦'):
                        j += 1
                    i = j
                    continue
                else:
                    output.append('')
                    i += 1
                    continue

            # Not an epigraph — this is content
            just_saw_chapter = False

        # === DETECT AND WRAP ✦ ORNAMENTAL BREAKS ===
        if stripped == '✦' or stripped == '**✦**':
            output.append('')
            output.append('<p class="ornamental-break">✦</p>')
            output.append('')
            i += 1
            continue

        # === DETECT AND WRAP --- HORIZONTAL RULES (as subtle dividers, skip if between sections) ===
        if stripped == '---':
            # Only add if not right before/after a heading
            output.append('')
            i += 1
            continue

        # === DETECT AND WRAP KEY TAKEAWAYS ===
        if '📌' in stripped and 'Key Takeaways' in stripped:
            output.append('')
            output.append('<div class="key-takeaways">')
            output.append('<p class="takeaway-title">📌 Key Takeaways</p>')
            i += 1
            # Collect ◆ items and bullet items
            while i < len(lines):
                item_line = lines[i].strip()
                # Strip markdown bold
                item_clean = re.sub(r'\*\*', '', item_line).strip()
                if item_clean.startswith('◆'):
                    output.append(f'<p class="takeaway-item">{item_clean}</p>')
                    i += 1
                elif item_clean.startswith('- '):
                    # Some takeaways use bullet points instead of ◆
                    output.append(f'<p class="takeaway-item">◆ {item_clean[2:]}</p>')
                    i += 1
                elif item_clean == '':
                    # Check if next line has ◆ or -
                    if i + 1 < len(lines):
                        next_clean = lines[i+1].strip()
                        if next_clean.startswith('◆') or (next_clean.startswith('- ') and not next_clean.startswith('---')):
                            i += 1
                            continue
                    break
                else:
                    break
            output.append('</div>')
            output.append('')
            continue

        # === DETECT AND WRAP CHECKLISTS ===
        if '✅' in stripped and 'What You Can Do Now' in stripped:
            output.append('')
            output.append('<div class="checklist-box">')
            output.append('<p class="checklist-title">✅ What You Can Do Now</p>')
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

        # === HANDLE ### SUBHEADINGS ===
        if stripped.startswith('### '):
            clean = re.sub(r'\*\*(.+?)\*\*', r'\\1', stripped[4:]).strip()
            clean = clean.strip('*').strip()

            # Check for "Why" section at the start — it's a sub-heading, promote to H2
            if stripped.startswith('### Why "The AI Species"'):
                output.append(f'## {clean}')
                just_saw_chapter = True
                chapter_start_pending = True
                i += 1
                continue

            # Variant headings — replace table with styled HTML table
            if clean.startswith('Variant A: The Conservative') or clean.startswith('Variant A — The Conservative'):
                output.append(f'### {clean}')
                output.append('')
                output.append(PORTFOLIO_TABLE_A)
                output.append('')
                # Skip the markdown table that follows
                i += 1
                i = skip_markdown_table(lines, i)
                continue
            if clean.startswith('Variant B: The Balanced') or clean.startswith('Variant B — The Balanced'):
                output.append(f'### {clean}')
                output.append('')
                output.append(PORTFOLIO_TABLE_B)
                output.append('')
                i += 1
                i = skip_markdown_table(lines, i)
                continue
            if clean.startswith('Variant C: The Aggressive') and 'Children' not in clean and 'Barbell' not in clean:
                output.append(f'### {clean}')
                output.append('')
                output.append(PORTFOLIO_TABLE_C)
                output.append('')
                i += 1
                i = skip_markdown_table(lines, i)
                continue

            # Regular subheading — keep as H3 but add ornamental break before if appropriate
            if not in_backmatter and not in_glossary and not in_bibliography:
                # Add ornamental break before subheadings if we don't already have one
                last_non_empty = ''
                for prev in reversed(output):
                    if prev.strip():
                        last_non_empty = prev.strip()
                        break
                if '✦' not in last_non_empty and 'ornamental-break' not in last_non_empty and 'epigraph' not in last_non_empty:
                    output.append('')
                    output.append('<p class="ornamental-break">✦</p>')
                    output.append('')
            output.append(f'### {clean}')
            i += 1
            continue

        # === DROP CAP for first content paragraph after chapter heading ===
        if chapter_start_pending and stripped and not stripped.startswith('#') and not stripped.startswith('<') and not stripped.startswith('!') and not stripped.startswith('*"') and stripped != '---':
            # Check it's actual content, not a style element
            if not stripped.startswith('✦') and not stripped.startswith('📌') and not stripped.startswith('✅') and not stripped.startswith('◆') and not stripped.startswith('☐'):
                if not stripped.startswith('—'):
                    output.append(f'<p class="drop-cap">{stripped}</p>')
                    output.append('')
                    chapter_start_pending = False
                    i += 1
                    continue

        # === GLOSSARY ENTRIES: "**Term:** Explanation" or "**Term (context):** Explanation" ===
        if in_glossary and stripped and not stripped.startswith('#'):
            glossary_match = re.match(r'^\*\*(.+?)\*\*\s*(.+)$', stripped)
            if glossary_match:
                term = glossary_match.group(1).rstrip(':')
                explanation = glossary_match.group(2).lstrip(':').strip()
                output.append(f'<p class="glossary-entry"><strong>{term}:</strong> {explanation}</p>')
                i += 1
                continue

        # === IMPORTANT NOTICE / WARNING BOX ===
        if stripped == 'Important Notice' or stripped == '**Important Notice**':
            hint_lines = []
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            while j < len(lines) and lines[j].strip() != '' and not lines[j].strip().startswith('Appendix') and not lines[j].strip().startswith('#'):
                hint_lines.append(lines[j].strip())
                j += 1
            hint_text = ' '.join(hint_lines)
            output.append('')
            output.append('<div class="callout-warning">')
            output.append('<p class="callout-warning-title">⚠️ Important Notice</p>')
            output.append(f'<p>{hint_text}</p>')
            output.append('</div>')
            output.append('')
            i = j
            continue

        # Default: pass through
        output.append(line)
        i += 1

    # Close any open bib-section div
    if in_bibliography:
        output.append('</div>')

    return '\n'.join(output)


def skip_markdown_table(lines, i):
    """Skip past a markdown table (lines starting with | or empty lines between them)."""
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith('|') or stripped == '':
            i += 1
        else:
            break
    return i


def count_elements(md_text):
    """Count style elements in the output markdown."""
    counts = {
        'Epigraphs': md_text.count('class="epigraph"'),
        'Key Takeaways': md_text.count('class="key-takeaways"'),
        'Checklists': md_text.count('class="checklist-box"'),
        'Ornamental Breaks': md_text.count('class="ornamental-break"'),
        'Drop Caps': md_text.count('class="drop-cap"'),
        'Glossary Entries': md_text.count('class="glossary-entry"'),
        'Portfolio Tables': md_text.count('class="portfolio-table"'),
    }
    return counts


def main():
    print("=" * 60)
    print("  THE AI SPECIES (English) — EPUB Build")
    print("=" * 60)

    # Read input
    print("\n📖 Step 1: Reading English translation...")
    with open(INPUT_MD, 'r') as f:
        md = f.read()
    word_count = len(md.split())
    line_count = len(md.split('\n'))
    print(f"  {line_count} lines, {word_count} words")

    # Process markdown
    print("\n🔧 Step 2: Processing markdown (style elements)...")
    processed = process_markdown(md)
    with open(PROCESSED_MD, 'w') as f:
        f.write(processed)

    counts = count_elements(processed)
    for name, count in counts.items():
        print(f"  {name}: {count}")

    # Write CSS
    print("\n🎨 Step 3: Writing CSS...")
    css_path = '/tmp/epub-style-en.css'
    with open(css_path, 'w') as f:
        f.write(EPUB_CSS)

    # Build EPUB
    print("\n📖 Step 4: Building EPUB with Pandoc...")
    cmd = [
        'pandoc', PROCESSED_MD,
        '-o', OUTPUT,
        '--epub-cover-image', COVER,
        '--css', css_path,
        '--toc', '--toc-depth=2',
        '--epub-chapter-level=1',
        '-f', 'markdown+raw_html+smart',
        '--metadata', 'title=The AI Species — Own Them, or They\'ll Own You',
        '--metadata', 'author=Thomas Huhn',
        '--metadata', 'lang=en-US',
        '--metadata', 'date=2026',
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr}")
        sys.exit(1)

    size = os.path.getsize(OUTPUT)
    print(f"  EPUB built: {size/1024:.0f} KB")

    # Quick EPUB analysis
    import zipfile
    with zipfile.ZipFile(OUTPUT) as z:
        xhtml_count = sum(1 for f in z.namelist() if f.endswith('.xhtml'))
        image_count = sum(1 for f in z.namelist() if f.endswith('.png') or f.endswith('.jpg'))
    print(f"  Chapters (XHTML files): {xhtml_count}")
    print(f"  Images: {image_count}")

    print("\n" + "=" * 60)
    print(f"  ✅ EPUB built: {OUTPUT}")
    print("=" * 60)


if __name__ == '__main__':
    main()
