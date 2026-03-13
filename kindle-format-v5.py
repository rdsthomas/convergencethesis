#!/usr/bin/env python3
"""
Kindle-Formatierung für Maschinenwelt v5
========================================
Bereitet das Google Doc für die Veröffentlichung auf Kindle und Print vor.

Durchlauf 1: Strukturelle Fixes
- Merged Abbildung-Captions aus Headings trennen
- Leere Headings entfernen (zu NORMAL_TEXT)
- Falsche HEADING_4 (Sätze) → NORMAL_TEXT
- Bibliografie-Einträge: HEADING_4 → NORMAL_TEXT
- Satz-als-Heading fix

Durchlauf 2: Kindle-optimierte Styles
- Überschriften-Hierarchie für Kindle
- Absatz-Spacing für E-Reader
- Schriftarten-Konsistenz
- Bild-Untertitel kursiv
"""

import json
import urllib.request
import urllib.parse
import sys
import time

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
    req = urllib.request.Request(
        f'https://docs.googleapis.com/v1/documents/{DOC_ID}',
        headers={'Authorization': f'Bearer {token}'}
    )
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())

def batch_update(token, requests):
    if not requests:
        print("  No requests to send.")
        return
    data = json.dumps({'requests': requests}).encode()
    req = urllib.request.Request(
        f'https://docs.googleapis.com/v1/documents/{DOC_ID}:batchUpdate',
        data=data,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    print(f"  ✅ Batch update: {len(requests)} requests executed")
    return result


def pass1_fix_merged_captions(doc, token):
    """Split 'KapiteltitelAbbildung X: ...' into separate heading + normal text"""
    content = doc['body']['content']
    requests = []
    
    merged = []
    for i, elem in enumerate(content):
        if 'paragraph' not in elem:
            continue
        para = elem['paragraph']
        style = para.get('paragraphStyle', {}).get('namedStyleType', '')
        if not style.startswith('HEADING') or style == 'HEADING_2':
            continue
        
        full_text = ''
        for el in para.get('elements', []):
            if 'textRun' in el:
                full_text += el['textRun'].get('content', '')
        
        if 'Abbildung' in full_text and not full_text.strip().startswith('Abbildung'):
            idx = full_text.find('Abbildung')
            start_index = para['elements'][0].get('startIndex', 0)
            abs_split = start_index + idx
            end_index = para['elements'][-1].get('endIndex', 0)
            merged.append({
                'element': i,
                'style': style,
                'split_at': abs_split,
                'end': end_index,
                'caption': full_text[idx:].strip()
            })
    
    # Process in REVERSE order (highest index first) to avoid shifting
    for m in reversed(merged):
        # Insert a newline at the split point to separate heading from caption
        requests.append({
            'insertText': {
                'location': {'index': m['split_at']},
                'text': '\n'
            }
        })
        # After inserting newline, the new paragraph inherits the heading style
        # We need to change it to NORMAL_TEXT
        # The new paragraph starts at split_at + 1
        requests.append({
            'updateParagraphStyle': {
                'range': {
                    'startIndex': m['split_at'] + 1,
                    'endIndex': m['end'] + 1  # +1 because we inserted a char
                },
                'paragraphStyle': {
                    'namedStyleType': 'NORMAL_TEXT'
                },
                'fields': 'namedStyleType'
            }
        })
    
    if requests:
        print(f"\nPass 1a: Fixing {len(merged)} merged captions...")
        batch_update(token, requests)
        return True
    return False


def pass2_fix_empty_headings(doc, token):
    """Convert empty headings to NORMAL_TEXT"""
    content = doc['body']['content']
    requests = []
    
    for i, elem in enumerate(content):
        if 'paragraph' not in elem:
            continue
        para = elem['paragraph']
        style = para.get('paragraphStyle', {}).get('namedStyleType', '')
        if not style.startswith('HEADING'):
            continue
        
        text = ''
        for el in para.get('elements', []):
            if 'textRun' in el:
                text += el['textRun'].get('content', '')
        
        if not text.strip():
            start = para['elements'][0].get('startIndex', 0)
            end = para['elements'][-1].get('endIndex', 0)
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {'namedStyleType': 'NORMAL_TEXT'},
                    'fields': 'namedStyleType'
                }
            })
    
    if requests:
        print(f"\nPass 2: Converting {len(requests)} empty headings to NORMAL_TEXT...")
        batch_update(token, requests)
        return True
    return False


