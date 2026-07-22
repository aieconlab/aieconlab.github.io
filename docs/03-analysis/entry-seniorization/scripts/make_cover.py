#!/usr/bin/env python3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams["font.family"] = "Apple SD Gothic Neo"

NAVY = "#1b2a4a"
BLUE = "#2563eb"
GRAY = "#4b5563"
LGRAY = "#6b7280"
STEPGRAY = "#cbd5e1"

fig = plt.figure(figsize=(16, 8), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1600)
ax.set_ylim(0, 800)
ax.axis("off")
ax.set_facecolor("white")
fig.patch.set_facecolor("white")

# top blue bar
ax.add_patch(Rectangle((0, 760), 1600, 40, color=BLUE, zorder=5))

# ---- left text column ----
LX = 183
ax.text(LX, 555, "첫 계단은 높아졌나", fontsize=42, color=NAVY,
        fontweight="bold", va="center", ha="left")
ax.text(LX, 442, "신입 일자리 시니어화의 증거와 빈칸", fontsize=21,
        color=BLUE, va="center", ha="left", fontweight="medium")

ax.text(LX, 300, "신입 채용은 줄고 요구 경력은 올라간다는 신호들\n"
                 "첫 계단이 정말 높아졌는지, 증거와 남은 빈칸을 짚는다",
        fontsize=16.5, color=GRAY, va="center", ha="left", linespacing=1.9)

ax.text(LX, 185, "채용공고·고용 데이터가 가리키는 진입장벽", fontsize=14,
        color=LGRAY, va="center", ha="left")

ax.text(LX, 78, "AIEconLab · 인공지능경제연구소", fontsize=15.5,
        color=BLUE, va="center", ha="left", fontweight="medium")

# ---- right graphic: staircase with raised first step ----
# label
ax.text(1185, 650, "커리어 사다리", fontsize=16, color=GRAY,
        ha="center", va="center")

base_y = 135
x0 = 930
step_w = 128
# first step conspicuously tall, then small uniform increments (staircase)
heights = [250, 312, 374, 436]
colors = [BLUE, STEPGRAY, STEPGRAY, STEPGRAY]
for i, (h, c) in enumerate(zip(heights, colors)):
    ax.add_patch(Rectangle((x0 + i * step_w, base_y), step_w, h,
                           color=c, zorder=3))
# thin white seams between steps so contiguous blocks still read as steps
for i in range(1, 4):
    ax.plot([x0 + i * step_w, x0 + i * step_w],
            [base_y, base_y + heights[i - 1]], color="white", lw=3, zorder=4)

# baseline
ax.plot([x0 - 46, x0 + 4 * step_w + 40], [base_y, base_y],
        color="#9ca3af", lw=1.2, zorder=2)

# annotate first step
ax.text(x0 + step_w / 2, base_y + heights[0] + 36, "첫 계단",
        fontsize=17, color=BLUE, ha="center", va="center", fontweight="bold")
# dashed line showing where the first step "used to be"
old_h = 88
# navy dashes left of the bar, white dashes across the blue bar for contrast
ax.plot([x0 - 38, x0], [base_y + old_h, base_y + old_h],
        color=NAVY, lw=1.6, ls=(0, (5, 4)), zorder=5)
ax.plot([x0, x0 + step_w], [base_y + old_h, base_y + old_h],
        color="white", lw=1.6, ls=(0, (5, 4)), zorder=5)
ax.text(x0 - 50, base_y + old_h, "이전", fontsize=13, color=NAVY,
        ha="right", va="center")
# gap arrow: how much the first step has risen
ax.annotate("", xy=(x0 - 90, base_y + heights[0]),
            xytext=(x0 - 90, base_y + old_h),
            arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.6), zorder=5)
ax.plot([x0 - 38, x0], [base_y + heights[0], base_y + heights[0]],
        alpha=0)  # keep layout
ax.plot([x0 - 100, x0 - 4], [base_y + heights[0], base_y + heights[0]],
        color=BLUE, lw=1.2, ls=(0, (2, 3)), zorder=5)
ax.plot([x0 - 100, x0 - 44], [base_y + old_h, base_y + old_h],
        color=BLUE, lw=1.2, ls=(0, (2, 3)), zorder=5, alpha=0)

fig.savefig("/Users/hayun/Documents/Github_AIEconLab/.claude/worktrees/ai-trends-july-17-1ce616/assets/images/post/entry_seniorization_cover.png")
print("saved")
