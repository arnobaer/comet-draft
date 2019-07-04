import pyvisa
import datetime
import random
import time

import env
from comet.device import Device

class BytesDevice(Device):

    def __init__(self, name, resource):
        super(BytesDevice, self).__init__(name, resource)

    def query_bytes(self, message, n_bytes):
        """Returns n bytes returned by writing raw query message.

        >>> device.query_bytes('T', 13)
        b'T120619130943'
        """
        self.resource.write_raw(message.encode())
        result = self.resource.read_bytes(n_bytes).decode()
        return result


class CTSDevice(BytesDevice):

    analog_channel_ids = {
        1: 'A0', 2: 'A1', 3: 'A2', 4: 'A3',
        5: 'A4', 6: 'A5', 7: 'A6', 8: 'A7',
        9: 'A8', 10: 'A9', 11: 'A:', 12: 'A;',
        13: 'A<', 14: 'A=', 15: 'A>', 16: 'A?'
    }
    """Mapping analog channel numbers to channel IDs."""

    warning_messages = {
        '\x01': "Wassernachfüllen",
        '\x02': "Temp. Toleranzband Oben",
        '\x03': "Temp. Toleranzband Unten",
        '\x04': "Feuchte Toleranzband Oben",
        '\x05': "Feuchte Toleranzband Unten",
        '\x06': "Wasserbad Abschlaemmen",
    }

    error_messages = {
        '\x31': "Temperatur Grenze Min 08-B1",
        '\x32': "Temperatur Grenze Max 08-B1",
        '\x33': "Temp. Begrenzer Pruefr. 01-F1.1",
        '\x34': "TK Vent. Pruefr. 02-F2.1",
        '\x35': "Pruefgutschutz Max 09-A1",
        '\x37': "Ueberdruck Kuehlung 03-B40",
        '\x38': "Feuchtegrenze Min 08-B2",
        '\x39': "Feuchtegrenze Max 08-B2",
        '\x3a': "Feuchtesensor 08-B2",
        '\x3b': "Wassermangel Feuchte 07-B80",
        '\x3c': "TK Ventilator Verfl. 03-F5.1",
        '\x3d': "Siededrucksensor 03-B60",
        '\x3f': "Pt100 Abluft 08-B1.1",
        '\x40': "Pt100 Zuluft 08-B1.2",
        '\x41': "Pt100 Wasserbad 07-B4",
        '\x42': "Schwimmer Wasservorrat 07-B81",
        '\x43': "Pt100 Beweglich 08-B15",
        '\x47': "Pt100 Sauggas K 03-B13",
        '\x4b': "Sauggastemp. K 03-B13",
        '\x53': "Absaugung Kuehlung 03-B43",
        '\x5b': "Schwimmer Wasserbad 07-B80",
        '\x5c': "Pt100 Saugdampf K 03-B12",
        '\x5e': "Siededrucksensor K 03-B43",
        '\x62': "Leistungsschalter Einspeisung 00-Q1",
    }

    def __init__(self, name, resource):
        super(CTSDevice, self).__init__(name, resource)

    def get_time(self):
        """Returns current date and time of device as datetime object.

        >>> device.set_time()
        datetime.datetime(2019, 6, 12, 13, 01, 21)
        """
        result = self.query_bytes('T', 13)
        return datetime.datetime.strptime(result, 'T%d%m%y%H%M%S')

    def set_time(self, dt):
        """Update device date and time, returns updated data and time as datetime object.

        >>> device.set_time(datetime.now())
        datetime.datetime(2019, 6, 12, 13, 12, 35)
        """
        result = self.query_bytes(dt.strftime('t%d%m%y%H%M%S'), 13)
        return datetime.datetime.strptime(result, 't%d%m%y%H%M%S')

    def get_analog_channel(self, channel):
        """Read analog channel, returns tuple containing actual value and target value.

        >>> device.get_analog_channel(1)
        (42.1, 45.0)
        """
        if channel not in self.analog_channel_ids:
            raise ValueError("no such channel number: '{}'".format(channel))
        result = self.query_bytes(self.analog_channel_ids.get(channel), 14)
        channel_id, actual, target = result.split()
        return float(actual), float(target)

    def set_analog_channel(self, channel, value):
        """Set target value for analog channel.

        >>> device.set_analog_channel(1, 42.0)
        """
        if not 1 <= channel <= 7:
            raise ValueError("invalid channel number: '{}'".format(channel))
        result = self.query_bytes("a{} {:05.1f}".format(channel, value), 1)
        if result != 'a':
            raise RuntimeError("failed to set target for channel '{}'".format(channel))

    def get_status(self):
        """Returns device status as JSON dictionary.

        >>> device.get_status()
        {'running': False, 'error': None, ''}
        """
        result = self.query_bytes('S', 10)
        running = bool(int(result[1]))
        is_error = bool(int(result[2]))
        channel_states = {channel: bool(int(state)) for channel, state in enumerate(result[3:9])}
        error_nr = result[9]
        warning = self.warning_messages[error_nr] if is_error and error_nr in self.warning_messages else None
        error = self.error_messages[error_nr] if is_error and error_nr in self.error_messages else None
        return {
            'running': running,
            'warning': warning,
            'error': error,
            'channels': channel_states,
        }

    # TODO

    def get_program(self):
        """Returns number of running program or None if no program is running.

        >>> device.get_program()
        3
        """
        result = self.query_bytes('P', 4)
        value =  int(result[1:])
        return value if value else None

    def start_program(self, number):
        """Starts a program. Returns program number or None for no program.

        >>> device.start_program(42)
        42
        """
        result = self.query_bytes('P{:03d}'.format(number), 4)
        value =  int(result[1:])
        return value if value else None

def main():
    rm = pyvisa.ResourceManager('@py')
    resource = rm.open_resource('TCPIP::192.168.100.205::1080::SOCKET', write_termination='')

    climate = CTSDevice('Climate', resource)

    # r = climate.get_time()
    # print(r)
    #
    # r = climate.set_time(datetime.datetime.now())
    # print(r)
    #
    # for i in range(1, 16+1):
    #     r = climate.get_analog_channel(i)
    #     print(r)
    #
    # for i in range(1, 7+1):
    #     r = climate.set_analog_channel(i, random.uniform(0., 5.))
    #     print(r)
    #
    # r = climate.get_status()
    # print(r)
    #
    # r = climate.get_program()
    # print(r)
    #
    # r = climate.start_program(42)
    # print(r)
    #
    # climate.resource.close()
    # time.sleep(10)
    # climate.resource.open()

    r = climate.get_status()
    print(r)

if __name__ == '__main__':
    main()
