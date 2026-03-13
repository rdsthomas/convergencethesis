#!/usr/bin/env python3
"""
Add style elements to Maschinenwelt v5 Google Doc — v2.
Batches ALL operations per phase into minimal API calls.

Elements:
1. Epigraphs — motto quote after each chapter heading (already done in v1!)
2. Szenische Trenner — ✦ before H4 subheadings  
3. Key Takeaways — "Auf einen Blick" at end of chapters
4. Checklists — action items at end of investment chapters (14, 15, 16)

Strategy: Collect all inserts, sort by descending index, execute in ONE batchUpdate.
Then apply all styling in a second batchUpdate.
"""

import json
import urllib.request
import urllib.parse
import re
import time

DOC_ID = '1JF7Kei019q0iunIISa-fCq7Y4aLcHWHmkjBOb7MBlms'

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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
    """Execute batch update with retry on rate limit."""
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
    print(f"  ❌ GAVE UP after 5 retries ({label})")
    return None


def get_chapter_key(text):
    m = re.match(r'(Kapitel \d+)', text)
    if m:
        return m.group(1)
    if 'Vorwort' in text:
        return 'Vorwort'
    if 'Epilog' in text:
        return 'Epilog'
    return None


def analyze_doc(doc):
    """Analyze document structure and find boundaries."""
    danksagung_start = 999999
    endnotes_start = 999999
    
    chapters = []  # (key, start, end_of_heading)
    h4s = []       # (start, end, text)
    teil_headings = []  # TEIL I, II, etc.
    
    for elem in doc['body']['content']:
        if 'paragraph' not in elem:
            continue
        p = elem['paragraph']
        style = p.get('paragraphStyle', {}).get('namedStyleType', '')
        text = ''.join(r.get('textRun', {}).get('content', '') for r in p.get('elements', []))
        text_stripped = text.strip()
        
        if text_stripped == 'Danksagung' and style.startswith('HEADING'):
            danksagung_start = min(danksagung_start, elem['startIndex'])
        if text_stripped == 'Endnotes' and style.startswith('HEADING'):
            endnotes_start = min(endnotes_start, elem['startIndex'])
        
        if elem['startIndex'] >= danksagung_start:
            continue
        
        if style == 'HEADING_3' and text_stripped.startswith('Kapitel '):
            chapters.append({
                'key': get_chapter_key(text_stripped),
                'start': elem['startIndex'],
                'end': elem['endIndex'],
                'text': text_stripped,
            })
        elif style == 'HEADING_2' and text_stripped == 'Vorwort':
            chapters.append({
                'key': 'Vorwort',
                'start': elem['startIndex'],
                'end': elem['endIndex'],
                'text': text_stripped,
            })
        elif style == 'HEADING_3' and text_stripped.startswith('Epilog'):
            chapters.append({
                'key': 'Epilog',
                'start': elem['startIndex'],
                'end': elem['endIndex'],
                'text': text_stripped,
            })
        elif style == 'HEADING_4':
            h4s.append({
                'start': elem['startIndex'],
                'end': elem['endIndex'],
                'text': text_stripped,
            })
        elif style == 'HEADING_2' and 'TEIL' in text_stripped:
            teil_headings.append({
                'start': elem['startIndex'],
                'end': elem['endIndex'],
                'text': text_stripped,
            })
    
    # Build list of major section starts (chapters + TEILs) for finding chapter ends
    section_starts = sorted(
        [ch['start'] for ch in chapters] + 
        [t['start'] for t in teil_headings] + 
        [danksagung_start]
    )
    
    # Assign end to each chapter
    for ch in chapters:
        ch['content_end'] = danksagung_start
        for s in section_starts:
            if s > ch['start'] + 10:
                ch['content_end'] = s
                break
    
    return {
        'chapters': chapters,
        'h4s': h4s,
        'danksagung_start': danksagung_start,
        'endnotes_start': endnotes_start,
    }


