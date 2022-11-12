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


def intercept_init_message(intercept_mode: InterceptionMode, channels, filters, priority_codes: bool):
    """Enter interception mode"""
    return ClientInitMessage(
        ConnectionMode.INTERCEPT,
        **{
            "InterceptionMode": intercept_mode,
            "Channels": channels,
            "Filters": filters,
            "PriorityCodes": priority_codes,
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
