from datetime import datetime
from enum import Enum
from typing import List


class ThumbnailInfoFormat(str, Enum):
    """Image formats for parsed thumbnails"""

    JPEG = "jpeg"
    PNG = "png"
    QOI = "qoi"

    @staticmethod
    def list():
        return list(map(lambda cc: cc.value, ThumbnailInfoFormat))


class ThumbnailInfo:
    """Information about a thumbnail from a G-code file"""

    def __init__(
            self,
            data: str,
            format: ThumbnailInfoFormat,
            height: int,
            offset: int,
            size: int,
            width: int):
        self.data = data
        self.format = ThumbnailInfoFormat(format)
        self.height = height
        self.offset = offset
        self.size = size
        self.width = width


class GCodeFileInfo:
    """Holds information about a parsed G-code file"""

    @classmethod
    def from_json(cls, data):
        """Deserialize an instance of this class from JSON deserialized dictionary"""
        return cls(**data)

    def __init__(
        self,
        filament: List[float],
        fileName: str,
        generatedBy: str,
        height: float,
        lastModified: str,
        layerHeight: float,
        numLayers: int,
        printTime: int,
        simulatedTime: int,
        size: int,
        thumbnails: List[dict]
    ):
        self.filament = filament
        self.file_name = fileName
        self.generated_by = generatedBy
        self.height = height
        self.last_modified = datetime.fromisoformat(lastModified)
        self.layer_height = layerHeight
        self.num_layers = numLayers
        self.print_time = printTime
        self.simulated_time = simulatedTime
        self.size = size
        self.thumbnails = [ThumbnailInfo(**t) for t in thumbnails]
