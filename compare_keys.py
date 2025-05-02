import json
import os

def extract_keys(data, parent_key=""):
    keys = {}
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            keys[full_key] = value if not isinstance(value, (dict, list)) else None
            keys.update(extract_keys(value, full_key))
    elif isinstance(data, list):
        for index, item in enumerate(data):
            full_key = f"{parent_key}[{index}]" if parent_key else f"[{index}]"
            keys.update(extract_keys(item, full_key))
    return keys

def add_missing_keys(target, source, log=[]):
    if isinstance(source, dict):
        for key, value in source.items():
            if key not in target:
                target[key] = value
                log.append(f"Added key: '{key}' with value: '{value}'")
            elif isinstance(value, dict):
                target[key] = add_missing_keys(target.get(key, {}), value, log)
            elif isinstance(value, list):
                if key not in target:
                    target[key] = value
                else:
                    target[key] = add_missing_keys(target[key], value, log)
    elif isinstance(source, list) and isinstance(target, list):
        for index, item in enumerate(source):
            if index >= len(target):
                target.append(item)
                log.append(f"Added list item at index [{index}]: {item}")
            elif isinstance(item, (dict, list)):
                target[index] = add_missing_keys(target[index], item, log)
    return target

def compare_and_update_all_keys(source_file_path, directory_path):
    # Load the source JSON (e.g., en.json)
    with open(source_file_path, 'r', encoding='utf-8') as src_file:
        source_json = json.load(src_file)
        source_keys = extract_keys(source_json)

    # Iterate through all .json files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".json") and filename != os.path.basename(source_file_path):
            target_file_path = os.path.join(directory_path, filename)
            with open(target_file_path, 'r', encoding='utf-8') as tgt_file:
                target_json = json.load(tgt_file)
                target_keys = extract_keys(target_json)

            only_in_source = set(source_keys.keys()) - set(target_keys.keys())
            only_in_target = set(target_keys.keys()) - set(source_keys.keys())

            print(f"\n--- Updating {filename} ---")
            print("Keys missing in target:")
            for key in sorted(only_in_source):
                print(key)

            print("Keys only in target:")
            for key in sorted(only_in_target):
                print(key)

            # Add missing keys
            log = []
            updated_json = add_missing_keys(target_json, source_json, log)

            # Write back updated JSON
            with open(target_file_path, 'w', encoding='utf-8') as tgt_file:
                json.dump(updated_json, tgt_file, indent=4, ensure_ascii=False)

            print("Keys added:")
            for index, entry in enumerate(log, 1):
                print(f"{index}. {entry}")
            print(f"✅ Updated: {target_file_path}")

# Example usage
source_file = 'S:\kombee\Translate\i18n\en.json'
directory = os.path.dirname(source_file)
compare_and_update_all_keys(source_file, directory)
