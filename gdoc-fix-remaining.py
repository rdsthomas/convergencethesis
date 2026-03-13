#!/usr/bin/env python3
"""
Fix remaining style elements in Maschinenwelt v5 Google Doc.
Phase 1 (Epigraphs): DONE (16/16)
Phase 2 (Trenner): PARTIAL (48/68) — need remaining ~20
Phase 3 (Key Takeaways): PARTIAL (2/16) — need remaining 14
Phase 4 (Checklists): DONE (3/3)
Phase 5 (Pull Quotes): PARTIAL (14/16) — need Kap 10 + 13

Strategy: Re-read doc, find what's missing, insert with proper rate limiting.
"""

import json
import urllib.request
import urllib.parse
import re
import time

DOC_ID = '1JF7Kei019q0iunIISa-fCq7Y4aLcHWHmkjBOb7MBlms'

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
        'Die Machine-to-Machine Economy funktioniert bereits heute.',
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


def get_document(token):
    url = f'https://docs.googleapis.com/v1/documents/{DOC_ID}'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())


def batch_update(token, requests, label=""):
    if not requests:
        return None
    url = f'https://docs.googleapis.com/v1/documents/{DOC_ID}:batchUpdate'
    body = json.dumps({'requests': requests}).encode()
    for attempt in range(5):
        req = urllib.request.Request(url, data=body, headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })
        try:
            resp = urllib.request.urlopen(req)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 30 * (attempt + 1)
                print(f"  ⏳ Rate limited ({label}), waiting {wait}s... (attempt {attempt+1}/5)")
                time.sleep(wait)
            else:
                error_body = e.read().decode()
                print(f"  ❌ ERROR {e.code} ({label}): {error_body[:300]}")
                return None
    return None


def get_chapter_key(text):
    m = re.match(r'Kapitel (\d+)', text)
    if m:
        return f"Kapitel {int(m.group(1))}"
    return None


