"""Minimal Firth penalized logistic regression implementation.

This implementation is designed for small pilot analyses with binary outcomes.
It uses the adjusted score equation for Firth's bias-reduced logistic
regression and reports approximate standard errors from the final information
matrix. For confirmatory analyses, the model should be replicated in a
specialized statistical package.
"""
from __future__ import annotations

import math
import numpy as np
import pandas as pd
from scipy.stats import norm


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
        One row per term, including approximate OR and 95% CI.
    """
    cols = [outcome] + predictors
    tmp = df[cols].apply(pd.to_numeric, errors="coerce").dropna().copy()
    n = len(tmp)
    y = tmp[outcome].to_numpy(dtype=float)
    X_pred = tmp[predictors].to_numpy(dtype=float)
    X = np.column_stack([np.ones(n), X_pred])
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
    for term, b, s in zip(terms, beta, se):
        # Wald-type p-values are approximate and are intended only for
        # transparent reporting in this pilot analysis. The manuscript
        # interprets Firth models primarily by effect direction and CI width.
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
            "success": bool(success),
        })
    return pd.DataFrame(rows)
