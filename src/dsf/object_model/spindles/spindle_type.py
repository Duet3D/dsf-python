from enum import Enum

from ...utils import DeprecatedAliasEnumType


class SpindleType(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Possible types of spindles"""

    # Enable and direction
    ENA_DIR = "enaDir"

    # Forward and reverse
    FWD_REV = "fwdRev"

    # Previous names, deprecated
    enaDir = ENA_DIR
    fwdRev = FWD_REV
