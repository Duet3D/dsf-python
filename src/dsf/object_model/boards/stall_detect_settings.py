from ..model_object import ModelObject


class StallDetectSettings(ModelObject):
    """Information about stall detection"""
    def __init__(self):
        super().__init__()
        # Stall detection threshold
        self._threshold = 0
        # Whether the input values are filtered
        self._filtered = False
        # Minimum steps
        self._min_steps = 0
        # Coolstep register value
        self._coolstep = 0
        # Action to perform when a stall is detected
        self._action = 0

    @property
    def threshold(self) -> int:
        """Stall detection threshold"""
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold = int(value) if value is not None else 0

    @property
    def filtered(self) -> bool:
        """Whether the input values are filtered"""
        return self._filtered

    @filtered.setter
    def filtered(self, value):
        self._filtered = bool(value)

    @property
    def min_steps(self) -> int:
        """Minimum steps"""
        return self._min_steps

    @min_steps.setter
    def min_steps(self, value):
        self._min_steps = int(value) if value is not None else 0

    @property
    def coolstep(self) -> int:
        """Coolstep register value"""
        return self._coolstep

    @coolstep.setter
    def coolstep(self, value):
        self._coolstep = int(value) if value is not None else 0

    @property
    def action(self) -> int:
        """Action to perform when a stall is detected"""
        return self._action

    @action.setter
    def action(self, value):
        self._action = int(value) if value is not None else 0
