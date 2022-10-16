from typing import Union

from .access_level import AccessLevel
from .session_type import SessionType
from ..model_object import ModelObject


class UserSession(ModelObject):
    """Class representing a user session"""
    def __init__(self):
        super().__init__()
        # Access level of this session
        self._access_level = AccessLevel.readOnly
        # Identifier of this session
        self._id = 0
        # Origin of this session. For remote sessions, this equals the remote IP address
        self._origin = None
        # Corresponding identifier of the origin.
        self._origin_id = -1
        # Type of this session
        self._session_type = SessionType.local
        
    @property
    def access_level(self) -> AccessLevel:
        """Access level of this session"""
        return self._access_level
    
    @access_level.setter
    def access_level(self, value):
        self._access_level = value
        
    @property
    def id(self) -> int:
        """Identifier of this session"""
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = int(value) if value is not None else 0
        
    @property
    def origin(self) -> Union[str, None]:
        """Origin of this session. For remote sessions, this equals the remote IP address"""
        return self._origin
    
    @origin.setter
    def origin(self, value):
        self._origin = str(value) if value is not None else None
        
    @property
    def origin_id(self) -> int:
        """Corresponding identifier of the origin.
        If it is a remote session, it is the remote port, else it defaults to the PID of the current process"""
        return self._origin_id
    
    @origin_id.setter
    def origin_id(self, value):
        self._origin_id = int(value) if value is not None else -1
        
    @property
    def session_type(self) -> SessionType:
        """Type of this session"""
        return self._session_type
    
    @session_type.setter
    def session_type(self, value):
        if value is None or value == "":
            self._session_type = SessionType.local
        elif isinstance(value, SessionType):
            self._session_type = value
        elif isinstance(value, str):
            self._session_type = SessionType(value)
        else:
            raise TypeError(f"{__name__}.session_type must be of type SessionType. Got {type(value)}: {value}")
