import inspect
import re
import warnings

from enum import Enum, EnumType
from types import UnionType
from typing import Any, Optional, Callable, TypeVar, TypeAlias, Union, get_args, get_origin, cast, overload


# We don't want our deprecations to be ignored by default, so create our own type.
class DeprecatedWarning(UserWarning):
    pass


TEnum = TypeVar("TEnum", bound=Enum)


def _warn_deprecated_alias(cls: type[Enum], alias: str, member: Enum) -> None:
    warnings.warn(
        f"{cls.__name__}.{alias} is deprecated, use {cls.__name__}.{member.name} instead",
        DeprecatedWarning,
        stacklevel=3,
    )


class _DeprecatedEnumAlias:
    """Class attribute of an enum alias that raises a DeprecatedWarning when it is used"""

    def __init__(self, alias: str, member: Enum) -> None:
        self._alias = alias
        self._member = member

    def __get__(self, instance: object, owner: Optional[type] = None) -> Enum:
        _warn_deprecated_alias(type(self._member), self._alias, self._member)
        return self._member


class DeprecatedAliasEnumType(EnumType):
    """
    Metaclass of enums whose aliases are previous member names.
    Using an alias raises a DeprecatedWarning, except for the aliases listed in __kept_aliases__
    """

    def __new__(metacls, cls: str, bases: tuple[type, ...], classdict: Any, **kwds: Any):
        enum_class = super().__new__(metacls, cls, bases, classdict, **kwds)
        kept_aliases: tuple[str, ...] = classdict.get("__kept_aliases__", ())
        members = cast(dict[str, Enum], enum_class.__members__)
        for alias, member in members.items():
            if alias != member.name and alias not in kept_aliases:
                # Replace the alias, EnumType does not allow members to be reassigned
                type.__setattr__(enum_class, alias, _DeprecatedEnumAlias(alias, member))
        return enum_class

    def __getitem__(cls: type[TEnum], name: str) -> TEnum:  # type: ignore[misc]
        member = cast(TEnum, cls.__members__[name])
        if isinstance(cls.__dict__.get(name), _DeprecatedEnumAlias):
            _warn_deprecated_alias(cls, name, member)
        return member


JSONElement: TypeAlias = dict[str, "JSONElement"] | list["JSONElement"] | str | int | float | bool | None
JSONObj: TypeAlias = dict[str, JSONElement]

T = TypeVar("T")


def _matches_type(value: Any, expected_type: Any) -> bool:
    origin = get_origin(expected_type)
    args = get_args(expected_type)

    if origin in (Union, UnionType):
        return any(_matches_type(value, arg) for arg in args)

    if origin is dict:
        if not isinstance(value, dict):
            return False
        if len(args) != 2:
            return True
        key_type, val_type = args
        typed_dict = cast(dict[Any, Any], value)
        return all(_matches_type(k, key_type) and _matches_type(v, val_type) for k, v in typed_dict.items())

    if origin is list:
        if not isinstance(value, list):
            return False
        if len(args) != 1:
            return True
        typed_list = cast(list[Any], value)
        return all(_matches_type(item, args[0]) for item in typed_list)

    if origin is tuple:
        if not isinstance(value, tuple):
            return False
        typed_tuple = cast(tuple[Any, ...], value)
        if len(args) == 2 and args[1] is Ellipsis:
            return all(_matches_type(item, args[0]) for item in typed_tuple)
        if len(args) != len(typed_tuple):
            return False
        return all(_matches_type(item, item_type) for item, item_type in zip(typed_tuple, args))

    if origin is set:
        if not isinstance(value, set):
            return False
        if len(args) != 1:
            return True
        typed_set = cast(set[Any], value)
        return all(_matches_type(item, args[0]) for item in typed_set)

    try:
        return isinstance(value, expected_type)
    except TypeError:
        return expected_type is Any


@overload
def get_typed_value(data: JSONObj, key: str, expected_type: type[T]) -> T: ...
@overload
def get_typed_value(data: JSONObj, key: str, expected_type: Any) -> Any: ...


def get_typed_value(data: JSONObj, key: str, expected_type: type[T] | Any) -> T:
    """Helper method to get a typed value from a JSON dictionary"""
    if key not in data:
        raise ValueError(f"Missing required parameter '{key}'")
    value = data[key]
    if not _matches_type(value, expected_type):
        raise ValueError(f"Expected parameter '{key}' to be of type {expected_type}, got {type(value)}")
    return cast(T, value)


def camel_to_snake(s: str, keep_acronyms: bool = True) -> str:
    """Convert a camel case string to snake case string
    :param s: The string to convert from
    :param keep_acronyms: Wheter acronyms should be kept uppercase or not
    :returns: The string in snake_case format"""
    # Added a look-behind (?!^) so initials like SBC are not getting snake-cased
    snake = re.sub(r"((?<=[a-z])[A-Z0-9]|(?!^)[A-Z0-9](?=[a-z]))", r"_\1", s)
    return "_".join(w if w.isupper() else w.lower() for w in snake.split("_")) if keep_acronyms else snake.lower()


F = TypeVar("F", bound=Callable[..., Any])


def deprecated(instructions: str) -> Callable[[F], F]:
    """Flags a function/method as deprecated.
    :param instructions: A human-friendly string of instructions
    """

    def decorator(func: F) -> F:
        """This is a decorator which can be used to mark functions as deprecated.
        It will result in a warning being emitted when the function is used."""

        def deprecated_func(*args: Any, **kwargs: Any) -> Any:
            # Do not show DeprecatedWarning on ObjectModel update (function called by update_from_json)
            frame = inspect.currentframe()
            if frame is not None and frame.f_back is not None:
                if frame.f_back.f_code.co_name not in ["_update_from_json", "update_from_json"]:
                    warnings.warn(
                        f"Call to deprecated function {func.__name__}(). {instructions}",
                        DeprecatedWarning,
                        stacklevel=2,
                    )
            return func(*args, **kwargs)

        return deprecated_func  # type: ignore[return-value]

    return decorator  # type: ignore[return-value]


def preserve_builtin(data: Optional[JSONObj]) -> JSONObj:
    """Add a trailing underscore to parameters using built-in name
    when unpacking parameters directly from JSON imported data
    to avoid name shadowing. e.g: type => type_"""
    if data is None:
        return {}
    reserved_keys = ["format", "global", "id", "license", "max", "min", "None", "type"]
    return {f"{k}_" if k in reserved_keys else k: v for k, v in data.items()}


def snake_to_camel(s: str, first_lower: bool = True, keep_acronyms: bool = True) -> str:
    """Convert a snake case string to camel case string
    :param s: The string to convert from
    :param first_lower: Wheter the first character is returned as lower case or not
    :param keep_acronyms: Wheter acronyms should be kept uppercase or not
    :returns: The string in CamelCase format"""
    res = "".join(w if w.isupper() and keep_acronyms else w.title() for w in s.split("_"))
    return f"{res[0].lower()}{res[1:]}" if first_lower and len(res) else res
