#!/usr/bin/env python3
"""
Build English version of Figure 24: Risk Matrix — Probability vs. Impact
Bubble chart with risks positioned by probability/impact.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

BG_COLOR = '#F5F5F5'
DARK_TEXT = '#1A1A1A'
GRAY_TEXT = '#666666'
GOLD = '#C8A84E'

fig, ax = plt.subplots(1, 1, figsize=(10.67, 7.33), dpi=150)
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1600)
ax.set_ylim(0, 1100)
ax.set_aspect('equal')
ax.axis('off')

# Title
ax.text(800, 1060, 'Risk Matrix: What Can Go Wrong?', fontsize=24, fontweight='bold',
        ha='center', va='top', color=DARK_TEXT, fontfamily='Liberation Sans')
ax.text(800, 1020, 'Probability vs. Impact — and how to protect yourself',
        fontsize=11, ha='center', va='top', color=GRAY_TEXT, fontfamily='Liberation Sans')

# Grid area
gx, gy = 160, 100  # grid origin
gw, gh = 1200, 820  # grid size

# Background quadrant shading
# Top-left: PLAN (low prob, high impact)
ax.fill([gx, gx+gw/2, gx+gw/2, gx], [gy+gh/2, gy+gh/2, gy+gh, gy+gh],
        color='#FEF9E7', alpha=0.4, zorder=0)
# Top-right: ACT (high prob, high impact)  
ax.fill([gx+gw/2, gx+gw, gx+gw, gx+gw/2], [gy+gh/2, gy+gh/2, gy+gh, gy+gh],
        color='#FDEDEC', alpha=0.4, zorder=0)
# Bottom-left: MONITOR
ax.fill([gx, gx+gw/2, gx+gw/2, gx], [gy, gy, gy+gh/2, gy+gh/2],
        color='#FAFAFA', alpha=0.4, zorder=0)
# Bottom-right: HEDGE
ax.fill([gx+gw/2, gx+gw, gx+gw, gx+gw/2], [gy, gy, gy+gh/2, gy+gh/2],
        color='#FEF5E7', alpha=0.4, zorder=0)

# Grid lines (dashed)
ax.plot([gx, gx+gw], [gy+gh/2, gy+gh/2], '--', color='#DDDDDD', linewidth=1, zorder=1)
ax.plot([gx+gw/2, gx+gw/2], [gy, gy+gh], '--', color='#DDDDDD', linewidth=1, zorder=1)

# Axis lines
ax.plot([gx, gx+gw], [gy, gy], '-', color='#AAAAAA', linewidth=1.5, zorder=1)
ax.plot([gx, gx], [gy, gy+gh], '-', color='#AAAAAA', linewidth=1.5, zorder=1)

# Quadrant labels
ax.text(gx + gw*0.25, gy + gh - 30, 'PLAN', fontsize=12, fontweight='bold',
        ha='center', va='top', color='#D4AC0D', fontfamily='Liberation Sans')
ax.text(gx + gw*0.75, gy + gh - 30, 'ACT', fontsize=12, fontweight='bold',
        ha='center', va='top', color='#C0392B', fontfamily='Liberation Sans')
ax.text(gx + gw*0.25, gy + 25, 'MONITOR', fontsize=12, fontweight='bold',
        ha='center', va='bottom', color='#D4AC0D', fontfamily='Liberation Sans')
ax.text(gx + gw*0.75, gy + 25, 'HEDGE', fontsize=12, fontweight='bold',
        ha='center', va='bottom', color='#C0392B', fontfamily='Liberation Sans')

# Axis labels
ax.text(gx + gw/2, gy - 50, 'Probability →', fontsize=13, fontweight='bold',
        ha='center', va='center', color=DARK_TEXT, fontfamily='Liberation Sans')
ax.text(gx - 50, gy + gh/2, 'Impact', fontsize=13, fontweight='bold',
        ha='center', va='center', color=DARK_TEXT, fontfamily='Liberation Sans', rotation=90)
ax.text(gx - 30, gy + gh/2, '↓', fontsize=14, ha='center', va='center', color=DARK_TEXT)

# Axis tick labels
ax.text(gx, gy - 20, 'Low', fontsize=9, ha='center', va='center', color=GRAY_TEXT)
ax.text(gx + gw/2, gy - 20, 'Medium', fontsize=9, ha='center', va='center', color=GRAY_TEXT)
ax.text(gx + gw, gy - 20, 'High', fontsize=9, ha='center', va='center', color=GRAY_TEXT)
ax.text(gx - 20, gy, 'Low', fontsize=9, ha='right', va='center', color=GRAY_TEXT)
ax.text(gx - 20, gy + gh/2, 'Medium', fontsize=9, ha='right', va='center', color=GRAY_TEXT)
ax.text(gx - 20, gy + gh, 'High', fontsize=9, ha='right', va='center', color=GRAY_TEXT)

# Risk bubbles
# (x_frac, y_frac, radius, color, name, subtitle)
risks = [
    (0.12, 0.88, 65, '#C5D5F0', 'Black Swan', 'War, pandemic,\nTSMC outage'),
    (0.22, 0.72, 60, '#C5D5F0', 'AI Winter', 'Technical setback'),
    (0.42, 0.70, 65, '#E8C8A0', 'Social\nInstability', 'Mass unemployment,\nsocial unrest'),
    (0.62, 0.65, 55, '#E8C8A0', 'Energy\nCrunch', 'Not enough power'),
    (0.40, 0.48, 55, '#E8C8A0', 'Regulation', 'EU/US bans,\ncrypto crackdown'),
    (0.78, 0.48, 70, '#F0C0C0', 'Valuation\nCrash', 'AI bubble bursts,\n-50–70% correction'),
    (0.68, 0.22, 55, '#D8D8D0', 'Crypto\nHacks', 'Individual losses,\nnot systemic'),
]

for xf, yf, r, color, name, subtitle in risks:
    cx = gx + gw * xf
    cy = gy + gh * yf
    circle = plt.Circle((cx, cy), r, color=color, alpha=0.7, ec='none', zorder=3)
    ax.add_patch(circle)
    ax.text(cx, cy + 12, name, fontsize=11, fontweight='bold', ha='center', va='center',
            color='#8B0000' if 'Crash' in name else DARK_TEXT, fontfamily='Liberation Sans',
            linespacing=1.1, zorder=4)
    ax.text(cx, cy - 22, subtitle, fontsize=7.5, ha='center', va='center',
            color=GRAY_TEXT, fontfamily='Liberation Sans', linespacing=1.2, zorder=4)

# Footer note
ax.text(800, 30, 'Bubble size ≈ uncertainty of estimate. Positioning based on scenarios in Chapters 10 + 15.',
        fontsize=9, ha='center', va='center', color=GRAY_TEXT, fontfamily='Liberation Sans',
        style='italic')

plt.tight_layout(pad=0.5)
outpath = '/root/clawd/projects/convergencethesis/graphics-en/24-risk-matrix-en.png'
fig.savefig(outpath, dpi=150, bbox_inches='tight', facecolor=BG_COLOR, pad_inches=0.3)
plt.close()
print(f'Saved: {outpath}')
