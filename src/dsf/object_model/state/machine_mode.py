from enum import Enum

from ...utils import DeprecatedAliasEnumType


class MachineMode(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Possible operation modes of the machine"""

    # Fused Filament Fabrication (default)
    FFF = "FFF"

    # Computer Numerical Control
    CNC = "CNC"

    # Laser operation mode (e.g. laser cutters)
    LASER = "Laser"

    # Previous names, deprecated
    Laser = LASER
