from enum import Enum

from .basecommands import BaseCommand


class AccessLevel(str, Enum):
    """Defines what a user is allowed to do"""

    ReadOnly = "ReadOnly"
    ReadWrite = "ReadWrite"


class SessionType(str, Enum):
    """Types of user sessions"""

    Local = "Local"
    HTTP = "HTTP"
    Telnet = "Telnet"


def add_user_session(access: AccessLevel, tpe: SessionType, origin: str):
    """
    Register a new user session.
    Returns the ID of the new user session
    :param access: Access level of this session
    :param tpe: Type of this session
    :param origin: Origin of this session. For remote sessions, this equals the remote IP address
    """
    if not isinstance(access, AccessLevel):
        raise TypeError("access must be an AccessLevel")
    if not isinstance(tpe, SessionType):
        raise TypeError("tpe must be an SessionType")
    if not isinstance(origin, str) or not origin:
        raise TypeError("origin must be a string")
    return BaseCommand(
        "AddUserSession",
        **{
            "AccessLevel": access,
            "SessionType": tpe,
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
