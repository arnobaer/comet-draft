import unittest
import env

from comet import DeviceManager

class DeviceManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.manager = DeviceManager()

class BasicDeviceManagerTestCase(DeviceManagerTestCase):
    def runTest(self):
        manager = self.manager
        self.assertEqual(manager.factory.__class__.__name__, 'DeviceFactory')
        self.assertEqual(type(manager.devices), dict)
        manager.create('SMU1', {'name': 'keithley1234'})
        device = manager.get('SMU1')

if __name__ == '__main__':
    unittest.main()
