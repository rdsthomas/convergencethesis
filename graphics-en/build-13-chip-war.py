#!/usr/bin/env python3
"""
Build English version of Figure 13: The Chip War — TSMC as the Bottleneck
Supply chain diagram: Chip Designers → TSMC → AI Labs & Cloud
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BG_COLOR = '#F5F5F5'
DARK_TEXT = '#1A1A1A'
GRAY_TEXT = '#666666'
TSMC_RED = '#B91C1C'
ASML_BOX = '#FEF3C7'

# Chip designer colors
NVIDIA_GREEN = '#76B900'
APPLE_BLACK = '#333333'
AMD_RED = '#ED1C24'
QUALCOMM_BLUE = '#3253DC'

# AI Lab colors
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
ax.text(800, 690, 'The Chip War: TSMC as the Bottleneck', fontsize=22, fontweight='bold',
        ha='center', va='top', color=DARK_TEXT, fontfamily='Liberation Sans')
ax.text(800, 655, '90% of all high-performance chips come from one company on a contested island',
        fontsize=10, ha='center', va='top', color=GRAY_TEXT, fontfamily='Liberation Sans')

# Column headers
ax.text(160, 610, 'CHIP DESIGNERS', fontsize=9, fontweight='bold', ha='center', va='center',
        color=GRAY_TEXT, fontfamily='Liberation Sans', )
ax.text(1200, 610, 'AI LABS & CLOUD', fontsize=9, fontweight='bold', ha='center', va='center',
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
tsmc_box = FancyBboxPatch((520, 320), 320, 160, boxstyle="round,pad=8",
                           facecolor=TSMC_RED, edgecolor='none')
ax.add_patch(tsmc_box)
ax.text(680, 435, 'TSMC', fontsize=26, fontweight='bold', ha='center', va='center',
        color='white', fontfamily='Liberation Sans')
ax.text(680, 395, 'Taiwan · 90% of all <7nm chips', fontsize=10, ha='center', va='center',
        color=(1,1,1,0.85), fontfamily='Liberation Sans')
ax.text(680, 365, '$27B quarterly revenue', fontsize=10, ha='center', va='center',
        color=(1,1,1,0.85), fontfamily='Liberation Sans')

# Exclamation mark (single point of failure)
ax.text(860, 510, '!', fontsize=28, fontweight='bold', ha='center', va='center',
        color=TSMC_RED, fontfamily='Liberation Sans',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEE2E2', edgecolor=TSMC_RED, linewidth=1.5))

# Single Point of Failure label
spf_box = FancyBboxPatch((870, 505), 230, 50, boxstyle="round,pad=5",
                          facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=1)
ax.add_patch(spf_box)
ax.text(985, 535, 'Single Point of Failure', fontsize=10, fontweight='bold',
        ha='center', va='center', color='#92400E', fontfamily='Liberation Sans')
ax.text(985, 515, '160 km from Chinese coast', fontsize=8, ha='center', va='center',
        color='#B45309', fontfamily='Liberation Sans')

# AI Labs (right side)
labs = [
    ('OpenAI / Microsoft', OPENAI_DARK, 530),
    ('Google DeepMind', GOOGLE_BLUE, 460),
    ('Amazon AWS', AMAZON_ORANGE, 390),
    ('Meta AI', META_BLUE, 320),
    ('xAI (Musk)', XAI_GRAY, 250),
]

for name, color, y in labs:
    box = FancyBboxPatch((1080, y - 22), 230, 45, boxstyle="round,pad=5",
                          facecolor=color, edgecolor='none', alpha=0.9)
    ax.add_patch(box)
    ax.text(1195, y, name, fontsize=11, fontweight='bold', ha='center', va='center',
            color='white', fontfamily='Liberation Sans')

# Arrows: designers → TSMC
for _, _, _, y in designers:
    ax.annotate('', xy=(520, 400), xytext=(265, y),
                arrowprops=dict(arrowstyle='->', color='#AAAAAA', lw=1, 
                                connectionstyle='arc3,rad=0.05'))

# Label "Design"
ax.text(390, 500, 'Design →', fontsize=9, ha='center', va='center',
        color=GRAY_TEXT, fontfamily='Liberation Sans', style='italic')

# Arrows: TSMC → labs
for name, _, y in labs:
    ax.annotate('', xy=(1080, y), xytext=(840, 400),
                arrowprops=dict(arrowstyle='->', color='#AAAAAA', lw=1,
                                connectionstyle='arc3,rad=-0.05'))

# Label "finished chips"
ax.text(980, 440, '← finished chips', fontsize=9, ha='center', va='center',
        color=GRAY_TEXT, fontfamily='Liberation Sans', style='italic')

# ASML box (bottom center)
asml_box = FancyBboxPatch((480, 140), 380, 60, boxstyle="round,pad=6",
                           facecolor=ASML_BOX, edgecolor='#F59E0B', linewidth=1)
ax.add_patch(asml_box)
ax.text(580, 178, '🔧', fontsize=14, ha='center', va='center')
ax.text(680, 178, 'ASML — EUV Lithography', fontsize=11, fontweight='bold',
        ha='center', va='center', color='#92400E', fontfamily='Liberation Sans')
ax.text(670, 155, 'Sole manufacturer worldwide · €28B/year', fontsize=9,
        ha='center', va='center', color='#B45309', fontfamily='Liberation Sans')

# Arrow ASML → TSMC
ax.annotate('', xy=(680, 320), xytext=(680, 205),
            arrowprops=dict(arrowstyle='->', color='#AAAAAA', lw=1, linestyle='dashed'))
ax.text(720, 260, 'machines', fontsize=8, ha='left', va='center',
        color=GRAY_TEXT, fontfamily='Liberation Sans', style='italic')

# Bottom stats bar
stats_y = 60
stats_bg = FancyBboxPatch((60, stats_y - 20), 1480, 60, boxstyle="round,pad=6",
                           facecolor='#F0F0F0', edgecolor='#DDDDDD', linewidth=1)
ax.add_patch(stats_bg)

stats = [
    ('TSMC Market Share', '~90%', 'for <7nm chips'),
    ('ASML EUV Market Share', '100%', 'no competitor'),
    ('Distance Taiwan–China', '160 km', 'Taiwan Strait'),
]

for i, (label, value, sublabel) in enumerate(stats):
    cx = 300 + i * 500
    ax.text(cx, stats_y + 28, label, fontsize=9, fontweight='bold', ha='center', va='center',
            color=TSMC_RED, fontfamily='Liberation Sans')
    ax.text(cx, stats_y + 5, value, fontsize=18, fontweight='bold', ha='center', va='center',
            color=DARK_TEXT, fontfamily='Liberation Sans')
    ax.text(cx, stats_y - 10, sublabel, fontsize=8, ha='center', va='center',
            color=GRAY_TEXT, fontfamily='Liberation Sans')

plt.tight_layout(pad=0.5)
outpath = '/root/clawd/projects/convergencethesis/graphics-en/13-chip-war-en.png'
fig.savefig(outpath, dpi=150, bbox_inches='tight', facecolor=BG_COLOR, pad_inches=0.3)
plt.close()
print(f'Saved: {outpath}')
