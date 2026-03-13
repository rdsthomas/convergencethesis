#!/usr/bin/env python3
"""
Build English version of Figure 1: The Convergence Thesis (Venn Diagram)
Recreates the German original programmatically with English labels.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# === Color palette (matching original) ===
BG_COLOR = '#F5F5F5'
AI_BLUE = '#C5D5F0'       # light blue circle
ROBOTICS_GREEN = '#C5E8D8' # light green circle  
CRYPTO_PEACH = '#F0DCC5'   # light peach circle
CENTER_DARK = '#4A4A4A'    # dark center
OVERLAP_AI_ROB = '#A8C8D8'
OVERLAP_AI_CRY = '#B8C8B0'
OVERLAP_ROB_CRY = '#D8C8A8'
GOLD = '#C8A84E'
NAVY = '#0A0A2E'
DARK_TEXT = '#1A1A1A'
GRAY_TEXT = '#666666'
LIGHT_GRAY = '#AAAAAA'

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

# === Title ===
ax.text(800, 1185, 'The Convergence Thesis', fontsize=28, fontweight='bold',
        ha='center', va='top', color=DARK_TEXT, fontfamily='Liberation Sans')
ax.text(800, 1140, 'Three Technologies Converge into a New Economy', fontsize=13,
        ha='center', va='top', color=GRAY_TEXT, fontfamily='Liberation Sans')

# === Venn Circles ===
# Positions tuned to match original layout
cx_ai, cy_ai = 500, 700
cx_rob, cy_rob = 900, 700
cx_cry, cy_cry = 700, 400

radius = 300

circle_ai = plt.Circle((cx_ai, cy_ai), radius, color=AI_BLUE, alpha=0.55, ec='none')
circle_rob = plt.Circle((cx_rob, cy_rob), radius, color=ROBOTICS_GREEN, alpha=0.55, ec='none')
circle_cry = plt.Circle((cx_cry, cy_cry), radius, color=CRYPTO_PEACH, alpha=0.55, ec='none')
ax.add_patch(circle_ai)
ax.add_patch(circle_rob)
ax.add_patch(circle_cry)

# Center dark circle
center_x, center_y = 700, 600
center_circle = plt.Circle((center_x, center_y), 120, color=CENTER_DARK, alpha=0.6, ec='none')
ax.add_patch(center_circle)

# === Circle Labels ===
# AI
ax.text(380, 780, 'AI', fontsize=26, fontweight='bold', ha='center', va='center',
        color='#2C5282', fontfamily='Liberation Sans')
ax.text(380, 740, 'Intelligence', fontsize=11, ha='center', va='center',
        color='#4A6FA5', fontfamily='Liberation Sans', style='italic')
ax.text(380, 710, 'GPT, Claude, Gemini', fontsize=10, ha='center', va='center',
        color='#7A8FAA', fontfamily='Liberation Sans')

# Robotics
ax.text(1000, 780, 'Robotics', fontsize=26, fontweight='bold', ha='center', va='center',
        color='#276749', fontfamily='Liberation Sans')
ax.text(1000, 740, 'Physical Form', fontsize=11, ha='center', va='center',
        color='#4A7A5A', fontfamily='Liberation Sans', style='italic')
ax.text(1000, 710, 'Tesla Bot, Figure, Atlas', fontsize=10, ha='center', va='center',
        color='#7A9A8A', fontfamily='Liberation Sans')

# Crypto
ax.text(700, 310, 'Crypto', fontsize=26, fontweight='bold', ha='center', va='center',
        color='#8B6914', fontfamily='Liberation Sans')
ax.text(700, 270, 'Money & Ownership', fontsize=11, ha='center', va='center',
        color='#A0864A', fontfamily='Liberation Sans', style='italic')
ax.text(700, 240, 'Bitcoin, Ethereum, Stablecoins', fontsize=10, ha='center', va='center',
        color='#B0A07A', fontfamily='Liberation Sans')

# === Overlap Labels ===
# AI + Robotics overlap
ax.text(700, 780, 'Autonomous\nAgents', fontsize=14, fontweight='bold',
        ha='center', va='center', color=DARK_TEXT, fontfamily='Liberation Sans',
        linespacing=1.3)

# AI + Crypto overlap
ax.text(530, 500, 'Machine\nPayments', fontsize=14, fontweight='bold',
        ha='center', va='center', color=DARK_TEXT, fontfamily='Liberation Sans',
        linespacing=1.3)

# Robotics + Crypto overlap
ax.text(870, 500, 'Tokenized\nAssets', fontsize=14, fontweight='bold',
        ha='center', va='center', color=DARK_TEXT, fontfamily='Liberation Sans',
        linespacing=1.3)

# === Center label ===
ax.text(center_x, center_y + 10, 'MACHINE\nECONOMY', fontsize=17, fontweight='bold',
        ha='center', va='center', color='white', fontfamily='Liberation Sans',
        linespacing=1.2)

# === Chapter Structure Bar (bottom) ===
bar_y = 95
bar_h = 70
bar_bg = FancyBboxPatch((80, bar_y - 10), 1440, bar_h + 20, 
                         boxstyle="round,pad=8", facecolor='#F0F0F0', edgecolor='#DDDDDD', linewidth=1)
ax.add_patch(bar_bg)

ax.text(155, bar_y + bar_h - 12, 'Chapter Structure:', fontsize=10, fontweight='bold',
        ha='center', va='center', color=DARK_TEXT, fontfamily='Liberation Sans')

# Chapter boxes
chapters = [
    ('Ch 1–2', 'AI & Phases', CH_BLUE, 340),
    ('Ch 3', 'Crypto & Tokens', CH_GREEN, 500),
    ('Ch 4–7', 'Geopolitics', CH_RED, 660),
    ('Ch 8–11', 'Future', CH_AMBER, 820),
    ('Ch 12–13', 'Strategy', CH_PURPLE, 980),
]

for label, sublabel, color, cx in chapters:
    box = FancyBboxPatch((cx - 55, bar_y + 22), 110, 30,
                          boxstyle="round,pad=4", facecolor=color, edgecolor='#CCCCCC', linewidth=0.8)
    ax.add_patch(box)
    ax.text(cx, bar_y + 40, label, fontsize=9, fontweight='bold',
            ha='center', va='center', color=DARK_TEXT, fontfamily='Liberation Sans')
    ax.text(cx, bar_y + 10, sublabel, fontsize=8,
            ha='center', va='center', color=GRAY_TEXT, fontfamily='Liberation Sans')

# Arrows between chapter boxes
for i in range(len(chapters) - 1):
    x1 = chapters[i][3] + 60
    x2 = chapters[i+1][3] - 60
    ax.annotate('', xy=(x2, bar_y + 37), xytext=(x1, bar_y + 37),
                arrowprops=dict(arrowstyle='->', color=GRAY_TEXT, lw=1.2))

plt.tight_layout(pad=0.5)
outpath = '/root/clawd/projects/convergencethesis/graphics-en/01-convergence-thesis-en.png'
fig.savefig(outpath, dpi=150, bbox_inches='tight', facecolor=BG_COLOR, pad_inches=0.3)
plt.close()
print(f'Saved: {outpath}')
