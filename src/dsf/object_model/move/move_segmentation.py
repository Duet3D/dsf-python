from ..model_object import ModelObject
from ..utils import model_prop


class MoveSegmentation(ModelObject):
    """Move segmentation parameters"""

    segments_per_sec = model_prop("segments_per_sec", float, 0.0)
    min_seg_length = model_prop("min_segment_length", float, 0.0)

    def __init__(self):
        super().__init__()
