import json
import os

def get_version() -> str:
    """
    Get the current version of the package from the *package.json* file. \n
    This function is useful for displaying the version in the CLI or GUI. \n
    ***
    Returns:
        str:
            - The version of the package as a string.
            - Returns **"unknown"** if the version cannot be determined.
    """
    
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    package_json_path = os.path.join(root_dir, 'package.json')
    try:
        with open(package_json_path, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
            return package_data.get("version", "unknown")
    except Exception:
        return "unknown"