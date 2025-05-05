import pandas as pd
import json

# Paths to the files
xlsx_path = r"S:\kombee\Translate\Multilanguage_Client_live_editing_sheet.xlsx"
json_path = r"S:\kombee\Translate\i18n\ka.json"
output_json_path = r"S:\kombee\Translate\updaed_ka_json_file.json"


# Load the sheet named "Sheet1" from the Excel file
sheet_name = "Frontend-live-editing"
df = pd.read_excel(xlsx_path, sheet_name=sheet_name)

# Extract the relevant columns: 'Key' and 'Corrected Telugu Content'
xlsx_data = df[['Key', 'Corrected Kannada Content']].dropna() #Change this according to your needs
xlsx_dict = dict(zip(xlsx_data['Key'], xlsx_data['Corrected Kannada Content'])) #Change this according to your needs

# Load the JSON file
with open(json_path, 'r', encoding='utf-8') as f:

    json_data = json.load(f)

def update_json_with_hierarchical_keys(json_obj, excel_dict):
    """
    Update JSON data based on hierarchical keys from an Excel dictionary.

    Args:
        json_obj (dict): The JSON object to update.
        excel_dict (dict): Dictionary with hierarchical keys from Excel.

    Returns:
        dict: Updated JSON object.
    """
    for hierarchical_key, value in excel_dict.items():
        keys = hierarchical_key.split('/')  # Split hierarchical key into parts
        current_level = json_obj

        # Traverse the JSON structure to reach the appropriate level
        for key in keys[:-1]:
            if key not in current_level or not isinstance(current_level[key], dict):
                # Ensure we don't overwrite non-dict structures
                current_level[key] = {}
            current_level = current_level[key]

        # Update the final key's value only
        final_key = keys[-1]
        if isinstance(current_level, dict):
            current_level[final_key] = value

    return json_obj

# Update the JSON data
updated_json_data = update_json_with_hierarchical_keys(json_data, xlsx_dict)

# Save the updated JSON to a new file
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(updated_json_data, f, indent=4, ensure_ascii=False)

print(f"Updated JSON saved at: {output_json_path}")


