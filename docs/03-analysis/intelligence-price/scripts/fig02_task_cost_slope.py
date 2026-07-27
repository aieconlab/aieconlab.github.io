#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그림 2: 토큰 단가의 순서와 과제당 비용의 순서는 다르다 — 기울기 그래프.

수치(집계사이트 Artificial Analysis 자체 측정, 2026-07-27 확인. '지수 완주 비용'은
동 사이트 지능지수(Intelligence Index) 전체 평가를 실행하는 비용으로, 입력·캐시·추론·
출력 요금을 모두 합산한 값):
- Claude Sonnet 5           지능 53 | 완주 토큰 300M  | 완주 비용 $4,010.12 | 출력 단가 $10
- Claude Opus 4.8 (max)     지능 56 | 완주 토큰 120M  | 완주 비용 $3,752.55 | 출력 단가 $25
- Claude Fable 5            지능 60 | 완주 토큰 87M   | 완주 비용 $5,630.52 | 출력 단가 $50
- GPT-5.6 Sol (low)         지능 49 | 완주 토큰 6.6M  | 완주 비용 $400.79   | 출력 단가 $30
핵심: Sonnet 5는 출력 단가가 Opus 4.8보다 60% 싼데 완주 비용은 약 7% 더 비싸다.

사용법: python3 fig02_task_cost_slope.py [--out PNG] [--font FONT]
의존성: matplotlib
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
BLUE, NAVY, GRAY, NOTE, SPINE = "#2563eb", "#1b2a4a", "#8290a6", "#5a6472", "#c8cdd6"

# (모델, 지능지수, 완주 토큰 표기, 완주 비용 $, 출력 단가 $/1M, 색, 굵기, 강조)
MODELS = [
    ("Claude Fable 5", 60, "8,700만", 5630.52, 50.0, "#4a5a7a", 2.0, False),
    ("GPT-5.6 Sol (low)", 49, "660만", 400.79, 30.0, GRAY, 2.0, False),
    ("Claude Opus 4.8 (max)", 56, "1억 2,000만", 3752.55, 25.0, NAVY, 3.0, True),
    ("Claude Sonnet 5", 53, "3억", 4010.12, 10.0, BLUE, 3.0, True),
]

# ---- 수치 검증 ----
_price = {m[0]: m[4] for m in MODELS}
_cost = {m[0]: m[3] for m in MODELS}
assert abs(_price["Claude Sonnet 5"] / _price["Claude Opus 4.8 (max)"] - 0.40) < 1e-9  # 단가 60% 저렴
assert abs(_cost["Claude Sonnet 5"] / _cost["Claude Opus 4.8 (max)"] - 1.0686) < 0.001  # 완주는 약 7% 비쌈
assert abs(_cost["Claude Opus 4.8 (max)"] / _cost["GPT-5.6 Sol (low)"] - 9.36) < 0.01   # 약 9분의 1
assert _cost["Claude Fable 5"] == max(_cost.values())
assert 300 / 120 == 2.5  # 완주 토큰 배수(3억 vs 1.2억)


