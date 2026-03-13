#!/usr/bin/env python3
"""
Build English version of Figure 24: Risk Matrix — v2 polished
Fixes: Y-axis label overlap, subtitle spacing, cleaner bubble text
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BG_COLOR = '#F5F5F5'
DARK_TEXT = '#1A1A1A'
GRAY_TEXT = '#666666'

fig, ax = plt.subplots(1, 1, figsize=(10.67, 7.33), dpi=150)
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1600)
ax.set_ylim(0, 1100)
ax.set_aspect('equal')
ax.axis('off')

# Title
ax.text(800, 1070, 'Risk Matrix: What Can Go Wrong?', fontsize=24, fontweight='bold',
        ha='center', va='top', color=DARK_TEXT, fontfamily='Liberation Sans')
ax.text(800, 1025, 'Probability vs. Impact — and how to protect yourself',
        fontsize=11, ha='center', va='top', color=GRAY_TEXT, fontfamily='Liberation Sans')

# Grid
gx, gy = 180, 120
gw, gh = 1180, 800

# Quadrant shading
ax.fill([gx, gx+gw/2, gx+gw/2, gx], [gy+gh/2, gy+gh/2, gy+gh, gy+gh],
        color='#FEF9E7', alpha=0.4, zorder=0)
ax.fill([gx+gw/2, gx+gw, gx+gw, gx+gw/2], [gy+gh/2, gy+gh/2, gy+gh, gy+gh],
        color='#FDEDEC', alpha=0.4, zorder=0)
ax.fill([gx, gx+gw/2, gx+gw/2, gx], [gy, gy, gy+gh/2, gy+gh/2],
        color='#FAFAFA', alpha=0.4, zorder=0)
ax.fill([gx+gw/2, gx+gw, gx+gw, gx+gw/2], [gy, gy, gy+gh/2, gy+gh/2],
        color='#FEF5E7', alpha=0.4, zorder=0)

# Grid lines
ax.plot([gx, gx+gw], [gy+gh/2, gy+gh/2], '--', color='#DDDDDD', linewidth=1, zorder=1)
ax.plot([gx+gw/2, gx+gw/2], [gy, gy+gh], '--', color='#DDDDDD', linewidth=1, zorder=1)

# Axis lines
ax.plot([gx, gx+gw], [gy, gy], '-', color='#AAAAAA', linewidth=1.5, zorder=1)
ax.plot([gx, gx], [gy, gy+gh], '-', color='#AAAAAA', linewidth=1.5, zorder=1)

# Quadrant labels
ax.text(gx + gw*0.25, gy + gh - 25, 'PLAN', fontsize=12, fontweight='bold',
        ha='center', va='top', color='#D4AC0D', fontfamily='Liberation Sans')
ax.text(gx + gw*0.75, gy + gh - 25, 'ACT', fontsize=12, fontweight='bold',
        ha='center', va='top', color='#C0392B', fontfamily='Liberation Sans')
ax.text(gx + gw*0.25, gy + 20, 'MONITOR', fontsize=12, fontweight='bold',
        ha='center', va='bottom', color='#D4AC0D', fontfamily='Liberation Sans')
ax.text(gx + gw*0.75, gy + 20, 'HEDGE', fontsize=12, fontweight='bold',
        ha='center', va='bottom', color='#C0392B', fontfamily='Liberation Sans')

# X-axis
ax.text(gx + gw/2, gy - 55, 'Probability', fontsize=13, fontweight='bold',
        ha='center', va='center', color=DARK_TEXT, fontfamily='Liberation Sans')
ax.annotate('', xy=(gx + gw, gy - 55), xytext=(gx + gw - 1, gy - 55),
            arrowprops=dict(arrowstyle='->', color=DARK_TEXT, lw=1.5))

# Y-axis — shifted left to avoid overlap
ax.text(gx - 65, gy + gh/2, 'Impact', fontsize=13, fontweight='bold',
        ha='center', va='center', color=DARK_TEXT, fontfamily='Liberation Sans', rotation=90)

# Tick labels
ax.text(gx, gy - 25, 'Low', fontsize=9, ha='center', va='center', color=GRAY_TEXT)
ax.text(gx + gw/2, gy - 25, 'Medium', fontsize=9, ha='center', va='center', color=GRAY_TEXT)
ax.text(gx + gw, gy - 25, 'High', fontsize=9, ha='center', va='center', color=GRAY_TEXT)
ax.text(gx - 30, gy, 'Low', fontsize=9, ha='right', va='center', color=GRAY_TEXT)
ax.text(gx - 30, gy + gh/2, 'Medium', fontsize=9, ha='right', va='center', color=GRAY_TEXT)
ax.text(gx - 30, gy + gh, 'High', fontsize=9, ha='right', va='center', color=GRAY_TEXT)

# Risk bubbles
risks = [
    (0.12, 0.88, 62, '#C5D5F0', 'Black Swan', 'War, pandemic,\nTSMC outage', DARK_TEXT),
    (0.22, 0.72, 57, '#C5D5F0', 'AI Winter', 'Technical setback', DARK_TEXT),
    (0.42, 0.70, 62, '#E8C8A0', 'Social\nInstability', 'Mass unemployment,\nsocial unrest', DARK_TEXT),
    (0.62, 0.65, 52, '#E8C8A0', 'Energy\nCrunch', 'Not enough power', DARK_TEXT),
    (0.40, 0.48, 52, '#E8C8A0', 'Regulation', 'EU/U.S. bans,\ncrypto crackdown', DARK_TEXT),
    (0.78, 0.48, 68, '#F0C0C0', 'Valuation\nCrash', 'AI bubble bursts,\n-50-70% correction', '#8B0000'),
    (0.68, 0.22, 52, '#D8D8D0', 'Crypto\nHacks', 'Individual losses,\nnot systemic', DARK_TEXT),
]

for xf, yf, r, color, name, subtitle, text_color in risks:
    cx = gx + gw * xf
    cy = gy + gh * yf
    circle = plt.Circle((cx, cy), r, color=color, alpha=0.7, ec='none', zorder=3)
    ax.add_patch(circle)
    ax.text(cx, cy + 15, name, fontsize=11, fontweight='bold', ha='center', va='center',
            color=text_color, fontfamily='Liberation Sans', linespacing=1.1, zorder=4)
    ax.text(cx, cy - 20, subtitle, fontsize=7.5, ha='center', va='center',
            color=GRAY_TEXT, fontfamily='Liberation Sans', linespacing=1.2, zorder=4)

# Footer
ax.text(800, 50, 'Bubble size = uncertainty of estimate. Positioning based on scenarios in Chapters 10 + 15.',
        fontsize=9, ha='center', va='center', color=GRAY_TEXT, fontfamily='Liberation Sans',
        style='italic')

plt.tight_layout(pad=0.5)
outpath = '/root/clawd/projects/convergencethesis/graphics-en/24-risk-matrix-en.png'
fig.savefig(outpath, dpi=150, bbox_inches='tight', facecolor=BG_COLOR, pad_inches=0.2)
plt.close()
print(f'Saved: {outpath}')
