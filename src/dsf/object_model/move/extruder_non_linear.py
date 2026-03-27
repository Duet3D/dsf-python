from ..model_object import ModelObject
from ..utils import model_prop


class ExtruderNonlinear(ModelObject):
    """Nonlinear extrusion parameters (see M592)"""

    # A coefficient in the extrusion formula
    a = model_prop("a", float, 0)

    # B coefficient in the extrusion formula
    b = model_prop("b", float, 0)

    upper_limit = model_prop("upper_limit", float, 0.2)

    def __init__(self):
        super().__init__()
