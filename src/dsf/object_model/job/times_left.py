from ..model_object import ModelObject


class TimesLeft(ModelObject):
    """Estimations about the times left"""

    def __init__(self) -> None:
        super().__init__()
        # Time left based on filament consumption (in s or null)
        self._filament: int | None = None
        # Time left based on file progress (in s or null)
        self._file: int | None = None
        # Time left based on the slicer reports (see M73, in s or null)
        self._slicer: int | None = None
        # Time left before the next colour change is expected (see M73 C, in s or null)
        self._to_pause: int | None = None

    @property
    def filament(self) -> int | None:
        """Time left based on filament consumption (in s or null)"""
        return self._filament

    @filament.setter
    def filament(self, value: int | str | None):
        self._filament = int(value) if value is not None else None

    @property
    def file(self) -> int | None:
        """Time left based on file progress (in s or null)"""
        return self._file

    @file.setter
    def file(self, value: int | str | None):
        self._file = int(value) if value is not None else None

    @property
    def slicer(self) -> int | None:
        """Time left based on the slicer reports (see M73, in s or null)"""
        return self._slicer

    @slicer.setter
    def slicer(self, value: int | str | None):
        self._slicer = int(value) if value is not None else None

    @property
    def to_pause(self) -> int | None:
        """Time left before the next colour change is expected (see M73 C, in s or null)"""
        return self._to_pause

    @to_pause.setter
    def to_pause(self, value: int | str | None):
        self._to_pause = int(value) if value is not None else None
