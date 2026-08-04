#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그림 2: 삼성전자+SK하이닉스 시가총액이 코스피 전체에서 차지한 몫, 이정표 열두 개.

자료: 언론 보도가 한국거래소 집계를 전재한 일자별 이정표를
data/cap_share_milestones.csv에 정리했다. 일별 연속 시계열이 아니라
보도로 확인된 날짜의 점들이다.

기준(basis) 구분:
- common_stated: 기사가 보통주(우선주 제외) 기준임을 명시
  (6/18 헤럴드경제: 우선주 포함 56.9% 병기 / 6/22 뉴시스: 우선주 제외 명시, 포함 시 58.08%)
- common_judged: 기사에 우선주 언급이 없고 삼성전자 시총 표기값이 보통주 시총과 일치해
  보통주 기준으로 판단

점 사이를 잇는 선은 파선(안내선)으로 그려 일별 연속 시계열이 아님을 드러낸다.

사용법: python3 fig02_cap_share.py [--out PNG] [--font FONT]
의존성: matplotlib
인터프리터: /opt/anaconda3/bin/python3
"""
import argparse
import csv
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
BLUE, NAVY, GRAY, NOTE, SPINE = "#2563eb", "#1b2a4a", "#8290a6", "#5a6472", "#c8cdd6"

rows = []
with open(HERE / ".." / "data" / "cap_share_milestones.csv", encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        rows.append({
            "date": datetime.strptime(r["date"], "%Y-%m-%d"),
            "share": float(r["share_pct"]),
            "basis": r["basis"],
            "label": r["label"],
        })

# --- 검산 -------------------------------------------------------------------
assert len(rows) == 12
assert rows == sorted(rows, key=lambda r: r["date"])
by = {r["date"].strftime("%Y-%m-%d"): r["share"] for r in rows}
assert by["2026-03-18"] == 40.61 and by["2026-05-27"] == 50.44
assert by["2026-07-28"] == 50.02 and by["2026-07-31"] == 51.23
# 40% 첫 돌파(3/18) 이전 점은 전부 40% 미만
assert all(r["share"] < 40 for r in rows if r["date"] < datetime(2026, 3, 18))
# 보도상 최고는 6/22 (뉴시스: 우선주 제외 기준 명시)
top = max(rows, key=lambda r: r["share"])
assert top["date"] == datetime(2026, 6, 22) and top["basis"] == "common_stated"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "out" / "fig02_cap_share.png")
    ap.add_argument("--font", default="Apple SD Gothic Neo")
    a = ap.parse_args()

    plt.rcParams["font.family"] = a.font
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(10, 5.8), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    xs = [r["date"] for r in rows]
    ys = [r["share"] for r in rows]
    # 파선 = 일별 연속 시계열이 아니라 이정표 점 사이의 안내선
    ax.plot(xs, ys, color=BLUE, lw=1.5, ls=(0, (4, 3)), alpha=0.85, zorder=3)
    for r in rows:
        ax.plot(r["date"], r["share"], "o", ms=7, color=BLUE, zorder=4)

    for lvl in (40, 50):
        ax.axhline(lvl, color=NAVY, lw=1, ls=(0, (4, 4)), zorder=2)

    ann = {
        "2025-12-30": ("2025년 말\n34.04%", (-8, -26)),
        "2026-03-18": ("3월 18일 40.61%\n(첫 40% 돌파, 보도 기준)", (-10, 12)),
        "2026-05-27": ("5월 27일 50.44%\n(첫 50% 돌파, 보도 기준)", (-84, 8)),
        "2026-06-22": ("6월 22일 55.67%\n(보도상 최고, 우선주 제외)", (-96, 10)),
        "2026-07-28": ("7월 28일\n50.02%", (6, -30)),
        "2026-07-31": ("7월 31일\n51.23%", (10, 2)),
    }
    for r in rows:
        key = r["date"].strftime("%Y-%m-%d")
        if key in ann:
            text, (dx, dy) = ann[key]
            ax.annotate(text, (r["date"], r["share"]), textcoords="offset points",
                        xytext=(dx, dy), fontsize=9.5, color=NAVY, zorder=5)

    ax.set_ylim(30, 60)
    ax.set_yticks([30, 35, 40, 45, 50, 55, 60])
    ax.set_yticklabels(["30", "35", "40", "45", "50", "55", "60%"],
                       fontsize=10.5, color=NOTE)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m월"))
    ax.tick_params(axis="x", labelsize=10.5, colors=NOTE, length=0)
    ax.tick_params(axis="y", length=0)

    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(SPINE)
    ax.spines["left"].set_color(SPINE)
    ax.grid(axis="y", color=SPINE, lw=0.6, alpha=0.5, zorder=1)
    ax.set_axisbelow(True)

    ax.set_title("삼성전자·SK하이닉스 시가총액이 코스피에서 차지한 몫: 일곱 달 이정표",
                 fontsize=15.5, color=NAVY, fontweight="bold", loc="left", pad=16)

    fig.text(0.065, 0.075,
             "언론이 한국거래소 집계를 전재한 날짜별 이정표. 파선은 점 사이를 이은 안내선일 뿐 "
             "일별 연속 시계열이 아니다.",
             fontsize=9.5, color=NOTE)
    fig.text(0.065, 0.035,
             "값은 보통주(우선주 제외) 기준으로, 6월 18일·22일 기사는 기준을 명시했고 "
             "나머지는 필자가 판단한 것이다.",
             fontsize=9.5, color=NOTE)

    fig.subplots_adjust(left=0.075, right=0.97, top=0.86, bottom=0.20)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.out, dpi=200, facecolor="white", metadata={"Date": None})
    print("wrote", a.out)


if __name__ == "__main__":
    main()
