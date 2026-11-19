"""Regression checks for the methodological issues raised in peer review."""
import importlib.util
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from icu_eol_analysis.stats import fisher_table
from icu_eol_analysis.firth import fit_firth_logistic


def table_frame(a, b, c, d):
    return pd.DataFrame({"x": [1]*(a+b)+[0]*(c+d),
                         "y": [1]*a+[0]*b+[1]*c+[0]*d})


def test_main_comparison_and_conditional_interval_boundaries():
    r = fisher_table(table_frame(22, 0, 2, 4), "x", "y")
    assert np.isclose(r["p_fisher"], 0.0007326007326007326)
    assert np.isinf(r["or_conditional"])
    assert np.isinf(r["or_exact95_upper"])
    assert r["or_exact95_lower"] > 1
    reverse = fisher_table(table_frame(19, 3, 5, 0), "x", "y")
    assert reverse["or_conditional"] == reverse["or_exact95_lower"] == 0


def test_missing_binary_responses_are_not_zero():
    spec = importlib.util.spec_from_file_location("derive", ROOT / "scripts/02_derive_variables.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.category_indicator(pd.Series(["B", "A", None, "A;B"]), ["B"], list("ABCDE"))
    assert result.iloc[:2].tolist() == [1, 0]
    assert result.iloc[2:].isna().all()


def test_firth_saturated_model_matches_closed_form_half_count_solution():
    r = fit_firth_logistic(table_frame(22, 0, 2, 4), "y", ["x"])
    term = r.loc[r.term == "x"].iloc[0]
    # Saturated two-group Firth estimate equals the 0.5-cell corrected OR.
    assert np.isclose(term.OR, 81.0, rtol=1e-6)
    assert term.OR95_lower_profile < term.OR < term.OR95_upper_profile
    assert r.profile_root_max_error.max() < 1e-5


def test_documented_primary_denominators():
    d = pd.read_csv(ROOT / "data/processed/survey_responses_derived.csv")
    assert d.hukuki_guvensizlik.notna().sum() == 27
    assert d.q5b_deger_etkisi_yuksek.notna().sum() == 27
    assert d.q5c_catismayi_dile_getirmede_gucluk_yuksek.notna().sum() == 27
    assert d.loc[d.katilimci_no == 13, "hukuki_guvensizlik"].isna().all()
