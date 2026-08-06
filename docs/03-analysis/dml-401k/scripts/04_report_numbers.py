"""본문 기입용 수치 리포트 — 요약 JSON/CSV에서 본문에 들어갈 수치를 한 번에 출력.

목적: 본문·그림·요약 파일 사이의 수치 전사 오류 방지 (검수 게이트에서 재실행해 대조).
실행: python 04_report_numbers.py   (05_aggregate.py 선행 필요)
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent / "out"


def main():
    print("=" * 76)
    print("S1 — 세 절차 (500회)")
    s1 = json.loads((OUT / "sim_s1_summary.json").read_text())
    for arm in ("oracle", "armA", "armB", "armBsym", "armC"):
        a = s1[arm]
        terms = {k.replace("_mean", ""): v for k, v in a.items()
                 if k.endswith("_mean") and k.startswith("term")}
        print(f"  {arm:8s} bias={a['bias']:+.4f} sd={a['sd']:.4f} "
              f"med_se={a['median_se']:.4f} cover={a['coverage']*100:5.1f}%  "
              + " ".join(f"{k}={v:+.4f}" for k, v in terms.items()))

    print("=" * 76)
    print("S2 — 나머지항 스트레스 테스트 (500회, 폴드 내 벌점 선택)")
    s2 = json.loads((OUT / "sim_s2_summary.json").read_text())
    print(f"  OVB 극한 (c→∞): {s2['ovb_limit']:+.4f}")
    for c, g in s2["by_c"].items():
        print(f"  c={c:>3s} bias={g['bias']:+.4f} cover={g['coverage']*100:5.1f}% "
              f"prod={g['prod_stat_mean']:7.2f} term_b={g['term_b_mean']:+.4f}")

    print("=" * 76)
    print("E1 — 401(k) expA (분할만 100회, 학습기 시드 고정)")
    e = json.loads((OUT / "e401k_summary2.json").read_text())
    an = e["anchors"]
    print(f"  미조정 OLS: {an['no_control']['theta']:.1f} (HC0 {an['no_control']['se_hc0']:.1f})")
    print(f"  선형 통제 OLS: {an['ols_linear_controls']['theta']:.1f} "
          f"(HC1 {an['ols_linear_controls']['se_hc1']:.1f})")
    ths = []
    for model in ("PLR", "IRM"):
        for learner in ("lasso", "forest", "boosting"):
            r = e["expA"][model][learner]
            p = e["paper"][model]["5fold"][learner]
            ths.append(r["theta_median"])
            ratio = r["split_sd"] / r["se_median_raw"]
            adj_pct = (r["se_split_adjusted"] / r["se_median_raw"] - 1) * 100
            rng = r["theta_max"] - r["theta_min"]
            print(f"  {model} {learner:9s} {r['theta_median']:8,.0f} "
                  f"[raw {r['se_median_raw']:,.0f}] (adj {r['se_split_adjusted']:,.0f}, "
                  f"+{adj_pct:.1f}%) splitSD {r['split_sd']:5,.0f} "
                  f"({ratio*100:4.1f}% of SE, var {ratio**2*100:4.1f}%) "
                  f"range {rng:5,.0f} [{r['theta_min']:,.0f},{r['theta_max']:,.0f}] "
                  f"| 논문 {p[0]:,} ({p[2]:,})")
    lo, hi = min(ths), max(ths)
    nc = an["no_control"]["theta"]
    print(f"  θ 대역: [{lo:,.0f}, {hi:,.0f}] = 미조정 차이의 {lo/nc*100:.1f}~{hi/nc*100:.1f}%")
    reps = pd.concat([pd.read_csv(OUT / f"e401k_expA_{l}.csv")
                      for l in ("lasso", "forest", "boosting")])
    for model in ("PLR", "IRM"):
        g = reps[reps["model"] == model]
        piv = g.pivot_table(index="split_seed", columns="learner", values="theta")
        rng_l = piv.max(axis=1) - piv.min(axis=1)
        print(f"  {model} 학습기 간 범위(같은 분할): 중위 {np.median(rng_l):,.0f}")
    irm = reps[reps["model"] == "IRM"]
    print(f"  IRM 클리핑 비중(평균): m<0.01 {irm['m_below_trim'].mean()*100:.2f}%")

    print("=" * 76)
    print("E2 — expB (분할 고정, 학습기 시드만 변경) · crossed (10×10 분산분해)")
    for model in ("PLR", "IRM"):
        for learner in ("lasso", "forest", "boosting"):
            b = e["expB"].get(model, {}).get(learner)
            c = e["crossed"].get(model, {}).get(learner)
            btxt = (f"expB SD {b['learner_sd']:5,.0f} (runs {b['n_runs']}, "
                    f"고유값 {b['distinct_values']})" if b else "expB —")
            ctxt = (f"| crossed: split {c['sd_split']:5,.0f} / learner "
                    f"{c['sd_learner']:5,.0f} / resid {c['sd_resid']:5,.0f}" if c else "")
            print(f"  {model} {learner:9s} {btxt} {ctxt}")


if __name__ == "__main__":
    main()
