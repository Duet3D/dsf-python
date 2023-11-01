from .scanner_status import ScannerStatus
from ..model_object import ModelObject


class Scanner(ModelObject):
    """Information about the 3D scanner subsystem"""

    def __init__(self):
        super().__init__()
        # Progress of the current action (on a scale between 0 and 1)
        self._progress = 0
        # Status of the 3D scanner
        self._status = ScannerStatus.disconnected

    @property
    def progress(self) -> float:
        """Progress of the current action (on a scale between 0 and 1)
        Previous status responses used a scale of 0..100"""
        return self._progress
    
    @progress.setter
    def progress(self, value: float):
        self._progress = float(value)
        
    @property
    def status(self) -> ScannerStatus:
        """Status of the 3D scanner
        See also ScannerStatus"""
        return self._status
    
    @status.setter
    def status(self, value: ScannerStatus = ScannerStatus.disconnected):
        if isinstance(value, str):
            self._status = ScannerStatus(value)
        elif isinstance(value, ScannerStatus):
            self._status = value
        else:
            raise TypeError(f"{__name__}.status must be of type ScannerStatus."
                            f" Got {type(value)}: {value}")
