import threading
import os
import pathlib
import socket
import time
import importlib.util

here = pathlib.Path(__file__).parent.parent.resolve()
example_path = here / "examples/send_simple_code.py"

spec = importlib.util.spec_from_file_location("send_simple_code", example_path)
send_simple_code = importlib.util.module_from_spec(spec)
spec.loader.exec_module(send_simple_code)


def test_send_simple_code(monkeypatch, tmp_path):
    mock_dcs_socket_file = os.path.join(tmp_path, "dsf.socket")
    monkeypatch.setattr(
        "dsf.connections.CommandConnection.connect.__defaults__",
        (mock_dcs_socket_file,),
    )

    dcs_passed = threading.Event()

    def mock_dcs():
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(mock_dcs_socket_file)
        server.listen(1)
        conn, _ = server.accept()
        conn.sendall('{"version":11, "id":"foobar"}'.encode())
        assert conn.recv(1024) == b'{"mode":"Command","version":11}'
        conn.sendall('{"success":true}'.encode())
        assert conn.recv(1024) == b'{"command":"SimpleCode","Code":"M115","Channel":"SBC"}'
        conn.sendall('{"result":"fake code executed", "success":true}'.encode())
        conn.close()
        dcs_passed.set()  # indicate that all asserts passed and the mock_dcs is shutting down

    thread = threading.Thread(target=mock_dcs, daemon=True)
    thread.start()
    time.sleep(1)

    send_simple_code.send_simple_code()

    thread.join()

    assert dcs_passed.is_set()
