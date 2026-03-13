"""
serverinitmessage holds everything relevant to the first message received from the server

    Python interface to DuetSoftwareFramework
    Copyright (C) 2020 Duet3D

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from ... import PROTOCOL_VERSION
from ...utils import preserve_builtin, JSONObj


class ServerInitMessage:
    """
    An instance of this class is sent by the server to the client
    in JSON format once a connection has been established.
    """

    @classmethod
    def from_json(cls, data: JSONObj) -> 'ServerInitMessage':
        """Deserialize a dictionary coming from JSON into an instance of this class"""
        version = data.get("version")
        id = data.get("id")
        if not version or not id:
            raise ValueError("Invalid ServerInitMessage: missing required fields 'version' or 'id'")
        if not isinstance(version, int) or not isinstance(id, int):
            raise ValueError("Invalid ServerInitMessage: 'version' and 'id' must be integers")
        return cls(version, id)

    PROTOCOL_VERSION = PROTOCOL_VERSION

    def __init__(self, version: int, id_: int):
        self.version = version
        self.id = id_

    def is_compatible(self):
        """Check if the message received from the server indicates compatibility with this client"""
        return self.version >= ServerInitMessage.PROTOCOL_VERSION
