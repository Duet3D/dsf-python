from ..model_object import ModelObject
from ..utils import nullable_model_prop, model_prop


class Volume(ModelObject):
    """Information about a storage device"""

    # Total capacity of the storage device (in bytes or null)
    capacity = nullable_model_prop('capacity', int)
    
    # How much space is still available on this device (in bytes or null)
    free_space = nullable_model_prop('free_space', int)
    
    # Whether the storage device is mounted
    mounted = model_prop('mounted', bool)
    
    # Name of this volume
    name = nullable_model_prop('name', str)
    
    # Whether any file is open on this volume or null if unknown
    open_files = nullable_model_prop('open_files', bool)
    
    # Total size of this volume (in bytes or null)
    partition_size = nullable_model_prop('partition_size', int)
    
    # Logical path of the storage device
    path = nullable_model_prop('path', str)
    
    # Speed of the storage device (in bytes/s or null if unknown)
    speed = nullable_model_prop('speed', int)

    def __init__(self):
        super().__init__()
