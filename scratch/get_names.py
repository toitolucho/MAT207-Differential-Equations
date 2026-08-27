import os
import json

mathcha_dir = r"d:\Documents\USFX\MAT207\Texto Guia -Latex\MAT207-Differential-Equations\mathcha"

def get_first_text(data):
    if isinstance(data, dict):
        if "text" in data and isinstance(data["text"], str) and not data["text"].startswith("\\"):
            return data["text"]
        for key, value in data.items():
            res = get_first_text(value)
            if res:
                return res
    elif isinstance(data, list):
        for item in data:
            res = get_first_text(item)
            if res:
                return res
    return None

for root, dirs, files in os.walk(mathcha_dir):
    for file in files:
        if len(file) > 10: # likely a uuid
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    first_text = get_first_text(data)
                    rel_path = os.path.relpath(file_path, mathcha_dir)
                    print(f"{rel_path}: {first_text}")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
