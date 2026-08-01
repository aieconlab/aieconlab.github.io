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

    # --- 전 기간 격차: 모집단·순위·부호 전환 (본문 서술의 근거) -----------
    # 실질 증가율이 있는 모든 분기를 쓴다. 직전 분기는 명목 수준만 있으면 되므로
    # 교집합의 첫 원소(1947Q2)를 버리면 안 된다.
    def _prev(q):
        y, n = int(q[:4]), int(q[-1])
        return f"{y - 1}Q4" if n == 1 else f"{y}Q{n - 1}"

    hist = []
    for q in sorted(d["Y034RL"], key=lambda x: (int(x[:4]), int(x[-1]))):
        pv = _prev(q)
        if q in d["Y034RC"] and pv in d["Y034RC"]:
            hist.append((q, ((d["Y034RC"][q] / d["Y034RC"][pv]) ** 4 - 1) * 100
                         - d["Y034RL"][q]))
    assert len(hist) == 317 and hist[0][0] == "1947Q2", (len(hist), hist[0][0])
    cur = dict(hist)["2026Q2"]
    assert abs(cur - gap) < 1e-6, (cur, gap)

    pos = sorted([g for g in hist if g[1] > 0], key=lambda g: -g[1])
    assert len(pos) == 95, len(pos)
    assert [q for q, _ in pos].index("2026Q2") + 1 == 3
    assert {q for q, v in hist if v > cur} == {"1954Q4", "1956Q3"}   # 1956Q3 이후 최대
    # 절댓값이 20%p를 넘는 음의 격차가 있다. '가장 큰 폭'은 양의 격차로만 한정한다.
    worst = min(hist, key=lambda g: g[1])
    assert worst[0] == "1956Q2" and abs(worst[1] + 23.96) < 0.01, worst

    # 지금 이어지는 양의 구간은 2021Q3에 시작해 20개 분기 연속이다.
    # 과거에도 양의 격차는 여러 번 있었으므로 '사상 최초 부호 전환'이 아니다.
    run = 0
    for _, v in hist:
        run = run + 1 if v > 0 else 0
    assert run == 20, run
    assert dict(hist)["2021Q3"] > 0 and dict(hist)["2021Q2"] < 0

    win = [(q, v) for q, v in hist
           if (1983, 2) <= (int(q[:4]), int(q[-1])) <= (2021, 3)]
    assert len(win) == 154, len(win)
    neg = sum(1 for _, v in win if v < 0)
    assert neg == 147, neg
    absavg = sum(abs(v) for _, v in win) / len(win)
    assert 5.7 < absavg < 5.9, absavg
    over10 = sum(1 for _, v in win if abs(v) > 10)
    assert over10 == 24, over10

    # 전기비 가격의 부호. 격차 부호(147개)와 개수가 1개 다르다. 그 차이인 2021Q1은
    # 명목 10.459% / 공표 실질 10.5% / 가격 +0.026%인 정밀도 경계 사례이며,
    # 원인을 특정 계열 하나의 반올림으로 단정할 수는 없다(아래는 사실 확인만 한다).
    def _pq(q):
        y, n = int(q[:4]), int(q[-1])
        return f"{y - 1}Q4" if n == 1 else f"{y}Q{n - 1}"

    pdn = sum(1 for q, _ in win if d["Y034RG"][q] < d["Y034RG"][_pq(q)])
    pup = sum(1 for q, _ in win if d["Y034RG"][q] > d["Y034RG"][_pq(q)])
    assert (pdn, pup, len(win) - pdn - pup) == (146, 8, 0), (pdn, pup)
    odd = [q for q, v in win if v < 0 and d["Y034RG"][q] >= d["Y034RG"][_pq(q)]]
    assert odd == ["2021Q1"], odd
    # 최근 네 분기: 폭이 단조 확대된 것이 아니다(2025Q4에 한 번 줄었다)
    recent = {q: round(v, 2) for q, v in hist[-4:]}
    assert recent == {"2025Q3": 7.59, "2025Q4": 2.59,
                      "2026Q1": 10.91, "2026Q2": 14.21}, recent

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
    print(f"        전 기간 {len(hist)}개, 양의 격차 {len(pos)}개 중 3위, 연속 양수 {run}분기(2021Q3~)")
    print(f"        1983Q2~2021Q3: |격차| 평균 {absavg:.2f}%p, 10%p 초과 {over10}개, 명목<실질 {neg}/154")
    print(f"        전기비 가격 하락 {pdn} / 상승 {pup} / 보합 {len(win)-pdn-pup}, 불일치 {odd}")


if __name__ == "__main__":
    main()
