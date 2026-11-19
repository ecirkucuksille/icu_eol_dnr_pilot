"""Build a complete field dictionary; retain Turkish CSV names and source codes."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / 'data/metadata'
RAW = 'data/raw/survey_responses_deidentified.csv'
DERIVED = 'data/processed/survey_responses_derived.csv'
SPECS = {}


def add(name, label, kind, source, rule, codes=None, missing='Blank CSV field is missing; no imputation.', note=''):
    SPECS[name] = dict(variable=name, label_en=label, storage_type=kind,
                       source=source, coding_or_derivation=rule,
                       value_labels_json=json.dumps(codes or {}, ensure_ascii=False),
                       missing_value_rule=missing, interpretation_note=note)


add('katilimci_no', 'Source-form participant code', 'integer', 'Form page codes',
    'Unique code: 1–22 and 24–29.', note='The absent code 23 does not establish exclusion or a recruitment count.')
for i in range(1, 4):
    add(f'pdf_sayfa_{i}', f'Private source PDF page {i}', 'integer', 'Manual source-page linkage',
        f'Page in 1–84; position {i} of each three-page response form.',
        note='Provenance index only. Completed source scans are not distributed.')
add('unvan', 'Professional title', 'string', 'Demographic item', 'Recorded selection.',
    {'Asistan hekim':'Resident physician','Uzman hekim':'Specialist physician','Öğretim üyesi':'Faculty member'})
add('birim', 'Clinical field', 'string', 'Demographic item', 'Recorded selection; semicolon separates joint selections.',
    {'Yoğun bakım':'Intensive care','Anesteziyoloji ve Reanimasyon':'Anesthesiology and reanimation',
     'Diğer':'Other','Yoğun bakım;Anesteziyoloji ve Reanimasyon':'Both clinical fields'})
add('birim_diger_metni', 'Other clinical field text', 'string', 'Demographic other field', 'Transcribed other-field label.',
    note='Blank usually means no other field specified; not a missing clinical outcome.')
add('mesleki_deneyim', 'Professional experience category', 'string', 'Demographic item', 'Recorded category; no continuous years available.',
    {'0-3 yıl':'0–3 years','4-10 yıl':'4–10 years','10+ yıl':'10+ years'},
    note='Source categories 4–10 and 10+ overlap at 10. Preserve recorded categories; do not infer exact years. Manuscript Table 1 should use 10+ years rather than >10 years.')
add('onceki_yasam_sonu_kararda_aktif_rol', 'Previous active role in an end-of-life treatment-limitation decision',
    'string', 'Demographic item', 'Recorded yes/no.', {'Evet':'Yes','Hayır':'No'},
    note='One blank response (participant 9); valid denominator 27.')
add('q1_hukuki_bilgi', 'Single legal-framework item response', 'string', 'Question 1', 'One response A–E; B is the keyed response.',
    {'A':'Detailed national DNR/treatment-termination regulation exists',
     'B':'Euthanasia prohibited; patient may refuse; no explicit standard national DNR/end-of-life limitation regulation',
     'C':'Patient cannot refuse treatment; physician must continue',
     'D':'Withholding permitted but withdrawal prohibited','E':'No opinion'},
    note='Questionnaire wording, not a legal opinion or a validated overall knowledge scale. See manuscript legal context and Supplement S1.')
add('q2_withholding_withdrawing_ayrimi', 'Perceived ethical difference between withholding and withdrawal',
    'string', 'Question 2', 'One response A–D.',
    {'A':'Withdrawal ethically more serious','B':'Withholding ethically more serious','C':'Ethically equivalent','D':'Undecided'})
add('q3_klinik_etik_karar', 'Hypothetical clinical-vignette preference', 'string', 'Question 3', 'One response A–E.',
    {'A':'Continue because of legal risk AND family pressure',
     'B':'Team decision on medical futility with communication and documentation',
     'C':'Leave decision entirely to family','D':'Consult ethics or palliative care team','E':'Undecided'},
    note='Hypothetical response only. A cannot distinguish legal from family motivation; B/D grouping is not validated shared decision-making.')
SECURITY = {'1':'No security','2':'Little security','3':'Undecided','4':'Largely adequate','5':'Completely adequate'}
add('q4_hukuki_guven', 'Perceived legal security, original marking', 'string', 'Question 4 security',
    'Ordinal 1–5 stored as text; 1;3 retains the double marking.',
    {**SECURITY,'1;3':'Ambiguous double selection, not a valid ordinal category'},
    missing='Blank is missing; 1;3 is nonblank but analytically missing in primary security analyses.',
    note='Participant 13 marked both 1 and 3. Primary denominator 27; two sensitivity codings are supplied.')
add('q4_pratik_engel', 'Principal practical barrier', 'string', 'Question 4 barrier', 'One response A–F.',
    {'A':'Legal uncertainty and legal-risk concern','B':'Family pressure and communication difficulty',
     'C':'Team disagreement','D':'Missing institutional protocol/standard form',
     'E':'Religious/cultural pressure','F':'Other'}, note='Other/all is not A in the main analysis.')
add('q4_pratik_engel_diger_metni', 'Other barrier text', 'string', 'Question 4 other', 'Transcribed other-barrier response.',
    note='Participant 17: Hepsi (all); included with legal risk only in sensitivity analysis.')
LIKERT = {'1':'Strongly disagree','2':'Disagree','3':'Undecided','4':'Agree','5':'Strongly agree'}
for name, label, statement in [
    ('q5a_yasam_sonu_konusmasi_yetkinlik', 'Self-rated end-of-life communication competence', 'Hasta/aile ile yaşam sonu konuşması yapmakta kendimi yetkin hissediyorum.'),
    ('q5b_dini_kulturel_degerler_etkisi', 'Influence of religious/cultural values', 'Dini veya kültürel değerlerim yaşam sonu kararlarımı etkiliyor.'),
    ('q5c_etik_gorus_catismasi_dile_getirme', 'Difficulty voicing ethical disagreement', 'Ekip kararı kendi etik görüşümle çatıştığında bunu dile getirmekte güçlük çekiyorum.'),
]:
    add(name, label, 'number', 'Question 5', statement, LIKERT,
        note='Higher endorsement means more of the stated construct. Q5c is difficulty, not communication ability. Q5a coding uncertainty is retained in coding_notes.txt.')
for suffix, label in [
    ('A_yasal_duzenleme','Comprehensive legal regulation'),
    ('B_yazili_protokol_DNR_formu','Written protocols/standard DNR form'),
    ('C_etik_kurul_danismanlik','Ethics committee/consultation'),
    ('D_hekim_egitimi','Physician education'),
    ('E_palyatif_bakim','Stronger palliative care services'),
    ('F_diger','Other system solution'),
]:
    add('q6_'+suffix, label+' selected', 'integer', 'Question 6 priorities',
        '1 if selected; 0 if not selected.', {'0':'Not selected','1':'Selected'},
        note='Two priorities requested; 16 forms selected one, 11 two, one three. Retain all markings in main analysis. Nonselection does not imply no need.')
add('q6_secimler', 'Selected solution letters', 'string', 'Question 6',
    'Semicolon-delimited A–F; redundant representation of the six binary columns.',
    note='Not a single-choice categorical variable.')
add('q6_diger_metni', 'Other system-solution text', 'string', 'Question 6 other', 'Transcribed other response if present.',
    note='All 28 fields blank in this dataset; no other option was selected.')
add('kodlama_notu', 'Manual coding note', 'string', 'Digitization quality control', 'De-identified coding/provenance comment.',
    note='Blank means no specific note recorded; not an outcome.')

add('q4_guven_clean', 'Clean legal-security score', 'number', 'q4_hukuki_guven',
    'Numeric value if exactly one valid score 1–5; otherwise missing.', SECURITY)
binary_missing = 'Missing/ambiguous/invalid source remains missing; 0 means an interpretable non-endorsing response.'
for name, label, source, rule, note in [
    ('hukuki_guvensizlik','Low legal security','q4_guven_clean','1 for 1/2; 0 for 3/4/5.','Primary security indicator; n=27.'),
    ('aktif_rol_var','Previous active role','onceki_yasam_sonu_kararda_aktif_rol','Evet→1; Hayır→0.','n=27.'),
    ('hukuki_bilgi_dogru','Keyed legal-item response','q1_hukuki_bilgi','B→1; A/C/D/E→0.','Legacy name means keyed response, not overall legal knowledge.'),
    ('etik_esdegerlik','Withholding/withdrawal ethically equivalent','q2_withholding_withdrawing_ayrimi','C→1; A/B/D→0.','Perceived ethical equivalence.'),
    ('withdraw_daha_agir','Withdrawal ethically more serious','q2_withholding_withdrawing_ayrimi','A→1; B/C/D→0.','Perception only.'),
    ('riskten_kacinan_tedaviye_devam','Vignette continuation citing legal risk and family pressure','q3_klinik_etik_karar','A→1; B/C/D/E→0.','Legacy name; do not interpret as measured defensive behaviour.'),
    ('ekip_belgeleme_karari','Vignette team/documentation response','q3_klinik_etik_karar','B→1; A/C/D/E→0.','Hypothetical preference.'),
    ('etik_kurul_palyatif_yonelim','Vignette ethics/palliative consultation response','q3_klinik_etik_karar','D→1; A/B/C/E→0.','Hypothetical preference.'),
    ('paylasimli_kurumsal_karar','Vignette B/D response grouping','q3_klinik_etik_karar','B/D→1; A/C/E→0.','Legacy name; analytic grouping, not a validated shared decision-making measure.'),
    ('hukuki_risk_ana_engel','Legal risk as principal barrier','q4_pratik_engel','A→1; B/C/D/E/F→0.','Other/all remains 0 in primary analysis.'),
    ('yasal_duzenleme_talebi','Legal regulation priority','q6_A_yasal_duzenleme','Copy valid binary source.','Priority, not an effectiveness measure.'),
    ('dnr_protokol_talebi','Written protocol/DNR-form priority','q6_B_yazili_protokol_DNR_formu','Copy valid binary source.','Priority, not an effectiveness measure.'),
    ('hukuki_prosedurel_cozum','Legal/procedural solution preference','yasal_duzenleme_talebi;dnr_protokol_talebi','1 if either indicator is 1; 0 if both 0; otherwise missing.','Logical OR includes both selections, not a count or validated scale.'),
    ('q5a_yetkinlik_yuksek','High communication-competence endorsement','q5a_yasam_sonu_konusmasi_yetkinlik','4/5→1; 1/2/3→0.','Self-rated competence.'),
    ('q5b_deger_etkisi_yuksek','High values-influence endorsement','q5b_dini_kulturel_degerler_etkisi','4/5→1; 1/2/3→0.','One missing; n=27.'),
    ('q5c_catismayi_dile_getirmede_gucluk_yuksek','High difficulty voicing disagreement','q5c_etik_gorus_catismasi_dile_getirme','4/5→1; 1/2/3→0.','One missing; n=27. Higher means greater difficulty.'),
]:
    add(name,label,'number',source,rule,{'0':'Absent/not endorsed','1':'Present/endorsed'},binary_missing,note)
for name, label, source, rule in [
    ('asistan','Resident indicator','unvan','1 if Asistan hekim; otherwise 0.'),
    ('deneyim_10plus','10+ experience category indicator','mesleki_deneyim','1 if 10+ yıl; otherwise 0.'),
    ('deneyim_0_3','0–3 experience category indicator','mesleki_deneyim','1 if 0-3 yıl; otherwise 0.'),
    ('deneyim_4plus','4+ experience categories indicator','mesleki_deneyim','1 if 4-10 yıl or 10+ yıl; otherwise 0.'),
    ('birim_anestezi','Anesthesiology field indicator','birim','1 if text contains Anesteziyoloji, including joint selection; otherwise 0.'),
]:
    add(name,label,'integer',source,rule,{'0':'No','1':'Yes'},
        'Current demographic sources are complete. Implementation evaluates other/blank entries as 0; not used as primary clinical missingness coding.')
for name,label,source,rule in [
    ('hukuki_guvensizlik_sens','Low security: double marking assigned 1','hukuki_guvensizlik;q4_hukuki_guven','Copy primary indicator; assign 1 for documented 1;3 marking.'),
    ('hukuki_guvensizlik_sens_high','Low security: double marking assigned 3','hukuki_guvensizlik;q4_hukuki_guven','Copy primary indicator; assign 0 for documented 1;3 marking.'),
    ('hukuki_risk_ana_engel_sens','Legal barrier including other/all','hukuki_risk_ana_engel;q4_pratik_engel_diger_metni','Copy primary indicator; assign 1 when stripped casefolded other text equals hepsi.'),
]:
    add(name,label,'number',source,rule,{'0':'No','1':'Yes'},
        'Other primary missing values remain missing.', 'Sensitivity only; does not replace the primary definition.')


def build():
    raw, derived = pd.read_csv(ROOT / RAW), pd.read_csv(ROOT / DERIVED)
    if set(derived) != set(SPECS):
        raise ValueError(f'Dictionary/schema difference: {set(derived) ^ set(SPECS)}')
    assert raw.equals(derived[list(raw)])
    rows=[]
    for col in derived:
        row = dict(SPECS[col])
        row['dataset_paths'] = RAW+';'+DERIVED if col in raw else DERIVED
        row['origin'] = 'raw, copied unchanged to processed' if col in raw else 'derived'
        row['observed_nonmissing_n'] = int(derived[col].notna().sum())
        row['observed_missing_n'] = int(derived[col].isna().sum())
        rows.append(row)
    result = pd.DataFrame(rows)
    result.to_csv(META/'data_dictionary.csv', index=False, encoding='utf-8-sig')
    intro = '''# Data dictionary — revised ICU end-of-life survey

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
'''
    out=[intro]
    for row in rows:
        out.append(f"\n### `{row['variable']}`\n\n{row['label_en']}\n\n")
        out.append(f"- Origin/type: {row['origin']}; {row['storage_type']}.\n- Source: {row['source']}.\n- Coding: {row['coding_or_derivation']}\n")
        codes=json.loads(row['value_labels_json'])
        if codes:
            out.append('- Values: '+ '; '.join(f'`{k}` = {v}' for k,v in codes.items())+'.\n')
        out.append(f"- Missing rule: {row['missing_value_rule']}\n- Observed: {row['observed_nonmissing_n']} nonmissing, {row['observed_missing_n']} blank/missing.\n")
        if row['interpretation_note']:
            out.append('- Note: '+row['interpretation_note']+'\n')
    (META/'data_dictionary.md').write_text(''.join(out),encoding='utf-8')
    print(f'Dictionary written: {len(raw.columns)} raw + {len(derived.columns)-len(raw.columns)} derived = {len(rows)} fields')
    return result


if __name__ == '__main__':
    build()
