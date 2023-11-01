from __future__ import annotations

from ...model_object import ModelObject


class TiltCorrection(ModelObject):
    """Tilt correction parameters for Z leadscrew compensation"""
    def __init__(self):
        super().__init__()
        # Correction factor
        self._correction_factor = 0
        # Last corrections (in mm)
        self._last_corrections = []
        # Maximum Z correction (in mm)
        self._max_correction = 0
        # Pitch of the Z leadscrews (in mm)
        self._screw_pitch = 0
        # X positions of the leadscrews (in mm)
        self._screw_x = []
        # Y positions of the leadscrews (in mm)
        self._screw_y = []
        
    @property
    def correction_factor(self) -> float:
        """Correction factor"""
        return self._correction_factor
    
    @correction_factor.setter
    def correction_factor(self, value: float):
        self._correction_factor = float(value)
        
    @property
    def last_corrections(self) -> list[float]:
        """Last corrections (in mm)"""
        return self._last_corrections

    @property
    def max_correction(self) -> float:
        """Maximum Z correction (in mm)"""
        return self._max_correction

    @max_correction.setter
    def max_correction(self, value: float):
        self._max_correction = float(value)

    @property
    def screw_pitch(self) -> float:
        """Pitch of the Z leadscrews (in mm)"""
        return self._screw_pitch

    @screw_pitch.setter
    def screw_pitch(self, value: float):
        self._screw_pitch = float(value)
        
    @property
    def screw_x(self) -> list[float]:
        """X positions of the leadscrews (in mm)"""
        return self._screw_x
    
    @property
    def screw_y(self) -> list[float]:
        """Y positions of the leadscrews (in mm)"""
        return self._screw_y
