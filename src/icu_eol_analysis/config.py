"""Project-level path configuration.

All scripts import these paths so the repository can be moved without
changing hard-coded file locations.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_METADATA = PROJECT_ROOT / "data" / "metadata"
OUTPUT_TABLES = PROJECT_ROOT / "outputs" / "tables"
OUTPUT_FIGURES = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_LOGS = PROJECT_ROOT / "outputs" / "logs"

RAW_SURVEY_CSV = DATA_RAW / "survey_responses_deidentified.csv"
DERIVED_SURVEY_CSV = DATA_PROCESSED / "survey_responses_derived.csv"

REQUIRED_RAW_COLUMNS = [
    "katilimci_no", "pdf_sayfa_1", "pdf_sayfa_2", "pdf_sayfa_3",
    "unvan", "birim", "mesleki_deneyim",
    "onceki_yasam_sonu_kararda_aktif_rol",
    "q1_hukuki_bilgi", "q2_withholding_withdrawing_ayrimi",
    "q3_klinik_etik_karar", "q4_hukuki_guven", "q4_pratik_engel",
    "q5a_yasam_sonu_konusmasi_yetkinlik",
    "q5b_dini_kulturel_degerler_etkisi",
    "q5c_etik_gorus_catismasi_dile_getirme",
    "q6_A_yasal_duzenleme", "q6_B_yazili_protokol_DNR_formu",
    "q6_C_etik_kurul_danismanlik", "q6_D_hekim_egitimi",
    "q6_E_palyatif_bakim", "q6_F_diger",
]
