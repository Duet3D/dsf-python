from typing import Optional, Sequence

from .axis import Axis
from .current_move import CurrentMove
from .extruder import Extruder
from .keepout_zone import KeepoutZone
from .kinematics import Kinematics
from .input_shaping import InputShaping
from .move_calibration import MoveCalibration
from .move_compensation import MoveCompensation
from .motors_idle_control import MotorsIdleControl
from .move_queue_item import MoveQueueItem
from .move_rotation import MoveRotation
from ..model_collection import ModelCollection
from ..model_object import ModelObject


class Move(ModelObject):
    """Information about the move subsystem"""

    def __init__(self) -> None:
        super().__init__()
        # List of the configured axes
        self._axes: ModelCollection[Axis] = ModelCollection(Axis)
        # Backlash distance multiplier
        self._backlash_factor: int = 10
        # Information about the automatic calibration
        self._calibration: MoveCalibration = MoveCalibration()
        # Information about the currently configured compensation options
        self._compensation: MoveCompensation = MoveCompensation()
        # Information about the current move
        self._current_move: CurrentMove = CurrentMove()
        # List of configured extruders
        self._extruders: ModelCollection[Extruder] = ModelCollection(Extruder)
        # Idle current reduction parameters
        self._idle: MotorsIdleControl = MotorsIdleControl()
        # List of configured keep-out zones
        self._keepout: ModelCollection[KeepoutZone] = ModelCollection(KeepoutZone)
        # Configured kinematics options
        self._kinematics: Kinematics = Kinematics()
        # Limit axis positions by their minima and maxima
        self._limit_axes: bool = True
        # Indicates if standard moves are forbidden if the corresponding axis is not homed
        self._no_moves_before_homing: bool = True
        # Maximum acceleration allowed while printing (in mm/s^2)
        self._printing_acceleration: float = 10000
        # List of move queue items (DDA rings)
        self._queue: ModelCollection[MoveQueueItem] = ModelCollection(MoveQueueItem)
        # Parameters for centre rotation
        self._rotation: MoveRotation = MoveRotation()
        # Parameters for input shaping
        self._shaping: InputShaping = InputShaping()
        # Speed factor applied to every regular move (0.01..1 or greater)
        self._speed_factor: float = 1
        # Maximum acceleration allowed while travelling (in mm/s^2)
        self._travel_acceleration: float = 0
        # Indicates if third-order S-curve acceleration is enabled
        self._s_curve_acceleration: bool = False
        # Virtual total extruder position
        self._virtual_e_pos: float = 0
        # Index of the currently selected workplace
        self._workplace_number: int = 0

    @property
    def axes(self) -> Sequence[Optional[Axis]]:
        """List of the configured axes
        See Axis()"""
        return self._axes

    @property
    def backlash_factor(self) -> int:
        """Backlash distance multiplier"""
        return self._backlash_factor

    @backlash_factor.setter
    def backlash_factor(self, value: int | str):
        self._backlash_factor = int(value)

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
    def extruders(self) -> Sequence[Optional[Extruder]]:
        """List of configured extruders
        See Extruder()"""
        return self._extruders

    @property
    def idle(self) -> MotorsIdleControl:
        """Idle current reduction parameters"""
        return self._idle

    @property
    def keepout(self) -> Sequence[Optional[KeepoutZone]]:
        """List of configured keep-out zones"""
        return self._keepout

    @property
    def kinematics(self) -> Kinematics:
        """Configured kinematics options"""
        return self._kinematics

    @property
    def limit_axes(self) -> bool:
        """Limit axis positions by their minima and maxima"""
        return self._limit_axes

    @limit_axes.setter
    def limit_axes(self, value: bool | int | str):
        self._limit_axes = bool(value)

    @property
    def no_moves_before_homing(self) -> bool:
        """Indicates if standard moves are forbidden if the corresponding axis is not homed"""
        return self._no_moves_before_homing

    @no_moves_before_homing.setter
    def no_moves_before_homing(self, value: bool | int | str):
        self._no_moves_before_homing = bool(value)

    @property
    def printing_acceleration(self) -> float:
        """Maximum acceleration allowed while printing (in mm/s^2)"""
        return self._printing_acceleration

    @printing_acceleration.setter
    def printing_acceleration(self, value: float | int | str):
        self._printing_acceleration = float(value)

    @property
    def queue(self) -> Sequence[Optional[MoveQueueItem]]:
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
    def speed_factor(self, value: float | int | str):
        self._speed_factor = float(value)

    @property
    def travel_acceleration(self) -> float:
        """Maximum acceleration allowed while travelling (in mm/s^2)"""
        return self._travel_acceleration

    @travel_acceleration.setter
    def travel_acceleration(self, value: float | int | str):
        self._travel_acceleration = float(value)

    @property
    def s_curve_acceleration(self) -> bool:
        """Indicates if third-order S-curve acceleration is enabled"""
        return self._s_curve_acceleration

    @s_curve_acceleration.setter
    def s_curve_acceleration(self, value: bool):
        self._s_curve_acceleration = bool(value)

    @property
    def virtual_e_pos(self) -> float:
        """Virtual total extruder position"""
        return self._virtual_e_pos

    @virtual_e_pos.setter
    def virtual_e_pos(self, value: float | int | str):
        self._virtual_e_pos = float(value)

    @property
    def workplace_number(self) -> int:
        """Index of the currently selected workplace"""
        return self._workplace_number

    @workplace_number.setter
    def workplace_number(self, value: int | str):
        self._workplace_number = int(value)
