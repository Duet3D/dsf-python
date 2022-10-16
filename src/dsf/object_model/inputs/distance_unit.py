from enum import Enum


class DistanceUnit(str, Enum):
    """Distance unit used for positioning"""

    # Millimeters
    mm = "mm"

    # Inches
    inch = "in"

    # TODO: Implements DistanceUnitConverter
    # See https://github.com/Duet3D/DuetSoftwareFramework/blob/master/src/DuetAPI/ObjectModel/Inputs/DistanceUnit.cs#L28
