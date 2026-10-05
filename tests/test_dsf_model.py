"""
Check the object model and the enums against DSF's own object model and enums.

tests/object_model/dsf_model.json is generated from DuetAPI by scripts/generate_dsf_model (make generate_dsf_model),
see there for a description of its contents. All expected JSON is written by DSF, so the JSON written by dsf-python
must match it exactly.
"""

import copy
import enum
import importlib
import json
import pkgutil
import unittest
from typing import Any, Callable, TypeVar, cast

import src.dsf.object_model as object_model
from src.dsf.object_model.model_dictionary import ModelDictionary
from src.dsf.object_model.model_object import ModelObject
from src.dsf.object_model.plugins.sbc_permissions import SbcPermissions
from src.dsf.utils import DeprecatedAliasEnumType, camel_to_snake, snake_to_camel
from tests.utils import get_enums

with open("tests/object_model/dsf_model.json") as fp:
    DSF_MODEL: dict[str, Any] = json.load(fp)
DSF_CLASSES: dict[str, dict[str, Any]] = DSF_MODEL["classes"]
DSF_DYNAMIC: list[dict[str, Any]] = DSF_MODEL["dynamic"]
# Properties left out of the DSF defaults because they depend on when or where DSF runs, as <class>.<JSON key>
DSF_RUNTIME_DEFAULTS: set[str] = set(DSF_MODEL["runtimeDefaults"])
DSF_ENUMS: dict[str, dict[str, Any]] = DSF_MODEL["enums"]

# DSF enums that have a different name in dsf-python
RENAMED_ENUMS: dict[str, str] = {
    "EventLogLevel": "LogLevel",
}
# DSF enums that dsf-python intentionally does not implement
UNIMPLEMENTED_ENUMS: set[str] = {
    # Used internally by DuetAPI to describe and update its object model, DSF never reads or writes them as JSON
    "ModelPropertyFlags",
    "ModelPropertyKind",
    "ModelUpdateScope",
}
# dsf-python enums that have no DSF counterpart
PYTHON_ONLY_ENUMS: set[str] = {
    # Axis letters, which DSF keeps as characters
    "AxisLetter",
}
# DSF writes flags enums such as SbcPermissions as lists of the flags that are set, so their zero member is written
# as an empty list rather than as an item of its own. DSF reads the item below for it, which is the value of
# dsf-python's zero member, as <DSF enum> => item
DSF_EMPTY_FLAGS_ITEMS: dict[str, str] = {
    "SbcPermissions": "none",
}

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


def _python_enums() -> dict[str, type[enum.Enum]]:
    enums: dict[str, type[enum.Enum]] = {}
    for cls in get_enums():
        if cls.__name__ in enums:
            raise ValueError(f"More than one dsf-python enum is called {cls.__name__}")
        enums[cls.__name__] = cls
    return enums


PYTHON_ENUMS = _python_enums()


def _comparable_json(value: object) -> str:
    """Key of a JSON value that tells apart values that compare equal in Python, e.g. 1, 1.0 and True"""
    return json.dumps(value)


def _python_enum_json(member: enum.Enum) -> object:
    """JSON written by dsf-python for an enum member"""

    def serialize(obj: object) -> object:
        # SbcPermissions are written by value, see ModelObject, the other enums are str or int enums
        if isinstance(obj, SbcPermissions):
            return obj.value
        raise TypeError(f"dsf-python does not write {obj!r} to JSON")

    return json.loads(json.dumps(member, default=serialize))


def _dsf_enum_json(name: str, member: dict[str, Any]) -> object:
    """JSON written by DSF for an enum member, a flag of a flags enum written as a list of flags is its item"""
    if "json" not in member:
        raise ValueError(f"DSF cannot write {name}.{member['name']}: {member.get('error')}")
    value: object = member["json"]
    if isinstance(value, list):
        items = cast(list[object], value)
        if len(items) == 1:
            return items[0]
        if not items and name in DSF_EMPTY_FLAGS_ITEMS:
            return DSF_EMPTY_FLAGS_ITEMS[name]
        raise ValueError(f"Cannot compare {name}.{member['name']}, DSF writes it as {value!r}")
    return value


def _enum_differences(cls: type[enum.Enum], dsf_name: str, dsf_enum: dict[str, Any]) -> tuple[list[str], list[str]]:
    """
    Compare the values of the canonical members of a dsf-python enum with the JSON DSF writes for its members.
    Aliases, i.e. previous or kept names of a member and values only accepted by _missing_, are not compared.
    Returns the values missing from dsf-python and the values DSF does not have, as JSON
    """
    dsf_values = {_comparable_json(_dsf_enum_json(dsf_name, member)) for member in dsf_enum["members"]}
    python_values = {
        _comparable_json(_python_enum_json(member)) for name, member in cls.__members__.items() if member.name == name
    }
    return sorted(dsf_values - python_values), sorted(python_values - dsf_values)


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


