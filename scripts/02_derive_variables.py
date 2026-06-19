from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np
import pandas as pd
from icu_eol_analysis.config import RAW_SURVEY_CSV, DERIVED_SURVEY_CSV
from icu_eol_analysis.io import write_csv


def yes_no_to_binary(series: pd.Series) -> pd.Series:
    return series.map({"Evet": 1, "Hayır": 0})


def main() -> None:
    df = pd.read_csv(RAW_SURVEY_CSV, encoding="utf-8")

    # Legal confidence is originally coded on a 1-5 scale.
    df["q4_guven_clean"] = pd.to_numeric(df["q4_hukuki_guven"], errors="coerce")

    # Main derived indicators used in the manuscript.
    df["hukuki_guvensizlik"] = np.where(df["q4_guven_clean"].isin([1, 2]), 1,
                                  np.where(df["q4_guven_clean"].notna(), 0, np.nan))
    df["hukuki_guvensizlik_sens"] = df["hukuki_guvensizlik"]
    df["hukuki_bilgi_dogru"] = (df["q1_hukuki_bilgi"] == "B").astype(int)
    df["etik_esdegerlik"] = (df["q2_withholding_withdrawing_ayrimi"] == "C").astype(int)
    df["withdraw_daha_agir"] = (df["q2_withholding_withdrawing_ayrimi"] == "A").astype(int)
    df["riskten_kacinan_tedaviye_devam"] = (df["q3_klinik_etik_karar"] == "A").astype(int)
    df["ekip_belgeleme_karari"] = (df["q3_klinik_etik_karar"] == "B").astype(int)
    df["etik_kurul_palyatif_yonelim"] = (df["q3_klinik_etik_karar"] == "D").astype(int)
    df["paylasimli_kurumsal_karar"] = df["q3_klinik_etik_karar"].isin(["B", "D"]).astype(int)
    df["hukuki_risk_ana_engel"] = (df["q4_pratik_engel"] == "A").astype(int)
    df["hukuki_risk_ana_engel_sens"] = df["hukuki_risk_ana_engel"]
    df["hukuki_prosedurel_cozum"] = ((df["q6_A_yasal_duzenleme"] == 1) |
                                       (df["q6_B_yazili_protokol_DNR_formu"] == 1)).astype(int)
    df["yasal_duzenleme_talebi"] = (df["q6_A_yasal_duzenleme"] == 1).astype(int)
    df["dnr_protokol_talebi"] = (df["q6_B_yazili_protokol_DNR_formu"] == 1).astype(int)
    df["aktif_rol_var"] = yes_no_to_binary(df["onceki_yasam_sonu_kararda_aktif_rol"])
    df["asistan"] = (df["unvan"] == "Asistan hekim").astype(int)
    df["deneyim_10plus"] = (df["mesleki_deneyim"] == "10+ yıl").astype(int)
    df["deneyim_0_3"] = (df["mesleki_deneyim"] == "0-3 yıl").astype(int)
    df["deneyim_4plus"] = df["mesleki_deneyim"].isin(["4-10 yıl", "10+ yıl"]).astype(int)
    df["birim_anestezi"] = df["birim"].fillna("").str.contains("Anesteziyoloji", case=False, regex=False).astype(int)
    df["q5a_yetkinlik_yuksek"] = (pd.to_numeric(df["q5a_yasam_sonu_konusmasi_yetkinlik"], errors="coerce") >= 4).astype(int)
    df["q5b_deger_etkisi_yuksek"] = (pd.to_numeric(df["q5b_dini_kulturel_degerler_etkisi"], errors="coerce") >= 4).astype(int)
    df["q5c_catismayi_dile_getirme_yuksek"] = (pd.to_numeric(df["q5c_etik_gorus_catismasi_dile_getirme"], errors="coerce") >= 4).astype(int)

    write_csv(df, DERIVED_SURVEY_CSV)
    print(f"Derived dataset written to: {DERIVED_SURVEY_CSV}")


if __name__ == "__main__":
    main()
