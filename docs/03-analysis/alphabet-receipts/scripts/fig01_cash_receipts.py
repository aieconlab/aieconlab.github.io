#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그림 1: 2026년 2분기 알파벳 현금의 산수(워터폴).

수치(백만 달러, 알파벳 2026년 2분기 실적 발표문 현금흐름표, 2026-07-22 공시):
- 영업활동 현금흐름(Net cash provided by operating activities): 39,069
- 유형자산 취득(Purchases of property and equipment): 44,924
- 잉여현금흐름(비GAAP, 위 둘의 차): -5,855 -> 표기 -59억 달러

검산(assert):
- 39,069 - 44,924 = -5,855
- 449.24억(설비투자)은 전년 동기 224.46억의 2.00배(전년 동기 22,446)

사용법: python3 fig01_cash_receipts.py [--out PNG] [--font FONT]
의존성: matplotlib
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = Path(__file__).resolve().parent
BLUE, NAVY, GRAY, NOTE, SPINE = "#2563eb", "#1b2a4a", "#8290a6", "#5a6472", "#c8cdd6"

OCF_M = 39_069        # 영업활동 현금흐름
CAPEX_M = 44_924      # 유형자산 취득
FCF_M = OCF_M - CAPEX_M
CAPEX_PREV_M = 22_446  # 전년 동기 유형자산 취득

assert FCF_M == -5_855
assert abs(CAPEX_M / CAPEX_PREV_M - 2.0) < 0.01

# 억 달러 단위 표시값(본문 표기와 동일한 반올림)
ocf, capex, fcf = OCF_M / 100.0, CAPEX_M / 100.0, FCF_M / 100.0
assert round(ocf) == 391 and round(capex) == 449
assert abs(fcf + 58.55) < 0.001  # 표기 -59는 통상(반올림 half-up) 기준


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "out" / "fig01_cash_receipts.png")
    ap.add_argument("--font", default="Apple SD Gothic Neo")
    a = ap.parse_args()

    plt.rcParams["font.family"] = a.font
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax = plt.subplots(figsize=(10, 6.4), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    bw = 0.52
    xs = [0, 1, 2]

    # 1) 영업활동 현금흐름: 0 -> +391
    ax.add_patch(Rectangle((xs[0] - bw / 2, 0), bw, ocf, color=NAVY, zorder=3))
    # 2) 설비투자: +391 -> -59 (감소 막대)
    ax.add_patch(Rectangle((xs[1] - bw / 2, fcf), bw, capex, color=GRAY, zorder=3))
    # 3) 잉여현금흐름: 0 -> -59
    ax.add_patch(Rectangle((xs[2] - bw / 2, fcf), bw, -fcf, color=BLUE, zorder=3))

    # 연결 점선(워터폴)
    ax.plot([xs[0] + bw / 2, xs[1] + bw / 2], [ocf, ocf],
            color=SPINE, lw=1.3, ls=(0, (4, 3)), zorder=2)
    ax.plot([xs[1] + bw / 2, xs[2] + bw / 2], [fcf, fcf],
            color=SPINE, lw=1.3, ls=(0, (4, 3)), zorder=2)

    # 0선
    ax.axhline(0, color="#9ca3af", lw=1.3, zorder=4)

    # 값 라벨
    ax.text(xs[0], ocf + 14, "+391", fontsize=17, fontweight="bold",
            color=NAVY, ha="center", va="bottom")
    ax.text(xs[1], ocf + 14, "-449", fontsize=17, fontweight="bold",
            color="#57647a", ha="center", va="bottom")
    ax.text(xs[2], fcf - 16, "-59", fontsize=17.5, fontweight="bold",
            color=BLUE, ha="center", va="top")

    # 보조 주석: 설비투자는 전년 동기의 2배
    note_capex = ax.annotate("전년 동기(224억 달러)의 2배", xy=(xs[1], fcf + capex * 0.45),
                             xytext=(2.02, 245), fontsize=13.5, color=NAVY,
                             ha="center", va="center",
                             arrowprops=dict(arrowstyle="-", color=NAVY, lw=1.0), zorder=6)

    ax.set_xticks(xs)
    ax.set_xticklabels(["영업활동\n현금흐름", "설비투자\n(유형자산 취득)", "잉여현금흐름"],
                       fontsize=14.5, color=NAVY)
    ax.set_xlim(-0.65, 2.65)
    # 하단 여백을 넉넉히 둬 '-59' 값 라벨이 x축 스파인에 걸리지 않게 한다
    ax.set_ylim(-125, 480)
    ax.set_yticks([0, 100, 200, 300, 400])  # 축 확장이 -100 눈금을 새로 만들지 않도록 고정
    ax.set_ylabel("2026년 2분기, 억 달러", fontsize=15.5, color=NAVY)
    ax.tick_params(colors=NAVY, labelsize=14)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(SPINE)
    ax.grid(axis="y", color=SPINE, linewidth=0.6, alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_title("번 것보다 많이 썼다: 상장 후 첫 마이너스로 보도된 잉여현금흐름",
                 loc="left", fontsize=19.5, fontweight="bold", color=NAVY, pad=16)

    fig.subplots_adjust(left=0.10, right=0.97, top=0.90, bottom=0.235)
    note1 = fig.text(0.10, 0.112, "주: 잉여현금흐름(-58.55억 달러, 표기 -59) = 영업활동 현금흐름 - 유형자산 취득(비GAAP).",
                     fontsize=11.8, color=NOTE)
    note2 = fig.text(0.10, 0.070, "‘상장 후 첫 마이너스’는 FactSet 집계(현지 보도 인용)이며, 막대 표기는 억 달러 반올림.",
                     fontsize=11.8, color=NOTE)
    note3 = fig.text(0.10, 0.028, "자료: Alphabet 2026년 2분기 실적 발표문(2026.7.22) 현금흐름표  |  계산: AIEconLab",
                     fontsize=11.8, color=NOTE)

    # 렌더링 후 텍스트 충돌·잘림 검사
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    bb = lambda t: t.get_window_extent(renderer=rend)
    fig_w = fig.canvas.get_width_height()[0]
    for t in (note1, note2, note3):
        assert bb(t).x1 <= fig_w - 5, ("주석 우측 잘림", t.get_text()[:16])
    gap12 = bb(note1).y0 - bb(note2).y1
    gap23 = bb(note2).y0 - bb(note3).y1
    assert gap12 >= 2 and gap23 >= 2, ("주석 줄간 겹침", round(gap12, 1), round(gap23, 1))
    assert not bb(note_capex).overlaps(bb(ax.title)), "주석-제목 겹침"
    # 값 라벨이 x축 스파인 아래로 삐져나가 취소선처럼 보이지 않는지 검사
    ax_y0 = ax.get_window_extent(renderer=rend).y0
    for t in ax.texts:
        assert bb(t).y0 > ax_y0 + 3, ("값 라벨-축선 겹침", t.get_text())
    print(f"layout checks passed: note gaps {gap12:.1f}/{gap23:.1f}px, width ok")

    a.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.out, dpi=200, facecolor="white")
    print("wrote", a.out)


if __name__ == "__main__":
    main()
