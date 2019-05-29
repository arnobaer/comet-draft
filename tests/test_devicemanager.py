import unittest
import env

from pyvisa import ResourceManager

from comet.device import DeviceManager

class DeviceManagerTestCase(unittest.TestCase):
    def setUp(self):
        rm = ResourceManager('@sim')
        self.manager = DeviceManager(rm)

class BasicDeviceManagerTestCase(DeviceManagerTestCase):
    def runTest(self):
        manager = self.manager
        self.assertEqual(manager.factory.__class__.__name__, 'DeviceFactory')
        self.assertEqual(type(manager.devices), dict)
        config = {'routines': {'get_value': {'method': 'query', 'message': 'VALUE?'}}}
        device = manager.create('SMU1', 'GPIB::16', config)
        self.assertTrue(device is manager.get('SMU1'))
        self.assertEqual(device.name, 'SMU1')
        self.assertEqual(device.get_value.method, 'query')
        self.assertEqual(device.get_value.kwargs.get('message'), 'VALUE?')

if __name__ == '__main__':
    unittest.main()
