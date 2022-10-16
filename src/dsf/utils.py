import functools
import inspect
import re
import warnings


# We don't want our deprecations to be ignored by default, so create our own type.
class DeprecatedWarning(UserWarning):
    pass


def camel_to_snake(s: str, keep_acronyms: bool = True) -> str:
    """Convert a camel case string to snake case string
    :param s: The string to convert from
    :param keep_acronyms: Wheter acronyms should be kept uppercase or not
    :returns: The string in snake_case format"""
    # Added a look-behind (?!^) so initials like SBC are not getting snake-cased
    snake = re.sub(r'((?<=[a-z])[A-Z0-9]|(?!^)[A-Z0-9](?=[a-z]))', r'_\1', s)
    return '_'.join(w if w.isupper() else w.lower() for w in snake.split('_')) if keep_acronyms else snake.lower()


def deprecated(instructions: str):
    """Flags a function/method as deprecated.
    :param instructions: A human-friendly string of instructions
    """
    def decorator(func):
        """This is a decorator which can be used to mark functions as deprecated.
        It will result in a warning being emitted when the function is used."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            frame = inspect.currentframe().f_back
            warnings.warn_explicit(f"Call to deprecated function {func.__name__}. {instructions}",
                                   category=DeprecatedWarning,
                                   filename=inspect.getfile(frame.f_code),
                                   lineno=frame.f_lineno)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def preserve_builtin(data: dict) -> dict:
    """Add a trailing underscore to parameters using built-in name
    when unpacking parameters directly from JSON imported data
    to avoid name shadowing. e.g: type => type_"""
    if data is None:
        return {}
    reserved_keys = ['format', 'global', 'id', 'license', 'max', 'min', 'None', 'type']
    return {f"{k}_" if k in reserved_keys else k: v for k, v in data.items()}


def snake_to_camel(s: str, first_lower=True, keep_acronyms: bool = True) -> str:
    """Convert a snake case string to camel case string
    :param s: The string to convert from
    :param first_lower: Wheter the first character is returned as lower case or not
    :param keep_acronyms: Wheter acronyms should be kept uppercase or not
    :returns: The string in CamelCase format"""
    res = ''.join(w if w.isupper() and keep_acronyms else w.title() for w in s.split('_'))
    return f'{res[0].lower()}{res[1:]}' if first_lower and len(res) else res
