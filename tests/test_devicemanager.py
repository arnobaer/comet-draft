import unittest
import env

from pyvisa import ResourceManager

from comet import DeviceManager

class DeviceManagerTestCase(unittest.TestCase):
    def setUp(self):
        rm = ResourceManager('@sim')
        self.manager = DeviceManager(rm)

class BasicDeviceManagerTestCase(DeviceManagerTestCase):
    def runTest(self):
        manager = self.manager
        self.assertEqual(manager.factory.__class__.__name__, 'DeviceFactory')
        self.assertEqual(type(manager.devices), dict)
        device = manager.create('SMU1', 'GPIB::16', {'get_value': {'method': 'query', 'message': 'VALUE?'})
        self.assertTrue(device is manager.get('SMU1'))
        self.assertEqual(device.name, 'SMU1')          
        self.assertEqual(device.get_value.method, 'query')
        self.assertEqual(device.get_value.message, 'VALUE?')

if __name__ == '__main__':
    unittest.main()
