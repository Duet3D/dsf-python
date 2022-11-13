from .base_command import BaseCommand
from ..object_model.http_endpoints import HttpEndpointType


def add_http_endpoint(endpoint_type: HttpEndpointType, namespace: str, path: str, is_upload_request: bool):
    """
    Register a new HTTP endpoint via DuetWebServer.
    This will create a new HTTP endpoint under /machine/{Namespace}/{EndpointPath}.
    :param endpoint_type: Type of the HTTP request
    :param namespace: Namespace of the plugin wanting to create a new third-party endpoint
    :param path: Path to the endpoint to register
    :param is_upload_request: Whether this is an upload request
    :returns: a path to the UNIX socket which DuetWebServer will connect
    to whenever a matching HTTP request is received.
    A plugin using this command has to open a new UNIX socket with the given path that DuetWebServer can connect to
    """
    if not isinstance(endpoint_type, HttpEndpointType):
        raise TypeError("endpoint_type must be a HttpEndpointType")
    if not isinstance(namespace, str) or not namespace:
        raise TypeError("namespace must be a string")
    if not isinstance(path, str) or not path:
        raise TypeError("path must be a string")
    if not isinstance(is_upload_request, bool):
        raise TypeError("is_upload_request must be a boolean")
    return BaseCommand(
        "AddHttpEndpoint",
        **{
            "EndpointType": endpoint_type,
            "Namespace": namespace,
            "Path": path,
            "IsUploadRequest": is_upload_request,
        },
    )


def remove_http_endpoint(endpoint_type: HttpEndpointType, namespace: str, path: str):
    """
    Remove an existing HTTP endpoint.
    :param endpoint_type: Type of the endpoint
    :param namespace: Namespace of the endpoint
    :param path: Path to the endpoint to unregister
    :returns: true if the endpoint could be successfully removed
    """
    if not isinstance(endpoint_type, HttpEndpointType):
        raise TypeError("endpoint_type must be a HttpEndpointType")
    if not isinstance(namespace, str) or not namespace:
        raise TypeError("namespace must be a string")
    if not isinstance(path, str) or not path:
        raise TypeError("path must be a string")
    return BaseCommand(
        "RemoveHttpEndpoint",
        **{"EndpointType": endpoint_type, "Namespace": namespace, "Path": path},
    )
