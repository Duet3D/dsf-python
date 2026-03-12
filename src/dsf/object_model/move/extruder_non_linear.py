from ..model_object import ModelObject


class ExtruderNonlinear(ModelObject):
    """Nonlinear extrusion parameters (see M592)"""

    def __init__(self) -> None:
        super().__init__()
        # A coefficient in the extrusion formula
        self._a: float = 0
        # B coefficient in the extrusion formula
        self._b: float = 0
        self._upper_limit: float = 0.2

    @property
    def a(self) -> float:
        """A coefficient in the extrusion formula"""
        return self._a

    @a.setter
    def a(self, value: float | int | str):
        self._a = float(value)

    @property
    def b(self) -> float:
        """B coefficient in the extrusion formula"""
        return self._b

    @b.setter
    def b(self, value: float | int | str):
        self._b = float(value)

    @property
    def upper_limit(self) -> float:
        """Upper limit of the nonlinear extrusion compensation"""
        return self._upper_limit

    @upper_limit.setter
    def upper_limit(self, value: float | int | str):
        self._upper_limit = float(value)
