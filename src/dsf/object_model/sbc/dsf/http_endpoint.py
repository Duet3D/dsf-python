from .http_endpoint_type import HttpEndpointType
from ...model_object import ModelObject
from ...utils import model_prop


class HttpEndpoint(ModelObject):
    """Class representing an extra HTTP endpoint"""

    REPRAPFIRMWARE_NAMESPACE = "rr_"

    # HTTP type of this endpoint
    endpoint_type = model_prop("endpoint_type", HttpEndpointType, HttpEndpointType.GET)

    # Whether this is an upload request
    is_upload_request = model_prop("is_upload_request", bool, False)

    # Namespace of the endpoint
    namespace = model_prop("namespace", str, "")

    # Path to the endpoint
    path = model_prop("path", str, "")

    # Path to the UNIX socket
    unix_socket = model_prop("unix_socket", str, "")

    def __init__(self):
        super().__init__()

