#!/usr/bin/env python3
"""Generate blog-index.json from Hugo content/blog/ markdown files.

Run before `hugo` build or as part of the deploy pipeline.
Output goes to static/blog-index.json → available at convergencethesis.com/blog-index.json

Used by council.theaispecies.world to display Weekly Dispatches
with headings, subtitles, and links — without crawling the site.
"""

import json, os, re, glob, sys

# Find project root (parent of scripts/)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
content_dir = os.path.join(project_dir, "content", "blog")
output_path = os.path.join(project_dir, "static", "blog-index.json")

posts = []
for f in sorted(glob.glob(os.path.join(content_dir, "*.md"))):
    if os.path.basename(f) == "_index.md":
        continue
    with open(f) as fh:
        content = fh.read()

    # Parse frontmatter
    fm_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not fm_match:
        continue
    fm_text, body = fm_match.groups()

    title = ""
    subtitle = ""
    date = ""
    for line in fm_text.split("\n"):
        if line.startswith("title:"):
            title = line.split(":", 1)[1].strip().strip('"').strip("'")
        elif line.startswith("subtitle:"):
            subtitle = line.split(":", 1)[1].strip().strip('"').strip("'")
        elif line.startswith("date:"):
            date = line.split(":", 1)[1].strip()

    # Extract H2 headings
    headings = []
    for line in body.split("\n"):
        m = re.match(r'^##\s+(.+)', line)
        if m:
            h = m.group(1).strip()
            if h:
                headings.append(h)

    slug = os.path.splitext(os.path.basename(f))[0]
    posts.append({
        "title": title,
        "subtitle": subtitle,
        "link": f"https://convergencethesis.com/blog/{slug}/",
        "date": date,
        "headings": headings
    })

# Sort by date desc
posts.sort(key=lambda p: p["date"], reverse=True)

os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w") as out:
    json.dump({"posts": posts}, out, indent=2, ensure_ascii=False)

print(f"Generated {output_path}: {len(posts)} posts")
for p in posts:
    print(f"  {p['date']} — {p['title']} ({len(p['headings'])} headings)")
