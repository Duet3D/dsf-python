import json
from datetime import datetime
from typing import Union


from .utils import is_model_object
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
        from .plugins.sbc_permissions import SbcPermissions
        from .move import DriverId

        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, float):
            return f'{obj:g}'
        if isinstance(obj, SbcPermissions):
            return obj.name
        if isinstance(obj, DriverId):
            return str(obj)

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
        instance_attributes = vars(self)
        for json_key, json_value in kwargs.items():
            # Convert JSON attributes from CamelCase to snake_case to satisfy python PEP8 naming
            # Remove trailing underscore set by preserve_builtin()
            json_key_snake = camel_to_snake(json_key.rstrip('_'))
            # Write public attributes by using their setter property
            if json_key_snake in writeable_properties:
                attr = getattr(self, json_key_snake)
                if is_model_object(attr):
                    new_value = attr.update_from_json(json_value)
                    setattr(self, json_key_snake, new_value)
                else:
                    setattr(self, json_key_snake, json_value)
            # Write protected attributes
            elif f"_{json_key_snake}" in instance_attributes:
                # Protected (non-writeable) attributes are prefixed by an underscore
                attr_name = f"_{json_key_snake}"
                attr = getattr(self, attr_name)
                if is_model_object(attr):
                    setattr(self, attr_name, attr.update_from_json(json_value))
                elif isinstance(attr, list):
                    setattr(self, attr_name, json_value)
        return self

    @classmethod
    def from_json(cls, data: Union[dict, str]) -> 'ModelObject':
        """Deserialize a new instance of this class from JSON deserialized dictionary"""
        # Deserialize a string object into a JSON (dict) object
        if isinstance(data, str):
            data = json.loads(data)
        return cls()._update_from_json(**preserve_builtin(data))

    def update_from_json(self, data: Union[dict, str]):
        """Update the current instance of this class from JSON deserialized dictionary"""
        if isinstance(data, str):
            data = json.loads(data)
        return self._update_from_json(**preserve_builtin(data))

    def to_json(self) -> str:
        """Serialize this instance of this class into a JSON dictionary"""
        return self.__str__()
