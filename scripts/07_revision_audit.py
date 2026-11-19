"""Write machine-readable checks connecting revised manuscript and analysis."""
from pathlib import Path
import json
import platform
import sys
import hashlib
import pandas as pd
import scipy
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def main():
    raw_path = ROOT / "data/raw/survey_responses_deidentified.csv"
    d = pd.read_csv(ROOT / "data/processed/survey_responses_derived.csv")
    f = pd.read_csv(ROOT / "outputs/tables/fisher_exact_tests.csv")
    p = pd.read_csv(ROOT / "outputs/tables/firth_logistic_models.csv")
    paired = d.loc[d.hukuki_bilgi_dogru.eq(1) & d.hukuki_guvensizlik.notna()]
    report = {
        "upstream_source_commit": "c4946ab57f47dd80444a0380b5f03cc39fd26678",
        "raw_sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest(),
        "n": len(d), "knowledge_correct": int(d.hukuki_bilgi_dogru.sum()),
        "low_security": int(d.hukuki_guvensizlik.sum()),
        "security_denominator": int(d.hukuki_guvensizlik.notna().sum()),
        "correct_item_with_valid_security": len(paired),
        "correct_item_and_low_security": int(paired.hukuki_guvensizlik.sum()),
        "legal_regulation": int(d.yasal_duzenleme_talebi.sum()),
        "written_protocol": int(d.dnr_protokol_talebi.sum()),
        "both_preferences": int((d.yasal_duzenleme_talebi.eq(1) & d.dnr_protokol_talebi.eq(1)).sum()),
        "either_preference": int(d.hukuki_prosedurel_cozum.sum()),
        "education_selected": int(d.q6_D_hekim_egitimi.sum()),
        "tests_in_multiplicity_family": len(f),
        "profile_models_all_converged": bool(p.success.all()),
        "max_profile_root_error": float(p.profile_root_max_error.max()),
        "versions": {"python": platform.python_version(), "pandas": pd.__version__,
                     "numpy": np.__version__, "scipy": scipy.__version__},
    }
    assert report["correct_item_and_low_security"] == 19
    assert report["both_preferences"] == 8
    assert report["max_profile_root_error"] < 1e-5
    target = ROOT / "outputs/logs/revision_audit.json"
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Revision audit passed")


if __name__ == "__main__":
    main()
