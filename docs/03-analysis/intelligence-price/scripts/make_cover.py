#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""trend16 커버 이미지(1600x800) 생성. 사용법: python3 make_cover.py [--out PNG] [--font FONT]

우측 그래픽 수치(집계사이트 Artificial Analysis 자체 측정, 2026-07-27 확인 —
data/aa_cost_per_task_rendered.txt):
- Claude Sonnet 5 (max): 출력 단가 $10 → 과제당 비용(Cost per Task) $1.53
- GPT-5.6 Sol (max):     출력 단가 $30 → 과제당 비용 $1.54
좌측 텍스트 수치: 단가 3배 차이가 과제당 1센트 차이. 7월 신모델(전작 비교 가능 3사)은
단가 동결 아니면 인상.
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--out", type=Path, default=HERE / "out" / "trend16_cover.png")
ap.add_argument("--font", default="Apple SD Gothic Neo")
args = ap.parse_args()

plt.rcParams["font.family"] = args.font
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["text.parse_math"] = False

NAVY = "#1b2a4a"
BLUE = "#2563eb"
GRAY = "#4b5563"
LGRAY = "#6b7280"
SPINE = "#cbd5e1"

P_SON, P_SOL = 10.0, 30.0          # 출력 단가($/1M)
C_SON, C_SOL = 1.53, 1.54          # 과제당 비용($, Cost per Task)
assert P_SOL / P_SON == 3.0 and abs(abs(C_SOL - C_SON) - 0.01) < 1e-9

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
LX = 130
left_texts = [
    ax.text(LX, 560, "토큰 단가와 과제 비용은\n다르다", fontsize=42, color=NAVY,
            fontweight="bold", va="center", ha="left", linespacing=1.35),
    ax.text(LX, 425, "AI 비용을 세는 두 가지 방법", fontsize=22,
            color=BLUE, va="center", ha="left", fontweight="medium"),
    ax.text(LX, 295, "출력 단가 3배인 모델, 과제당 비용은 1센트 차이\n"
                     "7월의 신모델들은 토큰 값을 내리지 않았다",
            fontsize=17, color=GRAY, va="center", ha="left", linespacing=1.9),
    ax.text(LX, 180, "2026년 7월, 모델 가격표와 과제당 비용 읽기", fontsize=14,
            color=LGRAY, va="center", ha="left"),
    ax.text(LX, 78, "AIEconLab · 인공지능경제연구소", fontsize=15.5,
            color=BLUE, va="center", ha="left", fontweight="medium"),
]

# ---- right graphic: 단가는 3배 차이, 과제당은 수렴 ----
gx1, gx2 = 1080, 1430
gy0, gy1 = 190, 620
for x in (gx1, gx2):
    ax.plot([x, x], [gy0, gy1], color=SPINE, lw=2.2, zorder=2)

y_son_l = gy0 + 70          # Sonnet 단가 $10 (아래)
y_sol_l = gy1 - 55          # Sol 단가 $30 (위)
y_son_r = (gy0 + gy1) / 2 - 16   # 과제당 $1.53 (수렴, 근소 아래)
y_sol_r = (gy0 + gy1) / 2 + 16   # 과제당 $1.54 (수렴, 근소 위)
ax.plot([gx1, gx2], [y_son_l, y_son_r], color=BLUE, lw=5.5, zorder=3,
        solid_capstyle="round")
ax.plot([gx1, gx2], [y_sol_l, y_sol_r], color=NAVY, lw=5.5, zorder=3,
        solid_capstyle="round")
for x, y, c in [(gx1, y_son_l, BLUE), (gx2, y_son_r, BLUE),
                (gx1, y_sol_l, NAVY), (gx2, y_sol_r, NAVY)]:
    ax.plot([x], [y], "o", ms=13, color=c, zorder=4)

right_texts = [
    ax.text((gx1 + gx2) / 2, 700, "출력 단가  vs  과제당 비용", fontsize=17,
            color=GRAY, ha="center", va="center"),
    ax.text(gx1 - 22, y_son_l, "Sonnet 5  $10", fontsize=15.5, color=BLUE,
            ha="right", va="center", fontweight="bold"),
    ax.text(gx1 - 22, y_sol_l, "Sol  $30", fontsize=15.5, color=NAVY,
            ha="right", va="center", fontweight="bold"),
    ax.text(gx2 + 22, y_son_r - 12, "$1.53", fontsize=16, color=BLUE,
            ha="left", va="center", fontweight="bold"),
    ax.text(gx2 + 22, y_sol_r + 12, "$1.54", fontsize=16, color=NAVY,
            ha="left", va="center", fontweight="bold"),
    ax.text((gx1 + gx2) / 2, 128, "자료: Artificial Analysis 과제당 비용(2026-07)",
            fontsize=12.5, color=LGRAY, ha="center", va="center"),
]

# ---- 레이아웃 검사: 잘림·겹침 ----
fig.canvas.draw()
rend = fig.canvas.get_renderer()
bb = lambda t: t.get_window_extent(renderer=rend)
W, Hpx = fig.canvas.get_width_height()
for t in left_texts + right_texts:
    assert bb(t).x1 <= W - 6, ("우측 잘림", t.get_text()[:14])
    assert bb(t).x0 >= 0, ("좌측 잘림", t.get_text()[:14])
    assert bb(t).y1 <= 760, ("상단 바 침범", t.get_text()[:14])
texts = left_texts + right_texts
for i in range(len(texts)):
    for j in range(i + 1, len(texts)):
        assert not bb(texts[i]).overlaps(bb(texts[j])), \
            ("텍스트 겹침", texts[i].get_text()[:12], texts[j].get_text()[:12])
left_right_edge = max(bb(t).x1 for t in left_texts)
graphic_left_edge = min(bb(t).x0 for t in right_texts)
assert graphic_left_edge - left_right_edge >= 30, ("좌우 블록 간격 부족",
                                                   left_right_edge, graphic_left_edge)
print("cover layout checks passed")

args.out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(args.out, dpi=100, facecolor="white", metadata={"Date": None})
print("wrote", args.out)
