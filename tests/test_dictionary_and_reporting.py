"""Metadata completeness and source-to-analysis consistency checks."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_dictionary_covers_actual_schema_and_valid_code_domains():
    d = pd.read_csv(ROOT/'data/processed/survey_responses_derived.csv')
    dictionary = pd.read_csv(ROOT/'data/metadata/data_dictionary.csv')
    assert dictionary.variable.is_unique
    assert dictionary.variable.tolist() == d.columns.tolist()
    assert dictionary.observed_missing_n.tolist() == d.isna().sum().tolist()
    for _,row in dictionary.iterrows():
        codes=json.loads(row.value_labels_json)
        if not codes:
            continue
        values=d[row.variable].dropna()
        if row.storage_type in ('number','integer'):
            observed={str(int(v)) for v in values}
        else:
            observed=set(values.astype(str))
        assert observed <= set(codes), (row.variable, observed-set(codes))


def test_redundant_q6_text_agrees_with_all_six_binary_columns():
    d = pd.read_csv(ROOT/'data/raw/survey_responses_deidentified.csv')
    options=[c for c in d if c.startswith('q6_') and c[3:5] in [x+'_' for x in 'ABCDEF']]
    assert len(options) == 6
    for _,row in d.iterrows():
        selected=set(row.q6_secimler.split(';'))
        assert selected == {col[3] for col in options if row[col] == 1}
