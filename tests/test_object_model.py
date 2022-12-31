import json
import unittest

from src.dsf.object_model import *
from src.dsf.object_model.move.kinematics import DeltaKinematics
from src.dsf.object_model.sensors.filament_monitors import LaserFilamentMonitor


class Model(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def test_update_from_json(self):
        with open('object_model/model_virgin.json') as fp:
            json_data = json.load(fp)
        model = ObjectModel.from_json(json_data)

        self.assertEqual(MessageBoxMode.OkOnly, model.state.message_box.mode)
        self.assertEqual("message", model.state.message_box.message)
        self.assertEqual("title", model.state.message_box.title)

        json_text = json.dumps(json_data, sort_keys=True)
        self.assertEqual(json_text, str(model))

    def test_patch(self):
        model_to_update = ObjectModel()
        board = Board()
        board.firmware_name = "Foobar"
        model_to_update.boards.append(board)
        model_to_update.heat.bed_heaters.append(-1)
        model_to_update.heat.bed_heaters.append(1)
        model_to_update.heat.bed_heaters.append(2)
        model_to_update.heat.heaters.append(None)
        heater = Heater()
        heater.standby = 20
        model_to_update.heat.heaters.append(heater)
        heater = Heater()
        heater.active = 45
        model_to_update.heat.heaters.append(heater)

        updated_model = ObjectModel()
        board = Board()
        board.firmware_name = "Yum"
        updated_model.boards.append(board)
        updated_model.heat.bed_heaters.append(0)
        updated_model.heat.bed_heaters.append(1)
        heater = Heater()
        heater.active = 90
        heater.standby = 21
        updated_model.heat.heaters.append(heater)
        heater = Heater()
        heater.standby = 20
        updated_model.heat.heaters.append(heater)
        fan = Fan()
        fan.actual_value = 0.5
        fan.requested_value = 0.75
        updated_model.fans.append(fan)
        updated_model.state.status = MachineStatus.pausing
        updated_model.scanner.status = ScannerStatus.postProcessing

        patch = str(updated_model)
        print(patch)
        model_to_update.update_from_json(patch)

        self.assertEqual("Yum", model_to_update.boards[0].firmware_name)
        self.assertEqual(2, len(model_to_update.heat.bed_heaters))
        self.assertEqual(90, model_to_update.heat.heaters[0].active)
        self.assertEqual(21, model_to_update.heat.heaters[0].standby)
        self.assertEqual(20, model_to_update.heat.heaters[1].standby)
        self.assertEqual(1, len(model_to_update.fans))
        self.assertEqual(0.5, model_to_update.fans[0].actual_value)
        self.assertEqual(0.75, model_to_update.fans[0].requested_value)
        self.assertEqual(MachineStatus.pausing, model_to_update.state.status)
        self.assertEqual(ScannerStatus.postProcessing, model_to_update.scanner.status)

    def test_patch_from_json(self):
        patch = """{
            "boards": [
                {
                    "firmwareFileName": "Test"
                }
            ],
            "global": {
                "defaultSpeed": 6000
            },
            "move": {
                "kinematics": {
                    "name": "delta",
                    "deltaRadius": 123
                }
            },
            "plugins": {
                "foobar": {
                    "id": "foobar",
                    "name": "Foo 123"
                }
            },
            "sensors": {
                "filamentMonitors": [
                    {
                        "type": "laser"
                    }
                ]
            }
        }"""

        with open('object_model/model_virgin.json') as fp:
            json_data = json.load(fp)
        model = ObjectModel.from_json(json_data)
        # model = model.from_json(patch)
        model.update_from_json(patch)
        self.assertIsInstance(model.boards[0], Board)
        self.assertIsInstance(model.move.kinematics, DeltaKinematics)
        self.assertEqual(model.move.kinematics.delta_radius, 123)
        self.assertEqual(len(model.plugins), 1)
        self.assertIsInstance(model.plugins.get('foobar'), Plugin)
        self.assertEqual(model.plugins.get('foobar').id, "foobar")
        self.assertEqual(model.plugins.get('foobar').name, "Foo 123")
        self.assertEqual(len(model.sensors.filament_monitors), 1)
        self.assertIsInstance(model.sensors.filament_monitors[0], LaserFilamentMonitor)
        self.assertEqual(len(model.globals), 1)
        self.assertEqual(model.globals.get('defaultSpeed'), 6000)

        model.update_from_json(json.loads('{"plugins": null}'))
        self.assertEqual(len(model.plugins), 0)

    def test_update_from_json_mini5(self):
        with open('object_model/model_duet5mini.json') as fp:
            json_data = json.load(fp)
        model = ObjectModel.from_json(json_data)
        json_text = json.dumps(json_data, sort_keys=True)
        self.assertEqual(json_text, str(model))


if __name__ == '__main__':
    unittest.main()
