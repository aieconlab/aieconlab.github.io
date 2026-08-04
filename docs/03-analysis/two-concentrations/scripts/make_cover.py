#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""trend19 커버 이미지(1600x800) 생성. 사용법: python3 make_cover.py [--out PNG] [--font FONT]

좌측 수치(산업통상부 2026년 7월 수출입 동향, 2026-08-01 발표):
- 반도체 410.1억 달러 / 총수출 988.9억 달러 = 41.5% (계산값)
우측 수치(한국거래소 집계를 전재한 헤럴드경제 보도, 2026-07-28 종가):
- 삼성전자+SK하이닉스 시가총액 2,390.9조 원 = 코스피 전체의 50.02% (보통주 기준 판단)
"""
import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--out", type=Path, default=HERE / "out" / "trend19_cover.png")
ap.add_argument("--font", default="Apple SD Gothic Neo")
args = ap.parse_args()

plt.rcParams["font.family"] = args.font
plt.rcParams["axes.unicode_minus"] = False

NAVY = "#1b2a4a"
BLUE = "#2563eb"
GRAY = "#4b5563"
LGRAY = "#6b7280"
LINE = "#cbd5e1"

# 표시값은 하드코딩하지 않고 data/의 CSV에서 계산·대조한다
with open(HERE / ".." / "data" / "monthly_semiconductor_exports.csv", encoding="utf-8") as fh:
    rows = list(csv.DictReader(fh))
last = rows[-1]
assert last["month"] == "2026-07"
EXPORT_SHARE = round(float(last["semis_export_100m_usd"]) / float(last["total_export_100m_usd"]) * 100, 1)
assert EXPORT_SHARE == 41.5, EXPORT_SHARE

with open(HERE / ".." / "data" / "cap_share_milestones.csv", encoding="utf-8") as fh:
    caps = {r["date"]: float(r["share_pct"]) for r in csv.DictReader(fh)}
CAP_SHARE = caps["2026-07-28"]
assert CAP_SHARE == 50.02, CAP_SHARE

fig = plt.figure(figsize=(16, 8), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1600)
ax.set_ylim(0, 800)
ax.axis("off")
fig.patch.set_facecolor("white")

ax.text(80, 690, "AIEconLab", fontsize=22, color=LGRAY, fontweight="bold")

ax.text(80, 560, "수출의 41.5%는 반도체 한 품목,", fontsize=52, color=NAVY, fontweight="bold")
ax.text(80, 470, "시총의 절반은 두 종목", fontsize=52, color=NAVY, fontweight="bold")
ax.text(80, 385, "두 개의 집중도", fontsize=30, color=GRAY)

ax.plot([80, 1520], [330, 330], color=LINE, lw=2)

ax.text(80, 215, f"{EXPORT_SHARE}%", fontsize=64, color=BLUE, fontweight="bold")
ax.text(80, 145, "월 수출 중 반도체", fontsize=22, color=GRAY)
ax.text(80, 95, "2026년 7월, 산업통상부 발표치로 계산", fontsize=16, color=LGRAY)

ax.text(850, 215, f"{CAP_SHARE}%", fontsize=64, color=BLUE, fontweight="bold")
ax.text(850, 145, "코스피 시총 중 삼성전자+SK하이닉스", fontsize=22, color=GRAY)
ax.text(850, 95, "2026년 7월 28일 종가, 한국거래소 집계 전재 보도", fontsize=16, color=LGRAY)

args.out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(args.out, dpi=100, facecolor="white", metadata={"Date": None})
print("wrote", args.out)
