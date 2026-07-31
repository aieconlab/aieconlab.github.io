#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그림 2: 미국 정보처리장비 투자 — 명목은 늘고 실질은 덜 늘었다.

자료: BEA 국민소득생산계정(NIPA) 2026년 2분기 속보치(2026-07-30 공표).
  - 실질 증가율(전기비 연율): 표 1.5.1, 계열 Y034RL
  - 가격지수(2017=100):       표 1.5.4, 계열 Y034RG
  - 명목 수준(백만 달러):      표 1.5.5, 계열 Y034RC
명목 증가율은 표 1.5.5의 수준에서 필자가 계산했다(전기비 연율 = (x_t/x_{t-1})^4 - 1).

원자료: ../data/Section1All_xls.xlsx → ../data/bea_extract.csv (extract_bea.py)

사용법: python3 fig02_nominal_real_gap.py [--out PNG] [--font FONT]
의존성: matplotlib
인터프리터: /opt/anaconda3/bin/python3
"""
import argparse
import csv
from collections import defaultdict
from math import log
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
CSV = HERE / ".." / "data" / "bea_extract.csv"
BLUE, NAVY, GRAY, NOTE, SPINE = "#2563eb", "#1b2a4a", "#8290a6", "#5a6472", "#c8cdd6"
AMBER = "#d97706"

# 2023Q4는 2024Q1의 전기비를 계산하기 위한 기준 분기이며 그림에는 그리지 않는다
ALL_QUARTERS = ["2023Q4"] + [f"{y}Q{q}" for y in (2024, 2025, 2026) for q in range(1, 5)]
QUARTERS = ALL_QUARTERS[1:]


def load():
    d = defaultdict(dict)
    with open(CSV, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d[r["code"]][r["quarter"]] = float(r["value"])
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "out" / "fig02_nominal_real_gap.png")
    ap.add_argument("--font", default="Apple SD Gothic Neo")
    a = ap.parse_args()

    d = load()
    qs = [q for q in QUARTERS if q in d["Y034RC"]]
    nominal, real, price = [], [], []
    for q in qs:
        prev = ALL_QUARTERS[ALL_QUARTERS.index(q) - 1]
        nominal.append(((d["Y034RC"][q] / d["Y034RC"][prev]) ** 4 - 1) * 100)
        real.append(d["Y034RL"][q])
        # 가격지수(Y034RG) 전기비 연율 — 라벨에 하드코딩하지 않고 자료에서 계산한다
        price.append(((d["Y034RG"][q] / d["Y034RG"][prev]) ** 4 - 1) * 100)

    # --- 검산 (BEA 공표치와 대조) ---------------------------------------
    assert qs[-1] == "2026Q2", qs[-1]
    assert abs(real[-1] - 8.3) < 0.05, real[-1]          # 표 1.5.1 공표치
    assert abs(real[-2] - 39.9) < 0.05, real[-2]
    assert abs(nominal[-1] - 22.5) < 0.15, nominal[-1]   # 필자 계산
    assert abs(nominal[-2] - 50.8) < 0.15, nominal[-2]
    assert nominal[-1] > real[-1]                        # 2분기는 명목 > 실질
    gap = nominal[-1] - real[-1]
    assert 13.5 < gap < 14.8, gap
    assert abs(price[-1] - 13.1) < 0.15, price[-1]   # 본문 '연율 13.1%'
    assert abs(price[-2] - 7.8) < 0.15, price[-2]    # 본문 '1분기 7.8%'
    # 명목 배수 = 실질 배수 x 가격 배수 (항등식 검산)
    assert abs((1 + real[-1] / 100) * (1 + price[-1] / 100)
               - (1 + nominal[-1] / 100)) < 2e-3, (real[-1], price[-1], nominal[-1])
    # 로그 분해로 본 가격의 몫 — 본문의 '약 60%'와 일치해야 한다
    price_share = log(1 + price[-1] / 100) / log(1 + nominal[-1] / 100) * 100
    assert 59.5 < price_share < 61.5, price_share

    plt.rcParams["font.family"] = a.font
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(10, 6.0), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    x = list(range(len(qs)))
    ax.fill_between(x, real, nominal, where=[n >= r for n, r in zip(nominal, real)],
                    color=AMBER, alpha=0.16, zorder=2, interpolate=True)
    ax.plot(x, nominal, color=NAVY, lw=2.6, marker="o", ms=5.5, zorder=4, label="명목")
    ax.plot(x, real, color=BLUE, lw=2.6, marker="o", ms=5.5, zorder=4, label="실질")

    ax.annotate("명목", (x[-1], nominal[-1]), xytext=(10, 2), textcoords="offset points",
                fontsize=12.5, color=NAVY, fontweight="bold", va="center")
    ax.annotate("실질", (x[-1], real[-1]), xytext=(10, -2), textcoords="offset points",
                fontsize=12.5, color=BLUE, fontweight="bold", va="center")

    for v, c in ((nominal[-1], NAVY), (real[-1], BLUE)):
        ax.text(x[-1] + 0.10, v + 3.4, f"{v:.1f}%", ha="left", fontsize=12,
                color=c, fontweight="bold", zorder=5)

    # 2026Q2 간격 표시
    ax.annotate("", xy=(x[-1] - 0.34, nominal[-1]), xytext=(x[-1] - 0.34, real[-1]),
                arrowprops=dict(arrowstyle="<->", color=AMBER, lw=1.7), zorder=5)
    ax.text(x[-1] - 0.46, (nominal[-1] + real[-1]) / 2,
            # U+2212(−)는 Apple SD Gothic Neo에 글리프가 없어 두부로 렌더된다. 표기로 대체.
            f"명목과 실질의 격차\n{gap:.1f}%p\n(가격 연율 {price[-1]:.1f}%)", ha="right", va="center",
            fontsize=11.5, color=AMBER, fontweight="bold", zorder=5)

    ax.axhline(0, color=SPINE, lw=1)
    ax.set_xticks(x)
    ax.set_xticklabels([q.replace("Q", "\nQ") if q.endswith("Q1") else "Q" + q[-1] for q in qs],
                       fontsize=10.5, color=NOTE)
    ax.set_ylabel("전 분기 대비 연율(%)", fontsize=11.5, color=NOTE, labelpad=18)
    ax.set_ylim(-8, 72)
    ax.set_yticks([0, 20, 40, 60])
    ax.tick_params(axis="y", labelsize=11, colors=NOTE, length=0)
    ax.tick_params(axis="x", length=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(SPINE)
    ax.grid(axis="y", color=SPINE, lw=0.6, alpha=0.5, zorder=1)
    ax.set_axisbelow(True)

    ax.set_title("같은 지출, 다른 기록: 미국 정보처리장비 투자의 명목과 실질",
                 fontsize=15.5, color=NAVY, fontweight="bold", loc="left", pad=16)

    fig.text(0.075, 0.045,
             "명목 증가율은 BEA 표 1.5.5의 명목 수준에서 필자가 계산했고, 실질 증가율은 표 1.5.1의 공표치다.\n"
             f"격차 {gap:.1f}%p는 두 증가율의 산술 차이이며, 가격지수 자체의 상승률은 연율 {price[-1]:.1f}%다.",
             fontsize=9.5, color=NOTE, linespacing=1.7)

    fig.subplots_adjust(left=0.115, right=0.925, top=0.84, bottom=0.19)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.out, dpi=200, facecolor="white", metadata={"Date": None})
    print("wrote", a.out)
    print(f"2026Q2  명목 {nominal[-1]:.2f}%  실질 {real[-1]:.1f}%  가격 {price[-1]:.2f}%  "
          f"격차 {gap:.2f}%p  로그 가격 몫 {price_share:.1f}%")


if __name__ == "__main__":
    main()
