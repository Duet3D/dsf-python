from typing import List

from .http_endpoint import HttpEndpoint
from .user_sessions import UserSession
from ...model_collection import ModelCollection
from ...model_object import ModelObject


class DSF(ModelObject):
    """Information about Duet Software Framework"""

    def __init__(self):
        super().__init__()
        self._build_date_time = ""
        self._http_endpoints = ModelCollection(HttpEndpoint)
        self._is64bit = False
        self._plugin_support = False
        self._root_plugin_support = False
        self._user_sessions = ModelCollection(UserSession)
        self._version = ""

    @property
    def build_date_time(self) -> str:
        """Datetime when DSF was built"""
        return self._build_date_time

    @build_date_time.setter
    def build_date_time(self, value):
        self._build_date_time = str(value)

    @property
    def is64bit(self) -> bool:
        """Indicates if the process is 64-bit"""
        return self._is64bit

    @is64bit.setter
    def is64bit(self, value):
        self._is64bit = bool(value)

    @property
    def http_endpoints(self) -> List[HttpEndpoint]:
        """List of registered third-party HTTP endpoints"""
        return self._http_endpoints

    @property
    def plugin_support(self) -> bool:
        """Indicates if DSF allows the installation and usage of third-party plugins"""
        return self._plugin_support

    @plugin_support.setter
    def plugin_support(self, value):
        self._plugin_support = bool(value)

    @property
    def root_plugin_support(self) -> bool:
        """Indicates if DSF allows the installation and usage of third-party root plugins (potentially dangerous)
        Requires plugin_support to be True"""
        return self._root_plugin_support

    @root_plugin_support.setter
    def root_plugin_support(self, value):
        self._root_plugin_support = bool(value)

    @property
    def user_sessions(self) -> List[UserSession]:
        """List of user sessions"""
        return self._user_sessions

    @property
    def version(self) -> str:
        """Version of the Duet Software Framework package (provided by Duet Control Server)"""
        return self._version

    @version.setter
    def version(self, value):
        self._version = str(value)
