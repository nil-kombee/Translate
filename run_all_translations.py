import os
import json
import pandas as pd

BASE_PATH = "/Users/imac/Documents/Nil/Translate"
I18N_PATH = os.path.join(BASE_PATH, "i18n")
CONVERTED_PATH = os.path.join(BASE_PATH, "converted")
EN_JSON_PATH = os.path.join(I18N_PATH, "en.json")
XLSX_PATH = os.path.join(BASE_PATH, "Sanitized.xlsx")
SHEET_NAME = "Frontend-live-editing"

LANGUAGE_COLUMN_MAP = {
    'pu': 'Corrected Punjabi Content',
    'gu': 'Corrected Gujarati Content',
    'ta': 'Corrected Tamil Content',
    'te': 'Corrected Telugu Content',
    'ml': 'Corrected Malayalam Content',
    'ka': 'Corrected Kannada Content',
    'mr': 'Corrected Marathi Content',
    'od': 'Corrected Odia Content',
    'be': 'Corrected Bengali Content',
    'as': 'Corrected Assamese Content',
    'hi': 'Corrected Hindi Content'
}

os.makedirs(CONVERTED_PATH, exist_ok=True)

def compare_keys(en_path, lang_path):
    with open(en_path, 'r', encoding='utf-8') as f1:
        en_data = json.load(f1)
    with open(lang_path, 'r', encoding='utf-8') as f2:
        lang_data = json.load(f2)

    for key, val in en_data.items():
        if key not in lang_data:
            lang_data[key] = val

    with open(lang_path, 'w', encoding='utf-8') as f:
        json.dump(lang_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Synced missing keys to {os.path.basename(lang_path)}")

def translate_json(lang, json_path, xlsx_path, column_name):
    df = pd.read_excel(xlsx_path, sheet_name=SHEET_NAME)
    df = df[['Key', column_name]].dropna()
    translation_map = dict(zip(df['Key'], df[column_name]))

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for k in data:
        if k in translation_map:
            data[k] = translation_map[k]

    output_path = os.path.join(CONVERTED_PATH, f"updated_{lang}.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"🎉 Updated translations for {lang} saved to: {output_path}")

for lang_code, column in LANGUAGE_COLUMN_MAP.items():
    print(f"\n--- Processing {lang_code.upper()} ---")
    lang_json_path = os.path.join(I18N_PATH, f"{lang_code}.json")

    compare_keys(EN_JSON_PATH, lang_json_path)
    translate_json(lang_code, lang_json_path, XLSX_PATH, column)

print("\n✅ All languages processed successfully!")

# python run_all_translations.py