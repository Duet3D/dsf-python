from typing import Generic, TypeVar, Type, List, Dict, Any, Union, Optional
from .utils import is_model_object

T = TypeVar('T')


class ModelCollection(Generic[T], list):
    """
    Class for storing model object items in a list
    Useful for updating model object items from JSON data (patches)
    """
    
    def __init__(self, item_constructor: Type[T], value: Optional[List[T]] = None) -> None:
        """
        :param item_constructor: Item constructor type that items must derive from
        :param value: Value used to initialize the list from
        """
        super().__init__()
        self._item_constructor: Type[T] = item_constructor

        if value is not None:
            self[:] = []
            for (i, item) in enumerate(value):
                if isinstance(item, self._item_constructor):
                    self.append(item)
                else:
                    ref_item = self._item_constructor()
                    ref_item.update_from_json(item)
                    self.append(ref_item)

    def update_from_json(self, json_element: List[Any]) -> 'ModelCollection[T]':
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
                else:
                    ref_item = self._item_constructor()
                    self[i] = ref_item.update_from_json(new_item)
            elif is_model_object(current_item):
                self[i] = current_item.update_from_json(json_element[i])
            else:
                self[i] = json_element[i]

        # Add new items
        for i in range(len(self), len(json_element)):
            item_to_add = json_element[i]
            if item_to_add is None or not isinstance(item_to_add, dict):
                self.append(item_to_add)
            else:
                self.append(self._item_constructor().update_from_json(item_to_add))

        return self
