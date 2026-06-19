from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
from icu_eol_analysis.config import DERIVED_SURVEY_CSV, OUTPUT_TABLES, OUTPUT_FIGURES
from icu_eol_analysis.plots import (
    save_composite_indicator_figure,
    save_solution_preferences_figure,
    save_legal_risk_solution_figure,
)


def main() -> None:
    derived = pd.read_csv(DERIVED_SURVEY_CSV, encoding="utf-8")
    composite = pd.read_csv(OUTPUT_TABLES / "composite_indicators.csv", encoding="utf-8")
    OUTPUT_FIGURES.mkdir(parents=True, exist_ok=True)

    save_composite_indicator_figure(composite, OUTPUT_FIGURES / "figure1_composite_indicators.png")
    save_solution_preferences_figure(derived, OUTPUT_FIGURES / "figure2_solution_preferences.png")
    save_legal_risk_solution_figure(derived, OUTPUT_FIGURES / "figure3_legal_risk_solution_demand.png")

    print("Figures generated.")


if __name__ == "__main__":
    main()
