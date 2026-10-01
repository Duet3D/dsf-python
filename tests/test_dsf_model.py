"""
Check the object model against DSF's own object model.

tests/object_model/dsf_model.json is generated from DuetAPI by scripts/generate_dsf_model (make generate_dsf_model),
see there for a description of its contents. All expected JSON is written by DSF, so the JSON written by dsf-python
must match it exactly.
"""

import copy
import importlib
import json
import pkgutil
import unittest
from typing import Any, Callable, TypeVar, cast

import src.dsf.object_model as object_model
from src.dsf.object_model.model_dictionary import ModelDictionary
from src.dsf.object_model.model_object import ModelObject
from src.dsf.utils import camel_to_snake, snake_to_camel

with open("tests/object_model/dsf_model.json") as fp:
    DSF_MODEL: dict[str, Any] = json.load(fp)
DSF_CLASSES: dict[str, dict[str, Any]] = DSF_MODEL["classes"]
DSF_DYNAMIC: list[dict[str, Any]] = DSF_MODEL["dynamic"]
# Properties left out of the DSF defaults because they depend on when or where DSF runs, as <class>.<JSON key>
DSF_RUNTIME_DEFAULTS: set[str] = set(DSF_MODEL["runtimeDefaults"])

T = TypeVar("T")


def _python_classes() -> dict[str, type[ModelObject]]:
    for module in pkgutil.walk_packages(object_model.__path__, f"{object_model.__name__}."):
        importlib.import_module(module.name)

    classes: dict[str, type[ModelObject]] = {}
    pending: list[type[ModelObject]] = [ModelObject]
    while pending:
        cls = pending.pop()
        if cls.__module__.startswith(object_model.__name__):
            classes[cls.__name__] = cls
        pending.extend(cls.__subclasses__())
    return classes


PYTHON_CLASSES = _python_classes()
TESTED_CLASSES = {name: dsf_class for name, dsf_class in DSF_CLASSES.items() if name in PYTHON_CLASSES}


def _property_name(json_key: str) -> str:
    # "global" is a reserved keyword in Python, so it is converted to "globals"
    return "globals" if json_key == "global" else camel_to_snake(json_key)


def _json_key(property_name: str) -> str:
    return "global" if property_name == "globals" else snake_to_camel(property_name)


def _properties(cls: type[ModelObject]) -> list[str]:
    return [name for name in dir(cls) if isinstance(getattr(cls, name), property)]


def _create(name: str) -> ModelObject:
    """Create a model object like DSF does, i.e. dynamic model objects are deserialized through their base class"""
    dsf_class = DSF_CLASSES[name]
    if "base" in dsf_class:
        return PYTHON_CLASSES[dsf_class["base"]].from_json(copy.deepcopy(dsf_class["create"]))
    return PYTHON_CLASSES[name]()


def _load(name: str, data: dict[str, Any]) -> ModelObject:
    """Deserialize a model object like DSF does, i.e. dynamic model objects are deserialized through their base class"""
    return PYTHON_CLASSES[DSF_CLASSES[name].get("base", name)].from_json(copy.deepcopy(data))


def _to_json(model: ModelObject) -> object:
    return json.loads(model.to_json())


def _remove_runtime_defaults(model: object, data: object) -> None:
    """Remove the properties DSF leaves out of its defaults from the JSON written for the given model"""
    if isinstance(model, ModelObject) and isinstance(data, dict):
        items = cast(dict[str, object], data)
        for name in _properties(type(model)):
            key = _json_key(name)
            if f"{type(model).__name__}.{key}" in DSF_RUNTIME_DEFAULTS:
                items.pop(key, None)
            elif key in items:
                _remove_runtime_defaults(getattr(model, name), items[key])
    elif isinstance(model, dict) and isinstance(data, dict):
        items = cast(dict[str, object], data)
        for key, value in cast(dict[str, object], model).items():
            if key in items:
                _remove_runtime_defaults(value, items[key])
    elif isinstance(model, list) and isinstance(data, list):
        for value, item in zip(cast(list[object], model), cast(list[object], data)):
            _remove_runtime_defaults(value, item)


def _differences(expected: object, actual: object, path: str) -> list[str]:
    """Compare the JSON written by DSF with the JSON written by dsf-python"""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [f"{path}: expected an object, got {actual!r}"]
        expected_items = cast(dict[str, object], expected)
        actual_items = cast(dict[str, object], actual)
        differences: list[str] = []
        for key, item in expected_items.items():
            if key in actual_items:
                differences.extend(_differences(item, actual_items[key], f"{path}.{key}"))
            else:
                differences.append(f"{path}.{key}: missing, expected {item!r}")
        for key, item in actual_items.items():
            if key not in expected_items:
                differences.append(f"{path}.{key}: not written by DSF, got {item!r}")
        return differences
    if isinstance(expected, list):
        expected_items = cast(list[object], expected)
        if not isinstance(actual, list) or len(cast(list[object], actual)) != len(expected_items):
            return [f"{path}: expected {expected!r}, got {actual!r}"]
        differences = []
        for index, (item, actual_item) in enumerate(zip(expected_items, cast(list[object], actual))):
            differences.extend(_differences(item, actual_item, f"{path}[{index}]"))
        return differences
    if isinstance(expected, bool) or isinstance(actual, bool):
        equal = type(expected) is type(actual) and expected == actual
    elif isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        # JSON does not tell integers and floats apart
        equal = expected == actual
    else:
        equal = type(expected) is type(actual) and expected == actual
    return [] if equal else [f"{path}: expected {expected!r}, got {actual!r}"]


