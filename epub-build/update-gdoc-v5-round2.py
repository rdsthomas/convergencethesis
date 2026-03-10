#!/usr/bin/env python3
"""
Google Doc v5 Update Round 2:
1. Kinderportfolio tables (Anhang E, Varianten A/B/C)
2. Endnotes: hanging indent (number flush left, text block indented)
"""

import json
import re
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
    url = f'https://docs.googleapis.com/v1/documents/{DOC_ID}:batchUpdate'
    body = json.dumps({'requests': requests}).encode()
    req = urllib.request.Request(url, data=body, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    })
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())


def find_paragraph_by_text(doc, search_text, exact=True):
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


def main():
    print("=" * 60)
    print("  MASCHINENWELT v5 — Google Doc Update Round 2")
    print("=" * 60)

    token = get_access_token()
    doc = get_document(token)
    print(f"  Document loaded: {len(doc['body']['content'])} elements")

    # === 1. ENDNOTES: Hanging indent ===
    print("\n📋 1. Endnotes: Applying hanging indent...")

    # Find the "Endnotes" heading
    endnotes_start = None
    for elem in doc['body']['content']:
        if 'paragraph' not in elem:
            continue
        p = elem['paragraph']
        text = ''.join(run.get('textRun', {}).get('content', '') for run in p.get('elements', []))
        if text.strip() == 'Endnotes':
            endnotes_start = elem.get('endIndex', 0)
            print(f"  Found 'Endnotes' heading, content starts at {endnotes_start}")
            break

    if not endnotes_start:
        print("  ❌ 'Endnotes' heading not found")
        return

    # Find all numbered endnote paragraphs
    endnote_requests = []
    endnote_count = 0
    doc_end = doc['body']['content'][-1].get('endIndex', 0)

    for elem in doc['body']['content']:
        if 'paragraph' not in elem:
            continue
        si = elem.get('startIndex', 0)
        ei = elem.get('endIndex', 0)
        if si < endnotes_start:
            continue

        p = elem['paragraph']
        text = ''.join(run.get('textRun', {}).get('content', '') for run in p.get('elements', []))
        text_clean = text.strip()

        # Match numbered endnotes: "1. ...", "12. ...", "265. ..." etc.
        if re.match(r'^\d+\.\s', text_clean):
            # Apply hanging indent: indentStart=36pt, indentFirstLine=0pt
            # This gives a hanging effect: first line (with number) flush to indentStart,
            # but with negative first-line offset to pull the number back
            endnote_requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': si, 'endIndex': ei},
                    'paragraphStyle': {
                        'indentStart': {'magnitude': 28, 'unit': 'PT'},
                        'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                    },
                    'fields': 'indentStart,indentFirstLine',
                }
            })
            endnote_count += 1

    print(f"  Found {endnote_count} endnote entries")

    if endnote_requests:
        # Send in batches of 100 to avoid API limits
        for batch_start in range(0, len(endnote_requests), 100):
            batch = endnote_requests[batch_start:batch_start + 100]
            try:
                batch_update(token, batch)
                print(f"  ✅ Applied batch {batch_start//100 + 1} ({len(batch)} requests)")
            except urllib.error.HTTPError as e:
                error_body = e.read().decode()
                print(f"  ❌ Error: {e.code}: {error_body[:500]}")

    # === 2. KINDERPORTFOLIO TABLES ===
    print("\n📋 2. Kinderportfolio tables (Anhang E)...")

    # Refresh doc after endnotes changes
    token = get_access_token()
    doc = get_document(token)

    # Find the Variante lines in Anhang E
    kinder_variantes = []
    for elem in doc['body']['content']:
        if 'paragraph' not in elem:
            continue
        p = elem['paragraph']
        text = ''.join(run.get('textRun', {}).get('content', '') for run in p.get('elements', []))
        text_clean = text.strip()

        if text_clean.startswith('Variante A') and 'einfache Weg' in text_clean:
            kinder_variantes.append(('A', elem.get('startIndex', 0), elem.get('endIndex', 0), text_clean))
        elif text_clean.startswith('Variante B') and 'KI-Tilt' in text_clean:
            kinder_variantes.append(('B', elem.get('startIndex', 0), elem.get('endIndex', 0), text_clean))
        elif text_clean.startswith('Variante C') and 'aggressive Kinderbarbell' in text_clean:
            kinder_variantes.append(('C', elem.get('startIndex', 0), elem.get('endIndex', 0), text_clean))

    print(f"  Found {len(kinder_variantes)} Kinderportfolio variantes")
    for v in kinder_variantes:
        print(f"    Variante {v[0]}: [{v[1]}-{v[2]}] {v[3][:60]}...")

    # Table data for Kinderportfolio
    kinder_tables = {
        'A': {
            'rows': [
                ['Asset', 'Produkt / ISIN', 'Anteil', 'Betrag'],
                ['MSCI World ETF', 'IE00B4L5Y983 (TER 0,20 %)', '100 %', '200 €'],
            ],
            'footer': 'Erwartung bei 8 % p.a., 18 J.: ca. 96.000 € (eingezahlt: 43.200 €)',
            'section_rows': [],
            'header_row': 0,
            'total_row': None,
        },
        'B': {
            'rows': [
                ['Asset', 'Produkt / ISIN', 'Anteil', 'Betrag'],
                ['MSCI World ETF', 'IE00B4L5Y983', '60 %', '120 €'],
                ['Nasdaq-100 ETF', 'IE00BFZXGZ54', '25 %', '50 €'],
                ['Robotik-ETF', 'IE00BYZK4552', '15 %', '30 €'],
                ['Gesamt', '', '100 %', '200 €'],
            ],
            'footer': 'Erwartung bei 10 % p.a., 18 J.: ca. 120.000 €',
            'section_rows': [],
            'header_row': 0,
            'total_row': 4,
        },
        'C': {
            'rows': [
                ['Asset', 'Produkt / ISIN', 'Anteil', 'Betrag'],
                ['MSCI World ETF', 'IE00B4L5Y983', '50 %', '100 €'],
                ['Nasdaq-100 ETF', 'IE00BFZXGZ54', '20 %', '40 €'],
                ['Robotik-ETF', 'IE00BYZK4552', '10 %', '20 €'],
                ['Bitcoin*', 'Im eigenen Depot', '15 %', '30 €'],
                ['Ethereum*', 'Im eigenen Depot', '5 %', '10 €'],
                ['Gesamt', '', '100 %', '200 €'],
            ],
            'footer': '* Krypto nicht im Junior-Depot — Kauf im eigenen Namen, Übertrag zum 18. Geb.\nKonservativ: ca. 141.000 € · Optimistisch: bis zu 195.000 €',
            'section_rows': [],
            'header_row': 0,
            'total_row': 6,
        },
    }

    # Insert tables BEFORE each Variante paragraph (in reverse order to preserve indices)
    kinder_variantes.sort(key=lambda v: v[1], reverse=True)

    for var_key, v_start, v_end, v_text in kinder_variantes:
        tdata = kinder_tables[var_key]
        rows = tdata['rows']
        n_rows = len(rows)
        n_cols = 4

        print(f"\n  Inserting table for Kinder-Variante {var_key}...")

        # Insert newline + table BEFORE the Variante paragraph
        table_requests = [
            {
                'insertText': {
                    'location': {'index': v_start},
                    'text': '\n',
                }
            },
            {
                'insertTable': {
                    'rows': n_rows,
                    'columns': n_cols,
                    'location': {'index': v_start + 1},
                }
            }
        ]

        try:
            batch_update(token, table_requests)
            print(f"    ✅ Table {var_key} structure created")
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            print(f"    ❌ Error: {e.code}: {error_body[:300]}")
            continue

        # Refresh doc to get table cell indices
        doc = get_document(token)

        # Find the table near v_start
        table_elem = None
        for elem in doc['body']['content']:
            if 'table' in elem:
                si = elem.get('startIndex', 0)
                if abs(si - v_start) < 30:
                    table_elem = elem
                    break

        if not table_elem:
            print(f"    ⚠️ Could not find inserted table")
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
                cell_para = cell['content'][0]
                cell_start = cell_para.get('startIndex', 0)
                cell_requests.append({
                    'insertText': {
                        'location': {'index': cell_start},
                        'text': cell_text,
                    }
                })

        cell_requests.sort(key=lambda r: r['insertText']['location']['index'], reverse=True)

        if cell_requests:
            try:
                batch_update(token, cell_requests)
                print(f"    ✅ Table {var_key} cells filled")
            except urllib.error.HTTPError as e:
                error_body = e.read().decode()
                print(f"    ❌ Cell fill error: {e.code}: {error_body[:300]}")
                continue

        # Style the table
        doc = get_document(token)

        # Find the table again
        table_elem = None
        for elem in doc['body']['content']:
            if 'table' in elem:
                si = elem.get('startIndex', 0)
                if abs(si - v_start) < 200:
                    table_elem = elem
                    break

        if not table_elem:
            continue

        style_requests = []
        table = table_elem['table']
        table_start_idx = table_elem.get('startIndex', 0)

        # Header row: dark blue background, white bold text
        header_row = table['tableRows'][0]
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

        # Header text styling
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

        # Total row if exists
        if tdata['total_row'] is not None:
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
        for row_idx in range(1, n_rows):
            if tdata['total_row'] is not None and row_idx == tdata['total_row']:
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
    print("  ✅ DONE — Google Doc v5 Round 2 complete")
    print("=" * 60)


if __name__ == '__main__':
    main()
