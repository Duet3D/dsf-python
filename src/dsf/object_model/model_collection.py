from enum import Enum
from typing import Generic, TypeVar, List, Dict, Any, Union, Optional, get_origin, get_args, cast
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
    
    def __init__(self, item_constructor: type[T] | object, value: Optional[List[T]] = None, allow_none: bool = False) -> None:
        """
        :param item_constructor: Item constructor type that items must derive from
        :param value: Value used to initialize the list from
        :param allow_none: Whether list items may be None
        """
        from .utils import is_model_object

        super().__init__()
        self._declared_item_constructor = item_constructor
        item_origin = get_origin(item_constructor)
        item_args = get_args(item_constructor)
        self._allow_none = allow_none or (item_origin in (Union, getattr(__import__('types'), 'UnionType', Union)) and type(None) in item_args)

        resolved_constructor: object = item_constructor
        if item_origin in (Union, getattr(__import__('types'), 'UnionType', Union)):
            non_none_args = [arg for arg in item_args if arg is not type(None)]
            if len(non_none_args) == 1:
                resolved_constructor = non_none_args[0]
                self._runtime_model_type = cast(type[object], get_origin(non_none_args[0]) or non_none_args[0])
            else:
                self._runtime_model_type = object
        else:
            self._runtime_model_type = cast(type[object], item_origin or item_constructor)

        if isinstance(resolved_constructor, type):
            self._item_constructor: type[T] = cast(type[T], resolved_constructor)
        elif isinstance(self._runtime_model_type, type):
            self._item_constructor = cast(type[T], self._runtime_model_type)
        else:
            self._item_constructor = cast(type[T], object)

        if value is not None:
            self[:] = []
            for (_, item) in enumerate(value):
                if item is None:
                    self.append(self._coerce_item_value(item))
                    continue

                if isinstance(item, self._runtime_model_type):
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

    def _coerce_item_value(self, value: JSONElement) -> T:
        """Coerce scalar/enum values using the declared item constructor when possible."""
        if value is None:
            if self._allow_none:
                return cast(T, None)
            raise TypeError(f"None is not allowed for collection of type {self._declared_item_constructor}")

        if issubclass(self._runtime_model_type, Enum):
            try:
                return self._item_constructor(value)
            except (TypeError, ValueError, KeyError):
                raise ValueError(f"Invalid enum value {value} for collection of type {self._runtime_model_type.__name__}")

        try:
            return self._item_constructor(value)
        except (TypeError, ValueError):
            return cast(T, value)

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
            if new_item_data is None and self._allow_none:
                self[i] = None
                continue

            # If the current item is null then we need to create a new item
            if current_item is None:
                if isinstance(new_item_data, self._runtime_model_type):
                    self[i] = cast(T, new_item_data)
                else:
                    ref_item: Optional[T] = None
                    try:
                        ref_item = self._item_constructor()
                    except TypeError:
                        ref_item = None

                    if ref_item is not None and is_model_object(ref_item):
                        self[i] = cast(T, cast(ModelType[JSONElement], ref_item).update_from_json(new_item_data))
                    else:
                        self[i] = self._coerce_item_value(new_item_data)
            # Use the `update_from_json` method of the current item if it's a model object, otherwise replace it with the new data
            elif is_model_object(current_item):
                self[i] = cast(T, cast(ModelType[JSONElement], current_item).update_from_json(new_item_data))
            else:
                self[i] = self._coerce_item_value(new_item_data)

        # Add new items
        for i in range(len(self), len(data)):
            item_to_add = data[i]
            if item_to_add is None:
                self.append(self._coerce_item_value(item_to_add))
            elif isinstance(item_to_add, self._runtime_model_type):
                self.append(cast(T, item_to_add))
            else:
                ref_item: Optional[T] = None
                try:
                    ref_item = self._item_constructor()
                except TypeError:
                    ref_item = None

                if ref_item is not None and is_model_object(ref_item):
                    self.append(cast(ModelType[JSONElement], ref_item).update_from_json(item_to_add))
                else:
                    self.append(self._coerce_item_value(item_to_add))


        return self
