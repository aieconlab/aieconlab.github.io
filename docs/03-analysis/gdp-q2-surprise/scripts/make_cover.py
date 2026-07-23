#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""커버 이미지(1600x800) 생성. 사용법: python3 make_cover.py [--out PNG] [--font FONT]"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--out", type=Path, default=HERE / "out" / "trend13_cover.png")
ap.add_argument("--font", default="Apple SD Gothic Neo")
args = ap.parse_args()

plt.rcParams["font.family"] = args.font
plt.rcParams["axes.unicode_minus"] = False

NAVY = "#1b2a4a"
BLUE = "#2563eb"
GRAY = "#4b5563"
LGRAY = "#6b7280"
STEPGRAY = "#cbd5e1"

fig = plt.figure(figsize=(16, 8), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1600)
ax.set_ylim(0, 800)
ax.axis("off")
ax.set_facecolor("white")
fig.patch.set_facecolor("white")

# top blue bar
ax.add_patch(Rectangle((0, 760), 1600, 40, color=BLUE, zorder=5))

# ---- left text column ----
LX = 183
ax.text(LX, 555, "0.2%가 0.6%가 됐다", fontsize=42, color=NAVY,
        fontweight="bold", va="center", ha="left")
ax.text(LX, 442, "2분기 깜짝 성장은 ‘AI 경제’의 실증인가", fontsize=21,
        color=BLUE, va="center", ha="left", fontweight="medium")

ax.text(LX, 300, "한국은행이 전망한 0.2%는 0.6%로 돌아왔다\n"
                 "반도체가 끌어올린 성장과 소득, 그 산수와 남는 질문",
        fontsize=16.5, color=GRAY, va="center", ha="left", linespacing=1.9)

ax.text(LX, 185, "2026년 2분기 GDP 속보 읽기", fontsize=14,
        color=LGRAY, va="center", ha="left")

ax.text(LX, 78, "AIEconLab · 인공지능경제연구소", fontsize=15.5,
        color=BLUE, va="center", ha="left", fontweight="medium")

# ---- right graphic: forecast bar vs actual bar ----
ax.text(1190, 668, "2분기 전기비 성장률", fontsize=16, color=GRAY,
        ha="center", va="center")

base_y = 150
SCALE = 700  # height per 1%p
bx1, bx2 = 985, 1245
bw = 150

h_fcst = 0.2 / 100 * SCALE * 100   # 0.2% -> 140px
h_act = 0.6 / 100 * SCALE * 100    # 0.6% -> 420px

ax.add_patch(Rectangle((bx1, base_y), bw, h_fcst, color=STEPGRAY, zorder=3))
ax.add_patch(Rectangle((bx2, base_y), bw, h_act, color=BLUE, zorder=3))

# baseline
ax.plot([bx1 - 55, bx2 + bw + 55], [base_y, base_y],
        color="#9ca3af", lw=1.2, zorder=2)

# dashed line carrying the forecast height across the actual bar
ax.plot([bx1 - 40, bx2 + bw + 30], [base_y + h_fcst, base_y + h_fcst],
        color=NAVY, lw=1.6, ls=(0, (5, 4)), zorder=4)

# labels on bars
ax.text(bx1 + bw / 2, base_y + h_fcst + 34, "5월 전망\n0.2%", fontsize=16,
        color=GRAY, ha="center", va="bottom", linespacing=1.5)
ax.text(bx2 + bw / 2, base_y + h_act + 34, "속보 0.6%", fontsize=18,
        color=BLUE, ha="center", va="bottom", fontweight="bold")

# gap arrow between forecast height and actual height on the actual bar
ax.annotate("", xy=(bx2 + bw + 44, base_y + h_act),
            xytext=(bx2 + bw + 44, base_y + h_fcst),
            arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.6), zorder=5)
ax.text(bx2 + bw + 62, base_y + (h_fcst + h_act) / 2, "3배", fontsize=16,
        color=BLUE, ha="left", va="center", fontweight="bold")

args.out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(args.out)
print("wrote", args.out)
