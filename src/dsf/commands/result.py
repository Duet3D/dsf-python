"""
result contains classes relevant to result messages from the server

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
from typing import List

from ..object_model.messages import Message


class CodeResult:
    """
    List-based representation of a code result.
    Each item represents a Message instance which can be easily converted to a string
    Deprecated: Will be replaced by Message in foreseeable future
    """

    @classmethod
    def from_json(cls, data):
        """Deserialize an instance of this class from JSON deserialized dictionary"""
        if data is None:
            return cls([])
        return cls(list(map(Message.from_json, data)))

    def __init__(self, messages: List[Message]):
        self.messages = messages
