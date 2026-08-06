"""E1·E2 집계 — expA/expB/crossed 산출물을 요약 JSON으로.

- expA(분할만 100회): 중위수법 점추정·조정 SE(논문 3.4절), 분할 SD, 범위 → 본문 표·그림
- expB(학습기 시드만 100회 변경): 내부 무작위성 SD (lasso는 결정성 확인)
- crossed(10×10): 반복 없는 2원 분산분석으로 분산 성분(분할/학습기 무작위성/잔여) 추정
출력: out/e401k_summary2.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dml_core import median_method  # noqa: E402

OUT = Path(__file__).resolve().parent / "out"

# 논문(§6.2) 보고치 — arXiv 1608.00060 LaTeX 원문에서 전사 (2026-08-04 확인)
PAPER = {
    "no_control": {"theta": 19559, "se": 1413},
    "PLR": {"5fold": {"lasso": (8187, 1298, 1558), "forest": (9247, 1295, 1328),
                       "boosting": (9110, 1314, 1328)},
            "2fold": {"lasso": (7717, 1346, 1749), "forest": (9116, 1302, 1377),
                       "boosting": (8759, 1339, 1382)}},
    "IRM": {"5fold": {"lasso": (7170, 1201, 1398), "forest": (8105, 1242, 1299),
                       "boosting": (7713, 1155, 1177)},
            "2fold": {"lasso": (6830, 1282, 1530), "forest": (7770, 1276, 1363),
                       "boosting": (7806, 1159, 1202)}},
}

LEARNERS = ["lasso", "forest", "boosting"]
MODELS = ["PLR", "IRM"]


def variance_components(pivot):
    """반복 없는 2원 배치(행=split, 열=learner_seed)의 분산 성분.

    sigma2_A = (MS_A - MS_E)/b, sigma2_B = (MS_B - MS_E)/a, sigma2_E = MS_E
    (음수는 0으로 절단). 반환은 표준편차.
    """
    M = pivot.to_numpy(dtype=float)
    a, b = M.shape
    gm = M.mean()
    row = M.mean(axis=1)
    col = M.mean(axis=0)
    ss_a = b * np.sum((row - gm) ** 2)
    ss_b = a * np.sum((col - gm) ** 2)
    ss_t = np.sum((M - gm) ** 2)
    ss_e = ss_t - ss_a - ss_b
    ms_a = ss_a / (a - 1)
    ms_b = ss_b / (b - 1)
    ms_e = ss_e / ((a - 1) * (b - 1))
    s2_split = max((ms_a - ms_e) / b, 0.0)
    s2_learn = max((ms_b - ms_e) / a, 0.0)
    return {"sd_split": float(np.sqrt(s2_split)),
            "sd_learner": float(np.sqrt(s2_learn)),
            "sd_resid": float(np.sqrt(ms_e))}


def main():
    anchors = json.loads((OUT / "e401k_anchors.json").read_text())
    summary = {"anchors": anchors, "paper": PAPER,
               "expA": {}, "expB": {}, "crossed": {}}

    for model in MODELS:
        summary["expA"][model] = {}
        summary["expB"][model] = {}
        summary["crossed"][model] = {}
        for learner in LEARNERS:
            fA = OUT / f"e401k_expA_{learner}.csv"
            assert fA.exists(), f"필수 입력 없음: {fA}"
            if fA.exists():
                g = pd.read_csv(fA)
                g = g[g["model"] == model]
                # 완전성 검증: 분할 시드 0..99 각 1회, 학습기 시드 0 고정
                assert len(g) == 100, (fA, model, len(g))
                assert set(g["split_seed"]) == set(range(100)), (fA, model)
                assert set(g["learner_seed"]) == {0}, (fA, model)
                th_med, se_adj, se_raw = median_method(g["theta"].to_numpy(),
                                                       g["se"].to_numpy())
                summary["expA"][model][learner] = {
                    "theta_median": float(th_med),
                    "se_split_adjusted": float(se_adj),
                    "se_median_raw": float(se_raw),
                    "split_sd": float(g["theta"].std(ddof=1)),
                    "theta_min": float(g["theta"].min()),
                    "theta_max": float(g["theta"].max()),
                    "m_below_trim_mean": float(g["m_below_trim"].mean()),
                }
            fB = OUT / f"e401k_expB_{learner}.csv"
            assert fB.exists(), f"필수 입력 없음: {fB}"
            if fB.exists():
                g = pd.read_csv(fB)
                g = g[g["model"] == model]
                # 완전성 검증: 분할 시드 0 고정, 학습기 시드 0..99 각 1회
                assert len(g) == 100, (fB, model, len(g))
                assert set(g["split_seed"]) == {0}, (fB, model)
                assert set(g["learner_seed"]) == set(range(100)), (fB, model)
                summary["expB"][model][learner] = {
                    "learner_sd": float(g["theta"].std(ddof=1)),
                    "theta_min": float(g["theta"].min()),
                    "theta_max": float(g["theta"].max()),
                    "n_runs": int(len(g)),
                    "distinct_values": int(g["theta"].round(6).nunique()),
                }
            fC = OUT / f"e401k_crossed_{learner}.csv"
            if learner in ("forest", "boosting"):
                assert fC.exists(), f"필수 입력 없음: {fC}"
            if fC.exists():
                g = pd.read_csv(fC)
                g = g[g["model"] == model]
                piv = g.pivot(index="split_seed", columns="learner_seed",
                              values="theta")
                # 완전성 검증: 시드 라벨 0..9의 10×10 완전 교차, 결측 없음
                assert list(piv.index) == list(range(10)), (fC, model)
                assert list(piv.columns) == list(range(10)), (fC, model)
                assert piv.shape == (10, 10) and not piv.isna().any().any(), (fC, model)
                summary["crossed"][model][learner] = variance_components(piv)

    (OUT / "e401k_summary2.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps({k: summary[k] for k in ("expA", "expB", "crossed")}, indent=2))


if __name__ == "__main__":
    main()
