"""
parsedfileinfo contains classes related to file information parsed
by RepRapFirmware.

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
from datetime import datetime
from typing import List


class MachineModel(dict):
    """
    MachineModel provides generic access to the machine model.
    """

    @classmethod
    def from_json(cls, data):
        """Deserialize an instance of this class from JSON deserialized dictionary"""
        return cls(**data)


class ParsedFileInfo:
    """Holds information about a parsed G-code file"""

    @classmethod
    def from_json(cls, data):
        """Deserialize an instance of this class from JSON deserialized dictionary"""
        return cls(**data)

    def __init__(
        self,
        fileName: str,
        size: int,
        lastModified: datetime,
        height: float,
        firstLayerHeight: float,
        numLayers: int,
        filament: List[float],
        generatedBy: str,
        printTime: int,
        simulatedTime: int,
    ):
        self.file_name = fileName
        self.size = size
        self.last_modified = lastModified
        self.height = height
        self.first_layer_height = firstLayerHeight
        self.num_layers = numLayers
        self.filament = filament
        self.generated_by = generatedBy
        self.print_time = printTime
        self.simulated_time = simulatedTime
