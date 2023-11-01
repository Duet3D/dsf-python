from __future__ import annotations

from .model_collection import ModelCollection
from .model_dictionary import ModelDictionary
from .model_object import ModelObject
from .boards import Board
from .directories import Directories
from .fans import Fan
from .heat import Heat
from .http_endpoints import HttpEndpoint
from .inputs import InputChannel
from .job import Job
from .limits import Limits
from .messages import Message
from .move import Move
from .network import Network
from .plugins import Plugin
from .scanner import Scanner
from .sensors import Sensors
from .spindles import Spindle
from .state import State
from .tools import Tool
from .user_sessions import UserSession
from .volumes import Volume


class ObjectModel(ModelObject):

    def __init__(self):
        super(ObjectModel, self).__init__()
        self._boards = ModelCollection(Board)
        self._directories = Directories()
        self._fans = ModelCollection(Fan)
        self._globals = ModelDictionary(False)
        self._heat = Heat()
        self._http_endpoints = ModelCollection(HttpEndpoint)
        self._inputs = ModelCollection(InputChannel)
        self._job = Job()
        self._limits = Limits()
        self._messages = ModelCollection(Message)
        self._move = Move()
        self._network = Network()
        self._plugins = ModelDictionary(True, Plugin)
        self._scanner = Scanner()
        self._sensors = Sensors()
        self._spindles = ModelCollection(Spindle)
        self._state = State()
        self._tools = ModelCollection(Tool)
        self._user_sessions = ModelCollection(UserSession)
        self._volumes = ModelCollection(Volume)

    @property
    def boards(self) -> list[Board]:
        """List of connected boards
        The first item represents the main board"""
        return self._boards

    @property
    def directories(self) -> Directories:
        """Information about the individual directories
        This may not be available in RepRapFirmware if no mass storages are available"""
        return self._directories

    @property
    def fans(self) -> list[Fan]:
        """List of configured fans
        See also Fan()"""
        return self._fans

    @property
    def globals(self):
        """Dictionary of global variables vs JSON values
        When DSF attempts to reconnect to RRF, this may be set to null to clear the contents
        NB: RRF uses 'global' as name but as it is a reserved keyword in Python, 'globals' is used here."""
        return self._globals

    @property
    def heat(self) -> Heat:
        """Information about the heat subsystem"""
        return self._heat

    @property
    def http_endpoints(self) -> list[HttpEndpoint]:
        """List of registered third-party HTTP endpoints"""
        return self._http_endpoints

    @property
    def inputs(self) -> list[InputChannel]:
        """Information about every available G/M/T-code channel"""
        return self._inputs

    @property
    def job(self) -> Job:
        """Information about the current job"""
        return self._job

    @property
    def limits(self) -> Limits:
        """Machine configuration limits"""
        return self._limits

    @property
    def messages(self) -> list[Message]:
        """Generic messages that do not belong explicitly to codes being executed.
        This includes status messages, generic errors and outputs generated by M118
        See also Message()"""
        return self._messages

    @property
    def move(self) -> Move:
        """Information about the move subsystem"""
        return self._move

    @property
    def network(self) -> Network:
        """Information about connected network adapters"""
        return self._network

    @property
    def plugins(self) -> dict:
        """Dictionary of SBC plugins where each key is the plugin identifier
        Values in this dictionary cannot become null. If a change to null is reported, the corresponding key is deleted.
        Do not rely on the setter of this property; it will be removed from a future version."""
        return self._plugins

    @property
    def scanner(self) -> Scanner:
        """Information about the 3D scanner subsystem"""
        return self._scanner

    @property
    def sensors(self):
        """Information about connected sensors including Z-probes and endstops"""
        return self._sensors

    @property
    def spindles(self) -> list[Spindle]:
        """List of configured CNC spindles
        See also Spindle()"""
        return self._spindles

    @property
    def state(self) -> State:
        """Information about the machine state"""
        return self._state

    @property
    def tools(self) -> list[Tool]:
        """List of configured tools
        See also Tool()"""
        return self._tools

    @property
    def user_sessions(self):
        """List of user sessions"""
        return self._user_sessions

    @property
    def volumes(self):
        """List of available mass storages
        See also Volume()"""
        return self._volumes

    def _update_from_json(self, **kwargs) -> 'ObjectModel':
        super(ObjectModel, self)._update_from_json(**kwargs)

        # "global" is a reserved keyword in Python, so it is converted to "globals"
        if 'global_' in kwargs:
            self._globals.update_from_json(kwargs.get('global_'))
        return self
