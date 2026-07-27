#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그림 1: 플래그십 출력 단가의 이동 — 전작 대비 (2026-07-27 확인, 달러/100만 토큰, 로그 눈금).

수치(각 사 공식 가격 문서, docs/03-analysis/intelligence-price/data/ 보존본과 1:1 대조):
- Anthropic: Opus 4.1 $75 → Opus 5 $25 (2025-11-24 Opus 4.5부터 인하), Fable 5 $50 신설
- OpenAI:    GPT-5.5 $30 → GPT-5.6 Sol $30 (동결, 2026-07-09)
- Moonshot:  Kimi K2.6 $4.00 → Kimi K3 $15.00 (3.75배, 2026-07-16)
- Google:    Gemini 2.5 Flash $2.50 → 3.5 Flash $9.00 (3.6배, 3.5 Flash는 2026-05-19
             I/O에서 전면 제공 — 7월 신모델 아님) → 3.6 Flash $7.50
- xAI:       Grok 4.3 $2.50 → Grok 4.5 $6.00 (2.4배, 2026-07-16)
- DeepSeek:  V4-Pro $3.48 → $0.87 (2026-05-25 발표, 05-31 발효 인하), V4-Flash $0.28
- 현행 스펙트럼: 최저 $0.28(V4-Flash) ~ 최고 $50(Fable 5) = 약 180배

사용법: python3 fig01_output_price_moves.py [--out PNG] [--font FONT]
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

# (회사, 구모델, 구가격, 신모델, 신가격, 시점 주석, 배수 라벨)
ROWS = [
    ("앤스로픽", "Opus 4.1", 75.0, "Opus 5", 25.0, "2025-11 인하", "×1/3"),
    ("오픈AI", "GPT-5.5", 30.0, "GPT-5.6 Sol", 30.0, "2026-07 신모델", "동결"),
    ("문샷AI", "Kimi K2.6", 4.0, "Kimi K3", 15.0, "2026-07 신모델", "×3.75"),
    ("구글", "2.5 Flash", 2.5, "3.6 Flash", 7.5, "2026-05~ 세대", "×3.0"),
    ("xAI", "Grok 4.3", 2.5, "Grok 4.5", 6.0, "2026-07 신모델", "×2.4"),
    ("딥시크", "V4-Pro", 3.48, "V4-Pro", 0.87, "2026-05 인하", "×1/4"),
]
FABLE5 = 50.0        # Anthropic 신설 최상위
GEMINI_35F = 9.0     # 구글 중간 경유(3.5 Flash)
V4_FLASH = 0.28      # 현행 최저

# ---- 수치 검증 ----
assert abs(FABLE5 / V4_FLASH - 178.6) < 1.0            # 약 180배
assert abs(15.0 / 4.0 - 3.75) < 1e-9                   # Kimi
assert abs(6.0 / 2.5 - 2.4) < 1e-9                     # Grok
assert abs(GEMINI_35F / 2.5 - 3.6) < 1e-9              # 3.5 Flash 대비
assert abs(7.5 / 2.5 - 3.0) < 1e-9                     # 3.6 Flash 대비
assert ROWS[1][2] == ROWS[1][4] == 30.0                # GPT 동결
assert abs(25.0 / 75.0 - 1 / 3) < 1e-9                 # Opus 인하
assert abs(0.87 / 3.48 - 0.25) < 1e-9                  # DeepSeek 인하
assert all(r[4] <= FABLE5 for r in ROWS)               # 현행 최고는 Fable 5


