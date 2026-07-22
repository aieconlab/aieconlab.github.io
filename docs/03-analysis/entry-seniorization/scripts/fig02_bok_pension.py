#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그림 2: 연령대별 국민연금 가입자 증감 — AI 고노출 vs 저노출 업종 (BOK 이슈노트 재구성).

수치 출처: 한국은행 BOK 이슈노트 제2025-30호(한진수·오삼일, 2025-10-30) <그림 4>에
인쇄된 값을 그대로 전사(만 명, 2022.7월 대비 2025.7월, 계절조정). 차트 픽셀 추정 없음.
원문 페이지: https://www.bok.or.kr/portal/bbs/P0002353/view.do?menuNo=200433&nttId=10094258
원문 PDF SHA-256: 4939c0e355c63d17d44a9b82da2b1013cfec568a70658f27dd7089214dfd0e96

  15~29세: 고노출(3~4분위) -20.8, 저노출(1~2분위) -0.4, 전체 -21.1
  30대:    고노출 +7.6,  저노출 +11.7, 전체 +19.4
  40대:    고노출 -6.1,  저노출 -5.8,  전체 -11.9
  50대:    고노출 +14.6, 저노출 +6.3,  전체 +20.9
  (연령대 합계와 노출도별 합의 차이는 원문 반올림)

사용법: python3 fig02_bok_pension.py [--out PNG] [--font FONT]
"""
import argparse
import datetime as dt
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
BLUE, GRAY, NAVY, NOTE, SPINE = "#2563eb", "#9aa5b8", "#1b2a4a", "#5a6472", "#c8cdd6"

AGES = ["청년층\n(15~29세)", "30대", "40대", "50대"]
HIGH = [-20.8, 7.6, -6.1, 14.6]   # AI 고노출(상위 3~4분위) 업종
LOW = [-0.4, 11.7, -5.8, 6.3]     # AI 저노출(하위 1~2분위) 업종
TOTAL = [-21.1, 19.4, -11.9, 20.9]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "out" / "fig02_bok_pension.png")
    ap.add_argument("--font", default="Apple SD Gothic Neo")
    a = ap.parse_args()

    plt.rcParams["font.family"] = a.font
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax = plt.subplots(figsize=(10, 7), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    y = np.arange(len(AGES))[::-1]  # 청년층 맨 위
    h = 0.32
    ax.barh(y + h / 2 + 0.02, HIGH, height=h, color=BLUE,
            label="AI 고노출 업종 (상위 3~4분위)", zorder=3)
    ax.barh(y - h / 2 - 0.02, LOW, height=h, color=GRAY,
            label="AI 저노출 업종 (하위 1~2분위)", zorder=3)

    for yy, v, c in ([(yi + h / 2 + 0.02, v, NAVY) for yi, v in zip(y, HIGH)]
                     + [(yi - h / 2 - 0.02, v, NOTE) for yi, v in zip(y, LOW)]):
        off = 0.6 if v >= 0 else -0.6
        ax.text(v + off, yy, f"{v:+.1f}", va="center",
                ha="left" if v >= 0 else "right",
                fontsize=15.5, color=c, fontweight="bold")

    ax.text(27.0, y[0] + 0.62, "전체 증감", va="center", ha="center",
            fontsize=13.5, color=NOTE)
    for yy, t in zip(y, TOTAL):
        ax.text(27.0, yy, f"{t:+.1f}", va="center", ha="center",
                fontsize=15.5, color=NAVY, fontweight="bold")

    ax.axvline(0, color=SPINE, lw=1.2, zorder=2)
    ax.set_yticks(y)
    ax.set_yticklabels(AGES, fontsize=16.5, color=NAVY)
    ax.set_xlim(-27, 31)
    ax.set_xticks(np.arange(-20, 21, 10))
    ax.set_xlabel("국민연금 가입자수 증감 (만 명)", fontsize=16, color=NAVY)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(SPINE)
    ax.tick_params(colors=NOTE, labelsize=15)
    for lbl in ax.get_yticklabels():
        lbl.set_color(NAVY)
    ax.xaxis.grid(True, color="#e8ebf0", lw=0.8, zorder=0)
    ax.set_axisbelow(True)

    ax.set_title("연령대별 국민연금 가입자 증감: AI 고노출 vs 저노출 업종",
                 loc="left", fontsize=21.5, fontweight="bold", color=NAVY, pad=42)
    ax.text(0, 1.05, "2022년 7월 → 2025년 7월 · 청년층 감소 21.1만 개 중 20.8만 개가 고노출 업종",
            transform=ax.transAxes, fontsize=14.5, color=NOTE)
    ax.legend(loc="lower left", frameon=False, fontsize=14, labelcolor=NAVY,
              bbox_to_anchor=(0.0, 0.02), handlelength=1.4)

    fig.subplots_adjust(left=0.15, right=0.97, top=0.85, bottom=0.17)
    today = dt.date.today().isoformat()
    fig.text(0.06, 0.075, "주: 산업 중분류·연령대별 가입자수(계절조정), 2022.7월 대비 2025.7월. 노출도 산정 방법은 본문 참조.",
             fontsize=12, color=NOTE, va="top")
    fig.text(0.06, 0.035, f"자료: BOK 이슈노트 No.2025-30(한진수·오삼일)에서 인용, <그림 4> ({today} 조회)  |  재구성: AIEconLab",
             fontsize=12, color=NOTE, va="top")

    a.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.out, dpi=200, facecolor="white")
    print("wrote", a.out)


if __name__ == "__main__":
    main()
