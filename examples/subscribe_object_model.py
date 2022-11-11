#!/usr/bin/env python3

"""
Example of a subscribe connection to get the object model

Make sure when running this script to have access to the DSF UNIX socket owned by the dsf user.
"""

from dsf.connections import SubscribeConnection
from dsf.initmessages.clientinitmessages import SubscriptionMode


def subscribe():
    subscribe_connection = SubscribeConnection(SubscriptionMode.PATCH)
    subscribe_connection.connect()

    try:
        # Get the complete model once
        object_model = subscribe_connection.get_object_model()
        print(object_model)

        # Get multiple incremental updates, due to SubscriptionMode.PATCH, only a
        # subset of the object model will be updated
        for _ in range(0, 3):
            update = subscribe_connection.get_object_model_patch()
            print(update)
    finally:
        subscribe_connection.close()


if __name__ == "__main__":
    subscribe()
