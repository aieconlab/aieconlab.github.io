#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그림 2: 단가와 청구서는 대체로 함께 가되 일대일이 아니다 — 출력 단가 vs 과제당 비용.

수치(집계사이트 Artificial Analysis 자체 측정, 2026-07-27 확인 — 원자료 스냅숏
data/aa_cost_per_task_rendered.txt. 'Cost per Task'의 사이트 정의는 "각 평가의 비용을
입력·캐시 적중·캐시 기록·추론·답변 토큰 가격에서 산출해 과제 수로 나누고 지수 가중치를
적용한 과제당 가중평균 비용"이다 — 출력 단가만의 함수가 아니다. 출력 단가는 각 사 공식 문서):
- DeepSeek V4-Pro (max)    출력 $0.87 | 과제당 $0.04
- Grok 4.5 (high)          출력 $6.00 | 과제당 $0.35
- Gemini 3.6 Flash         출력 $7.50 | 과제당 $0.50
- Claude Sonnet 5 (max)    출력 $10   | 과제당 $1.53
- Kimi K3                  출력 $15   | 과제당 $0.72
- Claude Opus 4.8 (max)    출력 $25   | 과제당 $1.80
- GPT-5.6 Sol (max)        출력 $30   | 과제당 $1.54
핵심: 두 축은 대체로 함께 움직인다(순위상관 0.929, 로그값 상관 0.953). 다만 일대일이 아니어서
단가 3배(Sol vs Sonnet)가 과제당엔 $0.01 차이로 압축되고, Sonnet의 단가 60% 우위(vs Opus 4.8)는
과제당 15%로 줄며, 인접 두 쌍(Sonnet-K3, Opus 4.8-Sol)에서 순위가 뒤집힌다.
모델마다 지능지수가 달라 동일 품질 비교가 아님.

사용법: python3 fig02_task_cost_slope.py [--out PNG] [--font FONT]
의존성: matplotlib
"""
import argparse
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
BLUE, NAVY, GRAY, NOTE, SPINE = "#2563eb", "#1b2a4a", "#8290a6", "#5a6472", "#c8cdd6"
DGRAY = "#4a5a7a"

# (표기, 출력 단가 $/1M, 과제당 비용 $, 색, 굵기, 강조)
MODELS = [
    ("DeepSeek V4-Pro (max)", 0.87, 0.04, GRAY, 1.8, False),
    ("Grok 4.5 (high)", 6.00, 0.35, GRAY, 1.8, False),
    ("Gemini 3.6 Flash", 7.50, 0.50, GRAY, 1.8, False),
    ("Claude Sonnet 5 (max)", 10.0, 1.53, BLUE, 3.0, True),
    ("Kimi K3", 15.0, 0.72, GRAY, 1.8, False),
    ("Claude Opus 4.8 (max)", 25.0, 1.80, DGRAY, 2.4, False),
    ("GPT-5.6 Sol (max)", 30.0, 1.54, NAVY, 3.0, True),
]
P = {m[0]: m[1] for m in MODELS}
C = {m[0]: m[2] for m in MODELS}

# ---- 수치 검증 ----
assert P["GPT-5.6 Sol (max)"] / P["Claude Sonnet 5 (max)"] == 3.0            # 단가 3배
assert abs(abs(C["GPT-5.6 Sol (max)"] - C["Claude Sonnet 5 (max)"]) - 0.01) < 1e-9  # 과제당 1센트 차
assert abs(1 - C["Claude Sonnet 5 (max)"] / C["Claude Opus 4.8 (max)"] - 0.15) < 0.005  # 15%
assert abs(1 - P["Claude Sonnet 5 (max)"] / P["Claude Opus 4.8 (max)"] - 0.60) < 1e-9   # 단가 60%
assert C["Grok 4.5 (high)"] / C["Claude Sonnet 5 (max)"] < 0.26              # 약 4분의 1 이하

# ---- 논지 검증: '대체로 함께 가되 일대일은 아니다' ----
# (구판의 '단가 순서는 청구서 순서를 예측하지 못한다'는 과장이어서 아래 두 조건으로 대체)
def _rank(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    r = [0] * len(vals)
    for pos, i in enumerate(order):
        r[i] = pos + 1
    return r


_p = [m[1] for m in MODELS]
_c = [m[2] for m in MODELS]
_rp, _rc = _rank(_p), _rank(_c)
_n = len(MODELS)
_spearman = 1 - 6 * sum((a - b) ** 2 for a, b in zip(_rp, _rc)) / (_n * (_n * _n - 1))
_inversions = [(MODELS[i][0], MODELS[j][0]) for i in range(_n) for j in range(_n)
               if _p[i] < _p[j] and _c[i] > _c[j]]
# (1) 두 축은 강하게 함께 움직인다 — '무관하다'로 읽히면 안 된다
assert _spearman > 0.85, ("순위상관이 낮아졌다 — 본문 서술 재검토 필요", round(_spearman, 3))
assert abs(_spearman - 0.929) < 0.005, ("본문 표기 0.93과 불일치", round(_spearman, 4))
# (2) 그러나 일대일은 아니다 — 역전이 존재하고, 그 수는 본문이 밝힌 두 쌍이다
assert len(_inversions) == 2, ("역전 쌍 수 변경 — 본문·캡션 수정 필요", _inversions)


def logpos(v, lo, hi):
    return (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "out" / "fig02_task_cost_slope.png")
    ap.add_argument("--font", default="Apple SD Gothic Neo")
    a = ap.parse_args()

    plt.rcParams["font.family"] = a.font
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["text.parse_math"] = False
    fig, ax = plt.subplots(figsize=(10, 7.0), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.06, 1.26)
    ax.axis("off")

    XL, XR = 0.335, 0.665
    plo, phi = min(P.values()), max(P.values())
    clo, chi = min(C.values()), max(C.values())

    for x in (XL, XR):
        ax.plot([x, x], [0, 1], color=SPINE, lw=1.2, zorder=1)
    heads = [
        ax.text(XL, 1.115, "토큰으로 센 값", fontsize=14.5, color=NAVY, ha="center",
                fontweight="bold"),
        ax.text(XL, 1.052, "출력 100만 토큰당 공식 단가", fontsize=10.5, color=NOTE,
                ha="center"),
        ax.text(XR, 1.115, "과제로 센 값", fontsize=14.5, color=NAVY, ha="center",
                fontweight="bold"),
        ax.text(XR, 1.052, "지능지수 과제당 가중평균 비용", fontsize=10.5, color=NOTE,
                ha="center"),
    ]

    # 오른쪽 라벨 y 슬롯(값이 거의 같은 Sonnet·Sol은 겹치지 않게 수동 배치)
    right_slot = {
        "Claude Opus 4.8 (max)": 1.000,
        "GPT-5.6 Sol (max)": 0.944,
        "Claude Sonnet 5 (max)": 0.896,
        "Kimi K3": 0.738,
        "Gemini 3.6 Flash": 0.651,
        "Grok 4.5 (high)": 0.564,
        "DeepSeek V4-Pro (max)": 0.040,
    }

    labels = list(heads)
    for name, price, cost, color, lw, strong in MODELS:
        yl = logpos(price, plo, phi) * 0.92 + 0.04
        yr = logpos(cost, clo, chi) * 0.92 + 0.04
        ax.plot([XL, XR], [yl, yr], color=color, lw=lw, zorder=3,
                alpha=1.0 if strong else 0.85, solid_capstyle="round")
        ax.plot([XL], [yl], "o", ms=8 if strong else 6, color=color, zorder=4)
        ax.plot([XR], [yr], "o", ms=8 if strong else 6, color=color, zorder=4)
        fw = "bold" if strong else "normal"
        labels.append(ax.text(XL - 0.022, yl, f"{name}  ${price:g}", fontsize=11.5,
                              color=color, ha="right", va="center", fontweight=fw))
        labels.append(ax.text(XR + 0.022, right_slot[name], f"${cost:.2f}  {name}",
                              fontsize=11, color=color, ha="left", va="center",
                              fontweight=fw))

    labels.append(ax.text((XL + XR) / 2, 0.30,
                          "두 축의 순위상관 0.93 — 대체로 함께 가지만\n단가 3배(Sonnet $10 vs Sol $30)가 과제당엔 1센트 차이",
                          fontsize=12, color=NAVY, ha="center", va="center",
                          fontweight="bold", linespacing=1.5))
    labels.append(ax.text((XL + XR) / 2, 0.135,
                          "Sonnet 5의 단가 60% 우위(vs Opus 4.8)는 과제당 15%로 줄고,\n인접 두 쌍(Sonnet 5–Kimi K3, Opus 4.8–Sol)에서는 순위가 뒤집힌다",
                          fontsize=10.5, color=NOTE, ha="center", va="center",
                          linespacing=1.5))

    ax.set_title("대체로 함께 가지만 일대일은 아니다: 토큰의 값 vs 과제의 값",
                 loc="left", fontsize=18, fontweight="bold", color=NAVY, pad=14)

    fig.subplots_adjust(left=0.015, right=0.985, top=0.905, bottom=0.185)

    NOTE_PARAS = [
        "주: 집계사이트 아티피셜 애널리시스(Artificial Analysis)의 자체 측정(2026-07-27 확인). 과제당 비용(Cost per "
        "Task)은 각 평가의 비용을 입력·캐시 적중·캐시 기록·추론·답변 토큰 가격에서 산출해 과제 수로 나누고 지수 "
        "가중치를 적용한 값이라 출력 단가만의 함수가 아니다. 괄호는 추론 설정이며, 모델마다 지능지수가 달라 같은 "
        "품질의 답에 대한 비교가 아니다. 세로 위치는 각 기둥 안의 로그 눈금 상대 위치다.",
        "자료: Artificial Analysis (artificialanalysis.ai), 각 사 공식 가격 문서  |  정리: AIEconLab",
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
    assert 2 <= len(wrapped) <= 5, ("주석 줄 수 이상", len(wrapped))
    ys_note = [0.132 - 0.033 * i for i in range(len(wrapped))]
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
