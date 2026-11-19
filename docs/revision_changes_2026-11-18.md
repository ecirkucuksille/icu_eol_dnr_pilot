# Peer-review revisions 18 November 2026

The working source texts were obtained from upstream commit
`c4946ab57f47dd80444a0380b5f03cc39fd26678`. The supplied local project folder
was empty, so a separate working copy was created in the task workspace.
The original raw response CSV was not edited.

## Analyses and reporting

- Replaced the mixture of sample ORs and Haldane–Anscombe confidence intervals
  with conditional maximum-likelihood ORs and exact equal-tailed conditional
  intervals. Zero and infinite boundaries are retained.
- Retained probability-ordered two-sided Fisher tests and documented that their
  tail convention differs from the equal-tailed confidence interval convention.
- Reported all nine exploratory tests and Holm adjustment across that family.
- Kept the original Firth point estimates, but implemented constrained full-model
  profile penalized-likelihood intervals and penalized LR tests. The full design
  determinant is used even when a coefficient is fixed. Models are supplementary.
- Preserved missing responses in all relevant derived questionnaire indicators.
  Previously, missing Q5b/Q5c responses were incorrectly converted to zero.
- Corrected the interpretation of Q5c: agreement means difficulty voicing an
  ethical disagreement, not competence in expressing disagreement.
- Added explicit coding sensitivities for the Q4 1/3 double marking, the
  other/all barrier, and the form with three solution selections.
- Retained each marked solution option in the main analysis; the original item
  asked for two priorities, and this instruction now frames interpretation.
- Regenerated all three figures; Figure 1 intervals contrast against the bars
  and denominators are visible, and Figure 3 displays group sizes and counts.

## Main results

The main comparison remains 22/22 versus 2/6, a 66.7 percentage-point difference.
Two-sided Fisher p=0.0007326007; Holm p=0.0065934066 (0.007 at three decimals).
Conditional OR=infinity, exact 95% CI 3.723866 to infinity.

The low-security comparison has nominal p=0.048547 (0.049), Holm p=0.339829,
and is sensitive to assigning the double marking to category 1 or 3.
The correct-item/low-security paired count is 19/22. Individual solution
preferences are regulation 19/28, protocol 13/28, both 8/28, either 24/28;
education 0/28.

The supplementary M2 Firth risk coefficient has OR=43.307944, profile 95% CI
3.430115–5525.483458 and penalized LR p=0.002617. Its breadth is a limitation,
not independent confirmatory evidence.

## Source instrument

The printed questionnaire text was checked against the retained 84-page source
scan. The clinical vignette's option A explicitly contains both legal risk and
family pressure. Its selection is a hypothetical preference, not observed care.
The unmarked items and coding rules are in supplementary Word material.
No source scans or participant handwriting were copied into this repository.

## Remaining author-dependent reporting fields

Data-collection dates, actual sampling/eligibility and invitation process,
invited/eligible counts, official ethics approval and actual consent procedure
must be supplied and verified. The old manuscript's bracketed ethics details
are not treated as verified. The revised documents visibly flag these gaps.
No claim that these reviewer requests have been completed should be sent until
the source records are checked. See `study_reporting_metadata.json`.

## Reproduction and verification

Run `python scripts/06_run_all.py` and `python -m pytest -q`.
The pipeline writes `outputs/logs/revision_audit.json` and all result CSVs.
Six tests cover raw-data structure, exact boundaries, missing-response coding,
primary denominators and the closed-form saturated Firth solution. Profile
endpoints are checked against the requested likelihood-ratio threshold.
`python scripts/08_check_submission_readiness.py` checks author-dependent fields;
it is expected to fail while reporting metadata are unfilled.

The repository visibility was public when inspected, whereas the original README
described a future public release. The revised availability wording reflects the
observed public repository. This local revision does not publish changes remotely.
