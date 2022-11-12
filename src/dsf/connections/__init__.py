from enum import Enum


class ConnectionMode(str, Enum):
    """Supported connection types for client connections"""

    # Unknown connection type. If this is used, the connection is immediately terminated
    UNKNOWN = "Unknown"

    # Command mode. This allows clients to send general purpose messages to the control server like
    # G-codes or requests of the full object model
    COMMAND = "Command"

    # Interception mode. This allows clients to intercept G/M/T-codes before or after they are initially processed
    INTERCEPT = "Intercept"

    # Subscription mode. In this mode object model updates are transmitted to the client after each update
    SUBSCRIBE = "Subscribe"


class InterceptionMode(str, Enum):
    """Type of the intercepting connection"""

    # Intercept codes before they are internally processed by the control server
    PRE = "Pre"

    # Intercept codes after the initial processing of the control server but before they are forwarded to the RepRapFirmware controller
    POST = "Post"

    # Receive a notification for executed codes. In this state the final result can be still changed
    EXECUTED = "Executed"


class SubscriptionMode(str, Enum):
    """Type of the model subscription"""

    # Receive full object model after every update
    # Generic messages may or may not be included in the full object model. To keep track of messages reliably,
    # it is strongly advised to create a subscription in Patch
    FULL = "Full"

    # Receive only updated JSON fragments of the object model
    PATCH = "Patch"


from .base_command_connection import BaseCommandConnection
from .base_connection import BaseConnection
from .command_connection import CommandConnection
from .exceptions import InternalServerException, TaskCanceledException
from .intercept_connection import InterceptConnection
from .subscribe_connection import SubscribeConnection
