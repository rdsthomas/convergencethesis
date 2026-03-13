#!/usr/bin/env python3
"""
Add style elements to Maschinenwelt v5 Google Doc.

Elements added:
1. Epigraphs — motto quote after each chapter heading
2. Pull Quotes — highlighted quotes within chapters
3. Szenische Trenner — ✦ ornaments before H4 subheadings
4. Key Takeaways — summary box at end of each chapter (via plain text, styled)
5. Checklists — action items at end of investment chapters

Strategy: Insert text in REVERSE order (highest index first) so that
earlier indices remain valid after each insertion.
"""

import json
import urllib.request
import urllib.parse
import time

DOC_ID = '1JF7Kei019q0iunIISa-fCq7Y4aLcHWHmkjBOb7MBlms'

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EPIGRAPHS = {
    'Kapitel 1': ('„Die Zukunft ist schon da — sie ist nur ungleich verteilt."', '— William Gibson'),
    'Kapitel 2': ('„Wir überschätzen immer die Veränderung der nächsten zwei Jahre und unterschätzen die Veränderung der nächsten zehn."', '— Bill Gates'),
    'Kapitel 3': ('„Geld ist nur ein Werkzeug. Es bringt dich überall hin, aber es ersetzt dich nicht als Fahrer."', '— Ayn Rand'),
    'Kapitel 4': ('„In der Kryptographie vertrauen wir."', '— Frei nach „In God We Trust"'),
    'Kapitel 5': ('„Das Netz kennt keinen Schlaf."', '— Kevin Kelly'),
    'Kapitel 6': ('„Wer die Chips kontrolliert, kontrolliert die Zukunft."', '— Frei nach Jensen Huang'),
    'Kapitel 7': ('„Zivilisation ist im Wesentlichen ein Wettlauf um Energie."', '— Frederick Soddy'),
    'Kapitel 8': ('„Wer einen Sinn zu leben hat, erträgt fast jedes Wie."', '— Viktor Frankl'),
    'Kapitel 9': ('„Regulierung ist der Versuch, mit den Werkzeugen von gestern die Probleme von morgen zu lösen."', ''),
    'Kapitel 10': ('„Schwerer-als-Luft-Flugmaschinen sind unmöglich."', '— Lord Kelvin, 1895'),
    'Kapitel 11': ('„Jede hinreichend fortgeschrittene Technologie ist von Magie nicht zu unterscheiden."', '— Arthur C. Clarke'),
    'Kapitel 12': ('„Cogito, ergo sum — aber was, wenn die Maschine auch denkt?"', '— Frei nach Descartes'),
    'Kapitel 13': ('„Der erste Mensch, der 1.000 Jahre alt wird, lebt möglicherweise bereits."', '— Aubrey de Grey'),
    'Kapitel 14': ('„Rule No. 1: Never lose money. Rule No. 2: Never forget Rule No. 1."', '— Warren Buffett'),
    'Kapitel 15': ('„Es ist schwer, Vorhersagen zu machen, besonders über die Zukunft."', '— Niels Bohr (zugeschrieben)'),
    'Kapitel 16': ('„Die beste Zeit, einen Baum zu pflanzen, war vor zwanzig Jahren. Die zweitbeste Zeit ist jetzt."', '— Chinesisches Sprichwort'),
}

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


def batch_update(token, requests):
    url = f'https://docs.googleapis.com/v1/documents/{DOC_ID}:batchUpdate'
    body = json.dumps({'requests': requests}).encode()
    req = urllib.request.Request(url, data=body, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    })
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"  ERROR {e.code}: {error_body[:500]}")
        return None


def get_chapter_key(text):
    """Extract 'Kapitel N' from heading text."""
    import re
    m = re.match(r'(Kapitel \d+)', text)
    if m:
        return m.group(1)
    if 'Vorwort' in text:
        return 'Vorwort'
    if 'Epilog' in text:
        return 'Epilog'
    return None


