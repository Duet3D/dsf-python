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
    def d(self, value):
        self._d = float(value) if value is not None else 0

    @property
    def i(self) -> float:
        """Integral value of the PID regulator"""
        return self._i

    @i.setter
    def i(self, value):
        self._i = float(value) if value is not None else 0

    @property
    def overridden(self) -> bool:
        """Indicates if custom PID values are used"""
        return self._overridden

    @overridden.setter
    def overridden(self, value):
        self._overridden = bool(value)

    @property
    def p(self) -> float:
        """Proportional value of the PID regulator"""
        return self._p

    @p.setter
    def p(self, value):
        self._p = float(value) if value is not None else 0

    @property
    def used(self) -> bool:
        """Indicates if PID control is being used"""
        return self._used

    @used.setter
    def used(self, value):
        self._used = bool(value)