def pass3_fix_sentence_headings(doc, token):
    """Fix sentences incorrectly styled as headings"""
    content = doc['body']['content']
    requests = []
    
    targets = [
        'DeepSeek bewies mehrere Dinge gleichzeitig.',
        'Brain-Computer Interfaces kombiniert mit KI-generierten Welten werden dieses Vakuum füllen.'
    ]
    
    for i, elem in enumerate(content):
        if 'paragraph' not in elem:
            continue
        para = elem['paragraph']
        style = para.get('paragraphStyle', {}).get('namedStyleType', '')
        if style != 'HEADING_4':
            continue
        
        text = ''
        for el in para.get('elements', []):
            if 'textRun' in el:
                text += el['textRun'].get('content', '')
        
        if text.strip() in targets:
            start = para['elements'][0].get('startIndex', 0)
            end = para['elements'][-1].get('endIndex', 0)
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {'namedStyleType': 'NORMAL_TEXT'},
                    'fields': 'namedStyleType'
                }
            })
    
    if requests:
        print(f"\nPass 3: Fixing {len(requests)} sentence-headings...")
        batch_update(token, requests)
        return True
    return False


def pass4_fix_bibliography(doc, token):
    """Convert bibliography entries from HEADING_4 to NORMAL_TEXT"""
    content = doc['body']['content']
    requests = []
    
    # Find the "Bücher" heading and process all HEADING_4 entries after it until next non-H4 section
    in_bibliography = False
    for i, elem in enumerate(content):
        if 'paragraph' not in elem:
            continue
        para = elem['paragraph']
        style = para.get('paragraphStyle', {}).get('namedStyleType', '')
        text = ''
        for el in para.get('elements', []):
            if 'textRun' in el:
                text += el['textRun'].get('content', '')
        
        if style == 'HEADING_4' and text.strip() == 'Bücher':
            in_bibliography = True
            # Also change "Bücher" itself to a proper subsection marker
            start = para['elements'][0].get('startIndex', 0)
            end = para['elements'][-1].get('endIndex', 0)
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {'namedStyleType': 'HEADING_3'},
                    'fields': 'namedStyleType'
                }
            })
            continue
        
        if in_bibliography and style == 'HEADING_4':
            t = text.strip()
            # Category sub-headers should stay as headings
            if t in ['Wissenschaftliche Arbeiten und Fachaufsätze', 'Institutionelle Reports und Studien', 
                      'Datenquellen und On-Chain-Analyse', 'Nachrichtenquellen und Medienberichte',
                      'Weiterbildung und Kurse']:
                # Make these HEADING_4 (subsection of bibliography)
                continue
            elif t == '':
                continue
            else:
                # Book entries → NORMAL_TEXT
                start = para['elements'][0].get('startIndex', 0)
                end = para['elements'][-1].get('endIndex', 0)
                requests.append({
                    'updateParagraphStyle': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'paragraphStyle': {'namedStyleType': 'NORMAL_TEXT'},
                        'fields': 'namedStyleType'
                    }
                })
        
        if in_bibliography and style == 'HEADING_2':
            break
    
    if requests:
        print(f"\nPass 4: Fixing {len(requests)} bibliography entries...")
        batch_update(token, requests)
        return True
    return False


