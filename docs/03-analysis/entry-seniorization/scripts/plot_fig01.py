#!/usr/bin/env python3
"""Fig 1: US recent college graduate unemployment vs other groups (NY Fed data)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

DATA = "/private/tmp/claude-501/-Users-hayun-Documents-Github-AIEconLab--claude-worktrees-ai-trends-july-17-1ce616/ae37edf6-cc22-4044-ad92-2e5d4cc51c0e/scratchpad/entry_seniorization/data/college-labor-unemployment-data.csv"
OUT = "/Users/hayun/Documents/Github_AIEconLab/.claude/worktrees/ai-trends-july-17-1ce616/static/images/post/entry_seniorization/fig01_us_recent_grads.png"

BLUE = "#2563eb"
MIDGRAY = "#9aa5b8"
LIGHTGRAY = "#cfd6e0"
NAVY = "#1b2a4a"
NOTEGRAY = "#5a6472"
SPINE = "#c8cdd6"

plt.rcParams["font.family"] = "Apple SD Gothic Neo"
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv(DATA, parse_dates=["Date"]).sort_values("Date")

fig, ax = plt.subplots(figsize=(10, 7), dpi=200)
fig.patch.set_facecolor("white")

# shade the current persistent inversion episode (gap > 0 for 12+ months): 2021-01 -> latest
ep_start = pd.Timestamp("2021-01-01")
ep_end = df.Date.max()
ax.axvspan(ep_start, ep_end, color=BLUE, alpha=0.07, zorder=0)

ax.plot(df.Date, df["College graduates"], color=LIGHTGRAY, lw=1.4, zorder=2)
ax.plot(df.Date, df["Young workers"], color=MIDGRAY, lw=1.4, zorder=3)
ax.plot(df.Date, df["All workers"], color=NAVY, lw=1.5, ls=(0, (4, 2)), zorder=4)
ax.plot(df.Date, df["Recent graduates"], color=BLUE, lw=2.4, zorder=5)

# line-end labels with latest values
last = df.iloc[-1]
x_txt = ep_end + pd.DateOffset(months=5)
labels = [
    ("Young workers", "청년 비대졸(22-27세) {:.1f}%", MIDGRAY, 0.55),
    ("Recent graduates", "신규 대졸자(22-27세) {:.1f}%", BLUE, 0.0),
    ("All workers", "전체 근로자(16-65세) {:.1f}%", NAVY, -0.45),
    ("College graduates", "대졸 전체(22-65세) {:.1f}%", "#8a93a6", -0.95),
]
for col, fmt, color, dy in labels:
    ax.text(x_txt, last[col] + dy, fmt.format(last[col]),
            color=color, fontsize=10.5, fontweight="bold", va="center", ha="left")

# episode annotation inside the shaded band
ax.text(pd.Timestamp("2023-08-01"), 21.6, "2021년 1월 이후\n63개월 연속 역전",
        color=BLUE, fontsize=10.5, ha="center", va="top")

ax.set_xlim(pd.Timestamp("1989-06-01"), pd.Timestamp("2034-06-01"))
ax.set_ylim(0, 23)
ax.set_yticks([0, 4, 8, 12, 16, 20])
ax.set_xticks([pd.Timestamp(f"{y}-01-01") for y in range(1990, 2030, 5)])
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.set_ylabel("실업률 (%)", fontsize=12, color=NAVY)

ax.set_title("미국 신규 대졸자의 실업률이 전체 근로자를 웃돌고 있다",
             loc="left", fontsize=16, fontweight="bold", color=NAVY, pad=16)

for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(SPINE)
ax.tick_params(colors=NOTEGRAY, labelsize=10.5)
ax.grid(axis="y", color=SPINE, lw=0.6, alpha=0.55)
ax.set_axisbelow(True)

fig.subplots_adjust(left=0.075, right=0.975, top=0.90, bottom=0.175)

note1 = ("주: 뉴욕 연은 정의 — 신규 대졸자=22-27세 학사 이상, 청년 비대졸=22-27세 학사 미만, 전체 근로자=16-65세,"
         " 대졸 전체=22-65세 학사 이상(재학생 제외).")
note2 = ("     실업률은 계절조정·3개월 이동평균(월별). 음영은 신규 대졸자 실업률이 전체 근로자를"
         " 12개월 이상 연속 상회 중인 기간(2021.1~2026.3).")
note3 = "자료: 뉴욕 연방준비은행 College Labor Market (2026-07-22 조회)  |  계산: AIEconLab"
fig.text(0.075, 0.085, note1, fontsize=9, color=NOTEGRAY)
fig.text(0.075, 0.055, note2, fontsize=9, color=NOTEGRAY)
fig.text(0.075, 0.02, note3, fontsize=9, color=NOTEGRAY)

fig.savefig(OUT, dpi=200, facecolor="white")
print("saved:", OUT)
