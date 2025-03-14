from typing import Type, TypeVar, Any, Union, Dict


def is_model_object(o):
    from .model_object import ModelObject
    from .model_collection import ModelCollection
    from .model_dictionary import ModelDictionary

    return isinstance(o, ModelObject) or isinstance(o, ModelCollection) or isinstance(o, ModelDictionary)


T = TypeVar('T')  # Type variable for model objects


def wrap_model_property(name: str, model_type: Type[T]) -> Union[Type[T], None]:
    """
    Wrap a nullable model object property so that type checks can be performed during update
    :param name: Property of the derived class
    :param model_type: Constructor for creating new elements
    :return:
    """

    STORAGE_NAME = '_' + name

    @property
    def prop(self) -> Union[Type[T], None]:
        return getattr(self, STORAGE_NAME)

    @prop.setter
    def prop(self, value: Union[Type[T], str, Dict[str, Any], None]):
        if value is None or isinstance(value, model_type):
            setattr(self, STORAGE_NAME, value)
        elif isinstance(value, dict):  # Update from JSON
            current_value = getattr(self, STORAGE_NAME)
            if current_value is None:
                setattr(self, STORAGE_NAME, model_type.from_json(value))
            else:
                current_value.update_from_json(value)
        elif isinstance(value, str):
            current_value = getattr(self, STORAGE_NAME)
            if current_value is None:
                setattr(self, STORAGE_NAME, model_type().update_from_json(value))
            else:
                current_value.update_from_json(value)
        else:
            raise TypeError(f"{self.__class__.__name__}.{name} must be None or of type {model_type.__name__}."
                            f" Got {type(value).__name__}: {value}")

    return prop
