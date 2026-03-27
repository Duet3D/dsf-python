from enum import Enum
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
        from .utils import is_model_object

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
                    if not is_model_object(ref_item):
                        raise TypeError(f"Item constructor for ModelCollection must inherit from type ModelType to update from a dict."
                                        f" Got {type(ref_item).__name__}: {ref_item}")
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
            new_item_data = data[i]
            
            # If the new item data is null, set the current item to null (even if it was a model object before)
            if new_item_data is None:
                self[i] = None
                continue

            # If the current item is null then we need to create a new item
            if current_item is None:
                if isinstance(new_item_data, self._item_constructor):
                    self[i] = new_item_data
                elif issubclass(self._item_constructor, Enum):
                    try:
                        enum_value = self._item_constructor(new_item_data)
                        self.append(enum_value)
                    except KeyError:
                        raise ValueError(f"Invalid enum value {new_item_data} for collection of type {self._item_constructor.__name__}")
                else:
                    ref_item = self._item_constructor()
                    if not is_model_object(ref_item):
                        raise TypeError(f"Item constructor for ModelCollection must inherit from type ModelType to update from a dict."
                                        f" Got {type(ref_item).__name__}: {ref_item}")
                    self[i] = cast(ModelType[JSONElement], ref_item).update_from_json(new_item_data)
            # Use the `update_from_json` method of the current item if it's a model object, otherwise replace it with the new data
            elif is_model_object(current_item):
                self[i] = cast(ModelType[JSONElement], current_item).update_from_json(new_item_data)
            else:
                self[i] = new_item_data

        # Add new items
        for i in range(len(self), len(data)):
            item_to_add = data[i]
            if item_to_add is None:
                self.append(item_to_add)
            elif issubclass(self._item_constructor, Enum):
                try:
                    enum_value = self._item_constructor(item_to_add)
                    self.append(enum_value)
                except KeyError:
                    raise ValueError(f"Invalid enum value {item_to_add} for collection of type {self._item_constructor.__name__}")
            else:
                    
                ref_item = self._item_constructor()
                if is_model_object(ref_item):
                    self.append(cast(ModelType[JSONElement], ref_item).update_from_json(item_to_add))
                else:
                    self.append(item_to_add)


        return self
