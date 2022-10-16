from ..model_object import ModelObject


class ExtruderNonlinear(ModelObject):
    """Nonlinear extrusion parameters (see M592)"""
    def __init__(self):
        super().__init__()
        # A coefficient in the extrusion formula
        self._a = 0
        # B coefficient in the extrusion formula
        self._b = 0
        self._upper_limit = 0.2

    @property
    def a(self) -> float:
        """A coefficient in the extrusion formula"""
        return self._a

    @a.setter
    def a(self, value):
        self._a = float(value) if value is not None else 0

    @property
    def b(self) -> float:
        """B coefficient in the extrusion formula"""
        return self._b

    @b.setter
    def b(self, value):
        self._b = float(value) if value is not None else 0

    @property
    def upper_limit(self) -> float:
        """Upper limit of the nonlinear extrusion compensation"""
        return self._upper_limit

    @upper_limit.setter
    def upper_limit(self, value):
        self._upper_limit = float(value) if value is not None else 0.2
