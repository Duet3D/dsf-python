from typing import Generic, TypeVar, List, Dict, Any, Union, Optional, get_origin, cast
from ..utils import JSONElement
from .model_type import ModelType
from .model_dictionary import ModelDictionary
from .model_object import ModelObject

T = TypeVar('T')
# T = TypeVar('T', bound=Union[JSONElement, "ModelCollection[Any]", ModelDictionary, ModelObject])


class ModelCollection(ModelType[list[JSONElement]], Generic[T], list[T]):
    """
    Class for storing model object items in a list
    Useful for updating model object items from JSON data (patches)
    """
    
    def __init__(self, item_constructor: type[T], value: Optional[List[T]] = None) -> None:
        """
        :param item_constructor: Item constructor type that items must derive from
        :param value: Value used to initialize the list from
        """
        super().__init__()
        self._item_constructor: type[T] = item_constructor
        self._runtime_model_type = cast(type[object], get_origin(item_constructor) or item_constructor)

        if value is not None:
            self[:] = []
            for (_, item) in enumerate(value):
                if isinstance(item, self._item_constructor):
                    self.append(item)
                else:
                    ref_item = self._item_constructor()
                    # if issubclass(self._item_constructor, ModelType[T]):
                    ref_item.update_from_json(item)

                    self.append(ref_item)

    @classmethod
    def from_json(cls, data: list[JSONElement]):
        raise RuntimeError("from_json is not supported for ModelCollection. Use the constructor instead.")

    def update_from_json(self, data: list[JSONElement]) -> 'ModelCollection[T]':
        """
        Update this instance from the given data
        :param json_element: JSON data to upgrade this instance from
        :return: Updated instance
        """
        from .utils import is_model_object

        if not isinstance(data, list):
            raise Exception(f"Invalid JSON element type for model collection {type(data)}.")

        # Remove deleted items
        self[:] = self[:len(data)]

        # Update existing items
        for i in range(0, min(len(self), len(data))):
            current_item = self[i]
            if current_item is None:
                new_item = data[i]
                if isinstance(new_item, self._item_constructor):
                    self[i] = new_item
                else:
                    ref_item = self._item_constructor()
                    if not is_model_object(ref_item):
                        raise TypeError(f"Item constructor for ModelCollection must inherit from type ModelType to update from a dict."
                                        f" Got {type(ref_item).__name__}: {ref_item}")
                    self[i] = cast(ModelType[JSONElement], ref_item).update_from_json(new_item)
            elif is_model_object(current_item):
                self[i] = cast(ModelType[JSONElement], current_item).update_from_json(data[i])
            else:
                self[i] = data[i]

        # Add new items
        for i in range(len(self), len(data)):
            item_to_add = data[i]
            if item_to_add is None:
                self.append(item_to_add)
            else:
                ref_item = self._item_constructor()
                if is_model_object(ref_item):
                    self.append(cast(ModelType[JSONElement], self._item_constructor()).update_from_json(item_to_add))
                else:
                    self.append(item_to_add)


        return self
