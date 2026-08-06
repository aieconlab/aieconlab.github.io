"""E1·E2 — 401(k) 적격성의 순금융자산 효과 재추정 + 분할/난수 분해 실험.

데이터: 1991 SIPP (sipp1991.dta, VC2015/DMLonGitHub 저자 공개 사본, raw-local).
모형:   PLR(잔차화 점수) + IRM ATE(직교 AIPW 점수, 성향점수 예측치 0.01/0.99 클리핑)
절차:   DML2, K=5 교차적합, 중위수법(논문 3.4절)

시드 설계 (검토 반영): 외부 K-fold 분할 시드(split_seed)와 학습기 시드
(learner_seed)를 분리한다.
  expA   : learner_seed=0 고정, split_seed 0..S-1  → 순수 분할 변동 (본 표·그림)
  expB   : split_seed=0 고정, learner_seed 0..S-1  → 순수 학습기 내부 무작위성 변동
  crossed: split_seed 0..9 × learner_seed 0..9     → 2원 분산분해용

실행:  python 02_401k.py --mode expA --learner lasso [--seeds 100]
출력:  out/e401k_<mode>_<learner>.csv  (한 행 = 한 실행)
집계는 05_aggregate.py 에서 수행.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import (
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.linear_model import LassoCV, LogisticRegressionCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dml_core import (  # noqa: E402
    crossfit_irm,
    crossfit_regression,
    irm_ate,
    kfold_indices,
    plr_dml2,
)

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
DTA = HERE.parent / "data" / "raw-local" / "sipp1991.dta"
SHA256_EXPECTED = "1123d5f0abf6adae1d8e200f756d2a22b0ce0ce30cb228e69342a0098e57b4b2"

COVARS = ["age", "inc", "educ", "fsize", "marr", "twoearn", "db", "pira", "hown"]


def load_data():
    sha = hashlib.sha256(DTA.read_bytes()).hexdigest()
    assert sha == SHA256_EXPECTED, f"SHA256 mismatch: {sha}"
    df = pd.read_stata(DTA)
    assert len(df) == 9915, f"N mismatch: {len(df)}"
    X = df[COVARS].to_numpy(dtype=float)
    y = df["net_tfa"].to_numpy(dtype=float)
    d = df["e401"].to_numpy(dtype=float)
    return X, y, d


# ---------------------------------------------------------------------------
# 학습기 팩토리 — 인자는 learner_seed 파생값만 받는다 (분할 시드와 완전 분리)
# ---------------------------------------------------------------------------

def lasso_reg(seed):
    return make_pipeline(
        PolynomialFeatures(degree=2, include_bias=False),
        StandardScaler(),
        LassoCV(cv=5, alphas=40, max_iter=100000, random_state=seed),
    )


def lasso_clf(seed):
    return make_pipeline(
        PolynomialFeatures(degree=2, include_bias=False),
        StandardScaler(),
        LogisticRegressionCV(
            Cs=8, cv=3, penalty="l1", solver="liblinear", max_iter=2000,
            random_state=seed, n_jobs=-1,
        ),
    )


def rf_reg(seed):
    return RandomForestRegressor(
        n_estimators=200, min_samples_leaf=20, random_state=seed, n_jobs=-1
    )


def rf_clf(seed):
    return RandomForestClassifier(
        n_estimators=200, min_samples_leaf=20, random_state=seed, n_jobs=-1
    )


def hgb_reg(seed):
    return HistGradientBoostingRegressor(
        max_iter=200, early_stopping=True, validation_fraction=0.15,
        random_state=seed,
    )


def hgb_clf(seed):
    return HistGradientBoostingClassifier(
        max_iter=200, early_stopping=True, validation_fraction=0.15,
        random_state=seed,
    )


LEARNERS = {
    "lasso": (lasso_reg, lasso_clf),
    "forest": (rf_reg, rf_clf),
    "boosting": (hgb_reg, hgb_clf),
}


# ---------------------------------------------------------------------------

def no_control_ols(y, d):
    """공변량 미조정 회귀 (검증 기준점: 논문 19,559 / SE 1,413). HC0·HC1 로버스트 SE 병기."""
    n = len(y)
    Xd = np.column_stack([np.ones(n), d])
    beta, *_ = np.linalg.lstsq(Xd, y, rcond=None)
    resid = y - Xd @ beta
    XtX_inv = np.linalg.inv(Xd.T @ Xd)
    meat = Xd.T @ (Xd * (resid ** 2)[:, None])
    hc0 = np.sqrt(np.diag(XtX_inv @ meat @ XtX_inv))
    hc1 = hc0 * np.sqrt(n / (n - 2))
    classical = np.sqrt(np.diag(XtX_inv) * (resid @ resid) / (n - 2))
    return {
        "theta": float(beta[1]),
        "se_classical": float(classical[1]),
        "se_hc0": float(hc0[1]),
        "se_hc1": float(hc1[1]),
    }


def ols_linear_controls(y, d, X):
    """기본 9개 공변량 선형 통제 OLS (가교 행: '선형이면 얼마인가')."""
    n = len(y)
    Z = np.column_stack([np.ones(n), d, X])
    beta, *_ = np.linalg.lstsq(Z, y, rcond=None)
    resid = y - Z @ beta
    ZtZ_inv = np.linalg.inv(Z.T @ Z)
    meat = Z.T @ (Z * (resid ** 2)[:, None])
    hc1 = np.sqrt(np.diag(ZtZ_inv @ meat @ ZtZ_inv)) * np.sqrt(n / (n - Z.shape[1]))
    return {"theta": float(beta[1]), "se_hc1": float(hc1[1])}


def run_one(X, y, d, learner, split_seed, learner_seed, k_folds):
    """한 번의 파이프라인 실행. 분할과 학습기 무작위성을 독립적으로 통제한다."""
    reg_f, clf_f = LEARNERS[learner]
    rng = np.random.default_rng(20260000 + split_seed)
    folds = kfold_indices(len(y), k_folds, rng)
    ls = 90000 + 10 * learner_seed
    # PLR — 장애모수는 회귀 학습기로 (m: E[D|X] 선형확률 취급)
    l_cf = crossfit_regression(X, y, folds, lambda: reg_f(ls))
    m_cf = crossfit_regression(X, d, folds, lambda: reg_f(ls + 1))
    th_plr, se_plr, _, _ = plr_dml2(y, d, l_cf, m_cf)
    # IRM — 성향점수는 분류기(proba), 결과회귀는 처치/통제 분리 적합
    g1, g0, m = crossfit_irm(X, y, d, folds, lambda: reg_f(ls + 2), lambda: clf_f(ls + 3))
    th_irm, se_irm = irm_ate(y, d, g1, g0, m, trim=(0.01, 0.99))
    return {
        "PLR": (th_plr, se_plr), "IRM": (th_irm, se_irm),
        "m_below_trim": float(np.mean(m < 0.01)),
        "m_above_trim": float(np.mean(m > 0.99)),
    }


MODES = {
    # (split_seeds, learner_seeds) 생성기
    "expA": lambda S: [(s, 0) for s in range(S)],
    "expB": lambda S: [(0, t) for t in range(S)],
    "crossed": lambda S: [(s, t) for s in range(10) for t in range(10)],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=list(MODES), required=True)
    ap.add_argument("--learner", choices=list(LEARNERS), required=True)
    ap.add_argument("--seeds", type=int, default=100)
    ap.add_argument("--kfolds", type=int, default=5)
    args = ap.parse_args()
    if args.mode == "crossed" and args.learner == "lasso":
        ap.error("crossed 모드는 본 실험 설계상 forest/boosting 전용입니다.")

    X, y, d = load_data()
    if args.mode == "expA" and args.learner == "lasso":
        anchors = {"no_control": no_control_ols(y, d),
                   "ols_linear_controls": ols_linear_controls(y, d, X),
                   "n": len(y), "d_mean": float(d.mean())}
        (OUT / "e401k_anchors.json").write_text(json.dumps(anchors, indent=2))
        print(json.dumps(anchors, indent=2), flush=True)

    pairs = MODES[args.mode](args.seeds)
    t0 = time.time()
    rows = []
    for i, (s, t) in enumerate(pairs):
        r = run_one(X, y, d, args.learner, s, t, args.kfolds)
        for model in ("PLR", "IRM"):
            th, se = r[model]
            rows.append({"mode": args.mode, "model": model, "learner": args.learner,
                         "split_seed": s, "learner_seed": t, "theta": th, "se": se,
                         "m_below_trim": r["m_below_trim"],
                         "m_above_trim": r["m_above_trim"]})
        if (i + 1) % 10 == 0:
            print(f"[{args.mode}/{args.learner}] {i+1}/{len(pairs)} "
                  f"elapsed {time.time()-t0:.0f}s", flush=True)
    pd.DataFrame(rows).to_csv(OUT / f"e401k_{args.mode}_{args.learner}.csv", index=False)
    print(f"done {args.mode}/{args.learner} in {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
