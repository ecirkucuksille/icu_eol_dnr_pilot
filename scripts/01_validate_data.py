from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
from icu_eol_analysis.config import RAW_SURVEY_CSV, REQUIRED_RAW_COLUMNS, OUTPUT_LOGS


def main() -> None:
    df = pd.read_csv(RAW_SURVEY_CSV, encoding="utf-8")
    missing = [c for c in REQUIRED_RAW_COLUMNS if c not in df.columns]
    errors = []
    if missing:
        errors.append(f"Missing required columns: {missing}")

    participant_numbers = df["katilimci_no"].tolist()
    if len(df) != 28:
        errors.append(f"Expected 28 participants, found {len(df)}")
    if 23 in participant_numbers:
        errors.append("Participant number 23 should not exist because the source form jumps from 22 to 24.")

    # Each participant should have three page references.
    page_cols = ["pdf_sayfa_1", "pdf_sayfa_2", "pdf_sayfa_3"]
    pages = df[page_cols].values.flatten().tolist()
    if len(set(pages)) != len(pages):
        errors.append("Duplicate PDF page references detected.")
    if min(pages) != 1 or max(pages) != 84:
        errors.append(f"Expected page range 1-84, observed {min(pages)}-{max(pages)}.")

    OUTPUT_LOGS.mkdir(parents=True, exist_ok=True)
    report_path = OUTPUT_LOGS / "validation_report.txt"
    if errors:
        report = "DATA VALIDATION FAILED\n" + "\n".join(f"- {e}" for e in errors)
        report_path.write_text(report, encoding="utf-8")
        raise SystemExit(report)

    report = (
        "DATA VALIDATION PASSED\n"
        f"Participants: {len(df)}\n"
        f"Participant IDs: {participant_numbers}\n"
        f"PDF page range: {min(pages)}-{max(pages)}\n"
        "Note: Participant ID 23 is intentionally absent in line with the source form numbering.\n"
    )
    report_path.write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
