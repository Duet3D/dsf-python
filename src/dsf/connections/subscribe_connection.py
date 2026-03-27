import json
from dataclasses import dataclass
from threading import Lock
from typing import Any, Callable, Sequence, List

from .base_connection import BaseConnection
from .init_messages import client_init_messages
from .. import commands, SOCKET_FILE
from ..object_model import ObjectModel
from ..utils import JSONObj


_MISSING = object()


@dataclass(frozen=True)
class _ObjectModelCallbackSubscription:
    keys: tuple[str, ...]
    callback: Callable[..., None]


class SubscribeConnection(BaseConnection):
    """
    Connection class for subscribing to model updates

    Constructor arguments:
    :param subscription_mode: Mode of the subscription
    :param filter_str: Delimited filter expression. Obsolete: Use filter_list instead.
    :param filter_list: Filter expressions
    :param debug: Whether debugging output is turned on for this connection
    """

    def __init__(
        self,
        subscription_mode: client_init_messages.SubscriptionMode,
        filter_list: List[str] = [],
        debug: bool = False,
    ):
        super().__init__(debug)
        self.subscription_mode = subscription_mode
        self.filter_list = filter_list
        self._object_model = ObjectModel()
        self._initial_object_model_received = False
        self._key_subscriptions: list[_ObjectModelCallbackSubscription] = []
        self._key_subscription_lock = Lock()

    def connect(self, socket_file: str = SOCKET_FILE):
        """Establishes a connection to the given UNIX socket file"""
        sim = client_init_messages.subscribe_init_message(
            self.subscription_mode, self.filter_list
        )
        return super()._connect(sim, socket_file)

    def get_object_model(self) -> ObjectModel:
        """
        Return the current object model as a deserialized ObjectModel instance.

        In SubscriptionMode.PATCH, the first call receives the full object model.
        Later calls consume at most one queued patch without blocking, update the
        cached object model, and run any registered key callbacks synchronously.
        """
        if (self.subscription_mode == client_init_messages.SubscriptionMode.FULL or not self._initial_object_model_received):
            self._object_model = self.receive(ObjectModel)
            self._initial_object_model_received = True
            self.send(commands.model_subscription.acknowledge())
            return self._object_model
        else:
            while (self.has_data_available()):
                patch_json = self.get_object_model_patch()
                patch_data = json.loads(patch_json)
                self._object_model.update_from_json(patch_data)
                self._notify_key_subscriptions(patch_data)
            return self._object_model

    def get_serialized_object_model(self) -> str:
        """
        Optimized method to query the object model UTF-8 JSON in any mode.
        May be used to get object model patches as well.
        """
        object_model_json = self.receive_json()
        self._initial_object_model_received = True
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

    def subscribe_to_keys(
        self,
        keys: Sequence[str],
        callback: Callable[..., None],
    ) -> Callable[[], None]:
        """
        Register a callback for one or more dot-delimited object model key paths.

        The initial object model must be consumed via get_object_model() or
        get_serialized_object_model() before this is called so that subsequent
        updates are patch fragments. The callback is invoked synchronously from
        get_object_model() once per matching key using keyword arguments
        ``key``, ``data``, and ``indices``. If a key contains one or more ``^``
        wildcards, ``indices`` contains the matched list indexes, otherwise it
        is ``None``.
        """
        normalized_keys = self._normalize_keys(keys)
        subscription = _ObjectModelCallbackSubscription(normalized_keys, callback)

        with self._key_subscription_lock:
            self._key_subscriptions.append(subscription)

        return lambda: self._remove_key_subscription(subscription)

    def close(self):
        super().close()

    def _remove_key_subscription(self, subscription: _ObjectModelCallbackSubscription) -> None:
        with self._key_subscription_lock:
            self._key_subscriptions = [
                current_subscription
                for current_subscription in self._key_subscriptions
                if current_subscription != subscription
            ]

    def _notify_key_subscriptions(self, patch_data: JSONObj) -> None:
        with self._key_subscription_lock:
            subscriptions = tuple(self._key_subscriptions)

        for subscription in subscriptions:
            matches = self._extract_key_changes(patch_data, subscription.keys)
            for key, data, indices in matches:
                self._invoke_callback(subscription.callback, key=key, data=data, indices=indices)

    @staticmethod
    def _normalize_keys(keys: Sequence[str]) -> tuple[str, ...]:
        normalized_keys = tuple(dict.fromkeys(key.strip() for key in keys if key.strip()))
        if not normalized_keys:
            raise ValueError("At least one non-empty object model key path is required")
        return normalized_keys

    @classmethod
    def _extract_key_changes(
        cls,
        patch_data: JSONObj,
        keys: Sequence[str],
    ) -> list[tuple[str, Any, tuple[int, ...] | None]]:
        matches: list[tuple[str, Any, tuple[int, ...] | None]] = []
        for key in keys:
            for indices, value in cls._extract_key_path_values(patch_data, key):
                matches.append((key, value, indices))
        return matches

    @classmethod
    def _extract_key_path_values(
        cls,
        patch_data: JSONObj,
        key: str,
    ) -> list[tuple[tuple[int, ...] | None, Any]]:
        matches = cls._walk_key_path(patch_data, key.split("."), ())
        return [
            (indexes if indexes else None, value)
            for indexes, value in matches
        ]

    @classmethod
    def _walk_key_path(
        cls,
        current_value: Any,
        remaining_parts: Sequence[str],
        indexes: tuple[int, ...],
    ) -> list[tuple[tuple[int, ...], Any]]:
        if not remaining_parts:
            return [(indexes, current_value)]

        part = remaining_parts[0]
        next_parts = remaining_parts[1:]

        if isinstance(current_value, dict):
            if part not in current_value:
                return []
            return cls._walk_key_path(current_value[part], next_parts, indexes)

        if isinstance(current_value, list):
            if part == "^":
                matches: list[tuple[tuple[int, ...], Any]] = []
                for index, item in enumerate(current_value):
                    if item is None:
                        continue
                    matches.extend(cls._walk_key_path(item, next_parts, indexes + (index,)))
                return matches

            try:
                index = int(part)
            except ValueError:
                return []
            if index < 0 or index >= len(current_value):
                return []
            item = current_value[index]
            if item is None:
                return []
            return cls._walk_key_path(item, next_parts, indexes)

        return []

    @staticmethod
    def _invoke_callback(
        callback: Callable[..., None],
        *,
        key: str,
        data: Any,
        indices: tuple[int, ...] | None,
    ) -> None:
        callback(key=key, data=data, indices=indices)
