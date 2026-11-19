from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
from icu_eol_analysis.config import DERIVED_SURVEY_CSV, OUTPUT_TABLES
from icu_eol_analysis.io import write_csv
from icu_eol_analysis.stats import summarize_categorical, summarize_binary_indicators

CATEGORICAL_VARIABLES = [
    "unvan",
    "birim",
    "mesleki_deneyim",
    "onceki_yasam_sonu_kararda_aktif_rol",
    "q1_hukuki_bilgi",
    "q2_withholding_withdrawing_ayrimi",
    "q3_klinik_etik_karar",
    "q4_hukuki_guven",
    "q4_pratik_engel",
]

COMPOSITE_INDICATORS = [
    "hukuki_bilgi_dogru",
    "etik_esdegerlik",
    "withdraw_daha_agir",
    "riskten_kacinan_tedaviye_devam",
    "paylasimli_kurumsal_karar",
    "hukuki_guvensizlik",
    "hukuki_risk_ana_engel",
    "hukuki_prosedurel_cozum",
    "yasal_duzenleme_talebi",
    "dnr_protokol_talebi",
    "q6_C_etik_kurul_danismanlik",
    "q6_D_hekim_egitimi",
    "q6_E_palyatif_bakim",
    "q5a_yetkinlik_yuksek",
    "q5b_deger_etkisi_yuksek",
    "q5c_catismayi_dile_getirmede_gucluk_yuksek",
]


def main() -> None:
    df = pd.read_csv(DERIVED_SURVEY_CSV, encoding="utf-8")
    OUTPUT_TABLES.mkdir(parents=True, exist_ok=True)

    desc = summarize_categorical(df, CATEGORICAL_VARIABLES)
    composite = summarize_binary_indicators(df, COMPOSITE_INDICATORS)

    write_csv(desc, OUTPUT_TABLES / "descriptive_frequencies.csv")
    write_csv(composite, OUTPUT_TABLES / "composite_indicators.csv")
    print("Descriptive analysis completed.")


if __name__ == "__main__":
    main()

