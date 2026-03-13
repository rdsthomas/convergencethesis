#!/usr/bin/env python3
"""
Build English version of Figure 7: Why Machines Can't Open a Bank Account
Two-column comparison: Traditional Banking vs Crypto Infrastructure
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BG_COLOR = '#F5F5F5'
DARK_TEXT = '#1A1A1A'
GRAY_TEXT = '#666666'
RED = '#DC2626'
GREEN = '#059669'
RED_BG = '#FEF2F2'
GREEN_BG = '#F0FDF4'

fig, ax = plt.subplots(1, 1, figsize=(10.67, 5.69), dpi=150)
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1600)
ax.set_ylim(0, 854)
ax.set_aspect('equal')
ax.axis('off')

# Title
ax.text(800, 820, "Why Machines Can't Open a Bank Account", fontsize=24, fontweight='bold',
        ha='center', va='top', color=DARK_TEXT, fontfamily='Liberation Sans')
ax.text(800, 780, "What an AI agent needs — and what the banking system offers",
        fontsize=11, ha='center', va='top', color=GRAY_TEXT, fontfamily='Liberation Sans')

# Left column header (red)
left_header = FancyBboxPatch((60, 680), 680, 55, boxstyle="round,pad=6",
                              facecolor=RED, edgecolor='none')
ax.add_patch(left_header)
ax.text(100, 708, '🏦  Traditional Banking System', fontsize=15, fontweight='bold',
        ha='left', va='center', color='white', fontfamily='Liberation Sans')

# Right column header (green)
right_header = FancyBboxPatch((860, 680), 680, 55, boxstyle="round,pad=6",
                               facecolor=GREEN, edgecolor='none')
ax.add_patch(right_header)
ax.text(900, 708, '₿  Crypto Infrastructure', fontsize=15, fontweight='bold',
        ha='left', va='center', color='white', fontfamily='Liberation Sans')

# VS circle
vs_circle = plt.Circle((800, 450), 32, color='white', ec='#DDDDDD', linewidth=2, zorder=5)
ax.add_patch(vs_circle)
ax.text(800, 450, 'VS', fontsize=14, fontweight='bold', ha='center', va='center',
        color=DARK_TEXT, fontfamily='Liberation Sans', zorder=6)

# Left items (banking limitations)
left_items = [
    ('✗', 'Open a bank account', 'Requires: passport, address, signature'),
    ('✗', 'KYC verification', 'Requires: human with face + ID'),
    ('✗', 'Apply for a credit card', 'Requires: credit score, income, employer'),
    ('✗', 'Wire transfers (Mon–Fri, 9–5)', 'Requires: SWIFT, 2–5 business days, fees'),
    ('✗', 'Sign contracts', 'Requires: legal personhood'),
]

# Right items (crypto advantages)
right_items = [
    ('✓', 'Wallet in milliseconds', 'Just a private key — no human needed'),
    ('✓', 'No identity verification', 'Permissionless — anyone (and any machine) can'),
    ('✓', 'Instant payments, global', 'USDC/USDT: seconds, micro-amounts, 24/7'),
    ('✓', 'Smart contracts = contracts', 'Code is law — no signature required'),
    ('✓', 'Autonomous transactions', 'M2M payments, DAOs, token governance'),
]

# Draw left column background
left_bg = FancyBboxPatch((60, 80), 680, 590, boxstyle="round,pad=6",
                          facecolor='white', edgecolor='#E5E5E5', linewidth=1)
ax.add_patch(left_bg)

# Draw right column background
right_bg = FancyBboxPatch((860, 80), 680, 590, boxstyle="round,pad=6",
                           facecolor='white', edgecolor='#E5E5E5', linewidth=1)
ax.add_patch(right_bg)

# Draw items
item_start_y = 630
item_spacing = 110

for i, (icon, title, desc) in enumerate(left_items):
    y = item_start_y - i * item_spacing
    ax.text(110, y, 'X', fontsize=18, fontweight='bold', ha='center', va='center',
            color=RED, fontfamily='Liberation Sans')
    ax.text(150, y, title, fontsize=13, fontweight='bold', ha='left', va='center',
            color=DARK_TEXT, fontfamily='Liberation Sans')
    ax.text(150, y - 30, desc, fontsize=9.5, ha='left', va='center',
            color=GRAY_TEXT, fontfamily='Liberation Sans')

for i, (icon, title, desc) in enumerate(right_items):
    y = item_start_y - i * item_spacing
    ax.text(910, y, 'V', fontsize=18, fontweight='bold', ha='center', va='center',
            color=GREEN, fontfamily='Liberation Sans')
    ax.text(950, y, title, fontsize=13, fontweight='bold', ha='left', va='center',
            color=DARK_TEXT, fontfamily='Liberation Sans')
    ax.text(950, y - 30, desc, fontsize=9.5, ha='left', va='center',
            color=GRAY_TEXT, fontfamily='Liberation Sans')

# Bottom tagline
ax.text(800, 30, "Crypto isn't the future of money. It's the future of machine money.",
        fontsize=12, ha='center', va='center', color=RED, fontfamily='Liberation Sans',
        style='italic')

plt.tight_layout(pad=0.5)
outpath = '/root/clawd/projects/convergencethesis/graphics-en/07-machine-vs-bank-en.png'
fig.savefig(outpath, dpi=150, bbox_inches='tight', facecolor=BG_COLOR, pad_inches=0.3)
plt.close()
print(f'Saved: {outpath}')
