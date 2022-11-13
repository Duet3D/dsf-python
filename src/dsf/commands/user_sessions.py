from enum import Enum

from .base_command import BaseCommand


class AccessLevel(str, Enum):
    """Defines what a user is allowed to do"""

    ReadOnly = "ReadOnly"
    ReadWrite = "ReadWrite"


class SessionType(str, Enum):
    """Types of user sessions"""

    Local = "Local"
    HTTP = "HTTP"
    Telnet = "Telnet"


def add_user_session(access_level: AccessLevel, session_type: SessionType, origin: str):
    """
    Register a new user session.
    Returns the ID of the new user session
    :param access_level: Access level of this session
    :param session_type: Type of this session
    :param origin: Origin of this session. For remote sessions, this equals the remote IP address
    """
    if not isinstance(access_level, AccessLevel):
        raise TypeError("access_level must be an AccessLevel")
    if not isinstance(session_type, SessionType):
        raise TypeError("session_type must be an SessionType")
    if not isinstance(origin, str) or not origin:
        raise TypeError("origin must be a string")
    return BaseCommand(
        "AddUserSession",
        **{
            "AccessLevel": access_level,
            "SessionType": session_type,
            "Origin": origin,
        },
    )


def remove_user_session(session_id: int):
    """
    Remove an existing user session
    :param session_id: Identifier of the user session to remove
    """
    if not isinstance(session_id, int):
        raise TypeError("session_id must be an integer")
    return BaseCommand("RemoveUserSession", **{"Id": session_id})
