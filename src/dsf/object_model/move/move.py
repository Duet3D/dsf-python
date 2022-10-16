from typing import List

from .axis import Axis
from .current_move import CurrentMove
from .extruder import Extruder
from .kinematics import Kinematics
from .input_shaping import InputShaping
from .move_calibration import MoveCalibration
from .move_compensation import MoveCompensation
from .motors_idle_control import MotorsIdleControl
from .move_queue_item import MoveQueueItem
from .move_rotation import MoveRotation
from ..model_object import ModelObject


class Move(ModelObject):
    """Information about the move subsystem"""
    def __init__(self):
        super().__init__()
        # List of the configured axes
        self._axes = []
        # Information about the automatic calibration
        self._calibration = MoveCalibration()
        # Information about the currently configured compensation options
        self._compensation = MoveCompensation()
        # Information about the current move
        self._current_move = CurrentMove()
        # List of configured extruders
        self._extruders = []
        # Idle current reduction parameters
        self._idle = MotorsIdleControl()
        # Configured kinematics options
        self._kinematics = Kinematics()
        # Limit axis positions by their minima and maxima
        self._limit_axes = True
        # Indicates if standard moves are forbidden if the corresponding axis is not homed
        self._no_moves_before_homing = True
        # Maximum acceleration allowed while printing (in mm/s^2)
        self._printing_acceleration = 10000
        # List of move queue items (DDA rings)
        self._queue = []
        # Parameters for centre rotation
        self._rotation = MoveRotation()
        # Parameters for input shaping
        self._shaping = InputShaping()
        # Speed factor applied to every regular move (0.01..1 or greater)
        self._speed_factor = 1
        # Maximum acceleration allowed while travelling (in mm/s^2)
        self._travel_acceleration = 0
        # Virtual total extruder position
        self._virtual_e_pos = 0
        # Index of the currently selected workplace
        self._workplace_number = 0

    @property
    def axes(self) -> List[Axis]:
        """List of the configured axes
        See Axis()"""
        return self._axes

    @property
    def calibration(self) -> MoveCalibration:
        """Information about the automatic calibration"""
        return self._calibration

    @property
    def compensation(self) -> MoveCompensation:
        """Information about the currently configured compensation options"""
        return self._compensation

    @property
    def current_move(self) -> CurrentMove:
        """Information about the current move"""
        return self._current_move

    @property
    def extruders(self) -> List[Extruder]:
        """List of configured extruders
        See Extruder()"""
        return self._extruders

    @property
    def idle(self) -> MotorsIdleControl:
        """Idle current reduction parameters"""
        return self._idle

    @property
    def kinematics(self) -> Kinematics:
        """Configured kinematics options"""
        return self._kinematics

    @kinematics.setter
    def kinematics(self, value):
        if value is None or isinstance(value, Kinematics):
            self._kinematics = value
        elif isinstance(value, dict):  # Update from JSON
            self._kinematics = Kinematics.from_json(value)
        else:
            raise TypeError(f"{__name__}.kinematics must be of type Kinematics. Got {type(value)}: {value}")

    @property
    def limit_axes(self) -> bool:
        """Limit axis positions by their minima and maxima"""
        return self._limit_axes

    @limit_axes.setter
    def limit_axes(self, value):
        self._limit_axes = bool(value)

    @property
    def no_moves_before_homing(self) -> bool:
        """Indicates if standard moves are forbidden if the corresponding axis is not homed"""
        return self._no_moves_before_homing

    @no_moves_before_homing.setter
    def no_moves_before_homing(self, value):
        self._no_moves_before_homing = bool(value)

    @property
    def printing_acceleration(self) -> float:
        """Maximum acceleration allowed while printing (in mm/s^2)"""
        return self._printing_acceleration

    @printing_acceleration.setter
    def printing_acceleration(self, value):
        self._printing_acceleration = float(value) if value is not None else 10000

    @property
    def queue(self) -> List[MoveQueueItem]:
        """List of move queue items (DDA rings)"""
        return self._queue

    @property
    def rotation(self) -> MoveRotation:
        """Parameters for centre rotation"""
        return self._rotation

    @property
    def shaping(self) -> InputShaping:
        """Parameters for input shaping"""
        return self._shaping

    @property
    def speed_factor(self) -> float:
        """Speed factor applied to every regular move (0.01..1 or greater)"""
        return self._speed_factor

    @speed_factor.setter
    def speed_factor(self, value):
        self._speed_factor = float(value) if value is not None else 1

    @property
    def travel_acceleration(self) -> float:
        """Maximum acceleration allowed while travelling (in mm/s^2)"""
        return self._travel_acceleration

    @travel_acceleration.setter
    def travel_acceleration(self, value):
        self._travel_acceleration = float(value) if value is not None else 0

    @property
    def virtual_e_pos(self) -> float:
        """Virtual total extruder position"""
        return self._virtual_e_pos

    @virtual_e_pos.setter
    def virtual_e_pos(self, value):
        self._virtual_e_pos = float(value) if value is not None else 0

    @property
    def workplace_number(self) -> int:
        """Index of the currently selected workplace"""
        return self._workplace_number

    @workplace_number.setter
    def workplace_number(self, value):
        self._workplace_number = int(value) if value is not None else 0

    def _update_from_json(self, **kwargs) -> 'Move':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(Move, self)._update_from_json(**kwargs)
        self._axes = [Axis.from_json(axis) for axis in kwargs.get('axes', [])]
        self._calibration = MoveCalibration.from_json(kwargs.get('calibration'))
        self._compensation = MoveCompensation.from_json(kwargs.get('compensation'))
        self._current_move = CurrentMove.from_json(kwargs.get('currentMove'))
        self._extruders = [Extruder.from_json(e) for e in kwargs.get('extruders', [])]
        self._idle = MotorsIdleControl.from_json(kwargs.get('idle'))
        self._queue = [MoveQueueItem.from_json(item) for item in kwargs.get('queue', [])]
        self._rotation = MoveRotation.from_json(kwargs.get('rotation'))
        self._shaping = InputShaping.from_json(kwargs.get('shaping'))
        return self
