# Data dictionary — revised ICU end-of-life survey

Version: 2026-11-19. Unit of observation: one physician response form. There are
28 rows, 27 raw columns and 25 additional derived columns (52 processed columns).
Turkish variable names and codes are preserved; descriptions below are in English.
`data_dictionary.csv` is the full machine-readable dictionary. This Markdown file
is a readable rendering of the same definitions. Regenerate both with
`python scripts/10_build_data_dictionary.py` after deriving the dataset.

## Reading and missing data

CSV files use UTF-8 (the writer includes a BOM). Semicolons occur inside some
values; the field delimiter is a comma. Blank fields are missing or unspecified,
depending on the field-specific rule; they are never a universal zero code.
Binary analytical indicators use 1/0, with missingness retained for clinical
items. Raw Q4 `1;3` is an ambiguous double marking, not a valid ordinal value;
primary security analyses exclude it. Q5b/Q5c each have one blank response.
Free-text blanks often mean no other response/note was supplied.

## Interpretation and coding limits

- Question 1 is one keyed legal-framework item, not a validated overall knowledge scale.
- Question 3 A combines legal risk and family pressure; it is hypothetical, not observed care.
- The B/D vignette grouping is not a validated shared decision-making score.
- High Q5c endorsement means greater difficulty expressing disagreement.
- Question 6 requested two priorities. Retained forms have one (16), two (11),
  or three (1) selections. Nonselection of education does not establish no need.
- The experience categories reproduce the printed form, including its boundary
  overlap (4–10 and 10+). Continuous experience cannot be recovered.
- Source scans/handwriting are excluded. PDF-page columns are provenance links,
  not links to publicly available completed forms.

## Fields

Raw variables occur unchanged in both datasets; derived variables occur only in
the processed dataset. Counts below describe this fixed 28-response snapshot.

### `katilimci_no`

Source-form participant code

- Origin/type: raw, copied unchanged to processed; integer.
- Source: Form page codes.
- Coding: Unique code: 1–22 and 24–29.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: The absent code 23 does not establish exclusion or a recruitment count.

### `pdf_sayfa_1`

Private source PDF page 1

- Origin/type: raw, copied unchanged to processed; integer.
- Source: Manual source-page linkage.
- Coding: Page in 1–84; position 1 of each three-page response form.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Provenance index only. Completed source scans are not distributed.

### `pdf_sayfa_2`

Private source PDF page 2

- Origin/type: raw, copied unchanged to processed; integer.
- Source: Manual source-page linkage.
- Coding: Page in 1–84; position 2 of each three-page response form.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Provenance index only. Completed source scans are not distributed.

### `pdf_sayfa_3`

Private source PDF page 3

- Origin/type: raw, copied unchanged to processed; integer.
- Source: Manual source-page linkage.
- Coding: Page in 1–84; position 3 of each three-page response form.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Provenance index only. Completed source scans are not distributed.

### `unvan`

Professional title

- Origin/type: raw, copied unchanged to processed; string.
- Source: Demographic item.
- Coding: Recorded selection.
- Values: `Asistan hekim` = Resident physician; `Uzman hekim` = Specialist physician; `Öğretim üyesi` = Faculty member.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.

### `birim`

Clinical field

- Origin/type: raw, copied unchanged to processed; string.
- Source: Demographic item.
- Coding: Recorded selection; semicolon separates joint selections.
- Values: `Yoğun bakım` = Intensive care; `Anesteziyoloji ve Reanimasyon` = Anesthesiology and reanimation; `Diğer` = Other; `Yoğun bakım;Anesteziyoloji ve Reanimasyon` = Both clinical fields.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.

### `birim_diger_metni`

Other clinical field text

- Origin/type: raw, copied unchanged to processed; string.
- Source: Demographic other field.
- Coding: Transcribed other-field label.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 3 nonmissing, 25 blank/missing.
- Note: Blank usually means no other field specified; not a missing clinical outcome.

### `mesleki_deneyim`

Professional experience category

