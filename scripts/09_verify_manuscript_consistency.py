"""Compare regenerated results with numeric cells extracted from revised Word files.

The fixed manifest records the checked document hashes. No Word file or private
source scan is required to repeat this comparison, and no document is modified.
"""
from pathlib import Path
import hashlib
import json
import math
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def number(x):
    x = float(x)
    if math.isinf(x):
        return '∞'
    if x == 0:
        return '0'
    return f'{x:.3f}' if 0 < x < .01 else f'{x:.2f}'


def pvalue(x):
    return '<0.001' if x < .001 else f'{x:.3f}'


def group_counts(r):
    a,b,c,d = [int(r[k]) for k in ('a_exp1_out1','b_exp1_out0','c_exp0_out1','d_exp0_out0')]
    return [f'{a}/{a+b}({100*a/(a+b):.1f}%)', f'{c}/{c+d}({100*c/(c+d):.1f}%)']


def interval(r):
    return f'{number(r.or_conditional)}({number(r.or_exact95_lower)}–{number(r.or_exact95_upper)})'


def verify():
    manifest = json.loads((ROOT/'docs/manuscript_results_manifest.json').read_text())
    raw = pd.read_csv(ROOT/'data/raw/survey_responses_deidentified.csv')
    derived = pd.read_csv(ROOT/'data/processed/survey_responses_derived.csv')
    tables = ROOT/'outputs/tables'
    composite = pd.read_csv(tables/'composite_indicators.csv').set_index('gosterge')
    fisher = pd.read_csv(tables/'fisher_exact_tests.csv')
    firth = pd.read_csv(tables/'firth_logistic_models.csv')
    sens = pd.read_csv(tables/'sensitivity_analyses.csv')
    checks = []

    def check(name, actual, expected):
        if actual != expected:
            raise AssertionError(f'{name}: obtained {actual!r}, expected {expected!r}')
        checks.append(name)

    check('participant count', len(raw), 28)
    check('raw fields preserved in processed data', raw.equals(derived[list(raw)]), True)
    demo = [('unvan','Asistan hekim'),('unvan','Uzman hekim'),('unvan','Öğretim üyesi'),
            ('birim','Anesteziyoloji ve Reanimasyon'),('birim','Yoğun bakım'),
            ('birim','Yoğun bakım;Anesteziyoloji ve Reanimasyon'),('birim','Diğer'),
            ('mesleki_deneyim','0-3 yıl'),('mesleki_deneyim','4-10 yıl'),('mesleki_deneyim','10+ yıl'),
            ('onceki_yasam_sonu_kararda_aktif_rol','Evet'),('onceki_yasam_sonu_kararda_aktif_rol','Hayır'),
            ('onceki_yasam_sonu_kararda_aktif_rol',None)]
    demo_rows=[]
    for col,value in demo:
        n=int((raw[col].isna() if value is None else raw[col].eq(value)).sum())
        demo_rows.append([f'{n}/28',f'{100*n/28:.1f}'])
    check('Table 1: all demographic numerators and percentages',demo_rows,manifest['main_table_numeric_cells'][0])
    indicator_order=['hukuki_bilgi_dogru','hukuki_guvensizlik','hukuki_risk_ana_engel',
        'hukuki_prosedurel_cozum','etik_esdegerlik','withdraw_daha_agir',
        'riskten_kacinan_tedaviye_devam','paylasimli_kurumsal_karar',
        'yasal_duzenleme_talebi','dnr_protokol_talebi','q6_C_etik_kurul_danismanlik',
        'q6_D_hekim_egitimi','q6_E_palyatif_bakim']
    rows=[]
    for key in indicator_order:
        r=composite.loc[key]
        check('Table 2 raw-derived count: '+key,[int(derived[key].sum()),int(derived[key].notna().sum())],
              [int(r.n_pozitif),int(r.payda)])
        rows.append([f'{int(r.n_pozitif)}/{int(r.payda)}',f'{r.yuzde:.1f}',f'{r.wilson95_alt:.1f}-{r.wilson95_ust:.1f}'])
    check('Table 2: all indicator cells including Wilson intervals',rows,manifest['main_table_numeric_cells'][1])
    selected=[('hukuki_risk_ana_engel','hukuki_prosedurel_cozum'),
              ('hukuki_guvensizlik','hukuki_prosedurel_cozum'),
              ('aktif_rol_var','riskten_kacinan_tedaviye_devam'),
              ('hukuki_bilgi_dogru','hukuki_guvensizlik'),('hukuki_bilgi_dogru','hukuki_prosedurel_cozum')]
    rows=[]
    for x,y in selected:
        r=fisher.loc[fisher.maruziyet.eq(x)&fisher.sonuc.eq(y)].iloc[0]
        rows.append([*group_counts(r),f'{100*r.risk_farki:.1f}',interval(r),pvalue(r.p_fisher)])
    check('Table 3: five comparisons, all numeric cells',rows,manifest['main_table_numeric_cells'][2])
    rows=[[*group_counts(r),interval(r),pvalue(r.p_fisher),pvalue(r.p_holm_9_tests)] for _,r in fisher.iterrows()]
    check('Table S2: all nine comparisons including Holm correction',rows,manifest['supplement_numeric_cells'][0])
    rows=[]
    for _,r in firth.loc[firth.term.ne('Intercept')].iterrows():
        rows.append([f'{int(r.n)}{int(r.events)}/{int(r.non_events)}',number(r.OR),
                     f'{number(r.OR95_lower_profile)}–{number(r.OR95_upper_profile)}',pvalue(r.p_penalized_LR)])
    check('Table S3: six coefficients, profile intervals and PLR p',rows,manifest['supplement_numeric_cells'][1])
    rows=[]
    for _,r in sens.iterrows():
        if r.scenario.startswith('confidence_') != (r.maruziyet=='hukuki_guvensizlik'):
            continue
        a,b,c,d=[int(r[k]) for k in ('a_exp1_out1','b_exp1_out0','c_exp0_out1','d_exp0_out0')]
        rows.append([f'{a}/{a+b}',f'{c}/{c+d}',pvalue(r.p_fisher)])
    check('Table S4: all four reported sensitivities',rows,manifest['supplement_numeric_cells'][2])
    check('paired keyed-response/low-security count',int(derived.loc[derived.hukuki_bilgi_dogru.eq(1),'hukuki_guvensizlik'].sum()),19)
    check('both solution priorities',int((derived.yasal_duzenleme_talebi.eq(1)&derived.dnr_protokol_talebi.eq(1)).sum()),8)
    counts=raw.filter(regex='^q6_[A-F]_').sum(axis=1).value_counts().sort_index().to_dict()
    check('Q6 marking counts',{str(k):int(v) for k,v in counts.items()},{'1':16,'2':11,'3':1})
    dictionary=pd.read_csv(ROOT/'data/metadata/data_dictionary.csv')
    check('dictionary coverage/order',dictionary.variable.tolist(),derived.columns.tolist())
    check('dictionary nonmissing counts',dictionary.observed_nonmissing_n.tolist(),derived.notna().sum().tolist())
    report={'status':'passed','scope':'Numerical agreement of six tables and key narrative counts with checked Word versions; not verification of author-dependent study facts.',
            'checked_documents':{k:manifest[k] for k in ('manuscript','supplement')},
            'raw_sha256':hashlib.sha256((ROOT/'data/raw/survey_responses_deidentified.csv').read_bytes()).hexdigest(),
            'checks_passed':len(checks),'checks':checks,'dictionary_fields':len(dictionary),
            'known_label_correction':manifest['known_label_correction'],'limitations':manifest['limitations']}
    (ROOT/'outputs/logs/manuscript_consistency.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f'Manuscript numerical consistency: {len(checks)} checks passed; one experience-category label correction documented.')
    return report


if __name__ == '__main__':
    verify()
