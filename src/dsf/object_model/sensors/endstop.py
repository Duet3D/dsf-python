from .endstop_type import EndstopType
from ..model_object import ModelObject


class Endstop(ModelObject):
    """Information about an endstop"""

    def __init__(self) -> None:
        super(Endstop, self).__init__()
        self._high_end: bool | None = None
        self._probe: int | None = None
        self._triggered: bool | None = None
        self._type: EndstopType | None = None

    @property
    def high_end(self) -> bool | None:
        """Whether this endstop is at the high end of the axis"""
        return self._high_end

    @high_end.setter
    def high_end(self, value: bool | int | str):
        self._high_end = bool(value)

    @property
    def probe(self) -> int | None:
        """Number of the referenced probe if type is ZProbeAsEndstop, else None"""
        return self._probe

    @probe.setter
    def probe(self, value: int | str | None):
        self._probe = int(value) if value is not None else None

    @property
    def triggered(self) -> bool | None:
        """Whether the endstop is hit"""
        return self._triggered

    @triggered.setter
    def triggered(self, value: bool | int | str):
        self._triggered = bool(value)

    @property
    def type(self) -> EndstopType | None:
        """Type of the endstop"""
        return self._type

    @type.setter
    def type(self, value: EndstopType | str | None):
        if value is None or isinstance(value, EndstopType):
            self._type = value
        elif isinstance(value, str):
            self._type = EndstopType(value)
        else:
            raise TypeError(f"{__name__}.type must be of type EndstopType or None. Got {type(value)}: {value}")
