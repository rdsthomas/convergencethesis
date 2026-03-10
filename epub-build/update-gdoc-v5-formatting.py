#!/usr/bin/env python3
"""
Update Google Doc v5 formatting:
1. Anhänge A-E als HEADING_1 (gleiche Ebene wie Kapitel)
2. Glossar: Begriffe fett (Term vor dem Doppelpunkt)
3. Literaturverzeichnis: Einrückungen entfernen
4. "Wichtiger Hinweis" als hervorgehobene Box
5. Portfolio-Tabellen für Kap. 14 Varianten A, B, C
"""

import json
import urllib.request
import urllib.parse

DOC_ID = '1JF7Kei019q0iunIISa-fCq7Y4aLcHWHmkjBOb7MBlms'


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
    """Send batchUpdate to Google Docs API."""
    url = f'https://docs.googleapis.com/v1/documents/{DOC_ID}:batchUpdate'
    body = json.dumps({'requests': requests}).encode()
    req = urllib.request.Request(url, data=body, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    })
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())


def find_paragraph_by_text(doc, search_text, exact=True):
    """Find a paragraph element by its text content. Returns (startIndex, endIndex, element)."""
    results = []
    for elem in doc['body']['content']:
        if 'paragraph' not in elem:
            continue
        p = elem['paragraph']
        text = ''.join(run.get('textRun', {}).get('content', '') for run in p.get('elements', []))
        text_clean = text.strip()
        if exact and text_clean == search_text:
            results.append((elem.get('startIndex', 0), elem.get('endIndex', 0), elem))
        elif not exact and search_text in text_clean:
            results.append((elem.get('startIndex', 0), elem.get('endIndex', 0), elem))
    return results


def find_glossary_entries(doc, start_idx, end_idx):
    """Find all glossary entries (Term: Explanation) between start and end indices."""
    entries = []
    for elem in doc['body']['content']:
        if 'paragraph' not in elem:
            continue
        si = elem.get('startIndex', 0)
        ei = elem.get('endIndex', 0)
        if si < start_idx or si >= end_idx:
            continue
        p = elem['paragraph']
        text = ''.join(run.get('textRun', {}).get('content', '') for run in p.get('elements', []))
        text_clean = text.strip()
        # Skip empty, heading-like, or intro paragraph
        if not text_clean or text_clean.startswith('Die wichtigsten Begriffe'):
            continue
        # Match "Term (optional): Explanation"
        colon_pos = text_clean.find(': ')
        if colon_pos > 0 and colon_pos < 80:
            term = text_clean[:colon_pos]
            # Verify it looks like a glossary term (starts with uppercase)
            if term[0].isupper():
                # Find the actual position of the term in the document
                for run in p.get('elements', []):
                    content = run.get('textRun', {}).get('content', '')
                    run_start = run.get('startIndex', 0)
                    # Find term start in this run
                    term_in_content = content.find(term)
                    if term_in_content >= 0:
                        abs_start = run_start + term_in_content
                        abs_end = abs_start + len(term)
                        # Check if already bold
                        is_bold = run.get('textRun', {}).get('textStyle', {}).get('bold', False)
                        entries.append({
                            'term': term,
                            'start': abs_start,
                            'end': abs_end,
                            'already_bold': is_bold,
                        })
                        break
    return entries


def find_literatur_entries(doc, start_idx, end_idx):
    """Find all literature entries that have indentation."""
    entries = []
    for elem in doc['body']['content']:
        if 'paragraph' not in elem:
            continue
        si = elem.get('startIndex', 0)
        if si < start_idx or si >= end_idx:
            continue
        p = elem['paragraph']
        ps = p.get('paragraphStyle', {})
        indent = ps.get('indentFirstLine', {}).get('magnitude', 0)
        indent_start = ps.get('indentStart', {}).get('magnitude', 0)
        if indent > 0 or indent_start > 0:
            entries.append((si, elem.get('endIndex', 0)))
    return entries