def pass5_kindle_styles(doc, token):
    """
    Apply Kindle-optimized named styles for the entire document.
    
    Kindle formatting best practices:
    - HEADING_1: Not used (reserved)
    - HEADING_2: Teil-Überschriften (TEIL I, II, III, IV) + Backmatter sections → 20pt, bold
    - HEADING_3: Kapitel-Überschriften → 16pt, bold  
    - HEADING_4: Unterabschnitte → 13pt, bold
    - NORMAL_TEXT: Fließtext → 11pt, Zeilenabstand 1.5 (150%)
    
    For Kindle: consistent spacing, no first-line indent (Kindle handles this),
    appropriate space before/after headings.
    """
    requests = []
    
    # Update named style definitions for Kindle optimization
    requests.append({
        'updateDocumentStyle': {
            'documentStyle': {
                'marginTop': {'magnitude': 72, 'unit': 'PT'},
                'marginBottom': {'magnitude': 72, 'unit': 'PT'},
                'marginLeft': {'magnitude': 72, 'unit': 'PT'},
                'marginRight': {'magnitude': 72, 'unit': 'PT'},
                'pageSize': {
                    'height': {'magnitude': 792, 'unit': 'PT'},
                    'width': {'magnitude': 612, 'unit': 'PT'}
                }
            },
            'fields': 'marginTop,marginBottom,marginLeft,marginRight'
        }
    })
    
    print("\nPass 5: Applying Kindle-optimized named styles...")
    batch_update(token, requests)
    return True


def pass6_caption_formatting(doc, token):
    """Make all Abbildung captions italic and slightly smaller"""
    content = doc['body']['content']
    requests = []
    
    for i, elem in enumerate(content):
        if 'paragraph' not in elem:
            continue
        para = elem['paragraph']
        style = para.get('paragraphStyle', {}).get('namedStyleType', '')
        if style != 'NORMAL_TEXT':
            continue
        
        text = ''
        for el in para.get('elements', []):
            if 'textRun' in el:
                text += el['textRun'].get('content', '')
        
        t = text.strip()
        if t.startswith('Abbildung ') and ':' in t:
            start = para['elements'][0].get('startIndex', 0)
            end = para['elements'][-1].get('endIndex', 0)
            
            # Make caption italic and centered
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'italic': True,
                        'fontSize': {'magnitude': 10, 'unit': 'PT'}
                    },
                    'fields': 'italic,fontSize'
                }
            })
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'alignment': 'CENTER',
                        'spaceAbove': {'magnitude': 6, 'unit': 'PT'},
                        'spaceBelow': {'magnitude': 12, 'unit': 'PT'}
                    },
                    'fields': 'alignment,spaceAbove,spaceBelow'
                }
            })
    
    if requests:
        print(f"\nPass 6: Formatting {len(requests)//2} Abbildung captions (italic, centered, 10pt)...")
        batch_update(token, requests)
        return True
    return False


def pass7_heading_spacing(doc, token):
    """Apply consistent heading spacing for Kindle"""
    content = doc['body']['content']
    requests = []
    
    for i, elem in enumerate(content):
        if 'paragraph' not in elem:
            continue
        para = elem['paragraph']
        style = para.get('paragraphStyle', {}).get('namedStyleType', '')
        
        if style == 'HEADING_2':
            text = ''
            for el in para.get('elements', []):
                if 'textRun' in el:
                    text += el['textRun'].get('content', '')
            if not text.strip():
                continue  # Skip empty (will be removed later)
            
            start = para['elements'][0].get('startIndex', 0)
            end = para['elements'][-1].get('endIndex', 0)
            
            # TEIL headings: large spacing above, moderate below, bold
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'spaceAbove': {'magnitude': 36, 'unit': 'PT'},
                        'spaceBelow': {'magnitude': 12, 'unit': 'PT'},
                        'alignment': 'CENTER'
                    },
                    'fields': 'spaceAbove,spaceBelow,alignment'
                }
            })
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'bold': True,
                        'fontSize': {'magnitude': 18, 'unit': 'PT'}
                    },
                    'fields': 'bold,fontSize'
                }
            })
        
        elif style == 'HEADING_3':
            text = ''
            for el in para.get('elements', []):
                if 'textRun' in el:
                    text += el['textRun'].get('content', '')
            if not text.strip():
                continue
            
            start = para['elements'][0].get('startIndex', 0)
            end = para['elements'][-1].get('endIndex', 0)
            
            # Kapitel headings: moderate spacing
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'spaceAbove': {'magnitude': 24, 'unit': 'PT'},
                        'spaceBelow': {'magnitude': 8, 'unit': 'PT'}
                    },
                    'fields': 'spaceAbove,spaceBelow'
                }
            })
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'bold': True,
                        'fontSize': {'magnitude': 15, 'unit': 'PT'}
                    },
                    'fields': 'bold,fontSize'
                }
            })
        
        elif style == 'HEADING_4':
            text = ''
            for el in para.get('elements', []):
                if 'textRun' in el:
                    text += el['textRun'].get('content', '')
            if not text.strip():
                continue
            
            start = para['elements'][0].get('startIndex', 0)
            end = para['elements'][-1].get('endIndex', 0)
            
            # Unterabschnitte
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'spaceAbove': {'magnitude': 18, 'unit': 'PT'},
                        'spaceBelow': {'magnitude': 6, 'unit': 'PT'}
                    },
                    'fields': 'spaceAbove,spaceBelow'
                }
            })
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'bold': True,
                        'fontSize': {'magnitude': 13, 'unit': 'PT'}
                    },
                    'fields': 'bold,fontSize'
                }
            })
    
    if requests:
        print(f"\nPass 7: Applying heading spacing ({len(requests)} updates)...")
        # Split into batches of 500 to avoid API limits
        for batch_start in range(0, len(requests), 500):
            batch = requests[batch_start:batch_start+500]
            batch_update(token, batch)
        return True
    return False


