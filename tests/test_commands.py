import json
import unittest

from src.dsf.commands import generic, object_model
from src.dsf.connections.init_messages import client_init_messages


def serialize(obj: object) -> dict:
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))


class TestCommands(unittest.TestCase):
    def test_get_object_model(self):
        self.assertEqual(serialize(object_model.get_object_model(["move.axes"])),
                         {"command": "GetObjectModel", "filters": ["move.axes"]})

    def test_query_object_model(self):
        self.assertEqual(serialize(object_model.query_object_model("heat", "fn")),
                         {"command": "QueryObjectModel", "key": "heat", "flags": "fn"})

    def test_set_network_protocol(self):
        self.assertEqual(serialize(object_model.set_network_protocol("http", True)),
                         {"command": "SetNetworkProtocol", "protocol": "http", "enabled": True})

    def test_set_wifi_country(self):
        self.assertEqual(serialize(object_model.set_wifi_country("GB")),
                         {"command": "SetWifiCountry", "countryCode": "GB"})

    def test_set_update_status(self):
        self.assertEqual(serialize(generic.set_update_status(True, "Installing", 0.25)),
                         {"command": "SetUpdateStatus", "updating": True, "message": "Installing", "progress": 0.25})

    def test_subscribe_init_message(self):
        message = serialize(client_init_messages.subscribe_init_message(
            client_init_messages.SubscriptionMode.PATCH, ["state"], verbose=True, obsolete=True))
        self.assertTrue(message["verbose"])
        self.assertTrue(message["obsolete"])
