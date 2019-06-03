import unittest
import env

from pyvisa import ResourceManager

from comet.device import DeviceManager
from comet.device import DeviceCommand

class DeviceManagerTestCase(unittest.TestCase):
    def setUp(self):
        rm = ResourceManager('@sim')
        self.manager = DeviceManager(rm)

class BasicDeviceManagerTestCase(DeviceManagerTestCase):
    def runTest(self):
        manager = self.manager
        self.assertEqual(manager.factory.__class__.__name__, 'DeviceFactory')
        self.assertEqual(type(manager.devices), dict)
        device = manager.create('DUMMY', 'GPIB::14', {})
        self.assertEqual(device.__class__.__name__, 'Device')
        self.assertEqual(device.name, 'DUMMY')
        device = manager.get('DUMMY')
        self.assertEqual(device.__class__.__name__, 'Device')
        self.assertEqual(device.name, 'DUMMY')
        config = {'commands': {'get_value': {'method': 'query', 'message': 'VALUE?', 'description': 'query value'}}}
        device = manager.create('SMU1', 'GPIB::16', config)
        self.assertEqual(device.__class__.__name__, 'Device')
        self.assertTrue(device is manager.get('SMU1'))
        self.assertEqual(device.name, 'SMU1')
        self.assertEqual(device.get_value.method, 'query')
        self.assertEqual(device.get_value.kwargs.get('message'), 'VALUE?')
        self.assertEqual(device.get_value.description, 'query value')

class DeviceCommandTestCase(DeviceManagerTestCase):
    def runTest(self):
        """This test depends on the default shipped pyvisa-sim configuration (device 1)."""
        device = self.manager.create('SMU', 'ASRL1::INSTR', {'read_termination': '\n'})

        # query command
        kwargs = {'message': '?FREQ'}
        command = DeviceCommand('get_frequency', 'query', **kwargs)
        self.assertEqual(command.name, 'get_frequency')
        self.assertEqual(command.method, 'query')
        self.assertEqual(command.require, None)
        self.assertEqual(command.description, '')
        result = command(device)
        self.assertEqual(result, '100.00')

        # query command with require and description
        kwargs = {'message': '?FREQ', 'require': '.*((\d+)\.(\d+))$', 'description': 'get frequency'}
        command = DeviceCommand('get_frequency', 'query', **kwargs)
        self.assertEqual(command.name, 'get_frequency')
        self.assertEqual(command.method, 'query')
        self.assertEqual(command.require, '.*((\d+)\.(\d+))$')
        self.assertEqual(command.description, 'get frequency')
        result = command(device)
        self.assertEqual(result, '100.00')

        # query command
        kwargs = {'message': 'NONE', 'require': '(ERROR)(\n?)$',}
        command = DeviceCommand('get_none', 'query', **kwargs)
        self.assertEqual(command.require, '(ERROR)(\n?)$')
        result = command(device)
        self.assertEqual(result, 'ERROR')

        # query command
        kwargs = {'message': '!FREQ {:.2f}', 'require': 'OK', 'description': 'set frequency'}
        command = DeviceCommand('set_frequency', 'query', **kwargs)
        self.assertEqual(command.method, 'query')
        self.assertEqual(command.description, 'set frequency')
        result = command(device, 4.2)
        self.assertEqual(result, 'OK')
        result = device.query('?FREQ')
        self.assertEqual(result, '4.20')

        # query_ascii_values command
        kwargs = {'message': '?FREQ', 'converter': 'f'}
        command = DeviceCommand('get_frequency', 'query_ascii_values', **kwargs)
        self.assertEqual(command.method, 'query_ascii_values')
        result = command(device)[0]
        self.assertEqual(result, 4.200)

if __name__ == '__main__':
    unittest.main()
