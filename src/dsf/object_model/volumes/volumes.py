from typing import Union

from ..model_object import ModelObject


class Volume(ModelObject):
    """Information about a storage device"""

    def __init__(self):
        super().__init__()
        # Total capacity of the storage device (in bytes or null)
        self._capacity = None
        # How much space is still available on this device (in bytes or null)
        self._free_space = None
        # Whether the storage device is mounted
        self._mounted = None
        # Name of this volume
        self._name = None
        # Number of currently open files or null if unknown
        self._open_files = None
        # Total size of this volume (in bytes or null)
        self._partition_size = None
        # Logical path of the storage device
        self._path = None
        # Speed of the storage device (in bytes/s or null if unknown)
        self._speed = None
        
    @property
    def capacity(self) -> Union[int, None]:
        """Total capacity of the storage device (in bytes or null)"""
        return self._capacity
    
    @capacity.setter
    def capacity(self, value):
        self._capacity = int(value) if value is not None else None
        
    @property
    def free_space(self) -> Union[int, None]:
        """How much space is still available on this device (in bytes or null)"""
        return self._free_space
    
    @free_space.setter
    def free_space(self, value):
        self._free_space = int(value) if value is not None else None
        
    @property
    def mounted(self) -> bool:
        """Whether the storage device is mounted"""
        return self._mounted
    
    @mounted.setter
    def mounted(self, value):
        self._mounted = bool(value)
    
    @property
    def name(self) -> Union[str, None]:
        """Name of this volume"""
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = str(value) if value is not None else None
    
    @property
    def open_files(self) -> Union[int, None]:
        """Number of currently open files or null if unknown"""
        return self._open_files
    
    @open_files.setter
    def open_files(self, value):
        self._open_files = int(value) if value is not None else None
        
    @property
    def partition_size(self) -> Union[int, None]:
        """Total size of this volume (in bytes or null)"""
        return self._partition_size
    
    @partition_size.setter
    def partition_size(self, value):
        self._partition_size = int(value) if value is not None else None
        
    @property
    def path(self) -> Union[str, None]:
        """Logical path of the storage device"""
        return self._path
    
    @path.setter
    def path(self, value):
        self._path = str(value) if value is not None else None
        
    @property
    def speed(self) -> Union[int, None]:
        """Speed of the storage device (in bytes/s or null if unknown)"""
        return self._speed
    
    @speed.setter
    def speed(self, value):
        self._speed = int(value) if value is not None else None
