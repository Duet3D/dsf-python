from typing import Generic, Protocol, Self, TypeVar, Type, List, Optional, cast
from .utils import is_model_object


class _ModelItem(Protocol):
    def update_from_json(self, data: dict[str, object] | str) -> Self:
        ...


T = TypeVar('T', bound=_ModelItem)


class ModelCollection(Generic[T], list[T | None]):
    """
    Class for storing model object items in a list
    Useful for updating model object items from JSON data (patches)
    """
    
    def __init__(self, item_constructor: Type[T], value: Optional[List[object]] = None) -> None:
        """
        :param item_constructor: Item constructor type that items must derive from
        :param value: Value used to initialize the list from
        """
        super().__init__()
        self._item_constructor: Type[T] = item_constructor

        if value is not None:
            self[:] = []
            for (i, item) in enumerate(value):
                if item is None:
                    self.append(None)
                elif isinstance(item, self._item_constructor):
                    self.append(item)
                else:
                    ref_item = self._item_constructor()
                    if isinstance(item, (dict, str)):
                        ref_item.update_from_json(item)
                        self.append(ref_item)
                    else:
                        raise TypeError(f"Invalid model collection item: {type(item)}")

    def update_from_json(self, json_element: List[object]) -> 'ModelCollection[T]':
        """
        Update this instance from the given data
        :param json_element: JSON data to upgrade this instance from
        :return: Updated instance
        """
        if not isinstance(json_element, list):
            raise Exception(f"Invalid JSON element type for model collection {type(json_element)}.")

        # Remove deleted items
        self[:] = self[:len(json_element)]

        # Update existing items
        for i in range(0, min(len(self), len(json_element))):
            current_item = self[i]
            if current_item is None:
                new_item = json_element[i]
                if isinstance(new_item, self._item_constructor):
                    self[i] = new_item
                elif new_item is None:
                    self[i] = None
                else:
                    ref_item = self._item_constructor()
                    if isinstance(new_item, (dict, str)):
                        self[i] = ref_item.update_from_json(new_item)
                    else:
                        raise TypeError(f"Invalid model collection item: {type(new_item)}")
            elif is_model_object(current_item):
                json_item = json_element[i]
                if json_item is None:
                    self[i] = None
                elif isinstance(json_item, (dict, str)):
                    self[i] = cast(T, current_item).update_from_json(json_item)
                elif isinstance(json_item, self._item_constructor):
                    self[i] = json_item
                else:
                    raise TypeError(f"Invalid model collection patch item: {type(json_item)}")
            else:
                json_item = json_element[i]
                if json_item is None:
                    self[i] = None
                elif isinstance(json_item, self._item_constructor):
                    self[i] = json_item
                elif isinstance(json_item, (dict, str)):
                    self[i] = cast(T, current_item).update_from_json(json_item)
                else:
                    raise TypeError(f"Invalid model collection patch item: {type(json_item)}")

        # Add new items
        for i in range(len(self), len(json_element)):
            item_to_add = json_element[i]
            if item_to_add is None:
                self.append(None)
            elif isinstance(item_to_add, self._item_constructor):
                self.append(item_to_add)
            elif isinstance(item_to_add, (dict, str)):
                self.append(self._item_constructor().update_from_json(item_to_add))
            else:
                raise TypeError(f"Invalid model collection item: {type(item_to_add)}")

        return self
