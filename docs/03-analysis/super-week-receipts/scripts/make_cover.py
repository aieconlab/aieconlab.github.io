#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""trend17 커버 이미지(1600x800) 생성. 사용법: python3 make_cover.py [--out PNG] [--font FONT]

우측 그래픽 수치(BEA 국민소득생산계정 2026년 2분기 속보치, 정보처리장비 투자,
전 분기 대비 연율):
- 명목 +22.5% (표 1.5.5 명목 수준에서 계산)
- 실질  +8.3% (표 1.5.1 공표치)
"""
import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--out", type=Path, default=HERE / "out" / "trend17_cover.png")
ap.add_argument("--font", default="Apple SD Gothic Neo")
args = ap.parse_args()

plt.rcParams["font.family"] = args.font
plt.rcParams["axes.unicode_minus"] = False

NAVY = "#1b2a4a"
BLUE = "#2563eb"
GRAY = "#4b5563"
LGRAY = "#6b7280"
STEPGRAY = "#cbd5e1"

# 표시값은 하드코딩하지 않고 extract_bea.py가 만든 CSV에서 계산·대조한다
_d = defaultdict(dict)
with open(HERE / ".." / "data" / "bea_extract.csv", encoding="utf-8") as _fh:
    for _r in csv.DictReader(_fh):
        _d[_r["code"]][_r["quarter"]] = float(_r["value"])
NOMINAL = round(((_d["Y034RC"]["2026Q2"] / _d["Y034RC"]["2026Q1"]) ** 4 - 1) * 100, 1)
REAL = round(_d["Y034RL"]["2026Q2"], 1)
CONTRIB_Q1 = _d["Y034RY"]["2026Q1"]
CONTRIB_Q2 = _d["Y034RY"]["2026Q2"]
assert (NOMINAL, REAL) == (22.5, 8.3), (NOMINAL, REAL)
assert (round(CONTRIB_Q1, 2), round(CONTRIB_Q2, 2)) == (0.77, 0.19), (CONTRIB_Q1, CONTRIB_Q2)

fig = plt.figure(figsize=(16, 8), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1600)
ax.set_ylim(0, 800)
ax.axis("off")
ax.set_facecolor("white")
fig.patch.set_facecolor("white")

ax.add_patch(Rectangle((0, 760), 1600, 40, color=BLUE, zorder=5))

# ---- 좌측 텍스트 ----
LX = 183
left_texts = [
    ax.text(LX, 555, f"명목 {NOMINAL}%, 실질 {REAL}%", fontsize=42, color=NAVY,
            fontweight="bold", va="center", ha="left"),
    ax.text(LX, 442, "‘AI 투자’를 세는 숫자는 왜 서로 다른가", fontsize=21,
            color=BLUE, va="center", ha="left", fontweight="medium"),
    ax.text(LX, 300, f"미국 실질 GDP 성장에 대한 정보처리장비 기여\n{CONTRIB_Q1:.2f}%p → {CONTRIB_Q2:.2f}%p (2026Q1→Q2)\n"
                     "기업 공시·공급자 매출·국민계정은 다른 것을 잰다",
            fontsize=16.5, color=GRAY, va="center", ha="left", linespacing=1.9),
    ax.text(LX, 185, "SK하이닉스·FOMC·메타·MS·미국 2분기 GDP 결산", fontsize=14,
            color=LGRAY, va="center", ha="left"),
    ax.text(LX, 78, "AIEconLab · 인공지능경제연구소", fontsize=15.5,
            color=BLUE, va="center", ha="left", fontweight="medium"),
]

# ---- 우측 그래픽: 같은 축 위의 명목·실질 ----
ax.text(1190, 706, "미국 정보처리장비 투자 증가율 (2026년 2분기, 전 분기 대비 연율 %)",
        fontsize=15, color=GRAY, ha="center", va="center")

base_y = 150
PX_PER_PCT = 420.0 / NOMINAL
bx1, bx2 = 985, 1245
bw = 150

h_nom = NOMINAL * PX_PER_PCT
h_real = REAL * PX_PER_PCT

ax.add_patch(Rectangle((bx1, base_y), bw, h_nom, color=BLUE, zorder=3))
ax.add_patch(Rectangle((bx2, base_y), bw, h_real, color=STEPGRAY, zorder=3))
ax.plot([bx1 - 55, bx2 + bw + 55], [base_y, base_y], color="#9ca3af", lw=1.2, zorder=2)

ax.text(bx1 + bw / 2, base_y + h_nom + 34, f"명목\n+{NOMINAL}%", fontsize=18,
        color=BLUE, ha="center", va="bottom", fontweight="bold", linespacing=1.4)
ax.text(bx2 + bw / 2, base_y + h_real + 34, f"실질\n+{REAL}%", fontsize=16,
        color=GRAY, ha="center", va="bottom", linespacing=1.5)

# 렌더링 후 침범 검사: 좌측 텍스트가 우측 그래픽 영역(x=930~)을 넘지 않는지
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
