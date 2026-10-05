from enum import Enum

from ...utils import DeprecatedAliasEnumType


class DistanceUnit(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Distance unit used for positioning"""

    # Millimeters
    MM = "mm"

    # Inches
    INCH = "in"

    # Previous names, deprecated
    inch = INCH
    mm = MM

    # TODO: Implements DistanceUnitConverter
    # See https://github.com/Duet3D/DuetSoftwareFramework/blob/master/src/DuetAPI/ObjectModel/Inputs/DistanceUnit.cs#L28
