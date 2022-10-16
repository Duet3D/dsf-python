from enum import Enum


class SpindleState(str, Enum):
    """Possible state of a spindles"""

    # Spinde not configured
    unconfigured = "unconfigured"

    # Spindle is stopped (inactive)
    stopped = "stopped"

    # Spindle is going forwards
    forward = "forward"

    # Spindle is going in reverse
    reverse = "reverse"
