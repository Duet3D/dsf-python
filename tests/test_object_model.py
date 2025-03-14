import json
import unittest

from src.dsf.object_model import *
from src.dsf.object_model.utils import is_model_object
from src.dsf.object_model.object_model import ModelCollection, ModelDictionary, ModelObject


class Model(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def test_boards(self):
        model = ObjectModel()

        json_patch = '{"boards": [{"accelerometer": null, "bootloaderFileName": null, "canAddress": 0, "closedLoop": null, "directDisplay": null, "firmwareDate": "2022-11-30", "firmwareFileName": "Duet3Firmware_Mini5plus.uf2", "firmwareName": "RepRapFirmware for Duet 3 Mini 5+", "firmwareVersion": "3.4.5", "iapFileNameSBC": "Duet3_SBCiap32_Mini5plus.bin", "iapFileNameSD": "Duet3_SDiap32_Mini5plus.bin", "maxHeaters": 32, "maxMotors": 7, "mcuTemp": {"current": 33.1, "max": 33.6, "min": 19.4}, "name": "Duet 3 Mini 5+", "shortName": "Mini5plus", "state": "unknown", "supports12864": true, "supportsDirectDisplay": true, "uniqueId": "F8AU7-6P6KL-K65J0-409N2-KKW1Z-Z5W3W", "v12": null, "vIn": {"current": 19.4, "max": 19.4, "min": 19.3}}]}'
        model.update_from_json(json_patch)

        # Voltage change
        json_patch = '{"boards":[{"vIn":{"current":42.5}}]}'
        model.update_from_json(json_patch)
        # Check if the value has been modified
        self.assertEqual(model.boards[0].v_in.current, 42.5)
        # Check if other values has not been altered
        self.assertEqual(model.boards[0].v_in.min, 19.3)
        self.assertEqual(model.boards[0].v_in.max, 19.4)

    def test_http_endpoints(self):
        from src.dsf.object_model import HttpEndpointType
        model = ObjectModel()

        json_patch = '{"sbc":{"dsf":{"httpEndpoints":[{"endpointType":"GET","namespace":"ExecOnMcode","path":"getCmdList","isUploadRequest":false,"unixSocket":"/run/dsf/ExecOnMcode/getCmdList-GET.sock"}]}}}'
        model.update_from_json(json_patch)
        self.assertEqual(len(model.sbc.dsf.http_endpoints), 1)
        self.assertEqual(model.sbc.dsf.http_endpoints[0].endpoint_type, HttpEndpointType.GET)

        json_patch = '{"sbc":{"dsf":{"httpEndpoints":[{},{"endpointType":"POST","namespace":"ExecOnMcode","path":"saveCmdList","isUploadRequest":false,"unixSocket":"/run/dsf/ExecOnMcode/saveCmdList-POST.sock"}]}}}'
        model.update_from_json(json_patch)
        self.assertEqual(len(model.sbc.dsf.http_endpoints), 2)
        self.assertEqual(model.sbc.dsf.http_endpoints[1].endpoint_type, HttpEndpointType.POST)

    @staticmethod
    def test_job():
        model = ObjectModel()
        json_patch = '{"job":{"file":{"filament":[496.4],"fileName":"0:/gcodes/Veil_Token.gcode","generatedBy":"ideaMaker 4.2.1.5321, 2022-10-01 17:45:38 UTC\u002B0200","height":1.04,"lastModified":"2022-10-01T16:45:39+01:00","layerHeight":0.12,"numLayers":9,"printTime":798,"size":594195,"thumbnails":[{"data":"iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAYAAACtWK6eAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAUnklEQVR4nO3cfYwcZ30H8O/zzMy\u002B3d77nl\u002BuztmOA7bjGIOdBBJioDSEJkBLStOWCERTaKS2alWkqqioqpD6BxSVSlUFaktVggRUjdomBVIaikrA4Y9AYkhsY5vEdnz2\u002Bezz3u3e3b7OzPP8\u002BsfM7O5dfMmdb\u002B9s1O9HWu3u3e7s8/xmnmeefZ7fLEBERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERET0/5261gXoljuA7N5cbuADw8PDU8bc6Isa3eJ5W3MaY/NWxiyQ6Xy9o1D0gCPnguBwv8jzvzY5\u002BTMAZq3L\u002BdG\u002BvqFfHRjYXDVmm0Dv2p72bimFZswCfZ2vc4GL/a5TnPTDM0UTHBtynBe/cv78\u002BOPALABZyzI\u002BAKTev2XL1poxb96bzR4oGbPLCAqdr3GgZvIaxZrF\u002BIwJpozIsY1aTz5Vr8/86/R08SWguZZlXC8/bw1E/3ImM3ZTOl24v39ot6OlcNmYnSOOuzWj9Zhv7UBW62FHqfRKNhpYWw1FXihZ84ILPPfVmZmnD1UqZ14GGqsp7Ad7e3ftdDOFd/f37r0Qhrs3uu4tWmGbo9RmT6nMa2\u002Bho4wijcDKBJRMzBjzk4xS4yfqwZGvz5dOfKdeH19NObcBmXv7\u002B/f81tDQnlIY3j7ierc5Su1MKdW/ku0YEb8pMuMpVZwJzZmGmHP9jvPSdBiePV71L/1naer0c8AlAHY15V1P13MDcf9\u002B4\u002BgDe3PpA3PW7negtg05zphWylmPDw9FmpNheOT5pvmdv7h0/shy3vO5jRt/6U2Z7IMN4NYRx9ntKOWtdTkBwIgEZWtOOMDh5xuNRz5\u002B8eJTy3nfp0dGbtqTyf3TJs99i7vCTuVqWREzY8y4hfxUizo6EQTHHpqc\u002BBcA4Xp8/kq517oAS9kDFLbkMl/2Fby840IjGv9YCBwAapVtOxRBAKAR39cB1CBoCDAnghIkXYXcOuXhLQCW1UC2ZHMPV5X6jawCqgBcicqqASgV3etVlltE0ABQhyAQYD6qg1cS7J2B7J1PpXIAnlrOtvqy2V9sOM7bp0TgQpCOy\u002BcAXS\u002B3FUETQAA4Ruvt88D2WbHvuZzyghHgfy4DF1f1AWvkum0gBghqgPgAVDzkFgAi0c1CoBGdq6ObwALQEj03AHwAAQQmfh5K1BCa8d8CAUIIfCzdffnG9Cy3zGVryspxkZQ5OaQ6yy1xXRTaDd7Gz61Erw0A\u002BB3lDgD4EjWKMC53gKihLB6rNMKwvNzyVq3NDTiCGhS0ADXVjvXiciOJL64Q87jsFlHM/bicSYxriMrrx/FuoP1lTwA0oipel67bBnICmC4a89NhR7/RU\u002B3zhQPAU4AjUeG1UlFPF/d8RgFGJD4jALMiKCNuICra2dHWXv17btPaSSvybDkMv7ncMp8Kgie3KvX\u002BYa03uAAcpRZ8SudjF0AWQEopaChoCBwV1TIQgYFCFdFZbTbufTu3caX\u002BvGnMuZLvf3e55X252XxCtL4rB/XOfkcPZSQq81LnCgFajdbGdeiBQkZF\u002B8WN94UPgZXoW3pNAVURVACUICjLwjiE1k7NA9PLLfN6u\u002B6\u002BgxwAvAO5XOGegYH\u002BqtXbJ8Tcf3M285sbtO7zgNZBtFwighqAM2LxsrG1sshpUWjOh\u002BHlukgttPYylJpztJ4GcPbM/Pz4nO9PHWs2X7rKKqjtmczYrb29u/dlMjdWwvCmPq1vvzGVunVIqXQvFFIA1FXUowzBRSu4LNJ80fefvWzN0XwqdWSiWj014ftnj1YqJ3CVM1w3AKP7h4dvvjGdLvRovdUDsr6VMc/RhR7AS2t3REFcLbJjm\u002BPkB5RCdoV1AKLGXxZBSezseL35RI\u002BSxzamUse/MzNz\u002BUeVSum56\u002Bxsci0biP5gPr97fyY/ckdv9pZJP9zd7zqb\u002Bx29o2mlkFaq39N62cOb5QhFalVrjzTF/qDkm6c/O3n\u002B6R8Dl7u1/T1A6s6BgZvv7\u002B3fXxO7f4Pr7nCV2hHPWuW79TkA0BSpiMhkzdpTc8YeySh14ofV\u002Bol/n5k6fgQodetzHsrnR27v7d0/6qbuGXKdNztK7ct0uS6\u002BSCMUuewoTJVDe6Eu5uQG1z17rF4/81i5fOxMozF9Mvq6te7WvIE8DHj3jI7uKAP7tzjeLqtx0IXaup4zUktJZn\u002BKYfiZD54//7WVvv/RTZtGqlq/64ZU6h4ruKPguq9fi3KuVDEMT3gK3zvj\u002B9/7WbX635\u002BZnV1xg3l0dOxdQ57\u002BqyHXfdNalHElRMRMxzNfrqijE37wbI\u002BWo1\u002B\u002BcGH8G9FIes2sdQNRj90w9s\u002BjrvtAt88G3VASi6IITlv52Z\u002BdfXnnSt//lRtu\u002BPwOL/X76asYaqyHkrX2ULPx\u002BU9duPBHK33vf2y/8eSgUq/PAfCuw/oF1laPBsG3P3r\u002B3Aewhguna/4lfUphq6fQkxULr2MKUcU3Hb9OYeXj8oQVac2sJF8gQ8QzVALMQ1AXoBLfz8Tj\u002BdYMkFxdfC8DPSkRpOIp0lRcNzeup1rqdpX1FJFW/Vozc4jG9fMQ1AQoQ6L6Rd\u002B99LzIihb7EnPxdLKLaLo6paLHHgBn8VRw/J5u7c/F9UxmxxoiKMV1nRDpOWvtwFV9wAqsdQMRALUmgM7p2k4qntWIpjmjg9aJ3yhoTylK6z4Kni/tqcQQ0RRugKhRROsb0XRuGP9/LZZujbVVdGy/vey\u002BqJ6CBfNmItFkb3IwJfVLpj7b94IgXqdpN4aongGima1mXM8A3c2T6ayBRTQjFe3Dxf9d\u002BKYF84PS7oSS6WHE5Wzvz/Z0cT1\u002BfYB2Pf14Gr7WXkdpl0ut7fAKWIcziAAXjAhcqFZXI0vcTMe7kgCGglZDMPF/Og96A8BIcgBJ6\u002BzRebAsdX4wIjURGZ8Ngr\u002B5mrqVQ3my37W/3qvVBhfRYlpnp7m4fp0HSNLYk78paZfZR3JQLjwzBvFaQ4D2gfRqDd\u002BKzDZEnrqauh2u1z51UyrzibxWO3NaZVyJG/SiaWDpuL9SfTsbQVK/UBY3wPY\u002B9RGt\u002BST1TOp9pX3oiExi6d3bFWs\u002BuPxQobD59ZnM72aBd/c6zu6s1oMpAJl4ujM6dSt4aJ\u002Buk1tnkGvxesa0CBrxAZIsogFR0P24B/I7/t9asLK20rD2rIgUNXBo1pgTPY5z\u002BKnJyfFL0cL3Vflwf//2kVzu7hHPO\u002BiJ7MxovTOndX8a7d4nOVskS4QeoszJlFJIoz1USSR1DhD1qqV4LaQs7UXCEO0GlBxcgbWzDWvHHeCFWWO\u002BB2O\u002B//Vi8eTV1u2tQO8bN20aE\u002BC2Ta672wH2aqV29yldSDs676E9rExGAUl9BQpGBKJUqzNQAHoB5KGQUapV784GZeI61xEN8yoQXBDBXDxi8K2drxlzGMCTl\u002Br1r/1vuXz2auu3HGvaQA4A3tuGhzfcmU5vnbdq37Z06kBTyX0j2tmsV/F9Y0IEzwT\u002BibKVFw2AmjWXrUgQaF33gGLW8y7XwnDuzPz8eN3a2ulqdXwOmOlu7ZakCsCmsZ6ekd3Z7NimVHZsg6vu3KjUfdscd7AHK1/LSRgRXBLBuNj5s2H4jUlrf1D0/fGLtdrkbK127hQw1d2qLK0PGBpNpws78vmxbel0YcB1\u002B\u002BrGjAiQs9YOp5TyUsoZCWGRh9ryhpS3b1RpvZq6F62dTAv\u002BayoMn3PEPH\u002B60Rh/dGbm0lqunXS1gbwZ6Hvn0NCet\u002Bfzt9dE7dvkOfuMYDSr1Ei3p3RDkYuTgf/Xf3Du3BfORxkk14178/mRB3sHDuRd9Z4R1zvoKbWj2\u002BsgRqTZsPbEnLGHG7CP/\u002BW5c9//CbDsNJP18NG\u002BvqEHh4b\u002BNK/1RzylN3Vz21bENEWKSmFiJgyPOMDhI43Gc1\u002Bemnr\u002BGFDp1uesuIE8APQf3LCh8LpMZvOFwNxycyZ1c9nYPVmtd/U5zmi3CrZcgUhlKgwe88PwH57x/Rc\u002BWyyu64LSA\u002Bgbeu8v9Baswb4tae\u002BOQHDXJs\u002B9bT3LAAC\u002BtbU5Y486GofP\u002B/5TvSIvfHFycuJbwNx6luPhwcH\u002Bd\u002BRyB4Zc9z2DjvtwtzuG12JFTMmYs0m28LgfHO918OKpqpn8t/LFqedWuG7yqg3kvp6eTQezvbsOxivdoylvL4DNAApZrdd8im0lrIgJIadKoXlyyg8f\u002B8jFiaewBl/gfhvI3DC44cBbezNv9ZRzMK2wx9G6kFaqt9uftRqBtTUDTNStnAzEHDru\u002Bz/8\u002BMWLT2ON0sq/uGHLG0Yy\u002BmMbXfdeD2qrXqdU/\u002BUwIsa3tqyUnhJIsRSaIwOuPn6k0XjxC5OTP3y1zINWA3konx95b3//Dqv1XQPafbuI7Cx47uvWpwrd93LT/9svnh//xLe6cGXbh4Ge\u002BzZvuWc45dzf67j3p9e5V\u002ByWpkilFAZP1EJ8db42d\u002BihcnnVQ7J7gfTHbhj7zPZU6o\u002B7UcZroWzMORE8M2PDZ7S1T39zdvbUlyqVywCgPjcy8qa9ufwnc1rdntF6VF/HGb4rMWNt7dH5uYP/WCweXs12HkT/4MPbhh7vc5y3dats14M5a559ZGrqfY9Uq6u6DuOThcL\u002Bu3v7Dg1onetW2a4lC4QNay8YkR\u002BfrQefdm/L5w/ltXPdpYGsVF0ENQguWMEZsThvrb4osurGXs36\u002BWlgVzpeTV7thVrXmolTz58xduxH1qZWu72667qnxerh\u002BKL6rIqn7H9OY6UBN6f1GICxjVm5zT0vUtssticLhdR1mHNzJbMirfWBmTj9IE6taC\u002B8AalCOn1VaRaLzYlARJABkIUgHa/huD8n8ZqL4zMpFhPx44rtTm7B9lSqzwFSNURjWUcEHqKUlBQEXrzu4\u002BHnK15nrMXzYQi3Ya1f0hplCLREOUUu4guToOLLLV\u002BZO3W16xiJzvyp5JYs6vkiqMbpE1WJFglnEDWKOazDT49cqbyI0lf8jqvudHxJbZSf1M7BWpxr1o08rFY5pL0IKuiIGQRVARoQVASYE4uyANMdK9hrISlHolUmAZoq\u002BksrV0ukdWxpxBe8IYrb4uOs8wZ073hLshiCuJxVEdQRdRpFEUyLtFaNayJww45pL4v2gkK0uinxFXgLSVxZwcK8KWBhwDp3TAhBKFF\u002BUeelpBbR6rBBx6Ww8TaSlISw4z3LnZZqWnvyTLl8dJkvX1Idr0znaOWOoR1sif8TX526YGUZ6MhR6sg3S7aBjm0lj9sxlDjPbGH2QCjty4o7L3E1EqVu\u002BGgfDFeigBBa\u002BysIxRUdKhaP3VUYOTekZasDAK9yIAuSPLL28\u002Bg\u002Bjl5HLldnAuSrxa0zRakzncfGcVucVeHHcWtdvowkVenKl1477\u002Brr\u002B5VerW9cnGOzWGdOUCu1IU6YawCt\u002B7q0n1fjvzUQZdI247/XEe3YprRbchgXOAlIZ6Ozi54vWUaRWihyrBaGj5wulf7wB/X6hdd4y2s6FYZz\u002B3pytZyjb3cVeqIfMlje6LozVWZh3NrXlCex6oxbDVGMGgCqiIaOPhbGLdlOiKXz2paKmRWplcLwT75fKj298ogsdDwIKi/Ozn5pIJud11oPWaUKWsFpHeDLjBXwyv19pbglyYtJrJqS/M4AWpdZNxBdqpwM\u002BxqIGkYD7QZqlviszng1rP2u\u002BvPR0Z0DjvN3Gxz37nzHeaydebpwQ7Joo0nCXfL6zkS0zvV/v9XHtndq8trkBwCS1pskIobSfu\u002BVKiAiUjXmuKfU8Wnff8JT6vCpqamXXlhFbtVSPjQyctP2dPrBLPT9w67e3a9U2ot3vY6vdRcAUO2YXSl5r93LyYKzhpH24yQ\u002B0eOOJD8sjFv7\u002BvCFP0wh8fB0cRZzzZijxtqv1YPg248Xi891KzYdUr\u002B3efNeR\u002BQNo573bgXsH3Scm3Iq\u002BhEwpyOZU2FRzLAwbsArz6jJ8QZ0nDWk3evbjr8nI5XW8SYLE1zDeEvJGSTJb0u2VTfmmZlK5cFWg3jf8PBtr0ulDg647jt6tN6RgRrJajWgAc/rGGZ17ujWc5WcBheePtunK1mQeRpIu0EIol/ESM4incMvI9IIrZ0VpSqi1GQ1DMcNMO4AP51oNE6fKZWOn1\u002B/HKuWXmD4/Rs33jnqeXvSSr1lUDtbNWTAgxpOK/Q4SmkH0S\u002BsJGnenb15q9GoOCayuFG0h2wL47ZwqGkk6Q0lGffbhtiyAWpa62IlDE8KcHKm2Tx0qlY78VK9fn6tY7PYENC3t69v596enp2eUnuyWu/q17rgKFXwgMG0UjkPqtdRHUmbi\u002BKW/OrLgs4mPiCtLGwUUawUgrgBSEeMWo2j43hrAIFv7awAMzVrf\u002BIAh8/U6986VCq9ACy9kp69e3Bw5I09PQPlMNziAje6WhcKrru5bm1BATkLFFwRV5Te4Kjkug6B0npQK5WNfpoH4lsz2dm7ATIXiFQCEau0vqSUqqS1nq8bU5kNw/HAmFoITA6m00VrzPzp2dnZS/V65eXrLM9oEWdXb\u002B/A7nR6eGsqlZ81ZhTWjmQ9b6zfcQoudM634YhA9SlBj1LoVUr1JuNpA1Epx9mcNBYLII6btNL5xV4KAWOVqgowl9b6cihSK/n\u002BeN3asmg9vcF1X56oVksXwrB2tFot4trMZyzLRqBnWzY7ONrTk9ueTg8Vw7Cggc09WhdcIDfoeRsq1m50RWkL2egoaCXIi1J9UVJf1IV4UdxU0tEG1l60EBsPo5rW2ul4pbgIpWppxynONJvjVWOmoFR5IJ0\u002Beb5SmZ0ol2eu1XXvRERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERNe3/wOxabcDNmswcQAAAABJRU5ErkJggg==","format":"png","height":200,"offset":483,"size":7144,"width":200}]},"build":{"currentObject":-1,"m486Names":false,"m486Numbers":false,"objects":[]},"duration":0,"pauseDuration":0,"rawExtrusion":0,"warmUpDuration":0,"layers":[],"lastDuration":null}}'
        model.update_from_json(json_patch)

    def test_json_serialization(self):
        with open('tests/object_model/model_full.json') as fp:
            json_data = json.load(fp)
        model = ObjectModel.from_json(json_data)

        def recursive_compare(obj1, obj2):
            if isinstance(obj1, dict):
                self.assertIsInstance(obj2, dict)
                self.assertEqual(set(obj1.keys()), set(obj2.keys()))
                for key in obj1:
                    recursive_compare(obj1[key], obj2[key])
            elif isinstance(obj1, list):
                self.assertIsInstance(obj2, list)
                self.assertEqual(len(obj1), len(obj2))
                for item1, item2 in zip(obj1, obj2):
                    recursive_compare(item1, item2)
            elif isinstance(obj1, ModelObject):
                self.assertIsInstance(obj2, ModelObject)
                recursive_compare(obj1.__dict__, obj2.__dict__)
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
        from src.dsf.object_model.move.kinematics import CoreKinematics, DeltaKinematics, KinematicsName

        model = ObjectModel()
        json_patch = '{"move": {"kinematics": {"name": "delta","deltaRadius": 123}}}'
        model.update_from_json(json_patch)

        self.assertIsInstance(model.move.kinematics, DeltaKinematics)
        self.assertEqual(model.move.kinematics.name, KinematicsName.delta)
        self.assertEqual(model.move.kinematics.delta_radius, 123)

        # Switch to CoreXY (eg: M669 K1)
        json_patch = '{"move":{"kinematics":{"forwardMatrix":[[0.5,0.5,0],[0.5,-0.5,0],[0,0,1]],"inverseMatrix":[[1,1,0],[1,-1,0],[0,0,1]],"tiltCorrection":{"correctionFactor":1,"lastCorrections":[],"maxCorrection":1,"screwPitch":0.5,"screwX":[],"screwY":[]},"name":"coreXY","segmentation":null}}}'
        model.update_from_json(json_patch)
        self.assertIsInstance(model.move.kinematics, CoreKinematics)
        self.assertEqual(model.move.kinematics.name, KinematicsName.coreXY)

        # Switch to linear delta (eg: M669 K3)
        json_patch = '{"move":{"kinematics":{"deltaRadius":105.6,"homedHeight":240,"printRadius":80,"towers":[{"angleCorrection":0,"diagonal":215,"endstopAdjustment":0,"xPos":-91.452,"yPos":-52.8},{"angleCorrection":0,"diagonal":215,"endstopAdjustment":0,"xPos":91.452,"yPos":-52.8},{"angleCorrection":0,"diagonal":215,"endstopAdjustment":0,"xPos":0,"yPos":105.6}],"xTilt":0,"yTilt":0,"name":"delta","segmentation":null}}}'
        model.update_from_json(json_patch)
        self.assertIsInstance(model.move.kinematics, DeltaKinematics)
        self.assertEqual(model.move.kinematics.name, KinematicsName.delta)
        self.assertEqual(model.move.kinematics.delta_radius, 105.6)

    def test_plugins(self):
        model = ObjectModel()
        self.assertEqual(len(model.plugins), 0)

        # Plugin installation
        json_patch = '{"plugins":{"ExecOnMcode":{"dsfFiles":["execOnMcode.py","http_endpoints.py","MCodeAction.py","__init__.py"],"dwcFiles":["js/ExecOnMcode.09113059.js","js/ExecOnMcode.09113059.js.gz","js/ExecOnMcode.09113059.js.map","js/ExecOnMcode.09113059.js.map.gz"],"sdFiles":["sys/ExecOnMcode/top-example.py"],"pid":-1,"id":"ExecOnMcode","name":"ExecOnMcode","author":"Lo\u00EFc GRENON","version":"0.2","license":"GPL-3.0-or-later","homepage":"https://github.com/LoicGRENON/DSF_ExecOnMcode_Plugin","tags":[],"dwcVersion":"3.4.5","dwcDependencies":[],"sbcRequired":true,"sbcDsfVersion":"3.4.5","sbcExecutable":"execOnMcode.py","sbcExecutableArguments":null,"sbcExtraExecutables":[],"sbcOutputRedirected":true,"sbcPermissions":["commandExecution","codeInterceptionRead","registerHttpEndpoints","fileSystemAccess","launchProcesses"],"sbcPackageDependencies":[],"sbcPythonDependencies":["dsf-python\u003E=3.4.5"],"sbcPluginDependencies":[],"rrfVersion":null,"data":{}}}}'
        model.update_from_json(json_patch)
        self.assertEqual(len(model.plugins), 1)
        self.assertIsInstance(model.plugins.get('ExecOnMcode'), Plugin)
        self.assertEqual(len(model.plugins['ExecOnMcode'].dsf_files), 4)
        self.assertEqual(len(model.plugins['ExecOnMcode'].sbc_permissions), 5)
        self.assertEqual(model.plugins['ExecOnMcode'].pid, -1)

        # Plugin start
        json_patch = '{"plugins":{"ExecOnMcode":{"pid":1125}}}'
        model.update_from_json(json_patch)
        self.assertEqual(model.plugins['ExecOnMcode'].pid, 1125)

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
        self.assertEqual(model.sensors.filament_monitors[0].type, FilamentMonitorType.Simple)

        # Change filament monitor to Pulsed (rg: M591 D0 P7 C"io2.in" S1)
        json_patch = '{"sensors":{"filamentMonitors":[{"calibrated":null,"configured":{"mmPerPulse":1,"percentMax":160,"percentMin":60,"sampleDistance":5},"enabled":true,"status":"ok","type":"pulsed"}]}}'
        model.update_from_json(json_patch)
        self.assertEqual(len(model.sensors.filament_monitors), 1)
        self.assertEqual(model.sensors.filament_monitors[0].type, FilamentMonitorType.Pulsed)

    def test_user_sessions(self):
        from src.dsf.object_model import AccessLevel, SessionType

        model = ObjectModel()
        json_patch = '{"sbc": {}}'
        model.update_from_json(json_patch)

        self.assertEqual(len(model.sbc.dsf.user_sessions), 0)

        json_patch = '{"sbc":{"dsf":{"userSessions":[{"accessLevel":"readWrite","id":2,"origin":"::ffff:192.168.1.200","originId":-1,"sessionType":"http"}]}}}'
        model.update_from_json(json_patch)
        self.assertEqual(len(model.sbc.dsf.user_sessions), 1)
        self.assertEqual(model.sbc.dsf.user_sessions[0].access_level, AccessLevel.readWrite)
        self.assertEqual(model.sbc.dsf.user_sessions[0].session_type, SessionType.http)


if __name__ == '__main__':
    unittest.main()
