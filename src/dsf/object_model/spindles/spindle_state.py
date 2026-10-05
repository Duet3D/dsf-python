from enum import Enum

from ...utils import DeprecatedAliasEnumType


class SpindleState(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Possible state of a spindles"""

    # Spinde not configured
    UNCONFIGURED = "unconfigured"

    # Spindle is stopped (inactive)
    STOPPED = "stopped"

    # Spindle is going forwards
    FORWARD = "forward"

    # Spindle is going in reverse
    REVERSE = "reverse"

    # Previous names, deprecated
    forward = FORWARD
    reverse = REVERSE
    stopped = STOPPED
    unconfigured = UNCONFIGURED
