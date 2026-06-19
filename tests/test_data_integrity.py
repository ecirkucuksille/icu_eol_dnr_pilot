"""Basic integrity tests for the de-identified pilot survey dataset."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_participant_count_and_numbering():
    df = pd.read_csv(ROOT / "data/raw/survey_responses_deidentified.csv")
    assert len(df) == 28
    assert 23 not in set(df["katilimci_no"])


def test_pdf_pages_cover_84_pages_once():
    df = pd.read_csv(ROOT / "data/raw/survey_responses_deidentified.csv")
    pages = df[["pdf_sayfa_1", "pdf_sayfa_2", "pdf_sayfa_3"]].values.flatten().tolist()
    assert min(pages) == 1
    assert max(pages) == 84
    assert len(set(pages)) == 84
