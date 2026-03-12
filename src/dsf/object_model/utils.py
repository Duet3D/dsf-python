from typing import Protocol, Self, TypeVar, cast


def is_model_object(o: object) -> bool:
    from .model_object import ModelObject
    from .model_collection import ModelCollection
    from .model_dictionary import ModelDictionary

    return isinstance(o, ModelObject) or isinstance(o, ModelCollection) or isinstance(o, ModelDictionary)


class _WrappedModel(Protocol):
    @classmethod
    def from_json(cls, data: dict[str, object]) -> Self:
        ...

    def update_from_json(self, data: dict[str, object] | str) -> Self:
        ...


T = TypeVar('T', bound=_WrappedModel)  # Type variable for model objects


def wrap_model_property(name: str, model_type: type[T]) -> property:
    """
    Wrap a nullable model object property so that type checks can be performed during update
    :param name: Property of the derived class
    :param model_type: Constructor for creating new elements
    :return:
    """

    STORAGE_NAME = '_' + name

    @property
    def prop(self) -> T | None:
        return getattr(self, STORAGE_NAME)

    @prop.setter
    def prop(self, value: T | str | dict[str, object] | None) -> None:
        if value is None or isinstance(value, model_type):
            setattr(self, STORAGE_NAME, value)
        elif isinstance(value, dict):  # Update from JSON
            current_value = getattr(self, STORAGE_NAME)
            if current_value is None:
                setattr(self, STORAGE_NAME, model_type.from_json(value))
            else:
                cast(T, current_value).update_from_json(value)
        elif isinstance(value, str):
            current_value = getattr(self, STORAGE_NAME)
            if current_value is None:
                setattr(self, STORAGE_NAME, model_type().update_from_json(value))
            else:
                cast(T, current_value).update_from_json(value)
        else:
            raise TypeError(f"{self.__class__.__name__}.{name} must be None or of type {model_type.__name__}."
                            f" Got {type(value).__name__}: {value}")

    return prop
