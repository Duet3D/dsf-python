from datetime import datetime
from typing import List, Sequence

from .thumbnail_info import ThumbnailInfo
from ..model_collection import ModelCollection
from ..model_object import ModelObject


class GCodeFileInfo(ModelObject):
    """Holds information about a parsed G-code file"""

    def __init__(self) -> None:
        super().__init__()
        self._custom_info: dict[str, object] = {}
        self._filament: List[float] = []
        self._file_name: str | None = ""
        self._generated_by: str | None = ""
        self._height: float = 0
        self._last_modified: datetime | None = None
        self._layer_height: float = 0
        self._num_layers: int = 0
        self._print_time: int | None = None
        self._simulated_time: int | None = None
        self._size: int | None = 0
        self._thumbnails: ModelCollection[ThumbnailInfo] = ModelCollection(ThumbnailInfo)

    @property
    def custom_info(self) -> dict[str, object]:
        """Custom information extracted from the G-code file"""
        return self._custom_info

    @property
    def filament(self) -> List[float]:
        """Filament consumption per extruder drive (in mm)"""
        return self._filament

    @property
    def file_name(self) -> str | None:
        """The filename of the G-code file"""
        return self._file_name

    @file_name.setter
    def file_name(self, value: str | None):
        self._file_name = str(value) if value is not None else None

    @property
    def generated_by(self) -> str | None:
        """Name of the application that generated this file"""
        return self._generated_by

    @generated_by.setter
    def generated_by(self, value: str | None):
        self._generated_by = str(value) if value is not None else None

    @property
    def height(self) -> float:
        """Build height of the G-code job or 0 if not found (in mm)"""
        return self._height

    @height.setter
    def height(self, value: float | int | str):
        self._height = float(value)

    @property
    def last_modified(self) -> datetime | None:
        """Value indicating when the file was last modified or null if unknown"""
        return self._last_modified

    @last_modified.setter
    def last_modified(self, value: datetime | str | None):
        if isinstance(value, datetime) or value is None:
            self._last_modified = value
        elif isinstance(value, str):
            self._last_modified = datetime.fromisoformat(value)
        else:
            raise TypeError(f"{__name__}.last_modified must be of type datetime or None. Got {type(value)}: {value}")

    @property
    def layer_height(self) -> float:
        """Height of each other layer or 0 if not found (in mm)"""
        return self._layer_height

    @layer_height.setter
    def layer_height(self, value: float | int | str):
        self._layer_height = float(value)

    @property
    def num_layers(self) -> int:
        """Number of total layers or 0 if unknown"""
        return self._num_layers

    @num_layers.setter
    def num_layers(self, value: int | str):
        self._num_layers = int(value)

    @property
    def print_time(self) -> int | None:
        """Estimated print time (in s)"""
        return self._print_time

    @print_time.setter
    def print_time(self, value: int | str | None):
        self._print_time = int(value) if value is not None else None

    @property
    def simulated_time(self) -> int | None:
        """Estimated print time from G-code simulation (in s)"""
        return self._simulated_time

    @simulated_time.setter
    def simulated_time(self, value: int | str | None):
        self._simulated_time = int(value) if value is not None else None

    @property
    def size(self) -> int | None:
        """Size of the file"""
        return self._size

    @size.setter
    def size(self, value: int | str | None):
        self._size = int(value) if value is not None else None

    @property
    def thumbnails(self) -> Sequence[ThumbnailInfo | None]:
        """Collection of thumbnails parsed from Gcode"""
        return self._thumbnails
