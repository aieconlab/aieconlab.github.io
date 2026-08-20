#!/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""
trend21 '국가대표 AI 2차 평가' 그림 생성 스크립트.

입력: 과기정통부 보도자료(2025-08-04, 2026-01-15, 2026-02-20, 2026-08-18)·보도설명자료(2026-08-20)
      원문 수치와 ../data/aaii_snapshot.json (Artificial Analysis 2026-08-18 조회값).
출력: 본문 그림 3종은 ../../../../static/images/post/dokpamo_eval/ (관례: 본문 그림은 static),
      표지는 ../../../../assets/images/post/trend21_cover.png (표지는 assets).
파일명은 본문 그림 번호와 일치한다: fig01_tournament=그림 1, fig02_weights=그림 2, fig03_aaii=그림 3.
모바일 가독성: 세 그림 모두 세로형·단순 구성으로 나누고 그림 안 최소 글꼴을 14.5pt 이상(핵심 값 18pt+)으로
유지한다(본문 표시 폭 기준). 출처·긴 주석은 그림이 아니라 본문 캡션이 담당한다.
입력 검증: 필수 값의 존재와 숫자형·유한값 검증을 첫 savefig 전에 모두 마친다(파일 단위의 원자적 교체까지 보장하지는 않는다).
재현성: savefig(metadata={"Date": None}), 생성 인터프리터 /opt/anaconda3/bin/python3
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "..", "data")
OUT = os.path.join(BASE, "..", "..", "..", "..", "static", "images", "post", "dokpamo_eval")
COVER_OUT = os.path.join(BASE, "..", "..", "..", "..", "assets", "images", "post")
os.makedirs(OUT, exist_ok=True)

# ---------- 입력 로드·검증 (그림을 쓰기 전에 전부 끝낸다) ----------
with open(os.path.join(DATA, "aaii_snapshot.json"), encoding="utf-8") as f:
    snap = json.load(f)
KM = snap["korean_models"]; RM = snap["reference_models"]
import math
def _check(d, k):
    assert k in d and "intelligence_index" in d[k], f"입력 누락: {k}"
    v = d[k]["intelligence_index"]
    assert isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v), \
        f"입력이 유한한 숫자가 아님: {k}={v!r}"
for k in ["motif-3", "solar-open2-250b", "a-x-k2", "k-exaone-2-0-0803"]:
    _check(KM, k)
for k in ["claude-opus-5", "gpt-5-6-sol", "kimi-k3", "deepseek-v4-pro"]:
    _check(RM, k)

