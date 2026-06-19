"""Statistical helper functions for the pilot survey analysis.

The functions are intentionally small and transparent so that reviewers can
inspect each calculation.
"""
from __future__ import annotations

import math
from typing import Iterable

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact


def wilson_ci(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """Wilson score confidence interval for a binomial proportion.

    Parameters
    ----------
    k:
        Number of positive observations.
    n:
        Number of valid observations.
    z:
        Standard normal quantile. The default is approximately 95%.

    Returns
    -------
    tuple[float, float]
        Lower and upper bounds as percentages.
    """
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    denom = 1 + (z**2 / n)
    centre = p + (z**2 / (2 * n))
    half_width = z * math.sqrt((p * (1 - p) / n) + (z**2 / (4 * n**2)))
    lower = (centre - half_width) / denom
    upper = (centre + half_width) / denom
    return lower * 100, upper * 100


def summarize_categorical(df: pd.DataFrame, variables: Iterable[str]) -> pd.DataFrame:
    """Return frequency table with Wilson intervals for each category."""
    rows: list[dict] = []
    for var in variables:
        valid = df[var].dropna()
        denom = len(valid)
        counts = valid.value_counts(dropna=True).sort_index()
        for category, n in counts.items():
            lo, hi = wilson_ci(int(n), denom)
            rows.append({
                "degisken": var,
                "kategori": category,
                "n": int(n),
                "yuzde": (n / denom * 100) if denom else np.nan,
                "wilson95_alt": lo,
                "wilson95_ust": hi,
                "payda": denom,
            })
    return pd.DataFrame(rows)


def summarize_binary_indicators(df: pd.DataFrame, indicators: Iterable[str]) -> pd.DataFrame:
    """Summarize binary indicators coded as 0/1 with Wilson intervals."""
    rows: list[dict] = []
    for col in indicators:
        s = pd.to_numeric(df[col], errors="coerce").dropna()
        n = int(len(s))
        k = int((s == 1).sum())
        lo, hi = wilson_ci(k, n)
        rows.append({
            "gosterge": col,
            "n_pozitif": k,
            "payda": n,
            "yuzde": (k / n * 100) if n else np.nan,
            "wilson95_alt": lo,
            "wilson95_ust": hi,
        })
    return pd.DataFrame(rows)


def fisher_table(df: pd.DataFrame, exposure: str, outcome: str) -> dict:
    """Compute a 2x2 Fisher exact test and Haldane-Anscombe OR CI.

    The 2x2 layout is:
        [[a, b], [c, d]]
    where rows represent exposure=1/exposure=0 and columns represent
    outcome=1/outcome=0.
    """
    tmp = df[[exposure, outcome]].dropna().copy()
    tmp[exposure] = pd.to_numeric(tmp[exposure], errors="coerce")
    tmp[outcome] = pd.to_numeric(tmp[outcome], errors="coerce")
    tmp = tmp.dropna()

    a = int(((tmp[exposure] == 1) & (tmp[outcome] == 1)).sum())
    b = int(((tmp[exposure] == 1) & (tmp[outcome] == 0)).sum())
    c = int(((tmp[exposure] == 0) & (tmp[outcome] == 1)).sum())
    d = int(((tmp[exposure] == 0) & (tmp[outcome] == 0)).sum())

    table = [[a, b], [c, d]]
    fisher_or, p_value = fisher_exact(table, alternative="two-sided")

    # Haldane-Anscombe correction for approximate OR CI when cells are sparse.
    ah, bh, ch, dh = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    or_ha = (ah * dh) / (bh * ch)
    se_log_or = math.sqrt(1 / ah + 1 / bh + 1 / ch + 1 / dh)
    lo = math.exp(math.log(or_ha) - 1.959963984540054 * se_log_or)
    hi = math.exp(math.log(or_ha) + 1.959963984540054 * se_log_or)

    exp1_total = a + b
    exp0_total = c + d
    rate1 = a / exp1_total if exp1_total else np.nan
    rate0 = c / exp0_total if exp0_total else np.nan

    return {
        "maruziyet": exposure,
        "sonuc": outcome,
        "n": int(len(tmp)),
        "a_exp1_out1": a,
        "b_exp1_out0": b,
        "c_exp0_out1": c,
        "d_exp0_out0": d,
        "pozitif_oran_exp1": rate1,
        "pozitif_oran_exp0": rate0,
        "risk_farki": rate1 - rate0 if pd.notna(rate1) and pd.notna(rate0) else np.nan,
        "fisher_or": fisher_or,
        "or_ha_95_alt": lo,
        "or_ha_95_ust": hi,
        "p_fisher": p_value,
    }
