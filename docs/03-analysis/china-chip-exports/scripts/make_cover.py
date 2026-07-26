#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""trend15 커버 이미지(1600x800) 생성. 사용법: python3 make_cover.py [--out PNG] [--font FONT]

우측 그래픽 수치(중국 해관총서 (5) 수량·금액표 2026년 6월판, 달러 기준, 2026년 상반기 YoY):
- 집적회로 수출 금액 +96.1%
- 집적회로 수출 수량(개수) +7.0%
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--out", type=Path, default=HERE / "out" / "trend15_cover.png")
ap.add_argument("--font", default="Apple SD Gothic Neo")
args = ap.parse_args()

plt.rcParams["font.family"] = args.font
plt.rcParams["axes.unicode_minus"] = False

NAVY = "#1b2a4a"
BLUE = "#2563eb"
GRAY = "#4b5563"
LGRAY = "#6b7280"
STEPGRAY = "#cbd5e1"

VALUE_YOY, VOLUME_YOY = 96.1, 7.0
assert VALUE_YOY == 96.1 and VOLUME_YOY == 7.0

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
    ax.text(LX, 555, "금액 +96%, 개수 +7%", fontsize=42, color=NAVY,
            fontweight="bold", va="center", ha="left"),
    ax.text(LX, 442, "중국 반도체 수출 통계를 읽는 세 개의 잣대", fontsize=21,
            color=BLUE, va="center", ha="left", fontweight="medium"),
    ax.text(LX, 300, "수출액 96.1% 증가의 90%는 개당 단가가 설명\n"
                     "개수·중량·물량지수, 잣대마다 다른 ‘물량’의 답",
            fontsize=16.5, color=GRAY, va="center", ha="left", linespacing=1.9),
    ax.text(LX, 185, "2026년 상반기 중국 해관총서 통계 읽기", fontsize=14,
            color=LGRAY, va="center", ha="left"),
    ax.text(LX, 78, "AIEconLab · 인공지능경제연구소", fontsize=15.5,
            color=BLUE, va="center", ha="left", fontweight="medium"),
]

# ---- right graphic: value vs volume growth, same axis ----
ax.text(1190, 706, "집적회로 수출 증가율 (2026년 상반기, %)", fontsize=16, color=GRAY,
        ha="center", va="center")

base_y = 150
PX_PER_PCT = 420.0 / 96.1  # +96.1% -> 420px
bx1, bx2 = 985, 1245
bw = 150

h_value = VALUE_YOY * PX_PER_PCT
h_volume = VOLUME_YOY * PX_PER_PCT

ax.add_patch(Rectangle((bx1, base_y), bw, h_value, color=BLUE, zorder=3))
ax.add_patch(Rectangle((bx2, base_y), bw, h_volume, color=STEPGRAY, zorder=3))

# baseline
ax.plot([bx1 - 55, bx2 + bw + 55], [base_y, base_y],
        color="#9ca3af", lw=1.2, zorder=2)

# labels on bars
ax.text(bx1 + bw / 2, base_y + h_value + 34, "금액\n+96.1%", fontsize=18,
        color=BLUE, ha="center", va="bottom", fontweight="bold", linespacing=1.4)
ax.text(bx2 + bw / 2, base_y + h_volume + 34, "개수\n+7.0%", fontsize=16,
        color=GRAY, ha="center", va="bottom", linespacing=1.5)

# 렌더링 후 잘림·침범 검사: 좌측 텍스트가 우측 그래픽 영역(x=930~)을 넘지 않는지
fig.canvas.draw()
rend = fig.canvas.get_renderer()
for t in left_texts:
    x1 = t.get_window_extent(renderer=rend).x1
    assert x1 < 930, ("좌측 텍스트가 그래픽 영역 침범", t.get_text()[:14], round(x1))
print("layout checks passed: left column clear of graphic area")

args.out.parent.mkdir(parents=True, exist_ok=True)
# 실행시각(Date) 메타데이터를 제거한다. 바이트·픽셀 재현성 기준은 분석 README 참조
fig.savefig(args.out, metadata={"Date": None})
print("wrote", args.out)
