from enum import Enum


class AccessLevel(str, Enum):
    """Defines what a user is allowed to do"""

    # Changes to the system and/or operation are not permitted
    readOnly = "readOnly"

    # Changes to the system and/or operation are permitted
    readWrite = "readWrite"
