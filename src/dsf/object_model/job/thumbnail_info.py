from __future__ import annotations
from enum import Enum

from ..model_object import ModelObject


class ThumbnailInfoFormat(str, Enum):
    """Image formats for parsed thumbnails"""

    JPEG = "jpeg"
    PNG = "png"
    QOI = "qoi"

    @staticmethod
    def list():
        return list(map(lambda cc: cc.value, ThumbnailInfoFormat))


class ThumbnailInfo(ModelObject):
    """Information about a thumbnail from a G-code file"""

    def __init__(self):
        super().__init__()
        # Base64-encoded thumbnail or null if invalid or not requested
        self._data = None
        # Format of this thumbnail
        self._format = ThumbnailInfoFormat.PNG
        # Height of this thumbnail
        self._height = 0
        # File offset of this thumbnail
        self._offset = 0
        # Size of this thumbnail
        self._size = 0
        # Width of this thumbnail
        self._width = 0

    @property
    def data(self) -> str | None:
        """Base64-encoded thumbnail or null if invalid or not requested
        This property is not provided by RepRapFirmware fileinfo results,
        and it may be null if no thumbnail content is requested"""
        return self._data

    @data.setter
    def data(self, value: str | None = None):
        self._data = str(value) if value is not None else None

    @property
    def format(self) -> ThumbnailInfoFormat:
        """Format of this thumbnail"""
        return self._format

    @format.setter
    def format(self, value: ThumbnailInfoFormat):
        if isinstance(value, ThumbnailInfoFormat):
            self._format = value
        elif isinstance(value, str):
            self._format = ThumbnailInfoFormat(value)
        else:
            raise TypeError(f"{__name__}.format must be of type ThumbnailInfoFormat."
                            f" Got {type(value)}: {value}")

    @property
    def height(self) -> int:
        """Height of this thumbnail"""
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = int(value)

    @property
    def offset(self) -> int:
        """File offset of this thumbnail"""
        return self._offset

    @offset.setter
    def offset(self, value: int):
        self._offset = int(value)

    @property
    def size(self) -> int:
        """Size of this thumbnail"""
        return self._size

    @size.setter
    def size(self, value: int):
        self._size = int(value)

    @property
    def width(self) -> int:
        """Width of this thumbnail"""
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = int(value)