def find_chapters_and_h4s(doc, danksagung_start):
    """Find all chapter headings (H3) and subheadings (H4) in main content."""
    chapters = []
    h4s = []
    
    for elem in doc['body']['content']:
        if elem.get('startIndex', 0) >= danksagung_start:
            break
        if 'paragraph' not in elem:
            continue
        p = elem['paragraph']
        style = p.get('paragraphStyle', {}).get('namedStyleType', '')
        text = ''.join(r.get('textRun', {}).get('content', '') for r in p.get('elements', []))
        text = text.strip()
        
        if not text:
            continue
            
        if style == 'HEADING_3' and (text.startswith('Kapitel ') or text.startswith('Epilog')):
            chapters.append({
                'start': elem['startIndex'],
                'end': elem['endIndex'],
                'text': text,
                'key': get_chapter_key(text),
            })
        elif style == 'HEADING_2' and text == 'Vorwort':
            chapters.append({
                'start': elem['startIndex'],
                'end': elem['endIndex'],
                'text': text,
                'key': 'Vorwort',
            })
        elif style == 'HEADING_4' and elem.get('startIndex', 0) > 7200:
            h4s.append({
                'start': elem['startIndex'],
                'end': elem['endIndex'],
                'text': text,
            })
    
    return chapters, h4s


