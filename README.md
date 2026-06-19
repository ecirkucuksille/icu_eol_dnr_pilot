# ICU End-of-Life and DNR Pilot Survey Analysis

This repository contains the de-identified dataset, analysis scripts, tables, and figures for a pilot cross-sectional study on physicians' legal knowledge, legal confidence, ethical attitudes, and procedural solution expectations regarding end-of-life decisions and do-not-resuscitate (DNR) decisions in intensive care practice.

## Repository purpose

The repository is prepared for transparent peer review and manuscript citation. It allows reviewers and readers to inspect how the survey responses were converted into analysis variables and how the reported descriptive, Fisher exact, and exploratory Firth logistic regression results were generated.

## Folder structure

```text
.
├── data/
│   ├── raw/                         # De-identified manually digitized survey data
│   ├── processed/                   # Analysis-ready derived dataset
│   └── metadata/                    # Codebook and coding notes
├── docs/                            # Methodological notes
├── outputs/
│   ├── tables/                      # Reproducible CSV result tables
│   ├── figures/                     # Manuscript-ready figures
│   └── logs/                        # Validation reports
├── scripts/                         # Reproducible analysis pipeline
├── src/icu_eol_analysis/            # Reusable helper functions
└── tests/                           # Basic data-integrity tests
```

## Data files

- `data/raw/survey_responses_deidentified.csv`: de-identified manually digitized survey responses.
- `data/processed/survey_responses_derived.csv`: derived analysis dataset generated from the raw CSV.
- `data/metadata/codebook.csv`: variable descriptions and coding information.
- `data/metadata/coding_notes.txt`: notes retained from the manual coding process.

The scanned source forms are not included in this repository because they may contain handwritten notes or contextual information that should not be redistributed publicly.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/06_run_all.py
```

Expected main outputs:

- `outputs/tables/descriptive_frequencies.csv`
- `outputs/tables/composite_indicators.csv`
- `outputs/tables/fisher_exact_tests.csv`
- `outputs/tables/firth_logistic_models.csv`
- `outputs/figures/figure1_composite_indicators.png`
- `outputs/figures/figure2_solution_preferences.png`
- `outputs/figures/figure3_legal_risk_solution_demand.png`

## Analysis pipeline

1. `01_validate_data.py` checks required columns, participant count, participant numbering, and PDF page coverage.
2. `02_derive_variables.py` creates binary and composite indicators used in the manuscript.
3. `03_descriptive_analysis.py` generates frequency tables and Wilson 95% confidence intervals.
4. `04_inferential_analysis.py` runs Fisher exact tests and exploratory Firth penalized logistic regression models.
5. `05_make_figures.py` creates manuscript-ready PNG figures.
6. `06_run_all.py` runs the complete pipeline.

## Methodological notes

This is a pilot cross-sectional survey with 28 participants. The analyses are therefore exploratory and hypothesis-generating. Fisher exact tests are used for small-sample categorical comparisons, and Firth penalized logistic regression is used to reduce instability associated with sparse cells and separation in small logistic models.

## Suggested citation

Please update `CITATION.cff` with the final author list, article title, journal information, DOI, and repository DOI before public release.

## License

The code license and data reuse terms should be confirmed by the research team before public release. A placeholder license file is included for this reason.
