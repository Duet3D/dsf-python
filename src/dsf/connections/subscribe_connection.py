from .base_connection import BaseConnection
from .init_messages import client_init_messages
from .. import commands, SOCKET_FILE
from ..object_model import ObjectModel


class SubscribeConnection(BaseConnection):
    """Connection class for subscribing to model updates"""

    def __init__(
        self,
        subscription_mode: client_init_messages.SubscriptionMode,
        filter_str: str = "",
        filter_list=None,
        debug: bool = False,
    ):
        super().__init__(debug)
        self.subscription_mode = subscription_mode
        self.filter_str = filter_str
        self.filter_list = filter_list

    def connect(self, socket_file: str = SOCKET_FILE):  # type: ignore
        """Establishes a connection to the given UNIX socket file"""
        sim = client_init_messages.subscribe_init_message(
            self.subscription_mode, self.filter_str, self.filter_list
        )
        return super().connect(sim, socket_file)

    def get_object_model(self) -> ObjectModel:
        """
        Retrieves the full object model of the machine
        In subscription mode this is the first command that has to be called once a
        ConnectionAbortedError has been established.
        """
        object_model = self.receive(ObjectModel)
        self.send(commands.model_subscription.acknowledge())
        return object_model

    def get_serialized_object_model(self) -> str:
        """
        Optimized method to query the object model UTF-8 JSON in any mode.
        May be used to get object model patches as well.
        """
        object_model_json = self.receive_json()
        self.send(commands.model_subscription.acknowledge())
        return object_model_json

    def get_object_model_patch(self) -> str:
        """
        Receive a (partial) object model update.
        If the subscription mode is set to SubscriptionMode.PATCH new update patches of
        the object model need to be applied manually. This method is intended to receive
        such fragments.
        """
        patch_json = self.receive_json()
        self.send(commands.model_subscription.acknowledge())
        return patch_json
