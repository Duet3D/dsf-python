"""
responses contains classes and helper functions related to responses
from DuetSoftwareFramework.

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


def decode_response(obj):
    """Deserialization helper to convert a response to the appropriate type"""
    if obj["success"]:
        if "result" in obj:
            return Response(obj["result"])
        return Response()

    return ErrorResponse(obj["errorType"], obj["errorMessage"])


class BaseResponse:
    """Base class for every response to a command request."""

    def __init__(self, success):
        self.success = success


class Response(BaseResponse):
    """Response of a Command"""

    def __init__(self, result=None):
        super().__init__(True)
        self.result = result


class ErrorResponse(BaseResponse):
    """Response indicating a runtime exception during the internal processing of a command"""

    def __init__(self, error_type, error_message):
        super().__init__(False)
        self.error_type = error_type
        self.error_message = error_message