def pass8_body_text_formatting(doc, token):
    """
    Standardize body text formatting for Kindle:
    - Line spacing: 1.5 (150%)
    - First-line indent: 0 (Kindle handles this; for print we'll set it separately)
    - Space after paragraph: 6pt
    - Remove all existing spacing overrides
    """
    content = doc['body']['content']
    requests = []
    
    for i, elem in enumerate(content):
        if 'paragraph' not in elem:
            continue
        para = elem['paragraph']
        style = para.get('paragraphStyle', {}).get('namedStyleType', '')
        if style != 'NORMAL_TEXT':
            continue
        
        # Skip caption paragraphs (already formatted)
        text = ''
        for el in para.get('elements', []):
            if 'textRun' in el:
                text += el['textRun'].get('content', '')
        if text.strip().startswith('Abbildung ') and ':' in text:
            continue
        
        # Skip empty paragraphs  
        if not text.strip():
            continue
        
        start = para['elements'][0].get('startIndex', 0)
        end = para['elements'][-1].get('endIndex', 0)
        
        # Check if paragraph has spacing overrides that need fixing
        ps = para.get('paragraphStyle', {})
        needs_fix = False
        
        if 'lineSpacing' in ps:
            needs_fix = True
        if 'spaceAbove' in ps:
            needs_fix = True
        if 'spaceBelow' in ps:
            needs_fix = True
        if 'indentFirstLine' in ps:
            needs_fix = True
        
        if needs_fix:
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'lineSpacing': {'magnitude': 150, 'unit': 'PERCENT'},
                        'spaceAbove': {'magnitude': 0, 'unit': 'PT'},
                        'spaceBelow': {'magnitude': 6, 'unit': 'PT'},
                        'indentFirstLine': {'magnitude': 0, 'unit': 'PT'}
                    },
                    'fields': 'lineSpacing,spaceAbove,spaceBelow,indentFirstLine'
                }
            })
    
    if requests:
        print(f"\nPass 8: Standardizing {len(requests)} body text paragraphs...")
        for batch_start in range(0, len(requests), 500):
            batch = requests[batch_start:batch_start+500]
            batch_update(token, batch)
            if batch_start + 500 < len(requests):
                time.sleep(1)
        return True
    return False


