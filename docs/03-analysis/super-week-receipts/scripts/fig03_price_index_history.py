#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그림 3: 미국 정보처리장비 가격지수 전년 동기 대비, 1948~2026.

이 계열은 품질조정을 반영하므로 오랫동안 '내려가는 것이 정상'이었다.
2021년 4분기에 상승으로 돌아섰고, 2026년 2분기에는 +7.4%로 1975년 2분기 이후
51년 만에 가장 높다(전년 동기 대비가 계산되는 1948년 1분기 이후 314개 분기에서 5번째).

자료: BEA NIPA 표 1.5.4 정보처리장비 가격지수(2017=100), 계열 Y034RG,
      2026년 2분기 속보치(2026-07-30 공표). 전년 동기 대비는 필자가 계산했다.
원자료: ../data/Section1All_xls.xlsx

사용법: python3 fig03_price_index_history.py [--out PNG] [--font FONT]
의존성: matplotlib, openpyxl
인터프리터: /opt/anaconda3/bin/python3
"""
import argparse
import hashlib
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import openpyxl

HERE = Path(__file__).resolve().parent
SRC = HERE / ".." / "data" / "Section1All_xls.xlsx"
# 원천 워크북 SHA-256 — extract_bea.py와 같은 빈티지를 쓰는지 확인한다
SRC_SHA = "ddcd0c5b693cb5d179198e67dda60f817e0e97196e6f1c158152971bbc80b136"
BLUE, NAVY, GRAY, NOTE, SPINE = "#2563eb", "#1b2a4a", "#8290a6", "#5a6472", "#c8cdd6"
AMBER, RED = "#d97706", "#b91c1c"


def load_yoy():
    got = hashlib.sha256(SRC.read_bytes()).hexdigest()
    if got != SRC_SHA:   # assert는 python -O에서 제거되므로 명시적 예외로 검사한다
        raise SystemExit(f"원천 워크북이 바뀌었다: {got}")
    wb = openpyxl.load_workbook(SRC, read_only=True)
    ws = wb["T10504-Q"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = [str(c) for c in rows[7]]
    row = next(r for r in rows[8:] if r and len(r) > 3 and r[2] == "Y034RG")
    p = {hdr[i]: row[i] for i in range(3, len(hdr)) if isinstance(row[i], (int, float))}
    qs = sorted(p, key=lambda q: (int(q[:4]), int(q[-1])))
    out = []
    for q in qs:
        prev = f"{int(q[:4]) - 1}Q{q[-1]}"
        if prev in p:
            out.append((int(q[:4]) + (int(q[-1]) - 1) / 4, q, (p[q] / p[prev] - 1) * 100))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "out" / "fig03_price_index_history.png")
    ap.add_argument("--font", default="Apple SD Gothic Neo")
    a = ap.parse_args()

    data = load_yoy()
    xs = [d[0] for d in data]
    ys = [d[2] for d in data]
    cur_q, cur_v = data[-1][1], data[-1][2]

    # --- 검산 ---------------------------------------------------------------
    assert cur_q == "2026Q2", cur_q
    assert abs(cur_v - 7.37) < 0.05, cur_v
    higher = [(q, v) for _, q, v in data if v > cur_v]
    assert len(higher) == 4, higher                    # 1951Q2, 1957Q2, 1975Q1, 1975Q2
    assert higher[-1][0] == "1975Q2", higher[-1]
    last_neg = [q for _, q, v in data if v < 0][-1]
    assert last_neg == "2021Q3", last_neg
    # 1983Q2~2021Q3의 154개 분기는 모두 전년 동기 대비 하락(본문 서술의 근거)
    run = [(q, v) for _, q, v in data
           if (1983, 2) <= (int(q[:4]), int(q[-1])) <= (2021, 3)]
    assert len(run) == 154, len(run)
    assert all(v < 0 for _, v in run), [q for q, v in run if v >= 0]
    # 순위 비교 모집단: 전년 동기 대비가 계산되는 1948Q1~2026Q2의 314개 분기
    assert len(data) == 314 and data[0][1] == "1948Q1", (len(data), data[0][1])
    # y축이 모든 관측치를 담아야 한다(절단 금지). 최저 1998Q4 -13.836%
    assert min(ys) > -15.5 and max(ys) < 11.5, (min(ys), max(ys))

    plt.rcParams["font.family"] = a.font
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(10, 5.6), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ax.fill_between(xs, ys, 0, where=[v < 0 for v in ys], color=BLUE, alpha=0.13, interpolate=True)
    ax.fill_between(xs, ys, 0, where=[v >= 0 for v in ys], color=AMBER, alpha=0.15, interpolate=True)
    ax.plot(xs, ys, color=NAVY, lw=1.5, zorder=3)
    ax.axhline(0, color=NOTE, lw=1.1, zorder=2)

    ax.scatter([xs[-1]], [cur_v], s=52, color=RED, zorder=5)
    ax.annotate(f"2026년 2분기\n+{cur_v:.1f}%",
                xy=(xs[-1], cur_v), xytext=(-14, 26), textcoords="offset points",
                ha="right", fontsize=12, color=RED, fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=RED, lw=1.2))

    i75 = next(i for i, d in enumerate(data) if d[1] == "1975Q2")
    ax.annotate(f"1975년 2분기\n+{ys[i75]:.1f}%", xy=(xs[i75], ys[i75]), xytext=(6, 22),
                textcoords="offset points", ha="left", fontsize=11, color=NOTE,
                arrowprops=dict(arrowstyle="-", color=NOTE, lw=1))

    # 계열선과 겹치지 않는 하단 여백에 배치한다(1960~1990 구간의 저점은 -6.5 부근)
    ax.text(1968, -13.6, "품질을 감안한 값이 해마다 내려가던 구간", fontsize=11.5,
            color=BLUE, ha="center", va="center", fontweight="bold")

    ax.set_xlim(1947.5, 2028.5)
    ax.set_ylim(-15.5, 11.5)
    ax.set_xticks([1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2026])
    ax.set_xticklabels(["1950", "60", "70", "80", "90", "2000", "10", "20", "26"],
                       fontsize=11, color=NOTE)
    ax.set_yticks([-12, -8, -4, 0, 4, 8])
    ax.set_yticklabels(["-12", "-8", "-4", "0", "+4", "+8%"], fontsize=11, color=NOTE)
    ax.set_ylabel("전년 동기 대비(%)", fontsize=11.5, color=NOTE, labelpad=12)
    ax.tick_params(length=0)
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color=SPINE, lw=0.6, alpha=0.45, zorder=1)
    ax.set_axisbelow(True)

    ax.set_title("정보처리장비 값이 오르고 있다: 미국 국민계정 가격지수, 1948~2026",
                 fontsize=15, color=NAVY, fontweight="bold", loc="left", pad=16)

    fig.text(0.075, 0.035,
             "BEA 국민계정 표 1.5.4(2017=100)의 분기 지수에서 전년 동기 대비를 필자가 계산했다. "
             "품질조정을 반영한 지수여서 성능 향상은 값 하락으로 나타난다.",
             fontsize=9.5, color=NOTE)

    fig.subplots_adjust(left=0.095, right=0.965, top=0.845, bottom=0.185)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.out, dpi=200, facecolor="white", metadata={"Date": None})
    print("wrote", a.out)
    print(f"2026Q2 +{cur_v:.2f}% / 이보다 높았던 분기 {len(higher)}개, 가장 최근 {higher[-1][0]}")


if __name__ == "__main__":
    main()
