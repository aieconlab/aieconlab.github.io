#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그림 1: SK하이닉스 2026년 2분기 매출 증가에서 ASP가 설명하는 몫 (전 분기 대비).

자료: SK하이닉스 2026년 2분기 실적 컨퍼런스콜(2026-07-29) 발언.
  - D램:  ASP 전 분기 대비 '약 30%' 상승, 출하량(빗그로스) '한 자릿수 후반' 증가
  - 낸드: ASP 전 분기 대비 '50% 중반' 상승, 출하량 '10% 중반' 증가

회사는 정량 수치를 공시하지 않고 정성 표현으로만 제시했다. 그래서 이 그림은
점추정이 아니라 **구간**으로 계산한다. 중심값과 함께 상·하한을 오차막대로 표시한다.
  D램  ASP 29~31%, 출하 7~9%
  낸드 ASP 54~56%, 출하 14~16%

분해 방법(trend15와 동일): 매출 배수 = ASP 배수 x 출하량 배수 이므로 로그를 취하면
  ln(매출배수) = ln(ASP배수) + ln(출하량배수)
ASP의 몫 = ln(ASP배수) / ln(매출배수).
ASP도 개당 단가도 제품 구성 변화를 포함하므로 순수한 가격 인상분과는 분리되지 않는다.

비교 대상으로 trend15가 중국 해관총서 상반기 통계에서 계산한 90.0%를 함께 놓는다
(다만 그쪽은 전년 동기 대비 누계·개수 기준이라 기준이 다르다 — 캡션에 명시).

사용법: python3 fig01_hynix_price_volume.py [--out PNG] [--font FONT]
의존성: matplotlib
인터프리터: /opt/anaconda3/bin/python3
"""
import argparse
from math import log
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
BLUE, NAVY, GRAY, NOTE, SPINE = "#2563eb", "#1b2a4a", "#8290a6", "#5a6472", "#c8cdd6"
AMBER = "#d97706"

# (이름, ASP 하한/중심/상한 %, 출하 하한/중심/상한 %)
ITEMS = [
    ("D램", (29, 30, 31), (7, 8, 9)),
    ("낸드", (54, 55, 56), (14, 15, 16)),
]
CHINA_SHARE = 90.0  # trend15: 중국 IC 수출액 증가 중 개당 단가의 몫


def price_share(asp_pct: float, vol_pct: float) -> float:
    """ASP가 매출 증가를 설명하는 몫(%)."""
    lp, lv = log(1 + asp_pct / 100), log(1 + vol_pct / 100)
    return lp / (lp + lv) * 100


def bounds(asp3, vol3):
    """중심값과, ASP 몫이 최소·최대가 되는 조합에서의 값."""
    mid = price_share(asp3[1], vol3[1])
    lo = price_share(asp3[0], vol3[2])   # ASP 최저 × 출하 최고 → 가격 몫 최소
    hi = price_share(asp3[2], vol3[0])   # ASP 최고 × 출하 최저 → 가격 몫 최대
    return lo, mid, hi


# --- 검산 -------------------------------------------------------------------
_d_lo, _d_mid, _d_hi = bounds(*ITEMS[0][1:])
_n_lo, _n_mid, _n_hi = bounds(*ITEMS[1][1:])
assert 74 < _d_lo < _d_mid < _d_hi < 81, (_d_lo, _d_mid, _d_hi)
assert 73 < _n_lo < _n_mid < _n_hi < 79, (_n_lo, _n_mid, _n_hi)
# 매출 배수 검산: D램 중심값 1.30 × 1.08 = 1.404
assert abs(1.30 * 1.08 - 1.404) < 1e-9
# 두 품목 모두 중국(90.0%)보다 가격 집중도가 낮다
assert _d_hi < CHINA_SHARE and _n_hi < CHINA_SHARE


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "out" / "fig01_hynix_price_volume.png")
    ap.add_argument("--font", default="Apple SD Gothic Neo")
    a = ap.parse_args()

    plt.rcParams["font.family"] = a.font
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(10, 5.8), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    labels, mids, los, his = [], [], [], []
    for name, asp3, vol3 in ITEMS:
        lo, mid, hi = bounds(asp3, vol3)
        labels.append(f"SK하이닉스 {name}\n(ASP)")
        mids.append(mid)
        los.append(mid - lo)
        his.append(hi - mid)
    labels.append("중국 집적회로 수출\n(개당 단가·기준 다름)")
    mids.append(CHINA_SHARE)
    los.append(0.0)
    his.append(0.0)

    y = list(range(len(labels)))[::-1]
    colors = [BLUE, BLUE, GRAY]
    bars = ax.barh(y, mids, height=0.52, color=colors, zorder=3)
    ax.errorbar(mids[:2], y[:2], xerr=[los[:2], his[:2]], fmt="none",
                ecolor=NAVY, elinewidth=1.6, capsize=6, capthick=1.6, zorder=4)

    for i, (yy, v) in enumerate(zip(y, mids)):
        if i < 2:
            lo, _, hi = bounds(*ITEMS[i][1:])
            txt = f"약 {v:.0f}%  ({lo:.0f}~{hi:.0f}%)"
            x = hi + 2.4          # 오차막대 상한 캡을 넘겨 배치
        else:
            txt = f"{v:.1f}%"
            x = v + 2.4
        ax.text(x, yy, txt, va="center", ha="left",
                fontsize=13, color=NAVY, fontweight="bold", zorder=5)

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=12.5, color=NAVY)
    ax.set_xlim(0, 108)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0", "25", "50", "75", "100%"], fontsize=11, color=NOTE)
    ax.set_xlabel("매출(수출액) 증가 가운데 개당 받는 금액이 설명하는 몫", fontsize=11.5, color=NOTE, labelpad=9)
    # 50% 기준선 — 눈금이 이미 '50'을 표시하므로 별도 라벨은 두지 않는다
    ax.axvline(50, color=SPINE, lw=1, ls=(0, (4, 4)), zorder=2)

    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(SPINE)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=SPINE, lw=0.6, alpha=0.5, zorder=1)
    ax.set_axisbelow(True)

    ax.set_title("개당 받는 금액이 설명하는 몫: 같은 잣대로 잰 세 개의 매출 증가",
                 fontsize=15.5, color=NAVY, fontweight="bold", loc="left", pad=16)

    fig.text(0.065, 0.035,
             "SK하이닉스는 전 분기 대비 2026년 2분기 ASP, 중국은 2026년 상반기 전년 동기 대비 누계 개당 단가. "
             "둘 다 제품 구성 변화가 섞여 있어 순수한 가격 인상분과 분리되지 않는다.",
             fontsize=9.5, color=NOTE)

    fig.subplots_adjust(left=0.24, right=0.97, top=0.83, bottom=0.20)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.out, dpi=200, facecolor="white", metadata={"Date": None})
    print("wrote", a.out)
    print(f"D램  ASP 몫: {_d_mid:.1f}% ({_d_lo:.1f}~{_d_hi:.1f})")
    print(f"낸드 ASP 몫: {_n_mid:.1f}% ({_n_lo:.1f}~{_n_hi:.1f})")


if __name__ == "__main__":
    main()
