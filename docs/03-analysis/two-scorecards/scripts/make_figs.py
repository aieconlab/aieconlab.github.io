#!/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""
trend20 '성적표 두 장' 그림 생성 스크립트.

입력: ../data/*.csv (FRED, 취득 대장은 ../data/_fetch_log.txt)
출력: 본문 그림 3종은 ../../../../static/images/post/two_scorecards/ (관례: 본문 그림은
      static, 표지는 assets), 표지는 ../../../../assets/images/post/trend20_cover.png
파일명은 본문 그림 번호와 일치한다: fig01_productivity=그림 1, fig02_payrolls=그림 2,
fig03_laborshare=그림 3.
모바일 가독성: 폭 7.2인치에 축 글자 14pt·주석 15pt 이상, 축 눈금 4~7개.
수치 검증은 verify_claims.py가 담당한다(이 스크립트는 그림 생성 전용).
재현성: savefig(metadata={"Date": None}), 생성 인터프리터 /opt/anaconda3/bin/python3
"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "..", "data")
OUT = os.path.join(BASE, "..", "..", "..", "..", "static", "images", "post", "two_scorecards")
COVER_OUT = os.path.join(BASE, "..", "..", "..", "..", "assets", "images", "post")
os.makedirs(OUT, exist_ok=True)

for cand in ["Apple SD Gothic Neo", "AppleGothic", "NanumGothic"]:
    if any(f.name == cand for f in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = cand
        break
plt.rcParams["axes.unicode_minus"] = False

GRAY = "#9AA5B1"
BLUE = "#2F5D8C"
DARK = "#1B3A5C"
RED = "#B4533A"
BAND = "#D9DEE4"


def load(name):
    rows = {}
    with open(os.path.join(DATA, name + ".csv")) as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            if len(row) < 2:
                continue
            try:
                rows[row[0]] = float(row[1])
            except ValueError:
                pass
    return rows


def ann_rate(cur, prev):
    return ((cur / prev) ** 4 - 1) * 100


pay = load("PAYEMS")
oph = load("OPHNFB")
out_ = load("OUTNFB")
hrs = load("HOANBS")
ls = load("PRS85006173")

q2, q1 = "2026-04-01", "2026-01-01"

# ---------- 그림 1: 생산성 (본문 그림 1, 세로 2단) ----------
all_q = sorted(oph)
qs = [d for d in all_q if d >= "2023-01-01"]
qlab = [f"{d[:4]}Q{(int(d[5:7]) - 1) // 3 + 1}" for d in qs]
qgr = [ann_rate(oph[d], oph[all_q[all_q.index(d) - 1]]) for d in qs]

fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.2, 8.6), gridspec_kw={"height_ratios": [1.15, 1]})
cols = [GRAY] * len(qgr)
cols[-1] = BLUE
a1.bar(range(len(qgr)), qgr, color=cols, width=0.68)
a1.axhline(0, color="#444444", lw=0.8)
a1.set_xticks(range(0, len(qgr), 2))
a1.set_xticklabels([qlab[i] for i in range(0, len(qgr), 2)], fontsize=14, rotation=45, ha="right")
a1.set_ylabel("전기 대비 연율 (%)", fontsize=16)
a1.yaxis.set_major_locator(plt.MaxNLocator(5))
a1.set_title("분기별 노동생산성 증가율", fontsize=16.5)
a1.annotate(f"2026Q2\n{qgr[-1]:+.1f}%", xy=(len(qgr) - 1, qgr[-1]), xytext=(len(qgr) - 5.4, 3.7),
            fontsize=15, color=BLUE, arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.9))
a1.spines[["top", "right"]].set_visible(False)
a1.tick_params(axis="y", labelsize=14)

dec = [ann_rate(out_[q2], out_[q1]), ann_rate(hrs[q2], hrs[q1]), ann_rate(oph[q2], oph[q1])]
names = ["산출", "노동시간", "생산성\n(산출/시간)"]
bars = a2.bar(names, dec, color=[BLUE, GRAY, DARK], width=0.58)
for b, v in zip(bars, dec):
    a2.text(b.get_x() + b.get_width() / 2, v + 0.06, f"{v:+.1f}%", ha="center", fontsize=15)
a2.axhline(0, color="#444444", lw=0.8)
a2.set_ylim(0, 2.3)
a2.set_title("2026년 2분기 예비치의 구성", fontsize=16.5)
a2.spines[["top", "right"]].set_visible(False)
a2.tick_params(labelsize=15)
a2.yaxis.set_major_locator(plt.MaxNLocator(5))
fig.suptitle("생산성 1.4%는 산출 증가가 노동시간 증가를 앞선 결과다", fontsize=17.5, y=0.985)
fig.tight_layout(rect=[0, 0, 1, 0.955])
fig.savefig(os.path.join(OUT, "fig01_productivity.png"), dpi=170, metadata={"Date": None})
plt.close(fig)

# ---------- 그림 2: 월별 일자리 증감 점추정치와 오차범위 (본문 그림 2) ----------
months = [d for d in sorted(pay) if "2025-07-01" <= d <= "2026-07-01"]
prev = {d: sorted(pay)[i - 1] for i, d in enumerate(sorted(pay))}
chg = [pay[d] - pay[prev[d]] for d in months]
labels = [f"{int(d[:4]) % 100}.{int(d[5:7])}" for d in months]

n_in = sum(1 for c in chg if abs(c) <= 122)
fig, ax = plt.subplots(figsize=(7.2, 5.8))
ax.axhspan(-122, 122, color=BAND, alpha=0.55, zorder=0)
colors = [RED if c < 0 else GRAY for c in chg]
colors[-1] = "#7A2E1D"
ax.bar(range(len(chg)), chg, color=colors, width=0.68, zorder=2)
ax.axhline(0, color="#444444", lw=0.8, zorder=3)
ax.annotate(f"2026년 7월\n{chg[-1] * 1000:+,.0f}개", xy=(len(chg) - 1, chg[-1]),
            xytext=(len(chg) - 4.6, -110), fontsize=15, color="#7A2E1D",
            arrowprops=dict(arrowstyle="-", color="#7A2E1D", lw=0.9), zorder=4)
ax.text(-0.45, 152, "음영: 오차한계 ±12만 2,000개를 적용할 때 신뢰구간이\n0을 포함하게 되는 점추정치의 범위", fontsize=13.5, color="#5B6673", va="center", zorder=4)
ax.set_xticks(range(0, len(chg), 2))
ax.set_xticklabels([labels[i] for i in range(0, len(chg), 2)], fontsize=14)
ax.set_ylabel("전월 대비 증감 (천 개)", fontsize=16)
ax.yaxis.set_major_locator(plt.MaxNLocator(5))
ax.set_title(f"현 오차한계 기준, 13개월 중 {n_in}개월은\n증감의 구간이 0을 포함했다", fontsize=16.5, pad=12)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(axis="y", labelsize=14)
ax.set_ylim(-175, 235)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig02_payrolls.png"), dpi=170, metadata={"Date": None})
plt.close(fig)

# ---------- 그림 3: 노동소득분배율 지수 (본문 그림 3) ----------
ds = sorted(ls)
xs = [int(d[:4]) + (int(d[5:7]) - 1) / 12 for d in ds]
fig, ax = plt.subplots(figsize=(7.2, 5.2))
ax.plot(xs, [ls[d] for d in ds], color=GRAY, lw=1.4)
ax.plot(xs[-1], ls[ds[-1]], "o", color=RED, ms=7)
ax.annotate(f"2026Q2 = {ls[ds[-1]]:.1f}\n1947년 집계 시작 이래 최저", xy=(xs[-1], ls[ds[-1]]),
            xytext=(1972, 97.2), fontsize=15, color=RED,
            arrowprops=dict(arrowstyle="-", color=RED, lw=0.9))
ax.set_ylabel("지수 (2017=100)", fontsize=16)
ax.yaxis.set_major_locator(plt.MaxNLocator(5))
ax.set_xticks([1950, 1975, 2000, 2025])
ax.set_title("미국 비농업 사업부문 노동소득분배율 지수", fontsize=17, pad=12)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(labelsize=14)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig03_laborshare.png"), dpi=170, metadata={"Date": None})
plt.close(fig)

# ---------- 표지 ----------
fig = plt.figure(figsize=(12, 6.3), facecolor="#122A44")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor("#122A44")
ax.axis("off")
ax.text(0.5, 0.80, "미국이 이틀 사이에 받은 성적표 두 장", ha="center", fontsize=27, color="#D8E1EA")
ax.text(0.28, 0.47, "+1.4%", ha="center", fontsize=64, color="#7FB2E5", fontweight="bold")
ax.text(0.28, 0.30, "2분기 비농업 사업부문 노동생산성\n(전기 대비 연율)", ha="center", fontsize=16, color="#9FB3C8")
ax.text(0.72, 0.47, "-2만 3,000개", ha="center", fontsize=52, color="#E5967F", fontweight="bold")
ax.text(0.72, 0.30, "7월 비농업 일자리 증감 점추정치\n(사업체조사)", ha="center", fontsize=16, color="#9FB3C8")
ax.text(0.5, 0.10, "자료: 미국 노동통계국(BLS) 2026. 8. 6.·8. 7. 발표", ha="center", fontsize=12, color="#6E8195")
fig.savefig(os.path.join(COVER_OUT, "trend20_cover.png"), dpi=140, metadata={"Date": None})
plt.close(fig)

print("figures written to", os.path.abspath(OUT))
