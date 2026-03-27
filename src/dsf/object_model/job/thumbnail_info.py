from enum import Enum

from ..model_object import ModelObject
from ..utils import model_prop, nullable_model_prop


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

    # Base64-encoded thumbnail or null if invalid or not requested
    data = nullable_model_prop("data", str)

    # Format of this thumbnail
    format = model_prop("format", ThumbnailInfoFormat, ThumbnailInfoFormat.PNG)

    # Height of this thumbnail
    height = model_prop("height", int, 0)

    # File offset of this thumbnail
    offset = model_prop("offset", int, 0)

    # Size of this thumbnail
    size = model_prop("size", int, 0)

    # Width of this thumbnail
    width = model_prop("width", int, 0)

    def __init__(self):
        super().__init__()
