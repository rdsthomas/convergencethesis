#!/usr/bin/env python3
"""
Build English version of Figure 13: The Chip War — v2 polished
Fixes: no emoji, proper spacing, no overlap of Single Point of Failure box
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BG_COLOR = '#F5F5F5'
DARK_TEXT = '#1A1A1A'
GRAY_TEXT = '#666666'
TSMC_RED = '#B91C1C'

NVIDIA_GREEN = '#76B900'
APPLE_BLACK = '#333333'
AMD_RED = '#ED1C24'
QUALCOMM_BLUE = '#3253DC'

OPENAI_DARK = '#412991'
GOOGLE_BLUE = '#4285F4'
AMAZON_ORANGE = '#FF9900'
META_BLUE = '#0668E1'
XAI_GRAY = '#555555'

fig, ax = plt.subplots(1, 1, figsize=(10.67, 4.8), dpi=150)
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1600)
ax.set_ylim(0, 720)
ax.set_aspect('equal')
ax.axis('off')

# Title
ax.text(800, 700, 'The Chip War: TSMC as the Bottleneck', fontsize=22, fontweight='bold',
        ha='center', va='top', color=DARK_TEXT, fontfamily='Liberation Sans')
ax.text(800, 662, '90% of all high-performance chips come from one company on a contested island',
        fontsize=10, ha='center', va='top', color=GRAY_TEXT, fontfamily='Liberation Sans')

# Column headers
ax.text(160, 610, 'CHIP DESIGNERS', fontsize=9, fontweight='bold', ha='center', va='center',
        color=GRAY_TEXT, fontfamily='Liberation Sans')
ax.text(1300, 610, 'AI LABS & CLOUD', fontsize=9, fontweight='bold', ha='center', va='center',
        color=GRAY_TEXT, fontfamily='Liberation Sans')

# Chip designers (left side)
designers = [
    ('NVIDIA', 'H100, B200, GB200', NVIDIA_GREEN, 530),
    ('Apple', 'M4, A18 Pro', APPLE_BLACK, 430),
    ('AMD', 'MI300, EPYC', AMD_RED, 330),
    ('Qualcomm', 'Snapdragon', QUALCOMM_BLUE, 230),
]

for name, chips, color, y in designers:
    box = FancyBboxPatch((60, y - 25), 200, 55, boxstyle="round,pad=5",
                          facecolor=color, edgecolor='none', alpha=0.9)
    ax.add_patch(box)
    ax.text(160, y + 8, name, fontsize=12, fontweight='bold', ha='center', va='center',
            color='white', fontfamily='Liberation Sans')
    ax.text(160, y - 12, chips, fontsize=8, ha='center', va='center',
            color=(1,1,1,0.8), fontfamily='Liberation Sans')

# TSMC center box
tsmc_box = FancyBboxPatch((550, 300), 300, 160, boxstyle="round,pad=8",
                           facecolor=TSMC_RED, edgecolor='none')
ax.add_patch(tsmc_box)
ax.text(700, 420, 'TSMC', fontsize=26, fontweight='bold', ha='center', va='center',
        color='white', fontfamily='Liberation Sans')
ax.text(700, 382, 'Taiwan  |  90% of all <7nm chips', fontsize=9.5, ha='center', va='center',
        color=(1,1,1,0.85), fontfamily='Liberation Sans')
ax.text(700, 355, '$27B quarterly revenue', fontsize=9.5, ha='center', va='center',
        color=(1,1,1,0.85), fontfamily='Liberation Sans')

# Exclamation mark
exc_circle = plt.Circle((870, 485), 14, color='#FEE2E2', ec=TSMC_RED, linewidth=2, zorder=5)
ax.add_patch(exc_circle)
ax.text(870, 487, '!', fontsize=16, fontweight='bold', ha='center', va='center',
        color=TSMC_RED, fontfamily='Liberation Sans', zorder=6)

# Single Point of Failure label — repositioned to avoid overlap
spf_box = FancyBboxPatch((900, 470), 220, 45, boxstyle="round,pad=5",
                          facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=1, zorder=4)
ax.add_patch(spf_box)
ax.text(1010, 498, 'Single Point of Failure', fontsize=9.5, fontweight='bold',
        ha='center', va='center', color='#92400E', fontfamily='Liberation Sans', zorder=5)
ax.text(1010, 478, '160 km from Chinese coast', fontsize=8, ha='center', va='center',
        color='#B45309', fontfamily='Liberation Sans', zorder=5)

# AI Labs (right side) — shifted right to avoid overlap
labs = [
    ('OpenAI / Microsoft', OPENAI_DARK, 530),
    ('Google DeepMind', GOOGLE_BLUE, 460),
    ('Amazon AWS', AMAZON_ORANGE, 390),
    ('Meta AI', META_BLUE, 320),
    ('xAI (Musk)', XAI_GRAY, 250),
]

for name, color, y in labs:
    box = FancyBboxPatch((1170, y - 22), 240, 45, boxstyle="round,pad=5",
                          facecolor=color, edgecolor='none', alpha=0.9)
    ax.add_patch(box)
    ax.text(1290, y, name, fontsize=11, fontweight='bold', ha='center', va='center',
            color='white', fontfamily='Liberation Sans')

# Arrows: designers -> TSMC
for _, _, _, y in designers:
    ax.annotate('', xy=(550, 380), xytext=(265, y),
                arrowprops=dict(arrowstyle='->', color='#BBBBBB', lw=1,
                                connectionstyle='arc3,rad=0.05'))

ax.text(400, 510, 'Design', fontsize=9, ha='center', va='center',
        color=GRAY_TEXT, fontfamily='Liberation Sans', style='italic')

# Arrows: TSMC -> labs
for name, _, y in labs:
    ax.annotate('', xy=(1170, y), xytext=(855, 380),
                arrowprops=dict(arrowstyle='->', color='#BBBBBB', lw=1,
                                connectionstyle='arc3,rad=-0.05'))

ax.text(1040, 400, 'finished chips', fontsize=9, ha='center', va='center',
        color=GRAY_TEXT, fontfamily='Liberation Sans', style='italic')

# ASML box (bottom center)
asml_box = FancyBboxPatch((510, 130), 380, 55, boxstyle="round,pad=6",
                           facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=1)
ax.add_patch(asml_box)
ax.text(700, 165, 'ASML — EUV Lithography', fontsize=11, fontweight='bold',
        ha='center', va='center', color='#92400E', fontfamily='Liberation Sans')
ax.text(700, 143, 'Sole manufacturer worldwide  |  EUR 28B/year', fontsize=9,
        ha='center', va='center', color='#B45309', fontfamily='Liberation Sans')

# Arrow ASML -> TSMC
ax.annotate('', xy=(700, 300), xytext=(700, 190),
            arrowprops=dict(arrowstyle='->', color='#AAAAAA', lw=1, linestyle='dashed'))
ax.text(730, 245, 'machines', fontsize=8, ha='left', va='center',
        color=GRAY_TEXT, fontfamily='Liberation Sans', style='italic')

# Bottom stats bar
stats_y = 50
stats_bg = FancyBboxPatch((60, stats_y - 20), 1480, 55, boxstyle="round,pad=6",
                           facecolor='#EEEEEE', edgecolor='#DDDDDD', linewidth=0.8)
ax.add_patch(stats_bg)

stats = [
    ('TSMC Market Share', '~90%', 'for <7nm chips'),
    ('ASML EUV Market Share', '100%', 'no competitor'),
    ('Distance Taiwan-China', '160 km', 'Taiwan Strait'),
]

for i, (label, value, sublabel) in enumerate(stats):
    cx = 300 + i * 500
    ax.text(cx, stats_y + 22, label, fontsize=8.5, fontweight='bold', ha='center', va='center',
            color=TSMC_RED, fontfamily='Liberation Sans')
    ax.text(cx, stats_y + 2, value, fontsize=16, fontweight='bold', ha='center', va='center',
            color=DARK_TEXT, fontfamily='Liberation Sans')
    ax.text(cx, stats_y - 12, sublabel, fontsize=7.5, ha='center', va='center',
            color=GRAY_TEXT, fontfamily='Liberation Sans')

plt.tight_layout(pad=0.5)
outpath = '/root/clawd/projects/convergencethesis/graphics-en/13-chip-war-en.png'
fig.savefig(outpath, dpi=150, bbox_inches='tight', facecolor=BG_COLOR, pad_inches=0.2)
plt.close()
print(f'Saved: {outpath}')
