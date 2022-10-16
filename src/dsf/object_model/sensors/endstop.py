from .endstop_type import EndstopType
from ..model_object import ModelObject


class Endstop(ModelObject):
    """Information about an endstop"""

    def __init__(self):
        super(Endstop, self).__init__()
        self._high_end = None
        self._triggered = None
        self._type = None

    @property
    def high_end(self) -> bool:
        """Whether this endstop is at the high end of the axis"""
        return self._high_end

    @high_end.setter
    def high_end(self, value):
        self._high_end = bool(value)

    @property
    def triggered(self) -> bool:
        """Whether or not the endstop is hit"""
        return self._triggered

    @triggered.setter
    def triggered(self, value):
        self._triggered = bool(value)

    @property
    def type(self) -> EndstopType:
        """Type of the endstop"""
        return self._type

    @type.setter
    def type(self, value):
        if value is None or isinstance(value, EndstopType):
            self._type = value
        elif isinstance(value, str):
            self._type = EndstopType(value)
        else:
            raise TypeError(f"{__name__}.type must be of type EndstopType or None. Got {type(value)}: {value}")
