"""S1·S2 몬테카를로 — 시리즈 4편 (DML) 재현 패키지.

S1: 세 절차의 비교 + 오차 항별 직접 측정
  Arm A  비직교 점수 + 표본 분할     (정규화 편향 b가 남는다)
  Arm B  직교 점수 + 분할 없음       (과적합 항 c*가 남는다)
  Arm C  직교 점수 + K=5 교차적합    (DML2 — 둘 다 제거)
  Oracle 참 장애모수              (a*만 남는 기준분포)
  참 함수를 알고 있으므로 a/b(2항), a*/c*/b*(3항)를 정확히 직접 측정한다.

S2: 곱-수렴률 조건의 이빨
  장애모수를 라쏘(2차 다항 사전)로 추정하되 벌점을 CV 최적의 c배로
  올려 수렴률을 인위적으로 늦춘다. c ∈ {1,3,10,30,100}.
  직접 계산한 곱-수렴률 통계 sqrt(n)·rmse_m·(rmse_m+rmse_l) 와 편향·포함률의 동행.

실행:  python 01_simulation.py [--pilot]
출력:  out/sim_s1_reps.csv, out/sim_s1_summary.json,
       out/sim_s2_reps.csv, out/sim_s2_summary.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy import linalg  # noqa: F401  (cholesky는 numpy로 충분하지만 명시 기록)
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso, LassoCV, LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dml_core import (  # noqa: E402
    kfold_indices,
    crossfit_regression,
    naive_nonorthogonal,
    plr_dml2,
    plr_terms,
)

OUT = Path(__file__).resolve().parent / "out"
OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# DGP (부분선형 모형, theta0 = 0.5)
#   m0(x) = sigma(3 x1) - 1/2 + 0.25 x2          (처치식)
#   g0(x) = 3 sigma(3 x1) + 0.5 x2 x3            (결과식)
#   X ~ N(0, Sigma), Sigma_jk = 0.5^{|j-k|}, p = 10
#   V ~ N(0, 0.75^2), U ~ N(0, 1)
# m0와 g0가 같은 방향(x1의 시그모이드)을 공유하므로, ghat의 평활화(정규화)
# 편향은 m0와 양의 상관을 갖고 -> 비직교 점수의 b항이 양(+)으로 남는다.
# ---------------------------------------------------------------------------

P_DIM = 10
THETA0 = 0.5
SD_V = 0.75
SD_U = 1.0


def sigmoid(u):
    return 1.0 / (1.0 + np.exp(-u))


def m0_fun(X):
    return sigmoid(3.0 * X[:, 0]) - 0.5 + 0.25 * X[:, 1]


def g0_fun(X):
    return 3.0 * sigmoid(3.0 * X[:, 0]) + 0.5 * X[:, 1] * X[:, 2]


def draw(n, rng):
    corr = 0.5 ** np.abs(np.subtract.outer(np.arange(P_DIM), np.arange(P_DIM)))
    L = np.linalg.cholesky(corr)
    X = rng.standard_normal((n, P_DIM)) @ L.T
    m0 = m0_fun(X)
    g0 = g0_fun(X)
    v = rng.normal(0.0, SD_V, n)
    u = rng.normal(0.0, SD_U, n)
    d = m0 + v
    y = THETA0 * d + g0 + u
    l0 = THETA0 * m0 + g0
    return X, y, d, m0, g0, l0, u, v


def make_rf(seed):
    return RandomForestRegressor(
        n_estimators=200, min_samples_leaf=5, random_state=seed, n_jobs=-1
    )


# ---------------------------------------------------------------------------
# S1
# ---------------------------------------------------------------------------

def s1_one_rep(rep, n, k_folds, rng):
    X, y, d, m0, g0, l0, u, v = draw(n, rng)
    z = 1.959963984540054  # Phi^{-1}(0.975)
    row = {"rep": rep}

    # ---- Oracle: 참 장애모수 ----
    th, se, _, _ = plr_dml2(y, d, l0, m0)
    row.update(oracle_theta=th, oracle_se=se,
               oracle_cover=int(abs(th - THETA0) <= z * se))

    # ---- Arm A: 비직교 + 50/50 분할, ghat은 theta 오프셋 반복(3회) ----
    n_half = n // 2
    idx = rng.permutation(n)
    aux, main = idx[:n_half], idx[n_half:]
    th_a = LinearRegression().fit(d[aux].reshape(-1, 1), y[aux]).coef_[0]
    ghat_est = None
    for it in range(3):
        ghat_est = make_rf(seed=100000 + rep * 10 + it)
        ghat_est.fit(X[aux], y[aux] - d[aux] * th_a)
        th_a = np.mean(d[aux] * (y[aux] - ghat_est.predict(X[aux]))) / np.mean(d[aux] ** 2)
    ghat_main = ghat_est.predict(X[main])
    th, se, terms = naive_nonorthogonal(y[main], d[main], ghat_main, u[main], g0[main])
    row.update(armA_theta=th, armA_se=se,
               armA_cover=int(abs(th - THETA0) <= z * se),
               armA_term_a=terms["a"], armA_term_b=terms["b"])

    # ---- Arm B: 직교 + 분할 없음 (결과 쪽 ℓ̂을 자기 관측 포함 전체 표본으로 적합) ----
    #   과적합 유입 경로를 결과 쪽으로 고립: m̂은 교차적합 유지 (원 논문 그림 2와 같은 구조).
    rf_l = make_rf(seed=200000 + rep)
    rf_l.fit(X, y)
    l_in = rf_l.predict(X)
    folds_b = kfold_indices(n, k_folds, rng)
    m_cf_b = crossfit_regression(X, d, folds_b, lambda: make_rf(seed=300000 + rep))
    th, se, _, _ = plr_dml2(y, d, l_in, m_cf_b)
    tb = plr_terms(th, d, m_cf_b, l_in, m0, l0, u, v, THETA0)
    row.update(armB_theta=th, armB_se=se,
               armB_cover=int(abs(th - THETA0) <= z * se),
               armB_term_a=tb["a"], armB_term_c=tb["c"], armB_term_b=tb["b"],
               armB_r2_l_in=1 - np.mean((y - l_in) ** 2) / np.var(y))

    # ---- Arm Bsym (각주용): 직교 + 양쪽 장애모수 모두 자기 표본 적합 ----
    #   두 흡수 효과가 평균에서 상쇄될 수 있음을 기록하기 위한 참고 팔.
    rf_m_in = make_rf(seed=310000 + rep)
    rf_m_in.fit(X, d)
    m_in = rf_m_in.predict(X)
    th, se, _, _ = plr_dml2(y, d, l_in, m_in)
    tbs = plr_terms(th, d, m_in, l_in, m0, l0, u, v, THETA0)
    row.update(armBsym_theta=th, armBsym_se=se,
               armBsym_cover=int(abs(th - THETA0) <= z * se),
               armBsym_term_a=tbs["a"], armBsym_term_c=tbs["c"],
               armBsym_term_b=tbs["b"])

    # ---- Arm C: 직교 + K폴드 교차적합 (DML2) — B와 동일한 학습기 사양 ----
    folds = kfold_indices(n, k_folds, rng)
    l_cf = crossfit_regression(X, y, folds, lambda: make_rf(seed=400000 + rep))
    m_cf = crossfit_regression(X, d, folds, lambda: make_rf(seed=500000 + rep))
    th, se, _, _ = plr_dml2(y, d, l_cf, m_cf)
    tc = plr_terms(th, d, m_cf, l_cf, m0, l0, u, v, THETA0)
    row.update(armC_theta=th, armC_se=se,
               armC_cover=int(abs(th - THETA0) <= z * se),
               armC_term_a=tc["a"], armC_term_c=tc["c"], armC_term_b=tc["b"],
               armC_rmse_l=float(np.sqrt(np.mean((l_cf - l0) ** 2))),
               armC_rmse_m=float(np.sqrt(np.mean((m_cf - m0) ** 2))))
    return row


# ---------------------------------------------------------------------------
# S2: 라쏘 벌점 배율 스트레스 테스트
#   S2 전용 DGP — 참 함수가 2차 다항 사전 안에 정확히 들어 있는 희소 설계.
#   c=1(CV 최적)에서 곱-수렴률 조건이 편안히 성립해 명목 포함률이 재현되고,
#   벌점을 c배로 올리면 나머지항이 커지는 만큼 편향은 증가하고 포함률은 낮아진다.
#   c→∞ 극한에서 두 학습기는 상수 예측으로 퇴화하므로 추정치는
#   '공변량 미조정 회귀'로 퇴화한다: 편향 극한 = Cov(m0, g0) / Var(D).
# ---------------------------------------------------------------------------

def m0_s2(X):
    return 0.5 * X[:, 0] + 0.3 * X[:, 1] * X[:, 2]


def g0_s2(X):
    return X[:, 0] + 0.8 * (X[:, 1] ** 2 - 1.0) + 0.6 * X[:, 3]


def draw_s2(n, rng):
    corr = 0.5 ** np.abs(np.subtract.outer(np.arange(P_DIM), np.arange(P_DIM)))
    L = np.linalg.cholesky(corr)
    X = rng.standard_normal((n, P_DIM)) @ L.T
    m0 = m0_s2(X)
    g0 = g0_s2(X)
    v = rng.normal(0.0, SD_V, n)
    u = rng.normal(0.0, SD_U, n)
    d = m0 + v
    y = THETA0 * d + g0 + u
    l0 = THETA0 * m0 + g0
    return X, y, d, m0, g0, l0, u, v


def s2_ovb_limit():
    """c→∞ 극한의 누락변수 편향 Cov(m0, g0)/Var(D) — 가우스 적률로 해석적 계산.

    Σ가 Toeplitz(0.5)일 때 E[x1 x4]=0.5^3, E[x2^3 x3]=3ρ23, E[x2 x3]=ρ23=0.5,
    Var(x2 x3)=1+ρ23^2 이므로
      Cov(m0, g0) = 0.5·1 + 0.5·0.6·0.5^3 + 0.3·0.8·(3·0.5 − 0.5) = 0.7775
      Var(m0)     = 0.25 + 0.09·(1 + 0.25) = 0.3625
      Var(D)      = Var(m0) + 0.75^2 = 0.925
      OVB_∞       = 0.7775 / 0.925 = 0.84054054…
    몬테카를로 교차 확인은 s2_ovb_limit_mc() 참조.
    """
    cov = 0.5 * 1.0 + 0.5 * 0.6 * 0.5 ** 3 + 0.3 * 0.8 * (3 * 0.5 - 0.5)
    var_d = (0.25 + 0.09 * 1.25) + 0.75 ** 2
    return cov / var_d


def s2_ovb_limit_mc(n_big=4_000_000, seed=123):
    """해석값의 몬테카를로 교차 확인 (시드 123, 4백만 관측치에서 약 0.8401)."""
    rng = np.random.default_rng(seed)
    X, y, d, m0, g0, l0, u, v = draw_s2(n_big, rng)
    return float(np.cov(m0, g0)[0, 1] / np.var(d))


def poly_lasso(alpha):
    return make_pipeline(
        PolynomialFeatures(degree=2, include_bias=False),
        StandardScaler(),
        Lasso(alpha=alpha, max_iter=50000),
    )


def s2_one_rep(rep, n, k_folds, c_grid, rng):
    X, y, d, m0, g0, l0, u, v = draw_s2(n, rng)
    z = 1.959963984540054
    folds = kfold_indices(n, k_folds, rng)
    # CV 기준 벌점을 '각 학습 폴드(I_k^c) 안에서' 선택 — 검증 폴드 누수 차단.
    # 각 폴드의 기준 벌점에 c를 곱해 같은 폴드에서 재적합·예측한다.
    base = {"l": [], "m": []}
    for idx in folds:
        mask = np.ones(n, dtype=bool)
        mask[idx] = False
        for name, t in (("l", y), ("m", d)):
            cv = make_pipeline(
                PolynomialFeatures(degree=2, include_bias=False),
                StandardScaler(),
                LassoCV(cv=5, alphas=40, max_iter=50000, random_state=0),
            )
            cv.fit(X[mask], t[mask])
            base[name].append(cv.named_steps["lassocv"].alpha_)
    rows = []
    for c in c_grid:
        l_cf = np.full(n, np.nan)
        m_cf = np.full(n, np.nan)
        for k, idx in enumerate(folds):
            mask = np.ones(n, dtype=bool)
            mask[idx] = False
            est_l = poly_lasso(base["l"][k] * c)
            est_l.fit(X[mask], y[mask])
            l_cf[idx] = est_l.predict(X[idx])
            est_m = poly_lasso(base["m"][k] * c)
            est_m.fit(X[mask], d[mask])
            m_cf[idx] = est_m.predict(X[idx])
        th, se, _, _ = plr_dml2(y, d, l_cf, m_cf)
        t3 = plr_terms(th, d, m_cf, l_cf, m0, l0, u, v, THETA0)
        rmse_l = float(np.sqrt(np.mean((l_cf - l0) ** 2)))
        rmse_m = float(np.sqrt(np.mean((m_cf - m0) ** 2)))
        rows.append({
            "rep": rep, "c": c, "theta": th, "se": se,
            "cover": int(abs(th - THETA0) <= z * se),
            "term_a": t3["a"], "term_c": t3["c"], "term_b": t3["b"],
            "rmse_l": rmse_l, "rmse_m": rmse_m,
            "prod_stat": float(np.sqrt(n) * rmse_m * (rmse_m + rmse_l)),
        })
    return rows


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--s2-only", action="store_true")
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--reps", type=int, default=500)
    ap.add_argument("--reps-s2", type=int, default=500)
    ap.add_argument("--kfolds", type=int, default=5)
    args = ap.parse_args()
    reps = 40 if args.pilot else args.reps
    reps_s2 = 40 if args.pilot else args.reps_s2
    c_grid = [1, 3, 10, 30, 100]

    import pandas as pd

    t0 = time.time()
    if not args.s2_only:
        rows = []
        for rep in range(reps):
            rng = np.random.default_rng(20260804 + rep)
            rows.append(s1_one_rep(rep, args.n, args.kfolds, rng))
            if (rep + 1) % 25 == 0:
                print(f"[S1] {rep+1}/{reps}  elapsed {time.time()-t0:.0f}s", flush=True)
        s1 = pd.DataFrame(rows)
        s1.to_csv(OUT / "sim_s1_reps.csv", index=False)
    else:
        s1 = pd.read_csv(OUT / "sim_s1_reps.csv")

    def summ(prefix, extra_terms):
        th = s1[f"{prefix}_theta"]
        out = {
            "mean": float(th.mean()), "bias": float(th.mean() - THETA0),
            "sd": float(th.std(ddof=1)), "rmse": float(np.sqrt(((th - THETA0) ** 2).mean())),
            "coverage": float(s1[f"{prefix}_cover"].mean()),
            "median_se": float(s1[f"{prefix}_se"].median()),
        }
        for t in extra_terms:
            col = f"{prefix}_term_{t}"
            if col in s1:
                out[f"term_{t}_mean"] = float(s1[col].mean())
                out[f"term_{t}_sd"] = float(s1[col].std(ddof=1))
        return out

    s1_summary = {
        "config": {"n": args.n, "reps": reps, "kfolds": args.kfolds,
                    "theta0": THETA0, "p": P_DIM, "sd_v": SD_V, "sd_u": SD_U,
                    "rf": "n_estimators=200, min_samples_leaf=5"},
        "oracle": summ("oracle", []),
        "armA": summ("armA", ["a", "b"]),
        "armB": summ("armB", ["a", "c", "b"]),
        "armBsym": summ("armBsym", ["a", "c", "b"]),
        "armC": summ("armC", ["a", "c", "b"]),
        "armB_r2_l_insample_mean": float(s1["armB_r2_l_in"].mean()),
        "armC_rmse_l_mean": float(s1["armC_rmse_l"].mean()),
        "armC_rmse_m_mean": float(s1["armC_rmse_m"].mean()),
    }
    (OUT / "sim_s1_summary.json").write_text(json.dumps(s1_summary, indent=2))
    print(json.dumps(s1_summary, indent=2), flush=True)

    rows2 = []
    for rep in range(reps_s2):
        rng = np.random.default_rng(90000000 + rep)
        rows2.extend(s2_one_rep(rep, args.n, args.kfolds, c_grid, rng))
        if (rep + 1) % 25 == 0:
            print(f"[S2] {rep+1}/{reps_s2}  elapsed {time.time()-t0:.0f}s", flush=True)
    s2 = pd.DataFrame(rows2)
    s2.to_csv(OUT / "sim_s2_reps.csv", index=False)
    s2_summary = {"config": {"n": args.n, "reps": reps_s2, "c_grid": c_grid,
                              "dgp": "m0=0.5x1+0.3x2x3, g0=x1+0.8(x2^2-1)+0.6x4",
                              "ovb_limit_method": "해석적 (가우스 적률; s2_ovb_limit 도출 참조)"},
                  "ovb_limit": s2_ovb_limit(),
                  "by_c": {}}
    for c in c_grid:
        g = s2[s2["c"] == c]
        s2_summary["by_c"][str(c)] = {
            "bias": float(g["theta"].mean() - THETA0),
            "sd": float(g["theta"].std(ddof=1)),
            "coverage": float(g["cover"].mean()),
            "prod_stat_mean": float(g["prod_stat"].mean()),
            "rmse_l_mean": float(g["rmse_l"].mean()),
            "rmse_m_mean": float(g["rmse_m"].mean()),
            "term_b_mean": float(g["term_b"].mean()),
        }
    (OUT / "sim_s2_summary.json").write_text(json.dumps(s2_summary, indent=2))
    print(json.dumps(s2_summary, indent=2), flush=True)
    print(f"done in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
