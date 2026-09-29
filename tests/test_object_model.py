import json
import unittest

from typing import Optional, cast

from src.dsf.object_model import (
    Accelerometer,
    Boards,
    BoardState,
    DriverId,
    ExpansionBoard,
    Heater,
    InputChannel,
    MainBoard,
    ObjectModel,
    Plugin,
    ProbeLoadCell,
    ProbeType,
)
from src.dsf.object_model.utils import is_model_object, JSONElement, JSONObj, model_prop, nullable_model_prop
from src.dsf.object_model.object_model import ModelCollection, ModelDictionary, ModelObject


class SubModel(ModelObject):
    value = model_prop("value", int, 0)


class TestModelObject(unittest.TestCase):
    class Dummy(ModelObject):
        p_int = model_prop("p_int", int, 1)
        np_int = nullable_model_prop("np_int", int)

        p_float = model_prop("p_float", float, 1.0)
        np_float = nullable_model_prop("np_float", float)

        p_str = model_prop("p_str", str, "default")
        np_str = nullable_model_prop("np_str", str)

        p_model = model_prop("p_model", SubModel, SubModel())
        np_model = nullable_model_prop("np_model", SubModel)

        p_model_collection = model_prop("p_model_collection", ModelCollection[SubModel], ModelCollection(SubModel))
        p_model_ncollection = model_prop(
            "p_model_ncollection", ModelCollection[Optional[SubModel]], ModelCollection(Optional[SubModel])
        )
        np_model_collection = nullable_model_prop(
            "np_model_collection", ModelCollection[SubModel], lambda: ModelCollection(SubModel)
        )
        np_model_ncollection = nullable_model_prop(
            "np_model_ncollection", ModelCollection[Optional[SubModel]], lambda: ModelCollection(Optional[SubModel])
        )

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_update_from_json(self):
        model = self.Dummy()

        self.assertEqual(model.p_int, 1)
        self.assertIsNone(model.np_int)
        self.assertEqual(model.p_float, 1.0)
        self.assertIsNone(model.np_float)
        self.assertEqual(model.p_str, "default")
        self.assertIsNone(model.np_str)

        patch: JSONObj = {
            "p_int": 10,
            "np_int": 11,
            "p_float": 1.1,
            "np_float": 1.2,
            "p_str": "hello",
            "np_str": "world",
        }
        model.update_from_json(patch)

        self.assertEqual(model.p_int, 10)
        self.assertEqual(model.np_int, 11)
        self.assertEqual(model.p_float, 1.1)
        self.assertEqual(model.np_float, 1.2)
        self.assertEqual(model.p_str, "hello")
        self.assertEqual(model.np_str, "world")

    def test_update_from_json_bad_data(self):
        model = self.Dummy()

        # Test non nullable props

        self.assertRaises(ValueError, lambda: model.update_from_json({"p_int": "not an int"}))
        self.assertRaises(TypeError, lambda: model.update_from_json({"p_int": None}))
        self.assertEqual(model.update_from_json({"p_int": 1.1}).p_int, 1)  # float should be cast to int
        self.assertEqual(model.update_from_json({"p_int": "2"}).p_int, 2)  # str should be cast to int

        self.assertRaises(ValueError, lambda: model.update_from_json({"p_float": "not a float"}))
        self.assertRaises(TypeError, lambda: model.update_from_json({"p_float": None}))
        self.assertEqual(model.update_from_json({"p_float": 2}).p_float, 2.0)  # int should be cast to float
        self.assertEqual(model.update_from_json({"p_float": "3.14"}).p_float, 3.14)  # str should be cast to float

        self.assertRaises(TypeError, lambda: model.update_from_json({"p_str": None}))
        self.assertEqual(model.update_from_json({"p_str": 123}).p_str, "123")  # int should be cast to str
        self.assertEqual(model.update_from_json({"p_str": 3.14}).p_str, "3.14")  # float should be cast to str

        # Test nullable props

        self.assertRaises(ValueError, lambda: model.update_from_json({"np_int": "not an int"}))
        self.assertEqual(model.update_from_json({"np_int": None}).np_int, None)  # nullable prop should be set to None
        self.assertEqual(model.update_from_json({"np_int": 1.1}).np_int, 1)  # float should be cast to int
        self.assertEqual(model.update_from_json({"np_int": "2"}).np_int, 2)  # str should be cast to int

        self.assertRaises(ValueError, lambda: model.update_from_json({"np_float": "not a float"}))
        self.assertEqual(
            model.update_from_json({"np_float": None}).np_float, None
        )  # nullable prop should be set to None
        self.assertEqual(model.update_from_json({"np_float": 2}).np_float, 2.0)  # int should be cast to float
        self.assertEqual(model.update_from_json({"np_float": "3.14"}).np_float, 3.14)  # str should be cast to float

        self.assertEqual(model.update_from_json({"np_str": None}).np_str, None)  # nullable prop should be set to None
        self.assertEqual(model.update_from_json({"np_str": 123}).np_str, "123")  # int should be cast to str
        self.assertEqual(model.update_from_json({"np_str": 3.14}).np_str, "3.14")  # float should be cast to str
        self.assertEqual(
            model.update_from_json({"np_str": "hello"}).np_str, "hello"
        )  # str should be accepted for nullable prop

    def test_update_from_json_model_object(self):
        model = self.Dummy()

        self.assertEqual(model.p_model.value, 0)
        self.assertIsNone(model.np_model)

        patch: JSONObj = {"p_model": {"value": 10}, "np_model": {"value": 20}}
        model.update_from_json(patch)

        self.assertEqual(model.p_model.value, 10)
        assert model.np_model is not None
        self.assertEqual(model.np_model.value, 20)

        model.update_from_json({"np_model": None})
        self.assertIsNone(model.np_model)

        self.assertRaises(
            TypeError, lambda: model.update_from_json({"p_model": None})
        )  # non nullable model prop should not accept None

    def test_update_from_json_model_collection(self):
        model = self.Dummy()

        self.assertEqual(len(model.p_model_collection), 0)
        self.assertIsNone(model.np_model_collection)

        patch: JSONObj = {
            "p_model_collection": [{}],
            "p_model_ncollection": [{}, None],
            "np_model_collection": [{}],
            "np_model_ncollection": [{}, None],
        }

        model.update_from_json(patch)
        assert model.np_model_collection is not None
        assert model.np_model_ncollection is not None
        self.assertEqual(len(model.p_model_collection), 1)
        self.assertIsNotNone(model.p_model_ncollection)
        self.assertEqual(len(model.p_model_ncollection), 2)
        self.assertEqual(len(model.np_model_collection), 1)
        self.assertEqual(len(model.np_model_ncollection), 2)

        self.assertIsNotNone(model.p_model_collection[0])
        self.assertIsNotNone(model.p_model_ncollection[0])
        self.assertIsNone(model.p_model_ncollection[1])

        model.update_from_json(
            {
                "p_model_collection": [{"value": 10}, {"value": 20}],
                "np_model_collection": [{"value": 30}, {"value": 40}],
            }
        )
        self.assertEqual(len(model.p_model_collection), 2)
        self.assertEqual(model.p_model_collection[0].value, 10)
        self.assertEqual(model.p_model_collection[1].value, 20)
        self.assertEqual(len(model.np_model_collection), 2)
        self.assertEqual(model.np_model_collection[0].value, 30)
        self.assertEqual(model.np_model_collection[1].value, 40)

        model.update_from_json(
            {
                "p_model_ncollection": [{"value": 30}, None, {"value": 40}],
                "np_model_ncollection": [{"value": 50}, None, {"value": 60}],
            }
        )
        self.assertEqual(len(model.p_model_ncollection), 3)
        p_first, p_second, p_third = model.p_model_ncollection
        assert p_first is not None and p_third is not None
        self.assertEqual(p_first.value, 30)
        self.assertIsNone(p_second)
        self.assertEqual(p_third.value, 40)
        self.assertEqual(len(model.np_model_ncollection), 3)
        np_first, np_second, np_third = model.np_model_ncollection
        assert np_first is not None and np_third is not None
        self.assertEqual(np_first.value, 50)
        self.assertIsNone(np_second)
        self.assertEqual(np_third.value, 60)

        model.update_from_json({"p_model_ncollection": [None], "np_model_ncollection": [None]})
        self.assertEqual(len(model.p_model_ncollection), 1)
        self.assertIsNone(model.p_model_ncollection[0])
        self.assertEqual(len(model.np_model_ncollection), 1)
        self.assertIsNone(model.np_model_ncollection[0])

        model.update_from_json({"p_model_collection": [], "p_model_ncollection": []})
        self.assertEqual(len(model.p_model_collection), 0)
        self.assertEqual(len(model.p_model_ncollection), 0)

        self.assertRaises(
            TypeError, lambda: model.update_from_json({"p_model_collection": None})
        )  # non nullable model collection should not accept None
        self.assertRaises(
            TypeError, lambda: model.update_from_json({"p_model_ncollection": None})
        )  # non nullable model collection should not accept None

        model.update_from_json({"np_model_collection": None})  # nullable model collection should accept None
        model.update_from_json({"np_model_ncollection": None})  # nullable model collection should accept None
        self.assertIsNone(model.np_model_collection)
        self.assertIsNone(model.np_model_ncollection)


