"""DML 공용 루틴 — 시리즈 4편 (DML·401k) 재현 패키지.

부분선형(PLR) 모형에서 잔차화(partialling-out) 점수의 DML2 추정과 오차 항별 분해,
상호작용 모형(IRM) ATE의 직교(AIPW) 점수 추정을 담는다.
구현은 Chernozhukov, Chetverikov, Demirer, Duflo, Hansen, Newey, Robins
(2018, Econometrics Journal; arXiv:1608.00060) 의 정의를 따른다.
패키지 의존을 피하고 정의 그대로 구현한다 (검증은 원 논문 보고치와 대조).
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------
# PLR: 잔차화(partialling-out, Robinson형) 점수
#   psi(W; theta, eta) = (Y - l(X) - theta (D - m(X))) (D - m(X)),  eta = (l, m)
# DML2: (1/K) sum_k E_{n,k}[psi] = 0 을 풀면 폴드 예측을 풀링한 닫힌형이 된다.
# ---------------------------------------------------------------------------

def plr_dml2(y, d, l_hat, m_hat):
    """폴드별 장애모수(nuisance) 예측(l_hat, m_hat)이 주어졌을 때 DML2 추정.

    반환: theta, se(정리 4.1 샌드위치), vhat, uhat
      sigma^2 = (E V^2)^{-1} E[V^2 U^2] (E V^2)^{-1},  U = Y - l - theta*V
    """
    y = np.asarray(y, dtype=float)
    d = np.asarray(d, dtype=float)
    vhat = d - m_hat
    ytil = y - l_hat
    denom = np.mean(vhat ** 2)
    theta = np.mean(vhat * ytil) / denom
    uhat = ytil - theta * vhat
    n = y.shape[0]
    var = np.mean(vhat ** 2 * uhat ** 2) / denom ** 2
    se = np.sqrt(var / n)
    return theta, se, vhat, uhat


def plr_terms(theta_hat, d, m_hat, l_hat, m0, l0, u, v, theta0):
    """잔차화 점수의 정확한 오차 분해 (참 함수 기지인 시뮬레이션 전용).

    theta_hat - theta0 = a* + c* + b*   (본문 3절과 동일, 모두 theta 단위 기여분)
      Qhat = n^{-1} sum Vhat_i^2,  Vhat = D - m_hat
      a* = (n Qhat)^{-1} sum V_i U_i                                  (오라클 항)
      c* = (n Qhat)^{-1} sum (-V_i el_i + theta0 V_i em_i - em_i U_i) (교차항)
      b* = (n Qhat)^{-1} sum (em_i el_i - theta0 em_i^2)              (추정 오차 곱 항)
    여기서 em = m_hat - m0, el = l_hat - l0.
    B의 구조는 Assumption 4.1(ii)의 곱-수렴률 조건
    ||m_hat-m0||(||m_hat-m0|| + ||l_hat-l0||) 과 정확히 대응한다.

    반환: dict(a, c, b, total_check, err)  — 모두 theta 단위 기여분.
    """
    em = m_hat - m0
    el = l_hat - l0
    vhat = d - m_hat
    n = d.shape[0]
    denom = np.mean(vhat ** 2)
    scale = 1.0 / (denom * n)  # theta 단위 기여분: term/(denom*n)
    A = np.sum(v * u) * scale
    C = np.sum(-v * el + theta0 * v * em - em * u) * scale
    B = np.sum(em * el - theta0 * em ** 2) * scale
    return {
        "a": A,
        "c": C,
        "b": B,
        "total_check": A + C + B,  # == theta_hat - theta0 (수치 오차 내)
        "err": theta_hat - theta0,
    }


def naive_nonorthogonal(y_main, d_main, ghat_main, u_main, g0_main):
    """비직교 점수(논문 식 1.4)의 추정과 2항 분해.

    theta_hat = (E_n D^2)^{-1} E_n[D (Y - ghat)]
    theta_hat - theta0 = a + b   (모두 theta 단위 기여분),
      a = (n Qhat_D)^{-1} sum D_i U_i,          Qhat_D = n^{-1} sum D_i^2
      b = (n Qhat_D)^{-1} sum D_i (g0 - ghat)(X_i)
    반환: theta_hat, se(나이브 샌드위치), dict(a, b) — theta 단위.
    """
    d2 = np.mean(d_main ** 2)
    n = d_main.shape[0]
    theta_hat = np.mean(d_main * (y_main - ghat_main)) / d2
    scale = 1.0 / (d2 * n)
    a = np.sum(d_main * u_main) * scale
    b = np.sum(d_main * (g0_main - ghat_main)) * scale
    ures = y_main - d_main * theta_hat - ghat_main
    var = np.mean(d_main ** 2 * ures ** 2) / d2 ** 2
    se = np.sqrt(var / n)
    return theta_hat, se, {"a": a, "b": b}


# ---------------------------------------------------------------------------
# IRM: ATE 직교 점수 (Robins–Rotnitzky 영향함수 기반, 논문 식 5.3)
#   psi = (g(1,X)-g(0,X)) + D(Y-g(1,X))/m(X) - (1-D)(Y-g(0,X))/(1-m(X)) - theta
# ---------------------------------------------------------------------------

def irm_ate(y, d, g1_hat, g0_hat, m_hat, trim=(0.01, 0.99)):
    """IRM ATE의 DML 추정 (성향점수 예측치는 0.01/0.99로 클리핑 — 경곗값 치환, 관측치 제거 아님).

    반환: theta, se  (sigma^2 = E[psi^2])
    """
    y = np.asarray(y, dtype=float)
    d = np.asarray(d, dtype=float)
    m = np.clip(m_hat, trim[0], trim[1])
    psi_b = (g1_hat - g0_hat) + d * (y - g1_hat) / m - (1 - d) * (y - g0_hat) / (1 - m)
    theta = np.mean(psi_b)
    psi = psi_b - theta
    n = y.shape[0]
    se = np.sqrt(np.mean(psi ** 2) / n)
    return theta, se


# ---------------------------------------------------------------------------
# 교차적합 유틸리티
# ---------------------------------------------------------------------------

def kfold_indices(n, k, rng):
    """크기 n을 K개 폴드로 무작위 분할 (DML 정의의 (I_k))."""
    perm = rng.permutation(n)
    return [np.sort(perm[i::k]) for i in range(k)]


def crossfit_regression(X, t, folds, make_learner):
    """각 폴드 k에 대해 보수집합 I_k^c 로 학습기를 적합하고 I_k 에서 예측.

    make_learner() 는 fit/predict 를 갖는 새 학습기를 반환하는 팩토리.
    반환: 전체 길이 예측 벡터 (폴드별 out-of-fold 예측).
    """
    n = X.shape[0]
    pred = np.full(n, np.nan)
    for idx in folds:
        mask = np.ones(n, dtype=bool)
        mask[idx] = False
        est = make_learner()
        est.fit(X[mask], t[mask])
        pred[idx] = est.predict(X[idx])
    assert not np.isnan(pred).any()
    return pred


def crossfit_irm(X, y, d, folds, make_reg, make_clf):
    """IRM용 교차적합: 폴드 보수집합에서 처치/통제 각각의 결과회귀와 성향점수를 적합.

    반환: g1_hat, g0_hat, m_hat (전체 길이, out-of-fold)
    """
    n = X.shape[0]
    g1 = np.full(n, np.nan)
    g0 = np.full(n, np.nan)
    m = np.full(n, np.nan)
    d_bool = d.astype(bool)
    for idx in folds:
        mask = np.ones(n, dtype=bool)
        mask[idx] = False
        r1 = make_reg()
        r1.fit(X[mask & d_bool], y[mask & d_bool])
        g1[idx] = r1.predict(X[idx])
        r0 = make_reg()
        r0.fit(X[mask & ~d_bool], y[mask & ~d_bool])
        g0[idx] = r0.predict(X[idx])
        c = make_clf()
        c.fit(X[mask], d[mask])
        m[idx] = c.predict_proba(X[idx])[:, 1]
    assert not (np.isnan(g1).any() or np.isnan(g0).any() or np.isnan(m).any())
    return g1, g0, m


# ---------------------------------------------------------------------------
# 분할 변동성: 중위수법 (논문 3.4절)
# ---------------------------------------------------------------------------

def median_method(thetas, ses):
    """S회 분할 반복의 중위수 집계.

    theta_med = median_s(theta_s)
    se_med_adj^2 = median_s( se_s^2 + (theta_s - theta_med)^2 )   # 분할 조정
    se_med_raw   = median_s( se_s )                               # 비조정(논문 표의 대괄호)
    """
    thetas = np.asarray(thetas, dtype=float)
    ses = np.asarray(ses, dtype=float)
    theta_med = np.median(thetas)
    se_adj = np.sqrt(np.median(ses ** 2 + (thetas - theta_med) ** 2))
    se_raw = np.median(ses)
    return theta_med, se_adj, se_raw
