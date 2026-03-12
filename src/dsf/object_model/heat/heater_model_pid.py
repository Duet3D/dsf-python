from ..model_object import ModelObject


class HeaterModelPID(ModelObject):
    """Details about the PID model of a heater"""

    def __init__(self) -> None:
        super().__init__()
        # Derivative value of the PID regulator
        self._d: float = 0
        # Integral value of the PID regulator
        self._i: float = 0
        # Indicates if custom PID values are used
        self._overridden: bool = False
        # Proportional value of the PID regulator
        self._p: float = 0
        # Indicates if PID control is being used
        self._used: bool = True

    @property
    def d(self) -> float:
        """Derivative value of the PID regulator"""
        return self._d

    @d.setter
    def d(self, value: float | int | str):
        self._d = float(value)

    @property
    def i(self) -> float:
        """Integral value of the PID regulator"""
        return self._i

    @i.setter
    def i(self, value: float | int | str):
        self._i = float(value)

    @property
    def overridden(self) -> bool:
        """Indicates if custom PID values are used"""
        return self._overridden

    @overridden.setter
    def overridden(self, value: bool | int | str):
        self._overridden = bool(value)

    @property
    def p(self) -> float:
        """Proportional value of the PID regulator"""
        return self._p

    @p.setter
    def p(self, value: float | int | str):
        self._p = float(value)

    @property
    def used(self) -> bool:
        """Indicates if PID control is being used"""
        return self._used

    @used.setter
    def used(self, value: bool | int | str):
        self._used = bool(value)