def main():
    print("=" * 60)
    print("  MASCHINENWELT v5 — Google Doc Formatting Update")
    print("=" * 60)

    token = get_access_token()
    doc = get_document(token)
    print(f"  Document loaded: {len(doc['body']['content'])} elements")

    requests = []

    # === 1. ANHÄNGE A-E ALS HEADING_1 ===
    print("\n📋 1. Setting Anhänge A-E as HEADING_1...")
    anhang_texts = [
        'Anhang A — Glossar',
        'Anhang B — Umsetzung für deutsche Anleger',
        'Anhang C — Tokenomics-Vergleich',
        'Anhang D — Literaturverzeichnis',
        'Anhang E — Das Kinderportfolio: Für Mila und Malou',
    ]

    anhang_positions = {}
    for text in anhang_texts:
        results = find_paragraph_by_text(doc, text)
        if results:
            start, end, elem = results[0]
            print(f"  Found: [{start}-{end}] {text}")
            anhang_positions[text] = (start, end)
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {'namedStyleType': 'HEADING_1'},
                    'fields': 'namedStyleType',
                }
            })
        else:
            print(f"  NOT FOUND: {text}")

    # === 2. GLOSSAR: Begriffe fett ===
    print("\n📋 2. Glossar: Making terms bold...")
    anhang_a_start = anhang_positions.get('Anhang A — Glossar', (0, 0))[1]
    anhang_b_start = anhang_positions.get('Anhang B — Umsetzung für deutsche Anleger', (0, 0))[0]

    if anhang_a_start and anhang_b_start:
        glossary_entries = find_glossary_entries(doc, anhang_a_start, anhang_b_start)
        bold_count = 0
        for entry in glossary_entries:
            if not entry['already_bold']:
                requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': entry['start'], 'endIndex': entry['end']},
                        'textStyle': {'bold': True},
                        'fields': 'bold',
                    }
                })
                bold_count += 1
        print(f"  {len(glossary_entries)} entries found, {bold_count} to bold")
    else:
        print("  Could not determine glossar range")

    # === 3. LITERATURVERZEICHNIS: Einrückungen entfernen ===
    print("\n📋 3. Literaturverzeichnis: Removing indentation...")
    anhang_d_start = anhang_positions.get('Anhang D — Literaturverzeichnis', (0, 0))[1]
    anhang_e_start = anhang_positions.get('Anhang E — Das Kinderportfolio: Für Mila und Malou', (0, 0))[0]

    if anhang_d_start and anhang_e_start:
        # Remove all indentation in the entire Literaturverzeichnis section
        requests.append({
            'updateParagraphStyle': {
                'range': {'startIndex': anhang_d_start, 'endIndex': anhang_e_start},
                'paragraphStyle': {
                    'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                    'indentStart': {'magnitude': 0, 'unit': 'PT'},
                },
                'fields': 'indentFirstLine,indentStart',
            }
        })
        print(f"  Removing indent for range [{anhang_d_start}-{anhang_e_start}]")
    else:
        print("  Could not determine literaturverzeichnis range")

    # === 4. "WICHTIGER HINWEIS" ALS BOX ===
    print("\n📋 4. 'Wichtiger Hinweis' as highlighted box...")
    hinweis_results = find_paragraph_by_text(doc, 'Wichtiger Hinweis')
    if hinweis_results:
        h_start, h_end, h_elem = hinweis_results[0]
        print(f"  Found title at [{h_start}-{h_end}]")

        # Find the paragraph after it (the hint text)
        hint_text_start = h_end
        hint_text_end = h_end
        for elem in doc['body']['content']:
            if 'paragraph' not in elem:
                continue
            si = elem.get('startIndex', 0)
            if si == h_end or (si > h_end and si < h_end + 5):
                ei = elem.get('endIndex', 0)
                text = ''.join(run.get('textRun', {}).get('content', '')
                               for run in elem['paragraph'].get('elements', []))
                if text.strip().startswith('Dieses Buch ist keine Anlageberatung'):
                    hint_text_end = ei
                    break

        # Style the title "Wichtiger Hinweis" — bold, colored
        requests.append({
            'updateTextStyle': {
                'range': {'startIndex': h_start, 'endIndex': h_end - 1},
                'textStyle': {
                    'bold': True,
                    'fontSize': {'magnitude': 12, 'unit': 'PT'},
                    'foregroundColor': {
                        'color': {'rgbColor': {'red': 0.8, 'green': 0.33, 'blue': 0.0}}
                    },
                },
                'fields': 'bold,fontSize,foregroundColor',
            }
        })

        # Add ⚠️ prefix to "Wichtiger Hinweis"
        requests.append({
            'insertText': {
                'location': {'index': h_start},
                'text': '⚠️ ',
            }
        })

        # Add background shading + border for both paragraphs
        # Note: insertText shifts indices by 3 (length of "⚠️ ")
        adjusted_start = h_start
        adjusted_end = hint_text_end + 3  # +3 for the inserted emoji prefix

        requests.append({
            'updateParagraphStyle': {
                'range': {'startIndex': adjusted_start, 'endIndex': adjusted_end},
                'paragraphStyle': {
                    'shading': {
                        'backgroundColor': {
                            'color': {'rgbColor': {'red': 1.0, 'green': 0.97, 'blue': 0.88}}
                        }
                    },
                    'borderLeft': {
                        'color': {'color': {'rgbColor': {'red': 1.0, 'green': 0.56, 'blue': 0.0}}},
                        'width': {'magnitude': 3, 'unit': 'PT'},
                        'padding': {'magnitude': 6, 'unit': 'PT'},
                        'dashStyle': 'SOLID',
                    },
                    'indentStart': {'magnitude': 18, 'unit': 'PT'},
                    'indentEnd': {'magnitude': 18, 'unit': 'PT'},
                },
                'fields': 'shading.backgroundColor,borderLeft,indentStart,indentEnd',
            }
        })

        print(f"  Styled hint box [{h_start}-{adjusted_end}]")
    else:
        print("  'Wichtiger Hinweis' not found")

    # === 5. PORTFOLIO-TABELLEN FÜR KAPITEL 14 ===
    print("\n📋 5. Portfolio tables for Kap. 14...")
    # Google Docs table insertion is complex — we insert tables after each Variante heading
    variante_headings = [
        ('Variante A: Der Konservative (Kapital 100K–500K€)', 'A'),
        ('Variante B: Der Ausgewogene (Kapital 500K–2M€)', 'B'),
        ('Variante C: Der Aggressive (Kapital 2M€+, hohe Risikotoleranz)', 'C'),
    ]

    # Define table data for each variante
    table_data = {
        'A': {
            'rows': [
                ['Seite', 'Allokation', 'Anteil'],
                ['SICHERE SEITE (70 %)', '', ''],
                ['Aktien', 'Globaler ETF (MSCI World), Tech-Übergewichtung', '30 %'],
                ['Big Tech', 'NVIDIA, Microsoft, Apple, Alphabet', '15 %'],
                ['Energie', 'Cameco, Constellation Energy, NextEra', '10 %'],
                ['Robotik', 'Intuitive Surgical, ABB, Fanuc', '10 %'],
                ['Cash', 'Tagesgeld / Geldmarkt', '5 %'],
                ['ASYMMETRISCHE SEITE (30 %)', '', ''],
                ['Bitcoin', 'DCA über 6–12 Monate', '15 %'],
                ['Ethereum', 'Layer-2-Ökosystem, Agent-TAM', '5 %'],
                ['RWA', 'BUIDL, Ondo Finance (Tokenisierte Treasuries)', '5 %'],
                ['Infrastruktur', 'Coinbase, OLAS, PEAQ, Agent-Payment-Rails', '5 %'],
                ['Gesamt', '', '100 %'],
            ],
            'section_rows': [1, 7],  # 0-indexed rows that are section headers
            'header_row': 0,
            'total_row': 12,
        },
        'B': {
            'rows': [
                ['Seite', 'Allokation', 'Anteil'],
                ['SICHERE SEITE (60 %)', '', ''],
                ['Aktien', 'Globaler ETF mit KI-Tilt', '20 %'],
                ['Big Tech', 'NVIDIA, Microsoft, Apple, Alphabet, Amazon, Meta', '15 %'],
                ['Robotik', 'Tesla, Intuitive Surgical, ABB, Figure AI', '10 %'],
                ['Energie', 'Cameco, Constellation, NuScale, Oklo, Uran-ETF', '10 %'],
                ['Cash', 'Cash-Reserve', '5 %'],
                ['ASYMMETRISCHE SEITE (40 %)', '', ''],
                ['Bitcoin', 'DCA über 12 Monate', '15 %'],
                ['Ethereum', 'Staking, Layer-2-Exposure', '8 %'],
                ['DeFi', 'Circle (IPO), Aave, Uniswap', '7 %'],
                ['RWA', 'Maple, Centrifuge, Hamilton Lane tokenisiert', '5 %'],
                ['Machine Economy', 'Olas, peaq, Fetch.ai/ASI, Render Network', '5 %'],
                ['Gesamt', '', '100 %'],
            ],
            'section_rows': [1, 7],
            'header_row': 0,
            'total_row': 13,
        },
        'C': {
            'rows': [
                ['Seite', 'Allokation', 'Anteil'],
                ['SICHERE SEITE (50 %)', '', ''],
                ['Big Tech', 'NVIDIA, Microsoft, Apple', '15 %'],
                ['Energie', 'Nuklear & Energie breit diversifiziert', '15 %'],
                ['Robotik', 'Tesla, Intuitive Surgical + Venture-Positionen', '10 %'],
                ['Cash / Treasuries', 'Tokenisierte Treasuries, yield-generierend', '10 %'],
                ['ASYMMETRISCHE SEITE (50 %)', '', ''],
                ['Bitcoin', 'Kernposition', '20 %'],
                ['Ethereum', 'Smart-Contract-Plattform', '10 %'],
                ['KI-Token / DeFi', 'Render, Filecoin, Olas, ASI Alliance, Aave', '8 %'],
                ['RWA', 'Private Equity, Immobilien, Private Credit', '7 %'],
                ['Venture / Angel', 'peaq-Ökosystem, Robotik-DAOs, BCI-nahe Firmen', '5 %'],
                ['Gesamt', '', '100 %'],
            ],
            'section_rows': [1, 6],
            'header_row': 0,
            'total_row': 12,
        },
    }

    # We need to find insert positions for the tables
    # Tables should be inserted AFTER the Variante heading paragraph and BEFORE the first content paragraph
    # We'll track the positions and insert tables in REVERSE order (highest index first)
    table_inserts = []
    for heading_text, var_key in variante_headings:
        results = find_paragraph_by_text(doc, heading_text)
        if results:
            start, end, elem = results[0]
            print(f"  Found {var_key}: [{start}-{end}]")
            table_inserts.append((end, var_key, table_data[var_key]))
        else:
            print(f"  NOT FOUND: {heading_text}")

    # Sort by position descending to insert from bottom up
    table_inserts.sort(key=lambda x: x[0], reverse=True)

    print(f"\n  Tables will be inserted at positions (reverse order):")
    for pos, key, _ in table_inserts:
        print(f"    Variante {key}: after index {pos}")

    # === SEND BATCH UPDATE (non-table requests first) ===
    if requests:
        print(f"\n🔧 Sending {len(requests)} formatting requests...")
        try:
            result = batch_update(token, requests)
            print("  ✅ Formatting requests applied")
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            print(f"  ❌ Error: {e.code}")
            print(f"  {error_body[:500]}")
            return

    # === INSERT TABLES (separate batch, needs fresh doc to get correct positions) ===
    if table_inserts:
        print(f"\n📊 Inserting {len(table_inserts)} portfolio tables...")
        # Refresh token and doc after the first batch update shifted indices
        token = get_access_token()
        doc = get_document(token)

        for heading_text, var_key in variante_headings:
            results = find_paragraph_by_text(doc, heading_text)
            if results:
                old_pos = [t for t in table_inserts if t[1] == var_key]
                if old_pos:
                    new_start, new_end, _ = results[0]
                    # Update the position
                    for idx, t in enumerate(table_inserts):
                        if t[1] == var_key:
                            table_inserts[idx] = (new_end, t[1], t[2])

        # Re-sort descending
        table_inserts.sort(key=lambda x: x[0], reverse=True)

        for insert_pos, var_key, tdata in table_inserts:
            rows = tdata['rows']
            n_rows = len(rows)
            n_cols = 3

            table_requests = []

            # First insert a newline where the table will go
            table_requests.append({
                'insertText': {
                    'location': {'index': insert_pos},
                    'text': '\n',
                }
            })

            # Insert the table after the newline
            table_requests.append({
                'insertTable': {
                    'rows': n_rows,
                    'columns': n_cols,
                    'location': {'index': insert_pos + 1},
                }
            })

            print(f"  Inserting table for Variante {var_key} at index {insert_pos}...")
            try:
                result = batch_update(token, table_requests)
                print(f"    ✅ Table {var_key} structure created")
            except urllib.error.HTTPError as e:
                error_body = e.read().decode()
                print(f"    ❌ Error: {e.code}: {error_body[:300]}")
                continue

            # Now we need to fill the table cells with content
            # Re-fetch the doc to get the table's exact cell indices
            doc = get_document(token)

            # Find the table we just inserted — it should be near insert_pos
            table_elem = None
            for elem in doc['body']['content']:
                if 'table' in elem:
                    si = elem.get('startIndex', 0)
                    # The table should be right after our insert position
                    if abs(si - insert_pos) < 20:
                        table_elem = elem
                        break

            if not table_elem:
                # Try to find any table near the Variante heading
                for i, elem in enumerate(doc['body']['content']):
                    if 'paragraph' in elem:
                        text = ''.join(run.get('textRun', {}).get('content', '')
                                       for run in elem['paragraph'].get('elements', []))
                        if heading_text := [h for h, k in variante_headings if k == var_key]:
                            if text.strip() == heading_text[0]:
                                # Look for table in next few elements
                                for j in range(i+1, min(i+5, len(doc['body']['content']))):
                                    if 'table' in doc['body']['content'][j]:
                                        table_elem = doc['body']['content'][j]
                                        break
                                break

            if not table_elem:
                print(f"    ⚠️ Could not find inserted table for Variante {var_key}")
                continue

            # Fill cells
            cell_requests = []
            table = table_elem['table']
            for row_idx, row_data in enumerate(rows):
                table_row = table['tableRows'][row_idx]
                for col_idx, cell_text in enumerate(row_data):
                    if not cell_text:
                        continue
                    cell = table_row['tableCells'][col_idx]
                    # Get the first paragraph in the cell
                    cell_para = cell['content'][0]
                    cell_start = cell_para.get('startIndex', 0)
                    cell_end = cell_para.get('endIndex', 0)

                    # Insert text into the cell
                    cell_requests.append({
                        'insertText': {
                            'location': {'index': cell_start},
                            'text': cell_text,
                        }
                    })

            # Apply cell text in reverse order (highest index first)
            cell_requests.sort(key=lambda r: r['insertText']['location']['index'], reverse=True)

            if cell_requests:
                try:
                    batch_update(token, cell_requests)
                    print(f"    ✅ Table {var_key} cells filled")
                except urllib.error.HTTPError as e:
                    error_body = e.read().decode()
                    print(f"    ❌ Cell fill error: {e.code}: {error_body[:300]}")
                    continue

            # Now style the table — header row, section rows, total row
            doc = get_document(token)  # Refresh after fills

            # Find the table again
            table_elem = None
            for elem in doc['body']['content']:
                if 'table' in elem:
                    si = elem.get('startIndex', 0)
                    if abs(si - insert_pos) < 200:
                        table_elem = elem
                        break
            if not table_elem:
                for i, elem in enumerate(doc['body']['content']):
                    if 'paragraph' in elem:
                        text = ''.join(run.get('textRun', {}).get('content', '')
                                       for run in elem['paragraph'].get('elements', []))
                        for h, k in variante_headings:
                            if k == var_key and text.strip() == h:
                                for j in range(i+1, min(i+5, len(doc['body']['content']))):
                                    if 'table' in doc['body']['content'][j]:
                                        table_elem = doc['body']['content'][j]
                                        break
                                break

            if not table_elem:
                continue

            style_requests = []
            table = table_elem['table']

            # Style header row (row 0): bold white text, dark blue background
            header_row = table['tableRows'][0]
            for cell in header_row['tableCells']:
                cell_start = cell['content'][0].get('startIndex', 0)
                cell_end = cell['content'][0].get('endIndex', 0)
                style_requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': cell_start, 'endIndex': cell_end},
                        'textStyle': {
                            'bold': True,
                            'foregroundColor': {
                                'color': {'rgbColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0}}
                            },
                        },
                        'fields': 'bold,foregroundColor',
                    }
                })
                style_requests.append({
                    'updateTableCellStyle': {
                        'tableCellStyle': {
                            'backgroundColor': {
                                'color': {'rgbColor': {'red': 0.1, 'green': 0.23, 'blue': 0.36}}
                            },
                        },
                        'tableRange': {
                            'tableCellLocation': {
                                'tableStartLocation': {'index': table_elem.get('startIndex', 0)},
                                'rowIndex': 0,
                                'columnIndex': cell['content'][0]['paragraph']['elements'][0].get('startIndex', cell_start) - cell_start if False else [c for c in range(3) if header_row['tableCells'][c] is cell][0] if any(header_row['tableCells'][c] is cell for c in range(3)) else 0,
                            },
                            'rowSpan': 1,
                            'columnSpan': 1,
                        },
                        'fields': 'backgroundColor',
                    }
                })

            # Actually, the updateTableCellStyle approach is complex. Let me use a simpler approach:
            # Style all header cells via a single updateTableCellStyle spanning the row
            table_start_idx = table_elem.get('startIndex', 0)

            # Clear previous style_requests and use simpler approach
            style_requests = []

            # Header row background
            for col_idx in range(n_cols):
                style_requests.append({
                    'updateTableCellStyle': {
                        'tableCellStyle': {
                            'backgroundColor': {
                                'color': {'rgbColor': {'red': 0.1, 'green': 0.23, 'blue': 0.36}}
                            },
                        },
                        'tableRange': {
                            'tableCellLocation': {
                                'tableStartLocation': {'index': table_start_idx},
                                'rowIndex': 0,
                                'columnIndex': col_idx,
                            },
                            'rowSpan': 1,
                            'columnSpan': 1,
                        },
                        'fields': 'backgroundColor',
                    }
                })

            # Header row text: bold + white
            for cell in header_row['tableCells']:
                for content in cell['content']:
                    if 'paragraph' in content:
                        for elem2 in content['paragraph'].get('elements', []):
                            s = elem2.get('startIndex', 0)
                            e = elem2.get('endIndex', 0)
                            if s < e:
                                style_requests.append({
                                    'updateTextStyle': {
                                        'range': {'startIndex': s, 'endIndex': e},
                                        'textStyle': {
                                            'bold': True,
                                            'foregroundColor': {
                                                'color': {'rgbColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0}}
                                            },
                                        },
                                        'fields': 'bold,foregroundColor',
                                    }
                                })

            # Section header rows: bold, light blue background
            for sec_row_idx in tdata['section_rows']:
                for col_idx in range(n_cols):
                    style_requests.append({
                        'updateTableCellStyle': {
                            'tableCellStyle': {
                                'backgroundColor': {
                                    'color': {'rgbColor': {'red': 0.91, 'green': 0.94, 'blue': 0.99}}
                                },
                            },
                            'tableRange': {
                                'tableCellLocation': {
                                    'tableStartLocation': {'index': table_start_idx},
                                    'rowIndex': sec_row_idx,
                                    'columnIndex': col_idx,
                                },
                                'rowSpan': 1,
                                'columnSpan': 1,
                            },
                            'fields': 'backgroundColor',
                        }
                    })
                # Bold text in section header row
                sec_row = table['tableRows'][sec_row_idx]
                for cell in sec_row['tableCells']:
                    for content in cell['content']:
                        if 'paragraph' in content:
                            for elem2 in content['paragraph'].get('elements', []):
                                s = elem2.get('startIndex', 0)
                                e = elem2.get('endIndex', 0)
                                if s < e:
                                    style_requests.append({
                                        'updateTextStyle': {
                                            'range': {'startIndex': s, 'endIndex': e},
                                            'textStyle': {'bold': True,
                                                          'foregroundColor': {
                                                              'color': {'rgbColor': {'red': 0.1, 'green': 0.23, 'blue': 0.36}}
                                                          }},
                                            'fields': 'bold,foregroundColor',
                                        }
                                    })

            # Total row: bold, light gray background
            total_row_idx = tdata['total_row']
            for col_idx in range(n_cols):
                style_requests.append({
                    'updateTableCellStyle': {
                        'tableCellStyle': {
                            'backgroundColor': {
                                'color': {'rgbColor': {'red': 0.94, 'green': 0.96, 'blue': 0.97}}
                            },
                        },
                        'tableRange': {
                            'tableCellLocation': {
                                'tableStartLocation': {'index': table_start_idx},
                                'rowIndex': total_row_idx,
                                'columnIndex': col_idx,
                            },
                            'rowSpan': 1,
                            'columnSpan': 1,
                        },
                        'fields': 'backgroundColor',
                    }
                })
            total_row = table['tableRows'][total_row_idx]
            for cell in total_row['tableCells']:
                for content in cell['content']:
                    if 'paragraph' in content:
                        for elem2 in content['paragraph'].get('elements', []):
                            s = elem2.get('startIndex', 0)
                            e = elem2.get('endIndex', 0)
                            if s < e:
                                style_requests.append({
                                    'updateTextStyle': {
                                        'range': {'startIndex': s, 'endIndex': e},
                                        'textStyle': {'bold': True},
                                        'fields': 'bold',
                                    }
                                })

            # Even row striping
            for row_idx in range(2, n_rows):
                if row_idx in tdata['section_rows'] or row_idx == tdata['total_row']:
                    continue
                if row_idx % 2 == 0:
                    for col_idx in range(n_cols):
                        style_requests.append({
                            'updateTableCellStyle': {
                                'tableCellStyle': {
                                    'backgroundColor': {
                                        'color': {'rgbColor': {'red': 0.96, 'green': 0.97, 'blue': 0.99}}
                                    },
                                },
                                'tableRange': {
                                    'tableCellLocation': {
                                        'tableStartLocation': {'index': table_start_idx},
                                        'rowIndex': row_idx,
                                        'columnIndex': col_idx,
                                    },
                                    'rowSpan': 1,
                                    'columnSpan': 1,
                                },
                                'fields': 'backgroundColor',
                            }
                        })

            if style_requests:
                try:
                    batch_update(token, style_requests)
                    print(f"    ✅ Table {var_key} styled")
                except urllib.error.HTTPError as e:
                    error_body = e.read().decode()
                    print(f"    ❌ Style error: {e.code}: {error_body[:300]}")

    print("\n" + "=" * 60)
    print("  ✅ DONE — Google Doc v5 updated")
    print("=" * 60)


if __name__ == '__main__':
    main()
