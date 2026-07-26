#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그림 1: 중국 집적회로 수출의 두 경로 — 누계 금액·수량 전년 동기 대비 증가율(2026년).

수치(중국 해관총서 「(5) Major Exports by Quantity and Value」 2~6월판, 달러 기준,
연초 누계 전년 동기 대비 증가율 %, 표에 인쇄된 공표치):
- 금액:  1-2월 +72.6 / 1-3월 +77.5 / 1-4월 +83.7 / 1-5월 +90.0 / 1-6월 +96.1
- 수량:  1-2월 +13.7 / 1-3월 +13.4 / 1-4월 +10.6 / 1-5월 +8.7 / 1-6월 +7.0
검산: 상반기 금액 배수 1.9610 = 단가 배수 1.8328 × 수량 배수 1.0699

사용법: python3 fig01_value_vs_volume.py [--out PNG] [--font FONT]
의존성: matplotlib
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
BLUE, NAVY, GRAY, NOTE, SPINE = "#2563eb", "#1b2a4a", "#8290a6", "#5a6472", "#c8cdd6"

LABELS = ["1-2월", "1-3월", "1-4월", "1-5월", "1-6월"]
VALUE_YOY = [72.6, 77.5, 83.7, 90.0, 96.1]   # 금액(달러) 누계 YoY
VOLUME_YOY = [13.7, 13.4, 10.6, 8.7, 7.0]    # 수량(개수) 누계 YoY

assert VALUE_YOY[-1] == 96.1 and VOLUME_YOY[-1] == 7.0
assert abs(1.9610 / 1.0699 - 1.8328) < 0.001            # 단가 배수 검산
assert all(a >= b for a, b in zip(VALUE_YOY[1:], VALUE_YOY[:-1]))    # 금액은 단조 상승
assert all(a <= b for a, b in zip(VOLUME_YOY[1:], VOLUME_YOY[:-1]))  # 수량은 단조 하락


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "out" / "fig01_value_vs_volume.png")
    ap.add_argument("--font", default="Apple SD Gothic Neo")
    a = ap.parse_args()

    plt.rcParams["font.family"] = a.font
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax = plt.subplots(figsize=(10, 6.4), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    xs = range(len(LABELS))

    # 두 경로 사이를 옅게 채워 격차를 보인다
    ax.fill_between(xs, VOLUME_YOY, VALUE_YOY, color=BLUE, alpha=0.05, zorder=1)

    ax.plot(xs, VALUE_YOY, color=NAVY, lw=3.0, marker="o", ms=6.5, zorder=4)
    ax.plot(xs, VOLUME_YOY, color=BLUE, lw=2.6, marker="o", ms=6.5, zorder=4)

    # 값 라벨: 금액은 점 위, 수량은 점 아래
    val_labels = []
    for i, v in enumerate(VALUE_YOY):
        bold = i == len(VALUE_YOY) - 1
        val_labels.append(ax.text(i, v + 3.0, f"+{v:.1f}%", fontsize=12.5 if bold else 11.5,
                                  fontweight="bold" if bold else "normal",
                                  color=NAVY, ha="center", va="bottom"))
    for i, v in enumerate(VOLUME_YOY):
        bold = i == len(VOLUME_YOY) - 1
        val_labels.append(ax.text(i, v - 3.0, f"+{v:.1f}%", fontsize=12.5 if bold else 11.5,
                                  fontweight="bold" if bold else "normal",
                                  color=BLUE, ha="center", va="top"))

    # 계열 이름
    series_val = ax.text(4.18, VALUE_YOY[-1] - 6.5, "수출 금액\n(달러 기준)", fontsize=13.5,
                         fontweight="bold", color=NAVY, ha="left", va="center", linespacing=1.4)
    series_vol = ax.text(4.18, VOLUME_YOY[-1] + 6.5, "수출 수량\n(개수 기준)", fontsize=13.5,
                         fontweight="bold", color=BLUE, ha="left", va="center", linespacing=1.4)

    ax.axhline(0, color="#9ca3af", lw=1.3, zorder=3)

    ax.set_xticks(list(xs))
    ax.set_xticklabels(LABELS, fontsize=13.5, color=NAVY)
    ax.set_xlim(-0.35, 5.35)
    ax.set_ylim(-6, 112)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_ylabel("연초 누계 전년 동기 대비 증가율(%)", fontsize=14.5, color=NAVY)
    ax.tick_params(colors=NAVY, labelsize=13)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(SPINE)
    ax.grid(axis="y", color=SPINE, linewidth=0.6, alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_title("같은 표의 두 경로: 중국 집적회로 수출, 금액은 오르고 수량은 내렸다",
                 loc="left", fontsize=18.5, fontweight="bold", color=NAVY, pad=16)

    fig.subplots_adjust(left=0.095, right=0.97, top=0.905, bottom=0.225)
    # 주석은 이미지 왼쪽 끝(x=0.01)에서 시작해, 본문에 삽입됐을 때 글의 왼쪽 선과 맞도록 한다
    note1 = fig.text(0.01, 0.112, "주: 각 시점의 연초 누계 전년 동기 대비 증가율(해관총서 공표치). 수량 단위는 개수(억 개)이며",
                     fontsize=11.8, color=NOTE)
    note2 = fig.text(0.01, 0.070, "제품 구성 변화를 통제하지 못한다. 6월 단월의 수량 증가율은 -0.4%(누계 차분).",
                     fontsize=11.8, color=NOTE)
    note3 = fig.text(0.01, 0.028, "자료: 중국 해관총서 「주요 수출상품 수량·금액표」 2~6월판(달러 기준)  |  계산: AIEconLab",
                     fontsize=11.8, color=NOTE)

    # 렌더링 후 텍스트 충돌·잘림 검사
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    bb = lambda t: t.get_window_extent(renderer=rend)
    fig_w = fig.canvas.get_width_height()[0]
    for t in (note1, note2, note3, series_val, series_vol):
        assert bb(t).x1 <= fig_w - 5, ("우측 잘림", t.get_text()[:16])
    gap12 = bb(note1).y0 - bb(note2).y1
    gap23 = bb(note2).y0 - bb(note3).y1
    assert gap12 >= 2 and gap23 >= 2, ("주석 줄간 겹침", round(gap12, 1), round(gap23, 1))
    # 값 라벨끼리 겹침 검사(같은 계열의 이웃 라벨 + 두 계열 간)
    boxes = [bb(t) for t in val_labels]
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            assert not boxes[i].overlaps(boxes[j]), ("값 라벨 겹침", i, j)
    # 계열 이름이 값 라벨과 겹치지 않는지
    for t in (series_val, series_vol):
        for b in boxes:
            assert not bb(t).overlaps(b), ("계열 이름-값 라벨 겹침", t.get_text()[:8])
    print(f"layout checks passed: note gaps {gap12:.1f}/{gap23:.1f}px, {len(boxes)} labels clear")

    a.out.parent.mkdir(parents=True, exist_ok=True)
    # 실행시각(Date) 메타데이터를 제거한다. 바이트·픽셀 재현성 기준은 분석 README 참조
    fig.savefig(a.out, dpi=200, facecolor="white", metadata={"Date": None})
    print("wrote", a.out)


if __name__ == "__main__":
    main()