- Origin/type: raw, copied unchanged to processed; string.
- Source: Demographic item.
- Coding: Recorded category; no continuous years available.
- Values: `0-3 yıl` = 0–3 years; `4-10 yıl` = 4–10 years; `10+ yıl` = 10+ years.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Source categories 4–10 and 10+ overlap at 10. Preserve recorded categories; do not infer exact years. Manuscript Table 1 should use 10+ years rather than >10 years.

### `onceki_yasam_sonu_kararda_aktif_rol`

Previous active role in an end-of-life treatment-limitation decision

- Origin/type: raw, copied unchanged to processed; string.
- Source: Demographic item.
- Coding: Recorded yes/no.
- Values: `Evet` = Yes; `Hayır` = No.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 27 nonmissing, 1 blank/missing.
- Note: One blank response (participant 9); valid denominator 27.

### `q1_hukuki_bilgi`

Single legal-framework item response

- Origin/type: raw, copied unchanged to processed; string.
- Source: Question 1.
- Coding: One response A–E; B is the keyed response.
- Values: `A` = Detailed national DNR/treatment-termination regulation exists; `B` = Euthanasia prohibited; patient may refuse; no explicit standard national DNR/end-of-life limitation regulation; `C` = Patient cannot refuse treatment; physician must continue; `D` = Withholding permitted but withdrawal prohibited; `E` = No opinion.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Questionnaire wording, not a legal opinion or a validated overall knowledge scale. See manuscript legal context and Supplement S1.

### `q2_withholding_withdrawing_ayrimi`

Perceived ethical difference between withholding and withdrawal

- Origin/type: raw, copied unchanged to processed; string.
- Source: Question 2.
- Coding: One response A–D.
- Values: `A` = Withdrawal ethically more serious; `B` = Withholding ethically more serious; `C` = Ethically equivalent; `D` = Undecided.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.

### `q3_klinik_etik_karar`

Hypothetical clinical-vignette preference

- Origin/type: raw, copied unchanged to processed; string.
- Source: Question 3.
- Coding: One response A–E.
- Values: `A` = Continue because of legal risk AND family pressure; `B` = Team decision on medical futility with communication and documentation; `C` = Leave decision entirely to family; `D` = Consult ethics or palliative care team; `E` = Undecided.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Hypothetical response only. A cannot distinguish legal from family motivation; B/D grouping is not validated shared decision-making.

### `q4_hukuki_guven`

Perceived legal security, original marking

- Origin/type: raw, copied unchanged to processed; string.
- Source: Question 4 security.
- Coding: Ordinal 1–5 stored as text; 1;3 retains the double marking.
- Values: `1` = No security; `2` = Little security; `3` = Undecided; `4` = Largely adequate; `5` = Completely adequate; `1;3` = Ambiguous double selection, not a valid ordinal category.
- Missing rule: Blank is missing; 1;3 is nonblank but analytically missing in primary security analyses.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Participant 13 marked both 1 and 3. Primary denominator 27; two sensitivity codings are supplied.

### `q4_pratik_engel`

Principal practical barrier

- Origin/type: raw, copied unchanged to processed; string.
- Source: Question 4 barrier.
- Coding: One response A–F.
- Values: `A` = Legal uncertainty and legal-risk concern; `B` = Family pressure and communication difficulty; `C` = Team disagreement; `D` = Missing institutional protocol/standard form; `E` = Religious/cultural pressure; `F` = Other.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Other/all is not A in the main analysis.

### `q4_pratik_engel_diger_metni`

Other barrier text

- Origin/type: raw, copied unchanged to processed; string.
- Source: Question 4 other.
- Coding: Transcribed other-barrier response.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 1 nonmissing, 27 blank/missing.
- Note: Participant 17: Hepsi (all); included with legal risk only in sensitivity analysis.

### `q5a_yasam_sonu_konusmasi_yetkinlik`

Self-rated end-of-life communication competence

