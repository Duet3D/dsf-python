from .http_endpoint import HttpEndpoint
from .user_sessions import UserSession
from ...model_collection import ModelCollection
from ...model_object import ModelObject
from ...utils import model_prop


class DSF(ModelObject):
    """Information about Duet Software Framework"""

    build_date_time = model_prop('build_date_time', str, "")
    http_endpoints = model_prop('http_endpoints', ModelCollection[HttpEndpoint], ModelCollection(HttpEndpoint))
    is64bit = model_prop('is64bit', bool, False)
    plugin_support = model_prop('plugin_support', bool, False)
    root_plugin_support = model_prop('root_plugin_support', bool, False)
    user_sessions = model_prop('user_sessions', ModelCollection[UserSession], ModelCollection(UserSession))
    version = model_prop('version', str, "")

    def __init__(self):
        super().__init__()
