import threading
import os
import pathlib
import socket
import time
import importlib.util

here = pathlib.Path(__file__).parent.parent.resolve()
example_path = here / "examples/subscribe_object_model.py"
spec = importlib.util.spec_from_file_location("subscribe_object_model", example_path)
subscribe_object_model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(subscribe_object_model)


def test_subscribe_object_model(monkeypatch, tmp_path):
    mock_dcs_socket_file = os.path.join(tmp_path, "dsf.socket")
    monkeypatch.setattr(
        "dsf.connections.SubscribeConnection.connect.__defaults__",
        (mock_dcs_socket_file,),
    )

    dcs_passed = threading.Event()

    def mock_dcs():
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(mock_dcs_socket_file)
        server.listen(1)
        conn, _ = server.accept()
        conn.sendall('{"version":12, "id":"foobar"}'.encode())
        assert (
            conn.recv(1024)
            == b'{"mode":"Subscribe","version":11,"SubscriptionMode":"Patch","Filter":"","Filters":null}'
        )
        conn.sendall('{"success":true}'.encode())
        conn.sendall('{"boards":"fake-data", "job":"fake-data", "state":"fake-data"}'.encode())
        assert conn.recv(1024) == b'{"command":"Acknowledge"}'
        conn.sendall('{"boards":"some-other-fake-data"}'.encode())
        assert conn.recv(1024) == b'{"command":"Acknowledge"}'
        conn.sendall('{"job":"some-other-fake-data"}'.encode())
        assert conn.recv(1024) == b'{"command":"Acknowledge"}'
        conn.sendall('{"state":"some-other-fake-data"}'.encode())
        assert conn.recv(1024) == b'{"command":"Acknowledge"}'
        conn.close()
        dcs_passed.set()  # indicate that all asserts passed and the mock_dcs is shutting down

    thread = threading.Thread(target=mock_dcs, daemon=True)
    thread.start()
    time.sleep(1)

    subscribe_object_model.subscribe()

    thread.join()

    assert dcs_passed.is_set()