- Origin/type: raw, copied unchanged to processed; number.
- Source: Question 5.
- Coding: Hasta/aile ile yaşam sonu konuşması yapmakta kendimi yetkin hissediyorum.
- Values: `1` = Strongly disagree; `2` = Disagree; `3` = Undecided; `4` = Agree; `5` = Strongly agree.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Higher endorsement means more of the stated construct. Q5c is difficulty, not communication ability. Q5a coding uncertainty is retained in coding_notes.txt.

### `q5b_dini_kulturel_degerler_etkisi`

Influence of religious/cultural values

- Origin/type: raw, copied unchanged to processed; number.
- Source: Question 5.
- Coding: Dini veya kültürel değerlerim yaşam sonu kararlarımı etkiliyor.
- Values: `1` = Strongly disagree; `2` = Disagree; `3` = Undecided; `4` = Agree; `5` = Strongly agree.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 27 nonmissing, 1 blank/missing.
- Note: Higher endorsement means more of the stated construct. Q5c is difficulty, not communication ability. Q5a coding uncertainty is retained in coding_notes.txt.

### `q5c_etik_gorus_catismasi_dile_getirme`

Difficulty voicing ethical disagreement

- Origin/type: raw, copied unchanged to processed; number.
- Source: Question 5.
- Coding: Ekip kararı kendi etik görüşümle çatıştığında bunu dile getirmekte güçlük çekiyorum.
- Values: `1` = Strongly disagree; `2` = Disagree; `3` = Undecided; `4` = Agree; `5` = Strongly agree.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 27 nonmissing, 1 blank/missing.
- Note: Higher endorsement means more of the stated construct. Q5c is difficulty, not communication ability. Q5a coding uncertainty is retained in coding_notes.txt.

### `q6_A_yasal_duzenleme`

Comprehensive legal regulation selected

- Origin/type: raw, copied unchanged to processed; integer.
- Source: Question 6 priorities.
- Coding: 1 if selected; 0 if not selected.
- Values: `0` = Not selected; `1` = Selected.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Two priorities requested; 16 forms selected one, 11 two, one three. Retain all markings in main analysis. Nonselection does not imply no need.

### `q6_B_yazili_protokol_DNR_formu`

Written protocols/standard DNR form selected

- Origin/type: raw, copied unchanged to processed; integer.
- Source: Question 6 priorities.
- Coding: 1 if selected; 0 if not selected.
- Values: `0` = Not selected; `1` = Selected.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Two priorities requested; 16 forms selected one, 11 two, one three. Retain all markings in main analysis. Nonselection does not imply no need.

### `q6_C_etik_kurul_danismanlik`

Ethics committee/consultation selected

- Origin/type: raw, copied unchanged to processed; integer.
- Source: Question 6 priorities.
- Coding: 1 if selected; 0 if not selected.
- Values: `0` = Not selected; `1` = Selected.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Two priorities requested; 16 forms selected one, 11 two, one three. Retain all markings in main analysis. Nonselection does not imply no need.

### `q6_D_hekim_egitimi`

Physician education selected

- Origin/type: raw, copied unchanged to processed; integer.
- Source: Question 6 priorities.
- Coding: 1 if selected; 0 if not selected.
- Values: `0` = Not selected; `1` = Selected.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Two priorities requested; 16 forms selected one, 11 two, one three. Retain all markings in main analysis. Nonselection does not imply no need.

### `q6_E_palyatif_bakim`

Stronger palliative care services selected

- Origin/type: raw, copied unchanged to processed; integer.
- Source: Question 6 priorities.
- Coding: 1 if selected; 0 if not selected.
- Values: `0` = Not selected; `1` = Selected.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Two priorities requested; 16 forms selected one, 11 two, one three. Retain all markings in main analysis. Nonselection does not imply no need.

### `q6_F_diger`

Other system solution selected

- Origin/type: raw, copied unchanged to processed; integer.
- Source: Question 6 priorities.
- Coding: 1 if selected; 0 if not selected.
- Values: `0` = Not selected; `1` = Selected.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Two priorities requested; 16 forms selected one, 11 two, one three. Retain all markings in main analysis. Nonselection does not imply no need.

### `q6_secimler`

