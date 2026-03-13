#!/usr/bin/env python3
"""
Insert text into a Google Doc at specific positions (by searching for anchor text).
Preserves all formatting, images, and existing content.

Usage:
  python3 gdocs-insert.py <doc_id> <inserts_json_file>

inserts_json_file format:
[
  {
    "anchor": "exact text to find in the doc",
    "position": "after",  // "after" or "before" the anchor
    "text": "new text to insert\n\nWith paragraphs"
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

def find_text_index(doc, anchor_text):
    """Find the start index of anchor_text in the document."""
    content = doc.get('body', {}).get('content', [])
    
    # Build full text with index mapping
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
    
    # Search for anchor in full text
    pos = full_text.find(anchor_text)
    if pos == -1:
        return None, None
    
    # Map back to document index
    doc_index = None
    for i, (ft_start, d_start) in enumerate(index_map):
        if i + 1 < len(index_map):
            ft_end = index_map[i + 1][0]
        else:
            ft_end = len(full_text)
        
        if ft_start <= pos < ft_end:
            offset = pos - ft_start
            doc_index = d_start + offset
            break
    
    end_doc_index = None
    end_pos = pos + len(anchor_text)
    for i, (ft_start, d_start) in enumerate(index_map):
        if i + 1 < len(index_map):
            ft_end = index_map[i + 1][0]
        else:
            ft_end = len(full_text)
        
        if ft_start <= end_pos <= ft_end:
            offset = end_pos - ft_start
            end_doc_index = d_start + offset
            break
    
    return doc_index, end_doc_index

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 gdocs-insert.py <doc_id> <inserts_json_file>")
        sys.exit(1)
    
    doc_id = sys.argv[1]
    inserts_file = sys.argv[2]
    
    with open(inserts_file) as f:
        inserts = json.load(f)
    
    creds = get_credentials()
    service = build('docs', 'v1', credentials=creds)
    
    # Get the document
    doc = service.documents().get(documentId=doc_id).execute()
    print(f"Document: {doc.get('title')}")
    
    # Process inserts in REVERSE order (to preserve indices)
    # First, find all positions
    insert_ops = []
    for insert in inserts:
        anchor = insert['anchor']
        position = insert.get('position', 'after')
        text = insert['text']
        
        start_idx, end_idx = find_text_index(doc, anchor)
        if start_idx is None:
            print(f"WARNING: Anchor not found: '{anchor[:80]}...'")
            continue
        
        if position == 'after':
            insert_at = end_idx
        else:
            insert_at = start_idx
        
        insert_ops.append({
            'index': insert_at,
            'text': text,
            'anchor_preview': anchor[:60]
        })
        print(f"Found anchor at index {insert_at}: '{anchor[:60]}...'")
    
    if not insert_ops:
        print("No inserts to make!")
        sys.exit(1)
    
    # Sort by index DESCENDING (so later inserts don't shift earlier ones)
    insert_ops.sort(key=lambda x: x['index'], reverse=True)
    
    # Build batchUpdate requests
    requests = []
    for op in insert_ops:
        requests.append({
            'insertText': {
                'location': {'index': op['index']},
                'text': op['text']
            }
        })
    
    # Execute
    result = service.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': requests}
    ).execute()
    
    print(f"\nSuccess! {len(requests)} insertions made.")
    print(f"Document: https://docs.google.com/document/d/{doc_id}/edit")

if __name__ == '__main__':
    main()