def main():
    print("=" * 60)
    print("  MASCHINENWELT v5 — Google Doc Style Elements v2")
    print("  (batched API calls)")
    print("=" * 60)
    
    token = get_access_token()
    
    # ━━━ Check if epigraphs already exist ━━━
    doc = get_document(token)
    full_text = ''.join(
        r.get('textRun', {}).get('content', '')
        for elem in doc['body']['content']
        if 'paragraph' in elem
        for r in elem['paragraph'].get('elements', [])
    )
    
    epigraphs_exist = '— William Gibson' in full_text
    if epigraphs_exist:
        print("\n✅ Epigraphs already present — skipping Phase 1")
    
    # ━━━ PHASE 2: SZENISCHE TRENNER ━━━
    print("\n━━━ PHASE 2: SZENISCHE TRENNER ━━━")
    doc = get_document(token)
    info = analyze_doc(doc)
    
    # Check if trenner already inserted
    if '✦' in full_text and full_text.count('✦') > 10:
        print(f"  ✦ already in document ({full_text.count('✦')} times) — skipping")
    else:
        # Collect ALL H4 positions, sorted descending by start index
        h4_positions = sorted(info['h4s'], key=lambda x: x['start'], reverse=True)
        
        # Filter: only before danksagung
        h4_positions = [h for h in h4_positions if h['start'] < info['danksagung_start']]
        
        print(f"  Found {len(h4_positions)} H4 subheadings to add trenner before")
        
        # Split into batches of 15 (each trenner = 3 requests: insert + 2 style updates)
        # 15 trenner = 45 requests per batch — well within limits
        BATCH_SIZE = 15
        total_done = 0
        
        for batch_start in range(0, len(h4_positions), BATCH_SIZE):
            batch = h4_positions[batch_start:batch_start + BATCH_SIZE]
            
            # Build all requests for this batch
            # Since we sorted descending, insertions won't affect each other
            all_requests = []
            
            for h4 in batch:
                idx = h4['start']
                trenner_text = "✦\n"
                
                all_requests.extend([
                    {'insertText': {'location': {'index': idx}, 'text': trenner_text}},
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
                                'bold': False,
                                'italic': False,
                            },
                            'fields': 'fontSize,foregroundColor,bold,italic'
                        }
                    },
                ])
            
            result = batch_update(token, all_requests, f"trenner batch {batch_start//BATCH_SIZE + 1}")
            if result:
                total_done += len(batch)
                print(f"  ✅ Batch {batch_start//BATCH_SIZE + 1}: {len(batch)} trenner inserted (total: {total_done})")
            
            # Re-read document for next batch since indices shifted
            if batch_start + BATCH_SIZE < len(h4_positions):
                time.sleep(2)
                doc = get_document(token)
                info = analyze_doc(doc)
                # Re-sort remaining H4s
                remaining_h4s = sorted(info['h4s'], key=lambda x: x['start'], reverse=True)
                remaining_h4s = [h for h in remaining_h4s if h['start'] < info['danksagung_start']]
                # We need to skip the ones we already processed
                # Since we re-read, just take from the updated list
                h4_positions = remaining_h4s
        
        print(f"\n  Total trenner inserted: {total_done}")
    
    # ━━━ PHASE 3: KEY TAKEAWAYS ━━━
    print("\n━━━ PHASE 3: KEY TAKEAWAYS ━━━")
    
    # Check if already present
    doc = get_document(token)
    full_text = ''.join(
        r.get('textRun', {}).get('content', '')
        for elem in doc['body']['content']
        if 'paragraph' in elem
        for r in elem['paragraph'].get('elements', [])
    )
    
    if '📌 Auf einen Blick' in full_text:
        print("  📌 Already present — skipping")
    else:
        info = analyze_doc(doc)
        
        # Insert takeaways at end of each chapter, working BACKWARDS
        chapters_with_takeaways = [ch for ch in info['chapters'] if ch['key'] in KEY_TAKEAWAYS]
        chapters_with_takeaways.sort(key=lambda x: x['start'], reverse=True)
        
        takeaway_count = 0
        for ch in chapters_with_takeaways:
            key = ch['key']
            items = KEY_TAKEAWAYS[key]
            
            # Build text
            takeaway_text = "\n📌 Auf einen Blick\n"
            for item in items:
                takeaway_text += f"◆ {item}\n"
            
            insert_idx = ch['content_end']
            
            # Insert text
            insert_req = [{'insertText': {'location': {'index': insert_idx}, 'text': takeaway_text}}]
            
            # Style requests
            title_start = insert_idx + 1
            title_end = title_start + len("📌 Auf einen Blick")
            items_start = title_end + 1
            items_end = insert_idx + len(takeaway_text) - 1
            
            style_reqs = [
                # Make sure it's NORMAL_TEXT (not a heading)
                {
                    'updateParagraphStyle': {
                        'range': {'startIndex': title_start, 'endIndex': items_end},
                        'paragraphStyle': {'namedStyleType': 'NORMAL_TEXT'},
                        'fields': 'namedStyleType'
                    }
                },
                # Title: bold, 11pt
                {
                    'updateTextStyle': {
                        'range': {'startIndex': title_start, 'endIndex': title_end},
                        'textStyle': {'bold': True, 'fontSize': {'magnitude': 11, 'unit': 'PT'}},
                        'fields': 'bold,fontSize'
                    }
                },
                # Title spacing
                {
                    'updateParagraphStyle': {
                        'range': {'startIndex': title_start, 'endIndex': title_end},
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
                # Items: 10pt
                {
                    'updateTextStyle': {
                        'range': {'startIndex': items_start, 'endIndex': items_end},
                        'textStyle': {'fontSize': {'magnitude': 10, 'unit': 'PT'}},
                        'fields': 'fontSize'
                    }
                },
            ]
            
            result = batch_update(token, insert_req + style_reqs, f"takeaway {key}")
            if result:
                takeaway_count += 1
                print(f"  ✅ {key}: Key Takeaways inserted")
            
            # Re-read document for fresh indices
            time.sleep(1)
            doc = get_document(token)
            info = analyze_doc(doc)
            # Update remaining chapters
            remaining = [c for c in info['chapters'] if c['key'] in KEY_TAKEAWAYS and c['start'] < ch['start']]
            # The reverse loop continues with original list, but indices shifted,
            # so we need to re-find each chapter. Let's just re-find in the loop.
        
        # Actually, we need to refactor: re-read and re-find each time
        # Let me redo this properly
        takeaway_count = 0
        chapters_done = set()
        
        for kap_num in range(16, 0, -1):
            key = f"Kapitel {kap_num}"
            if key not in KEY_TAKEAWAYS or key in chapters_done:
                continue
            
            doc = get_document(token)
            info = analyze_doc(doc)
            
            # Find this chapter
            ch = next((c for c in info['chapters'] if c['key'] == key), None)
            if not ch:
                print(f"  ❌ {key}: not found")
                continue
            
            items = KEY_TAKEAWAYS[key]
            takeaway_text = "\n📌 Auf einen Blick\n"
            for item in items:
                takeaway_text += f"◆ {item}\n"
            
            insert_idx = ch['content_end']
            
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
                takeaway_count += 1
                chapters_done.add(key)
                print(f"  ✅ {key}: Key Takeaways inserted")
            
            time.sleep(1.5)
        
        print(f"\n  Total takeaways: {takeaway_count}")
    
    # ━━━ PHASE 4: CHECKLISTS ━━━
    print("\n━━━ PHASE 4: CHECKLISTS ━━━")
    
    doc = get_document(token)
    full_text = ''.join(
        r.get('textRun', {}).get('content', '')
        for elem in doc['body']['content']
        if 'paragraph' in elem
        for r in elem['paragraph'].get('elements', [])
    )
    
    if '✅ Was Sie jetzt tun können' in full_text:
        print("  ✅ Already present — skipping")
    else:
        checklist_count = 0
        
        for kap_num in [16, 15, 14]:  # Reverse order
            key = f"Kapitel {kap_num}"
            
            doc = get_document(token)
            info = analyze_doc(doc)
            
            ch = next((c for c in info['chapters'] if c['key'] == key), None)
            if not ch:
                print(f"  ❌ {key}: not found")
                continue
            
            items = CHECKLISTS[key]
            checklist_text = "\n✅ Was Sie jetzt tun können\n"
            for item in items:
                checklist_text += f"☐ {item}\n"
            
            # Insert after takeaways (which are now at chapter end)
            # Find the takeaway for this chapter and insert after it
            insert_idx = ch['content_end']
            
            title_start = insert_idx + 1
            title_end = title_start + len("✅ Was Sie jetzt tun können")
            items_start = title_end + 1
            items_end = insert_idx + len(checklist_text) - 1
            
            all_reqs = [
                {'insertText': {'location': {'index': insert_idx}, 'text': checklist_text}},
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
                            'spaceAbove': {'magnitude': 18, 'unit': 'PT'},
                            'spaceBelow': {'magnitude': 6, 'unit': 'PT'},
                        },
                        'fields': 'spaceAbove,spaceBelow'
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
            
            result = batch_update(token, all_reqs, f"checklist {key}")
            if result:
                checklist_count += 1
                print(f"  ✅ {key}: Checklist inserted")
            
            time.sleep(1.5)
        
        print(f"\n  Total checklists: {checklist_count}")
    
    # ━━━ PHASE 5: PULL QUOTES ━━━
    # Pull quotes need to find the EXACT text in each chapter, then style it
    print("\n━━━ PHASE 5: PULL QUOTES (styling existing text) ━━━")
    
    PULL_QUOTES = {
        'Kapitel 1': 'Und diesmal ist die Transformation radikaler als alles, was wir kennen.',
        'Kapitel 2': 'Wenn ich Klavier übe, werden Sie dadurch nicht besser.',
        'Kapitel 3': 'Das Geld, das Maschinen brauchen, um in einer Welt zu funktionieren, die sie selbst miterschaffen.',
        'Kapitel 4': 'Wer sein Geld nicht selbst verwahrt, besitzt es nicht wirklich.',
        'Kapitel 5': 'Unternehmen, die keine Menschen brauchen, um zu funktionieren.',
        'Kapitel 6': 'Wir konnten keinen europäischen Hoster finden, der das Modell legal betreiben konnte.',
        'Kapitel 7': 'Wer die Energie kontrolliert, kontrolliert das Tempo der KI-Revolution.',
        'Kapitel 8': 'Die größte Gefahr der Maschinenökonomie ist nicht der Kontrollverlust über KI.',
        'Kapitel 9': 'Ob der Roboter besteuert wird oder nicht',
        'Kapitel 10': 'Unternehmen, die KI nicht adoptieren, verschwinden.',
        'Kapitel 11': 'Menschen müssen keine neue Fähigkeit erlernen, um zu sprechen.',
        'Kapitel 12': 'Wir können nicht einmal bei einem anderen Menschen beweisen, dass er bewusst ist.',
        'Kapitel 13': 'Sam Altman hat 180 Millionen Dollar in Retro Biosciences investiert.',
        'Kapitel 14': 'Wer in einem Crash kein Cash hat, kann nur zuschauen',
        'Kapitel 15': '2011 fiel Bitcoin um 93 Prozent.',
        'Kapitel 16': 'Die Frage ist nicht: Kann ich es mir leisten, jetzt zu investieren?',
    }
    
    doc = get_document(token)
    
    # Get full text with indices  
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
    
    pull_quote_count = 0
    style_reqs = []
    
    for key, quote_text in PULL_QUOTES.items():
        # Find the quote in the full text
        # Build character-to-index mapping
        pos = 0
        char_to_idx = {}
        for seg in text_segments:
            for i, c in enumerate(seg['text']):
                char_to_idx[pos] = seg['start'] + i
                pos += 1
        
        # Search for the quote
        char_pos = full_text.find(quote_text)
        if char_pos == -1:
            # Try shorter match
            short = quote_text[:40]
            char_pos = full_text.find(short)
            if char_pos == -1:
                print(f"  ❌ {key}: Quote not found: '{quote_text[:50]}...'")
                continue
            # Find end of sentence
            end_pos = full_text.find('.', char_pos + len(short))
            if end_pos == -1:
                end_pos = char_pos + len(short)
            else:
                end_pos += 1  # include the period
        else:
            end_pos = char_pos + len(quote_text)
        
        doc_start = char_to_idx.get(char_pos)
        doc_end = char_to_idx.get(end_pos - 1, char_to_idx.get(end_pos))
        if doc_start is None or doc_end is None:
            print(f"  ❌ {key}: Could not map indices")
            continue
        doc_end += 1  # exclusive end
        
        # Style: make the paragraph centered, larger, italic, with borders
        style_reqs.extend([
            {
                'updateTextStyle': {
                    'range': {'startIndex': doc_start, 'endIndex': doc_end},
                    'textStyle': {
                        'italic': True,
                        'bold': True,
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
        
        pull_quote_count += 1
    
    if style_reqs:
        result = batch_update(token, style_reqs, "pull quotes")
        if result:
            print(f"\n  ✅ Styled {pull_quote_count} pull quotes in one batch")
        else:
            print(f"\n  ❌ Pull quotes styling failed")
    
    print("\n" + "=" * 60)
    print("  ✅ ALL PHASES COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
