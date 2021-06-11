import threading
import os
import pathlib
import socket
import time
import importlib.util

here = pathlib.Path(__file__).parent.parent.resolve()
example_path = here / "examples/custom_http_endpoint.py"
spec = importlib.util.spec_from_file_location("custom_http_endpoint", example_path)
custom_http_endpoint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(custom_http_endpoint)


def test_custom_http_endpoint(monkeypatch, tmp_path):
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
        assert (
            conn.recv(1024) == b"{"
            b'"command":"AddHttpEndpoint","EndpointType":"GET",'
            b'"Namespace":"custom","Path":"getIt","IsUploadRequest":false'
            b"}"
        )
        conn.sendall('{"result":"/var/run/dsf/custom/getIt-GET.sock","success":true}'.encode())
        conn.close()
        dcs_passed.set()  # indicate that all asserts passed and the mock_dcs is shutting down

    thread = threading.Thread(target=mock_dcs, daemon=True)
    thread.start()
    time.sleep(1)

    cmd_conn, endpoint = custom_http_endpoint.custom_http_endpoint()
    dcs_passed.wait(5)
    endpoint.close()
    cmd_conn.close()

    thread.join()

    assert dcs_passed.is_set()
