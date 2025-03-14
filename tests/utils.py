import json

from typing import Dict, Union

def check_json(expected_dict: Dict[str, Union[Dict, str, int, float]], json_str: str) -> None:
    try:
        json_obj = json.loads(json_str)
    except json.JSONDecodeError:
        raise AssertionError("Invalid JSON string")

    for key, expected_value in expected_dict.items():
        if key not in json_obj:
            raise AssertionError(f"Key '{key}' not found in JSON {json_str}")
        if json_obj[key] != expected_value:
            raise AssertionError(f"Value for key '{key}' does not match. Expected: {expected_value}, Found: {json_obj[key]}")