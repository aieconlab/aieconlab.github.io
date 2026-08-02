#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""trend18 그림 3종 생성: 커버(1600x800), 그림1 일정 변경(2000x1200), 그림2 한·EU 시간표(2000x1080).

- 커버의 서명 수치(83·152·매칭 0건)는 ../data/match_results.json에서 읽어 검산한다.
- 일정 날짜는 Regulation (EU) 2026/1744(관보 2026-07-24, 발효 2026-07-27)와
  EU 집행위 공지, 한국은 과기정통부·정책브리핑 발표 기준(절대 날짜 하드코딩).
- 실행시각(Date) 메타데이터를 제거해 재현성을 확보한다.

인터프리터: /opt/anaconda3/bin/python3
사용법: python3 make_figures.py   (이 파일이 있는 디렉터리에서; 출력은 out/)
"""
import json
from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, Rectangle

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

plt.rcParams["font.family"] = "Apple SD Gothic Neo"
plt.rcParams["axes.unicode_minus"] = False

NAVY = "#1b2a4a"
BLUE = "#2563eb"
GRAY = "#4b5563"
LGRAY = "#6b7280"
STEPGRAY = "#cbd5e1"
AXGRAY = "#9ca3af"

# ---- 확정 수치: 서명 집계는 대조 결과 파일에서 읽어 검산 ----
res = json.loads((HERE / ".." / "data" / "match_results.json").read_text(encoding="utf-8"))
S1 = res["counts"]["section1"]
S2 = res["counts"]["section2"]
HITS = sum(len(m["hits"]) for m in res["matches"])
if (S1, S2, HITS) != (83, 152, 0):
    raise SystemExit(f"대조 결과가 바뀌었다: {(S1, S2, HITS)}")


# ============================== 커버 (1600x800) ==============================
def make_cover() -> None:
    fig = plt.figure(figsize=(16, 8), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 800)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.add_patch(Rectangle((0, 760), 1600, 40, color=BLUE, zorder=5))

    LX = 183
    left_texts = [
        ax.text(LX, 555, f"서명 약 190곳, 국내 29종 검색 매칭 0건", fontsize=34, color=NAVY,
                fontweight="bold", va="center", ha="left"),
        ax.text(LX, 442, "8월 2일 EU AI법에서 실제로 시작된 것", fontsize=21,
                color=BLUE, va="center", ha="left", fontweight="medium"),
        ax.text(LX, 300, "투명성 의무 적용과 범용 AI 집행이 시작됐다\n"
                         "고위험·샌드박스 일정은 2027년 이후로 연기\n"
                         "국내 주요 기업·서비스 29종 대조, 매칭 0건",
                fontsize=16.5, color=GRAY, va="center", ha="left", linespacing=1.9),
        ax.text(LX, 185, "EU 투명성 행동강령 최초 서명자 명단 (2026-07-31 공개)", fontsize=14,
                color=LGRAY, va="center", ha="left"),
        ax.text(LX, 78, "AIEconLab · 인공지능경제연구소", fontsize=15.5,
                color=BLUE, va="center", ha="left", fontweight="medium"),
    ]

    # 우측 그래픽: 섹션별 서명 건수와 국내 검색 매칭 0건
    ax.text(1190, 706, "투명성 행동강령 서명 (2026-07-31 명단, 건)",
            fontsize=15, color=GRAY, ha="center", va="center")
    base_y = 150
    px_per = 420.0 / S2
    bw = 130
    bars = [(985, S1, BLUE, f"제공자 섹션\n{S1}건", 17, BLUE, "bold"),
            (1175, S2, BLUE, f"배포자 섹션\n{S2}건", 17, BLUE, "bold"),
            (1365, HITS, NAVY, f"국내 검색 매칭\n{HITS}건", 17, NAVY, "bold")]
    for bx, val, color, label, fs, lc, fw in bars:
        h = val * px_per
        if val > 0:
            ax.add_patch(Rectangle((bx, base_y), bw, h, color=color, zorder=3))
        else:  # 0건은 굵은 밑금으로 부재를 표시
            ax.add_patch(Rectangle((bx, base_y), bw, 5, color=color, zorder=3))
        ax.text(bx + bw / 2, base_y + max(h, 5) + 30, label, fontsize=fs, color=lc,
                ha="center", va="bottom", fontweight=fw, linespacing=1.4)
    ax.plot([930, 1495 + 55 - 55], [base_y, base_y], color=AXGRAY, lw=1.2, zorder=2)

    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    for t in left_texts:
        x1 = t.get_window_extent(renderer=rend).x1
        assert x1 < 930, ("좌측 텍스트가 그래픽 영역 침범", t.get_text()[:14], round(x1))

    fig.savefig(OUT / "trend18_cover.png", metadata={"Date": None})
    plt.close(fig)
    print("wrote", OUT / "trend18_cover.png")


# =================== 그림 1: 일정 변경 덤벨 (2000x1200) ===================
def make_fig01() -> None:
    rows = [  # (라벨, 종전, 개정 후) — 개정 후가 None이면 유지
        ("투명성 의무 (제50조)", date(2026, 8, 2), None),
        ("고위험 독립형 (부속서 III)", date(2026, 8, 2), date(2027, 12, 2)),
        ("고위험 제품 내장형 (부속서 I)", date(2027, 8, 2), date(2028, 8, 2)),
        ("회원국 샌드박스 기한 (제57조)", date(2026, 8, 2), date(2027, 8, 2)),
        ("기존 시스템 표식 경과기간 (제50조 2항)", date(2026, 8, 2), date(2026, 12, 2)),
    ]
    fig, ax = plt.subplots(figsize=(10, 6.0), dpi=200)
    fig.subplots_adjust(left=0.30, right=0.97, top=0.82, bottom=0.16)
    ys = list(range(len(rows), 0, -1))
    for y, (label, old, new) in zip(ys, rows):
        ax.axhline(y, color="#eef1f5", lw=1, zorder=1)
        if new is None:
            ax.plot([old], [y], "o", color=BLUE, ms=9, zorder=4)
            ax.annotate("2026-08-02 유지", (mdates.date2num(old), y),
                        xytext=(14, 0), textcoords="offset points",
                        fontsize=10.5, color=BLUE, va="center", fontweight="bold")
        else:
            ax.plot([old], [y], "o", color=STEPGRAY, ms=8, zorder=3)
            ax.plot([new], [y], "o", color=BLUE, ms=9, zorder=4)
            ax.add_patch(FancyArrowPatch(
                (mdates.date2num(old), y), (mdates.date2num(new), y),
                arrowstyle="-|>", mutation_scale=13, color=AXGRAY, lw=1.4,
                shrinkA=7, shrinkB=7, zorder=2))
            ax.annotate(new.isoformat(), (mdates.date2num(new), y),
                        xytext=(14, 0), textcoords="offset points",
                        fontsize=10.5, color=GRAY, va="center")
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=11.5, color=NAVY)
    ax.set_ylim(0.4, len(rows) + 0.9)

    apply_day = mdates.date2num(date(2026, 8, 2))
    ax.axvline(apply_day, color=NAVY, lw=1.1, ls=(0, (4, 3)), zorder=2)
    ax.text(apply_day, len(rows) + 0.62, " 일반 적용일 2026-08-02", fontsize=10.5,
            color=NAVY, ha="left", va="center", fontweight="bold")

    ax.set_xlim(mdates.date2num(date(2026, 5, 1)), mdates.date2num(date(2029, 2, 1)))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y년"))
    ax.tick_params(axis="x", colors=GRAY, labelsize=11)
    ax.tick_params(axis="y", length=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(AXGRAY)

    ax.legend(handles=[
        Line2D([], [], marker="o", ls="", color=STEPGRAY, ms=8, label="종전 일정"),
        Line2D([], [], marker="o", ls="", color=BLUE, ms=9, label="개정 후 일정"),
    ], loc="upper right", frameon=False, fontsize=10.5, bbox_to_anchor=(1.0, 1.13))

    fig.text(0.06, 0.945, "엿새 전에 확정된 새 일정표: EU AI법 주요 일정 비교",
             fontsize=15.5, color=NAVY, fontweight="bold", ha="left")
    fig.text(0.06, 0.045, "개정 규정(Regulation (EU) 2026/1744)은 2026년 7월 24일 관보 게재, 7월 27일 발효했다.\n"
                          "마지막 행은 2026년 8월 2일 이전 출시된 생성형 AI 시스템의 기계 판독 가능 표식 의무에 적용되는 경과기간이다.",
             fontsize=9.5, color=LGRAY, ha="left", va="bottom", linespacing=1.6)
    fig.savefig(OUT / "fig01_schedule_shift.png", dpi=200, facecolor="white",
                metadata={"Date": None})
    plt.close(fig)
    print("wrote", OUT / "fig01_schedule_shift.png")


# ================= 그림 2: 한·EU 시행-집행 시간표 (2000x1080) =================
def make_fig02() -> None:
    fig, ax = plt.subplots(figsize=(10, 5.4), dpi=200)
    fig.subplots_adjust(left=0.17, right=0.965, top=0.80, bottom=0.17)
    x0, x1 = mdates.date2num(date(2024, 4, 1)), mdates.date2num(date(2028, 1, 1))

    for y in (2, 1):
        ax.axhline(y, color="#e5e9f0", lw=1.6, zorder=1)

    # EU 트랙 (y=2)
    eu_events = [
        (date(2024, 8, 1), "발효", False),
        (date(2025, 8, 2), "범용 AI 의무 적용", False),
        (date(2026, 8, 2), "일반 적용·집행 개시", True),
    ]
    for d, label, em in eu_events:
        ax.plot([d], [2], "o", color=BLUE, ms=10 if em else 8, zorder=4)
        ax.annotate(f"{label}\n{d.isoformat()}", (mdates.date2num(d), 2),
                    xytext=(0, 13), textcoords="offset points", fontsize=10.5,
                    color=BLUE if em else GRAY, ha="center", va="bottom",
                    fontweight="bold" if em else "normal", linespacing=1.4,
                    zorder=6, bbox=dict(facecolor="white", edgecolor="none", pad=1.5))

    # 한국 트랙 (y=1): 시행 + 계도기간 최소 1년(연장 가능)
    kr_start = date(2026, 1, 22)
    kr_min_end = date(2027, 1, 22)
    ax.add_patch(Rectangle((mdates.date2num(kr_start), 1 - 0.09),
                           mdates.date2num(kr_min_end) - mdates.date2num(kr_start), 0.18,
                           color=STEPGRAY, alpha=0.65, zorder=2))
    ax.add_patch(FancyArrowPatch(
        (mdates.date2num(kr_min_end), 1), (mdates.date2num(date(2027, 8, 1)), 1),
        arrowstyle="-|>", mutation_scale=12, color=AXGRAY, lw=1.3,
        ls=(0, (4, 3)), zorder=2))
    ax.plot([kr_start], [1], "o", color=BLUE, ms=10, zorder=4)
    ax.annotate(f"시행 (의무·제재 효력 발생)\n{kr_start.isoformat()}",
                (mdates.date2num(kr_start), 1), xytext=(0, 13),
                textcoords="offset points", fontsize=10.5, color=BLUE,
                ha="center", va="bottom", fontweight="bold", linespacing=1.4)
    mid = mdates.date2num(kr_start) + (mdates.date2num(kr_min_end) - mdates.date2num(kr_start)) / 2
    ax.text(mid, 1 - 0.19, "계도기간 최소 1년: 제재 원칙적 최소화", fontsize=10,
            color=GRAY, ha="center", va="top", zorder=6,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
    ax.text(mdates.date2num(date(2027, 4, 15)), 1 - 0.19, "연장 가능", fontsize=10,
            color=LGRAY, ha="center", va="top")

    apply_day = mdates.date2num(date(2026, 8, 2))
    ax.axvline(apply_day, color=NAVY, lw=1.1, ls=(0, (4, 3)), zorder=3)

    ax.set_yticks([2, 1])
    ax.set_yticklabels(["EU AI법", "한국 AI기본법"], fontsize=12.5, color=NAVY,
                       fontweight="bold")
    ax.set_ylim(0.45, 2.75)
    ax.set_xlim(x0, x1)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y년"))
    ax.tick_params(axis="x", colors=GRAY, labelsize=11)
    ax.tick_params(axis="y", length=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(AXGRAY)

    fig.text(0.06, 0.935, "시행일과 집행 방침: 한국 AI기본법과 EU AI법의 시간표",
             fontsize=15.5, color=NAVY, fontweight="bold", ha="left")
    fig.text(0.06, 0.04, "세로 점선은 2026년 8월 2일(EU 일반 적용일). 한국의 계도기간은 과기정통부가 밝힌 최소 기간이며 연장 가능성이 열려 있고,\n"
                         "중대한 사회적 피해가 우려되는 경우의 제한적 조사·제재 가능성은 계도기간 중에도 남는다.",
             fontsize=9.5, color=LGRAY, ha="left", va="bottom", linespacing=1.6)
    fig.savefig(OUT / "fig02_kr_eu_timeline.png", dpi=200, facecolor="white",
                metadata={"Date": None})
    plt.close(fig)
    print("wrote", OUT / "fig02_kr_eu_timeline.png")


make_cover()
make_fig01()
make_fig02()
