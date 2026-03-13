#!/usr/bin/env python3
"""Convert maschinengeld-v2.txt to Markdown with proper headings for Google Docs upload."""

import re

with open("/tmp/maschinengeld-v2.txt") as f:
    lines = f.readlines()

output = []

# Known beat lines patterns (short standalone italic lines)
beat_line_cache = set()

i = 0
while i < len(lines):
    line = lines[i].rstrip('\n')
    
    # Skip first line (title handled separately)
    if i == 0:
        output.append(f"# {line}")
        i += 1
        continue
    
    # Subtitle
    if i == 1 and line.startswith("Warum"):
        output.append(f"*{line}*")
        i += 1
        continue
    
    # Author
    if i == 2 and line.startswith("Thomas"):
        output.append(f"**{line}**")
        i += 1
        continue
    
    # H2: TEIL headings, Vorwort, Epilog
    if re.match(r'^TEIL [IVX]+:', line):
        output.append(f"\n## {line}")
        i += 1
        continue
    
    # H3: Kapitel headings
    if re.match(r'^Kapitel \d+\w*:', line):
        output.append(f"\n### {line}")
        i += 1
        continue
    
    # H3: Vorwort
    if line == "Vorwort":
        output.append(f"\n## {line}")
        i += 1
        continue
    
    # H3: Epilog
    if re.match(r'^Epilog:', line):
        output.append(f"\n### {line}")
        i += 1
        continue
    
    # H4: Known subheadings
    h4_patterns = [
        r'^Die tektonischen',
        r'^Warum „diesmal',
        r'^Ich bin kein Prophet',
        r'^Eine These, die nie',
        r'^Wie Sie dieses Buch',
        r'^Phase \d:',
        r'^Die Landschaft der KI',
        r'^DeepSeek',
        r'^Die Kurzweil',
        r'^Jede Phase',
        r'^Das Gedankenexperiment',
        r'^Krypto als nativer',
        r'^Smart Contracts',
        r'^Bitcoin als digitales',
        r'^Die Kernthese',
        r'^Stablecoins',
        r'^Mikrotransaktionen',
        r'^Machine-to-Machine',
        r'^Zwei KI-Supermächte',
        r'^America First',
        r'^China: Der unter',
        r'^Europa: Ein Kontinent',
        r'^Der Chip-Krieg',
        r'^Krypto als geopolitischer',
        r'^Warum KI einen',
        r'^Die Zahlen:',
        r'^Warum die Tech',
        r'^Small Modular',
        r'^Vertikale Integration',
        r'^Investmentimplikationen',
        r'^Die ehrliche Rechnung',
        r'^Wissensarbeiter',
        r'^Die Sinn-Krise',
        r'^Politische Radikalisierung',
        r'^Universal Basic',
        r'^Die Gewinner-Verlierer',
        r'^Was das für Investoren',
        r'^EU AI Act',
        r'^USA: Light Touch',
        r'^China: Regulierung',
        r'^Krypto-Regulierung',
        r'^Roboter-Steuern',
        r'^Wer profitiert',
        r'^2026.2028:',
        r'^2028.2031:',
        r'^2031.2035:',
        r'^Drei Szenarien',
        r'^Was Kurzweil',
        r'^Die Geschichte der Interfaces',
        r'^Voice als',
        r'^Brain-Computer Interfaces',
        r'^KI-generierte',
        r'^Die Konvergenz: BCI',
        r'^Die dunkle Seite',
        r'^Investmentimplikationen: BCI',
        r'^Compute-Hunger',
        r'^Wem gehört',
        r'^Bewusstsein, Rechte',
        r'^Die Eigentumsfrage',
        r'^Digitale Souveränität',
        r'^Der philosophische',
        r'^Ein persönlicher',
        r'^Talebs Barbell',
        r'^Der sichere Kern',
        r'^Die asymmetrischen',
        r'^Drei Modellportfolios',
        r'^Timing und Execution',
        r'^Der nächste KI-Winter',
        r'^Regulatorische Über',
        r'^Krypto-Verbote',
        r'^Bewertungsrisiken',
        r'^Black Swans',
        r'^Arbeitsmärkte',
        r'^Technologische Risiken',
        r'^Konzentrationrisiko',
        r'^Der persönliche Stress',
        r'^Howard Marks',
        r'^Was ich bei',
        r'^Peter Thiels',
        r'^Praktischer Aktionsplan',
        r'^Die Schlussfrage',
        r'^Neuralink:',
        r'^Synchron:',
        r'^Merge Labs',
        r'^Paradromics',
        r'^NVIDIA und',
        r'^Das Big-Tech',
        r'^Robotik-Pure',
        r'^Energie & Nuklear',
        r'^ETF-Strategien',
        r'^Bitcoin: Die Basis',
        r'^Ethereum: Smart',
        r'^Stablecoin-Infra',
        r'^KI-Infrastruktur-Token',
        r'^BCI-nahe',
        r'^Private Equity',
        r'^Die Longevity-Revolution',
        r'^Warum Langlebigkeit',
        r'^Die Biologie des Alterns',
        r'^Wer baut',
        r'^Das Smart Money',
        r'^Longevity als',
        r'^Was das für Ihre',
    ]
    
    is_h4 = False
    for pat in h4_patterns:
        if re.match(pat, line):
            is_h4 = True
            break
    
    if is_h4 and len(line) < 120 and len(line) > 5:
        output.append(f"\n#### {line}")
        i += 1
        continue
    
    # Abbildung references - keep as-is
    if re.match(r'^Abbildung \d+:', line):
        output.append(f"\n{line}\n")
        i += 1
        continue
    
    # Beat lines: short standalone paragraphs (italic)
    if line and len(line) < 100 and len(line) > 10:
        prev_empty = (i == 0 or not lines[i-1].strip())
        next_empty = (i + 1 >= len(lines) or not lines[i + 1].strip())
        if prev_empty and next_empty and (line.endswith('.') or line.endswith('?') or line.endswith('!')):
            output.append(f"\n*{line}*\n")
            i += 1
            continue
    
    # Regular paragraph or empty line
    output.append(line)
    i += 1

result = '\n'.join(output)

with open("/tmp/maschinengeld-v2-formatted.md", "w") as f:
    f.write(result)

# Count headings
h1 = result.count('\n# ')
h2 = result.count('\n## ')
h3 = result.count('\n### ')
h4 = result.count('\n#### ')
italics = len(re.findall(r'^\*[^*\n]+\*$', result, re.MULTILINE))

print(f"Formatted output: /tmp/maschinengeld-v2-formatted.md")
print(f"H1: {h1}, H2: {h2}, H3: {h3}, H4: {h4}")
print(f"Beat lines (italic): {italics}")
print(f"Words: {len(result.split())}")
