#!/usr/bin/env python3

"""
Example of a subscribe connection to keep a local copy of the object model up-to-date
and to react when selected values change

Make sure when running this script to have access to the DSF UNIX socket owned by the dsf user.
"""

import time
from typing import Callable, Optional

from dsf.connections import SubscribeConnection, SubscriptionMode
from dsf.object_model import Heater, ObjectModel


def on_status_changed(*, key: str, data: str, indices: Optional[tuple[int, ...]]) -> None:
    # indices is None because the key has no ^ wildcard
    print("Machine status changed to", data)


def on_heater_temperature_changed(*, key: str, data: float, indices: tuple[int, ...]) -> None:
    # indices holds the list indexes matched by each ^ wildcard in the key
    print(f"Heater {indices[0]} is now at {data}C")


def subscribe() -> None:
    # Filters limit the updates DSF sends to the parts of the object model we need.
    # Use ** at the end of a filter to receive everything below a path, e.g. "heat/**"
    filters: list[str] = ["state/status", "heat/heaters[*]/current"]
    subscribe_connection: SubscribeConnection = SubscribeConnection(SubscriptionMode.PATCH, filter_list=filters)
    subscribe_connection.connect()

    try:
        # The first call receives the complete (filtered) object model
        object_model: ObjectModel = subscribe_connection.get_object_model()
        print("Machine status is", object_model.state.status.value)

        # Register callbacks for the keys we are interested in, ^ matches any list index
        unsubscribe_status: Callable[[], None] = subscribe_connection.subscribe_to_keys(["state.status"], on_status_changed)
        subscribe_connection.subscribe_to_keys(["heat.heaters.^.current"], on_heater_temperature_changed)

        for _ in range(20):
            # Later calls apply any pending patches to the object model and run the matching callbacks
            object_model = subscribe_connection.get_object_model()
            time.sleep(0.5)

        # Callbacks can be removed again at any time
        unsubscribe_status()

        # The object model returned by get_object_model() is always up-to-date
        heater: Optional[Heater]
        for index, heater in enumerate(object_model.heat.heaters):
            if heater is not None:
                print(f"Heater {index} final temperature: {heater.current}C")
    finally:
        subscribe_connection.close()


if __name__ == "__main__":
    subscribe()
