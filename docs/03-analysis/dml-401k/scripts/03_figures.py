"""그림 6장 + 커버 — 시리즈 4편 (DML·401k).

입력:  out/sim_s1_reps.csv, out/sim_s2_reps.csv, out/sim_s2_summary.json,
       out/e401k_expA_{lasso,forest,boosting}.csv, out/e401k_summary2.json
출력:  static/images/post/dml_401k/fig01–fig06.png, assets/images/post/dml_401k_cover.png

스타일은 3편(prediction_causation)과 통일: 흰 배경, 옅은 격자, 선언문 제목,
참값 점선, 하단 주석("주: … | 시뮬레이션·계산: AIEconLab").
한글 렌더에 Apple SD Gothic Neo 폰트 필요(다른 환경은 rcParams 폰트 교체).
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
ROOT = HERE.parents[3]  # 저장소 루트
FIGDIR = ROOT / "static" / "images" / "post" / "dml_401k"
COVER = ROOT / "assets" / "images" / "post" / "dml_401k_cover.png"
FIGDIR.mkdir(parents=True, exist_ok=True)

THETA0 = 0.5

plt.rcParams.update({
    "font.family": "Apple SD Gothic Neo",
    "axes.unicode_minus": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#D5DBE3",
    "axes.grid": True,
    "grid.color": "#E9EDF2",
    "grid.linewidth": 1.0,
    "axes.axisbelow": True,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize": 15,
    "font.size": 12,
})

NAVY = "#1F2D46"
RED = "#DD6B65"
BLUE = "#7FB3E8"
LIGHTBLUE = "#AECFF2"
GRAY = "#7A8699"
GREEN = "#67A882"
ORANGE = "#E3A04B"


def note(fig, text):
    fig.text(0.06, 0.012, text, fontsize=9.5, color="#6B7686", ha="left")


def title(fig, text, y=0.965):
    fig.suptitle(text, fontsize=17, color=NAVY, x=0.06, y=y, ha="left", fontweight="bold")


# ---------------------------------------------------------------------------
# fig01 — 세 절차의 분포
# ---------------------------------------------------------------------------

def fig01(s1):
    fig, axes = plt.subplots(1, 3, figsize=(12.8, 5.1), sharex=True, sharey=True)
    plt.subplots_adjust(top=0.79, bottom=0.20, left=0.06, right=0.98, wspace=0.08)
    o_sd = s1["oracle_theta"].std(ddof=1)
    xs = np.linspace(0.25, 0.85, 400)
    oracle_pdf = stats.norm.pdf(xs, THETA0, o_sd)
    panels = [
        ("armA", "A. 비직교 점수 + 분할", RED),
        ("armB", "B. 직교 점수 + 결과모형 자기표본 적합", ORANGE),
        ("armC", "C. DML (직교 + 교차적합)", BLUE),
    ]
    for ax, (arm, label, color) in zip(axes, panels):
        th = s1[f"{arm}_theta"]
        cover = s1[f"{arm}_cover"].mean()
        ax.hist(th, bins=34, range=(0.25, 0.85), density=True, color=color, alpha=0.75,
                edgecolor="white", linewidth=0.4)
        ax.plot(xs, oracle_pdf, color=NAVY, lw=1.8, ls="-", alpha=0.85)
        ax.axvline(THETA0, color="black", ls="--", lw=1.6)
        ax.set_title(label, color=NAVY, fontsize=13.5, pad=8)
        ax.text(0.03, 0.95,
                f"평균 편향 {th.mean()-THETA0:+.3f}\n95% CI 포함률 {cover*100:.0f}%",
                transform=ax.transAxes, va="top", ha="left", fontsize=11.5,
                bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#D5DBE3"))
        ax.set_xlabel("처치효과 추정치")
    axes[0].set_ylabel("밀도")
    axes[0].text(THETA0 + 0.012, axes[0].get_ylim()[1] * 0.68, "참값 θ = 0.5",
                 fontsize=11, va="top")
    axes[1].plot([], [], color=NAVY, lw=1.8, label="오라클 분포\n(참 장애모수)")
    axes[1].legend(loc="upper right", frameon=False, fontsize=10.5)
    title(fig, "같은 학습기, 다른 배치: 직교화와 교차적합이 각각 무엇을 바꾸는가", y=0.94)
    note(fig, "주: 부분선형 모형, 참값 θ=0.5, n=1,000, 몬테카를로 500회. 검은 실선은 참 장애모수를 아는 오라클 추정량의 정규근사.\n"
              "     모든 절차가 동일한 랜덤포레스트 사양이며, B는 결과 쪽 잔차화만 자기 표본으로 적합(처치 쪽 교차적합은 유지)  |  시뮬레이션·계산: AIEconLab")
    fig.savefig(FIGDIR / "fig01_three_procedures.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# fig02 — 오차 항별 분해 (오리지널 ①)
# ---------------------------------------------------------------------------

def fig02(s1):
    fig, ax = plt.subplots(figsize=(12.8, 5.6))
    plt.subplots_adjust(top=0.84, bottom=0.20, left=0.07, right=0.97)
    groups = [
        ("A. 비직교+분할", [("a", "armA_term_a", GRAY), ("b", "armA_term_b", RED)]),
        ("B. 직교+결과모형 자기표본 적합", [("a*", "armB_term_a", GRAY), ("c*", "armB_term_c", ORANGE),
                                ("b*", "armB_term_b", RED)]),
        ("C. DML", [("a*", "armC_term_a", GRAY), ("c*", "armC_term_c", ORANGE),
                     ("b*", "armC_term_b", RED)]),
    ]
    pos, xticks, xlabels = 0.0, [], []
    rng = np.random.default_rng(0)
    for gname, terms in groups:
        start = pos
        for tname, col, color in terms:
            vals = s1[col].to_numpy()
            ax.bar(pos, vals.mean(), width=0.62, color=color, alpha=0.8,
                   edgecolor="white")
            ax.errorbar(pos, vals.mean(), yerr=vals.std(ddof=1), color=NAVY,
                        capsize=4, lw=1.4)
            jitter = rng.uniform(-0.16, 0.16, len(vals))
            ax.plot(pos + jitter, vals, ".", color=NAVY, alpha=0.05, ms=3,
                    zorder=1)
            xticks.append(pos)
            xlabels.append(tname)
            pos += 1.0
        ax.text((start + pos - 1.0) / 2, -0.20, gname, ha="center", fontsize=12.5,
                color=NAVY, transform=ax.get_xaxis_transform())
        pos += 0.9
    ax.axhline(0, color="black", lw=1.0)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels, fontsize=12)
    ax.set_ylabel("추정오차 기여분 (θ 단위)")
    title(fig, "오차 항등식의 항별 분해: 직교화와 교차적합의 역할")
    note(fig, "주: 각 반복에서 오차 항등식의 항을 참 함수로 직접 계산한 값. 막대는 500회 평균, 수염은 표준편차, 점은 개별 반복. "
              "a(a*)=오라클 항, b(b*)=정규화 편향 항, c*=구조 오차×추정 오차 교차항  |  시뮬레이션·계산: AIEconLab")
    fig.savefig(FIGDIR / "fig02_term_ledger.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# fig03 — 곱-수렴률 스트레스 테스트 (S2)
# ---------------------------------------------------------------------------

def fig03(s2, ovb=None):
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.2))
    plt.subplots_adjust(top=0.82, bottom=0.20, left=0.07, right=0.97, wspace=0.22)
    cs = sorted(s2["c"].unique())
    ax = axes[0]
    cov = [s2.loc[s2["c"] == c, "cover"].mean() for c in cs]
    ax.plot(cs, cov, "o-", color=NAVY, lw=2, ms=7)
    ax.axhline(0.95, color=GREEN, ls="--", lw=1.6)
    ax.text(cs[0], 0.955, "명목 95%", color=GREEN, fontsize=11, va="bottom")
    ax.set_xscale("log")
    ax.set_xticks(cs)
    ax.set_xticklabels([str(c) for c in cs])
    ax.set_xlabel("벌점 배율 c (CV 최적 λ의 c배)")
    ax.set_ylabel("95% 신뢰구간 포함률")
    ax.set_ylim(-0.04, 1.04)
    ax.set_title("나머지항이 커질수록 포함률이 낮아진다", color=NAVY, fontsize=13.5)
    ax = axes[1]
    palette = {1: "#9CB6D8", 3: "#7FA3D1", 10: ORANGE, 30: RED, 100: "#8E4444"}
    for c in cs:
        g = s2[s2["c"] == c]
        ax.plot(g["prod_stat"], g["term_b"], ".", ms=5, alpha=0.45,
                color=palette.get(int(c), GRAY), label=f"c={int(c)}")
    if ovb is not None:
        ax.axhline(ovb, color="black", ls=":", lw=1.6)
        ax.text(0.02, ovb + 0.015, "공변량 미조정 회귀의 누락변수 편향", fontsize=10.5,
                ha="left", va="bottom", transform=ax.get_yaxis_transform())
    ax.set_xscale("log")
    ax.set_xlabel(r"직접 계산한 곱-통계 $\sqrt{n}\,\cdot\,\|\hat e_m\|\,(\|\hat e_m\|+\|\hat e_\ell\|)$")
    ax.set_ylabel("정규화 편향 항 b* (θ 단위)")
    ax.legend(frameon=False, fontsize=10.5, loc="lower right")
    ax.set_title("편향 항 b*와 곱-통계가 함께 증가한다", color=NAVY, fontsize=13.5)
    title(fig, "곱-수렴률 조건이 필요한 이유: 벌점을 CV 최적의 c배로 올렸을 때")
    note(fig, "주: 장애모수가 2차 다항 사전 안에 있는 희소 설계, n=1,000, 반복 500회, K=5 교차적합 유지.\n"
              "     기준 벌점은 각 학습 폴드 안에서 CV로 선택하고 그 c배를 적용. c→∞ 극한에서 추정치는 공변량 미조정 회귀로 퇴화  |  시뮬레이션·계산: AIEconLab")
    fig.savefig(FIGDIR / "fig03_rate_dial.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# fig04 — 401(k) 추정치 비교
# ---------------------------------------------------------------------------

def fig04(summ):
    res, paper, anch = summ["expA"], summ["paper"], summ["anchors"]
    rows = [
        ("미조정 OLS", anch["no_control"]["theta"], anch["no_control"]["se_hc0"], None, GRAY),
        ("선형 통제 OLS", anch["ols_linear_controls"]["theta"],
         anch["ols_linear_controls"]["se_hc1"], None, GRAY),
    ]
    for model, color in (("PLR", BLUE), ("IRM", GREEN)):
        for learner, klabel in (("lasso", "라쏘"), ("forest", "랜덤포레스트"),
                                 ("boosting", "부스팅")):
            r = res[model][learner]
            p = paper[model]["5fold"][learner]
            rows.append((f"{model} · {klabel}", r["theta_median"],
                         r["se_split_adjusted"], p[0], color))
    fig, ax = plt.subplots(figsize=(12.8, 6.4))
    plt.subplots_adjust(top=0.86, bottom=0.15, left=0.20, right=0.96)
    ys = np.arange(len(rows))[::-1]
    for y, (label, th, se, ppoint, color) in zip(ys, rows):
        ax.errorbar(th, y, xerr=1.959963984540054 * se, fmt="o", color=color,
                    ms=8, capsize=4, lw=2)
        if ppoint is not None:
            ax.plot(ppoint, y, marker="D", mfc="white", mec=NAVY, ms=8, mew=1.6,
                    ls="none", zorder=5)
    ax.axvline(0, color="#C6CDD6", lw=1.2)
    ax.axvline(rows[0][1], color=GRAY, ls=":", lw=1.4)
    ax.text(rows[0][1], len(rows) - 0.35, "미조정 \\$19,559", fontsize=10.5,
            color=GRAY, ha="center", va="bottom")
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=12)
    ax.set_xlabel("401(k) 적격성과 순금융자산의 미조정 차이 및 효과 추정치 (달러)")
    ax.plot([], [], "o", color=NAVY, label="본 글 재추정 (중위수법, 분할 조정 95% CI)")
    ax.plot([], [], marker="D", mfc="white", mec=NAVY, ls="none",
            label="원 논문 보고치 (DML2, 5-fold, 분할 100회 중위수)")
    ax.legend(frameon=True, facecolor="white", edgecolor="#D5DBE3", framealpha=0.95, fontsize=11, loc="lower right")
    title(fig, "유연하게 공변량을 조정하면: 미조정 차이 \\$19,559가 약 40–51%로 낮아진다")
    note(fig, "주: N=9,915 (1991 SIPP). 본 글 추정은 DML2·K=5, 학습기 시드 고정·분할 시드 100회의 중위수법이며 학습기 사양은 원 논문과 다르다(부록).\n"
              "     구간은 분할 변동을 더한 분할 조정 표준오차 기준의 95% 신뢰구간  |  계산: AIEconLab, 원자료: Chernozhukov et al. (2018)의 공개 데이터")
    fig.savefig(FIGDIR / "fig04_401k_estimates.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# fig05 — 분할에 따른 추정치 분포 (오리지널 ②)
# ---------------------------------------------------------------------------

def fig05(reps, summ):
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.6), sharey=False)
    plt.subplots_adjust(top=0.82, bottom=0.18, left=0.09, right=0.97, wspace=0.18)
    order = [("lasso", "라쏘"), ("forest", "랜덤포레스트"), ("boosting", "부스팅")]
    rng = np.random.default_rng(1)
    for ax, model, color in ((axes[0], "PLR", BLUE), (axes[1], "IRM", GREEN)):
        for i, (learner, klabel) in enumerate(order):
            g = reps[(reps["model"] == model) & (reps["learner"] == learner)]
            th = g["theta"].to_numpy()
            jitter = rng.uniform(-0.13, 0.13, len(th))
            ax.plot(th, i + jitter, ".", color=color, alpha=0.45, ms=6)
            med = np.median(th)
            ax.plot(med, i, marker="|", color=NAVY, ms=26, mew=3)
            r = summ["expA"][model][learner]
            ax.text(0.985, i + 0.30,
                    f"분할 SD \\${r['split_sd']:,.0f} / 분할별 SE 중위수 \\${r['se_median_raw']:,.0f}",
                    transform=ax.get_yaxis_transform(), fontsize=10.5,
                    ha="right", color="#5A6575")
        ax.set_yticks(range(len(order)))
        ax.set_yticklabels([k for _, k in order], fontsize=12)
        ax.set_title(f"{model}", color=NAVY, fontsize=13.5)
        ax.set_xlabel("추정치 (달러)")
        ax.set_ylim(-0.6, len(order) - 0.2)
    title(fig, "같은 자료와 학습기, 다른 분할: 추정치 100개의 분포")
    note(fig, "주: 학습기 시드를 고정하고 무작위 분할 시드만 바꾼 DML2(K=5) 추정 100회(순수한 분할 변동). 두 패널의 가로축 범위는 서로 다르다.\n"
              "     세로 막대는 중위수(중위수법 점추정), 분할 SD는 100개 추정치의 표준편차, 분할별 SE 중위수는 각 분할 표준오차의 중위수  |  계산: AIEconLab")
    fig.savefig(FIGDIR / "fig05_multiverse.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# fig06 — 추정치 변동의 구성: 분할 vs 학습기 내부 무작위성 (crossed 10×10 분산 성분)
# ---------------------------------------------------------------------------

def fig06(summ):
    fig, ax = plt.subplots(figsize=(12.8, 5.2))
    plt.subplots_adjust(top=0.82, bottom=0.24, left=0.08, right=0.97)
    combos = [("PLR", "forest", "PLR·랜덤포레스트"), ("PLR", "boosting", "PLR·부스팅"),
              ("IRM", "forest", "IRM·랜덤포레스트"), ("IRM", "boosting", "IRM·부스팅")]
    comps = [("sd_split", "분할", BLUE), ("sd_learner", "학습기 내부 무작위성", ORANGE),
             ("sd_resid", "상호작용·잔여", GRAY)]
    width = 0.24
    xs = np.arange(len(combos))
    for j, (key, klabel, color) in enumerate(comps):
        vals = [summ["crossed"][m][l][key] for m, l, _ in combos]
        bars = ax.bar(xs + (j - 1) * width, vals, width=width, color=color,
                      alpha=0.85, edgecolor="white", label=klabel)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v, f"\\${v:,.0f}", ha="center",
                    va="bottom", fontsize=10, color="#44506B")
    ax.set_xticks(xs)
    ax.set_xticklabels([lab for _, _, lab in combos], fontsize=12)
    ax.set_ylabel("표준편차 성분 (달러)")
    ax.legend(frameon=False, fontsize=11, loc="upper left")
    ax.text(0.99, 0.95,
            "참고: LASSO의 학습기 성분은 사실상 0.\n"
            "PLR은 100회 모두 동일값(결정론적), IRM은 \\$3 수준 미세 변동",
            transform=ax.transAxes, ha="right", va="top", fontsize=10.5,
            color="#5A6575")
    title(fig, "추정치 변동의 구성: 분할, 학습기 무작위성, 상호작용·잔여")
    note(fig, "주: 분할 시드 10 × 학습기 시드 10의 교차 설계(DML2, K=5)를 반복 없는 2원 분산분석으로 분해한 표준편차 성분. "
              "부스팅의 내부 무작위성은 조기 종료용 검증 분할에서, 랜덤포레스트는 부트스트랩 표본에서 나온다  |  계산: AIEconLab")
    fig.savefig(FIGDIR / "fig06_variance_components.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 커버
# ---------------------------------------------------------------------------

def cover(s1):
    fig = plt.figure(figsize=(12.8, 6.7))
    fig.patch.set_facecolor("#F5F7FA")
    ax = fig.add_axes([0.55, 0.16, 0.40, 0.52])
    ax.set_facecolor("#F5F7FA")
    o_sd = s1["oracle_theta"].std(ddof=1)
    xs = np.linspace(0.3, 0.8, 400)
    ax.hist(s1["armA_theta"], bins=30, density=True, color=RED, alpha=0.7,
            edgecolor="white", linewidth=0.4)
    ax.hist(s1["armC_theta"], bins=30, density=True, color=BLUE, alpha=0.75,
            edgecolor="white", linewidth=0.4)
    ax.plot(xs, stats.norm.pdf(xs, THETA0, o_sd), color=NAVY, lw=2)
    ax.axvline(THETA0, color="black", ls="--", lw=1.6)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.grid(False)
    ax.set_yticks([])
    ax.set_xticks([THETA0])
    ax.set_xticklabels(["참값"], fontsize=13)
    fig.text(0.06, 0.72, "잔차끼리의 회귀", fontsize=40, color=NAVY, fontweight="bold")
    fig.text(0.06, 0.60, "90년 된 정리와 DML,\n그리고 401(k)의 재추정", fontsize=20,
             color="#445064", linespacing=1.5, va="top")
    fig.text(0.06, 0.30, "직교화는 1차 편향을 2차 항으로 바꾸고\n교차적합은 과적합 교차항을 줄인다",
             fontsize=14, color="#6B7686", linespacing=1.6, va="top")
    fig.text(0.06, 0.08, "AIEconLab · AI를 활용한 경제분석 시리즈 4편", fontsize=12,
             color="#8A94A4")
    fig.savefig(COVER, dpi=150)
    plt.close(fig)


def main():
    s1 = pd.read_csv(OUT / "sim_s1_reps.csv")
    s2 = pd.read_csv(OUT / "sim_s2_reps.csv")
    reps = pd.concat([pd.read_csv(OUT / f"e401k_expA_{l}.csv")
                      for l in ("lasso", "forest", "boosting")])
    summ = json.loads((OUT / "e401k_summary2.json").read_text())
    ovb = json.loads((OUT / "sim_s2_summary.json").read_text()).get("ovb_limit")
    fig01(s1)
    fig02(s1)
    fig03(s2, ovb=ovb)
    fig04(summ)
    fig05(reps, summ)
    fig06(summ)
    cover(s1)
    print("figures written to", FIGDIR)


if __name__ == "__main__":
    main()
