"""
codechannel contains an enum with available code channels.

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
from enum import Enum


class CodeChannel(str, Enum):
    """Enumeration of every available code channel"""

    HTTP = "HTTP"
    Telnet = "Telnet"
    File = "File"
    USB = "USB"
    Aux = "Aux"
    Trigger = "Trigger"
    Queue = "Queue"
    LCD = "LCD"
    SBC = "SBC"
    Daemon = "Daemon"
    Aux2 = "Aux2"
    AutoPause = "AutoPause"
    Unknown = "Unknown"

    DEFAULT_CHANNEL = SBC

    @staticmethod
    def list():
        return list(map(lambda cc: cc.value, CodeChannel))
