from datetime import datetime
from typing import Optional, Protocol, TypeVar, Union, Callable, cast, get_origin, overload

from .model_object import ModelObject
from .model_collection import ModelCollection
from .model_dictionary import ModelDictionary
from ..utils import JSONObj, JSONElement


_TProperty = TypeVar("_TProperty", covariant=True)


class TypedReadableProperty(Protocol[_TProperty]):
    @overload
    def __get__(self, obj: None, objtype: Optional[type[object]] = None) -> "TypedReadableProperty[_TProperty]":
        ...

    @overload
    def __get__(self, obj: object, objtype: Optional[type[object]] = None) -> _TProperty:
        ...


T = TypeVar("T")


def is_model_object(o: object) -> bool:
    from .model_object import ModelObject
    from .model_collection import ModelCollection
    from .model_dictionary import ModelDictionary

    return isinstance(o, ModelObject) or isinstance(o, ModelCollection) or isinstance(o, ModelDictionary)


def _set_model_prop(instance: object, name: str, runtime_type: type[JSONElement | datetime], current_value: T, value: Union[T, JSONElement]):
    if isinstance(value, dict):  # Update from JSON
        if not isinstance(current_value, (ModelObject, ModelDictionary)):
            raise TypeError(f"{instance.__class__.__name__}.{name} must be of type ModelObject or ModelDictionary to update from a dict."
                            f" Got {type(current_value).__name__}: {current_value}")
        current_value.update_from_json(cast(JSONObj, value))
    elif isinstance(value, list):
        if not isinstance(current_value, ModelCollection):
            raise TypeError(f"{instance.__class__.__name__}.{name} must be of type ModelCollection to update from a list."
                            f" Got {type(current_value).__name__}: {current_value}")
        current_value.update_from_json(cast(list[JSONElement], value))
    elif runtime_type is datetime and isinstance(value, str):
        try:
            parsed_date = datetime.fromisoformat(value)
            setattr(instance, name, parsed_date)
        except ValueError:
            raise TypeError(f"{instance.__class__.__name__}.{name} must be a valid ISO format datetime string to update from JSON. Got: {value}")
    elif isinstance(value, (str, int, float, bool)):
        value = runtime_type(value) # ignore type
        setattr(instance, name, value)
    else:
        raise TypeError(f"{instance.__class__.__name__}.{name} must be of type {runtime_type} or a compatible JSON element to update from."
                        f" Got {type(value).__name__}: {value}")

def model_prop(name: str, model_type: type[T], default: Optional[T] = None) -> TypedReadableProperty[T]:
    """
    Wrap a none nullable model object property so that type checks can be performed during update
    :param name: Property of the derived class
    :param model_type: Constructor for creating new elements
    :param default: Default value of type to use if not set during update from JSON, if None then the default constructor of the model is used
    :return:
    """

    STORAGE_NAME = '_' + name
    runtime_model_type = cast(type[object], get_origin(model_type) or model_type)

    # For mutable types (ModelObject, ModelCollection, ModelDictionary), always create per-instance.
    # For immutable scalar defaults, the scalar value is safe to share.
    _scalar_default: Optional[T] = default
    _use_factory = default is None and issubclass(runtime_model_type, (ModelObject, ModelCollection, ModelDictionary))

    if not _use_factory and default is None:
        _scalar_default = model_type()

    def _make_default() -> T:
        return model_type() if _use_factory else cast(T, _scalar_default)

    @property
    def prop(self: object) -> T:
        v = getattr(self, STORAGE_NAME, None)
        if v is None:
            v = _make_default()
            setattr(self, STORAGE_NAME, v)
        return v

    @prop.setter
    def prop(self: object, value: Union[T, JSONElement]) -> None:
        def get_or_create_value() -> T:
            current_value: Optional[T] = getattr(self, STORAGE_NAME, None)
            if current_value is None:
                current_value = _make_default()
                setattr(self, STORAGE_NAME, current_value)
            return current_value

        if isinstance(value, runtime_model_type):
            setattr(self, STORAGE_NAME, value)
            return
        
        current_value = get_or_create_value()
        _set_model_prop(self, STORAGE_NAME, runtime_model_type, current_value, value)

    return cast(TypedReadableProperty[T], prop)

def nullable_model_prop(name: str, model_type: type[T], constructor: Optional[Callable[[], T]] = None) -> TypedReadableProperty[Optional[T]]:
    """
    Wrap a nullable model object property so that type checks can be performed during update
    :param name: Property of the derived class
    :param model_type: Constructor for creating new elements
    :param constructor: Optional constructor for creating new elements
    :return: TypedReadableProperty[Optional[T]]
    """

    STORAGE_NAME = '_' + name
    runtime_model_type = cast(type[object], get_origin(model_type) or model_type)
    model_type_name = getattr(runtime_model_type, "__name__", str(model_type))

    if constructor is None:
        try:
            model_type()  # validate that the default constructor works
        except Exception:
            raise TypeError(f"Default constructor failed for type {model_type_name}. Provide a constructor function to create default values for the property {name}.")
        _factory: Callable[[], Optional[T]] = model_type
    else:
        _factory = constructor

    @property
    def prop(self: object) -> Optional[T]:
        return getattr(self, STORAGE_NAME, None)

    @prop.setter
    def prop(self: object, value: Union[T, JSONElement, None]) -> None:
        def get_or_create_value() -> Optional[T]:
            v = getattr(self, STORAGE_NAME, None)
            if v is None:
                new_val = _factory()
                if new_val is not None:
                    setattr(self, STORAGE_NAME, new_val)
            return getattr(self, STORAGE_NAME, None)

        if value is None or isinstance(value, runtime_model_type):
            setattr(self, STORAGE_NAME, value)
            return

        current_value = get_or_create_value()
        _set_model_prop(self, STORAGE_NAME, runtime_model_type, current_value, value)

    return cast(TypedReadableProperty[Optional[T]], prop)