Selected solution letters

- Origin/type: raw, copied unchanged to processed; string.
- Source: Question 6.
- Coding: Semicolon-delimited A–F; redundant representation of the six binary columns.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Not a single-choice categorical variable.

### `q6_diger_metni`

Other system-solution text

- Origin/type: raw, copied unchanged to processed; string.
- Source: Question 6 other.
- Coding: Transcribed other response if present.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 0 nonmissing, 28 blank/missing.
- Note: All 28 fields blank in this dataset; no other option was selected.

### `kodlama_notu`

Manual coding note

- Origin/type: raw, copied unchanged to processed; string.
- Source: Digitization quality control.
- Coding: De-identified coding/provenance comment.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 7 nonmissing, 21 blank/missing.
- Note: Blank means no specific note recorded; not an outcome.

### `q4_guven_clean`

Clean legal-security score

- Origin/type: derived; number.
- Source: q4_hukuki_guven.
- Coding: Numeric value if exactly one valid score 1–5; otherwise missing.
- Values: `1` = No security; `2` = Little security; `3` = Undecided; `4` = Largely adequate; `5` = Completely adequate.
- Missing rule: Blank CSV field is missing; no imputation.
- Observed: 27 nonmissing, 1 blank/missing.

### `hukuki_guvensizlik`

Low legal security

- Origin/type: derived; number.
- Source: q4_guven_clean.
- Coding: 1 for 1/2; 0 for 3/4/5.
- Values: `0` = Absent/not endorsed; `1` = Present/endorsed.
- Missing rule: Missing/ambiguous/invalid source remains missing; 0 means an interpretable non-endorsing response.
- Observed: 27 nonmissing, 1 blank/missing.
- Note: Primary security indicator; n=27.

### `hukuki_guvensizlik_sens`

Low security: double marking assigned 1

- Origin/type: derived; number.
- Source: hukuki_guvensizlik;q4_hukuki_guven.
- Coding: Copy primary indicator; assign 1 for documented 1;3 marking.
- Values: `0` = No; `1` = Yes.
- Missing rule: Other primary missing values remain missing.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Sensitivity only; does not replace the primary definition.

### `aktif_rol_var`

Previous active role

- Origin/type: derived; number.
- Source: onceki_yasam_sonu_kararda_aktif_rol.
- Coding: Evet→1; Hayır→0.
- Values: `0` = Absent/not endorsed; `1` = Present/endorsed.
- Missing rule: Missing/ambiguous/invalid source remains missing; 0 means an interpretable non-endorsing response.
- Observed: 27 nonmissing, 1 blank/missing.
- Note: n=27.

### `asistan`

Resident indicator

- Origin/type: derived; integer.
- Source: unvan.
- Coding: 1 if Asistan hekim; otherwise 0.
- Values: `0` = No; `1` = Yes.
- Missing rule: Current demographic sources are complete. Implementation evaluates other/blank entries as 0; not used as primary clinical missingness coding.
- Observed: 28 nonmissing, 0 blank/missing.

### `deneyim_10plus`

10+ experience category indicator

- Origin/type: derived; integer.
- Source: mesleki_deneyim.
- Coding: 1 if 10+ yıl; otherwise 0.
- Values: `0` = No; `1` = Yes.
- Missing rule: Current demographic sources are complete. Implementation evaluates other/blank entries as 0; not used as primary clinical missingness coding.
- Observed: 28 nonmissing, 0 blank/missing.

### `deneyim_0_3`

0–3 experience category indicator

- Origin/type: derived; integer.
- Source: mesleki_deneyim.
- Coding: 1 if 0-3 yıl; otherwise 0.
- Values: `0` = No; `1` = Yes.
- Missing rule: Current demographic sources are complete. Implementation evaluates other/blank entries as 0; not used as primary clinical missingness coding.
- Observed: 28 nonmissing, 0 blank/missing.

### `deneyim_4plus`

4+ experience categories indicator