def norm(v, lo, hi):
    return (v - lo) / (hi - lo)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "out" / "fig02_task_cost_slope.png")
    ap.add_argument("--font", default="Apple SD Gothic Neo")
    a = ap.parse_args()

    plt.rcParams["font.family"] = a.font
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["text.parse_math"] = False  # '$' 라벨의 mathtext 오파싱 방지
    fig, ax = plt.subplots(figsize=(10, 6.9), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.10, 1.24)
    ax.axis("off")

    XL, XR = 0.315, 0.685  # 두 기둥의 x 위치
    prices = [m[4] for m in MODELS]
    costs = [m[3] for m in MODELS]
    plo, phi = min(prices), max(prices)
    clo, chi = min(costs), max(costs)

    # 기둥
    for x in (XL, XR):
        ax.plot([x, x], [0, 1], color=SPINE, lw=1.2, zorder=1)
    col_heads = [
        ax.text(XL, 1.10, "토큰으로 센 값", fontsize=14, color=NAVY, ha="center",
                fontweight="bold"),
        ax.text(XL, 1.045, "출력 100만 토큰당 단가", fontsize=10.5, color=NOTE, ha="center"),
        ax.text(XR, 1.10, "답으로 센 값", fontsize=14, color=NAVY, ha="center",
                fontweight="bold"),
        ax.text(XR, 1.045, "같은 지능지수 평가 전체를 완주한 비용", fontsize=10.5,
                color=NOTE, ha="center"),
    ]

    labels = list(col_heads)
    for name, iq, tok, cost, price, color, lw, strong in MODELS:
        yl = norm(price, plo, phi) * 0.92 + 0.04
        yr = norm(cost, clo, chi) * 0.92 + 0.04
        ax.plot([XL, XR], [yl, yr], color=color, lw=lw, zorder=3,
                alpha=1.0 if strong else 0.85, solid_capstyle="round")
        ax.plot([XL], [yl], "o", ms=8 if strong else 6.5, color=color, zorder=4)
        ax.plot([XR], [yr], "o", ms=8 if strong else 6.5, color=color, zorder=4)
        fw = "bold" if strong else "normal"
        labels.append(ax.text(XL - 0.022, yl, f"{name}  ${price:g}", fontsize=11.5,
                              color=color, ha="right", va="center", fontweight=fw))
        labels.append(ax.text(XR + 0.022, yr, f"${cost:,.0f}  (지능 {iq} · {tok} 토큰)",
                              fontsize=11, color=color, ha="left", va="center",
                              fontweight=fw))

    # 교차 강조 주석: 단가는 싼데 완주는 비싸다
    labels.append(ax.text((XL + XR) / 2, 0.145,
                          "단가 60% 싼 Sonnet 5가\n완주 비용은 7% 더 비싸다",
                          fontsize=12, color=BLUE, ha="center", va="center",
                          fontweight="bold", linespacing=1.45))
    labels.append(ax.text((XL + XR) / 2, -0.055,
                          "지능 49로 낮춘 GPT-5.6 Sol (low)의 완주 비용은 Opus 4.8의 약 9분의 1",
                          fontsize=10.5, color=GRAY, ha="center", va="center"))

    ax.set_title("같은 자를 대도 순서가 뒤집힌다: 토큰의 값 vs 답의 값",
                 loc="left", fontsize=18.5, fontweight="bold", color=NAVY, pad=14)

    fig.subplots_adjust(left=0.015, right=0.985, top=0.90, bottom=0.185)

    NOTE_PARAS = [
        "주: 집계사이트 아티피셜 애널리시스(Artificial Analysis)의 자체 측정(2026-07-27 확인). '완주 비용'은 동 사이트 "
        "지능지수(Intelligence Index) 전체 평가를 실행할 때의 입력·캐시·추론·출력 요금 합산으로, 출력 단가만으로 계산되지 "
        "않는다. 괄호는 추론 설정, 세로 위치는 각 기둥 안의 상대 위치다.",
        "자료: Artificial Analysis (artificialanalysis.ai)  |  정리: AIEconLab",
    ]
    NOTE_X, NOTE_FS = 0.01, 11.3
    rend0 = fig.canvas.get_renderer()
    fig_w0 = fig.canvas.get_width_height()[0]
    limit = fig_w0 * (0.99 - NOTE_X)

    def measure(s):
        t = fig.text(0, -1, s, fontsize=NOTE_FS)
        w = t.get_window_extent(renderer=rend0).width
        t.remove()
        return w

    wrapped = []
    for pi, para in enumerate(NOTE_PARAS):
        cur = ""
        for word in para.split(" "):
            trial = (cur + " " + word).strip()
            if measure(trial) <= limit or not cur:
                cur = trial
            else:
                wrapped.append((pi, cur))
                cur = word
        wrapped.append((pi, cur))
    assert 2 <= len(wrapped) <= 4, ("주석 줄 수 이상", len(wrapped))
    ys_note = [0.126 - 0.038 * i for i in range(len(wrapped))]
    notes = [fig.text(NOTE_X, y, ln, fontsize=NOTE_FS, color=NOTE)
             for (pi, ln), y in zip(wrapped, ys_note)]
    for i, (pi, ln) in enumerate(wrapped[:-1]):
        if wrapped[i + 1][0] == pi:
            assert measure(ln) >= 0.86 * limit, ("주석 줄 채움 부족", ln[:20])

    # ---- 렌더링 후 겹침·잘림 검사 ----
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    bb = lambda t: t.get_window_extent(renderer=rend)
    fig_w, fig_h = fig.canvas.get_width_height()
    for t in labels + notes:
        assert bb(t).x1 <= fig_w - 3, ("우측 잘림", t.get_text()[:18])
        assert bb(t).x0 >= 0, ("좌측 잘림", t.get_text()[:18])
    boxes = [bb(t) for t in labels]
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            assert not boxes[i].overlaps(boxes[j]), \
                ("라벨 겹침", labels[i].get_text()[:16], labels[j].get_text()[:16])
    gaps = [bb(notes[k]).y0 - bb(notes[k + 1]).y1 for k in range(len(notes) - 1)]
    assert all(g >= 2 for g in gaps), ("주석 줄간 겹침", [round(g, 1) for g in gaps])
    print(f"layout checks passed: {len(boxes)} labels clear, note gaps "
          f"{'/'.join(f'{g:.1f}' for g in gaps)}px")

    a.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.out, dpi=200, facecolor="white", metadata={"Date": None})
    print("wrote", a.out)


if __name__ == "__main__":
    main()