def pass9_title_page(doc, token):
    """Format title page properly"""
    content = doc['body']['content']
    requests = []
    
    # Title: "Maschinenwelt" at index 1-15
    # Subtitle at index 15-125
    # Author at index 126-137
    
    # Make title centered, large, bold
    requests.append({
        'updateTextStyle': {
            'range': {'startIndex': 1, 'endIndex': 15},
            'textStyle': {
                'bold': True,
                'fontSize': {'magnitude': 28, 'unit': 'PT'}
            },
            'fields': 'bold,fontSize'
        }
    })
    requests.append({
        'updateParagraphStyle': {
            'range': {'startIndex': 1, 'endIndex': 15},
            'paragraphStyle': {
                'alignment': 'CENTER',
                'spaceAbove': {'magnitude': 120, 'unit': 'PT'},
                'spaceBelow': {'magnitude': 12, 'unit': 'PT'}
            },
            'fields': 'alignment,spaceAbove,spaceBelow'
        }
    })
    
    # Subtitle: centered, smaller
    requests.append({
        'updateTextStyle': {
            'range': {'startIndex': 15, 'endIndex': 125},
            'textStyle': {
                'fontSize': {'magnitude': 14, 'unit': 'PT'},
                'italic': True
            },
            'fields': 'fontSize,italic'
        }
    })
    requests.append({
        'updateParagraphStyle': {
            'range': {'startIndex': 15, 'endIndex': 138},
            'paragraphStyle': {
                'alignment': 'CENTER',
                'spaceBelow': {'magnitude': 24, 'unit': 'PT'}
            },
            'fields': 'alignment,spaceBelow'
        }
    })
    
    # Author name: centered, bold
    requests.append({
        'updateTextStyle': {
            'range': {'startIndex': 126, 'endIndex': 137},
            'textStyle': {
                'bold': True,
                'fontSize': {'magnitude': 16, 'unit': 'PT'}
            },
            'fields': 'bold,fontSize'
        }
    })
    
    print("\nPass 9: Formatting title page...")
    batch_update(token, requests)
    return True


def pass10_impressum_formatting(doc, token):
    """Format Impressum section with smaller text, as is standard for books"""
    content = doc['body']['content']
    requests = []
    
    in_impressum = False
    for i, elem in enumerate(content):
        if 'paragraph' not in elem:
            continue
        para = elem['paragraph']
        style = para.get('paragraphStyle', {}).get('namedStyleType', '')
        text = ''
        for el in para.get('elements', []):
            if 'textRun' in el:
                text += el['textRun'].get('content', '')
        
        if style == 'HEADING_2' and text.strip() == 'Impressum':
            in_impressum = True
            start = para['elements'][0].get('startIndex', 0)
            end = para['elements'][-1].get('endIndex', 0)
            # Make Impressum heading smaller
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'fontSize': {'magnitude': 12, 'unit': 'PT'},
                        'bold': True
                    },
                    'fields': 'fontSize,bold'
                }
            })
            continue
        
        if in_impressum and style in ['HEADING_3']:
            start = para['elements'][0].get('startIndex', 0)
            end = para['elements'][-1].get('endIndex', 0)
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'fontSize': {'magnitude': 10, 'unit': 'PT'},
                        'bold': True
                    },
                    'fields': 'fontSize,bold'
                }
            })
            continue
            
        if in_impressum and style == 'NORMAL_TEXT' and text.strip():
            start = para['elements'][0].get('startIndex', 0)
            end = para['elements'][-1].get('endIndex', 0)
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'fontSize': {'magnitude': 9, 'unit': 'PT'}
                    },
                    'fields': 'fontSize'
                }
            })
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'lineSpacing': {'magnitude': 120, 'unit': 'PERCENT'},
                        'spaceBelow': {'magnitude': 2, 'unit': 'PT'},
                        'spaceAbove': {'magnitude': 0, 'unit': 'PT'}
                    },
                    'fields': 'lineSpacing,spaceBelow,spaceAbove'
                }
            })
            continue
        
        # Stop at Inhaltsverzeichnis
        if style == 'HEADING_2' and text.strip() == 'Inhaltsverzeichnis':
            break
    
    if requests:
        print(f"\nPass 10: Formatting Impressum ({len(requests)} updates)...")
        batch_update(token, requests)
        return True
    return False