- Origin/type: derived; integer.
- Source: mesleki_deneyim.
- Coding: 1 if 4-10 yıl or 10+ yıl; otherwise 0.
- Values: `0` = No; `1` = Yes.
- Missing rule: Current demographic sources are complete. Implementation evaluates other/blank entries as 0; not used as primary clinical missingness coding.
- Observed: 28 nonmissing, 0 blank/missing.

### `birim_anestezi`

Anesthesiology field indicator

- Origin/type: derived; integer.
- Source: birim.
- Coding: 1 if text contains Anesteziyoloji, including joint selection; otherwise 0.
- Values: `0` = No; `1` = Yes.
- Missing rule: Current demographic sources are complete. Implementation evaluates other/blank entries as 0; not used as primary clinical missingness coding.
- Observed: 28 nonmissing, 0 blank/missing.

### `hukuki_bilgi_dogru`

Keyed legal-item response

- Origin/type: derived; number.
- Source: q1_hukuki_bilgi.
- Coding: B→1; A/C/D/E→0.
- Values: `0` = Absent/not endorsed; `1` = Present/endorsed.
- Missing rule: Missing/ambiguous/invalid source remains missing; 0 means an interpretable non-endorsing response.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Legacy name means keyed response, not overall legal knowledge.

### `etik_esdegerlik`

Withholding/withdrawal ethically equivalent

- Origin/type: derived; number.
- Source: q2_withholding_withdrawing_ayrimi.
- Coding: C→1; A/B/D→0.
- Values: `0` = Absent/not endorsed; `1` = Present/endorsed.
- Missing rule: Missing/ambiguous/invalid source remains missing; 0 means an interpretable non-endorsing response.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Perceived ethical equivalence.

### `withdraw_daha_agir`

Withdrawal ethically more serious

- Origin/type: derived; number.
- Source: q2_withholding_withdrawing_ayrimi.
- Coding: A→1; B/C/D→0.
- Values: `0` = Absent/not endorsed; `1` = Present/endorsed.
- Missing rule: Missing/ambiguous/invalid source remains missing; 0 means an interpretable non-endorsing response.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Perception only.

### `riskten_kacinan_tedaviye_devam`

Vignette continuation citing legal risk and family pressure

- Origin/type: derived; number.
- Source: q3_klinik_etik_karar.
- Coding: A→1; B/C/D/E→0.
- Values: `0` = Absent/not endorsed; `1` = Present/endorsed.
- Missing rule: Missing/ambiguous/invalid source remains missing; 0 means an interpretable non-endorsing response.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Legacy name; do not interpret as measured defensive behaviour.

### `ekip_belgeleme_karari`

Vignette team/documentation response

- Origin/type: derived; number.
- Source: q3_klinik_etik_karar.
- Coding: B→1; A/C/D/E→0.
- Values: `0` = Absent/not endorsed; `1` = Present/endorsed.
- Missing rule: Missing/ambiguous/invalid source remains missing; 0 means an interpretable non-endorsing response.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Hypothetical preference.

### `etik_kurul_palyatif_yonelim`

Vignette ethics/palliative consultation response

- Origin/type: derived; number.
- Source: q3_klinik_etik_karar.
- Coding: D→1; A/B/C/E→0.
- Values: `0` = Absent/not endorsed; `1` = Present/endorsed.
- Missing rule: Missing/ambiguous/invalid source remains missing; 0 means an interpretable non-endorsing response.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Hypothetical preference.

### `paylasimli_kurumsal_karar`

Vignette B/D response grouping

- Origin/type: derived; number.
- Source: q3_klinik_etik_karar.
- Coding: B/D→1; A/C/E→0.
- Values: `0` = Absent/not endorsed; `1` = Present/endorsed.
- Missing rule: Missing/ambiguous/invalid source remains missing; 0 means an interpretable non-endorsing response.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Legacy name; analytic grouping, not a validated shared decision-making measure.

### `hukuki_risk_ana_engel`

Legal risk as principal barrier

