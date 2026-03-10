#!/usr/bin/env python3
"""
Google Doc v5 Update Round 3:
1. Fix Endnotes — proper hanging indent (indentFirstLine < indentStart)
2. Abbildungsverzeichnis — remove indentation
3. Stichwortverzeichnis — remove indentation + bold keywords
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


def main():
    print("=" * 60)
    print("  MASCHINENWELT v5 — Google Doc Update Round 3")
    print("=" * 60)

    token = get_access_token()
    doc = get_document(token)
    print(f"  Document loaded: {len(doc['body']['content'])} elements")

    requests = []

    # === Find key section positions ===
    sections = {}
    for elem in doc['body']['content']:
        if 'paragraph' not in elem:
            continue
        p = elem['paragraph']
        text = ''.join(run.get('textRun', {}).get('content', '') for run in p.get('elements', []))
        tc = text.strip()
        si = elem.get('startIndex', 0)
        ei = elem.get('endIndex', 0)

        if tc == 'Endnotes':
            sections['endnotes'] = (si, ei)
        elif tc == 'Abbildungsverzeichnis':
            sections['abbildungen'] = (si, ei)
        elif tc == 'Stichwortverzeichnis':
            sections['stichwort'] = (si, ei)

    for name, (s, e) in sections.items():
        print(f"  {name}: [{s}-{e}]")

    # === 1. FIX ENDNOTES — proper hanging indent ===
    print("\n📋 1. Fixing Endnotes hanging indent...")

    endnotes_start = sections.get('endnotes', (0, 0))[1]
    abbildungen_start = sections.get('abbildungen', (0, 0))[0]

    if endnotes_start and abbildungen_start:
        # Find all numbered endnote paragraphs and apply PROPER hanging indent
        # In Google Docs, hanging indent = indentStart > indentFirstLine
        # indentFirstLine controls where the FIRST line starts
        # indentStart controls where SUBSEQUENT lines start
        # For hanging: indentFirstLine=0, indentStart=28pt → number at 0, text at 28pt
        endnote_count = 0
        for elem in doc['body']['content']:
            if 'paragraph' not in elem:
                continue
            si = elem.get('startIndex', 0)
            ei = elem.get('endIndex', 0)
            if si < endnotes_start or si >= abbildungen_start:
                continue

            p = elem['paragraph']
            text = ''.join(run.get('textRun', {}).get('content', '') for run in p.get('elements', []))
            tc = text.strip()

            if re.match(r'^\d+\.\s', tc):
                requests.append({
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

        print(f"  {endnote_count} endnotes with hanging indent")
    else:
        print("  ❌ Could not find Endnotes/Abbildungsverzeichnis boundaries")

    # === 2. ABBILDUNGSVERZEICHNIS — remove indentation ===
    print("\n📋 2. Abbildungsverzeichnis: removing indentation...")

    abbildungen_end = sections.get('abbildungen', (0, 0))[1]
    stichwort_start = sections.get('stichwort', (0, 0))[0]

    if abbildungen_end and stichwort_start:
        requests.append({
            'updateParagraphStyle': {
                'range': {'startIndex': abbildungen_end, 'endIndex': stichwort_start},
                'paragraphStyle': {
                    'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                    'indentStart': {'magnitude': 0, 'unit': 'PT'},
                },
                'fields': 'indentFirstLine,indentStart',
            }
        })
        print(f"  Range: [{abbildungen_end}-{stichwort_start}]")
    else:
        print("  ❌ Could not determine range")

    # === 3. STICHWORTVERZEICHNIS — remove indentation + bold keywords ===
    print("\n📋 3. Stichwortverzeichnis: removing indentation + bold keywords...")

    stichwort_end = sections.get('stichwort', (0, 0))[1]
    doc_end = doc['body']['content'][-1].get('endIndex', 0)

    if stichwort_end:
        # Remove indentation for entire section
        requests.append({
            'updateParagraphStyle': {
                'range': {'startIndex': stichwort_end, 'endIndex': doc_end},
                'paragraphStyle': {
                    'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                    'indentStart': {'magnitude': 0, 'unit': 'PT'},
                },
                'fields': 'indentFirstLine,indentStart',
            }
        })

        # Bold the keywords (text before "  —  ")
        keyword_count = 0
        for elem in doc['body']['content']:
            if 'paragraph' not in elem:
                continue
            si = elem.get('startIndex', 0)
            ei = elem.get('endIndex', 0)
            if si < stichwort_end:
                continue

            p = elem['paragraph']
            text = ''.join(run.get('textRun', {}).get('content', '') for run in p.get('elements', []))
            tc = text.strip()

            # Skip empty, single-letter headings (A, B, C...), and the intro note
            if not tc or len(tc) <= 2 or tc.startswith('['):
                continue

            # Find the keyword: text before "  —  " (with surrounding spaces)
            dash_pos = tc.find('  —  ')
            if dash_pos > 0:
                keyword = tc[:dash_pos]
                # Find actual position in document
                for run in p.get('elements', []):
                    content = run.get('textRun', {}).get('content', '')
                    run_start = run.get('startIndex', 0)
                    kw_pos = content.find(keyword)
                    if kw_pos >= 0:
                        abs_start = run_start + kw_pos
                        abs_end = abs_start + len(keyword)
                        is_bold = run.get('textRun', {}).get('textStyle', {}).get('bold', False)
                        if not is_bold:
                            requests.append({
                                'updateTextStyle': {
                                    'range': {'startIndex': abs_start, 'endIndex': abs_end},
                                    'textStyle': {'bold': True},
                                    'fields': 'bold',
                                }
                            })
                            keyword_count += 1
                        break

        print(f"  {keyword_count} keywords to bold")
    else:
        print("  ❌ Could not determine range")

    # === SEND BATCH ===
    if requests:
        print(f"\n🔧 Sending {len(requests)} requests...")
        # Split into batches to avoid size limits
        for batch_start in range(0, len(requests), 200):
            batch = requests[batch_start:batch_start + 200]
            try:
                batch_update(token, batch)
                print(f"  ✅ Batch {batch_start//200 + 1} applied ({len(batch)} requests)")
            except urllib.error.HTTPError as e:
                error_body = e.read().decode()
                print(f"  ❌ Error: {e.code}: {error_body[:500]}")

    print("\n" + "=" * 60)
    print("  ✅ DONE — Google Doc v5 Round 3 complete")
    print("=" * 60)


if __name__ == '__main__':
    main()