class TestModelCollection(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_int_list(self):
        model = ModelCollection(int)
        model.update_from_json([1, 2, 3])

        self.assertEqual(model, [1, 2, 3])

    def test_nullable_int_list(self):
        model: ModelCollection[Optional[int]] = ModelCollection(Optional[int])

        model.update_from_json([1, None, 3])
        self.assertEqual(model, [1, None, 3])

    def test_nullable_float_list_updates_none_with_int(self):
        model: ModelCollection[Optional[float]] = ModelCollection(Optional[float])

        model.update_from_json([1.5, None])
        model.update_from_json([2.5, 3])

        self.assertEqual(model, [2.5, 3.0])
        self.assertIsInstance(model[1], float)

    def test_non_nullable_list_rejects_none_items(self):
        model: ModelCollection[float] = ModelCollection(float)

        model.update_from_json([1.5])
        self.assertRaises(TypeError, lambda: model.update_from_json([None]))

    def test_scalar_list_coerces_convertible_values(self):
        model: ModelCollection[int] = ModelCollection(int)

        model.update_from_json(["1"])
        model.update_from_json(["2", 3.9])

        self.assertEqual(model, [2, 3])
        self.assertIsInstance(model[0], int)
        self.assertIsInstance(model[1], int)

    def test_model_object_list(self):
        model: ModelCollection[Heater] = ModelCollection(Heater)

        patch: list[JSONElement] = [{"current": 10}, {"current": 20}]
        model.update_from_json(patch)
        self.assertEqual(len(model), 2)
        self.assertTrue(is_model_object(model[0]))
        self.assertTrue(is_model_object(model[1]))
        self.assertEqual(model[0].current, 10)
        self.assertEqual(model[1].current, 20)

        patch = [{"current": 30}]
        model.update_from_json(patch)
        self.assertEqual(len(model), 1)
        self.assertTrue(is_model_object(model[0]))
        self.assertEqual(model[0].current, 30)

    def test_nullable_model_object_list(self):
        model: ModelCollection[Optional[Heater]] = ModelCollection(Optional[Heater])

        patch: list[JSONElement] = [{"current": 10}, None, {"current": 20}]
        model.update_from_json(patch)
        self.assertEqual(len(model), 3)
        self.assertTrue(is_model_object(model[0]))
        self.assertIsNone(model[1])
        self.assertTrue(is_model_object(model[2]))
        first, _, third = model
        assert first is not None and third is not None
        self.assertEqual(first.current, 10)
        self.assertEqual(third.current, 20)

        patch = [None, {}]
        model.update_from_json(patch)
        self.assertEqual(len(model), 2)
        self.assertIsNone(model[0])
        self.assertTrue(is_model_object(model[1]))


class TestModelDictionary(unittest.TestCase):
    class Dummy(ModelObject):
        value = model_prop("value", int, 0)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_from_json(self):
        model = ModelDictionary.from_json({"key1": 1, "key2": {"nested": "dict"}})
        self.assertIsInstance(model, ModelDictionary)
        self.assertEqual(dict(model), {"key1": 1, "key2": {"nested": "dict"}})

        # Keys matching Python builtins are kept as-is
        self.assertEqual(dict(ModelDictionary.from_json({"type": 1})), {"type": 1})

        # null creates an empty dictionary
        self.assertEqual(len(ModelDictionary.from_json(None)), 0)

    def test_generic_dict(self):
        model = ModelDictionary(False)

        model.update_from_json(
            {"key1": 1, "key2": "hello", "key3": [1, 2, 3], "key4": {"nested": "dict"}, "key5": None}
        )
        self.assertEqual(model["key1"], 1)
        self.assertEqual(model["key2"], "hello")
        self.assertEqual(model["key3"], [1, 2, 3])
        self.assertEqual(model["key4"], {"nested": "dict"})
        self.assertIsNone(model["key5"])

        model.update_from_json(
            {"key1": 2, "key2": "world", "key3": [4, 5], "key4": {"nested": "updated"}, "key5": "not null anymore"}
        )
        self.assertEqual(model["key1"], 2)
        self.assertEqual(model["key2"], "world")
        self.assertEqual(model["key3"], [4, 5])
        self.assertEqual(model["key4"], {"nested": "updated"})
        self.assertEqual(model["key5"], "not null anymore")

        model.update_from_json({"key1": None, "key2": None, "key3": None, "key4": None, "key5": None})
        self.assertIsNone(model["key1"])
        self.assertIsNone(model["key2"])
        self.assertIsNone(model["key3"])
        self.assertIsNone(model["key4"])
        self.assertIsNone(model["key5"])

    def test_generic_non_nullable_dict(self):
        model = ModelDictionary(True)

        model.update_from_json(
            {"key1": 1, "key2": "hello", "key3": [1, 2, 3], "key4": {"nested": "dict"}, "key5": None}
        )
        self.assertEqual(model["key1"], 1)
        self.assertNotIn("key5", model)  # non nullable dict should delete the key when set to null

        model.update_from_json({"key1": None})
        self.assertNotIn("key1", model)  # non nullable dict should delete the key when set to null

    def test_model_object_dict(self):
        model = ModelDictionary(True, self.Dummy)

        model.update_from_json({"item1": {"value": 10}, "item2": {"value": 20}})
        self.assertTrue(is_model_object(model["item1"]))
        self.assertTrue(is_model_object(model["item2"]))
        self.assertEqual(model["item1"].value, 10)
        self.assertEqual(model["item2"].value, 20)

        model.update_from_json({"item1": {"value": 30}})
        self.assertEqual(model["item1"].value, 30)  # item1 should be updated instead of replaced
        self.assertEqual(model["item2"].value, 20)  # item2 should not be altered

        model.update_from_json({"item1": None})
        self.assertNotIn("item1", model)

        self.assertRaises(
            TypeError, lambda: model.update_from_json({"item1": 1})
        )  # can't update a model object with a non-dict value


class TestDriverId(unittest.TestCase):
    def test_defaults(self):
        driver = DriverId()
        self.assertEqual((driver.board, driver.port), (0, 0))
        self.assertEqual(driver.as_int(), 0)
        self.assertEqual(str(driver), "0.0")

    def test_constructors(self):
        self.assertEqual(DriverId(as_str="3"), DriverId(board=0, port=3))
        self.assertEqual(DriverId(as_str="1.2"), DriverId(board=1, port=2))
        self.assertEqual(DriverId(as_int=(1 << 16) | 2), DriverId(board=1, port=2))
        self.assertEqual(DriverId(board=1, port=2).as_int(), (1 << 16) | 2)

    def test_update_from_json(self):
        driver = DriverId(board=5, port=5)
        self.assertIs(driver.update_from_json("1.2"), driver)
        self.assertEqual((driver.board, driver.port), (1, 2))

        # A port-only string refers to the main board
        driver.update_from_json("3")
        self.assertEqual((driver.board, driver.port), (0, 3))
        self.assertEqual(driver.as_int(), 3)
        self.assertEqual(str(driver), "0.3")

        self.assertRaises(TypeError, lambda: driver.update_from_json({"board": 1, "port": 2}))

    def test_equality_and_hash(self):
        self.assertEqual(DriverId(board=1, port=2), DriverId(as_str="1.2"))
        self.assertNotEqual(DriverId(board=1, port=2), DriverId(board=2, port=1))
        self.assertNotEqual(DriverId(board=1, port=2), "1.2")
        self.assertEqual(len({DriverId(board=1, port=2), DriverId(as_str="1.2"), DriverId(board=0, port=2)}), 2)


class Model(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def test_instance_defaults_are_isolated(self):
        m1 = ObjectModel()
        m2 = ObjectModel()

        self.assertIsNot(m1.plugins, m2.plugins)
        self.assertIsNot(m1.sensors.filament_monitors, m2.sensors.filament_monitors)

        m1.update_from_json('{"sbc": {}}')
        m2.update_from_json('{"sbc": {}}')
        assert m1.sbc is not None and m2.sbc is not None
        self.assertIsNot(m1.sbc.dsf.user_sessions, m2.sbc.dsf.user_sessions)

    def test_boards(self):
        model = ObjectModel()

        json_patch = '{"boards": [{"accelerometer": null, "bootloaderFileName": null, "canAddress": 0, "closedLoop": null, "directDisplay": null, "firmwareDate": "2022-11-30", "firmwareFileName": "Duet3Firmware_Mini5plus.uf2", "firmwareName": "RepRapFirmware for Duet 3 Mini 5+", "firmwareVersion": "3.4.5", "iapFileNameSBC": "Duet3_SBCiap32_Mini5plus.bin", "iapFileNameSD": "Duet3_SDiap32_Mini5plus.bin", "maxHeaters": 32, "maxMotors": 7, "mcuTemp": {"current": 33.1, "max": 33.6, "min": 19.4}, "name": "Duet 3 Mini 5+", "shortName": "Mini5plus", "state": "unknown", "supports12864": true, "supportsDirectDisplay": true, "uniqueId": "F8AU7-6P6KL-K65J0-409N2-KKW1Z-Z5W3W", "v12": null, "vIn": {"current": 19.4, "max": 19.4, "min": 19.3}}]}'
        model.update_from_json(json_patch)

        # Voltage change
        json_patch = '{"boards":[{"vIn":{"current":42.5}}]}'
        model.update_from_json(json_patch)
        # Check if the value has been modified
        assert model.boards[0].v_in is not None
        self.assertEqual(model.boards[0].v_in.current, 42.5)
        # Check if other values has not been altered
        self.assertEqual(model.boards[0].v_in.min, 19.3)
        self.assertEqual(model.boards[0].v_in.max, 19.4)

    def test_boards_main_and_expansion(self):
        model = ObjectModel()
        model.update_from_json(
            '{"boards": [{"name": "Duet 3 MB6HC", "firmwareName": "RepRapFirmware", "maxHeaters": 32},'
            ' {"canAddress": 1, "name": "Duet 3 EXP3HC", "state": "timedOut", "timeout": 15}]}'
        )
        self.assertIsInstance(model.boards, Boards)
        main_board, expansion_board = model.boards
        assert isinstance(main_board, MainBoard)
        assert isinstance(expansion_board, ExpansionBoard)
        self.assertEqual(main_board.firmware_name, "RepRapFirmware")
        self.assertEqual(main_board.max_heaters, 32)
        self.assertEqual(expansion_board.state, BoardState.timedOut)
        self.assertEqual(expansion_board.timeout, 15)

        # Boards added by a later patch are typed by their position as well
        model.update_from_json('{"boards": [{}, {}, {"canAddress": 2}]}')
        new_board = model.boards[2]
        assert isinstance(new_board, ExpansionBoard)
        self.assertEqual(new_board.timeout, 10)

    def test_sensors_accelerometers_and_load_cell(self):
        model = ObjectModel()
        model.update_from_json(
            '{"sensors": {"accelerometers": [null, {"orientation": 25, "port": "121.spi.cs0",'
            ' "resolution": 16, "samplingRate": 1344}],'
            ' "probes": [{"type": 12, "loadCell": {"force": 12.5, "gramsPerCount": 0.01,'
            ' "preload": 50, "preloadWindow": [10, 100]}}]}}'
        )
        self.assertIsNone(model.sensors.accelerometers[0])
        accelerometer = model.sensors.accelerometers[1]
        assert isinstance(accelerometer, Accelerometer)
        self.assertEqual(accelerometer.port, "121.spi.cs0")
        self.assertEqual(accelerometer.resolution, 16)
        self.assertEqual(accelerometer.sampling_rate, 1344)

        probe = model.sensors.probes[0]
        assert probe is not None
        self.assertEqual(probe.type, ProbeType.LoadCell)
        assert isinstance(probe.load_cell, ProbeLoadCell)
        self.assertEqual(probe.load_cell.force, 12.5)
        self.assertEqual(list(probe.load_cell.preload_window), [10.0, 100.0])

    def test_rc2_fields(self):
        from src.dsf.object_model.move.input_shaping import InputShapingType

        model = ObjectModel()
        model.update_from_json(
            '{"limits": {"reportedAxes": 9},'
            ' "move": {"minSpeed": 60, "usingSCurve": true, "currentMove": {"filePosition": 1234},'
            ' "axes": [{"phaseStep": true}], "shaping": {"type": "ei2"},'
            ' "motionSystems": [{"printingAcceleration": 3000, "userPosition": [1, 2, 3]}]},'
            ' "job": {"build": {"objects": [{"cancelled": true}]}},'
            ' "sbc": {"upgrade": {"message": "Installing packages", "progress": 0.5}}}'
        )
        self.assertEqual(model.limits.reported_axes, 9)
        self.assertEqual(model.move.min_speed, 60)
        self.assertTrue(model.move.using_S_curve)
        self.assertEqual(model.move.current_move.file_position, 1234)
        self.assertTrue(model.move.axes[0].phase_step)
        self.assertEqual(model.move.shaping.type, InputShapingType.ei2)
        self.assertEqual(model.move.motion_systems[0].printing_acceleration, 3000)
        self.assertEqual(list(model.move.motion_systems[0].user_position), [1.0, 2.0, 3.0])
        assert model.job.build is not None
        self.assertTrue(model.job.build.objects[0].cancelled)
        assert model.sbc is not None and model.sbc.upgrade is not None
        self.assertEqual(model.sbc.upgrade.message, "Installing packages")
        self.assertEqual(model.sbc.upgrade.progress, 0.5)

        # Input shaping types reported by older DSF versions are still accepted
        model.update_from_json('{"move": {"shaping": {"type": "eI3"}}}')
        self.assertEqual(model.move.shaping.type, InputShapingType.ei3)

    def test_null_clears_dictionary(self):
        # DSF sends null for a dictionary that has been cleared, e.g. job.file.customInfo when a job ends
        model = ObjectModel()
        model.update_from_json({"job": {"file": {"customInfo": {"material": "PETG"}}}})
        self.assertEqual(dict(model.job.file.custom_info), {"material": "PETG"})
        custom_info = model.job.file.custom_info
        model.update_from_json({"job": {"file": {"customInfo": None}}})
        self.assertIs(model.job.file.custom_info, custom_info)
        self.assertEqual(dict(model.job.file.custom_info), {})

    def test_global(self):
        # "global" is a Python keyword so the JSON key is exposed as ObjectModel.globals
        with open("tests/object_model/model_full.json") as fp:
            json_data = json.load(fp)
        model = ObjectModel.from_json(json_data)
        self.assertEqual(dict(model.globals), json_data["global"])
        self.assertEqual(model.globals["daemonTick"], 250)
        self.assertEqual(model.globals["nozzleDiameters"], [0.6, 0.4])
        self.assertIsNone(model.globals["ret"])

        # Serialization converts "globals" back to "global"
        serialized = json.loads(model.to_json())
        self.assertIn("global", serialized)
        self.assertNotIn("globals", serialized)
        self.assertEqual(serialized["global"], json_data["global"])

        # Patch updates, adds and nulls variables (null does not delete global variables)
        model.update_from_json('{"global":{"daemonTick":500,"newVar":"hello","debug":null}}')
        self.assertEqual(model.globals["daemonTick"], 500)
        self.assertEqual(model.globals["newVar"], "hello")
        self.assertIn("debug", model.globals)
        self.assertIsNone(model.globals["debug"])
        self.assertEqual(model.globals["lastTool"], -1)

        # Global variable names matching reserved keys are kept untouched
        model.update_from_json('{"global":{"type":1,"global":2}}')
        self.assertEqual(model.globals["type"], 1)
        self.assertEqual(model.globals["global"], 2)
        self.assertNotIn("type_", model.globals)

        # Setting the whole object to null clears it
        model.update_from_json('{"global":null}')
        self.assertEqual(len(model.globals), 0)

        # Anything other than an object or null is rejected
        self.assertRaises(TypeError, lambda: model.update_from_json('{"global":[1, 2]}'))
        self.assertRaises(TypeError, lambda: model.update_from_json('{"global":5}'))

    def test_reserved_keys(self):
        # JSON keys shadowing Python builtins get a trailing underscore while being unpacked
        # (see preserve_builtin) and must still map to the correct properties
        from src.dsf.object_model.job import ThumbnailInfoFormat
        from src.dsf.object_model.move import InputShapingType

        model = ObjectModel()
        model.update_from_json(
            '{"job":{"file":{"thumbnails":[{"format":"qoi","height":48,"width":48}]}},'
            '"move":{"axes":[{"letter":"X","max":336,"min":-20.2}],"shaping":{"type":"ei2"}},'
            '"plugins":{"TestPlugin":{"id":"TestPlugin","license":"MIT"}},'
            '"state":{"messageBox":{"max":10.5,"min":-1.5,"message":"test"}}}'
        )

        self.assertEqual(model.job.file.thumbnails[0].format, ThumbnailInfoFormat.QOI)
        self.assertEqual(model.move.axes[0].max, 336)
        self.assertEqual(model.move.axes[0].min, -20.2)
        self.assertEqual(model.move.shaping.type, InputShapingType.ei2)
        self.assertEqual(model.plugins["TestPlugin"].id, "TestPlugin")
        self.assertEqual(model.plugins["TestPlugin"].license, "MIT")
        assert model.state.message_box is not None
        self.assertEqual(model.state.message_box.max, 10.5)
        self.assertEqual(model.state.message_box.min, -1.5)

        # Serialization uses the original JSON key names
        serialized = json.loads(model.to_json())
        self.assertEqual(serialized["job"]["file"]["thumbnails"][0]["format"], "qoi")
        self.assertEqual(serialized["move"]["axes"][0]["max"], 336)
        self.assertEqual(serialized["move"]["axes"][0]["min"], -20.2)
        self.assertEqual(serialized["move"]["shaping"]["type"], "ei2")
        self.assertEqual(serialized["plugins"]["TestPlugin"]["id"], "TestPlugin")
        self.assertEqual(serialized["plugins"]["TestPlugin"]["license"], "MIT")
        self.assertEqual(serialized["state"]["messageBox"]["max"], 10.5)
        self.assertEqual(serialized["state"]["messageBox"]["min"], -1.5)
        for key in ("format_", "id_", "license_", "max_", "min_", "type_"):
            self.assertNotIn(f'"{key}"', model.to_json())

    def test_http_endpoints(self):
        from src.dsf.object_model import HttpEndpointType

        model = ObjectModel()

        json_patch = '{"sbc":{"dsf":{"httpEndpoints":[{"endpointType":"GET","namespace":"ExecOnMcode","path":"getCmdList","isUploadRequest":false,"unixSocket":"/run/dsf/ExecOnMcode/getCmdList-GET.sock"}]}}}'
        model.update_from_json(json_patch)
        assert model.sbc is not None
        self.assertEqual(len(model.sbc.dsf.http_endpoints), 1)
        self.assertEqual(model.sbc.dsf.http_endpoints[0].endpoint_type, HttpEndpointType.GET)

        json_patch = '{"sbc":{"dsf":{"httpEndpoints":[{},{"endpointType":"POST","namespace":"ExecOnMcode","path":"saveCmdList","isUploadRequest":false,"unixSocket":"/run/dsf/ExecOnMcode/saveCmdList-POST.sock"}]}}}'
        model.update_from_json(json_patch)
        self.assertEqual(len(model.sbc.dsf.http_endpoints), 2)
        self.assertEqual(model.sbc.dsf.http_endpoints[1].endpoint_type, HttpEndpointType.POST)

    def test_inputs(self):
        from src.dsf.object_model.inputs import InputChannelState
        from src.dsf.commands.code_channel import CodeChannel

        model = ObjectModel()
        self.assertEqual(len(model.inputs), 0)

        # RRF reports null for input channels that are not available
        json_patch = '{"inputs":[{"active":true,"axesRelative":false,"compatibility":"RepRapFirmware","distanceUnit":"mm","drivesRelative":true,"feedRate":50,"inMacro":false,"lineNumber":0,"name":"HTTP","stackDepth":0,"state":"idle","volumetric":false},null,{"active":true,"axesRelative":false,"compatibility":"RepRapFirmware","distanceUnit":"mm","drivesRelative":true,"feedRate":50,"inMacro":false,"lineNumber":42,"name":"File","stackDepth":0,"state":"idle","volumetric":false},null]}'
        model.update_from_json(json_patch)

        self.assertEqual(len(model.inputs), 4)
        first_channel, second_channel, third_channel, fourth_channel = model.inputs
        assert isinstance(first_channel, InputChannel)
        self.assertIsNone(second_channel)
        assert isinstance(third_channel, InputChannel)
        self.assertIsNone(fourth_channel)
        self.assertEqual(first_channel.name, CodeChannel.HTTP)
        self.assertEqual(third_channel.name, CodeChannel.File)
        self.assertEqual(third_channel.line_number, 42)

        # Existing channels are updated in place, not replaced
        model.update_from_json('{"inputs":[{"state":"executing"},null,{"lineNumber":43},null]}')
        self.assertIs(model.inputs[0], first_channel)
        self.assertIs(model.inputs[2], third_channel)
        self.assertEqual(first_channel.state, InputChannelState.executing)
        self.assertEqual(third_channel.line_number, 43)

        # A channel may become null, and a previously null one may become a channel
        model.update_from_json('{"inputs":[null,{"name":"Telnet"},null,null]}')
        self.assertIsNone(model.inputs[0])
        second_channel = model.inputs[1]
        assert isinstance(second_channel, InputChannel)
        self.assertEqual(second_channel.name, CodeChannel.Telnet)
        self.assertIsNone(model.inputs[2])

        # Helper properties still work
        self.assertEqual(model.inputs.total, len(model.inputs.valid_channels))
        self.assertNotIn(CodeChannel.Unknown, model.inputs.valid_channels)

    @staticmethod
    def test_job():
        model = ObjectModel()
        json_patch = '{"job":{"file":{"filament":[496.4],"fileName":"0:/gcodes/Veil_Token.gcode","generatedBy":"ideaMaker 4.2.1.5321, 2022-10-01 17:45:38 UTC\u002b0200","height":1.04,"lastModified":"2022-10-01T16:45:39+01:00","layerHeight":0.12,"numLayers":9,"printTime":798,"size":594195,"thumbnails":[{"data":"iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAYAAACtWK6eAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAUnklEQVR4nO3cfYwcZ30H8O/zzMy\u002b3d77nl\u002buztmOA7bjGIOdBBJioDSEJkBLStOWCERTaKS2alWkqqioqpD6BxSVSlUFaktVggRUjdomBVIaikrA4Y9AYkhsY5vEdnz2\u002bezz3u3e3b7OzPP8\u002bsfM7O5dfMmdb\u002b9s1O9HWu3u3e7s8/xmnmeefZ7fLEBERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERET0/5261gXoljuA7N5cbuADw8PDU8bc6Isa3eJ5W3MaY/NWxiyQ6Xy9o1D0gCPnguBwv8jzvzY5\u002bTMAZq3L\u002bdG\u002bvqFfHRjYXDVmm0Dv2p72bimFZswCfZ2vc4GL/a5TnPTDM0UTHBtynBe/cv78\u002bOPALABZyzI\u002bAKTev2XL1poxb96bzR4oGbPLCAqdr3GgZvIaxZrF\u002bIwJpozIsY1aTz5Vr8/86/R08SWguZZlXC8/bw1E/3ImM3ZTOl24v39ot6OlcNmYnSOOuzWj9Zhv7UBW62FHqfRKNhpYWw1FXihZ84ILPPfVmZmnD1UqZ14GGqsp7Ad7e3ftdDOFd/f37r0Qhrs3uu4tWmGbo9RmT6nMa2\u002bho4wijcDKBJRMzBjzk4xS4yfqwZGvz5dOfKdeH19NObcBmXv7\u002b/f81tDQnlIY3j7ierc5Su1MKdW/ku0YEb8pMuMpVZwJzZmGmHP9jvPSdBiePV71L/1naer0c8AlAHY15V1P13MDcf9\u002b4\u002bgDe3PpA3PW7negtg05zphWylmPDw9FmpNheOT5pvmdv7h0/shy3vO5jRt/6U2Z7IMN4NYRx9ntKOWtdTkBwIgEZWtOOMDh5xuNRz5\u002b8eJTy3nfp0dGbtqTyf3TJs99i7vCTuVqWREzY8y4hfxUizo6EQTHHpqc\u002bBcA4Xp8/kq517oAS9kDFLbkMl/2Fby840IjGv9YCBwAapVtOxRBAKAR39cB1CBoCDAnghIkXYXcOuXhLQCW1UC2ZHMPV5X6jawCqgBcicqqASgV3etVlltE0ABQhyAQYD6qg1cS7J2B7J1PpXIAnlrOtvqy2V9sOM7bp0TgQpCOy\u002bcAXS\u002b3FUETQAA4Ruvt88D2WbHvuZzyghHgfy4DF1f1AWvkum0gBghqgPgAVDzkFgAi0c1CoBGdq6ObwALQEj03AHwAAQQmfh5K1BCa8d8CAUIIfCzdffnG9Cy3zGVryspxkZQ5OaQ6yy1xXRTaDd7Gz61Erw0A\u002bB3lDgD4EjWKMC53gKihLB6rNMKwvNzyVq3NDTiCGhS0ADXVjvXiciOJL64Q87jsFlHM/bicSYxriMrrx/FuoP1lTwA0oipel67bBnICmC4a89NhR7/RU\u002b3zhQPAU4AjUeG1UlFPF/d8RgFGJD4jALMiKCNuICra2dHWXv17btPaSSvybDkMv7ncMp8Kgie3KvX\u002bYa03uAAcpRZ8SudjF0AWQEopaChoCBwV1TIQgYFCFdFZbTbufTu3caX\u002bvGnMuZLvf3e55X252XxCtL4rB/XOfkcPZSQq81LnCgFajdbGdeiBQkZF\u002b8WN94UPgZXoW3pNAVURVACUICjLwjiE1k7NA9PLLfN6u\u002b6\u002bgxwAvAO5XOGegYH\u002bqtXbJ8Tcf3M285sbtO7zgNZBtFwighqAM2LxsrG1sshpUWjOh\u002bHlukgttPYylJpztJ4GcPbM/Pz4nO9PHWs2X7rKKqjtmczYrb29u/dlMjdWwvCmPq1vvzGVunVIqXQvFFIA1FXUowzBRSu4LNJ80fefvWzN0XwqdWSiWj014ftnj1YqJ3CVM1w3AKP7h4dvvjGdLvRovdUDsr6VMc/RhR7AS2t3REFcLbJjm\u002bPkB5RCdoV1AKLGXxZBSezseL35RI\u002bSxzamUse/MzNz\u002bUeVSum56\u002bxsci0biP5gPr97fyY/ckdv9pZJP9zd7zqb\u002bx29o2mlkFaq39N62cOb5QhFalVrjzTF/qDkm6c/O3n\u002b6R8Dl7u1/T1A6s6BgZvv7\u002b3fXxO7f4Pr7nCV2hHPWuW79TkA0BSpiMhkzdpTc8YeySh14ofV\u002bol/n5k6fgQodetzHsrnR27v7d0/6qbuGXKdNztK7ct0uS6\u002bSCMUuewoTJVDe6Eu5uQG1z17rF4/81i5fOxMozF9Mvq6te7WvIE8DHj3jI7uKAP7tzjeLqtx0IXaup4zUktJZn\u002bKYfiZD54//7WVvv/RTZtGqlq/64ZU6h4ruKPguq9fi3KuVDEMT3gK3zvj\u002b9/7WbX635\u002bZnV1xg3l0dOxdQ57\u002bqyHXfdNalHElRMRMxzNfrqijE37wbI\u002bWo1\u002b\u002bcGH8G9FIes2sdQNRj90w9s\u002bjrvtAt88G3VASi6IITlv52Z\u002bdfXnnSt//lRtu\u002bPwOL/X76asYaqyHkrX2ULPx\u002bU9duPBHK33vf2y/8eSgUq/PAfCuw/oF1laPBsG3P3r\u002b3Aewhguna/4lfUphq6fQkxULr2MKUcU3Hb9OYeXj8oQVac2sJF8gQ8QzVALMQ1AXoBLfz8Tj\u002bdYMkFxdfC8DPSkRpOIp0lRcNzeup1rqdpX1FJFW/Vozc4jG9fMQ1AQoQ6L6Rd\u002b99LzIihb7EnPxdLKLaLo6paLHHgBn8VRw/J5u7c/F9UxmxxoiKMV1nRDpOWvtwFV9wAqsdQMRALUmgM7p2k4qntWIpjmjg9aJ3yhoTylK6z4Kni/tqcQQ0RRugKhRROsb0XRuGP9/LZZujbVVdGy/vey\u002bqJ6CBfNmItFkb3IwJfVLpj7b94IgXqdpN4aongGima1mXM8A3c2T6ayBRTQjFe3Dxf9d\u002bKYF84PS7oSS6WHE5Wzvz/Z0cT1\u002bfYB2Pf14Gr7WXkdpl0ut7fAKWIcziAAXjAhcqFZXI0vcTMe7kgCGglZDMPF/Og96A8BIcgBJ6\u002bzRebAsdX4wIjURGZ8Ngr\u002b5mrqVQ3my37W/3qvVBhfRYlpnp7m4fp0HSNLYk78paZfZR3JQLjwzBvFaQ4D2gfRqDd\u002bKzDZEnrqauh2u1z51UyrzibxWO3NaZVyJG/SiaWDpuL9SfTsbQVK/UBY3wPY\u002b9RGt\u002bST1TOp9pX3oiExi6d3bFWs\u002buPxQobD59ZnM72aBd/c6zu6s1oMpAJl4ujM6dSt4aJ\u002buk1tnkGvxesa0CBrxAZIsogFR0P24B/I7/t9asLK20rD2rIgUNXBo1pgTPY5z\u002bKnJyfFL0cL3Vflwf//2kVzu7hHPO\u002biJ7MxovTOndX8a7d4nOVskS4QeoszJlFJIoz1USSR1DhD1qqV4LaQs7UXCEO0GlBxcgbWzDWvHHeCFWWO\u002bB2O\u002b//Vi8eTV1u2tQO8bN20aE\u002bC2Ta672wH2aqV29yldSDs676E9rExGAUl9BQpGBKJUqzNQAHoB5KGQUapV784GZeI61xEN8yoQXBDBXDxi8K2drxlzGMCTl\u002br1r/1vuXz2auu3HGvaQA4A3tuGhzfcmU5vnbdq37Z06kBTyX0j2tmsV/F9Y0IEzwT\u002bibKVFw2AmjWXrUgQaF33gGLW8y7XwnDuzPz8eN3a2ulqdXwOmOlu7ZakCsCmsZ6ekd3Z7NimVHZsg6vu3KjUfdscd7AHK1/LSRgRXBLBuNj5s2H4jUlrf1D0/fGLtdrkbK127hQw1d2qLK0PGBpNpws78vmxbel0YcB1\u002b\u002brGjAiQs9YOp5TyUsoZCWGRh9ryhpS3b1RpvZq6F62dTAv\u002bayoMn3PEPH\u002b60Rh/dGbm0lqunXS1gbwZ6Hvn0NCet\u002bfzt9dE7dvkOfuMYDSr1Ei3p3RDkYuTgf/Xf3Du3BfORxkk14178/mRB3sHDuRd9Z4R1zvoKbWj2\u002bsgRqTZsPbEnLGHG7CP/\u002bW5c9//CbDsNJP18NG\u002bvqEHh4b\u002bNK/1RzylN3Vz21bENEWKSmFiJgyPOMDhI43Gc1\u002bemnr\u002bGFDp1uesuIE8APQf3LCh8LpMZvOFwNxycyZ1c9nYPVmtd/U5zmi3CrZcgUhlKgwe88PwH57x/Rc\u002bWyyu64LSA\u002bgbeu8v9Baswb4tae\u002bOQHDXJs\u002b9bT3LAAC\u002btbU5Y486GofP\u002b/5TvSIvfHFycuJbwNx6luPhwcH\u002bd\u002bRyB4Zc9z2DjvtwtzuG12JFTMmYs0m28LgfHO918OKpqpn8t/LFqedWuG7yqg3kvp6eTQezvbsOxivdoylvL4DNAApZrdd8im0lrIgJIadKoXlyyg8f\u002b8jFiaewBl/gfhvI3DC44cBbezNv9ZRzMK2wx9G6kFaqt9uftRqBtTUDTNStnAzEHDru\u002bz/8\u002bMWLT2ON0sq/uGHLG0Yy\u002bmMbXfdeD2qrXqdU/\u002bUwIsa3tqyUnhJIsRSaIwOuPn6k0XjxC5OTP3y1zINWA3konx95b3//Dqv1XQPafbuI7Cx47uvWpwrd93LT/9svnh//xLe6cGXbh4Ge\u002bzZvuWc45dzf67j3p9e5V\u002byWpkilFAZP1EJ8db42d\u002bihcnnVQ7J7gfTHbhj7zPZU6o\u002b7UcZroWzMORE8M2PDZ7S1T39zdvbUlyqVywCgPjcy8qa9ufwnc1rdntF6VF/HGb4rMWNt7dH5uYP/WCweXs12HkT/4MPbhh7vc5y3dats14M5a559ZGrqfY9Uq6u6DuOThcL\u002bu3v7Dg1onetW2a4lC4QNay8YkR\u002bfrQefdm/L5w/ltXPdpYGsVF0ENQguWMEZsThvrb4osurGXs36\u002bWlgVzpeTV7thVrXmolTz58xduxH1qZWu72667qnxerh\u002bKL6rIqn7H9OY6UBN6f1GICxjVm5zT0vUtssticLhdR1mHNzJbMirfWBmTj9IE6taC\u002b8AalCOn1VaRaLzYlARJABkIUgHa/huD8n8ZqL4zMpFhPx44rtTm7B9lSqzwFSNURjWUcEHqKUlBQEXrzu4\u002bHnK15nrMXzYQi3Ya1f0hplCLREOUUu4guToOLLLV\u002bZO3W16xiJzvyp5JYs6vkiqMbpE1WJFglnEDWKOazDT49cqbyI0lf8jqvudHxJbZSf1M7BWpxr1o08rFY5pL0IKuiIGQRVARoQVASYE4uyANMdK9hrISlHolUmAZoq\u002bksrV0ukdWxpxBe8IYrb4uOs8wZ073hLshiCuJxVEdQRdRpFEUyLtFaNayJww45pL4v2gkK0uinxFXgLSVxZwcK8KWBhwDp3TAhBKFF\u002bUeelpBbR6rBBx6Ww8TaSlISw4z3LnZZqWnvyTLl8dJkvX1Idr0znaOWOoR1sif8TX526YGUZ6MhR6sg3S7aBjm0lj9sxlDjPbGH2QCjty4o7L3E1EqVu\u002bGgfDFeigBBa\u002bysIxRUdKhaP3VUYOTekZasDAK9yIAuSPLL28\u002bg\u002bjl5HLldnAuSrxa0zRakzncfGcVucVeHHcWtdvowkVenKl1477\u002brr\u002b5VerW9cnGOzWGdOUCu1IU6YawCt\u002b7q0n1fjvzUQZdI247/XEe3YprRbchgXOAlIZ6Ozi54vWUaRWihyrBaGj5wulf7wB/X6hdd4y2s6FYZz\u002b3pytZyjb3cVeqIfMlje6LozVWZh3NrXlCex6oxbDVGMGgCqiIaOPhbGLdlOiKXz2paKmRWplcLwT75fKj298ogsdDwIKi/Ozn5pIJud11oPWaUKWsFpHeDLjBXwyv19pbglyYtJrJqS/M4AWpdZNxBdqpwM\u002bxqIGkYD7QZqlviszng1rP2u\u002bvPR0Z0DjvN3Gxz37nzHeaydebpwQ7Joo0nCXfL6zkS0zvV/v9XHtndq8trkBwCS1pskIobSfu\u002bVKiAiUjXmuKfU8Wnff8JT6vCpqamXXlhFbtVSPjQyctP2dPrBLPT9w67e3a9U2ot3vY6vdRcAUO2YXSl5r93LyYKzhpH24yQ\u002b0eOOJD8sjFv7\u002bvCFP0wh8fB0cRZzzZijxtqv1YPg248Xi891KzYdUr\u002b3efNeR\u002bQNo573bgXsH3Scm3Iq\u002bhEwpyOZU2FRzLAwbsArz6jJ8QZ0nDWk3evbjr8nI5XW8SYLE1zDeEvJGSTJb0u2VTfmmZlK5cFWg3jf8PBtr0ulDg647jt6tN6RgRrJajWgAc/rGGZ17ujWc5WcBheePtunK1mQeRpIu0EIol/ESM4incMvI9IIrZ0VpSqi1GQ1DMcNMO4AP51oNE6fKZWOn1\u002b/HKuWXmD4/Rs33jnqeXvSSr1lUDtbNWTAgxpOK/Q4SmkH0S\u002bsJGnenb15q9GoOCayuFG0h2wL47ZwqGkk6Q0lGffbhtiyAWpa62IlDE8KcHKm2Tx0qlY78VK9fn6tY7PYENC3t69v596enp2eUnuyWu/q17rgKFXwgMG0UjkPqtdRHUmbi\u002bKW/OrLgs4mPiCtLGwUUawUgrgBSEeMWo2j43hrAIFv7awAMzVrf\u002bIAh8/U6986VCq9ACy9kp69e3Bw5I09PQPlMNziAje6WhcKrru5bm1BATkLFFwRV5Te4Kjkug6B0npQK5WNfpoH4lsz2dm7ATIXiFQCEau0vqSUqqS1nq8bU5kNw/HAmFoITA6m00VrzPzp2dnZS/V65eXrLM9oEWdXb\u002b/A7nR6eGsqlZ81ZhTWjmQ9b6zfcQoudM634YhA9SlBj1LoVUr1JuNpA1Epx9mcNBYLII6btNL5xV4KAWOVqgowl9b6cihSK/n\u002beN3asmg9vcF1X56oVksXwrB2tFot4trMZyzLRqBnWzY7ONrTk9ueTg8Vw7Cggc09WhdcIDfoeRsq1m50RWkL2egoaCXIi1J9UVJf1IV4UdxU0tEG1l60EBsPo5rW2ul4pbgIpWppxynONJvjVWOmoFR5IJ0\u002beb5SmZ0ol2eu1XXvRERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERNe3/wOxabcDNmswcQAAAABJRU5ErkJggg==","format":"png","height":200,"offset":483,"size":7144,"width":200}]},"build":{"currentObject":-1,"m486Names":false,"m486Numbers":false,"objects":[]},"duration":0,"pauseDuration":0,"rawExtrusion":0,"warmUpDuration":0,"layers":[],"lastDuration":null}}'
        model.update_from_json(json_patch)

    def test_json_serialization(self):
        with open("tests/object_model/model_full.json") as fp:
            json_data = json.load(fp)
        model = ObjectModel.from_json(json_data)

        def recursive_compare(obj1: object, obj2: object) -> None:
            if isinstance(obj1, dict):
                self.assertIsInstance(obj2, dict)
                dict1, dict2 = cast(dict[str, object], obj1), cast(dict[str, object], obj2)
                self.assertEqual(set(dict1.keys()), set(dict2.keys()))
                for key in dict1:
                    recursive_compare(dict1[key], dict2[key])
            elif isinstance(obj1, list):
                self.assertIsInstance(obj2, list)
                list1, list2 = cast(list[object], obj1), cast(list[object], obj2)
                self.assertEqual(len(list1), len(list2))
                for item1, item2 in zip(list1, list2):
                    recursive_compare(item1, item2)
            elif isinstance(obj1, ModelObject):
                self.assertIsInstance(obj2, ModelObject)
                recursive_compare(vars(obj1), vars(obj2))
            else:
                self.assertEqual(obj1, obj2)

        model2 = ObjectModel().update_from_json(str(model))
        recursive_compare(model.__dict__, model2.__dict__)

    def test_messages(self):
        from src.dsf.object_model.messages import MessageType

        model = ObjectModel()
        json_patch = '{"messages":[{"content":"File 0:/gcodes/Veil_Token.gcode will print in 0h 14m plus heating time","time":"2022-12-31T16:42:22.8058935+00:00","type":0}]}'
        model.update_from_json(json_patch)
        self.assertEqual(len(model.messages), 1)
        self.assertEqual(str(model.messages[0].time), "2022-12-31 16:42:22.805893+00:00")
        self.assertEqual(model.messages[0].type, MessageType.Success)

        json_patch = '{"messages":[]}'
        model.update_from_json(json_patch)
        self.assertEqual(len(model.messages), 0)

    def test_move_kinematics(self):
        from src.dsf.object_model.move.kinematics import CoreKinematics, DeltaKinematics, Kinematics, KinematicsName

        model = ObjectModel()
        json_patch = '{"move": {"kinematics": {"name": "delta","deltaRadius": 123}}}'
        model.update_from_json(json_patch)

        assert isinstance(model.move.kinematics, DeltaKinematics)
        self.assertEqual(model.move.kinematics.name, KinematicsName.linearDelta)
        self.assertEqual(model.move.kinematics.delta_radius, 123)

        # Switch to CoreXY (eg: M669 K1)
        json_patch = '{"move":{"kinematics":{"forwardMatrix":[[0.5,0.5,0],[0.5,-0.5,0],[0,0,1]],"inverseMatrix":[[1,1,0],[1,-1,0],[0,0,1]],"tiltCorrection":{"correctionFactor":1,"lastCorrections":[],"maxCorrection":1,"screwPitch":0.5,"screwX":[],"screwY":[]},"name":"coreXY","segmentation":null}}}'
        model.update_from_json(json_patch)
        self.assertIsInstance(model.move.kinematics, CoreKinematics)
        self.assertEqual(model.move.kinematics.name, KinematicsName.coreXY)

        # Switch to linear delta (eg: M669 K3)
        json_patch = '{"move":{"kinematics":{"deltaRadius":105.6,"homedHeight":240,"printRadius":80,"towers":[{"angleCorrection":0,"diagonal":215,"endstopAdjustment":0,"xPos":-91.452,"yPos":-52.8},{"angleCorrection":0,"diagonal":215,"endstopAdjustment":0,"xPos":91.452,"yPos":-52.8},{"angleCorrection":0,"diagonal":215,"endstopAdjustment":0,"xPos":0,"yPos":105.6}],"xTilt":0,"yTilt":0,"name":"delta","segmentation":null}}}'
        model.update_from_json(json_patch)
        assert isinstance(model.move.kinematics, DeltaKinematics)
        self.assertEqual(model.move.kinematics.name, KinematicsName.linearDelta)
        self.assertEqual(model.move.kinematics.delta_radius, 105.6)

        # Kinematics without a dedicated class use the base type (eg: M669 K0 on an unconfigured machine)
        model.update_from_json('{"move":{"kinematics":{"name":"unknown"}}}')
        self.assertIs(type(model.move.kinematics), Kinematics)
        self.assertEqual(model.move.kinematics.name, KinematicsName.unknown)

    def test_get_kinematics_type(self):
        from src.dsf.object_model.move.kinematics import (
            CoreKinematics,
            DeltaKinematics,
            HangprinterKinematics,
            Kinematics,
            KinematicsName,
            PolarKinematics,
            ScaraKinematics,
        )

        expected_types = {
            KinematicsName.cartesian: CoreKinematics,
            KinematicsName.coreXY: CoreKinematics,
            KinematicsName.markForged: CoreKinematics,
            KinematicsName.linearDelta: DeltaKinematics,
            KinematicsName.rotaryDelta: Kinematics,
            KinematicsName.hangprinter: HangprinterKinematics,
            KinematicsName.fiveBarScara: ScaraKinematics,
            KinematicsName.scara: ScaraKinematics,
            KinematicsName.polar: PolarKinematics,
            KinematicsName.unknown: Kinematics,
        }
        for name, expected_type in expected_types.items():
            kinematics = Kinematics.get_kinematics_type(name)
            self.assertIs(type(kinematics), expected_type, name)
            self.assertEqual(kinematics.name, name)

        # Names reported by RRF are normalized
        self.assertIs(type(Kinematics.get_kinematics_type("Core XY")), CoreKinematics)
        self.assertEqual(Kinematics.get_kinematics_type("Rotary Delta").name, KinematicsName.rotaryDelta)
        self.assertRaises(ValueError, lambda: Kinematics.get_kinematics_type("not a kinematics"))

    def test_plugins(self):
        model = ObjectModel()
        self.assertEqual(len(model.plugins), 0)

        # Plugin installation
        json_patch = '{"plugins":{"ExecOnMcode":{"dsfFiles":["execOnMcode.py","http_endpoints.py","MCodeAction.py","__init__.py"],"dwcFiles":["js/ExecOnMcode.09113059.js","js/ExecOnMcode.09113059.js.gz","js/ExecOnMcode.09113059.js.map","js/ExecOnMcode.09113059.js.map.gz"],"sdFiles":["sys/ExecOnMcode/top-example.py"],"pid":-1,"id":"ExecOnMcode","name":"ExecOnMcode","author":"Lo\u00efc GRENON","version":"0.2","license":"GPL-3.0-or-later","homepage":"https://github.com/LoicGRENON/DSF_ExecOnMcode_Plugin","tags":[],"dwcVersion":"3.4.5","dwcDependencies":[],"sbcRequired":true,"sbcDsfVersion":"3.4.5","sbcExecutable":"execOnMcode.py","sbcExecutableArguments":null,"sbcExtraExecutables":[],"sbcOutputRedirected":true,"sbcPermissions":["commandExecution","codeInterceptionRead","registerHttpEndpoints","fileSystemAccess","launchProcesses"],"sbcPackageDependencies":[],"sbcPythonDependencies":["dsf-python\u003e=3.4.5"],"sbcPluginDependencies":[],"rrfVersion":null,"data":{}}}}'
        model.update_from_json(json_patch)
        self.assertEqual(len(model.plugins), 1)
        self.assertIsInstance(model.plugins.get("ExecOnMcode"), Plugin)
        self.assertEqual(len(model.plugins["ExecOnMcode"].dsf_files), 4)
        self.assertEqual(len(model.plugins["ExecOnMcode"].sbc_permissions), 5)
        self.assertEqual(model.plugins["ExecOnMcode"].pid, -1)

        # Plugin start
        json_patch = '{"plugins":{"ExecOnMcode":{"pid":1125}}}'
        model.update_from_json(json_patch)
        self.assertEqual(model.plugins["ExecOnMcode"].pid, 1125)

        # Plugin removal
        json_patch = '{"plugins":{"ExecOnMcode":null}}'
        model.update_from_json(json_patch)
        self.assertEqual(len(model.plugins), 0)

    def test_sensors_filament_monitor(self):
        from src.dsf.object_model.sensors.filament_monitors import FilamentMonitorType

        model = ObjectModel()
        self.assertEqual(len(model.sensors.filament_monitors), 0)

        # Change filament monitor to Simple (eg: M591 D0 P1 C"io2.in" S1)
        json_patch = '{"sensors":{"filamentMonitors":[{"enabled":true,"status":"ok","type":"simple"}]}}'
        model.update_from_json(json_patch)
        self.assertEqual(len(model.sensors.filament_monitors), 1)
        filament_monitor = model.sensors.filament_monitors[0]
        assert filament_monitor is not None
        self.assertEqual(filament_monitor.type, FilamentMonitorType.Simple)

        # Change filament monitor to Pulsed (rg: M591 D0 P7 C"io2.in" S1)
        json_patch = '{"sensors":{"filamentMonitors":[{"calibrated":null,"configured":{"mmPerPulse":1,"percentMax":160,"percentMin":60,"sampleDistance":5},"enabled":true,"status":"ok","type":"pulsed"}]}}'
        model.update_from_json(json_patch)
        self.assertEqual(len(model.sensors.filament_monitors), 1)
        filament_monitor = model.sensors.filament_monitors[0]
        assert filament_monitor is not None
        self.assertEqual(filament_monitor.type, FilamentMonitorType.Pulsed)

    def test_get_filament_monitor(self):
        from src.dsf.object_model.sensors.filament_monitors import (
            FilamentMonitor,
            FilamentMonitorType,
            LaserFilamentMonitor,
            PulsedFilamentMonitor,
            RotatingMagnetFilamentMonitor,
        )

        expected_types = {
            FilamentMonitorType.Laser: LaserFilamentMonitor,
            FilamentMonitorType.Pulsed: PulsedFilamentMonitor,
            FilamentMonitorType.RotatingMagnet: RotatingMagnetFilamentMonitor,
            FilamentMonitorType.Simple: FilamentMonitor,
            FilamentMonitorType.Unknown: FilamentMonitor,
        }
        for monitor_type, expected_type in expected_types.items():
            # Both the enum and its JSON string value are accepted
            for type_ in (monitor_type, monitor_type.value):
                monitor = FilamentMonitor.get_filament_monitor(type_)
                self.assertIs(type(monitor), expected_type, type_)
                self.assertEqual(monitor.type, monitor_type)

        self.assertRaises(ValueError, lambda: FilamentMonitor.get_filament_monitor("not a monitor"))

    def test_sensors_filament_monitor_rc2_fields(self):
        from src.dsf.object_model.sensors.filament_monitors import RotatingMagnetFilamentMonitor

        model = ObjectModel()
        model.update_from_json(
            '{"sensors":{"filamentMonitors":[{"type":"rotatingMagnet","filamentPresent":true,"agc":120,'
            '"calibrated":{"mmPerRev":28.8,"percentMax":110,"percentMin":90,"totalDistance":100}}]}}'
        )
        monitor = model.sensors.filament_monitors[0]
        assert isinstance(monitor, RotatingMagnetFilamentMonitor)
        self.assertTrue(monitor.filament_present)
        self.assertEqual(monitor.agc, 120)
        assert monitor.calibrated is not None
        self.assertEqual(monitor.calibrated.mm_per_rev, 28.8)

    def test_user_sessions(self):
        from src.dsf.object_model import AccessLevel, SessionType

        model = ObjectModel()
        json_patch = '{"sbc": {}}'
        model.update_from_json(json_patch)

        assert model.sbc is not None
        self.assertEqual(len(model.sbc.dsf.user_sessions), 0)

        json_patch = '{"sbc":{"dsf":{"userSessions":[{"accessLevel":"readWrite","id":2,"origin":"::ffff:192.168.1.200","originId":-1,"sessionType":"http"}]}}}'
        model.update_from_json(json_patch)
        self.assertEqual(len(model.sbc.dsf.user_sessions), 1)
        self.assertEqual(model.sbc.dsf.user_sessions[0].access_level, AccessLevel.readWrite)
        self.assertEqual(model.sbc.dsf.user_sessions[0].session_type, SessionType.http)


if __name__ == "__main__":
    unittest.main()
