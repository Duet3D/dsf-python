from ..model_object import ModelObject


class MoveSegmentation(ModelObject):
    """Move segmentation parameters"""
    def __init__(self):
        super().__init__()
        self._segments_per_sec = 0
        self._min_segment_length = 0
        
    @property
    def segments_per_sec(self) -> int:
        """Number of segments per second"""
        return self._segments_per_sec
    
    @segments_per_sec.setter
    def segments_per_sec(self, value):
        self._segments_per_sec = int(value) if value is not None else 0
        
    @property
    def min_segment_length(self) -> float:
        """Minimum length of a segment (in mm)"""
        return self._min_segment_length
    
    @min_segment_length.setter
    def min_segment_length(self, value):
        self._min_segment_length = float(value) if value is not None else 0
