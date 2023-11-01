from ..model_object import ModelObject


class HeaterModelPID(ModelObject):
    """Details about the PID model of a heater"""

    def __init__(self):
        super().__init__()
        # Derivative value of the PID regulator
        self._d = 0
        # Integral value of the PID regulator
        self._i = 0
        # Indicates if custom PID values are used
        self._overridden = False
        # Proportional value of the PID regulator
        self._p = 0
        # Indicates if PID control is being used
        self._used = True

    @property
    def d(self) -> float:
        """Derivative value of the PID regulator"""
        return self._d

    @d.setter
    def d(self, value: float):
        self._d = float(value)

    @property
    def i(self) -> float:
        """Integral value of the PID regulator"""
        return self._i

    @i.setter
    def i(self, value: float):
        self._i = float(value)

    @property
    def overridden(self) -> bool:
        """Indicates if custom PID values are used"""
        return self._overridden

    @overridden.setter
    def overridden(self, value: bool):
        self._overridden = bool(value)

    @property
    def p(self) -> float:
        """Proportional value of the PID regulator"""
        return self._p

    @p.setter
    def p(self, value: float):
        self._p = float(value)

    @property
    def used(self) -> bool:
        """Indicates if PID control is being used"""
        return self._used

    @used.setter
    def used(self, value: bool):
        self._used = bool(value)
