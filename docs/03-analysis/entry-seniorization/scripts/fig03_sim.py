# -*- coding: utf-8 -*-
"""
Fig 3: conditional-arithmetic cohort model (NOT a calibrated model).

Model:
- Years 2010..2040, baseline hires H(t)=100 every year.
- Scenarios: hires fall by delta in {10%, 20%, 30%} during 2026-2028 only;
  from 2029 hires return to 100 (temporary shock).
- Mid-career pool P(t) = sum_{k=5..9} w_k * H(t-k).
- Headline: flat w_k = 1. Sensitivity: w_k = p^k, p in {0.80, 0.90}.
- Output: % deviation of P(t) from baseline, 2026..2040.

Sanity check: with flat weights the peak deviation is -0.6*delta in 2033-2035
(3 of the 5 cohorts in the 5-9 tenure window are shock cohorts).
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SCRATCH = ("/private/tmp/claude-501/-Users-hayun-Documents-Github-AIEconLab--claude-"
           "worktrees-ai-trends-july-17-1ce616/ae37edf6-cc22-4044-ad92-2e5d4cc51c0e/"
           "scratchpad/entry_seniorization")
OUT_JSON = os.path.join(SCRATCH, "out", "sim_results.json")
FIG_PATH = ("/Users/hayun/Documents/Github_AIEconLab/.claude/worktrees/"
            "ai-trends-july-17-1ce616/static/images/post/entry_seniorization/"
            "fig03_pipeline_arithmetic.png")

YEARS = list(range(2010, 2041))
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
    if year in SHOCK_YEARS:
        return 100.0 * (1.0 - delta)
    return 100.0


def pool(year, delta, weights):
    return sum(weights[k] * hires(year - k, delta) for k in TENURE)


def deviation_series(delta, weights):
    """% deviation of P(t) from baseline, for PLOT_YEARS."""
    out = []
    for t in PLOT_YEARS:
        base = pool(t, 0.0, weights)
        shocked = pool(t, delta, weights)
        out.append(100.0 * (shocked - base) / base)
    return out


# ---------------- compute ----------------
results = {}  # results[delta_label][profile] = {years, dev, peak_dev, peak_years}
for delta in DELTAS:
    dl = f"delta={int(delta*100)}%"
    results[dl] = {}
    for pname, w in WEIGHT_PROFILES.items():
        dev = deviation_series(delta, w)
        peak = min(dev)
        peak_years = [y for y, d in zip(PLOT_YEARS, dev) if abs(d - peak) < 1e-9]
        results[dl][pname] = {
            "years": PLOT_YEARS,
            "deviation_pct": [round(d, 4) for d in dev],
            "peak_deviation_pct": round(peak, 4),
            "peak_years": peak_years,
        }

# Sanity check: flat-weight peak must equal -0.6*delta over 2033-2035
for delta in DELTAS:
    dl = f"delta={int(delta*100)}%"
    r = results[dl]["flat"]
    expected = -0.6 * delta * 100.0
    assert abs(r["peak_deviation_pct"] - expected) < 1e-6, (dl, r["peak_deviation_pct"], expected)
    assert r["peak_years"] == [2033, 2034, 2035], (dl, r["peak_years"])
print("Sanity check passed: flat-weight peak = -0.6*delta over 2033-2035")

# Sensitivity spread per delta (min/max of peak deviation across profiles)
spread = {}
for delta in DELTAS:
    dl = f"delta={int(delta*100)}%"
    peaks = {p: results[dl][p]["peak_deviation_pct"] for p in WEIGHT_PROFILES}
    spread[dl] = {
        "peaks_by_profile": peaks,
        "min_peak_pct": min(peaks.values()),
        "max_peak_pct": max(peaks.values()),
        "spread_pp": round(max(peaks.values()) - min(peaks.values()), 4),
    }
    print(dl, peaks, "spread(pp):", spread[dl]["spread_pp"])

os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump({
        "model": "conditional arithmetic cohort model (not calibrated)",
        "spec": {
            "years": [2010, 2040], "baseline_hires": 100,
            "shock_years": sorted(SHOCK_YEARS), "deltas": DELTAS,
            "tenure_window": [5, 9],
            "weight_profiles": {p: {str(k): v for k, v in w.items()}
                                for p, w in WEIGHT_PROFILES.items()},
        },
        "results": results,
        "sensitivity_spread": spread,
    }, f, ensure_ascii=False, indent=2)
print("wrote", OUT_JSON)

# ---------------- plot ----------------
plt.rcParams["font.family"] = "Apple SD Gothic Neo"
plt.rcParams["axes.unicode_minus"] = False

C_BLUE = "#2563eb"
C_MID = "#9aa5b8"
C_LIGHT = "#cfd6e0"
C_NAVY = "#1b2a4a"
C_NOTE = "#5a6472"
C_SPINE = "#c8cdd6"

fig, ax = plt.subplots(figsize=(10, 7), dpi=200)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

line_specs = [  # (delta, color, lw, label)
    (0.10, C_LIGHT, 2.0, "채용 10% 감소"),
    (0.20, C_MID, 2.0, "채용 20% 감소"),
    (0.30, C_BLUE, 2.8, "채용 30% 감소"),
]

for delta, color, lw, label in line_specs:
    dl = f"delta={int(delta*100)}%"
    flat = results[dl]["flat"]["deviation_pct"]
    lo = [min(results[dl][p]["deviation_pct"][i] for p in WEIGHT_PROFILES)
          for i in range(len(PLOT_YEARS))]
    hi = [max(results[dl][p]["deviation_pct"][i] for p in WEIGHT_PROFILES)
          for i in range(len(PLOT_YEARS))]
    ax.fill_between(PLOT_YEARS, lo, hi, color=color, alpha=0.25, linewidth=0)
    ax.plot(PLOT_YEARS, flat, color=color, linewidth=lw, label=label, zorder=3)

ax.axhline(0, color=C_SPINE, linewidth=1.0, zorder=1)

# annotate the 30% peak
peak30 = results["delta=30%"]["flat"]["peak_deviation_pct"]
ax.annotate("최대 %.0f%%" % peak30,
            xy=(2034, peak30), xytext=(2034, peak30 - 2.8),
            ha="center", va="top", fontsize=13, fontweight="bold", color=C_BLUE,
            arrowprops=dict(arrowstyle="-", color=C_BLUE, lw=0.9))

ax.set_xlim(2025.5, 2040.5)
ax.set_ylim(-24, 3)
ax.set_xticks(range(2026, 2041, 2))
ax.set_ylabel("기준선 대비 편차 (%)", fontsize=12, color=C_NAVY)
ax.set_xlabel("연도", fontsize=12, color=C_NAVY)
ax.tick_params(colors=C_NAVY, labelsize=11)

for side in ["top", "right"]:
    ax.spines[side].set_visible(False)
for side in ["left", "bottom"]:
    ax.spines[side].set_color(C_SPINE)
ax.grid(axis="y", color=C_SPINE, linewidth=0.6, alpha=0.5)
ax.set_axisbelow(True)

ax.set_title("신입 채용을 3년간 줄이면: 5~9년차 인력 풀의 상대적 결손",
             loc="left", fontsize=16, fontweight="bold", color=C_NAVY, pad=16)

leg = ax.legend(loc="lower right", frameon=False, fontsize=11)
for t in leg.get_texts():
    t.set_color(C_NAVY)

fig.subplots_adjust(left=0.09, right=0.97, top=0.90, bottom=0.17)
fig.text(0.09, 0.078,
         "주: 개념적 산수 모형: 신규 입직을 100으로 정규화, 2026~28년 채용 감소 외 모든 조건 동일 가정.",
         fontsize=9, color=C_NOTE, ha="left")
fig.text(0.09, 0.051,
         "     이탈률 프로파일(민감도 밴드)은 결과를 크게 바꾸지 않음. 실측 캘리브레이션 아님.",
         fontsize=9, color=C_NOTE, ha="left")
fig.text(0.09, 0.024,
         "계산: AIEconLab",
         fontsize=9, color=C_NOTE, ha="left")

fig.savefig(FIG_PATH, dpi=200, facecolor="white")
print("wrote", FIG_PATH)
