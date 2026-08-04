#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그림 1: 월 수출에서 반도체가 차지한 몫, 2025년 7월~2026년 7월.

자료: 산업통상부 각 월 '수출입 동향' 발표치(통관 잠정치)를 언론·KDI 전재로 교차 확인해
data/monthly_semiconductor_exports.csv에 정리했다. 비중은 발표문에 없는 값으로,
각 월 [반도체 수출액 / 총수출액]을 필자가 계산했다.

주의:
- 2025년 12월 반도체 수출액은 발표·보도 모두 '208억 달러' 단위까지만 확인돼 근사값이다
  (approx_flag=1). 해당 막대는 그림에서 빗금으로 구분한다.
- 월별 잠정치의 합은 산업통상부가 발표한 상반기 누계와 약 14억 달러 어긋난다(확정치 반영
  추정). 이 그림은 월별 잠정치만 쓴다.
- 산업통상부는 2026-06-01부터 품목 분류(MTI)를 개편하고 2022년 이후 계열을 소급
  정비했다(2026-05-06 발표, 게시번호 171803). 이 시계열은 각 월 발표 당시 값을 이은
  것이라 개편 전후 정의가 완전히 같다고 보장할 수 없다. '처음 40% 돌파' 같은 판정은
  이 발표·보도 범위 안으로 한정된다.

사용법: python3 fig01_export_share.py [--out PNG] [--font FONT]
의존성: matplotlib
인터프리터: /opt/anaconda3/bin/python3
"""
import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
BLUE, NAVY, GRAY, NOTE, SPINE = "#2563eb", "#1b2a4a", "#8290a6", "#5a6472", "#c8cdd6"

rows = []
with open(HERE / ".." / "data" / "monthly_semiconductor_exports.csv", encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        rows.append({
            "month": r["month"],
            "total": float(r["total_export_100m_usd"]),
            "semis": float(r["semis_export_100m_usd"]),
            "approx": r["approx_flag"] == "1",
        })

for r in rows:
    r["share"] = r["semis"] / r["total"] * 100

# --- 검산 -------------------------------------------------------------------
by = {r["month"]: r for r in rows}
assert len(rows) == 13 and rows[0]["month"] == "2025-07" and rows[-1]["month"] == "2026-07"
assert round(by["2025-07"]["share"], 1) == 24.2, by["2025-07"]["share"]
assert round(by["2026-05"]["share"], 1) == 42.3, by["2026-05"]["share"]
assert round(by["2026-06"]["share"], 1) == 43.8, by["2026-06"]["share"]
assert round(by["2026-07"]["share"], 1) == 41.5, by["2026-07"]["share"]
# 40% 첫 돌파는 2026년 5월: 그 전 달까지는 전부 40% 미만
first_over_40 = next(r["month"] for r in rows if r["share"] >= 40)
assert first_over_40 == "2026-05", first_over_40
# 최고는 2026년 6월(7월이 역대 최대가 아님)
assert max(rows, key=lambda r: r["share"])["month"] == "2026-06"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "out" / "fig01_export_share.png")
    ap.add_argument("--font", default="Apple SD Gothic Neo")
    a = ap.parse_args()

    plt.rcParams["font.family"] = a.font
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(10, 5.8), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    x = list(range(len(rows)))
    for i, r in enumerate(rows):
        color = BLUE if r["share"] >= 40 else GRAY
        hatch = "///" if r["approx"] else None
        ax.bar(i, r["share"], width=0.62, color=color, hatch=hatch,
               edgecolor="white" if not r["approx"] else NOTE,
               linewidth=0.5, zorder=3)

    # 값 라벨: 시작, 40% 첫 돌파, 최고, 마지막
    marked = {"2025-07", "2026-05", "2026-06", "2026-07"}
    for i, r in enumerate(rows):
        if r["month"] in marked:
            ax.text(i, r["share"] + 0.9, f"{r['share']:.1f}%", ha="center",
                    fontsize=11.5, color=NAVY, fontweight="bold", zorder=5)

    ax.axhline(40, color=NAVY, lw=1, ls=(0, (4, 4)), zorder=2)
    ax.text(-0.45, 40.8, "40%", fontsize=10, color=NAVY)

    labels = []
    for r in rows:
        y, m = r["month"].split("-")
        labels.append(f"{y[2:]}.{int(m)}" if m in ("01", "07") else f"{int(m)}")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10.5, color=NOTE)
    ax.set_ylim(0, 50)
    ax.set_yticks([0, 10, 20, 30, 40, 50])
    ax.set_yticklabels(["0", "10", "20", "30", "40", "50%"], fontsize=10.5, color=NOTE)

    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(SPINE)
    ax.spines["left"].set_color(SPINE)
    ax.tick_params(length=0)
    ax.grid(axis="y", color=SPINE, lw=0.6, alpha=0.5, zorder=1)
    ax.set_axisbelow(True)

    ax.set_title("월 수출에서 반도체가 차지한 몫: 1년 만에 24.2%에서 41.5%로",
                 fontsize=15.5, color=NAVY, fontweight="bold", loc="left", pad=16)

    fig.text(0.065, 0.075,
             "비중은 각 월 수출입 동향(통관 잠정치)의 반도체 수출액을 총수출액으로 나눈 계산값. "
             "2025년 12월(빗금)은 반도체 수출액이 억 달러 단위(208억 달러)까지만 공표되어 근사값이다.",
             fontsize=9.5, color=NOTE)
    fig.text(0.065, 0.035,
             "품목 분류(MTI)는 2026년 6월 개편됐고 2022년 이후 계열이 소급 정비되어, "
             "개편 전후 정의가 완전히 같지 않을 수 있다.",
             fontsize=9.5, color=NOTE)

    fig.subplots_adjust(left=0.075, right=0.97, top=0.86, bottom=0.19)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.out, dpi=200, facecolor="white", metadata={"Date": None})
    print("wrote", a.out)
    for r in rows:
        print(r["month"], f"{r['share']:.2f}%", "(근사)" if r["approx"] else "")


if __name__ == "__main__":
    main()