class TestDsfEnums(unittest.TestCase):
    def test_enums(self):
        # Every DSF enum has a dsf-python counterpart unless it is listed above, and vice versa
        mapped = [RENAMED_ENUMS.get(name, name) for name in DSF_ENUMS]
        missing = sorted(
            name
            for name in DSF_ENUMS
            if RENAMED_ENUMS.get(name, name) not in PYTHON_ENUMS and name not in UNIMPLEMENTED_ENUMS
        )
        self.assertEqual(
            missing, [], "DSF enums missing from dsf-python, implement them or add them to UNIMPLEMENTED_ENUMS"
        )
        extra = sorted(name for name in PYTHON_ENUMS if name not in mapped and name not in PYTHON_ONLY_ENUMS)
        self.assertEqual(
            extra, [], "dsf-python enums that do not exist in DSF, map them or add them to PYTHON_ONLY_ENUMS"
        )
        duplicates = sorted({name for name in mapped if mapped.count(name) > 1 and name in PYTHON_ENUMS})
        self.assertEqual(duplicates, [], "dsf-python enums mapped to more than one DSF enum")

    def test_enum_lists(self):
        # The lists above do not contain stale entries
        stale = sorted(name for name in RENAMED_ENUMS if name not in DSF_ENUMS)
        self.assertEqual(stale, [], "RENAMED_ENUMS lists DSF enums that do not exist")
        stale = sorted(name for name in RENAMED_ENUMS.values() if name not in PYTHON_ENUMS)
        self.assertEqual(stale, [], "RENAMED_ENUMS lists dsf-python enums that do not exist")
        stale = sorted(
            name
            for name in UNIMPLEMENTED_ENUMS
            if name not in DSF_ENUMS or name in RENAMED_ENUMS or name in PYTHON_ENUMS
        )
        self.assertEqual(stale, [], "UNIMPLEMENTED_ENUMS lists DSF enums that do not exist or are implemented")
        stale = sorted(
            name
            for name in PYTHON_ONLY_ENUMS
            if name not in PYTHON_ENUMS or name in DSF_ENUMS or name in RENAMED_ENUMS.values()
        )
        self.assertEqual(stale, [], "PYTHON_ONLY_ENUMS lists dsf-python enums that do not exist or exist in DSF")
        stale = sorted(
            name
            for name in DSF_EMPTY_FLAGS_ITEMS
            if name not in DSF_ENUMS or not any(member.get("json") == [] for member in DSF_ENUMS[name]["members"])
        )
        self.assertEqual(stale, [], "DSF_EMPTY_FLAGS_ITEMS lists DSF enums that do not write an empty list")

    def test_enum_values(self):
        # Every dsf-python enum has a member for every value DSF writes, and no other ones
        for dsf_name, dsf_enum in DSF_ENUMS.items():
            cls = PYTHON_ENUMS.get(RENAMED_ENUMS.get(dsf_name, dsf_name))
            if cls is None:
                continue
            with self.subTest(enum=cls.__name__):
                try:
                    missing, extra = _enum_differences(cls, dsf_name, dsf_enum)
                except ValueError as e:
                    self.fail(str(e))
                differences: list[str] = []
                if missing:
                    differences.append(f"values missing from dsf-python: {', '.join(missing)}")
                if extra:
                    differences.append(f"values DSF does not have: {', '.join(extra)}")
                if differences:
                    self.fail(f"{cls.__name__} differs from DSF's {dsf_name}, {'; '.join(differences)}")

    def test_enum_differences(self):
        # The comparison above detects both missing and extra values, but no aliases
        dsf_enum: dict[str, Any] = {
            "members": [{"name": "A", "value": 0, "json": "a"}, {"name": "B", "value": 1, "json": "b"}]
        }

        class MissingValue(str, enum.Enum):
            A = "a"

        class ExtraValue(str, enum.Enum):
            A = "a"
            B = "b"
            C = "c"

        class AliasOnly(str, enum.Enum, metaclass=DeprecatedAliasEnumType):
            __kept_aliases__ = ("KEPT_B",)

            A = "a"
            B = "b"

            # Previous and kept names of members
            OldB = B
            KEPT_B = B

            @classmethod
            def _missing_(cls, value: object):
                # Values only read
                return cls.B if value == "bb" else None

        self.assertEqual(_enum_differences(MissingValue, "Test", dsf_enum), (['"b"'], []))
        self.assertEqual(_enum_differences(ExtraValue, "Test", dsf_enum), ([], ['"c"']))
        self.assertEqual(_enum_differences(AliasOnly, "Test", dsf_enum), ([], []))
        self.assertIs(AliasOnly("bb"), AliasOnly.B)

    def test_enum_differences_types(self):
        # Values are only equal if their JSON types are the same
        dsf_enum: dict[str, Any] = {
            "members": [{"name": "A", "value": 1, "json": True}, {"name": "B", "value": 2, "json": "2"}]
        }

        class IntValues(enum.IntEnum):
            A = 1
            B = 2

        self.assertEqual(_enum_differences(IntValues, "Test", dsf_enum), (['"2"', "true"], ["1", "2"]))

    def test_enum_differences_flags(self):
        # Flags written as lists are compared by their item, an empty list only if DSF_EMPTY_FLAGS_ITEMS lists it
        dsf_enum: dict[str, Any] = {
            "members": [{"name": "None", "value": 0, "json": []}, {"name": "A", "value": 1, "json": ["a"]}]
        }

        class Flags(str, enum.Enum):
            NONE = "none"
            A = "a"

        self.assertEqual(_enum_differences(Flags, "SbcPermissions", dsf_enum), ([], []))
        with self.assertRaisesRegex(ValueError, r"Cannot compare Test\.None, DSF writes it as \[\]"):
            _enum_differences(Flags, "Test", dsf_enum)
        with self.assertRaisesRegex(ValueError, r"DSF cannot write Test\.A: Error"):
            _enum_differences(Flags, "Test", {"members": [{"name": "A", "value": 1, "error": "Error"}]})


if __name__ == "__main__":
    unittest.main()
