# ICU End-of-Life and DNR Exploratory Survey Analysis

Data, analysis code and metadata accompanying **End-of-Life Decisions in Intensive
Care at a University Hospital: An Evaluation of Physicians’ Approaches**.
This is a single-centre exploratory cross-sectional survey of 28 physicians.
The historical repository name includes `pilot`; this does not imply a verified,
prespecified feasibility-study design. One legal-framework item is not a validated
measure of overall legal knowledge, and vignette responses are hypothetical.

Repository: https://github.com/ecirkucuksille/icu_eol_dnr_pilot

## Data and dictionary

- [Raw responses](data/raw/survey_responses_deidentified.csv): 28 rows × 27 columns.
- Processed responses: `data/processed/survey_responses_derived.csv` is generated locally; 28 rows × 52 columns (raw fields plus 25 derived fields). It is excluded from Git.
- **[Data dictionary](data/metadata/data_dictionary.md)**: readable descriptions of every raw and derived variable, response codes, derivation rules, missing values, denominators and interpretation limits.
- [Machine-readable dictionary](data/metadata/data_dictionary.csv): one row per processed-data column; includes dataset paths, source fields and observed missing counts.
- [Original response-option codebook](data/metadata/codebook.csv): retained Turkish option wording; the complete current dictionary above also covers derived fields.
- [Coding notes](data/metadata/coding_notes.txt): digitization ambiguities and unusual markings.

The pre-revision processed snapshot is removed from version control; run the pipeline to regenerate the corrected version locally. This update does not upload any participant-level records. Existing upstream raw data are left unchanged.

Completed source questionnaires, scans and handwriting are excluded. The tabular
data have no direct personal identifiers. Public availability is not evidence of
an ethics/consent determination; author-dependent approval, consent, recruitment
and collection-date facts remain pending in
[study reporting metadata](docs/study_reporting_metadata.json).

## Reproduce the revised analyses

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/06_run_all.py
python -m pytest -q
```

The pipeline validates the source data, derives variables, generates descriptive
and inferential tables and three PNG figures, rebuilds both dictionary formats,
and checks numerical agreement with the revised manuscript and supplement.

| Step | Script | Purpose |
| --- | --- | --- |
| 1 | `01_validate_data.py` | Source schema, count, numbering and private PDF-page linkage |
| 2 | `02_derive_variables.py` | Main indicators and explicit sensitivity scenarios |
| 3 | `03_descriptive_analysis.py` | Frequencies and Wilson 95% intervals |
| 4 | `04_inferential_analysis.py` | Nine Fisher tests with Holm correction, conditional ORs, supplementary profile Firth models and sensitivities |
| 5 | `05_make_figures.py` | Figures 1–3 |
| 6 | `07_revision_audit.py` | Raw-data checksum, denominators and numerical convergence |
| 7 | `10_build_data_dictionary.py` | Complete CSV and Markdown dictionary |
| 8 | `09_verify_manuscript_consistency.py` | Six main/supplementary result tables and key narrative counts |

`06_run_all.py` orchestrates these steps. Script numbering reflects when a check
was added; dictionary generation runs before its consistency check.

Check author-dependent submission metadata separately:

```bash
python scripts/08_check_submission_readiness.py
```

That command deliberately returns a nonzero exit code while required study facts
are unverified. Passing analysis checks does not mean those facts are complete.

## Manuscript alignment

[Consistency report](docs/manuscript_consistency_2026-11-19.md) and
[machine-readable results](outputs/logs/manuscript_consistency.json) document the
checked Word versions, source checksums and scope. All numeric cells in Tables
1–3 and S2–S4 are compared with a fixed manifest extracted from the checked Word
files; the actual Word files are not distributed here.

The main comparison is 22/22 versus 2/6, Fisher p=0.0007326 and Holm-adjusted
p=0.0065934 (reported as 0.007). Conditional OR is infinite, with exact 95% CI
3.72–infinity. Supplementary Firth M2 gives OR 43.31, profile 95% CI
3.43–5525.48 and PLR p=0.003. These are exploratory associations and cannot
establish causal or independent effects.

One label correction remains for the author: manuscript Table 1 should show
**10+ years**, matching the source form and CSV, instead of **>10 years**.
Counts and analyses are unaffected. The source categories 4–10 and 10+ overlap
at 10; the dictionary preserves that limitation.

## Outputs and interpretation

Current tables are under `outputs/tables/`; figures under `outputs/figures/`.
Older cross-tabulations and Spearman summaries are retained only in
`outputs/legacy_pre_revision/`, explicitly excluded from current manuscript
results. Wald approximations in the Firth CSV are diagnostic columns; the
manuscript uses profile penalized-likelihood intervals and PLR p-values.

The revised security denominator is 27 because one 1/3 double marking is missing
in the main analysis. Missing Q5b/Q5c remain missing, and high Q5c endorsement
means more difficulty voicing disagreement. Q6 requested two priorities; all
marked options are retained, with an explicit sensitivity for the three-selection
form. See the dictionary and [methodological notes](docs/methodological_notes.md).

## Citation and reuse

`CITATION.cff` provides software citation metadata, version 0.2.0. An article DOI
has not been supplied and is not invented. The code licence and data reuse terms
remain unspecified in `LICENSE_TO_BE_SELECTED.md`; public access does not itself
grant a new licence. This revision does not change those terms.

See [18 November revision log](docs/revision_changes_2026-11-18.md) for the
statistical corrections and [19 November consistency report](docs/manuscript_consistency_2026-11-19.md)
for the dictionary and manuscript alignment verification.
