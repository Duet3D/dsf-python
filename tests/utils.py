import json


def check_json(expected_dict: dict[str, object], json_str: str) -> None:
    try:
        json_obj = json.loads(json_str)
    except json.JSONDecodeError:
        raise AssertionError("Invalid JSON string")

    for key, expected_value in expected_dict.items():
        if key not in json_obj:
            raise AssertionError(f"Key '{key}' not found in JSON {json_str}")
        if json_obj[key] != expected_value:
            raise AssertionError(f"Value for key '{key}' does not match. Expected: {expected_value}, Found: {json_obj[key]}")