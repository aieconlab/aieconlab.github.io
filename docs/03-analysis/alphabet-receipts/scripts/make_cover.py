#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""trend14 커버 이미지(1600x800) 생성. 사용법: python3 make_cover.py [--out PNG] [--font FONT]

우측 그래픽 수치(알파벳 분기 설비투자, 현금흐름표 '유형자산 취득'):
- 2025년 2분기 22,446백만 달러 -> 224억 달러
- 2026년 2분기 44,924백만 달러 -> 449억 달러 (전년 동기의 2.00배)
자료: 알파벳 2026년 2분기 실적 발표문(2026-07-22) 현금흐름표.
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--out", type=Path, default=HERE / "out" / "trend14_cover.png")
ap.add_argument("--font", default="Apple SD Gothic Neo")
args = ap.parse_args()

plt.rcParams["font.family"] = args.font
plt.rcParams["axes.unicode_minus"] = False

NAVY = "#1b2a4a"
BLUE = "#2563eb"
GRAY = "#4b5563"
LGRAY = "#6b7280"
STEPGRAY = "#cbd5e1"

# 검산: 표기 수치와 원자료(백만 달러)의 정합
CAPEX_2025Q2_M, CAPEX_2026Q2_M = 22_446, 44_924
assert round(CAPEX_2025Q2_M / 100) == 224
assert round(CAPEX_2026Q2_M / 100) == 449
assert abs(CAPEX_2026Q2_M / CAPEX_2025Q2_M - 2.0) < 0.01

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
left_texts = [
    ax.text(LX, 555, "이익 +298%, 주가 -7%", fontsize=42, color=NAVY,
            fontweight="bold", va="center", ha="left"),
    ax.text(LX, 442, "알파벳 2분기, ‘AI 영수증’ 읽기", fontsize=21,
            color=BLUE, va="center", ha="left", fontweight="medium"),
    ax.text(LX, 300, "사상 최대 순이익의 대부분은 영업 밖 지분 평가이익\n"
                     "분기 잉여현금흐름은 상장 후 첫 마이너스(FactSet 집계)",
            fontsize=16.5, color=GRAY, va="center", ha="left", linespacing=1.9),
    ax.text(LX, 185, "2026년 2분기 알파벳 실적 읽기", fontsize=14,
            color=LGRAY, va="center", ha="left"),
    ax.text(LX, 78, "AIEconLab · 인공지능경제연구소", fontsize=15.5,
            color=BLUE, va="center", ha="left", fontweight="medium"),
]

# ---- right graphic: quarterly capex, doubled in a year ----
ax.text(1190, 706, "분기 설비투자 (억 달러)", fontsize=16, color=GRAY,
        ha="center", va="center")

base_y = 150
PX_PER_100M = 420.0 / 449.0  # 449억 달러 -> 420px
bx1, bx2 = 985, 1245
bw = 150

h_prev = 224 * PX_PER_100M
h_now = 449 * PX_PER_100M

ax.add_patch(Rectangle((bx1, base_y), bw, h_prev, color=STEPGRAY, zorder=3))
ax.add_patch(Rectangle((bx2, base_y), bw, h_now, color=BLUE, zorder=3))

# baseline
ax.plot([bx1 - 55, bx2 + bw + 55], [base_y, base_y],
        color="#9ca3af", lw=1.2, zorder=2)

# dashed line carrying last year's height across this year's bar
ax.plot([bx1 - 40, bx2 + bw + 30], [base_y + h_prev, base_y + h_prev],
        color=NAVY, lw=1.6, ls=(0, (5, 4)), zorder=4)

# labels on bars
ax.text(bx1 + bw / 2, base_y + h_prev + 34, "2025년 2분기\n224", fontsize=16,
        color=GRAY, ha="center", va="bottom", linespacing=1.5)
ax.text(bx2 + bw / 2, base_y + h_now + 34, "2026년 2분기\n449", fontsize=18,
        color=BLUE, ha="center", va="bottom", fontweight="bold", linespacing=1.4)

# gap arrow between last year's height and this year's height
ax.annotate("", xy=(bx2 + bw + 44, base_y + h_now),
            xytext=(bx2 + bw + 44, base_y + h_prev),
            arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.6), zorder=5)
ax.text(bx2 + bw + 62, base_y + (h_prev + h_now) / 2, "2배", fontsize=16,
        color=BLUE, ha="left", va="center", fontweight="bold")

# 렌더링 후 잘림·침범 검사: 좌측 텍스트가 우측 그래픽 영역(x=930~)을 넘지 않는지
fig.canvas.draw()
rend = fig.canvas.get_renderer()
for t in left_texts:
    x1 = t.get_window_extent(renderer=rend).x1
    assert x1 < 930, ("좌측 텍스트가 그래픽 영역 침범", t.get_text()[:14], round(x1))
print("layout checks passed: left column clear of graphic area")

args.out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(args.out)
print("wrote", args.out)
