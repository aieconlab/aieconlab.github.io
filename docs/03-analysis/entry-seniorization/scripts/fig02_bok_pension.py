# -*- coding: utf-8 -*-
"""
fig02_bok_pension.png
BOK 이슈노트 제2025-30호 <그림 4> 'AI 노출도에 따른 연령대별 고용 증감' 재구성.
수치 출처: 한진수·오삼일 (2025), "AI 확산과 청년고용 위축: 연공편향(seniority-biased)
기술변화를 중심으로", BOK 이슈노트 제2025-30호, p.6 <그림 4> (인쇄된 값만 사용).
기간: 22.7월 대비 25.7월 (계절조정), 단위: 만 명.
  15~29세: 상위(3~4분위) -20.8, 하위(1~2분위) -0.4, 전체 -21.1
  30대:    상위 +7.6,  하위 +11.7, 전체 +19.4
  40대:    상위 -6.1,  하위 -5.8,  전체 -11.9
  50대:    상위 +14.6, 하위 +6.3,  전체 +20.9
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "Apple SD Gothic Neo"
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#2563eb"
GRAY = "#9aa5b8"
NAVY = "#1b2a4a"
NOTE = "#5a6472"
SPINE = "#c8cdd6"

ages = ["청년층\n(15~29세)", "30대", "40대", "50대"]
high = [-20.8, 7.6, -6.1, 14.6]   # AI 고노출(상위 3~4분위) 업종
low = [-0.4, 11.7, -5.8, 6.3]     # AI 저노출(하위 1~2분위) 업종
total = [-21.1, 19.4, -11.9, 20.9]

fig, ax = plt.subplots(figsize=(10, 7), dpi=200)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

y = np.arange(len(ages))[::-1]  # 청년층 맨 위
h = 0.32

b1 = ax.barh(y + h / 2 + 0.02, high, height=h, color=BLUE,
             label="AI 고노출 업종 (노출도 상위 3~4분위)", zorder=3)
b2 = ax.barh(y - h / 2 - 0.02, low, height=h, color=GRAY,
             label="AI 저노출 업종 (노출도 하위 1~2분위)", zorder=3)

# 값 레이블 (고노출: 남색, 저노출: 회색톤)
for yy, v, c in ([(yi + h / 2 + 0.02, v, NAVY) for yi, v in zip(y, high)]
                 + [(yi - h / 2 - 0.02, v, NOTE) for yi, v in zip(y, low)]):
    off = 0.5 if v >= 0 else -0.5
    ax.text(v + off, yy, f"{v:+.1f}", va="center",
            ha="left" if v >= 0 else "right",
            fontsize=11.5, color=c, fontweight="bold")

# 연령대별 전체 증감 주석 (오른쪽 여백)
ax.text(27.0, y[0] + 0.62, "전체 증감", va="center", ha="center",
        fontsize=10, color=NOTE)
for yy, t in zip(y, total):
    ax.text(27.0, yy, f"{t:+.1f}", va="center", ha="center",
            fontsize=11.5, color=NAVY, fontweight="bold")

ax.axvline(0, color=SPINE, lw=1.2, zorder=2)

ax.set_yticks(y)
ax.set_yticklabels(ages, fontsize=13, color=NAVY)
ax.set_xlim(-27, 31)
ax.set_xticks(np.arange(-20, 21, 10))
ax.set_xlabel("국민연금 가입자수 증감 (만 명)", fontsize=11.5, color=NAVY)

ax.spines[["top", "right"]].set_visible(False)
ax.spines[["left", "bottom"]].set_color(SPINE)
ax.tick_params(colors=NOTE, labelsize=11)
for lbl in ax.get_yticklabels():
    lbl.set_color(NAVY)
ax.xaxis.grid(True, color="#e8ebf0", lw=0.8, zorder=0)
ax.set_axisbelow(True)

ax.set_title("연령대별 국민연금 가입자 증감: AI 고노출 vs 저노출 업종",
             loc="left", fontsize=16, fontweight="bold", color=NAVY, pad=34)
ax.text(0, 1.045, "2022년 7월 → 2025년 7월 · 청년층 일자리 감소 21.1만 개 중 20.8만 개가 AI 고노출 업종에서 발생",
        transform=ax.transAxes, fontsize=11, color=NOTE)

ax.legend(loc="lower left", frameon=False, fontsize=10.5, labelcolor=NAVY,
          bbox_to_anchor=(0.0, 0.02), handlelength=1.4)

fig.subplots_adjust(left=0.15, right=0.97, top=0.87, bottom=0.20)

fig.text(0.06, 0.09,
         "주: 국민연금 가입자수(산업 중분류·연령대별, 계절조정) 기준, 2022.7월 대비 2025.7월 증감. AI 노출도는 Felten et al.(2021)의\n"
         "     AIOE를 업종 내 직업분포(2024년 상반기 지역별고용조사)로 가중평균해 75개 업종에 적용, 상위 50%(3~4분위)를 고노출로 구분",
         fontsize=9, color=NOTE, va="top")
fig.text(0.06, 0.035,
         "자료: 한국은행, BOK 이슈노트 제2025-30호 <그림 4> (2026-07-22 조회)  |  재구성: AIEconLab",
         fontsize=9, color=NOTE, va="top")

out = "/Users/hayun/Documents/Github_AIEconLab/.claude/worktrees/ai-trends-july-17-1ce616/static/images/post/entry_seniorization/fig02_bok_pension.png"
import os
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out, dpi=200, facecolor="white")
print("saved:", out)
