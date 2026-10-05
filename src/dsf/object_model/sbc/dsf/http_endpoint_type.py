from enum import Enum

from ....utils import DeprecatedAliasEnumType


class HttpEndpointType(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Enumeration of supported HTTP request types"""

    # HTTP GET request
    GET = "GET"

    # HTTP POST request
    POST = "POST"

    # HTTP PUT request
    PUT = "PUT"

    # HTTP PATCH request
    PATCH = "PATCH"

    # HTTP TRACE request
    TRACE = "TRACE"

    # HTTP DELETE request
    DELETE = "DELETE"

    # HTTP OPTIONS request
    OPTIONS = "OPTIONS"

    # WebSocket request for bidirection communication with a custom endpoint
    WEBSOCKET = "WebSocket"

    # Previous names, deprecated
    WebSocket = WEBSOCKET
