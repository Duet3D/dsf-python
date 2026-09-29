import json
import os
import tempfile
import unittest

from src.dsf import _read_socket_file  # pyright: ignore[reportPrivateUsage]


class TestSocketFile(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.tmp_dir.name, "config.json")

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_default_without_config(self):
        self.assertEqual(_read_socket_file(self.config_path), "/run/dsf/dcs.sock")

    def test_reads_socket_path_from_config(self):
        with open(self.config_path, "w") as f:
            json.dump({"SocketDirectory": "/var/run/custom", "SocketFile": "custom.sock"}, f)
        self.assertEqual(_read_socket_file(self.config_path), "/var/run/custom/custom.sock")

    def test_missing_config_keys_use_defaults(self):
        with open(self.config_path, "w") as f:
            json.dump({"SocketFile": "custom.sock"}, f)
        self.assertEqual(_read_socket_file(self.config_path), "/run/dsf/custom.sock")

    def test_invalid_config_uses_default(self):
        with open(self.config_path, "w") as f:
            f.write("{not json")
        self.assertEqual(_read_socket_file(self.config_path), "/run/dsf/dcs.sock")


if __name__ == "__main__":
    unittest.main()