def main():
    print("=" * 60)
    print("  MASCHINENWELT v5 — Google Doc Style Elements")
    print("=" * 60)
    
    token = get_access_token()
    
    # Phase 1: Add EPIGRAPHS after chapter headings
    # Must re-read document between phases since indices shift
    
    print("\n━━━ PHASE 1: EPIGRAPHS ━━━")
    doc = get_document(token)
    chapters, _ = find_chapters_and_h4s(doc, 447220)
    
    # Work in reverse order
    epigraph_count = 0
    for ch in reversed(chapters):
        key = ch['key']
        if key not in EPIGRAPHS:
            continue
        
        quote, source = EPIGRAPHS[key]
        insert_idx = ch['end']  # Insert right after the heading
        
        # Build the epigraph text
        if source:
            epi_text = f"\n{quote}\n{source}\n"
        else:
            epi_text = f"\n{quote}\n"
        
        requests = [
            # Insert the text
            {'insertText': {'location': {'index': insert_idx}, 'text': epi_text}},
        ]
        
        # Style the inserted text
        quote_start = insert_idx + 1  # after first \n
        quote_end = insert_idx + 1 + len(quote)
        
        style_requests = [
            # Quote text: italic, 10pt, gray, right-aligned
            {
                'updateTextStyle': {
                    'range': {'startIndex': quote_start, 'endIndex': quote_end},
                    'textStyle': {
                        'italic': True,
                        'fontSize': {'magnitude': 10, 'unit': 'PT'},
                        'foregroundColor': {'color': {'rgbColor': {'red': 0.4, 'green': 0.4, 'blue': 0.4}}},
                    },
                    'fields': 'italic,fontSize,foregroundColor'
                }
            },
            {
                'updateParagraphStyle': {
                    'range': {'startIndex': quote_start, 'endIndex': quote_end},
                    'paragraphStyle': {
                        'alignment': 'END',
                        'spaceAbove': {'magnitude': 6, 'unit': 'PT'},
                        'spaceBelow': {'magnitude': 2, 'unit': 'PT'},
                    },
                    'fields': 'alignment,spaceAbove,spaceBelow'
                }
            },
        ]
        
        if source:
            source_start = quote_end + 1  # after \n
            source_end = source_start + len(source)
            style_requests.extend([
                {
                    'updateTextStyle': {
                        'range': {'startIndex': source_start, 'endIndex': source_end},
                        'textStyle': {
                            'italic': False,
                            'fontSize': {'magnitude': 9, 'unit': 'PT'},
                            'foregroundColor': {'color': {'rgbColor': {'red': 0.5, 'green': 0.5, 'blue': 0.5}}},
                        },
                        'fields': 'italic,fontSize,foregroundColor'
                    }
                },
                {
                    'updateParagraphStyle': {
                        'range': {'startIndex': source_start, 'endIndex': source_end},
                        'paragraphStyle': {
                            'alignment': 'END',
                            'spaceAbove': {'magnitude': 0, 'unit': 'PT'},
                            'spaceBelow': {'magnitude': 12, 'unit': 'PT'},
                        },
                        'fields': 'alignment,spaceAbove,spaceBelow'
                    }
                },
            ])
        
        result = batch_update(token, requests + style_requests)
        if result:
            epigraph_count += 1
            print(f"  ✅ {key}: Epigraph inserted")
        else:
            print(f"  ❌ {key}: Failed")
        time.sleep(0.3)
    
    print(f"\n  Total epigraphs: {epigraph_count}")
    
    # Phase 2: Add SZENISCHE TRENNER (✦) before H4 subheadings
    print("\n━━━ PHASE 2: SZENISCHE TRENNER ━━━")
    doc = get_document(token)
    chapters, h4s = find_chapters_and_h4s(doc, 500000)  # Use high number, will be recalculated
    
    # Find Danksagung again
    dank_start = 999999
    for elem in doc['body']['content']:
        if 'paragraph' in elem:
            text = ''.join(r.get('textRun', {}).get('content', '') for r in elem['paragraph'].get('elements', []))
            if text.strip() == 'Danksagung':
                dank_start = elem['startIndex']
                break
    
    # Filter H4s to only those before Danksagung
    h4s = [h for h in h4s if h['start'] < dank_start]
    
    trenner_count = 0
    for h4 in reversed(h4s):
        insert_idx = h4['start']
        trenner_text = "✦\n"
        
        requests = [
            {'insertText': {'location': {'index': insert_idx}, 'text': trenner_text}},
            {
                'updateParagraphStyle': {
                    'range': {'startIndex': insert_idx, 'endIndex': insert_idx + len(trenner_text) - 1},
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
                    'range': {'startIndex': insert_idx, 'endIndex': insert_idx + 1},
                    'textStyle': {
                        'fontSize': {'magnitude': 14, 'unit': 'PT'},
                        'foregroundColor': {'color': {'rgbColor': {'red': 0.55, 'green': 0.55, 'blue': 0.55}}},
                    },
                    'fields': 'fontSize,foregroundColor'
                }
            },
        ]
        
        result = batch_update(token, requests)
        if result:
            trenner_count += 1
        time.sleep(0.2)
    
    print(f"  Total trenner: {trenner_count}")
    
    # Phase 3: Add KEY TAKEAWAYS at end of each chapter
    print("\n━━━ PHASE 3: KEY TAKEAWAYS ━━━")
    doc = get_document(token)
    
    # Re-find chapters with updated indices
    dank_start = 999999
    for elem in doc['body']['content']:
        if 'paragraph' in elem:
            text = ''.join(r.get('textRun', {}).get('content', '') for r in elem['paragraph'].get('elements', []))
            if text.strip() == 'Danksagung':
                dank_start = elem['startIndex']
                break
    
    chapters_new, _ = find_chapters_and_h4s(doc, dank_start)
    
    # For each chapter, find where it ends (= start of next chapter/section)
    # Then insert Key Takeaways before that
    takeaway_count = 0
    
    # Build chapter end points
    all_headings = []
    for elem in doc['body']['content']:
        if elem.get('startIndex', 0) >= dank_start:
            break
        if 'paragraph' in elem:
            p = elem['paragraph']
            style = p.get('paragraphStyle', {}).get('namedStyleType', '')
            if style in ('HEADING_2', 'HEADING_3'):
                text = ''.join(r.get('textRun', {}).get('content', '') for r in p.get('elements', []))
                all_headings.append({
                    'start': elem['startIndex'],
                    'text': text.strip(),
                    'style': style,
                })
    
    # For each chapter, find its end = next H2/H3 heading
    for i, ch in enumerate(chapters_new):
        key = ch['key']
        if key not in KEY_TAKEAWAYS:
            continue
        
        # Find end of this chapter
        ch_end = dank_start
        for h in all_headings:
            if h['start'] > ch['start'] + 10:
                ch_end = h['start']
                break
        
        # Build takeaway text
        items = KEY_TAKEAWAYS[key]
        takeaway_text = "\n📌 Auf einen Blick\n"
        for item in items:
            takeaway_text += f"◆ {item}\n"
        
        # Insert before the next chapter heading
        insert_idx = ch_end
        
        requests = [
            {'insertText': {'location': {'index': insert_idx}, 'text': takeaway_text}},
        ]
        
        # Style: title bold, items normal, all 10pt
        title_start = insert_idx + 1
        title_end = title_start + len("📌 Auf einen Blick")
        
        style_requests = [
            # Title: bold, 11pt
            {
                'updateTextStyle': {
                    'range': {'startIndex': title_start, 'endIndex': title_end},
                    'textStyle': {
                        'bold': True,
                        'fontSize': {'magnitude': 11, 'unit': 'PT'},
                    },
                    'fields': 'bold,fontSize'
                }
            },
            {
                'updateParagraphStyle': {
                    'range': {'startIndex': title_start, 'endIndex': title_end},
                    'paragraphStyle': {
                        'spaceAbove': {'magnitude': 18, 'unit': 'PT'},
                        'spaceBelow': {'magnitude': 6, 'unit': 'PT'},
                        'namedStyleType': 'NORMAL_TEXT',
                    },
                    'fields': 'spaceAbove,spaceBelow,namedStyleType'
                }
            },
        ]
        
        # Style items
        pos = title_end + 1  # after \n
        for item in items:
            item_text = f"◆ {item}"
            item_end = pos + len(item_text)
            style_requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': pos, 'endIndex': item_end},
                    'textStyle': {
                        'fontSize': {'magnitude': 10, 'unit': 'PT'},
                    },
                    'fields': 'fontSize'
                }
            })
            style_requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': pos, 'endIndex': item_end},
                    'paragraphStyle': {
                        'spaceBelow': {'magnitude': 3, 'unit': 'PT'},
                        'namedStyleType': 'NORMAL_TEXT',
                    },
                    'fields': 'spaceBelow,namedStyleType'
                }
            })
            pos = item_end + 1  # after \n
        
        # Must insert in reverse to keep indices valid — but we do one chapter at a time
        # so we need to work backwards through chapters
        # Skip for now — we'll do it after collecting all insertions
    
    # Actually, let's do takeaways one by one, re-reading the doc each time
    # (slower but safer with index shifts)
    for ch in reversed(chapters_new):
        key = ch['key']
        if key not in KEY_TAKEAWAYS:
            continue
        
        # Re-read document to get fresh indices
        doc = get_document(token)
        
        # Find this chapter's end
        dank_start_fresh = 999999
        for elem in doc['body']['content']:
            if 'paragraph' in elem:
                text = ''.join(r.get('textRun', {}).get('content', '') for r in elem['paragraph'].get('elements', []))
                if text.strip() == 'Danksagung':
                    dank_start_fresh = elem['startIndex']
                    break
        
        # Find chapter heading
        ch_start = None
        for elem in doc['body']['content']:
            if 'paragraph' in elem:
                p = elem['paragraph']
                style = p.get('paragraphStyle', {}).get('namedStyleType', '')
                text = ''.join(r.get('textRun', {}).get('content', '') for r in p.get('elements', []))
                text = text.strip()
                if style in ('HEADING_3', 'HEADING_2') and get_chapter_key(text) == key:
                    if elem['startIndex'] < dank_start_fresh:
                        ch_start = elem['startIndex']
                        break
        
        if ch_start is None:
            print(f"  ❌ {key}: Could not find heading")
            continue
        
        # Find end (next H2/H3 after this chapter)
        ch_end = dank_start_fresh
        found_self = False
        for elem in doc['body']['content']:
            if 'paragraph' in elem:
                p = elem['paragraph']
                style = p.get('paragraphStyle', {}).get('namedStyleType', '')
                if style in ('HEADING_2', 'HEADING_3'):
                    if elem['startIndex'] == ch_start:
                        found_self = True
                        continue
                    if found_self and elem['startIndex'] > ch_start:
                        ch_end = elem['startIndex']
                        break
        
        items = KEY_TAKEAWAYS[key]
        takeaway_text = "\n📌 Auf einen Blick\n"
        for item in items:
            takeaway_text += f"◆ {item}\n"
        
        insert_idx = ch_end
        
        requests = [
            {'insertText': {'location': {'index': insert_idx}, 'text': takeaway_text}},
        ]
        
        # Simple style: just make it 10pt and the title bold
        result = batch_update(token, requests)
        if result:
            # Now style it
            title_start = insert_idx + 1
            title_end = title_start + len("📌 Auf einen Blick")
            
            style_reqs = [
                {
                    'updateTextStyle': {
                        'range': {'startIndex': title_start, 'endIndex': title_end},
                        'textStyle': {'bold': True, 'fontSize': {'magnitude': 11, 'unit': 'PT'}},
                        'fields': 'bold,fontSize'
                    }
                },
                {
                    'updateParagraphStyle': {
                        'range': {'startIndex': title_start, 'endIndex': insert_idx + len(takeaway_text) - 1},
                        'paragraphStyle': {'namedStyleType': 'NORMAL_TEXT'},
                        'fields': 'namedStyleType'
                    }
                },
            ]
            
            # Style all items as 10pt
            items_start = title_end + 1
            items_end = insert_idx + len(takeaway_text) - 1
            if items_end > items_start:
                style_reqs.append({
                    'updateTextStyle': {
                        'range': {'startIndex': items_start, 'endIndex': items_end},
                        'textStyle': {'fontSize': {'magnitude': 10, 'unit': 'PT'}},
                        'fields': 'fontSize'
                    }
                })
            
            batch_update(token, style_reqs)
            takeaway_count += 1
            print(f"  ✅ {key}: Key Takeaways inserted")
        else:
            print(f"  ❌ {key}: Failed")
        
        time.sleep(0.3)
    
    print(f"\n  Total takeaways: {takeaway_count}")
    
    # Phase 4: Add CHECKLISTS after Key Takeaways for investment chapters
    print("\n━━━ PHASE 4: CHECKLISTS ━━━")
    
    checklist_count = 0
    for ch_key in reversed(list(CHECKLISTS.keys())):
        doc = get_document(token)
        
        # Find the "📌 Auf einen Blick" text we just inserted for this chapter
        # The checklist goes AFTER the takeaways
        
        # Find chapter end
        dank_start_fresh = 999999
        for elem in doc['body']['content']:
            if 'paragraph' in elem:
                text = ''.join(r.get('textRun', {}).get('content', '') for r in elem['paragraph'].get('elements', []))
                if text.strip() == 'Danksagung':
                    dank_start_fresh = elem['startIndex']
                    break
        
        ch_start = None
        for elem in doc['body']['content']:
            if 'paragraph' in elem:
                p = elem['paragraph']
                style = p.get('paragraphStyle', {}).get('namedStyleType', '')
                text = ''.join(r.get('textRun', {}).get('content', '') for r in p.get('elements', []))
                if style in ('HEADING_3', 'HEADING_2') and get_chapter_key(text.strip()) == ch_key:
                    if elem['startIndex'] < dank_start_fresh:
                        ch_start = elem['startIndex']
                        break
        
        if ch_start is None:
            continue
        
        # Find the next H2/H3 heading after this chapter
        ch_end = dank_start_fresh
        found_self = False
        for elem in doc['body']['content']:
            if 'paragraph' in elem:
                p = elem['paragraph']
                style = p.get('paragraphStyle', {}).get('namedStyleType', '')
                if style in ('HEADING_2', 'HEADING_3'):
                    if elem['startIndex'] == ch_start:
                        found_self = True
                        continue
                    if found_self and elem['startIndex'] > ch_start:
                        ch_end = elem['startIndex']
                        break
        
        items = CHECKLISTS[ch_key]
        checklist_text = "\n✅ Was Sie jetzt tun können\n"
        for item in items:
            checklist_text += f"☐ {item}\n"
        
        insert_idx = ch_end
        
        requests = [
            {'insertText': {'location': {'index': insert_idx}, 'text': checklist_text}},
        ]
        
        result = batch_update(token, requests)
        if result:
            title_start = insert_idx + 1
            title_end = title_start + len("✅ Was Sie jetzt tun können")
            
            style_reqs = [
                {
                    'updateTextStyle': {
                        'range': {'startIndex': title_start, 'endIndex': title_end},
                        'textStyle': {'bold': True, 'fontSize': {'magnitude': 11, 'unit': 'PT'}},
                        'fields': 'bold,fontSize'
                    }
                },
            ]
            
            items_start = title_end + 1
            items_end = insert_idx + len(checklist_text) - 1
            if items_end > items_start:
                style_reqs.append({
                    'updateTextStyle': {
                        'range': {'startIndex': items_start, 'endIndex': items_end},
                        'textStyle': {'fontSize': {'magnitude': 10, 'unit': 'PT'}},
                        'fields': 'fontSize'
                    }
                })
            
            batch_update(token, style_reqs)
            checklist_count += 1
            print(f"  ✅ {ch_key}: Checklist inserted")
        
        time.sleep(0.3)
    
    print(f"\n  Total checklists: {checklist_count}")
    
    print("\n" + "=" * 60)
    print("  ✅ GOOGLE DOC STYLING COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
