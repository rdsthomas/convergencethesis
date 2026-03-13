#!/usr/bin/env python3
"""
Build English version of Figure 1: The Convergence Thesis (Venn Diagram) — v2 polished
Fixes: title/subtitle spacing, proportions, cleaner chapter bar
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

BG_COLOR = '#F5F5F5'
DARK_TEXT = '#1A1A1A'
GRAY_TEXT = '#666666'

# Chapter bar colors
CH_BLUE = '#DBEAFE'
CH_GREEN = '#D1FAE5'
CH_RED = '#FEE2E2'
CH_AMBER = '#FEF3C7'
CH_PURPLE = '#EDE9FE'

fig, ax = plt.subplots(1, 1, figsize=(10.67, 8.3), dpi=150)
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1600)
ax.set_ylim(0, 1245)
ax.set_aspect('equal')
ax.axis('off')

# === Title with proper spacing ===
ax.text(800, 1200, 'The Convergence Thesis', fontsize=30, fontweight='bold',
        ha='center', va='top', color=DARK_TEXT, fontfamily='Liberation Sans')
ax.text(800, 1145, 'Three Technologies Converge into a New Economy', fontsize=13,
        ha='center', va='top', color=GRAY_TEXT, fontfamily='Liberation Sans')

# === Venn Circles ===
cx_ai, cy_ai = 500, 680
cx_rob, cy_rob = 900, 680
cx_cry, cy_cry = 700, 390

radius = 295

circle_ai = plt.Circle((cx_ai, cy_ai), radius, color='#C5D5F0', alpha=0.55, ec='none')
circle_rob = plt.Circle((cx_rob, cy_rob), radius, color='#C5E8D8', alpha=0.55, ec='none')
circle_cry = plt.Circle((cx_cry, cy_cry), radius, color='#F0DCC5', alpha=0.55, ec='none')
ax.add_patch(circle_ai)
ax.add_patch(circle_rob)
ax.add_patch(circle_cry)

# Center dark circle
center_x, center_y = 700, 585
center_circle = plt.Circle((center_x, center_y), 115, color='#4A4A4A', alpha=0.65, ec='none')
ax.add_patch(center_circle)

# === Circle Labels ===
ax.text(380, 770, 'AI', fontsize=28, fontweight='bold', ha='center', va='center',
        color='#2C5282', fontfamily='Liberation Sans')
ax.text(380, 725, 'Intelligence', fontsize=11, ha='center', va='center',
        color='#4A6FA5', fontfamily='Liberation Sans', style='italic')
ax.text(380, 697, 'GPT, Claude, Gemini', fontsize=10, ha='center', va='center',
        color='#7A8FAA', fontfamily='Liberation Sans')

ax.text(1010, 770, 'Robotics', fontsize=28, fontweight='bold', ha='center', va='center',
        color='#276749', fontfamily='Liberation Sans')
ax.text(1010, 725, 'Physical Form', fontsize=11, ha='center', va='center',
        color='#4A7A5A', fontfamily='Liberation Sans', style='italic')
ax.text(1010, 697, 'Tesla Bot, Figure, Atlas', fontsize=10, ha='center', va='center',
        color='#7A9A8A', fontfamily='Liberation Sans')

ax.text(700, 295, 'Crypto', fontsize=28, fontweight='bold', ha='center', va='center',
        color='#8B6914', fontfamily='Liberation Sans')
ax.text(700, 252, 'Money & Ownership', fontsize=11, ha='center', va='center',
        color='#A0864A', fontfamily='Liberation Sans', style='italic')
ax.text(700, 225, 'Bitcoin, Ethereum, Stablecoins', fontsize=10, ha='center', va='center',
        color='#B0A07A', fontfamily='Liberation Sans')

# === Overlap Labels ===
ax.text(700, 765, 'Autonomous\nAgents', fontsize=14, fontweight='bold',
        ha='center', va='center', color=DARK_TEXT, fontfamily='Liberation Sans', linespacing=1.3)

ax.text(530, 490, 'Machine\nPayments', fontsize=14, fontweight='bold',
        ha='center', va='center', color=DARK_TEXT, fontfamily='Liberation Sans', linespacing=1.3)

ax.text(870, 490, 'Tokenized\nAssets', fontsize=14, fontweight='bold',
        ha='center', va='center', color=DARK_TEXT, fontfamily='Liberation Sans', linespacing=1.3)

# === Center label ===
ax.text(center_x, center_y + 10, 'MACHINE\nECONOMY', fontsize=18, fontweight='bold',
        ha='center', va='center', color='white', fontfamily='Liberation Sans', linespacing=1.2)

# === Chapter Structure Bar (bottom) ===
bar_y = 75
bar_h = 75
bar_bg = FancyBboxPatch((100, bar_y - 5), 1400, bar_h + 10,
                         boxstyle="round,pad=8", facecolor='#EEEEEE', edgecolor='#DDDDDD', linewidth=0.8)
ax.add_patch(bar_bg)

ax.text(170, bar_y + bar_h - 15, 'Chapter Structure:', fontsize=10, fontweight='bold',
        ha='center', va='center', color=DARK_TEXT, fontfamily='Liberation Sans')

chapters = [
    ('Ch 1-2', 'AI & Phases', CH_BLUE, 360),
    ('Ch 3', 'Crypto & Tokens', CH_GREEN, 520),
    ('Ch 4-7', 'Geopolitics', CH_RED, 680),
    ('Ch 8-11', 'Future', CH_AMBER, 840),
    ('Ch 12-13', 'Strategy', CH_PURPLE, 1000),
]

for label, sublabel, color, cx in chapters:
    box = FancyBboxPatch((cx - 60, bar_y + 25), 120, 32,
                          boxstyle="round,pad=4", facecolor=color, edgecolor='#CCCCCC', linewidth=0.6)
    ax.add_patch(box)
    ax.text(cx, bar_y + 44, label, fontsize=9, fontweight='bold',
            ha='center', va='center', color=DARK_TEXT, fontfamily='Liberation Sans')
    ax.text(cx, bar_y + 10, sublabel, fontsize=8,
            ha='center', va='center', color=GRAY_TEXT, fontfamily='Liberation Sans')

for i in range(len(chapters) - 1):
    x1 = chapters[i][3] + 65
    x2 = chapters[i+1][3] - 65
    ax.annotate('', xy=(x2, bar_y + 41), xytext=(x1, bar_y + 41),
                arrowprops=dict(arrowstyle='->', color='#AAAAAA', lw=1))

plt.tight_layout(pad=0.5)
outpath = '/root/clawd/projects/convergencethesis/graphics-en/01-convergence-thesis-en.png'
fig.savefig(outpath, dpi=150, bbox_inches='tight', facecolor=BG_COLOR, pad_inches=0.2)
plt.close()
print(f'Saved: {outpath}')
