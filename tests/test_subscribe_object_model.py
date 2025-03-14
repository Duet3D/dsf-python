import threading
import os
import pathlib
import socket
import time
import importlib.util
import json

from tests.utils import check_json
from src.dsf import PROTOCOL_VERSION
from examples import subscribe_object_model

# here = pathlib.Path(__file__).parent.parent.resolve()
# example_path = here / "examples/subscribe_object_model.py"
# spec = importlib.util.spec_from_file_location("subscribe_object_model", example_path)
# subscribe_object_model = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(subscribe_object_model)

success_response = b'{"success":true}'
acknowledge_response = b'{"command":"Acknowledge"}'

def test_subscribe_object_model(monkeypatch, tmp_path):
    # Set up mock DCS socket
    mock_dcs_socket_file = os.path.join(tmp_path, "dsf.socket")
    monkeypatch.setattr(
        "dsf.connections.SubscribeConnection.connect.__defaults__",
        (mock_dcs_socket_file,),
    )

    # Event to track successful completion of the mock DCS server
    dcs_passed = threading.Event()
    # Event to track when the server is ready to accept connections
    server_ready = threading.Event()

    def mock_dcs():
        try:
            server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            server.bind(mock_dcs_socket_file)
            server.listen(1)
            server_ready.set()

            # Set a timeout for accepting connections
            server.settimeout(5)
            conn, _ = server.accept()

            # Initial handshake - send version and ID
            conn.sendall(f'{{"version":{PROTOCOL_VERSION}, "id":"foobar"}}'.encode())

            # Receive and verify the subscription setup message
            setup_msg = conn.recv(1024)
            expected_setup = {
                "mode": "Subscribe",
                "version": PROTOCOL_VERSION,
                "subscriptionMode": "Patch",
                "filter": "",
                "filters": None
            }
            check_json(expected_setup, setup_msg.decode())

            # Send success response for connection setup
            conn.sendall(success_response)

            # Send initial object model data
            initial_data = json.loads(open("tests/data/object_model.json").read())
            conn.sendall(str(initial_data).encode())

            # Expect acknowledge response
            ack1 = conn.recv(1024)
            assert ack1 == acknowledge_response, \
                f"Expected acknowledge command, received: {ack1.decode()}"

            # Send update to boards section
            conn.sendall('{"boards":"some-other-fake-data"}'.encode())

            # Expect acknowledge response
            ack2 = conn.recv(1024)
            assert ack2 == acknowledge_response, \
                f"Expected acknowledge command, received: {ack2.decode()}"

            # Send update to job section
            conn.sendall('{"job":"some-other-fake-data"}'.encode())

            # Expect acknowledge response
            ack3 = conn.recv(1024)
            assert ack3 == acknowledge_response, \
                f"Expected acknowledge command, received: {ack3.decode()}"

            # Send update to state section
            conn.sendall('{"state":"some-other-fake-data"}'.encode())

            # Expect acknowledge response
            ack4 = conn.recv(1024)
            assert ack4 == acknowledge_response, \
                f"Expected acknowledge command, received: {ack4.decode()}"

            conn.close()
            dcs_passed.set()  # indicate that all asserts passed
        except Exception as e:
            print(f"Mock DCS server error: {e}")
            # Don't set dcs_passed if there was an exception

    # Start mock DCS server thread
    thread = threading.Thread(target=mock_dcs, daemon=True)
    thread.start()

    # Wait for server to be ready before continuing
    assert server_ready.wait(timeout=5), "Mock DCS server failed to start"

    # Execute the example code we're testing
    subscribe_object_model.subscribe()

    # Wait for the mock DCS to complete with a timeout
    thread.join(timeout=5)

    # Verify the test completed successfully
    assert dcs_passed.is_set(), "The mock DCS did not complete successfully"
