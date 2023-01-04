from __future__ import annotations

from .build_object import BuildObject
from ..model_collection import ModelCollection
from ..model_object import ModelObject


class Build(ModelObject):
    """Information about the current build"""
    def __init__(self):
        super().__init__()
        # Index of the current object being printed or -1 if unknown
        self._current_object = -1
        # Whether M486 names are being used
        self._m486_names = False
        # Whether M486 numbers are being used
        self._m486_numbers = False
        # List of detected build objects
        self._objects = ModelCollection(BuildObject)

    @property
    def current_object(self) -> int:
        """Index of the current object being printed or -1 if unknown
        This value may not be greater than the length of the job.build.objects array.
        This is because the size of job.build.objects is limited to conserve memory (to 20 on Duet 2 or 40 on Duet 3),
        whereas when M486 labelling is used, many more objects can be numbered
        and the first 64 can be cancelled individually"""
        return self._current_object

    @current_object.setter
    def current_object(self, value: int):
        self._current_object = int(value)

    @property
    def m486_names(self) -> bool:
        """Whether M486 names are being used"""
        return self._m486_names

    @m486_names.setter
    def m486_names(self, value: bool):
        self._m486_names = bool(value)

    @property
    def m486_numbers(self) -> bool:
        """Whether M486 numbers are being used"""
        return self._m486_numbers

    @m486_numbers.setter
    def m486_numbers(self, value: bool):
        self._m486_numbers = bool(value)

    @property
    def objects(self) -> list[BuildObject]:
        """List of detected build objects"""
        return self._objects
