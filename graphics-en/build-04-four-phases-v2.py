#!/usr/bin/env python3
"""
Build English version of Figure 4: The Four Phases of AI — v2 polished
Fixes: title/subtitle spacing, text clipping on Phase 4
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BG_COLOR = '#F5F5F5'
DARK_TEXT = '#1A1A1A'
GRAY_TEXT = '#666666'

PHASE_COLORS = ['#60A5FA', '#A78BFA', '#F472B6', '#FB923C']

fig, ax = plt.subplots(1, 1, figsize=(10.67, 5.55), dpi=150)
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1600)
ax.set_ylim(0, 832)
ax.set_aspect('equal')
ax.axis('off')

# Title with proper spacing
ax.text(800, 810, 'The Four Phases of Artificial Intelligence', fontsize=24, fontweight='bold',
        ha='center', va='top', color=DARK_TEXT, fontfamily='Liberation Sans')
ax.text(800, 765, 'From tool to autonomous machine — and how the market grows exponentially',
        fontsize=11, ha='center', va='top', color=GRAY_TEXT, fontfamily='Liberation Sans')

# Phase data — widened Phase 4 box to avoid text clipping
phases = [
    {'num': 1, 'name': 'Tool', 'years': '2020-2024',
     'market': 'Market: ~$200B', 'examples': 'ChatGPT, Copilot, Midjourney',
     'x': 80, 'y': 100, 'w': 280, 'h': 180},
    {'num': 2, 'name': 'Coworker', 'years': '2024-2027',
     'market': 'Market: ~$1 Trillion', 'examples': 'AI Agents, Devin, Harvey',
     'x': 360, 'y': 240, 'w': 280, 'h': 180},
    {'num': 3, 'name': 'Agent', 'years': '2027-2030',
     'market': 'Market: ~$5 Trillion', 'examples': 'Autonomous AI Firms, M2M',
     'x': 650, 'y': 380, 'w': 280, 'h': 180},
    {'num': 4, 'name': 'Robot', 'years': '2028-2035+',
     'market': 'Market: ~$25+ Trillion', 'examples': 'Tesla Bot, Figure, Atlas, Optimus',
     'x': 960, 'y': 520, 'w': 310, 'h': 180},
]

bottom_labels = [
    ('Humans control AI', 200),
    ('AI works with humans', 470),
    ('AI works alone', 760),
    ('AI + body = autonomous', 1080),
]

# Connecting dashed lines
for i in range(len(phases) - 1):
    p1, p2 = phases[i], phases[i+1]
    ax.plot([p1['x'] + p1['w'], p2['x']], 
            [p1['y'] + p1['h']/2, p2['y'] + p2['h']/2],
            '--', color='#AAAAAA', linewidth=1.2, zorder=1)

# Phase boxes
for i, p in enumerate(phases):
    box = FancyBboxPatch((p['x'], p['y']), p['w'], p['h'],
                          boxstyle="round,pad=8", facecolor=PHASE_COLORS[i],
                          edgecolor='none', alpha=0.85, zorder=2)
    ax.add_patch(box)

    # Number circle
    circle = plt.Circle((p['x'] + 30, p['y'] + p['h'] - 30), 18,
                         color='white', alpha=0.3, zorder=3)
    ax.add_patch(circle)
    ax.text(p['x'] + 30, p['y'] + p['h'] - 30, str(p['num']),
            fontsize=14, fontweight='bold', ha='center', va='center',
            color='white', fontfamily='Liberation Sans', zorder=4)

    ax.text(p['x'] + 65, p['y'] + p['h'] - 30, p['name'],
            fontsize=20, fontweight='bold', ha='left', va='center',
            color='white', fontfamily='Liberation Sans', zorder=4)

    ax.text(p['x'] + 65, p['y'] + p['h'] - 65, p['years'],
            fontsize=11, ha='left', va='center',
            color=(1,1,1,0.85), fontfamily='Liberation Sans', zorder=4)

    ax.text(p['x'] + 20, p['y'] + p['h'] - 100, p['market'],
            fontsize=12, fontweight='bold', ha='left', va='center',
            color='white', fontfamily='Liberation Sans', zorder=4)

    ax.text(p['x'] + 20, p['y'] + p['h'] - 130, p['examples'],
            fontsize=9.5, ha='left', va='center',
            color=(1,1,1,0.8), fontfamily='Liberation Sans',
            style='italic', zorder=4)

# Y-axis arrow
ax.text(1380, 420, 'Addressable Market', fontsize=10, ha='center', va='center',
        color=GRAY_TEXT, fontfamily='Liberation Sans', rotation=90)
ax.annotate('', xy=(1350, 700), xytext=(1350, 120),
            arrowprops=dict(arrowstyle='->', color=GRAY_TEXT, lw=1.5))

# Bottom labels
for label, cx in bottom_labels:
    box_bg = FancyBboxPatch((cx - 120, 30), 240, 35,
                             boxstyle="round,pad=4", facecolor='white',
                             edgecolor='#DDDDDD', linewidth=0.8, zorder=2)
    ax.add_patch(box_bg)
    ax.text(cx, 48, label, fontsize=9, ha='center', va='center',
            color=GRAY_TEXT, fontfamily='Liberation Sans', zorder=3)

plt.tight_layout(pad=0.5)
outpath = '/root/clawd/projects/convergencethesis/graphics-en/04-four-phases-ai-en.png'
fig.savefig(outpath, dpi=150, bbox_inches='tight', facecolor=BG_COLOR, pad_inches=0.2)
plt.close()
print(f'Saved: {outpath}')
