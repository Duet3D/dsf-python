import threading
import os
import pathlib
import socket
import time
import importlib.util
import json

from src.dsf import PROTOCOL_VERSION

here = pathlib.Path(__file__).parent.parent.resolve()
example_path = here / "examples/send_simple_code.py"

spec = importlib.util.spec_from_file_location("send_simple_code", example_path)
send_simple_code = importlib.util.module_from_spec(spec)
spec.loader.exec_module(send_simple_code)


def test_send_simple_code(monkeypatch, tmp_path):
    # Set up mock DCS socket
    mock_dcs_socket_file = os.path.join(tmp_path, "dsf.socket")
    monkeypatch.setattr(
        "dsf.connections.CommandConnection.connect.__defaults__",
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

            # Receive and verify the command setup message
            setup_msg = conn.recv(1024)
            assert setup_msg == f'{{"mode":"Command","version":{PROTOCOL_VERSION}}}'.encode(), \
                f"Expected command setup message, received: {setup_msg.decode()}"

            # Send success response for connection setup
            conn.sendall('{"success":true}'.encode())

            # Receive and verify the SimpleCode command
            cmd_msg = conn.recv(1024)
            expected_cmd = '{"command":"SimpleCode","code":"M115","channel":"SBC","executeAsynchronously":false}'.encode()
            assert cmd_msg == expected_cmd, f"Expected SimpleCode command, received: {cmd_msg.decode()}"

            # Send success response for the command
            conn.sendall('{"result":"fake code executed", "success":true}'.encode())
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
    send_simple_code.send_simple_code()

    # Wait for the mock DCS to complete with a timeout
    thread.join(timeout=5)

    # Verify the test completed successfully
    assert dcs_passed.is_set(), "The mock DCS did not complete successfully"
