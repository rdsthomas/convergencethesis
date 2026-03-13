#!/usr/bin/env python3
"""
Build all 5 English graphics — v3 with generous spacing.
Key fix: use figure-fraction coordinates for titles to avoid overlap,
and increase margins between all text elements.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

OUTDIR = '/root/clawd/projects/convergencethesis/graphics-en'
BG = '#F5F5F5'
DK = '#1A1A1A'
GR = '#666666'
FONT = 'Liberation Sans'


def save(fig, name):
    path = os.path.join(OUTDIR, name)
    fig.savefig(path, dpi=150, facecolor=BG, pad_inches=0.15)
    plt.close(fig)
    print(f'  Saved: {name}')


# ===== 1. CONVERGENCE THESIS =====
def build_convergence():
    fig, ax = plt.subplots(figsize=(10, 8.2))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.set_aspect('equal'); ax.axis('off')

    # Title in figure space (never overlaps)
    fig.text(0.5, 0.96, 'The Convergence Thesis', fontsize=28, fontweight='bold',
             ha='center', va='top', color=DK, fontfamily=FONT)
    fig.text(0.5, 0.915, 'Three Technologies Converge into a New Economy', fontsize=12,
             ha='center', va='top', color=GR, fontfamily=FONT)

    # Venn circles (in axes coords 0-100)
    for cx, cy, col in [(35, 62, '#C5D5F0'), (65, 62, '#C5E8D8'), (50, 35, '#F0DCC5')]:
        ax.add_patch(plt.Circle((cx, cy), 24, color=col, alpha=0.55, ec='none'))
    ax.add_patch(plt.Circle((50, 52), 9.5, color='#4A4A4A', alpha=0.65, ec='none'))

    # Circle labels
    ax.text(25, 68, 'AI', fontsize=24, fontweight='bold', ha='center', color='#2C5282', fontfamily=FONT)
    ax.text(25, 63, 'Intelligence', fontsize=10, ha='center', color='#4A6FA5', fontfamily=FONT, style='italic')
    ax.text(25, 59, 'GPT, Claude, Gemini', fontsize=8.5, ha='center', color='#7A8FAA', fontfamily=FONT)

    ax.text(75, 68, 'Robotics', fontsize=24, fontweight='bold', ha='center', color='#276749', fontfamily=FONT)
    ax.text(75, 63, 'Physical Form', fontsize=10, ha='center', color='#4A7A5A', fontfamily=FONT, style='italic')
    ax.text(75, 59, 'Tesla Bot, Figure, Atlas', fontsize=8.5, ha='center', color='#7A9A8A', fontfamily=FONT)

    ax.text(50, 22, 'Crypto', fontsize=24, fontweight='bold', ha='center', color='#8B6914', fontfamily=FONT)
    ax.text(50, 17.5, 'Money & Ownership', fontsize=10, ha='center', color='#A0864A', fontfamily=FONT, style='italic')
    ax.text(50, 14, 'Bitcoin, Ethereum, Stablecoins', fontsize=8.5, ha='center', color='#B0A07A', fontfamily=FONT)

    # Overlaps
    ax.text(50, 70, 'Autonomous\nAgents', fontsize=12, fontweight='bold', ha='center', color=DK, fontfamily=FONT, linespacing=1.2)
    ax.text(37, 43, 'Machine\nPayments', fontsize=12, fontweight='bold', ha='center', color=DK, fontfamily=FONT, linespacing=1.2)
    ax.text(63, 43, 'Tokenized\nAssets', fontsize=12, fontweight='bold', ha='center', color=DK, fontfamily=FONT, linespacing=1.2)

    # Center
    ax.text(50, 53, 'MACHINE\nECONOMY', fontsize=14, fontweight='bold', ha='center', va='center',
            color='white', fontfamily=FONT, linespacing=1.15)

    # Chapter bar
    fig.text(0.08, 0.055, 'Chapter Structure:', fontsize=9, fontweight='bold', color=DK, fontfamily=FONT)
    chs = [('Ch 1-2','AI & Phases','#DBEAFE',0.24), ('Ch 3','Crypto & Tokens','#D1FAE5',0.38),
           ('Ch 4-7','Geopolitics','#FEE2E2',0.52), ('Ch 8-11','Future','#FEF3C7',0.66),
           ('Ch 12-13','Strategy','#EDE9FE',0.80)]
    for label, sub, col, x in chs:
        fig.text(x, 0.055, label, fontsize=8.5, fontweight='bold', ha='center', color=DK, fontfamily=FONT,
                 bbox=dict(boxstyle='round,pad=0.35', facecolor=col, edgecolor='#CCC', linewidth=0.5))
        fig.text(x, 0.025, sub, fontsize=7.5, ha='center', color=GR, fontfamily=FONT)
    for i in range(len(chs)-1):
        x1 = chs[i][3] + 0.05; x2 = chs[i+1][3] - 0.05
        fig.text((x1+x2)/2, 0.055, chr(0x2192), fontsize=10, ha='center', va='center', color='#AAA', fontfamily=FONT)

    save(fig, '01-convergence-thesis-en.png')

# ===== 4. FOUR PHASES =====
def build_four_phases():
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(0, 160); ax.set_ylim(0, 85); ax.set_aspect('equal'); ax.axis('off')

    fig.text(0.5, 0.96, 'The Four Phases of Artificial Intelligence', fontsize=22, fontweight='bold',
             ha='center', va='top', color=DK, fontfamily=FONT)
    fig.text(0.5, 0.905, 'From tool to autonomous machine — and how the market grows exponentially',
             fontsize=10, ha='center', va='top', color=GR, fontfamily=FONT)

    colors = ['#60A5FA', '#A78BFA', '#F472B6', '#FB923C']
    phases = [
        (1, 'Tool', '2020-2024', '~$200B', 'ChatGPT, Copilot, Midjourney', 5, 10, 28, 18),
        (2, 'Coworker', '2024-2027', '~$1 Trillion', 'AI Agents, Devin, Harvey', 33, 24, 28, 18),
        (3, 'Agent', '2027-2030', '~$5 Trillion', 'Autonomous AI Firms, M2M', 63, 38, 28, 18),
        (4, 'Robot', '2028-2035+', '~$25+ Trillion', 'Tesla Bot, Figure, Atlas, Optimus', 96, 52, 32, 18),
    ]

    for i, (num, name, yrs, mkt, ex, x, y, w, h) in enumerate(phases):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.8",
                              facecolor=colors[i], edgecolor='none', alpha=0.85)
        ax.add_patch(box)
        c = plt.Circle((x+3, y+h-3), 1.8, color='white', alpha=0.3)
        ax.add_patch(c)
        ax.text(x+3, y+h-3, str(num), fontsize=11, fontweight='bold', ha='center', va='center',
                color='white', fontfamily=FONT)
        ax.text(x+7, y+h-3, name, fontsize=16, fontweight='bold', ha='left', va='center',
                color='white', fontfamily=FONT)
        ax.text(x+7, y+h-6.5, yrs, fontsize=9, ha='left', va='center',
                color=(1,1,1,0.85), fontfamily=FONT)
        ax.text(x+2, y+h-10, f'Market: {mkt}', fontsize=10, fontweight='bold', ha='left', va='center',
                color='white', fontfamily=FONT)
        ax.text(x+2, y+h-13.5, ex, fontsize=8, ha='left', va='center',
                color=(1,1,1,0.8), fontfamily=FONT, style='italic')

    # Dashed connectors
    for i in range(3):
        p1 = phases[i]; p2 = phases[i+1]
        ax.plot([p1[5]+p1[7], p2[5]], [p1[6]+p1[8]/2, p2[6]+p2[8]/2],
                '--', color='#AAA', lw=1, zorder=0)

    # Right arrow
    ax.annotate('', xy=(140, 72), xytext=(140, 12),
                arrowprops=dict(arrowstyle='->', color=GR, lw=1.5))
    ax.text(143, 42, 'Addressable\nMarket', fontsize=8, ha='left', va='center',
            color=GR, fontfamily=FONT, rotation=90)

    # Bottom labels
    labels = [('Humans control AI', 18), ('AI works with humans', 46),
              ('AI works alone', 76), ('AI + body = autonomous', 110)]
    for label, cx in labels:
        ax.text(cx, 4, label, fontsize=7.5, ha='center', va='center', color=GR, fontfamily=FONT,
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#DDD', lw=0.6))

    save(fig, '04-four-phases-ai-en.png')

# ===== 7. MACHINE VS BANK =====
def build_machine_bank():
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(0, 160); ax.set_ylim(0, 90); ax.set_aspect('equal'); ax.axis('off')

    fig.text(0.5, 0.97, "Why Machines Can't Open a Bank Account", fontsize=22, fontweight='bold',
             ha='center', va='top', color=DK, fontfamily=FONT)
    fig.text(0.5, 0.925, "What an AI agent needs — and what the banking system offers",
             fontsize=10, ha='center', va='top', color=GR, fontfamily=FONT)

    RED = '#DC2626'; GREEN = '#059669'

    # Headers
    ax.add_patch(FancyBboxPatch((5, 75), 68, 6, boxstyle="round,pad=0.6", facecolor=RED, ec='none'))
    ax.text(39, 78, 'Traditional Banking System', fontsize=12, fontweight='bold',
            ha='center', va='center', color='white', fontfamily=FONT)
    ax.add_patch(FancyBboxPatch((87, 75), 68, 6, boxstyle="round,pad=0.6", facecolor=GREEN, ec='none'))
    ax.text(121, 78, 'Crypto Infrastructure', fontsize=12, fontweight='bold',
            ha='center', va='center', color='white', fontfamily=FONT)

    # VS
    vs = plt.Circle((80, 48), 3, color='white', ec='#DDD', lw=1.5, zorder=5)
    ax.add_patch(vs)
    ax.text(80, 48, 'VS', fontsize=10, fontweight='bold', ha='center', va='center',
            color=DK, fontfamily=FONT, zorder=6)

    # Backgrounds
    ax.add_patch(FancyBboxPatch((5, 8), 68, 65, boxstyle="round,pad=0.6", facecolor='white', ec='#E5E5E5', lw=0.8))
    ax.add_patch(FancyBboxPatch((87, 8), 68, 65, boxstyle="round,pad=0.6", facecolor='white', ec='#E5E5E5', lw=0.8))

    left = [
        ('Open a bank account', 'Requires: passport, address, signature'),
        ('KYC verification', 'Requires: human with face + ID'),
        ('Apply for a credit card', 'Requires: credit score, income, employer'),
        ('Wire transfers (Mon-Fri, 9-5)', 'Requires: SWIFT, 2-5 business days, fees'),
        ('Sign contracts', 'Requires: legal personhood'),
    ]
    right = [
        ('Wallet in milliseconds', 'Just a private key — no human needed'),
        ('No identity verification', 'Permissionless — anyone (and any machine) can'),
        ('Instant payments, global', 'USDC/USDT: seconds, micro-amounts, 24/7'),
        ('Smart contracts = contracts', 'Code is law — no signature required'),
        ('Autonomous transactions', 'M2M payments, DAOs, token governance'),
    ]

    for i, (title, desc) in enumerate(left):
        y = 67 - i * 12
        c = plt.Circle((10, y), 1.4, color='#FEE2E2', ec=RED, lw=1.2, zorder=3)
        ax.add_patch(c)
        ax.text(10, y, 'X', fontsize=8, fontweight='bold', ha='center', va='center', color=RED, fontfamily=FONT, zorder=4)
        ax.text(14, y + 0.8, title, fontsize=10, fontweight='bold', ha='left', va='center', color=DK, fontfamily=FONT)
        ax.text(14, y - 2.5, desc, fontsize=7.5, ha='left', va='center', color=GR, fontfamily=FONT)

    for i, (title, desc) in enumerate(right):
        y = 67 - i * 12
        c = plt.Circle((92, y), 1.4, color='#D1FAE5', ec=GREEN, lw=1.2, zorder=3)
        ax.add_patch(c)
        # Checkmark as V shape
        cx, cy = 92, y
        ax.plot([cx-0.7, cx-0.1, cx+0.8], [cy+0.1, cy-0.7, cy+0.8],
                color=GREEN, lw=2, solid_capstyle='round', zorder=4)
        ax.text(96, y + 0.8, title, fontsize=10, fontweight='bold', ha='left', va='center', color=DK, fontfamily=FONT)
        ax.text(96, y - 2.5, desc, fontsize=7.5, ha='left', va='center', color=GR, fontfamily=FONT)

    fig.text(0.5, 0.03, "Crypto isn't the future of money. It's the future of machine money.",
             fontsize=11, ha='center', color=RED, fontfamily=FONT, style='italic')

    save(fig, '07-machine-vs-bank-en.png')

# ===== 13. CHIP WAR =====
def build_chip_war():
    fig, ax = plt.subplots(figsize=(10.5, 5.0))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(0, 160); ax.set_ylim(0, 72); ax.set_aspect('equal'); ax.axis('off')

    fig.text(0.5, 0.97, 'The Chip War: TSMC as the Bottleneck', fontsize=20, fontweight='bold',
             ha='center', va='top', color=DK, fontfamily=FONT)
    fig.text(0.5, 0.915, '90% of all high-performance chips come from one company on a contested island',
             fontsize=9, ha='center', va='top', color=GR, fontfamily=FONT)

    TSMC_RED = '#B91C1C'
    ax.text(16, 64, 'CHIP DESIGNERS', fontsize=7.5, fontweight='bold', ha='center', color=GR, fontfamily=FONT)
    ax.text(140, 64, 'AI LABS & CLOUD', fontsize=7.5, fontweight='bold', ha='center', color=GR, fontfamily=FONT)

    designers = [('NVIDIA','H100, B200, GB200','#76B900',56),('Apple','M4, A18 Pro','#333',46),
                 ('AMD','MI300, EPYC','#ED1C24',36),('Qualcomm','Snapdragon','#3253DC',26)]
    for name, chips, col, y in designers:
        ax.add_patch(FancyBboxPatch((3, y-2.5), 26, 7, boxstyle="round,pad=0.5", facecolor=col, ec='none', alpha=0.9))
        ax.text(16, y+1, name, fontsize=9, fontweight='bold', ha='center', va='center', color='white', fontfamily=FONT)
        ax.text(16, y-1.2, chips, fontsize=6.5, ha='center', va='center', color=(1,1,1,0.8), fontfamily=FONT)

    # TSMC
    ax.add_patch(FancyBboxPatch((55, 30), 35, 18, boxstyle="round,pad=0.8", facecolor=TSMC_RED, ec='none'))
    ax.text(72.5, 44, 'TSMC', fontsize=20, fontweight='bold', ha='center', va='center', color='white', fontfamily=FONT)
    ax.text(72.5, 39, 'Taiwan | 90% of all <7nm chips', fontsize=7.5, ha='center', va='center', color=(1,1,1,0.85), fontfamily=FONT)
    ax.text(72.5, 35.5, '$27B quarterly revenue', fontsize=7.5, ha='center', va='center', color=(1,1,1,0.85), fontfamily=FONT)

    # Single point of failure
    ax.add_patch(FancyBboxPatch((93, 50), 27, 6, boxstyle="round,pad=0.4", facecolor='#FEF3C7', ec='#F59E0B', lw=0.8))
    ax.text(93.5, 54.2, '!', fontsize=12, fontweight='bold', ha='center', va='center', color=TSMC_RED, fontfamily=FONT)
    ax.text(106.5, 54, 'Single Point of Failure', fontsize=7.5, fontweight='bold', ha='center', va='center', color='#92400E', fontfamily=FONT)
    ax.text(106.5, 51.3, '160 km from Chinese coast', fontsize=6.5, ha='center', va='center', color='#B45309', fontfamily=FONT)

    labs = [('OpenAI / Microsoft','#412991',56),('Google DeepMind','#4285F4',48),
            ('Amazon AWS','#FF9900',40),('Meta AI','#0668E1',32),('xAI (Musk)','#555',24)]
    for name, col, y in labs:
        ax.add_patch(FancyBboxPatch((126, y-2.2), 27, 5.5, boxstyle="round,pad=0.5", facecolor=col, ec='none', alpha=0.9))
        ax.text(139.5, y, name, fontsize=8, fontweight='bold', ha='center', va='center', color='white', fontfamily=FONT)

    # Arrows
    for _,_,_,y in designers:
        ax.annotate('', xy=(55, 39), xytext=(30, y), arrowprops=dict(arrowstyle='->', color='#BBB', lw=0.8, connectionstyle='arc3,rad=0.05'))
    ax.text(42, 52, 'Design', fontsize=7, ha='center', color=GR, fontfamily=FONT, style='italic')
    for _,_,y in labs:
        ax.annotate('', xy=(126, y), xytext=(91, 39), arrowprops=dict(arrowstyle='->', color='#BBB', lw=0.8, connectionstyle='arc3,rad=-0.05'))
    ax.text(110, 42, 'finished chips', fontsize=7, ha='center', color=GR, fontfamily=FONT, style='italic')

    # ASML
    ax.add_patch(FancyBboxPatch((50, 14), 45, 7, boxstyle="round,pad=0.5", facecolor='#FEF3C7', ec='#F59E0B', lw=0.8))
    ax.text(72.5, 19, 'ASML — EUV Lithography', fontsize=9, fontweight='bold', ha='center', va='center', color='#92400E', fontfamily=FONT)
    ax.text(72.5, 15.8, 'Sole manufacturer worldwide | EUR 28B/year', fontsize=7, ha='center', va='center', color='#B45309', fontfamily=FONT)
    ax.annotate('', xy=(72.5, 30), xytext=(72.5, 22), arrowprops=dict(arrowstyle='->', color='#AAA', lw=0.8, ls='dashed'))

    # Stats bar
    ax.add_patch(FancyBboxPatch((5, 2), 150, 7, boxstyle="round,pad=0.5", facecolor='#EEE', ec='#DDD', lw=0.6))
    for label, val, sub, cx in [('TSMC Market Share','~90%','for <7nm chips',35),
                                  ('ASML EUV Market Share','100%','no competitor',80),
                                  ('Distance Taiwan-China','160 km','Taiwan Strait',125)]:
        ax.text(cx, 7.5, label, fontsize=6.5, fontweight='bold', ha='center', color=TSMC_RED, fontfamily=FONT)
        ax.text(cx, 5, val, fontsize=12, fontweight='bold', ha='center', color=DK, fontfamily=FONT)
        ax.text(cx, 3, sub, fontsize=6, ha='center', color=GR, fontfamily=FONT)

    save(fig, '13-chip-war-en.png')

# ===== 24. RISK MATRIX =====
def build_risk_matrix():
    fig, ax = plt.subplots(figsize=(10, 8.0))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(-5, 105); ax.set_ylim(-12, 105); ax.set_aspect('equal'); ax.axis('off')

    fig.text(0.5, 0.97, 'Risk Matrix: What Can Go Wrong?', fontsize=22, fontweight='bold',
             ha='center', va='top', color=DK, fontfamily=FONT)
    fig.text(0.5, 0.925, 'Probability vs. Impact — and how to protect yourself',
             fontsize=10, ha='center', va='top', color=GR, fontfamily=FONT)

    # Quadrant fills
    ax.fill([0,50,50,0],[50,50,100,100], color='#FEF9E7', alpha=0.4)
    ax.fill([50,100,100,50],[50,50,100,100], color='#FDEDEC', alpha=0.4)
    ax.fill([0,50,50,0],[0,0,50,50], color='#FAFAFA', alpha=0.4)
    ax.fill([50,100,100,50],[0,0,50,50], color='#FEF5E7', alpha=0.4)

    ax.plot([0,100],[50,50],'--',color='#DDD',lw=0.8)
    ax.plot([50,50],[0,100],'--',color='#DDD',lw=0.8)
    ax.plot([0,100],[0,0],'-',color='#AAA',lw=1.2)
    ax.plot([0,0],[0,100],'-',color='#AAA',lw=1.2)

    # Quadrant labels
    ax.text(25, 97, 'PLAN', fontsize=11, fontweight='bold', ha='center', color='#D4AC0D', fontfamily=FONT)
    ax.text(75, 97, 'ACT', fontsize=11, fontweight='bold', ha='center', color='#C0392B', fontfamily=FONT)
    ax.text(25, 3, 'MONITOR', fontsize=11, fontweight='bold', ha='center', color='#D4AC0D', fontfamily=FONT)
    ax.text(75, 3, 'HEDGE', fontsize=11, fontweight='bold', ha='center', color='#C0392B', fontfamily=FONT)

    # Axis labels — well separated
    fig.text(0.5, 0.04, 'Probability  \u2192', fontsize=12, fontweight='bold', ha='center', color=DK, fontfamily=FONT)
    fig.text(0.06, 0.5, 'Impact  \u2191', fontsize=12, fontweight='bold', ha='center', va='center',
             color=DK, fontfamily=FONT, rotation=90)

    # Tick labels
    ax.text(0, -4, 'Low', fontsize=8, ha='center', color=GR, fontfamily=FONT)
    ax.text(50, -4, 'Medium', fontsize=8, ha='center', color=GR, fontfamily=FONT)
    ax.text(100, -4, 'High', fontsize=8, ha='center', color=GR, fontfamily=FONT)
    ax.text(-3.5, 0, 'Low', fontsize=8, ha='right', va='center', color=GR, fontfamily=FONT)
    ax.text(-3.5, 50, 'Med.', fontsize=8, ha='right', va='center', color=GR, fontfamily=FONT)
    ax.text(-3.5, 100, 'High', fontsize=8, ha='right', va='center', color=GR, fontfamily=FONT)

    # Bubbles
    bubbles = [
        (12, 88, 6.5, '#C5D5F0', 'Black Swan', 'War, pandemic,\nTSMC outage', DK),
        (22, 72, 5.8, '#C5D5F0', 'AI Winter', 'Technical\nsetback', DK),
        (42, 70, 6.2, '#E8C8A0', 'Social\nInstability', 'Mass unemployment,\nsocial unrest', DK),
        (62, 65, 5.2, '#E8C8A0', 'Energy\nCrunch', 'Not enough\npower', DK),
        (40, 48, 5.2, '#E8C8A0', 'Regulation', 'EU/U.S. bans,\ncrypto crackdown', DK),
        (78, 48, 7.0, '#F0C0C0', 'Valuation\nCrash', 'AI bubble bursts,\n-50-70% correction', '#8B0000'),
        (68, 22, 5.2, '#D8D8D0', 'Crypto\nHacks', 'Individual losses,\nnot systemic', DK),
    ]
    for x, y, r, col, name, sub, tcol in bubbles:
        ax.add_patch(plt.Circle((x, y), r, color=col, alpha=0.7, ec='none', zorder=3))
        ax.text(x, y+1.5, name, fontsize=9, fontweight='bold', ha='center', va='center',
                color=tcol, fontfamily=FONT, linespacing=1.05, zorder=4)
        ax.text(x, y-2.5, sub, fontsize=6.5, ha='center', va='center',
                color=GR, fontfamily=FONT, linespacing=1.1, zorder=4)

    fig.text(0.5, 0.015, 'Bubble size = uncertainty of estimate. Positioning based on scenarios in Ch. 10 + 15.',
             fontsize=8, ha='center', color=GR, fontfamily=FONT, style='italic')

    save(fig, '24-risk-matrix-en.png')


# === RUN ALL ===
print("Building v3 graphics...")
build_convergence()
build_four_phases()
build_machine_bank()
build_chip_war()
build_risk_matrix()
print("ALL 5 DONE")
