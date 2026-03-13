#!/usr/bin/env python3
"""
Build EPUB from Maschinenwelt v5 Google Doc.

Pipeline: Google Doc → DOCX export → Pandoc Markdown → fix headings → Pandoc EPUB
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
OUTPUT = os.path.join(BUILD_DIR, 'Maschinenwelt-v5-test.epub')
DOCX_PATH = '/tmp/maschinenwelt-v5.docx'
MD_PATH = '/tmp/maschinenwelt-v5-epub.md'

# CSS for Kindle-optimized styling
EPUB_CSS = """
body {
    font-family: Georgia, "Times New Roman", serif;
    line-height: 1.6;
    margin: 1em;
}
h1 {
    font-size: 1.8em;
    text-align: center;
    margin-top: 3em;
    margin-bottom: 1.5em;
    page-break-before: always;
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
p {
    text-indent: 1.5em;
    margin-top: 0;
    margin-bottom: 0.3em;
    text-align: justify;
}
/* First paragraph after heading: no indent */
h1 + p, h2 + p, h3 + p, hr + p, blockquote + p {
    text-indent: 0;
}
blockquote {
    margin: 1em 2em;
    font-style: italic;
    border-left: 3px solid #ccc;
    padding-left: 1em;
}
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1em auto;
}
/* Figure captions */
.caption, figcaption, p em:only-child {
    text-align: center;
    font-style: italic;
    font-size: 0.9em;
    margin-top: 0.5em;
    margin-bottom: 1em;
    text-indent: 0;
}
/* Impressum */
.impressum {
    font-size: 0.85em;
    line-height: 1.4;
}
/* Endnotes */
.endnotes {
    font-size: 0.85em;
    line-height: 1.3;
}
ul, ol {
    margin: 0.5em 0 0.5em 2em;
}
li {
    margin-bottom: 0.3em;
}
/* Title page */
.title-page {
    text-align: center;
    margin-top: 30%;
}
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
    """Download Google Doc as DOCX"""
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
    """Convert DOCX to Markdown via Pandoc"""
    result = subprocess.run(
        ['pandoc', DOCX_PATH, '-t', 'markdown', '--wrap=none', '--extract-media=/tmp/epub-media'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr}")
        return None
    return result.stdout


def fix_markdown(md):
    """
    Fix markdown for proper EPUB structure:
    1. Separate images from captions (critical for EPUB readers!)
    2. Remove absolute width/height attributes (use CSS max-width instead)
    3. Shift heading levels: ## → #, ### → ##, #### → ###
    4. Add YAML front matter
    5. Clean up formatting artifacts
    6. Remove duplicate TOC (EPUB has its own)
    """
    lines = md.split('\n')
    output = []
    
    # Add YAML front matter
    output.append('---')
    output.append('title: "Maschinenwelt"')
    output.append('subtitle: "Wenn du nichts besitzt, werden sie dich besitzen"')
    output.append('author: "Thomas Huhn"')
    output.append('date: "2026"')
    output.append('lang: de-DE')
    output.append('rights: "© 2026 Thomas Huhn. Alle Rechte vorbehalten."')
    output.append('---')
    output.append('')
    
    skip_toc = False
    skip_title = True  # Skip the first few lines (title/subtitle/author already in YAML)
    title_lines_skipped = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip the raw title lines at the very beginning (before first heading)
        if skip_title:
            if line.startswith('##') or line.startswith('# '):
                skip_title = False
            else:
                title_lines_skipped += 1
                i += 1
                continue
        
        # Skip the Google Docs TOC section (EPUB generates its own)
        if re.match(r'^##\s+\*\*Inhaltsverzeichnis\*\*', line):
            skip_toc = True
            i += 1
            continue
        if skip_toc:
            # End TOC when we hit the next ## heading
            if re.match(r'^##\s+\*\*(?!Inhaltsverzeichnis)', line):
                skip_toc = False
            else:
                i += 1
                continue
        
        # === IMAGE + CAPTION FIX (critical for EPUB) ===
        # Pattern: ![alt](path){width="..." height="..."}*Caption text*
        # This needs to become separate image and caption lines
        img_caption_pattern = r'^(!\[[^\]]*\]\([^)]+\))\{[^}]*\}\*(.+?)\*\s*$'
        img_only_pattern = r'^(!\[[^\]]*\]\([^)]+\))\{[^}]*\}\s*$'
        
        m = re.match(img_caption_pattern, line)
        if m:
            img_part = m.group(1)
            caption_text = m.group(2)
            # Remove width/height from image (CSS handles sizing)
            output.append('')
            output.append(img_part)
            output.append('')
            output.append(f'*{caption_text}*')
            output.append('')
            i += 1
            continue
        
        m2 = re.match(img_only_pattern, line)
        if m2:
            img_part = m2.group(1)
            output.append('')
            output.append(img_part)
            output.append('')
            i += 1
            continue
        
        # Also handle images without {}-attributes but with caption on same line
        m3 = re.match(r'^(!\[[^\]]*\]\([^)]+\))\*(.+?)\*\s*$', line)
        if m3:
            img_part = m3.group(1)
            caption_text = m3.group(2)
            output.append('')
            output.append(img_part)
            output.append('')
            output.append(f'*{caption_text}*')
            output.append('')
            i += 1
            continue
        
        # Shift heading levels: ## → #, ### → ##, #### → ###
        if line.startswith('####'):
            line = line.replace('####', '###', 1)
        elif line.startswith('###'):
            line = line.replace('###', '##', 1)
        elif line.startswith('##'):
            line = line.replace('##', '#', 1)
        
        # Clean up bold headings: # **Text** → # Text
        line = re.sub(r'^(#+)\s+\*\*(.+?)\*\*\s*$', r'\1 \2', line)
        
        # Clean up escaped brackets
        line = line.replace('\\[', '[').replace('\\]', ']')
        
        # Fix em dashes
        line = line.replace(' --- ', ' — ')
        line = line.replace('---', '—')
        
        # Fix en dashes in number ranges
        line = re.sub(r'(\d)--(\d)', r'\1–\2', line)
        
        output.append(line)
        i += 1
    
    return '\n'.join(output)


def build_epub(md_path):
    """Build EPUB with Pandoc"""
    # Write CSS
    css_path = '/tmp/epub-kindle.css'
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
        '--metadata', 'subtitle=Wenn du nichts besitzt, werden sie dich besitzen',
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
        # Filter out common warnings
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
    """Verify EPUB structure"""
    import zipfile
    z = zipfile.ZipFile(OUTPUT)
    
    # Count chapters
    chapters = [f for f in z.namelist() if f.startswith('EPUB/text/ch') and f.endswith('.xhtml')]
    images = [f for f in z.namelist() if f.startswith('EPUB/media/') and 'cover' not in f]
    
    # Extract TOC
    nav = z.read('EPUB/nav.xhtml').decode('utf-8')
    toc_entries = re.findall(r'<a[^>]*>([^<]+)</a>', nav)
    toc_entries = [t.strip() for t in toc_entries if t.strip()]
    
    print(f"\n  Chapters: {len(chapters)}")
    print(f"  Images: {len(images)} (+ cover)")
    print(f"  TOC entries: {len(toc_entries)}")
    
    if len(toc_entries) <= 30:
        for entry in toc_entries:
            print(f"    · {entry[:80]}")
    else:
        for entry in toc_entries[:15]:
            print(f"    · {entry[:80]}")
        print(f"    ... ({len(toc_entries) - 15} more)")
    
    # Chapter sizes
    print(f"\n  Chapter file sizes:")
    for ch in sorted(chapters):
        data = z.read(ch)
        print(f"    {ch}: {len(data)/1024:.0f} KB")
    
    z.close()


def main():
    print("=" * 60)
    print("  MASCHINENWELT v5 — EPUB Build")
    print("=" * 60)
    
    print("\n1. Download DOCX from Google Docs...")
    token = get_access_token()
    download_docx(token)
    
    print("\n2. Convert DOCX → Markdown...")
    md = docx_to_markdown()
    if not md:
        return
    print(f"  Raw markdown: {len(md)/1024:.0f} KB")
    
    print("\n3. Fix markdown for EPUB...")
    fixed_md = fix_markdown(md)
    with open(MD_PATH, 'w') as f:
        f.write(fixed_md)
    print(f"  Fixed markdown: {len(fixed_md)/1024:.0f} KB")
    
    # Quick check
    h1_count = len(re.findall(r'^# ', fixed_md, re.MULTILINE))
    h2_count = len(re.findall(r'^## ', fixed_md, re.MULTILINE))
    h3_count = len(re.findall(r'^### ', fixed_md, re.MULTILINE))
    print(f"  Headings: H1={h1_count}, H2={h2_count}, H3={h3_count}")
    
    print("\n4. Build EPUB...")
    if build_epub(MD_PATH):
        print("\n5. Verify EPUB...")
        verify_epub()
    
    print("\n" + "=" * 60)
    print("  ✅ EPUB BUILD COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
