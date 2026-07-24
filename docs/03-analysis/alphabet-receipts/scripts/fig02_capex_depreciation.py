#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그림 2: 지출과 비용 사이의 시차 — 설비투자와 감가상각비.

수치(백만 달러, 알파벳 실적 발표문 현금흐름표, 분기 기준):
- 2025년 2분기: 유형자산 취득 22,446 / 유형자산 감가상각 4,998
- 2026년 2분기: 유형자산 취득 44,924 / 유형자산 감가상각 7,104

검산(assert):
- 설비투자 2.00배, 감가상각 1.42배
- 두 항목은 서로 다른 시점의 자산을 가리키므로 비율(당기 감가상각/당기 설비투자)을
  '당기 지출의 비용 반영률'로 해석하지 않는다(그림·주석에도 그렇게 표기하지 않음)

사용법: python3 fig02_capex_depreciation.py [--out PNG] [--font FONT]
의존성: matplotlib
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.text import Text

HERE = Path(__file__).resolve().parent
BLUE, NAVY, GRAY, NOTE, SPINE = "#2563eb", "#1b2a4a", "#8290a6", "#5a6472", "#c8cdd6"

CAPEX = {"2025 2분기": 22_446, "2026 2분기": 44_924}
DEP = {"2025 2분기": 4_998, "2026 2분기": 7_104}

assert abs(CAPEX["2026 2분기"] / CAPEX["2025 2분기"] - 2.0) < 0.01
assert abs(DEP["2026 2분기"] / DEP["2025 2분기"] - 1.42) < 0.01


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path,
                    default=HERE / "out" / "fig02_capex_depreciation.png")
    ap.add_argument("--font", default="Apple SD Gothic Neo")
    a = ap.parse_args()

    plt.rcParams["font.family"] = a.font
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    labels = list(CAPEX.keys())
    xs = [0, 1]
    bw = 0.34
    cap = [CAPEX[k] / 100.0 for k in labels]   # 억 달러
    dep = [DEP[k] / 100.0 for k in labels]

    b1 = ax.bar([x - bw / 2 - 0.015 for x in xs], cap, width=bw, color=BLUE,
                label="설비투자(유형자산 취득)", zorder=3)
    b2 = ax.bar([x + bw / 2 + 0.015 for x in xs], dep, width=bw, color=GRAY,
                label="유형자산 감가상각비", zorder=3)

    val_texts = []
    for rect, v in zip(list(b1) + list(b2), cap + dep):
        val_texts.append(
            ax.text(rect.get_x() + rect.get_width() / 2, v + 8, f"{v:.0f}",
                    fontsize=15.5, fontweight="bold", ha="center", va="bottom",
                    color=BLUE if v in cap else "#57647a"))

    ann = ax.annotate("지출은 2배로 뛰는 동안\n비용화(감가상각)는 +42%",
                      xy=(xs[1] + bw / 2 + 0.13, dep[1] * 0.55),
                      xytext=(1.36, 245), fontsize=13.5, fontweight="bold",
                      color=NAVY, ha="center", va="center",
                      arrowprops=dict(arrowstyle="-", color=NAVY, lw=1.0), zorder=6)

    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=15, color=NAVY)
    ax.set_xlim(-0.55, 1.75)
    ax.set_ylim(0, 520)
    ax.set_ylabel("억 달러 (분기)", fontsize=15.5, color=NAVY)
    ax.tick_params(colors=NAVY, labelsize=14)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(SPINE)
    ax.grid(axis="y", color=SPINE, linewidth=0.6, alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_title("지출은 두 배, 비용은 아직: 설비투자와 감가상각의 시차",
                 loc="left", fontsize=20, fontweight="bold", color=NAVY, pad=16)
    leg = ax.legend(loc="upper left", frameon=False, fontsize=13.5)
    for t in leg.get_texts():
        t.set_color(NAVY)

    fig.subplots_adjust(left=0.10, right=0.97, top=0.89, bottom=0.17)
    note1 = fig.text(0.10, 0.068, "주: 감가상각은 과거에 취득한 자산에서 발생해 당기 설비투자와 1대 1로 대응하지 않는다. 두 항목 모두 분기 기준.",
                     fontsize=11.8, color=NOTE)
    note2 = fig.text(0.10, 0.028, "자료: Alphabet 2026년 2분기 실적 발표문(2026.7.22) 현금흐름표  |  계산: AIEconLab",
                     fontsize=11.8, color=NOTE)

    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    bb = lambda t: t.get_window_extent(renderer=rend)
    fig_w = fig.canvas.get_width_height()[0]
    for t in (note1, note2):
        assert bb(t).x1 <= fig_w - 5, ("주석 우측 잘림", t.get_text()[:16])
    gap_notes = bb(note1).y0 - bb(note2).y1
    assert gap_notes >= 2, ("주석 줄간 겹침", round(gap_notes, 1))
    # annotation의 get_window_extent는 화살표 영역까지 포함하므로 텍스트 상자만 비교
    ann_text_bb = Text.get_window_extent(ann, renderer=rend)
    assert not ann_text_bb.overlaps(bb(leg.get_texts()[0])), "주석-범례 겹침"
    for t in val_texts:
        assert not ann_text_bb.overlaps(bb(t)), ("주석-값 라벨 겹침", t.get_text())
    # 화살표 선분이 값 라벨을 가로지르지 않는지: 선분 x범위가 라벨 우측 경계 밖에 있는지 확인
    tip_x_px = ax.transData.transform((xs[1] + bw / 2 + 0.13, dep[1] * 0.55))[0]
    for t in val_texts:
        assert tip_x_px > bb(t).x1 or tip_x_px < bb(t).x0 - 200, ("화살표-값 라벨 근접", t.get_text())
    print(f"layout checks passed: notes gap {gap_notes:.1f}px, width ok")

    a.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.out, dpi=200, facecolor="white")
    print("wrote", a.out)


if __name__ == "__main__":
    main()
