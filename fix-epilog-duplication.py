#!/usr/bin/env python3
"""
Fix epilog duplication in 'The AI Species' Google Doc.

The document has 2 copies of the epilog body text:
1. After "Epilog: Für Mila" heading — "Liebe Mila," at pos 444592
2. Directly after version 1 ends — "Liebe Mila," at pos 450819 (the revised version)

Version 2 is the newer/revised version (slightly edited wording).
Version 2 does NOT have its own "Epilog: Für Mila" heading.

Plan: Delete version 1's body text (444592-450819) but KEEP the "Epilog: Für Mila" heading.
This way the heading remains and version 2 follows directly under it.
"""

import json
import sys
import os

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


def get_credentials():
    with open('/tmp/gog-token.json') as f:
        token_data = json.load(f)
    with open(os.path.expanduser('~/.config/gogcli/credentials.json')) as f:
        client_data = json.load(f)
    creds = Credentials(
        token=None,
        refresh_token=token_data['refresh_token'],
        token_uri='https://oauth2.googleapis.com/token',
        client_id=client_data['client_id'],
        client_secret=client_data['client_secret'],
        scopes=['https://www.googleapis.com/auth/documents']
    )
    creds.refresh(Request())
    return creds


def build_full_text(doc):
    content = doc.get('body', {}).get('content', [])
    full_text = ''
    index_map = []
    for element in content:
        if 'paragraph' in element:
            for pe in element['paragraph'].get('elements', []):
                if 'textRun' in pe:
                    text = pe['textRun']['content']
                    doc_start = pe['startIndex']
                    index_map.append((len(full_text), doc_start))
                    full_text += text
    return full_text, index_map


def map_to_doc_index(pos, index_map, full_text_len):
    for i, (ft_start, d_start) in enumerate(index_map):
        if i + 1 < len(index_map):
            ft_end = index_map[i + 1][0]
        else:
            ft_end = full_text_len
        if ft_start <= pos < ft_end:
            offset = pos - ft_start
            return d_start + offset
    if pos == full_text_len and index_map:
        last_ft_start, last_d_start = index_map[-1]
        return last_d_start + (pos - last_ft_start)
    return None


def find_all(text, search):
    positions = []
    start = 0
    while True:
        pos = text.find(search, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    return positions


def main():
    dry_run = '--dry-run' in sys.argv

    creds = get_credentials()
    service = build('docs', 'v1', credentials=creds)

    doc_id = '1JF7Kei019q0iunIISa-fCq7Y4aLcHWHmkjBOb7MBlms'
    doc = service.documents().get(documentId=doc_id).execute()
    print(f"Document: {doc.get('title')}")

    full_text, index_map = build_full_text(doc)
    print(f"Full text length: {len(full_text)} chars")

    # Find key positions
    liebe_positions = find_all(full_text, "Liebe Mila,")
    opa_positions = find_all(full_text, "Dein Opa Thomas")
    heading_positions = find_all(full_text, "Epilog: Für Mila")

    print(f"'Liebe Mila,' at: {liebe_positions}")
    print(f"'Dein Opa Thomas' at: {opa_positions}")
    print(f"'Epilog: Für Mila' at: {heading_positions}")

    if len(liebe_positions) != 2:
        print(f"Expected 2 'Liebe Mila,' occurrences, found {len(liebe_positions)}")
        if len(liebe_positions) == 1:
            print("Only one epilog found — nothing to deduplicate!")
            return
        sys.exit(1)

    # Version 1 body: from first "Liebe Mila," to just before second "Liebe Mila,"
    v1_body_start = liebe_positions[0]  # 444592
    v1_body_end = liebe_positions[1]     # 450819

    # Preview
    preview = full_text[v1_body_start:v1_body_end]
    print(f"\n--- DELETION: Version 1 body text ---")
    print(f"  Range: {v1_body_start} - {v1_body_end} ({v1_body_end - v1_body_start} chars)")
    print(f"  Starts: '{preview[:80]}...'")
    print(f"  Ends: '...{preview[-80:]}'")

    # Verify what's before (should be heading)
    before = full_text[v1_body_start - 30:v1_body_start]
    print(f"\n  Before deletion: '...{before}'")
    assert "Epilog: Für Mila" in before, "Heading not found before deletion start!"

    # Verify what's after (should be version 2)
    after = full_text[v1_body_end:v1_body_end + 80]
    print(f"  After deletion: '{after}...'")
    assert "Liebe Mila," in after, "Version 2 not found after deletion end!"

    # Map to document indices
    doc_start = map_to_doc_index(v1_body_start, index_map, len(full_text))
    doc_end = map_to_doc_index(v1_body_end, index_map, len(full_text))

    if doc_start is None or doc_end is None:
        print("ERROR: Could not map to document indices")
        sys.exit(1)

    print(f"\n  Document indices: {doc_start} - {doc_end}")

    if dry_run:
        print("\n=== DRY RUN — no changes made ===")
        return

    # Execute deletion
    requests = [{
        'deleteContentRange': {
            'range': {
                'startIndex': doc_start,
                'endIndex': doc_end
            }
        }
    }]

    print(f"\nExecuting deletion...")
    result = service.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': requests}
    ).execute()

    print(f"\n✅ Success! Deleted {v1_body_end - v1_body_start} chars of duplicate epilog text.")
    print(f"The heading 'Epilog: Für Mila' is preserved, followed by the revised version.")
    print(f"Document: https://docs.google.com/document/d/{doc_id}/edit")


if __name__ == '__main__':
    main()