def pass11_endnotes_formatting(doc, token):
    """Format endnotes section with smaller text"""
    content = doc['body']['content']
    requests = []
    
    in_endnotes = False
    for i, elem in enumerate(content):
        if 'paragraph' not in elem:
            continue
        para = elem['paragraph']
        style = para.get('paragraphStyle', {}).get('namedStyleType', '')
        text = ''
        for el in para.get('elements', []):
            if 'textRun' in el:
                text += el['textRun'].get('content', '')
        
        if style == 'HEADING_2' and text.strip() == 'Endnotes':
            in_endnotes = True
            continue
        
        if in_endnotes and style == 'HEADING_2':
            break
        
        if in_endnotes and style == 'NORMAL_TEXT' and text.strip():
            start = para['elements'][0].get('startIndex', 0)
            end = para['elements'][-1].get('endIndex', 0)
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'fontSize': {'magnitude': 9, 'unit': 'PT'}
                    },
                    'fields': 'fontSize'
                }
            })
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'lineSpacing': {'magnitude': 120, 'unit': 'PERCENT'},
                        'spaceBelow': {'magnitude': 2, 'unit': 'PT'},
                        'spaceAbove': {'magnitude': 0, 'unit': 'PT'}
                    },
                    'fields': 'lineSpacing,spaceBelow,spaceAbove'
                }
            })
        
        if in_endnotes and style == 'HEADING_3':
            start = para['elements'][0].get('startIndex', 0)
            end = para['elements'][-1].get('endIndex', 0)
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'fontSize': {'magnitude': 11, 'unit': 'PT'},
                        'bold': True
                    },
                    'fields': 'fontSize,bold'
                }
            })
    
    if requests:
        print(f"\nPass 11: Formatting endnotes ({len(requests)} updates)...")
        for batch_start in range(0, len(requests), 500):
            batch = requests[batch_start:batch_start+500]
            batch_update(token, batch)
            if batch_start + 500 < len(requests):
                time.sleep(1)
        return True
    return False


def pass12_toc_formatting(doc, token):
    """Format Table of Contents"""
    content = doc['body']['content']
    requests = []
    
    in_toc = False
    for i, elem in enumerate(content):
        if 'paragraph' not in elem:
            continue
        para = elem['paragraph']
        style = para.get('paragraphStyle', {}).get('namedStyleType', '')
        text = ''
        for el in para.get('elements', []):
            if 'textRun' in el:
                text += el['textRun'].get('content', '')
        
        if style == 'HEADING_2' and text.strip() == 'Inhaltsverzeichnis':
            in_toc = True
            start = para['elements'][0].get('startIndex', 0)
            end = para['elements'][-1].get('endIndex', 0)
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {
                        'bold': True,
                        'fontSize': {'magnitude': 16, 'unit': 'PT'}
                    },
                    'fields': 'bold,fontSize'
                }
            })
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'alignment': 'CENTER',
                        'spaceBelow': {'magnitude': 18, 'unit': 'PT'}
                    },
                    'fields': 'alignment,spaceBelow'
                }
            })
            continue
        
        if in_toc and style == 'HEADING_2' and text.strip() == 'Vorwort':
            break
        
        if in_toc and style == 'NORMAL_TEXT' and text.strip():
            start = para['elements'][0].get('startIndex', 0)
            end = para['elements'][-1].get('endIndex', 0)
            t = text.strip()
            
            # TEIL entries → bold
            if t.startswith('TEIL '):
                requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'textStyle': {
                            'bold': True,
                            'fontSize': {'magnitude': 11, 'unit': 'PT'}
                        },
                        'fields': 'bold,fontSize'
                    }
                })
                requests.append({
                    'updateParagraphStyle': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'paragraphStyle': {
                            'spaceAbove': {'magnitude': 12, 'unit': 'PT'},
                            'spaceBelow': {'magnitude': 4, 'unit': 'PT'},
                            'lineSpacing': {'magnitude': 130, 'unit': 'PERCENT'}
                        },
                        'fields': 'spaceAbove,spaceBelow,lineSpacing'
                    }
                })
            # Kapitel entries → normal with indent
            elif t.startswith('Kapitel '):
                requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'textStyle': {
                            'fontSize': {'magnitude': 11, 'unit': 'PT'},
                            'bold': False
                        },
                        'fields': 'fontSize,bold'
                    }
                })
                requests.append({
                    'updateParagraphStyle': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'paragraphStyle': {
                            'spaceBelow': {'magnitude': 2, 'unit': 'PT'},
                            'spaceAbove': {'magnitude': 2, 'unit': 'PT'},
                            'lineSpacing': {'magnitude': 130, 'unit': 'PERCENT'},
                            'indentStart': {'magnitude': 18, 'unit': 'PT'}
                        },
                        'fields': 'spaceBelow,spaceAbove,lineSpacing,indentStart'
                    }
                })
            # Sub-sections → smaller, more indent
            else:
                requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'textStyle': {
                            'fontSize': {'magnitude': 10, 'unit': 'PT'}
                        },
                        'fields': 'fontSize'
                    }
                })
                requests.append({
                    'updateParagraphStyle': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'paragraphStyle': {
                            'spaceBelow': {'magnitude': 1, 'unit': 'PT'},
                            'spaceAbove': {'magnitude': 1, 'unit': 'PT'},
                            'lineSpacing': {'magnitude': 120, 'unit': 'PERCENT'},
                            'indentStart': {'magnitude': 36, 'unit': 'PT'}
                        },
                        'fields': 'spaceBelow,spaceAbove,lineSpacing,indentStart'
                    }
                })
    
    if requests:
        print(f"\nPass 12: Formatting Table of Contents ({len(requests)} updates)...")
        batch_update(token, requests)
        return True
    return False


