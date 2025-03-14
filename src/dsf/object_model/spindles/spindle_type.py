from enum import Enum


class SpindleType(str, Enum):
    """Possible types of spindles"""

    # Spindle not configured
    null = "null"

    # Enable and direction
    enaDir = "enaDir"

    # Forward and reverse
    fwdRev = "fwdRev"
