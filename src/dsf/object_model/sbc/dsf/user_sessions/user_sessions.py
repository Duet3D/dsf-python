from .access_level import AccessLevel
from .session_type import SessionType
from ....model_object import ModelObject
from ....utils import model_prop


class UserSession(ModelObject):
    """Class representing a user session"""

    # Access level of this session
    access_level = model_prop("access_level", AccessLevel, AccessLevel.readOnly)

    # Identifier of this session
    id = model_prop("id", int, 0)

    # Origin of this session. For remote sessions, this equals the remote IP address
    origin = model_prop("origin", str)

    # Corresponding identifier of the origin.
    origin_id = model_prop("origin_id", int, -1)

    # Type of this session
    session_type = model_prop("session_type", SessionType, SessionType.local)

    def __init__(self):
        super().__init__()
