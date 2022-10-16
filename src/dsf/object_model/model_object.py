import json
from datetime import datetime
from typing import Union

from ..utility.driver_id import DriverId
from ..utils import preserve_builtin, camel_to_snake, snake_to_camel


class FloatJSON(float):
    # Remove trailing zeros from float numbers
    __repr__ = staticmethod(lambda o: f'{o:g}')


json.encoder.c_make_encoder = None
json.encoder.float = FloatJSON


class ModelObject:
    """Base class for object model classes"""

    def __init__(self, *args, **kwargs):
        pass

    def __str__(self, **kwargs):
        """Serialize this instance of this class into a JSON dictionary"""
        return json.dumps(self, default=self.__json_serialize, sort_keys=True, **kwargs)

    @staticmethod
    def __json_serialize(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, DriverId):
            return str(obj)
        if isinstance(obj, float):
            return f'{obj:g}'

        # Convert snake_case class attributes into CamelCase JSON style
        # also convert back 'globals' to 'global'
        return {snake_to_camel(k if k != '_globals' else '_global'): v for k, v in obj.__dict__.items()}

    def _update_from_json(self, **kwargs) -> 'ModelObject':
        """Update this instance from a given JSON element
        This method iterate over all writeable properties to update them.
        It means classes with get-only properties should override this method in order to update them.
        """
        # Get the class writeable properties including from inherited classes
        # (the ones which have a setter -> fset property object attribute)
        cls_dict = {attr: getattr(self.__class__, attr) for attr in dir(self.__class__)}
        writeable_properties = [attr for attr, value in cls_dict.items()
                                if isinstance(value, property) and value.fset is not None]
        for name, value in kwargs.items():
            # Convert JSON attributes from CamelCase to snake_case to satisfy python PEP8 naming
            # Remove trailing underscore set by preserve_builtin()
            name_snake = camel_to_snake(name.rstrip('_'))
            if name_snake in writeable_properties:
                setattr(self, name_snake, value)
        return self

    @classmethod
    def from_json(cls, data: Union[dict, str]) -> 'ModelObject':
        """Deserialize a new instance of this class from JSON deserialized dictionary"""
        # Deserialize a string object into a JSON (dict) object
        if isinstance(data, str):
            data = json.loads(data)
        return cls()._update_from_json(**preserve_builtin(data))

    def update(self, data: Union[dict, str]):
        """Update the current instance of this class from JSON deserialized dictionary"""
        if isinstance(data, str):
            data = json.loads(data)
        return self._update_from_json(**preserve_builtin(data))

    def to_json(self) -> str:
        """Serialize this instance of this class into a JSON dictionary"""
        return self.__str__()
