import json
import os

def get_version() -> str:
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    package_json_path = os.path.join(root_dir, 'package.json')
    try:
        with open(package_json_path, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
            return package_data.get("version", "unknown")
    except Exception:
        return "unknown"