for cand in ["Apple SD Gothic Neo", "AppleGothic", "NanumGothic"]:
    if any(f.name == cand for f in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = cand
        break
plt.rcParams["axes.unicode_minus"] = False

GRAY = "#9AA5B1"
LIGHT = "#D9DEE4"
BLUE = "#2F5D8C"
DARK = "#1B3A5C"
RED = "#B4533A"
TEXT = "#333333"
MUTE = "#6B7785"

# ---------- 그림 1: 압축 토너먼트 (세로 나열형 가로 막대) ----------
# (단계, 날짜, 남은 팀 수) — 전부 보도자료 원문 수치. 마지막 '2'는 종전 계획(미확정).
stages = [
    ("공모 접수", "2025.7.21", 15),
    ("서면평가", "2025.7.25", 10),
    ("발표평가", "2025.8.4", 5),
    ("1차 단계평가", "2026.1.15", 3),
    ("추가 공모", "2026.2.20", 4),
    ("2차 단계평가", "2026.8.18", 3),
    ("3차 단계평가", "방식 협의 중", 2),
]
cols = [GRAY, GRAY, BLUE, BLUE, GRAY, RED, LIGHT]
fig, ax = plt.subplots(figsize=(7.2, 8.0))
ypos = list(range(len(stages)))[::-1]
vals = [s[2] for s in stages]
bars = ax.barh(ypos, vals, color=cols, height=0.6)
bars[-1].set_edgecolor(GRAY)
bars[-1].set_linestyle((0, (4, 3)))
bars[-1].set_linewidth(1.6)
for y, v, c in zip(ypos, vals, cols):
    ax.text(v + 0.3, y, str(v), va="center", fontsize=21, fontweight="bold",
            color=DARK if c != LIGHT else MUTE)
ax.text(vals[-1] + 1.5, ypos[-1], "종전 계획(미확정)", va="center", fontsize=15.5, color=MUTE)
ax.text(vals[3] + 1.5, ypos[3], "네이버클라우드\n'독자성 기준 미충족'\n(점수 상위 4팀 안이었음)",
        va="center", fontsize=15, color=BLUE, linespacing=1.25)
ax.text(vals[5] + 1.5, ypos[5], "모티프테크놀로지스 탈락\nAAII 47점(4팀 중 1위)\n'근소한 차이'",
        va="center", fontsize=15, color=RED, linespacing=1.25)
ax.set_yticks(ypos)
ax.set_yticklabels([f"{n}\n{d}" for n, d, _ in stages], fontsize=16, linespacing=1.2)
ax.set_xlim(0, 16.5)
ax.set_xticks([])
for sp in ["top", "right", "bottom"]:
    ax.spines[sp].set_visible(False)
ax.spines["left"].set_color("#CCCCCC")
ax.set_title("15팀에서 3팀까지:\n단계마다 잣대가 달랐다", fontsize=19, pad=14, linespacing=1.25)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig01_tournament.png"), dpi=170, metadata={"Date": None})
plt.close(fig)

# ---------- 그림 2: 배점 100점 구성 (가로 누적 막대 단독) ----------
parts = [("AAII\n25", 25, RED), ("NIA\n15", 15, "#C9A79A"), ("전문가\n35", 35, BLUE), ("사용자\n25", 25, DARK)]
fig, ax = plt.subplots(figsize=(7.2, 3.5))
left = 0
for name, v, c in parts:
    ax.barh([0], [v], left=left, color=c, height=0.6, edgecolor="white", linewidth=1.4)
    ax.text(left + v / 2, 0, name, ha="center", va="center", fontsize=19, color="white",
            fontweight="bold", linespacing=1.1)
    left += v
ax.plot([0.4, 24.6], [-0.48, -0.48], color=RED, lw=2)
ax.plot([25.4, 99.6], [-0.48, -0.48], color=DARK, lw=2)
ax.text(12.5, -0.62, "국제 지수 25점", ha="center", va="top", fontsize=17, color=RED, fontweight="bold")
ax.text(62.5, -0.62, "AAII 외 75점", ha="center", va="top", fontsize=17, color=DARK, fontweight="bold")
ax.set_xlim(0, 100)
ax.set_ylim(-1.15, 0.75)
ax.set_xticks([0, 25, 50, 75, 100])
ax.tick_params(axis="x", labelsize=15)
ax.set_yticks([])
ax.set_title("2차 단계평가 배점 100점", fontsize=19, pad=12)
for sp in ["top", "right", "left"]:
    ax.spines[sp].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig02_weights.png"), dpi=170, metadata={"Date": None})
plt.close(fig)

# ---------- 그림 3: AAII 점수 (가로 막대 단독) ----------
# 점수는 aaii_snapshot.json(사이트 조회값)을 반올림해 쓴다. 모티프3 47과 상위 모델 값은
# 보도자료 표의 정수 표기와 일치함을 extract 스크립트가 검증한다.
kr = [("모티프3\n(모티프테크놀로지스)", round(KM["motif-3"]["intelligence_index"]), RED),
      ("솔라 오픈2\n(업스테이지)", round(KM["solar-open2-250b"]["intelligence_index"]), BLUE),
      ("A.X K2\n(SK텔레콤)", round(KM["a-x-k2"]["intelligence_index"]), BLUE),
      ("K-엑사원 2.0\n(LG AI연구원)", round(KM["k-exaone-2-0-0803"]["intelligence_index"]), BLUE)]
ref = [("클로드 오퍼스 5", round(RM["claude-opus-5"]["intelligence_index"])),
       ("GPT-5.6 솔", round(RM["gpt-5-6-sol"]["intelligence_index"])),
       ("Kimi K3", round(RM["kimi-k3"]["intelligence_index"])),
       ("딥시크 V4 프로", round(RM["deepseek-v4-pro"]["intelligence_index"]))]
labels = [k[0] for k in kr] + [r[0] for r in ref]
vals = [k[1] for k in kr] + [r[1] for r in ref]
colors = [k[2] for k in kr] + [LIGHT] * len(ref)
fig, ax = plt.subplots(figsize=(7.2, 7.6))
ypos = list(range(len(labels)))[::-1]
ax.barh(ypos, vals, color=colors, height=0.62)
for y, v in zip(ypos, vals):
    ax.text(v + 1.2, y, f"{v}", va="center", fontsize=19, color=TEXT)
ax.set_yticks(ypos)
ax.set_yticklabels(labels, fontsize=15.5, linespacing=1.2)
ax.set_xlim(0, 88)
ax.set_xticks([0, 20, 40, 60])
ax.tick_params(axis="x", labelsize=15)
ax.axhline(3.5, color="#BBBBBB", lw=1, ls="--")
ax.text(87, 3.7, "국내 4팀 ↑", ha="right", va="bottom", fontsize=14.5, color=MUTE)
ax.text(87, 3.3, "비교 대상 ↓", ha="right", va="top", fontsize=14.5, color=MUTE)
ax.set_title("AAII 점수(2026.8, 정수 표기)\n붉은색이 탈락 팀", fontsize=19, pad=12, linespacing=1.25)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig03_aaii.png"), dpi=170, metadata={"Date": None})
plt.close(fig)

# ---------- 표지 ----------
fig = plt.figure(figsize=(12, 6.3), facecolor="#122A44")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor("#122A44")
ax.axis("off")
ax.text(0.5, 0.82, "국가대표 AI 2차 평가: 네 팀 중 국제 지수 1위가 떨어졌다", ha="center", fontsize=25, color="#D8E1EA")
ax.text(0.27, 0.48, "25점", ha="center", fontsize=68, color="#E5967F", fontweight="bold")
ax.text(0.27, 0.30, "국제 성능 지수(AAII)의 배점\n탈락 팀 모티프3 47점 = 4팀 중 1위", ha="center", fontsize=16, color="#9FB3C8")
ax.text(0.73, 0.48, "75점", ha="center", fontsize=68, color="#7FB2E5", fontweight="bold")
ax.text(0.73, 0.30, "전문가·사용자·국내 벤치마크의 배점\n정부: \"사용성·활용성에 무게\"", ha="center", fontsize=16, color="#9FB3C8")
ax.text(0.5, 0.10, "자료: 과학기술정보통신부 2026. 8. 18. 발표", ha="center", fontsize=12, color="#6E8195")
fig.savefig(os.path.join(COVER_OUT, "trend21_cover.png"), dpi=140, metadata={"Date": None})
plt.close(fig)

print("figures written to", os.path.abspath(OUT))
