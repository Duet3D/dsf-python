from __future__ import annotations

from ..model_object import ModelObject


class TimesLeft(ModelObject):
    """Estimations about the times left"""

    def __init__(self):
        super().__init__()
        # Time left based on filament consumption (in s or null)
        self._filament = None
        # Time left based on file progress (in s or null)
        self._file = None
        # Time left based on the slicer reports (see M73, in s or null)
        self._slicer = None

    @property
    def filament(self) -> int | None:
        """Time left based on filament consumption (in s or null)"""
        return self._filament

    @filament.setter
    def filament(self, value: int | None = None):
        self._filament = int(value) if value is not None else None

    @property
    def file(self) -> int | None:
        """Time left based on file progress (in s or null)"""
        return self._file

    @file.setter
    def file(self, value: int | None = None):
        self._file = int(value) if value is not None else None

    @property
    def slicer(self) -> int | None:
        """Time left based on the slicer reports (see M73, in s or null)"""
        return self._slicer

    @slicer.setter
    def slicer(self, value: int | None = None):
        self._slicer = int(value) if value is not None else None
