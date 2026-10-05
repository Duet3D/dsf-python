import enum
import importlib
import json
import pkgutil
from typing import Mapping

import src.dsf as dsf


def check_json(expected_dict: Mapping[str, object], json_str: str) -> None:
    try:
        json_obj = json.loads(json_str)
    except json.JSONDecodeError:
        raise AssertionError("Invalid JSON string")

    for key, expected_value in expected_dict.items():
        if key not in json_obj:
            raise AssertionError(f"Key '{key}' not found in JSON {json_str}")
        if json_obj[key] != expected_value:
            raise AssertionError(
                f"Value for key '{key}' does not match. Expected: {expected_value}, Found: {json_obj[key]}"
            )


def get_enums() -> list[type[enum.Enum]]:
    """Get every enum defined by dsf-python"""
    enums: list[type[enum.Enum]] = []
    for module_info in pkgutil.walk_packages(dsf.__path__, f"{dsf.__name__}."):
        module = importlib.import_module(module_info.name)
        for value in vars(module).values():
            if isinstance(value, type) and issubclass(value, enum.Enum) and value.__module__ == module.__name__:
                enums.append(value)
    return enums
