import dataiku
import re
from datetime import datetime


def load_data(note_id):
    data = dataiku.Dataset("discharge_llm_mapped_icd10cm_ranked").get_dataframe()
    selected_note = data[data['note_id']==note_id]
    return selected_note

def load_note_id():
    data = dataiku.Dataset("note_id").get_dataframe()
    return data

def extract_section_headers(text):
    pattern = r"\n\d+\..*?:"
    headers = re.findall(pattern, text)
    return headers

def create_header_replacements(text, text_style):
    h_dict = {}
    headers = extract_section_headers(text)
    for h in headers:
        header = h.split('.')[1]
        hformat = header.strip().replace(":", "").title()
        h_dict[h] = f'<span style="{text_style}"><br><br>{hformat}<br></span>'
    return h_dict

def collect_evidence_from_df(df, diagnosis_type):
    evidence_set = set()
    evidence_series = df.query(f"code_type=='{diagnosis_type}'")['evidence'].dropna()
    if not evidence_series.empty:
        for evidence in evidence_series.values:
            quotes = [q.strip() for q in evidence.split("|")]
            evidence_set.update(quotes)
    return evidence_set

def create_evidence_replacements(evidence_set, text_style_set):
    # In case a quote is used as evidence twice, we prioritize the quote to pair with the style in the following order: principal diagnosis, problem list, medical history
    h_dict = {}
    for evidence, text_style in zip(evidence_set, text_style_set):
        if evidence:
            for quotes in evidence:
                if quotes not in h_dict:
                    h_dict[quotes] = f'<span style="{text_style}">{quotes}</span>'
    return h_dict

def replace_strings_regex(corpus, replacements):
    if replacements:
        # Sort keys by length in descending order to avoid partial replacements
        sorted_keys = sorted(replacements.keys(), key=len, reverse=True)
        # Create a regex pattern with all keys
        pattern = re.compile('|'.join(re.escape(key) for key in sorted_keys))
        
        # Function to return the replacement value
        def replace(match):
            return replacements[match.group(0)]

        # Perform the replacement
        return pattern.sub(replace, corpus)
    else:
        return corpus
    

def format_datetime(dt_str):
    dt = datetime.fromisoformat(dt_str.rstrip('Z'))
    return dt.strftime('%B %d, %Y %H:%M:%S')

def load_selected_discharge_summary(note_id):
    data = dataiku.Dataset("discharge_llm_mapped_icd10cm_ranked").get_dataframe()
    discharge_summary_df = (
        data
        .loc[data['note_id']==note_id, ['patient_id', 'note_id', 'discharge_summary']]
        .iloc[0].fillna(""))
    return discharge_summary_df

def load_verified_diagnoses(edit_df, note_id):
    selected_discharged_diagnoses = edit_df[edit_df['Note ID']==note_id]
    selected_discharged_diagnoses = selected_discharged_diagnoses.sort_values(by="Priority", ascending=True)
    return selected_discharged_diagnoses

def load_validated_note_id(edit_df):
    data = edit_df['Note ID'].unique()
    return data

def filter_diagnose(edit_df, type):
    diagnoses = edit_df[edit_df['Diagnosis type'].str.contains(type)]['Mapped ICD10CM code'].values
    return diagnoses
