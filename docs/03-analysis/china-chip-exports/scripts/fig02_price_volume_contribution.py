#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그림 2: 수출액 증가에서 물량이 설명하는 몫 — 같은 로그 분해, 네 계열(2026년 상반기 YoY).

수치:
- 중국 집적회로 수출: 금액 +96.1%, 수량(개수) +7.0% -> 물량 기여 10.0%
  (중국 해관총서 (5) 수량·금액표 2026년 6월판, 달러 기준)
- 한국 집적회로 수출: 금액지수 +170.4%, 물량지수 +13.9% -> 물량 기여 13.1%
- 한국 반도체 수출:  금액지수 +166.7%, 물량지수 +16.6% -> 물량 기여 15.7%
- 한국 총수출:       금액지수 +50.8%,  물량지수 +20.8% -> 물량 기여 45.9%
  (한국은행 ECOS 403Y001·403Y002, 2020=100, 2025H1·2026H1 월별 지수 평균, 필자 계산)
기여도 = ln(물량 배수)/ln(금액 배수) × 100. 중국은 개수, 한국은 물량지수로 잣대가 다름.

사용법: python3 fig02_price_volume_contribution.py [--out PNG] [--font FONT]
의존성: matplotlib
"""
import argparse
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = Path(__file__).resolve().parent
BLUE, NAVY, GRAY, NOTE, SPINE = "#2563eb", "#1b2a4a", "#8290a6", "#5a6472", "#c8cdd6"

# (라벨, 금액증가율%, 물량증가율%, 물량기여도%, 잣대)
ROWS = [
    ("중국 집적회로 수출", 96.1, 7.0, 10.0, "개수"),
    ("한국 집적회로 수출", 170.4, 13.9, 13.1, "물량지수"),
    ("한국 반도체 수출", 166.7, 16.6, 15.7, "물량지수"),
    ("한국 총수출", 50.8, 20.8, 45.9, "물량지수"),
]


def contrib(v, q):  # v, q는 배수
    return math.log(q) / math.log(v) * 100


assert abs(contrib(1.9610, 1.0699) - 10.0) < 0.15
assert abs(contrib(2.7044, 1.1389) - 13.1) < 0.15
assert abs(contrib(2.6667, 1.1664) - 15.7) < 0.15
assert abs(contrib(1.5084, 1.2077) - 45.9) < 0.15
# 표의 증가율과 기여도가 서로 정합한지도 검산
for _label, v_pct, q_pct, c_pct, _m in ROWS:
    assert abs(contrib(1 + v_pct / 100, 1 + q_pct / 100) - c_pct) < 0.15, _label


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "out" / "fig02_price_volume_contribution.png")
    ap.add_argument("--font", default="Apple SD Gothic Neo")
    a = ap.parse_args()

    plt.rcParams["font.family"] = a.font
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax = plt.subplots(figsize=(10.6, 6.4), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    bh = 0.56
    ys = [3, 2, 1, 0]  # 중국이 맨 위

    right_notes = []
    for (label, v_pct, q_pct, c_pct, measure), y in zip(ROWS, ys):
        ax.add_patch(Rectangle((0, y - bh / 2), c_pct, bh, color=BLUE, zorder=3))
        ax.add_patch(Rectangle((c_pct, y - bh / 2), 100 - c_pct, bh, color=GRAY, zorder=3))
        # 물량 기여(%) 라벨: 좁은 구간은 막대 왼쪽 밖 대신 파란 구간 오른쪽에 흰 글씨가 안 들어가므로 밖에 표기
        if c_pct >= 18:
            ax.text(c_pct / 2, y, f"{c_pct:.1f}%", fontsize=13.5, fontweight="bold",
                    color="white", ha="center", va="center", zorder=5)
        else:
            ax.text(c_pct + 1.6, y, f"{c_pct:.1f}%", fontsize=13.5, fontweight="bold",
                    color="white", ha="left", va="center", zorder=5)
        # 단가 기여 라벨(회색 구간 중앙)
        ax.text(c_pct + (100 - c_pct) / 2 + (4 if c_pct < 18 else 0), y, f"단가 기여 {100 - c_pct:.1f}%",
                fontsize=12.5, color="white", ha="center", va="center", zorder=5)
        # 막대 오른쪽: 원 증가율 병기
        right_notes.append(ax.text(101.8, y, f"금액 +{v_pct:.1f}%\n물량 +{q_pct:.1f}%",
                                   fontsize=11.8, color=NOTE, ha="left", va="center", linespacing=1.45))

    # 중국 행과 한국 3행 사이 옅은 구분선
    ax.axhline(2.5, color=SPINE, lw=1.0, ls=(0, (4, 3)), zorder=2)
    sep_note = ax.text(-1.5, 2.5, "잣대: 개수 ↑ / 물량지수 ↓", fontsize=10.5, color=NOTE,
                       ha="right", va="center")

    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in ROWS], fontsize=14, color=NAVY)
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.62, 3.62)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=12.5)
    ax.set_xlabel("수출액 증가에 대한 기여도(물량 = 파랑, 단가 = 회색)", fontsize=14, color=NAVY)
    ax.tick_params(colors=NAVY, labelsize=13)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(SPINE)
    ax.set_axisbelow(True)
    ax.set_title("물량이 설명하는 몫: 10%에서 46%까지 (2026년 상반기, 전년 동기 대비)",
                 loc="left", fontsize=18, fontweight="bold", color=NAVY, pad=14)

    fig.subplots_adjust(left=0.185, right=0.865, top=0.9, bottom=0.26)
    # 주석은 이미지 왼쪽 끝(x=0.01)에서 시작하고, '주' 문단은 그림 폭에 맞춰
    # 그리디 줄바꿈으로 채운다(마지막 줄을 제외한 각 줄이 폭의 88% 이상이어야 통과)
    NOTE_PARAS = [
        "주: 물량 기여도 = ln(물량 배수)/ln(금액 배수). 중국은 수출 개수, 한국은 가격 변동분을 제거한 "
        "수출물량지수(2020=100)로 잣대가 다르다. 한국은 2025·2026년 상반기 월별 지수 평균 기준.",
        "자료: 중국 해관총서 「주요 수출상품 수량·금액표」, 한국은행 ECOS 403Y001·403Y002  |  계산: AIEconLab",
    ]
    NOTE_X, NOTE_FS = 0.01, 11.8
    rend0 = fig.canvas.get_renderer()
    fig_w0 = fig.canvas.get_width_height()[0]
    limit = fig_w0 * (0.99 - NOTE_X)

    def measure(s):
        t = fig.text(0, -1, s, fontsize=NOTE_FS)
        w = t.get_window_extent(renderer=rend0).width
        t.remove()
        return w

    wrapped = []  # (para_index, line)
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
    assert len(wrapped) == 3, ("주석 줄 수 변경 — y 좌표 재설계 필요", len(wrapped))
    ys = [0.135, 0.093, 0.051]
    notes = [fig.text(NOTE_X, y, ln, fontsize=NOTE_FS, color=NOTE)
             for (pi, ln), y in zip(wrapped, ys)]
    # 문단 중간 줄(다음 줄이 같은 문단)은 폭을 충분히 채워야 한다
    for i, (pi, ln) in enumerate(wrapped[:-1]):
        if wrapped[i + 1][0] == pi:
            assert measure(ln) >= 0.88 * limit, ("주석 줄 채움 부족", ln[:20])
    # 필수 문구('잣대가 다르다')가 줄바꿈 과정에서 사라지지 않았는지
    assert any("잣대가 다르다" in ln for _pi, ln in wrapped)

    # 렌더링 후 텍스트 충돌·잘림 검사
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    bb = lambda t: t.get_window_extent(renderer=rend)
    fig_w = fig.canvas.get_width_height()[0]
    for t in notes:
        assert bb(t).x1 <= fig_w - 5, ("주석 우측 잘림", t.get_text()[:16])
    for t in right_notes:
        assert bb(t).x1 <= fig_w - 3, ("우측 병기 잘림", t.get_text()[:12])
    gap12 = bb(notes[0]).y0 - bb(notes[1]).y1
    gap23 = bb(notes[1]).y0 - bb(notes[2]).y1
    assert gap12 >= 2 and gap23 >= 2, ("주석 줄간 겹침", round(gap12, 1), round(gap23, 1))
    # 막대 안 라벨끼리 겹침 검사
    inbar = [t for t in ax.texts if t not in right_notes and t is not sep_note]
    for i in range(len(inbar)):
        for j in range(i + 1, len(inbar)):
            assert not bb(inbar[i]).overlaps(bb(inbar[j])), ("막대 라벨 겹침", i, j)
    print(f"layout checks passed: note gaps {gap12:.1f}/{gap23:.1f}px, bar labels clear")

    a.out.parent.mkdir(parents=True, exist_ok=True)
    # 실행시각(Date) 메타데이터를 제거한다. 바이트·픽셀 재현성 기준은 분석 README 참조
    fig.savefig(a.out, dpi=200, facecolor="white", metadata={"Date": None})
    print("wrote", a.out)


if __name__ == "__main__":
    main()