- Origin/type: derived; number.
- Source: q4_pratik_engel.
- Coding: A→1; B/C/D/E/F→0.
- Values: `0` = Absent/not endorsed; `1` = Present/endorsed.
- Missing rule: Missing/ambiguous/invalid source remains missing; 0 means an interpretable non-endorsing response.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Other/all remains 0 in primary analysis.

### `yasal_duzenleme_talebi`

Legal regulation priority

- Origin/type: derived; number.
- Source: q6_A_yasal_duzenleme.
- Coding: Copy valid binary source.
- Values: `0` = Absent/not endorsed; `1` = Present/endorsed.
- Missing rule: Missing/ambiguous/invalid source remains missing; 0 means an interpretable non-endorsing response.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Priority, not an effectiveness measure.

### `dnr_protokol_talebi`

Written protocol/DNR-form priority

- Origin/type: derived; number.
- Source: q6_B_yazili_protokol_DNR_formu.
- Coding: Copy valid binary source.
- Values: `0` = Absent/not endorsed; `1` = Present/endorsed.
- Missing rule: Missing/ambiguous/invalid source remains missing; 0 means an interpretable non-endorsing response.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Priority, not an effectiveness measure.

### `hukuki_prosedurel_cozum`

Legal/procedural solution preference

- Origin/type: derived; number.
- Source: yasal_duzenleme_talebi;dnr_protokol_talebi.
- Coding: 1 if either indicator is 1; 0 if both 0; otherwise missing.
- Values: `0` = Absent/not endorsed; `1` = Present/endorsed.
- Missing rule: Missing/ambiguous/invalid source remains missing; 0 means an interpretable non-endorsing response.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Logical OR includes both selections, not a count or validated scale.

### `q5a_yetkinlik_yuksek`

High communication-competence endorsement

- Origin/type: derived; number.
- Source: q5a_yasam_sonu_konusmasi_yetkinlik.
- Coding: 4/5→1; 1/2/3→0.
- Values: `0` = Absent/not endorsed; `1` = Present/endorsed.
- Missing rule: Missing/ambiguous/invalid source remains missing; 0 means an interpretable non-endorsing response.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Self-rated competence.

### `q5b_deger_etkisi_yuksek`

High values-influence endorsement

- Origin/type: derived; number.
- Source: q5b_dini_kulturel_degerler_etkisi.
- Coding: 4/5→1; 1/2/3→0.
- Values: `0` = Absent/not endorsed; `1` = Present/endorsed.
- Missing rule: Missing/ambiguous/invalid source remains missing; 0 means an interpretable non-endorsing response.
- Observed: 27 nonmissing, 1 blank/missing.
- Note: One missing; n=27.

### `q5c_catismayi_dile_getirmede_gucluk_yuksek`

High difficulty voicing disagreement

- Origin/type: derived; number.
- Source: q5c_etik_gorus_catismasi_dile_getirme.
- Coding: 4/5→1; 1/2/3→0.
- Values: `0` = Absent/not endorsed; `1` = Present/endorsed.
- Missing rule: Missing/ambiguous/invalid source remains missing; 0 means an interpretable non-endorsing response.
- Observed: 27 nonmissing, 1 blank/missing.
- Note: One missing; n=27. Higher means greater difficulty.

### `hukuki_guvensizlik_sens_high`

Low security: double marking assigned 3

- Origin/type: derived; number.
- Source: hukuki_guvensizlik;q4_hukuki_guven.
- Coding: Copy primary indicator; assign 0 for documented 1;3 marking.
- Values: `0` = No; `1` = Yes.
- Missing rule: Other primary missing values remain missing.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Sensitivity only; does not replace the primary definition.

### `hukuki_risk_ana_engel_sens`

Legal barrier including other/all

- Origin/type: derived; number.
- Source: hukuki_risk_ana_engel;q4_pratik_engel_diger_metni.
- Coding: Copy primary indicator; assign 1 when stripped casefolded other text equals hepsi.
- Values: `0` = No; `1` = Yes.
- Missing rule: Other primary missing values remain missing.
- Observed: 28 nonmissing, 0 blank/missing.
- Note: Sensitivity only; does not replace the primary definition.
