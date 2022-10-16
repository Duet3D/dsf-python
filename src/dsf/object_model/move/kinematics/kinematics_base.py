from typing import Union

from .kinematics_name import KinematicsName
from ..move_segmentation import MoveSegmentation
from ...model_object import ModelObject


class KinematicsBase(ModelObject):
    """Information about the configured geometry"""

    def __init__(self, name: KinematicsName = KinematicsName.unknown):
        super().__init__()
        self._name = name
        self._segmentation = None

    @property
    def name(self) -> KinematicsName:
        """Name of the configured kinematics"""
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, KinematicsName):
            self._name = value
        elif isinstance(value, str):
            self._name = KinematicsName(value)
        else:
            raise TypeError(f"{__name__}.name must be of type KinematicsName. Got {type(value)}: {value}")

    @property
    def segmentation(self) -> Union[MoveSegmentation, None]:
        """Segmentation parameters or null if not configured"""
        return self._segmentation

    def _update_from_json(self, **kwargs) -> 'ModelObject':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(KinematicsBase, self)._update_from_json(**kwargs)
        segmentation = kwargs.get('segmentation')
        self._segmentation = MoveSegmentation.from_json(segmentation) if segmentation else None
        return self