def main():
    print("=" * 60)
    print("  FIX REMAINING STYLE ELEMENTS")
    print("=" * 60)
    
    token = get_access_token()
    doc = get_document(token)
    
    # Build full text to check what exists
    full_text = ''
    for elem in doc['body']['content']:
        if 'paragraph' in elem:
            for r in elem['paragraph'].get('elements', []):
                if 'textRun' in r:
                    full_text += r['textRun']['content']
    
    # ━━━ PHASE A: Find which Key Takeaways are missing ━━━
    print("\n━━━ PHASE A: KEY TAKEAWAYS ━━━")
    
    # Find which chapters already have takeaways
    # Search for each chapter's first takeaway item
    chapters_with_takeaways = set()
    for key, items in KEY_TAKEAWAYS.items():
        # Check if the first item text exists in the doc
        if items[0][:30] in full_text:
            chapters_with_takeaways.add(key)
    
    missing_takeaways = [k for k in KEY_TAKEAWAYS if k not in chapters_with_takeaways]
    print(f"  Existing: {sorted(chapters_with_takeaways)}")
    print(f"  Missing: {sorted(missing_takeaways)}")
    
    if missing_takeaways:
        # Find Danksagung boundary
        dank_start = 999999
        for elem in doc['body']['content']:
            if 'paragraph' in elem:
                text = ''.join(r.get('textRun', {}).get('content', '') for r in elem['paragraph'].get('elements', []))
                if text.strip() == 'Danksagung':
                    dank_start = elem['startIndex']
                    break
        
        # Insert missing takeaways, from highest chapter number to lowest
        missing_sorted = sorted(missing_takeaways, key=lambda k: int(re.search(r'\d+', k).group()), reverse=True)
        
        for key in missing_sorted:
            # Re-read document each time
            doc = get_document(token)
            
            # Find this chapter heading
            ch_start = None
            ch_heading_end = None
            for elem in doc['body']['content']:
                if 'paragraph' in elem:
                    p = elem['paragraph']
                    style = p.get('paragraphStyle', {}).get('namedStyleType', '')
                    text = ''.join(r.get('textRun', {}).get('content', '') for r in p.get('elements', []))
                    text_stripped = text.strip()
                    if style == 'HEADING_3' and get_chapter_key(text_stripped) == key and elem['startIndex'] < dank_start:
                        ch_start = elem['startIndex']
                        ch_heading_end = elem['endIndex']
                        break
            
            if ch_start is None:
                print(f"  ❌ {key}: heading not found")
                continue
            
            # Find end of chapter (next H2/H3 or TEIL or Danksagung)
            # Re-read danksagung
            dank_fresh = 999999
            for elem in doc['body']['content']:
                if 'paragraph' in elem:
                    text = ''.join(r.get('textRun', {}).get('content', '') for r in elem['paragraph'].get('elements', []))
                    if text.strip() == 'Danksagung':
                        dank_fresh = elem['startIndex']
                        break
            
            ch_end = dank_fresh
            found = False
            for elem in doc['body']['content']:
                if 'paragraph' in elem:
                    p = elem['paragraph']
                    style = p.get('paragraphStyle', {}).get('namedStyleType', '')
                    if style in ('HEADING_2', 'HEADING_3'):
                        if elem['startIndex'] == ch_start:
                            found = True
                            continue
                        if found and elem['startIndex'] > ch_start:
                            ch_end = elem['startIndex']
                            break
            
            items = KEY_TAKEAWAYS[key]
            takeaway_text = "\n📌 Auf einen Blick\n"
            for item in items:
                takeaway_text += f"◆ {item}\n"
            
            insert_idx = ch_end
            title_start = insert_idx + 1
            title_end = title_start + len("📌 Auf einen Blick")
            items_start = title_end + 1
            items_end = insert_idx + len(takeaway_text) - 1
            
            all_reqs = [
                {'insertText': {'location': {'index': insert_idx}, 'text': takeaway_text}},
                {
                    'updateParagraphStyle': {
                        'range': {'startIndex': title_start, 'endIndex': items_end},
                        'paragraphStyle': {'namedStyleType': 'NORMAL_TEXT'},
                        'fields': 'namedStyleType'
                    }
                },
                {
                    'updateTextStyle': {
                        'range': {'startIndex': title_start, 'endIndex': title_end},
                        'textStyle': {'bold': True, 'fontSize': {'magnitude': 11, 'unit': 'PT'}},
                        'fields': 'bold,fontSize'
                    }
                },
                {
                    'updateParagraphStyle': {
                        'range': {'startIndex': title_start, 'endIndex': title_end + 1},
                        'paragraphStyle': {
                            'spaceAbove': {'magnitude': 24, 'unit': 'PT'},
                            'spaceBelow': {'magnitude': 6, 'unit': 'PT'},
                            'borderTop': {
                                'color': {'color': {'rgbColor': {'red': 0.7, 'green': 0.7, 'blue': 0.7}}},
                                'width': {'magnitude': 1, 'unit': 'PT'},
                                'padding': {'magnitude': 8, 'unit': 'PT'},
                                'dashStyle': 'SOLID',
                            },
                        },
                        'fields': 'spaceAbove,spaceBelow,borderTop'
                    }
                },
                {
                    'updateTextStyle': {
                        'range': {'startIndex': items_start, 'endIndex': items_end},
                        'textStyle': {'fontSize': {'magnitude': 10, 'unit': 'PT'}},
                        'fields': 'fontSize'
                    }
                },
            ]
            
            result = batch_update(token, all_reqs, f"takeaway {key}")
            if result:
                print(f"  ✅ {key}")
            else:
                print(f"  ❌ {key}: failed")
            
            time.sleep(2)
    
    # ━━━ PHASE B: Fix missing trenner ━━━
    print("\n━━━ PHASE B: SZENISCHE TRENNER ━━━")
    doc = get_document(token)
    
    # Find Danksagung
    dank_start = 999999
    for elem in doc['body']['content']:
        if 'paragraph' in elem:
            text = ''.join(r.get('textRun', {}).get('content', '') for r in elem['paragraph'].get('elements', []))
            if text.strip() == 'Danksagung':
                dank_start = elem['startIndex']
                break
    
    # Find all H4s and check which ones have a ✦ paragraph right before them
    h4s_missing_trenner = []
    prev_text = ''
    prev_elem = None
    
    for elem in doc['body']['content']:
        if elem.get('startIndex', 0) >= dank_start:
            break
        if 'paragraph' in elem:
            p = elem['paragraph']
            style = p.get('paragraphStyle', {}).get('namedStyleType', '')
            text = ''.join(r.get('textRun', {}).get('content', '') for r in p.get('elements', []))
            text_stripped = text.strip()
            
            if style == 'HEADING_4' and text_stripped:
                # Check if previous paragraph was ✦
                if prev_text != '✦':
                    h4s_missing_trenner.append({
                        'start': elem['startIndex'],
                        'text': text_stripped[:50],
                    })
            
            prev_text = text_stripped
            prev_elem = elem
    
    print(f"  H4s missing trenner: {len(h4s_missing_trenner)}")
    
    if h4s_missing_trenner:
        # Insert in batches of 10, from bottom to top
        h4s_missing_trenner.sort(key=lambda x: x['start'], reverse=True)
        
        BATCH_SIZE = 10
        total_done = 0
        
        for batch_idx in range(0, len(h4s_missing_trenner), BATCH_SIZE):
            # Re-read document for fresh indices
            doc = get_document(token)
            
            # Re-find missing H4s
            dank_start = 999999
            for elem in doc['body']['content']:
                if 'paragraph' in elem:
                    text = ''.join(r.get('textRun', {}).get('content', '') for r in elem['paragraph'].get('elements', []))
                    if text.strip() == 'Danksagung':
                        dank_start = elem['startIndex']
                        break
            
            missing = []
            prev_text = ''
            for elem in doc['body']['content']:
                if elem.get('startIndex', 0) >= dank_start:
                    break
                if 'paragraph' in elem:
                    p = elem['paragraph']
                    style = p.get('paragraphStyle', {}).get('namedStyleType', '')
                    text = ''.join(r.get('textRun', {}).get('content', '') for r in p.get('elements', []))
                    text_stripped = text.strip()
                    if style == 'HEADING_4' and text_stripped and prev_text != '✦':
                        missing.append(elem['startIndex'])
                    prev_text = text_stripped
            
            if not missing:
                break
            
            # Take batch from the end (highest indices first)
            missing.sort(reverse=True)
            batch = missing[:BATCH_SIZE]
            
            all_reqs = []
            for idx in batch:
                all_reqs.extend([
                    {'insertText': {'location': {'index': idx}, 'text': '✦\n'}},
                    {
                        'updateParagraphStyle': {
                            'range': {'startIndex': idx, 'endIndex': idx + 1},
                            'paragraphStyle': {
                                'alignment': 'CENTER',
                                'spaceAbove': {'magnitude': 18, 'unit': 'PT'},
                                'spaceBelow': {'magnitude': 6, 'unit': 'PT'},
                                'namedStyleType': 'NORMAL_TEXT',
                            },
                            'fields': 'alignment,spaceAbove,spaceBelow,namedStyleType'
                        }
                    },
                    {
                        'updateTextStyle': {
                            'range': {'startIndex': idx, 'endIndex': idx + 1},
                            'textStyle': {
                                'fontSize': {'magnitude': 14, 'unit': 'PT'},
                                'foregroundColor': {'color': {'rgbColor': {'red': 0.55, 'green': 0.55, 'blue': 0.55}}},
                                'bold': False, 'italic': False,
                            },
                            'fields': 'fontSize,foregroundColor,bold,italic'
                        }
                    },
                ])
            
            result = batch_update(token, all_reqs, f"trenner batch {batch_idx//BATCH_SIZE + 1}")
            if result:
                total_done += len(batch)
                print(f"  ✅ Batch {batch_idx//BATCH_SIZE + 1}: +{len(batch)} trenner (total new: {total_done})")
            
            time.sleep(3)
        
        print(f"  Added {total_done} missing trenner")
    
    # ━━━ PHASE C: Fix missing Pull Quotes (Kap 10 + 13) ━━━
    print("\n━━━ PHASE C: MISSING PULL QUOTES ━━━")
    doc = get_document(token)
    
    # Build full text with position mapping
    text_segments = []
    for elem in doc['body']['content']:
        if 'paragraph' in elem:
            for r in elem['paragraph'].get('elements', []):
                if 'textRun' in r:
                    text_segments.append({
                        'text': r['textRun']['content'],
                        'start': r['startIndex'],
                        'end': r['endIndex'],
                    })
    
    full_text = ''.join(s['text'] for s in text_segments)
    
    # Build character-to-doc-index mapping
    char_to_idx = {}
    pos = 0
    for seg in text_segments:
        for i in range(len(seg['text'])):
            char_to_idx[pos] = seg['start'] + i
            pos += 1
    
    # Kap 10: "Die Unternehmen, die heute KI adoptieren"
    quote_10 = 'Die Unternehmen, die heute KI adoptieren, sind in der Minderheit.'
    # Kap 13: "hat 180 Millionen Dollar in Retro Biosciences investiert"
    quote_13 = 'hat 180 Millionen Dollar in Retro Biosciences investiert.'
    
    style_reqs = []
    
    for label, quote in [('Kap 10', quote_10), ('Kap 13', quote_13)]:
        char_pos = full_text.find(quote)
        if char_pos == -1:
            # Try shorter
            short = quote[:30]
            char_pos = full_text.find(short)
            if char_pos == -1:
                print(f"  ❌ {label}: not found: '{quote[:40]}...'")
                continue
            # Extend to end of sentence
            end = full_text.find('.', char_pos + len(short))
            if end == -1:
                end = char_pos + len(short)
            else:
                end += 1
        else:
            end = char_pos + len(quote)
        
        doc_start = char_to_idx.get(char_pos)
        doc_end = char_to_idx.get(end - 1)
        if doc_start is None or doc_end is None:
            print(f"  ❌ {label}: index mapping failed")
            continue
        doc_end += 1
        
        # For Kap 13, we want the full sentence starting with "Sam Altman"
        if label == 'Kap 13':
            # Find "Sam Altman" or beginning of sentence before "hat 180"
            # Look backwards for "Sam" or start of sentence
            look_back = full_text[max(0, char_pos-100):char_pos]
            # Find last period or newline before this
            last_break = max(look_back.rfind('. '), look_back.rfind('\n'))
            if last_break >= 0:
                sentence_start = char_pos - (len(look_back) - last_break - 1)
                if sentence_start >= 0:
                    # Trim leading whitespace
                    while sentence_start < char_pos and full_text[sentence_start] in ' \n':
                        sentence_start += 1
                    doc_start = char_to_idx.get(sentence_start, doc_start)
        
        context = full_text[char_pos:min(end, char_pos+80)]
        print(f"  {label}: '{context[:60]}...' [{doc_start}-{doc_end}]")
        
        style_reqs.extend([
            {
                'updateTextStyle': {
                    'range': {'startIndex': doc_start, 'endIndex': doc_end},
                    'textStyle': {
                        'italic': True, 'bold': True,
                        'fontSize': {'magnitude': 13, 'unit': 'PT'},
                    },
                    'fields': 'italic,bold,fontSize'
                }
            },
            {
                'updateParagraphStyle': {
                    'range': {'startIndex': doc_start, 'endIndex': doc_end},
                    'paragraphStyle': {
                        'alignment': 'CENTER',
                        'spaceAbove': {'magnitude': 18, 'unit': 'PT'},
                        'spaceBelow': {'magnitude': 18, 'unit': 'PT'},
                        'indentStart': {'magnitude': 36, 'unit': 'PT'},
                        'indentEnd': {'magnitude': 36, 'unit': 'PT'},
                        'borderTop': {
                            'color': {'color': {'rgbColor': {'red': 0.6, 'green': 0.6, 'blue': 0.6}}},
                            'width': {'magnitude': 0.5, 'unit': 'PT'},
                            'padding': {'magnitude': 8, 'unit': 'PT'},
                            'dashStyle': 'SOLID',
                        },
                        'borderBottom': {
                            'color': {'color': {'rgbColor': {'red': 0.6, 'green': 0.6, 'blue': 0.6}}},
                            'width': {'magnitude': 0.5, 'unit': 'PT'},
                            'padding': {'magnitude': 8, 'unit': 'PT'},
                            'dashStyle': 'SOLID',
                        },
                    },
                    'fields': 'alignment,spaceAbove,spaceBelow,indentStart,indentEnd,borderTop,borderBottom'
                }
            },
        ])
    
    if style_reqs:
        result = batch_update(token, style_reqs, "pull quotes fix")
        if result:
            print(f"  ✅ Missing pull quotes styled")
    
    # ━━━ FINAL COUNT ━━━
    print("\n━━━ FINAL VERIFICATION ━━━")
    doc = get_document(token)
    full_text = ''
    for elem in doc['body']['content']:
        if 'paragraph' in elem:
            for r in elem['paragraph'].get('elements', []):
                if 'textRun' in r:
                    full_text += r['textRun']['content']
    
    print(f"  ✦ Trenner: {full_text.count('✦')}")
    print(f"  📌 Auf einen Blick: {full_text.count('📌 Auf einen Blick')}")
    print(f"  ✅ Was Sie jetzt tun können: {full_text.count('✅ Was Sie jetzt tun können')}")
    print(f"  ◆ takeaway items: {full_text.count('◆')}")
    print(f"  ☐ checklist items: {full_text.count('☐')}")
    
    print("\n" + "=" * 60)
    print("  ✅ ALL FIXES COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
