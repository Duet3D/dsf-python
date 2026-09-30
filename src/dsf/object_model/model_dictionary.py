from typing import Any, Optional, Self, TYPE_CHECKING, cast

from .model_type import ModelType
from ..utils import JSONObj

if TYPE_CHECKING:
    from .model_object import ModelObject


class ModelDictionary(ModelType[JSONObj], dict[str, Any]):
    """
    Class for storing model object items in a dictionary
    Useful for updating model object items from JSON data (patches)
    """

    def __init__(
        self,
        null_deletes_keys: bool,
        item_constructor: Optional[type["ModelObject"]] = None,
        value: Optional[dict[str, Any]] = None,
    ):
        """
        :param null_deletes_keys: Whether setting null to items effectively deletes them
        :param item_constructor: Item constructor type to use for type-checking
        :param value: Value used to initialize the dictionary from
        """
        super().__init__()
        self._item_constructor = item_constructor
        self._null_deletes_keys = null_deletes_keys

        if value is not None:
            for k, v in value.items():
                self[k] = v

    def __setitem__(self, key: str, value: Any) -> None:
        from .utils import is_model_object

        if value is None:
            if self._null_deletes_keys:
                self.pop(key, None)
                return
            return super().__setitem__(key, value)

        current_item = self.get(key)
        if current_item is None and self._item_constructor:
            if not isinstance(value, dict):
                raise TypeError(
                    f"Value for key '{key}' must be of type dict to update the model object."
                    f" Got {type(value)}: {value}"
                )
            new_item = self._item_constructor()
            return super().__setitem__(key, new_item.update_from_json(cast(JSONObj, value)))
        elif is_model_object(current_item):
            return super().__setitem__(key, current_item.update_from_json(value))

        return super().__setitem__(key, value)

    @classmethod
    def from_json(cls, data: Optional[JSONObj]) -> Self:
        """Deserialize a new instance of this class from JSON deserialized dictionary"""
        return cls(False).update_from_json(data)

    def update_from_json(self, data: Optional[JSONObj]) -> Self:
        if data is None:
            super().clear()
        else:
            for k, v in data.items():
                self[k] = v
        return self
