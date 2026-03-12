import json
from datetime import datetime
from typing import Optional, Self


from .utils import is_model_object
from ..utils import preserve_builtin, camel_to_snake, snake_to_camel


class FloatJSON(float):
    # Remove trailing zeros from float numbers
    def __repr__(self) -> str:
        return f'{self:g}'


setattr(json.encoder, "c_make_encoder", None)
setattr(json.encoder, "float", FloatJSON)


class ModelObject:
    """Base class for object model classes"""

    def __init__(self, *args: object, **kwargs: object) -> None:
        pass

    def __str__(
        self,
        *,
        skipkeys: bool = False,
        ensure_ascii: bool = True,
        check_circular: bool = True,
        allow_nan: bool = True,
        cls: Optional[type[json.JSONEncoder]] = None,
        indent: Optional[int | str] = None,
        separators: Optional[tuple[str, str]] = None,
    ) -> str:
        """Serialize this instance of this class into a JSON dictionary"""
        return json.dumps(
            self,
            default=self.__json_serialize,
            sort_keys=True,
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            cls=cls,
            indent=indent,
            separators=separators,
        )

    @staticmethod
    def __json_serialize(obj: object) -> object:
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

    def _update_from_json(self, **kwargs: object) -> Self:
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
    def from_json(cls, data: dict[str, object] | str) -> Self:
        """Deserialize a new instance of this class from JSON deserialized dictionary"""
        # Deserialize a string object into a JSON (dict) object
        json_data: dict[str, object]
        if isinstance(data, str):
            json_data = json.loads(data)
        else:
            json_data = data
        return cls()._update_from_json(**preserve_builtin(json_data))

    def update_from_json(self, data: dict[str, object] | str) -> Self:
        """Update the current instance of this class from JSON deserialized dictionary"""
        json_data: dict[str, object]
        if isinstance(data, str):
            json_data = json.loads(data)
        else:
            json_data = data
        return self._update_from_json(**preserve_builtin(json_data))

    def to_json(self) -> str:
        """Serialize this instance of this class into a JSON dictionary"""
        return self.__str__()
