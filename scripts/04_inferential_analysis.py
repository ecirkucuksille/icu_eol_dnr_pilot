from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
from icu_eol_analysis.config import DERIVED_SURVEY_CSV, OUTPUT_TABLES
from icu_eol_analysis.io import write_csv
from icu_eol_analysis.stats import fisher_table
from icu_eol_analysis.firth import fit_firth_logistic

FISHER_PAIRS = [
    ("hukuki_bilgi_dogru", "hukuki_guvensizlik"),
    ("aktif_rol_var", "etik_esdegerlik"),
    ("aktif_rol_var", "withdraw_daha_agir"),
    ("aktif_rol_var", "riskten_kacinan_tedaviye_devam"),
    ("hukuki_risk_ana_engel", "hukuki_prosedurel_cozum"),
    ("hukuki_guvensizlik", "hukuki_prosedurel_cozum"),
    ("hukuki_bilgi_dogru", "hukuki_prosedurel_cozum"),
    ("q5a_yetkinlik_yuksek", "paylasimli_kurumsal_karar"),
    ("q5b_deger_etkisi_yuksek", "riskten_kacinan_tedaviye_devam"),
]

FIRTH_MODELS = {
    "M1_hukuki_guvensizlik_bilgi_aktif": (
        "hukuki_guvensizlik", ["hukuki_bilgi_dogru", "aktif_rol_var"]
    ),
    "M2_hukuki_prosedurel_cozum_risk_guven": (
        "hukuki_prosedurel_cozum", ["hukuki_risk_ana_engel", "hukuki_guvensizlik"]
    ),
    "M3_tedaviye_devam_guven_bilgi": (
        "riskten_kacinan_tedaviye_devam", ["hukuki_guvensizlik", "hukuki_bilgi_dogru"]
    ),
}


def main() -> None:
    df = pd.read_csv(DERIVED_SURVEY_CSV, encoding="utf-8")
    OUTPUT_TABLES.mkdir(parents=True, exist_ok=True)

    fisher_results = pd.DataFrame([fisher_table(df, exp, out) for exp, out in FISHER_PAIRS])
    # Nine exploratory tests form one family. Holm is reported for transparency.
    import numpy as np
    p = fisher_results["p_fisher"].to_numpy()
    order = np.argsort(p)
    holm = np.maximum.accumulate((len(p)-np.arange(len(p))) * p[order]).clip(0, 1)
    fisher_results.loc[order, "p_holm_9_tests"] = holm
    write_csv(fisher_results, OUTPUT_TABLES / "fisher_exact_tests.csv")

    firth_rows = []
    for model_name, (outcome, predictors) in FIRTH_MODELS.items():
        result = fit_firth_logistic(df, outcome, predictors)
        result.insert(0, "model", model_name)
        firth_rows.append(result)
    firth_results = pd.concat(firth_rows, ignore_index=True)
    write_csv(firth_results, OUTPUT_TABLES / "firth_logistic_models.csv")

    sensitivity = []
    scenarios = {
        "confidence_double_mark_as_1": df.assign(hukuki_guvensizlik=df["hukuki_guvensizlik_sens"]),
        "confidence_double_mark_as_3": df.assign(hukuki_guvensizlik=df["hukuki_guvensizlik_sens_high"]),
        "all_barriers_includes_legal_risk": df.assign(hukuki_risk_ana_engel=df["hukuki_risk_ana_engel_sens"]),
        "exclude_three_solution_selections": df.loc[df.filter(regex="^q6_[A-F]_").sum(axis=1) <= 2],
    }
    for name, subset in scenarios.items():
        for exposure, outcome in [("hukuki_risk_ana_engel", "hukuki_prosedurel_cozum"),
                                  ("hukuki_guvensizlik", "hukuki_prosedurel_cozum")]:
            sensitivity.append({"scenario": name, **fisher_table(subset, exposure, outcome)})
    write_csv(pd.DataFrame(sensitivity), OUTPUT_TABLES / "sensitivity_analyses.csv")

    print("Inferential analysis completed.")


if __name__ == "__main__":
    main()

