from typing import Generic, Optional, Protocol, Self, TypeVar, cast

from .utils import is_model_object


class _ModelItem(Protocol):
    def update_from_json(self, data: dict[str, object] | str) -> Self:
        ...


T = TypeVar("T", bound=_ModelItem)


class ModelDictionary(dict[str, T | None], Generic[T]):
    """
    Class for storing model object items in a dictionary
    Useful for updating model object items from JSON data (patches)
    """

    def __init__(self, null_deletes_keys: bool, item_constructor: type[T] | None = None, value: dict[str, object] | None = None):
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

    def __setitem__(self, key: str, value: object) -> None:
        if value is None:
            if self._null_deletes_keys:
                self.pop(key, None)
                return
            super().__setitem__(key, None)
            return

        current_item = self.get(key)
        if current_item is None and self._item_constructor:
            new_item = self._item_constructor()
            if is_model_object(new_item):
                if not isinstance(value, (dict, str)):
                    raise TypeError(f"Invalid model dictionary value: {type(value)}")
                updated_item = new_item.update_from_json(value)
                super().__setitem__(key, updated_item)
                return
            else:
                ref_item = self._item_constructor()
                if not isinstance(value, (dict, str)):
                    raise TypeError(f"Invalid model dictionary value: {type(value)}")
                new_item = ref_item.update_from_json(value)
                super().__setitem__(key, new_item)
                return
        elif is_model_object(current_item):
            if not isinstance(value, (dict, str)):
                raise TypeError(f"Invalid model dictionary value: {type(value)}")
            new_item = cast(T, current_item).update_from_json(value)
            super().__setitem__(key, new_item)
            return

        super().__setitem__(key, cast(T, value))

    def update_from_json(self, json_element: dict[str, object] | None) -> "ModelDictionary[T]":
        if json_element is None:
            super().clear()
        else:
            for k, v in json_element.items():
                self[k] = v
        return self
