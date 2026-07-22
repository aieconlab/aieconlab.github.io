#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그림 3: 조건부 산수 코호트 모형 (실측 캘리브레이션 아님).

모형:
- 2010~2040년, 기준선 신규 입직 H(t)=100.
- 시나리오: 2026~28년에만 채용이 δ∈{10%, 20%, 30%} 감소, 2029년부터 100 복귀.
- 5~9년차 풀 P(t) = Σ_{k=5..9} w_k · H(t−k).
- 기본 가중: 균등(w_k=1). 민감도: w_k = p^k, p∈{0.80, 0.90} (연 일정 비율 이탈).

산술 검증: 균등 가중에서 최대 결손은 −0.6δ(2033~35년) — 5개 코호트 창 중
3개가 축소 코호트인 데서 나오는 결과. 스크립트가 assert로 확인한다.

사용법: python3 fig03_sim.py [--out PNG] [--json JSON] [--font FONT]
외부 데이터 없음. 의존성: matplotlib.
"""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
BLUE, MID, LIGHT, NAVY, NOTE, SPINE = ("#2563eb", "#8290a6", "#aab6c6",
                                       "#1b2a4a", "#5a6472", "#c8cdd6")

SHOCK_YEARS = {2026, 2027, 2028}
DELTAS = [0.10, 0.20, 0.30]
PLOT_YEARS = list(range(2026, 2041))
TENURE = range(5, 10)  # k = 5..9
WEIGHT_PROFILES = {
    "flat": {k: 1.0 for k in TENURE},
    "p=0.90": {k: 0.90 ** k for k in TENURE},
    "p=0.80": {k: 0.80 ** k for k in TENURE},
}


def hires(year, delta):
    return 100.0 * (1.0 - delta) if year in SHOCK_YEARS else 100.0


def pool(year, delta, weights):
    return sum(weights[k] * hires(year - k, delta) for k in TENURE)


def deviation_series(delta, weights):
    out = []
    for t in PLOT_YEARS:
        base = pool(t, 0.0, weights)
        out.append(100.0 * (pool(t, delta, weights) - base) / base)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "out" / "fig03_pipeline_arithmetic.png")
    ap.add_argument("--json", type=Path, default=HERE / "out" / "sim_results.json")
    ap.add_argument("--font", default="Apple SD Gothic Neo")
    a = ap.parse_args()

    results = {}
    for delta in DELTAS:
        dl = f"delta={int(delta*100)}%"
        results[dl] = {}
        for pname, w in WEIGHT_PROFILES.items():
            dev = deviation_series(delta, w)
            peak = min(dev)
            results[dl][pname] = {
                "years": PLOT_YEARS,
                "deviation_pct": [round(d, 4) for d in dev],
                "peak_deviation_pct": round(peak, 4),
                "peak_years": [y for y, d in zip(PLOT_YEARS, dev) if abs(d - peak) < 1e-9],
            }

    for delta in DELTAS:
        r = results[f"delta={int(delta*100)}%"]["flat"]
        assert abs(r["peak_deviation_pct"] - (-0.6 * delta * 100.0)) < 1e-6
        assert r["peak_years"] == [2033, 2034, 2035]
    print("sanity check passed: flat-weight peak = -0.6*delta over 2033-2035")

    spread = {}
    for delta in DELTAS:
        dl = f"delta={int(delta*100)}%"
        peaks = {pn: results[dl][pn]["peak_deviation_pct"] for pn in WEIGHT_PROFILES}
        spread[dl] = {"peaks_by_profile": peaks,
                      "min_peak_pct": min(peaks.values()),
                      "max_peak_pct": max(peaks.values()),
                      "spread_pp": round(max(peaks.values()) - min(peaks.values()), 4)}

    a.json.parent.mkdir(parents=True, exist_ok=True)
    a.json.write_text(json.dumps({
        "model": "conditional arithmetic cohort model (not calibrated)",
        "spec": {"years": [2010, 2040], "baseline_hires": 100,
                 "shock_years": sorted(SHOCK_YEARS), "deltas": DELTAS,
                 "tenure_window": [5, 9],
                 "weight_profiles": {pn: {str(k): v for k, v in w.items()}
                                     for pn, w in WEIGHT_PROFILES.items()}},
        "results": results,
        "sensitivity_spread": spread,
    }, ensure_ascii=False, indent=2))
    print("wrote", a.json)

    plt.rcParams["font.family"] = a.font
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax = plt.subplots(figsize=(10, 7), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    for delta, color, lw, label in [(0.10, LIGHT, 2.4, "채용 10% 감소"),
                                    (0.20, MID, 2.4, "채용 20% 감소"),
                                    (0.30, BLUE, 3.4, "채용 30% 감소")]:
        dl = f"delta={int(delta*100)}%"
        flat = results[dl]["flat"]["deviation_pct"]
        lo = [min(results[dl][p]["deviation_pct"][i] for p in WEIGHT_PROFILES)
              for i in range(len(PLOT_YEARS))]
        hi = [max(results[dl][p]["deviation_pct"][i] for p in WEIGHT_PROFILES)
              for i in range(len(PLOT_YEARS))]
        ax.fill_between(PLOT_YEARS, lo, hi, color=color, alpha=0.25, linewidth=0)
        ax.plot(PLOT_YEARS, flat, color=color, linewidth=lw, label=label, zorder=3)

    ax.axhline(0, color=SPINE, linewidth=1.0, zorder=1)
    peak30 = results["delta=30%"]["flat"]["peak_deviation_pct"]
    ax.annotate(f"균등가중 기준 최대 {peak30:.0f}%",
                xy=(2034.6, peak30), xytext=(2035.2, peak30 - 3.2),
                ha="center", va="top", fontsize=16.5, fontweight="bold", color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=1.0))

    ax.set_xlim(2025.5, 2040.5)
    ax.set_ylim(-26, 3)
    ax.set_xticks(range(2026, 2041, 2))
    ax.set_ylabel("기준선 대비 편차 (%)", fontsize=16.5, color=NAVY)
    ax.set_xlabel("연도", fontsize=16.5, color=NAVY)
    ax.tick_params(colors=NAVY, labelsize=15.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(SPINE)
    ax.grid(axis="y", color=SPINE, linewidth=0.6, alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_title("신입 채용을 3년간 줄이면: 5~9년차 인력 풀의 상대적 결손",
                 loc="left", fontsize=22, fontweight="bold", color=NAVY, pad=18)
    leg = ax.legend(loc="lower right", frameon=False, fontsize=14.5)
    for t in leg.get_texts():
        t.set_color(NAVY)

    fig.subplots_adjust(left=0.09, right=0.97, top=0.90, bottom=0.16)
    fig.text(0.09, 0.068, "주: 개념적 산수 모형 — 신규 입직 100 정규화, 2026~28년 채용 감소 외 모든 조건 동일 가정. 밴드는 이탈률 민감도.",
             fontsize=12.5, color=NOTE)
    fig.text(0.09, 0.03, "실측 캘리브레이션 아님  |  계산: AIEconLab",
             fontsize=12.5, color=NOTE)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.out, dpi=200, facecolor="white")
    print("wrote", a.out)


if __name__ == "__main__":
    main()
