from .base_command import BaseCommand
from ..object_model import AccessLevel, SessionType


def add_user_session(access_level: AccessLevel, session_type: SessionType, origin: str):
    """
    Register a new user session.
    Returns the ID of the new user session
    :param access_level: Access level of this session
    :param session_type: Type of this session
    :param origin: Origin of this session. For remote sessions, this equals the remote IP address
    """
    if not origin:
        raise ValueError("origin must not be empty")
    return BaseCommand(
        "AddUserSession",
        **{
            "accessLevel": access_level,
            "sessionType": session_type,
            "origin": origin,
        },
    )


def remove_user_session(session_id: int):
    """
    Remove an existing user session
    :param session_id: Identifier of the user session to remove
    """
    return BaseCommand("RemoveUserSession", **{"id": session_id})
