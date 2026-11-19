"""Minimal Firth penalized logistic regression implementation.

Supplementary exploratory models use the adjusted Firth score, full-model
profile penalized-likelihood confidence limits and penalized LR tests. Wald
columns remain diagnostic only and are not used in revised manuscript tables.
"""
from __future__ import annotations

import math
import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.stats import chi2
from scipy.optimize import minimize, brentq


def _logit_inv(eta: np.ndarray) -> np.ndarray:
    eta = np.clip(eta, -35, 35)
    return 1.0 / (1.0 + np.exp(-eta))


def _penalized_loglik(X: np.ndarray, y: np.ndarray, beta: np.ndarray) -> float:
    eta = X @ beta
    p = _logit_inv(eta)
    eps = 1e-12
    ll = np.sum(y * np.log(p + eps) + (1 - y) * np.log(1 - p + eps))
    w = p * (1 - p)
    info = X.T @ (w[:, None] * X)
    sign, logdet = np.linalg.slogdet(info)
    if sign <= 0:
        logdet = -1e12
    return float(ll + 0.5 * logdet)


def _profile_inference(X, y, beta, index):
    """Profile the full-model Jeffreys penalty with one coefficient fixed.

    The determinant always uses the full design matrix, including the fixed
    term. Dropping that column would change the penalty and invalidate the LR.
    """
    free = np.arange(X.shape[1]) != index
    optimum = _penalized_loglik(X, y, beta)
    def profile(value):
        start = beta.copy()
        start[index] = value
        if not free.any():
            return _penalized_loglik(X, y, start)
        def objective(nuisance):
            b = start.copy()
            b[free] = nuisance
            return -_penalized_loglik(X, y, b)
        result = minimize(objective, start[free], method="Nelder-Mead",
            options={"maxiter": 3000, "xatol": 1e-9, "fatol": 1e-10})
        if not result.success or not np.isfinite(result.fun):
            raise RuntimeError("Constrained Firth optimization did not converge")
        return -result.fun
    target = chi2.ppf(0.95, 1)
    def equation(value):
        return 2 * (optimum - profile(value)) - target
    roots = []
    for direction in [-1, 1]:
        step = 1.0
        edge = beta[index] + direction * step
        while equation(edge) < 0 and step < 64:
            step *= 2
            edge = beta[index] + direction * step
        if equation(edge) < 0:
            raise RuntimeError("Could not bracket Firth profile confidence limit")
        roots.append(brentq(equation, min(edge, beta[index]), max(edge, beta[index]), xtol=1e-7))
    statistic = max(0.0, 2 * (optimum - profile(0.0)))
    return roots[0], roots[1], float(chi2.sf(statistic, 1)), [equation(v) for v in roots]


def fit_firth_logistic(
    df: pd.DataFrame,
    outcome: str,
    predictors: list[str],
    max_iter: int = 200,
    tol: float = 1e-8,
) -> pd.DataFrame:
    """Fit a Firth penalized logistic regression model.

    Parameters
    ----------
    df:
        Data frame containing binary outcome and predictors.
    outcome:
        Binary dependent variable coded 0/1.
    predictors:
        Binary or numeric predictors.

    Returns
    -------
    pandas.DataFrame
        One row per term, including OR, profile 95% CI and penalized LR p.
    """
    cols = [outcome] + predictors
    tmp = df[cols].apply(pd.to_numeric, errors="coerce").dropna().copy()
    n = len(tmp)
    y = tmp[outcome].to_numpy(dtype=float)
    X_pred = tmp[predictors].to_numpy(dtype=float)
    X = np.column_stack([np.ones(n), X_pred])
    if not n or not np.isin(y, [0, 1]).all():
        raise ValueError("Firth outcome must contain binary nonmissing observations")
    if np.linalg.matrix_rank(X) < X.shape[1]:
        raise ValueError("Firth design matrix is rank deficient")
    terms = ["Intercept"] + predictors

    beta = np.zeros(X.shape[1], dtype=float)
    success = False

    for _ in range(max_iter):
        eta = X @ beta
        p = _logit_inv(eta)
        w = np.clip(p * (1 - p), 1e-12, None)
        info = X.T @ (w[:, None] * X)
        inv_info = np.linalg.pinv(info)

        # Leverage values: diagonal of W^(1/2) X I^-1 X' W^(1/2).
        Xw = X * np.sqrt(w)[:, None]
        h = np.einsum("ij,jk,ik->i", Xw, inv_info, Xw)

        # Adjusted score for Firth logistic regression.
        adjusted_residual = y - p + h * (0.5 - p)
        score = X.T @ adjusted_residual
        step = inv_info @ score

        current_ll = _penalized_loglik(X, y, beta)
        step_factor = 1.0
        while step_factor > 1e-8:
            candidate = beta + step_factor * step
            if _penalized_loglik(X, y, candidate) >= current_ll - 1e-10:
                break
            step_factor *= 0.5

        beta_new = beta + step_factor * step
        if np.max(np.abs(beta_new - beta)) < tol:
            beta = beta_new
            success = True
            break
        beta = beta_new

    p = _logit_inv(X @ beta)
    w = np.clip(p * (1 - p), 1e-12, None)
    info = X.T @ (w[:, None] * X)
    cov = np.linalg.pinv(info)
    se = np.sqrt(np.clip(np.diag(cov), 0, np.inf))

    rows = []
    if not success:
        raise RuntimeError("Firth adjusted-score iteration failed to converge")
    for index, (term, b, s) in enumerate(zip(terms, beta, se)):
        lower, upper, p_profile, residuals = _profile_inference(X, y, beta, index)
        # Wald-type p-values are approximate and are intended only for
        # transparent reporting in this pilot analysis. The revised tables use profile intervals and penalized LR p-values.
        z_value = b / s if s > 0 else np.nan
        p_wald = 2 * norm.sf(abs(z_value)) if np.isfinite(z_value) else np.nan
        rows.append({
            "n": n,
            "sonuc": outcome,
            "term": term,
            "beta": float(b),
            "se_approx": float(s),
            "OR": float(math.exp(b)),
            "OR95_alt_approx": float(math.exp(b - 1.959963984540054 * s)),
            "OR95_ust_approx": float(math.exp(b + 1.959963984540054 * s)),
            "p_wald_approx": float(p_wald) if np.isfinite(p_wald) else np.nan,
            "OR95_lower_profile": float(math.exp(lower)),
            "OR95_upper_profile": float(math.exp(upper)),
            "p_penalized_LR": p_profile,
            "profile_root_max_error": max(abs(v) for v in residuals),
            "events": int(y.sum()),
            "non_events": int(n-y.sum()),
            "success": bool(success),
        })
    return pd.DataFrame(rows)