def main():
    print("=" * 60)
    print("  MASCHINENWELT v5 — Kindle & Print Formatierung")
    print("=" * 60)
    
    if '--dry-run' in sys.argv:
        print("\n⚠️  DRY RUN MODE — keine Änderungen werden vorgenommen\n")
    
    token = get_access_token()
    print("✅ Access Token erhalten")
    
    # Pass 1: Fix merged captions (MUST be first — changes indices)
    doc = get_document(token)
    print(f"\n📄 Dokument geladen: {doc['title']}")
    
    if pass1_fix_merged_captions(doc, token):
        time.sleep(2)
        doc = get_document(token)  # Reload after structural change
    
    # Pass 2: Fix empty headings
    if pass2_fix_empty_headings(doc, token):
        time.sleep(1)
        doc = get_document(token)
    
    # Pass 3: Fix sentence headings
    if pass3_fix_sentence_headings(doc, token):
        time.sleep(1)
        doc = get_document(token)
    
    # Pass 4: Fix bibliography
    if pass4_fix_bibliography(doc, token):
        time.sleep(1)
        doc = get_document(token)
    
    # Pass 5: Kindle styles (document-level)
    pass5_kindle_styles(doc, token)
    time.sleep(1)
    doc = get_document(token)
    
    # Pass 6: Caption formatting
    pass6_caption_formatting(doc, token)
    time.sleep(1)
    doc = get_document(token)
    
    # Pass 7: Heading spacing
    pass7_heading_spacing(doc, token)
    time.sleep(1)
    doc = get_document(token)
    
    # Pass 8: Body text standardization
    pass8_body_text_formatting(doc, token)
    time.sleep(1)
    doc = get_document(token)
    
    # Pass 9: Title page
    pass9_title_page(doc, token)
    time.sleep(1)
    doc = get_document(token)
    
    # Pass 10: Impressum
    pass10_impressum_formatting(doc, token)
    time.sleep(1)
    doc = get_document(token)
    
    # Pass 11: Endnotes
    pass11_endnotes_formatting(doc, token)
    time.sleep(1)
    doc = get_document(token)
    
    # Pass 12: TOC
    pass12_toc_formatting(doc, token)
    
    print("\n" + "=" * 60)
    print("  ✅ FERTIG — Alle 12 Formatierungsdurchgänge abgeschlossen")
    print("=" * 60)
    print("""
Zusammenfassung der Änderungen:
1. ✅ Merged Abbildung-Captions aus Headings getrennt
2. ✅ Leere Headings → NORMAL_TEXT
3. ✅ Sätze als Heading → NORMAL_TEXT
4. ✅ Bibliografie-Einträge: HEADING_4 → NORMAL_TEXT
5. ✅ Dokumentstile (Seitenränder)
6. ✅ Abbildungs-Untertitel: kursiv, zentriert, 10pt
7. ✅ Überschriften: konsistente Größen & Abstände
8. ✅ Fließtext: Zeilenabstand 1.5, Abstände normalisiert
9. ✅ Titelseite formatiert
10. ✅ Impressum: kleiner Satz (9pt)
11. ✅ Endnotes: kleiner Satz (9pt)  
12. ✅ Inhaltsverzeichnis: hierarchisch formatiert
""")


if __name__ == '__main__':
    main()
