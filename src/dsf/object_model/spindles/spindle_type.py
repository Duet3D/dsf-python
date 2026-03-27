from enum import Enum


class SpindleType(str, Enum):
    """Possible types of spindles"""

    # Enable and direction
    enaDir = "enaDir"

    # Forward and reverse
    fwdRev = "fwdRev"
