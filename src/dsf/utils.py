import inspect
import re
import warnings

from types import UnionType
from typing import Any, Optional, Callable, TypeVar, TypeAlias, Union, get_args, get_origin, cast, overload

# We don't want our deprecations to be ignored by default, so create our own type.
class DeprecatedWarning(UserWarning):
    pass


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
        typed_value = cast(dict[Any, Any], value)
        return all(_matches_type(k, key_type) and _matches_type(v, val_type) for k, v in typed_value.items())

    if origin is list:
        if not isinstance(value, list):
            return False
        if len(args) != 1:
            return True
        typed_value = cast(list[Any], value)
        return all(_matches_type(item, args[0]) for item in typed_value)

    if origin is tuple:
        if not isinstance(value, tuple):
            return False
        typed_value = cast(tuple[Any, ...], value)
        if len(args) == 2 and args[1] is Ellipsis:
            return all(_matches_type(item, args[0]) for item in typed_value)
        if len(args) != len(typed_value):
            return False
        return all(_matches_type(item, item_type) for item, item_type in zip(typed_value, args))

    if origin is set:
        if not isinstance(value, set):
            return False
        if len(args) != 1:
            return True
        typed_value = cast(set[Any], value)
        return all(_matches_type(item, args[0]) for item in typed_value)

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
    snake = re.sub(r'((?<=[a-z])[A-Z0-9]|(?!^)[A-Z0-9](?=[a-z]))', r'_\1', s)
    return '_'.join(w if w.isupper() else w.lower() for w in snake.split('_')) if keep_acronyms else snake.lower()


F = TypeVar('F', bound=Callable[..., Any])


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
                if frame.f_back.f_code.co_name not in ['_update_from_json', 'update_from_json']:
                    warnings.warn(f"Call to deprecated function {func.__name__}(). {instructions}",
                                  DeprecatedWarning, stacklevel=2)
            return func(*args, **kwargs)
        return deprecated_func  # type: ignore[return-value]
    return decorator  # type: ignore[return-value]


def preserve_builtin(data: Optional[JSONObj]) -> JSONObj:
    """Add a trailing underscore to parameters using built-in name
    when unpacking parameters directly from JSON imported data
    to avoid name shadowing. e.g: type => type_"""
    if data is None:
        return {}
    reserved_keys = ['format', 'global', 'id', 'license', 'max', 'min', 'None', 'type']
    return {f"{k}_" if k in reserved_keys else k: v for k, v in data.items()}


def snake_to_camel(s: str, first_lower: bool = True, keep_acronyms: bool = True) -> str:
    """Convert a snake case string to camel case string
    :param s: The string to convert from
    :param first_lower: Wheter the first character is returned as lower case or not
    :param keep_acronyms: Wheter acronyms should be kept uppercase or not
    :returns: The string in CamelCase format"""
    res = ''.join(w if w.isupper() and keep_acronyms else w.title() for w in s.split('_'))
    return f'{res[0].lower()}{res[1:]}' if first_lower and len(res) else res
