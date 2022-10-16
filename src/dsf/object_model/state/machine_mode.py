from enum import Enum


class MachineMode(str, Enum):
    """Possible operation modes of the machine"""

    # Fused Filament Fabrication (default)
    FFF = "FFF"

    # Computer Numerical Control
    CNC = "CNC"

    # Laser operation mode (e.g. laser cutters)
    Laser = "Laser"
