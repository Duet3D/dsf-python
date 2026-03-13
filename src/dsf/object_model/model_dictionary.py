from typing import Optional, TypeVar, Self

from .model_object import TModelObject
from .model_type import ModelType
from ..utils import JSONObj, JSONElement, preserve_builtin

T = TypeVar("T")


class ModelDictionary(ModelType[JSONObj], JSONObj):
    """
    Class for storing model object items in a dictionary
    Useful for updating model object items from JSON data (patches)
    """

    def __init__(self, null_deletes_keys: bool, item_constructor: Optional[type[TModelObject]] = None, value: Optional[JSONObj | TModelObject] = None):
        """
        :param null_deletes_keys: Whether setting null to items effectively deletes them
        :param item_constructor: Item constructor type to use for type-checking
        :param value: Value used to initialize the dictionary from
        """
        super().__init__()
        self._item_constructor = item_constructor
        self._null_deletes_keys = null_deletes_keys

        if value is not None:
            if not isinstance(value, dict):
                raise TypeError(f"value must be of type dict or None. Got {type(value)}: {value}")
            for k, v in value.items():
                self[k] = v

    def __setitem__(self, key: str, value: JSONElement) -> Self | None:
        from .utils import is_model_object

        if value is None:
            if self._null_deletes_keys:
                self.pop(key, None)
                return self
            return super().__setitem__(key, value)

        current_item = self.get(key)
        if current_item is None and self._item_constructor:
            new_item = self._item_constructor()
            if is_model_object(new_item):
                if not isinstance(value, dict):
                    raise TypeError(f"Value for key '{key}' must be of type dict to update the model object. Got {type(value)}: {value}")
                updated_item = new_item.update_from_json(value)
                return super().__setitem__(key, updated_item)
            else:
                ref_item = self._item_constructor()
                new_item = ref_item.update_from_json(value)
                return super().__setitem__(key, new_item)
        elif is_model_object(current_item):
            new_item = current_item.update_from_json(value)
            return super().__setitem__(key, new_item)

        return super().__setitem__(key, value)

    @classmethod
    def from_json(cls, data: JSONObj):
        """Deserialize a new instance of this class from JSON deserialized dictionary"""
        return cls().update_from_json(**preserve_builtin(data))

    def update_from_json(self, data: JSONObj):
        if data is None:
            super().clear()
        else:
            for k, v in data.items():
                self[k] = v
        return self
