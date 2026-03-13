#!/usr/bin/env python3
"""
Delete text ranges from a Google Doc by searching for start and end anchors.
Preserves all formatting, images, and content outside the deleted ranges.

Usage:
  python3 gdocs-delete.py <doc_id> <deletes_json_file>

deletes_json_file format:
[
  {
    "start_anchor": "exact text marking the START of the range to delete",
    "end_anchor": "exact text marking the END of the range to delete",
    "include_anchors": true  // whether to delete the anchor texts themselves
  },
  ...
]

Requires: google-api-python-client, google-auth-oauthlib
"""

import json
import sys
import os

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


def get_credentials():
    """Load credentials from gog's exported token + client credentials."""
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
    """Build full text from document with index mapping."""
    content = doc.get('body', {}).get('content', [])
    full_text = ''
    index_map = []  # (start_index_in_full_text, start_index_in_doc)

    for element in content:
        if 'paragraph' in element:
            for pe in element['paragraph'].get('elements', []):
                if 'textRun' in pe:
                    text = pe['textRun']['content']
                    doc_start = pe['startIndex']
                    index_map.append((len(full_text), doc_start))
                    full_text += text

    return full_text, index_map


def find_all_occurrences(full_text, search_text):
    """Find all occurrences of search_text in full_text, return list of positions."""
    positions = []
    start = 0
    while True:
        pos = full_text.find(search_text, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    return positions


def map_to_doc_index(pos, index_map, full_text_len):
    """Map a position in full_text to a document index."""
    for i, (ft_start, d_start) in enumerate(index_map):
        if i + 1 < len(index_map):
            ft_end = index_map[i + 1][0]
        else:
            ft_end = full_text_len

        if ft_start <= pos < ft_end:
            offset = pos - ft_start
            return d_start + offset

    return None


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 gdocs-delete.py <doc_id> <deletes_json_file>")
        sys.exit(1)

    doc_id = sys.argv[1]
    deletes_file = sys.argv[2]

    with open(deletes_file) as f:
        deletes = json.load(f)

    creds = get_credentials()
    service = build('docs', 'v1', credentials=creds)

    # Get the document
    doc = service.documents().get(documentId=doc_id).execute()
    print(f"Document: {doc.get('title')}")

    full_text, index_map = build_full_text(doc)
    print(f"Document length: {len(full_text)} chars")

    # Process deletes — find ranges
    delete_ops = []
    for delete_spec in deletes:
        start_anchor = delete_spec['start_anchor']
        end_anchor = delete_spec['end_anchor']
        include_anchors = delete_spec.get('include_anchors', True)
        occurrence = delete_spec.get('occurrence', 1)  # which occurrence (1-based)

        # Find the nth occurrence of start_anchor
        start_positions = find_all_occurrences(full_text, start_anchor)
        if len(start_positions) < occurrence:
            print(f"WARNING: Start anchor occurrence {occurrence} not found: '{start_anchor[:80]}...'")
            print(f"  (Found {len(start_positions)} occurrences)")
            continue

        start_ft_pos = start_positions[occurrence - 1]

        # Find end_anchor AFTER the start position
        end_ft_pos = full_text.find(end_anchor, start_ft_pos)
        if end_ft_pos == -1:
            print(f"WARNING: End anchor not found after start: '{end_anchor[:80]}...'")
            continue

        # Calculate range
        if include_anchors:
            range_start_ft = start_ft_pos
            range_end_ft = end_ft_pos + len(end_anchor)
        else:
            range_start_ft = start_ft_pos + len(start_anchor)
            range_end_ft = end_ft_pos

        # Map to document indices
        doc_start = map_to_doc_index(range_start_ft, index_map, len(full_text))
        doc_end = map_to_doc_index(range_end_ft, index_map, len(full_text))

        if doc_start is None or doc_end is None:
            print(f"WARNING: Could not map indices for range")
            continue

        # Preview what we're deleting
        preview = full_text[range_start_ft:range_end_ft]
        if len(preview) > 200:
            preview = preview[:100] + '\n...[' + str(len(preview) - 200) + ' chars]...\n' + preview[-100:]

        delete_ops.append({
            'start': doc_start,
            'end': doc_end,
            'length': doc_end - doc_start,
            'preview': preview
        })
        print(f"\nDelete range: doc index {doc_start} - {doc_end} ({doc_end - doc_start} chars)")
        print(f"  Preview: {preview[:150]}...")

    if not delete_ops:
        print("\nNo deletions to make!")
        sys.exit(1)

    # Sort by start index DESCENDING (so later deletes don't shift earlier ones)
    delete_ops.sort(key=lambda x: x['start'], reverse=True)

    # Dry run confirmation
    print(f"\n{'='*60}")
    print(f"About to delete {len(delete_ops)} range(s):")
    for i, op in enumerate(delete_ops):
        print(f"  {i+1}. Index {op['start']}-{op['end']} ({op['length']} chars)")

    if '--dry-run' in sys.argv:
        print("\nDRY RUN — no changes made.")
        sys.exit(0)

    # Build batchUpdate requests
    requests = []
    for op in delete_ops:
        requests.append({
            'deleteContentRange': {
                'range': {
                    'startIndex': op['start'],
                    'endIndex': op['end']
                }
            }
        })

    # Execute
    result = service.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': requests}
    ).execute()

    print(f"\nSuccess! {len(requests)} deletion(s) made.")
    print(f"Document: https://docs.google.com/document/d/{doc_id}/edit")


if __name__ == '__main__':
    main()
