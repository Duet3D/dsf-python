from typing import List, Union

from ..model_object import ModelObject


class BuildObject(ModelObject):
    """Information about a detected build object"""

    def __init__(self):
        super().__init__()
        # Indicates if this build object is cancelled
        self._canceled = False
        # Name of the build object (if any)
        self._name = None
        # X coordinates of the build object (in mm or null if not found)
        self._x = None
        # Y coordinates of the build object (in mm or null if not found)
        self._y = None

    @property
    def canceled(self) -> bool:
        """Indicates if this build object is cancelled"""
        return self._canceled

    @canceled.setter
    def canceled(self, value):
        self._canceled = bool(value)

    @property
    def name(self) -> Union[str, None]:
        """Name of the build object (if any)"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value) if value is not None else None

    @property
    def x(self) -> Union[List[float], None]:
        """X coordinates of the build object (in mm or null if not found)"""
        return self._x

    @property
    def y(self) -> Union[List[float], None]:
        """Y coordinates of the build object (in mm or null if not found)"""
        return self._y

    def _update_from_json(self, **kwargs) -> 'BuildObject':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(BuildObject, self)._update_from_json(**kwargs)
        self._x = [float(coord) for coord in kwargs.get('x', [])]
        self._y = [float(coord) for coord in kwargs.get('y', [])]
        return self
