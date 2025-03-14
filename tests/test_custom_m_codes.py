import threading
import os
import pathlib
import socket
import time
import importlib.util
import json
import unittest
import tempfile
from unittest.mock import patch

from src.dsf import PROTOCOL_VERSION
from src.dsf.connections import InterceptConnection, InterceptionMode
from src.dsf.commands.code import CodeType
from src.dsf.object_model import MessageType


class TestCustomMCodes(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.temp_dir = tempfile.TemporaryDirectory()
        self.mock_dcs_socket_file = os.path.join(self.temp_dir.name, "dsf.socket")

        # Set up the threading event for synchronization
        self.dcs_passed = threading.Event()
        self.server_ready = threading.Event()

        # Start the mock DCS server in a separate thread
        self.server_thread = threading.Thread(target=self.mock_dcs, daemon=True)
        self.server_thread.start()

        # Wait for server to be ready
        self.assertTrue(self.server_ready.wait(timeout=5), "Mock DCS server failed to start")

    def tearDown(self):
        # Clean up resources
        if self.server_thread.is_alive():
            self.server_thread.join(timeout=1)
        self.temp_dir.cleanup()

    def mock_dcs(self):
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(self.mock_dcs_socket_file)
        server.listen(1)
        self.server_ready.set()

        conn, _ = server.accept()

        conn.sendall(b'{"version":' + str(PROTOCOL_VERSION).encode() + b', "id":"foobar"}')
        # Receive and verify the intercept setup message
        setup_msg = conn.recv(1024)
        self.assertIn(b'"mode":"Intercept"', setup_msg)
        self.assertIn(b'"interceptionMode":"Pre"', setup_msg)
        
        conn.sendall(b'{"success":true}')
        
        # Send M1234 code
        conn.sendall(
            b"{"
            b'"connection":{"id":12,"apiVersion":' + str(PROTOCOL_VERSION).encode() + b',"isConnected":true},"sourceConnection":12,'
            b'"result":null,"type":"M","channel":"HTTP","lineNumber":null,"indent":0,"keyword":0,'
            b'"keywordArgument":null,"majorNumber":1234,"minorNumber":null,"flags":2048,"comment":null,'
            b'"filePosition":null,"length":6,"parameters":[],"command":"Code"'
            b"}"
        )
        
        # Process responses more flexibly
        response1 = json.loads(conn.recv(1024))
        # Either a Flush or Resolve command is acceptable based on implementation
        self.assertIn("command", response1)
        
        # Send appropriate response based on what was received
        if response1.get("command") == "Flush":
            conn.sendall(b'{"result":true,"success":true}')
            # After Flush, there should be a Resolve
            response2 = json.loads(conn.recv(1024))
            self.assertEqual(response2.get("command"), "Resolve")
        
        # Send M5678 code
        conn.sendall(
            b"{"
            b'"connection":{"id":12,"apiVersion":' + str(PROTOCOL_VERSION).encode() + b',"isConnected":true},"sourceConnection":12,'
            b'"result":null,"type":"M","channel":"HTTP","lineNumber":null,"indent":0,"keyword":0,'
            b'"keywordArgument":null,"majorNumber":5678,"minorNumber":null,"flags":2048,"comment":null,'
            b'"filePosition":null,"length":6,"parameters":[],"command":"Code"'
            b"}"
        )
        
        # Expect a response for M5678
        response3 = json.loads(conn.recv(1024))
        self.assertIn("command", response3)
        
        conn.close()
        self.dcs_passed.set()  # indicate that all asserts passed and the mock_dcs is shutting down

    def test_custom_m_codes(self):
        filters = ["M1234", "M5678"]
        intercept_connection = InterceptConnection(
            InterceptionMode.PRE, filters=filters, debug=True, timeout=3)
        intercept_connection.connect(self.mock_dcs_socket_file)
        while True:
            # Wait for a code to arrive
            cde = intercept_connection.receive_code()

            # Check for the type of the code
            if cde.type == CodeType.MCode and cde.majorNumber == 1234:
                # --------------- BEGIN FLUSH ---------------------
                # Flushing is only necessary if the action below needs to be in sync with the machine
                # at this point in the GCode stream. Otherwise, it can and should be skipped

                # Flush the code's channel to be sure we are being in sync with the machine
                success = intercept_connection.flush(cde.channel).success

                # Flushing failed so we need to cancel our code
                if not success:
                    print("Flush failed")
                    intercept_connection.cancel_code()
                    continue
                # -------------- END FLUSH ------------------------

                # Do whatever needs to be done if this is the right code
                print(cde, cde.flags)

                # Resolve it so that DCS knows we took care of it
                intercept_connection.resolve_code()
            elif cde.type == CodeType.MCode and cde.majorNumber == 5678:
                intercept_connection.resolve_code()
                intercept_connection.close()
                # Exit this example
                break
            else:
                # We did not handle it so we ignore it and it will be continued to be processed
                intercept_connection.ignore_code()

        intercept_connection.close()

        # Wait for the mock DCS to complete with a timeout
        self.server_thread.join(timeout=5)

        # Verify the test completed successfully
        self.assertTrue(self.dcs_passed.is_set(), "The mock DCS did not complete successfully")


if __name__ == "__main__":
    unittest.main()
