from .http_endpoint_type import HttpEndpointType
from ..model_object import ModelObject


class HttpEndpoint(ModelObject):
    """Class representing an extra HTTP endpoint"""

    def __init__(self):
        super().__init__()
        # HTTP type of this endpoint
        self._endpoint_type = HttpEndpointType.GET
        # Whether this is an upload request
        # If set to true, the whole body payload is written to a temporary file
        # and the file path is passed via the Commands.ReceivedHttpRequest.Body property
        self._is_upload_request = False
        # Namespace of the endpoint
        self._namespace = ""
        # Path to the endpoint
        self._path = ""
        # Path to the UNIX socket
        self._unix_socket = ""

    @property
    def endpoint_type(self) -> HttpEndpointType:
        """HTTP type of this endpoint"""
        return self._endpoint_type

    @endpoint_type.setter
    def endpoint_type(self, value):
        if isinstance(value, HttpEndpointType):
            self._endpoint_type = value
        elif isinstance(value, str):
            self._endpoint_type = HttpEndpointType(value)
        else:
            raise TypeError(f"{__name__}.endpoint_type must be of type HttpEndpointType. Got {type(value)}: {value}")

    @property
    def is_upload_request(self) -> bool:
        """Whether this is an upload request
        If set to true, the whole body payload is written to a temporary file
        and the file path is passed via the Commands.ReceivedHttpRequest.Body property"""
        return self._is_upload_request

    @is_upload_request.setter
    def is_upload_request(self, value):
        self._is_upload_request = bool(value)

    @property
    def namespace(self) -> str:
        """Namespace of the endpoint"""
        return self._namespace

    @namespace.setter
    def namespace(self, value):
        self._namespace = str(value) if value is not None else ""

    @property
    def path(self) -> str:
        """Path to the endpoint"""
        return self._path

    @path.setter
    def path(self, value):
        self._path = str(value) if value is not None else ""

    @property
    def unix_socket(self) -> str:
        """Path to the UNIX socket"""
        return self._unix_socket

    @unix_socket.setter
    def unix_socket(self, value):
        self._unix_socket = str(value) if value is not None else ""
