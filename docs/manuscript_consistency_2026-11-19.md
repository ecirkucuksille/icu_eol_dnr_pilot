# Manuscript and analysis consistency — 19 November 2026

## Result and scope

The full revised pipeline completed successfully. All **26 numerical consistency
checks** and **8 automated tests** passed. Raw participant responses are unchanged.
A complete dictionary covers the 27 raw fields and 25 additional derived fields
(52 processed fields). The dictionary records response codes, derivations,
missing-value conventions, observed denominators and interpretation limits.

The checked documents are the revised manuscript
`ICU_Ethic_Makale_Renkli_Revizyon.docx` (version 1) and
`ICU_Ethic_Ek_Materyal.docx` (version 0), supplied on 18 November 2026. Their exact
SHA-256 fingerprints are retained in `manuscript_results_manifest.json` and the
machine-readable audit. Word files have not been edited in this update.

All numerical cells in manuscript Tables 1–3 and supplementary Tables S2–S4
were extracted from those documents and compared with regenerated data/results
at the precision used in the documents. Key narrative counts were also checked.
The audit does not assert that every prose statement is independently verified,
or that pending author-dependent study facts are complete.

| Checked item | Reproduced result |
| --- | --- |
| Responses / resident physicians | 28 / 21 (75.0%) |
| Keyed legal-framework response | 23/28 (82.1%) |
| Low security | 24/27 (88.9%) |
| Low security among keyed responses with valid security | 19/22 (86.4%) |
| Legal regulation / written protocol / both / either | 19/28 / 13/28 / 8/28 / 24/28 |
| Physician education priority | 0/28 |
| Main association | 22/22 vs 2/6; difference 66.7 percentage points |
| Main Fisher p / Holm p (nine tests) | 0.0007326007 / 0.0065934066 (reported 0.007) |
| Main conditional OR, exact 95% CI | infinity, 3.72–infinity |
| Low security association, Fisher p / Holm p | 0.049 / 0.340 |
| Prior active role / continuation, Fisher p / Holm p | 0.033 / 0.263 |
| Supplementary Firth M2 legal-risk coefficient | OR 43.31; profile 95% CI 3.43–5525.48; PLR p=0.003 |
| Q6 selections per form | one: 16; two: 11; three: 1 |
| Coding sensitivities | All four reported scenarios reproduce Table S4 |

## One wording correction for the author

Manuscript Table 1 currently labels the upper experience category **>10 years**.
The printed questionnaire and CSV use **10+ years** (`10+ yıl`). Replace the
Table 1 label with **10+ years**. The count (4/28), percentage (14.3%) and all
analyses are unchanged. The source categories 4–10 and 10+ overlap at 10; exact
continuous experience was not collected, so no boundary reassignment was made.

## Author facts that remain pending

The previous red author fields for recruitment, collection dates, ethics approval,
consent and the consistency of public data sharing with the approved arrangements
remain unresolved. Numerical consistency is not verification of those facts.
`08_check_submission_readiness.py` deliberately reports them separately; its
pending status is not a failure of the numerical analysis pipeline.

## Reproduce this verification

```bash
python scripts/06_run_all.py
python -m pytest -q
```

See `outputs/logs/manuscript_consistency.json` for all 26 checks and document/data
fingerprints, and `data/metadata/data_dictionary.md` or `.csv` for field definitions.
Historical `outputs/legacy_pre_revision/` files are not current manuscript results.
The prepared GitHub update includes the 18 November analysis corrections as well as this
19 November dictionary/consistency update, because the remote main branch was
still at source commit `c4946ab57f47dd80444a0380b5f03cc39fd26678` when checked.

## Publication boundary

No participant-level records are uploaded in this update. The existing upstream raw CSV remains byte-for-byte unchanged. The outdated processed CSV is removed from tracking; the corrected 52-field dataset is generated locally by the pipeline and excluded from Git. The dictionary documents that generated schema. This avoids publishing a new participant-level snapshot while approval/consent metadata remain unverified.

## GitHub publication scope

Initial publication attempts failed with HTTP 403. A subsequent authorized retry restored write access. This revision publishes the dictionary, corrected scripts, aggregate result tables/figures and consistency checks. It uploads no new participant-level records. The existing upstream raw CSV remains unchanged; the corrected processed dataset is regenerated locally and excluded from version control. The availability paragraph in `data_and_analysis_code_availability.md` describes the resulting repository contents.