class TestDsfModel(unittest.TestCase):
    maxDiff = None

    def _call(self, description: str, function: Callable[[], T]) -> T:
        """Report exceptions raised by dsf-python as test failures"""
        try:
            return function()
        except Exception as e:
            self.fail(f"{description} failed: {type(e).__name__}: {e}")

    def _assert_class(self, model: ModelObject, name: str):
        self.assertEqual(type(model).__name__, name, "DSF creates a different class")

    def test_classes(self):
        missing = sorted(name for name in DSF_CLASSES if name not in PYTHON_CLASSES)
        self.assertEqual(missing, [], "DSF object model classes missing from dsf-python")

    def test_properties(self):
        for name, dsf_class in TESTED_CLASSES.items():
            with self.subTest(dsf_class=name):
                dsf_keys = set(cast(dict[str, object], dsf_class["properties"]))
                python_keys = {_json_key(prop) for prop in _properties(PYTHON_CLASSES[name])}
                self.assertEqual(sorted(dsf_keys - python_keys), [], "Properties missing from dsf-python")
                self.assertEqual(sorted(python_keys - dsf_keys), [], "Properties that do not exist in DSF")

    def test_nullable(self):
        for name, dsf_class in TESTED_CLASSES.items():
            cls = PYTHON_CLASSES[name]
            for key, dsf_property in cast(dict[str, dict[str, Any]], dsf_class["properties"]).items():
                prop = _property_name(key)
                if not isinstance(getattr(cls, prop, None), property):
                    continue
                with self.subTest(property=f"{name}.{key}"):
                    model = self._call("Creating the model", lambda: _create(name))
                    if isinstance(getattr(model, prop), ModelDictionary):
                        # DSF sends null to clear dictionaries
                        continue
                    try:
                        setattr(model, prop, None)
                        nullable = True
                    except (TypeError, ValueError):
                        nullable = False
                    except AttributeError as e:
                        self.fail(f"Cannot be set: {e}")
                    self.assertEqual(nullable, dsf_property["nullable"], "Nullable differs from DSF")

    def test_defaults(self):
        for name, dsf_class in TESTED_CLASSES.items():
            with self.subTest(dsf_class=name):
                model = self._call("Creating the model", lambda: _create(name))
                self._assert_class(model, name)
                actual = _to_json(model)
                _remove_runtime_defaults(model, actual)
                differences = _differences(dsf_class["default"], actual, name)
                self.assertEqual(differences, [], "Default values differ from DSF")

    def test_values(self):
        for name, dsf_class in TESTED_CLASSES.items():
            with self.subTest(dsf_class=name):
                model = self._call("Deserializing", lambda: _load(name, dsf_class["values"]))
                self._assert_class(model, name)
                differences = _differences(dsf_class["values"], _to_json(model), name)
                self.assertEqual(differences, [], "Values differ from DSF")

    def test_patch(self):
        # Update from "values" and then from "nulls" like DSF applies object model patches
        for name, dsf_class in TESTED_CLASSES.items():
            with self.subTest(dsf_class=name):
                model = self._call("Deserializing", lambda: _load(name, dsf_class["values"]))
                model = self._call("Patching", lambda: model.update_from_json(copy.deepcopy(dsf_class["nulls"])))
                self._assert_class(model, name)
                differences = _differences(dsf_class["patched"], _to_json(model), name)
                self.assertEqual(differences, [], "Patched values differ from DSF")

    def test_dynamic(self):
        # Every class selector of dynamic model objects is deserialized to the same class and JSON as in DSF
        for case in DSF_DYNAMIC:
            base = PYTHON_CLASSES[case["base"]]
            data: dict[str, Any] = case["json"]
            with self.subTest(base=case["base"], json=data):
                if "error" in case:
                    with self.assertRaises(Exception, msg=f"DSF rejects it with {case['error']}"):
                        base.from_json(copy.deepcopy(data))
                    continue
                model = self._call("Deserializing", lambda: base.from_json(copy.deepcopy(data)))
                self._assert_class(model, case["class"])
                differences = _differences(case["result"], _to_json(model), case["base"])
                self.assertEqual(differences, [], "Values differ from DSF")


if __name__ == "__main__":
    unittest.main()
