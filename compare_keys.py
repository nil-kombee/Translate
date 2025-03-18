import json

def extract_keys(data, parent_key=""):
    """
    Recursively extract all keys from a JSON object.

    Args:
        data (dict or list): The JSON object (can be a dictionary or a list).
        parent_key (str): The base key to prepend for nested keys.

    Returns:
        dict: A dictionary of keys and their corresponding values.
    """
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
    """
    Add missing key-value pairs from the source JSON to the target JSON.

    Args:
        target (dict or list): Target JSON object to update.
        source (dict or list): Source JSON object to take values from.
        log (list): List of log messages about added keys.

    Returns:
        dict: Updated target JSON object.
    """
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

def compare_and_update_keys(file1_path, file2_path):
    """
    Compare keys of two JSON files and update the second file with missing keys from the first file.

    Args:
        file1_path (str): Path to the first JSON file (source).
        file2_path (str): Path to the second JSON file (target).
    """
    # Load JSON files
    with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
        json1 = json.load(file1)
        json2 = json.load(file2)

    # Extract keys
    keys1 = extract_keys(json1)
    keys2 = extract_keys(json2)

    # Identify missing keys
    only_in_file1 = set(keys1.keys()) - set(keys2.keys())
    print("Keys present in file 1 but not in file 2:")
    for key in sorted(only_in_file1):
        print(key)

    print("\nKeys present in file 2 but not in file 1:")
    only_in_file2 = set(keys2.keys()) - set(keys1.keys())
    for key in sorted(only_in_file2):
        print(key)

    # Add missing keys to JSON 2
    log = []
    updated_json2 = add_missing_keys(json2, json1, log)

    # Overwrite the second JSON file with the updated content
    with open(file2_path, 'w', encoding='utf-8') as file2:
        json.dump(updated_json2, file2, indent=4, ensure_ascii=False)

    # Log added keys in the terminal
    print("\nKeys added to File 2:")
    for index, entry in enumerate(log, start=1):
        print(f"{index}. {entry}")

    print(f"\nUpdated JSON file saved at: {file2_path}")

# Example Usage
file1_path = '/Users/imac/Documents/Nil/Translate/i18n/en.json'  # Path to the first JSON file
file2_path = '/Users/imac/Documents/Nil/Translate/i18n/te.json'  # Path to the second JSON file

compare_and_update_keys(file1_path, file2_path)