def dollar(v):
    return f"${v:g}" if v >= 1 else f"${v:.2f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "out" / "fig01_output_price_moves.png")
    ap.add_argument("--font", default="Apple SD Gothic Neo")
    a = ap.parse_args()

    plt.rcParams["font.family"] = a.font
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["text.parse_math"] = False  # '$' 두 개짜리 라벨의 mathtext 오파싱 방지
    fig, ax = plt.subplots(figsize=(10, 6.8), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    n = len(ROWS)
    ys = list(range(n, 0, -1))  # 위에서 아래로
    ax.set_xscale("log")
    ax.set_xlim(0.17, 300)
    ax.set_ylim(0.15, n + 1.05)

    labels = []
    for (comp, old_m, old_p, new_m, new_p, when, mult), y in zip(ROWS, ys):
        frozen = old_p == new_p
        if comp == "구글":  # 2.5 → 3.5 → 3.6 두 구간 경로
            ax.plot([old_p, GEMINI_35F], [y, y], color=NAVY, lw=2.0, zorder=3,
                    solid_capstyle="round")
            ax.plot([GEMINI_35F, new_p], [y, y], color=NAVY, lw=2.0, zorder=3,
                    solid_capstyle="round")
            ax.plot([GEMINI_35F], [y], "o", ms=6.5, mfc="white", mec=NAVY, mew=1.4, zorder=4)
            labels.append(ax.text(GEMINI_35F * 1.06, y + 0.30, f"3.5 Flash {dollar(GEMINI_35F)}",
                                  fontsize=9.5, color=NOTE, ha="left", va="center"))
        elif not frozen:
            ax.annotate("", xy=(new_p, y), xytext=(old_p, y),
                        arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=2.0,
                                        shrinkA=5, shrinkB=5, mutation_scale=16), zorder=3)
        if frozen:
            ax.plot([old_p], [y], "o", ms=13, mfc="none", mec=GRAY, mew=1.6, zorder=3)
            ax.plot([new_p], [y], "o", ms=8, color=NAVY, zorder=4)
            labels.append(ax.text(old_p, y + 0.34, f"{old_m} → {new_m}  {dollar(new_p)}",
                                  fontsize=10.5, color=NAVY, ha="center", va="center",
                                  fontweight="bold"))
        else:
            ax.plot([old_p], [y], "o", ms=8, mfc="white", mec=GRAY, mew=1.8, zorder=4)
            ax.plot([new_p], [y], "o", ms=8, color=NAVY, zorder=5)
            old_lab = f"{old_m} {dollar(old_p)}" if comp != "딥시크" else f"인하 전 {dollar(old_p)}"
            old_dy = -0.36 if comp == "앤스로픽" else 0.34  # 앤스로픽 행 상단은 Fable 라벨 몫
            labels.append(ax.text(old_p, y + old_dy, old_lab, fontsize=10, color=GRAY,
                                  ha="center", va="center"))
            labels.append(ax.text(new_p, y - 0.36, f"{new_m} {dollar(new_p)}", fontsize=10.5,
                                  color=NAVY, ha="center", va="center", fontweight="bold"))

        # 회사명(왼쪽 밖) · 배수/시점(오른쪽 밖)
        labels.append(ax.text(0.185, y, comp, fontsize=12, color=NAVY, ha="left",
                              va="center", fontweight="bold"))
        labels.append(ax.text(120, y + 0.14, mult, fontsize=11.5, ha="left", va="center",
                              color=(GRAY if mult in ("×1/3", "×1/4") else NAVY),
                              fontweight=("normal" if mult in ("×1/3", "×1/4") else "bold")))
        labels.append(ax.text(120, y - 0.24, when, fontsize=9, color=NOTE, ha="left",
                              va="center"))

    # Anthropic 행: Fable 5 신설(다이아몬드) / DeepSeek 행: V4-Flash 최저
    y_anth, y_ds = ys[0], ys[-1]
    ax.plot([FABLE5], [y_anth], marker="D", ms=8.5, color=BLUE, zorder=5, ls="none")
    labels.append(ax.text(FABLE5, y_anth + 0.34, f"Fable 5 {dollar(FABLE5)} (신설)",
                          fontsize=10.5, color=BLUE, ha="center", va="center",
                          fontweight="bold"))
    ax.plot([V4_FLASH], [y_ds], "o", ms=7, color=BLUE, zorder=5)
    labels.append(ax.text(0.19, y_ds - 0.36, f"V4-Flash {dollar(V4_FLASH)} (현행 최저)",
                          fontsize=9.5, color=BLUE, ha="left", va="center"))

    # 상단 스펙트럼 브래킷: $0.28 ~ $50 ≈ 180배
    y_br = n + 0.68
    ax.plot([V4_FLASH, FABLE5], [y_br, y_br], color=BLUE, lw=1.3, zorder=2)
    for x in (V4_FLASH, FABLE5):
        ax.plot([x, x], [y_br - 0.10, y_br + 0.10], color=BLUE, lw=1.3, zorder=2)
    labels.append(ax.text(math.sqrt(V4_FLASH * FABLE5), y_br + 0.13,
                          "현행 최저 $0.28 ~ 최고 $50 : 약 180배", fontsize=11, color=BLUE,
                          ha="center", va="bottom", fontweight="bold"))

    ax.set_yticks([])
    ax.set_xticks([0.3, 1, 3, 10, 30, 100])
    ax.set_xticklabels(["$0.3", "$1", "$3", "$10", "$30", "$100"], fontsize=12, color=NAVY)
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(SPINE)
    ax.tick_params(colors=NAVY, labelsize=12)
    ax.grid(axis="x", color=SPINE, linewidth=0.6, alpha=0.45)
    ax.set_axisbelow(True)
    ax.set_xlabel("출력 100만 토큰당 공식 단가 (달러, 로그 눈금)", fontsize=12.5, color=NAVY,
                  labelpad=7)
    ax.set_title("플래그십의 가격표: 7월의 신모델은 값을 내리지 않았다",
                 loc="left", fontsize=18.5, fontweight="bold", color=NAVY, pad=14)

    fig.subplots_adjust(left=0.02, right=0.985, top=0.925, bottom=0.285)

    NOTE_PARAS = [
        "주: 각 사 공식 문서의 표준 출력 단가(2026-07-27 확인, 캐시·배치 할인 제외). 회색은 비교 기준으로 원칙은 "
        "직전 모델이되, 구글은 기존 2.5 Flash(현행 3.6 Flash는 2026년 5월 이후 세대), 딥시크는 같은 모델의 "
        "인하 전 가격이다. 남색은 현행. 확인된 대폭 인하는 모두 2026년 7월 이전이다(앤스로픽 2025-11-24 "
        "Opus 4.5부터, 딥시크 2026-05-31 발효).",
        "자료: OpenAI·Anthropic·Google·xAI·Moonshot AI·DeepSeek 공식 가격 문서  |  정리: AIEconLab",
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
    ys_note = [0.150 - 0.041 * i for i in range(len(wrapped))]
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
        assert bb(t).y1 <= fig_h - 2, ("상단 잘림", t.get_text()[:18])
    boxes = [bb(t) for t in labels]
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            assert not boxes[i].overlaps(boxes[j]), \
                ("라벨 겹침", labels[i].get_text()[:14], labels[j].get_text()[:14])
    gaps = [bb(notes[k]).y0 - bb(notes[k + 1]).y1 for k in range(len(notes) - 1)]
    assert all(g >= 2 for g in gaps), ("주석 줄간 겹침", [round(g, 1) for g in gaps])
    xlab = ax.xaxis.get_label()
    assert bb(xlab).y0 - bb(notes[0]).y1 >= 4, "x축 라벨과 주석 겹침"
    for tick in ax.get_xticklabels():
        assert bb(xlab).y1 <= bb(tick).y0 + 2 or not bb(xlab).overlaps(bb(tick)), \
            "x축 라벨과 눈금 겹침"
    print(f"layout checks passed: {len(boxes)} labels clear, note gaps "
          f"{'/'.join(f'{g:.1f}' for g in gaps)}px")

    a.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.out, dpi=200, facecolor="white", metadata={"Date": None})
    print("wrote", a.out)


if __name__ == "__main__":
    main()
