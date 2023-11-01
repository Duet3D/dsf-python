"""
clientinitmessages holds all messages a client can send to the server to initiate a connection

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
from .server_init_message import ServerInitMessage
from .. import ConnectionMode, InterceptionMode, SubscriptionMode
from ...commands.code_channel import CodeChannel


class ClientInitMessage:
    """
    An instance of this class is sent from the client to the server as a response
    to the ServerInitMessage. It allows a client to select the connection mode.
    """

    def __init__(self, mode: ConnectionMode = ConnectionMode.UNKNOWN, **kwargs):
        self.mode = mode
        self.version = ServerInitMessage.PROTOCOL_VERSION
        for key, value in kwargs.items():
            self.__dict__[key] = value


def intercept_init_message(
        intercept_mode: InterceptionMode,
        channels: list[CodeChannel],
        filters: list[str],
        priority_codes: bool,
        auto_flush: bool = True):
    """
    Enter interception mode
    Whenever a code is received, the connection must respond with one of
    - `Cancel` to cancel the code
    - `Ignore` to pass through the code without modifications
    - `Resolve` to resolve the current code and to return a message
    In addition the interceptor may issue custom commands once a code has been received

    :param intercept_mode: Defines in what mode commands are supposed to be intercepted
    :param channels: List of channel where codes may be intercepted.
    If the list is empty, all available channels are used
    :param filters: List of G/M/T-codes to filter or Q for comments
    This may only specify the code type and major/minor number (e.g. G1 or M105).
    Alternatively keyword types may be specified (e.g. if or elif).
    Asterisks are supported, too (e.g. T*)
    :param priority_codes: Defines if either regular or priority codes are supposed to be intercepted
    :param auto_flush: Automatically flush the code channel before notifying the client in case a code filter
    is specified.
    This option makes extra Flush calls in the interceptor implementation obsolete.
    It is highly recommended to enable this in order to avoid potential deadlocks when dealing with macros!
    """
    return ClientInitMessage(
        ConnectionMode.INTERCEPT,
        **{
            "InterceptionMode": intercept_mode,
            "Channels": channels,
            "AutoFlush": auto_flush,
            "Filters": filters,
            "PriortyCodes": priority_codes,
        },
    )


def command_init_message():
    """Enter command-based connection mode"""
    return ClientInitMessage(ConnectionMode.COMMAND)


def subscribe_init_message(subscription_mode: SubscriptionMode, filter_string: str, filter_list):
    """Enter subscription mode"""
    return ClientInitMessage(
        ConnectionMode.SUBSCRIBE,
        **{
            "SubscriptionMode": subscription_mode,
            "Filter": filter_string,
            "Filters": filter_list,
        },
    )
