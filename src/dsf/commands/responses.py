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
from ..utils import JSONObj, JSONElement
from ..object_model.model_object import ModelObject


class BaseResponse:
    """Base class for every response to a command request."""
    success: bool

    def __init__(self, success: bool):
        self.success = success

class Response(BaseResponse):
    """Response of a Command"""
    result: JSONElement | ModelObject

    def __init__(self, result: JSONElement = None):
        super().__init__(True)
        self.result = result


class ErrorResponse(BaseResponse):
    """Response indicating a runtime exception during the internal processing of a command"""
    error_type: str
    error_message: str

    def __init__(self, error_type: str, error_message: str):
        super().__init__(False)
        self.error_type = error_type
        self.error_message = error_message


def decode_response(obj: JSONObj) -> Response | ErrorResponse:
    """Deserialization helper to convert a response to the appropriate type"""
    if obj["success"]:
        if "result" in obj:
            return Response(obj["result"])
        return Response()

    error_type = obj.get("errorType")
    if not isinstance(error_type, str):
        raise TypeError("Error type must be string")

    error_message = obj.get("errorMessage")
    if not isinstance(error_message, str):
        raise TypeError("Error message must be string")

    return ErrorResponse(error_type, error_message)
