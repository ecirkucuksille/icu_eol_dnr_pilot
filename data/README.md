# Data files

One row represents one physician response form (28 respondents).

- `raw/survey_responses_deidentified.csv`: manually digitized, de-identified responses; 27 columns. Preserved unchanged from the upstream source.
- `processed/survey_responses_derived.csv`: generated locally, excluded from Git; all 27 raw columns plus 25 reproducibly derived variables (52 columns).
- **`metadata/data_dictionary.md`**: complete readable dictionary for all 52 fields.
- **`metadata/data_dictionary.csv`**: machine-readable version, including source fields, valid codes, derivations, missing-value rules and observed counts.
- `metadata/codebook.csv`: retained original Turkish option codebook; not a complete description of derived fields.
- `metadata/coding_notes.txt`: retained manual coding notes.

The comma-delimited CSV files are UTF-8; a BOM may be present. Semicolons inside
cells denote multiple source markings or selections. Blank clinical values remain
missing rather than zero. In particular, Q4 `1;3` becomes missing in the main
security indicator. Free-text blanks may mean no other response or note.

Generate the processed dataset and dictionary with the full pipeline:
`python scripts/06_run_all.py`. For metadata-only regeneration after data derivation,
run `python scripts/10_build_data_dictionary.py`.

Scanned completed forms and handwriting are excluded. Private PDF page indices
provide provenance only. They do not make source scans publicly available.
