import unittest
import re
import env

from pyvisa import ResourceManager

from comet.device import DeviceException
from comet.device import DeviceFactory
from comet.device import DeviceCommand
from comet.device import DeviceMessageHandler
from comet.device import DeviceErrorHandler

class DeviceManagerTestCase(unittest.TestCase):
    def setUp(self):
        rm = ResourceManager('@sim')
        self.factory = DeviceFactory(rm)

class BasicDeviceManagerTestCase(DeviceManagerTestCase):
    def runTest(self):
        factory = self.factory
        self.assertEqual(factory.__class__.__name__, 'DeviceFactory')
        device = factory.create('DUMMY', 'GPIB::14', {})
        self.assertEqual(device.__class__.__name__, 'Device')
        self.assertEqual(device.name, 'DUMMY')
        config = {'commands': {'get_value': {'method': 'query', 'message': 'VALUE?', 'description': 'query value'}}}
        device = factory.create('SMU1', 'GPIB::16', config)
        self.assertEqual(device.__class__.__name__, 'Device')
        self.assertEqual(device.name, 'SMU1')
        self.assertEqual(device.get_value.method, 'query')
        self.assertEqual(device.get_value.kwargs.get('message'), 'VALUE?')
        self.assertEqual(device.get_value.description, 'query value')

class DeviceCommandTestCase(DeviceManagerTestCase):
    def runTest(self):
        """This test depends on the default shipped pyvisa-sim configuration (device 1)."""
        device = self.factory.create('SMU', 'ASRL1::INSTR', {'read_termination': '\n'})

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
        self.assertEqual(command.require, re.compile('.*((\d+)\.(\d+))$'))
        self.assertEqual(command.description, 'get frequency')
        result = command(device)
        self.assertEqual(result, '100.00')

        # query command
        kwargs = {'message': 'NONE', 'require': '(ERROR)(\n?)$',}
        command = DeviceCommand('get_none', 'query', **kwargs)
        self.assertEqual(command.require, re.compile('(ERROR)(\n?)$'))
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

        # applying choices
        kwargs = {'message': '!FREQ {:.2f}', 'choices': [1.2, 2.4]}
        command = DeviceCommand('set_frequency', 'query', **kwargs)
        result = command(device, 1.200)
        self.assertEqual(result, 'OK')
        result = command(device, 2.400)
        self.assertEqual(result, 'OK')

        # query converter
        kwargs = {'message': '?FREQ'}
        command = DeviceCommand('set_frequency', 'query', **kwargs)
        result = command(device)
        self.assertEqual(result.float, 2.400)
        self.assertEqual(result.str, '2.40')
        self.assertEqual(str(result.str), '2.40')
        self.assertEqual(result, '2.40')

class DeviceMessageHandlerTestCase(DeviceManagerTestCase):
    def runTest(self):
        """This test depends on the default shipped pyvisa-sim configuration (device 1)."""

        # Default message handler base class
        handler = DeviceMessageHandler()
        self.assertEqual(None, handler.handle(42.0))

        # Custom message handler class
        class MyCustomMessageHandler:
            def handle(self, message):
                if message >= 42.0:
                    raise ValueError(message)
        handler = MyCustomMessageHandler()
        self.assertRaises(ValueError, handler.handle, 42.0)

        # Default error handler class
        handler = DeviceErrorHandler('ERR(\d+)', messages={42: "minor error"})
        self.assertRaises(DeviceException, handler.handle, 'ERR42')

        # key error_parser automatically creates an error handler
        device = self.factory.create('SMU', 'ASRL1::INSTR', {
            'read_termination': '\n',
            'errors': {
                'expression': 'ERROR',
                'messages': { 42: "a minor error" }
            }
        })
        self.assertRaises(DeviceException, device.query, '?INVLD')

if __name__ == '__main__':
    unittest.main()
