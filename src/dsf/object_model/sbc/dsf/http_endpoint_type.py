from enum import Enum


class HttpEndpointType(str, Enum):
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

    # WebSocket request. This has not been implemented yet, but it is reserved for future usage
    WebSocket = "WebSocket"
