"""
This module contains all basic commands to be sent to the server.

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


class BaseCommand:
    """Base class of a command."""

    @classmethod
    def from_json(cls, data):
        """Deserialize an instance of this class from a JSON deserialized dictionary"""
        return cls(**data)

    def __init__(self, command: str, **kwargs):
        self.command = command
        for key, value in kwargs.items():
            self.__dict__[key] = value
