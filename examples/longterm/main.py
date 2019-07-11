import time
import logging
import random

import comet
from devices import CTSDevice

class Application(comet.Application):

    max_sensors = 10

    def setup(self):
        # Set attributes
        self.set('default_op', 'Monty')
        self.set('cts_resource', 'TCPIP::192.168.100.205::1080::SOCKET')
        # Register parameters
        self.add_param('n_sensors', type=int, min=0, max=self.max_sensors, label="# of sensors")
        for i in range(self.max_sensors):
            self.add_param('sensors_{}'.format(i), type=str, required=True, label="Sensor #{}".format(i))
        self.add_param('operator', default=self.get('default_op'), type=str)
        self.add_param('v_max', default=800.0, min=0.0, max=1000.0, prec=4, unit='V', label="ramp up end voltage")
        self.add_param('v_step', default=5.0, prec=1, unit='V', label="stepsize")
        self.add_param('t_ramp', default=1.0, prec=2, unit='sec')
        self.add_param('v_bias', default=600.0, prec=2, unit='V')
        self.add_param('i_smu_compliance', default=80.0, prec=1, unit='uA')
        self.add_param('i_sensor_compliance', default=25.0, prec=1, unit='uA')
        self.add_param('t_longterm', default=60.0, prec=2, unit='min')
        self.add_param('t_interval', default=60.0, prec=2, unit='sec')
        self.add_param('t_tcp_recover', min=0, type=int, label="Wait on TCP reconnect to cliamte chamber")
        # register devices
        self.add_device('climate', self.get('cts_resource'))
        # self.add_device('smu', 'ASRL1::INSTR')
        # self.add_device('multi', 'ASRL1::INSTR')
        # self.add_device('shunt', 'ASRL1::INSTR')
        # HACK: create a CTS binary device from allocated resource
        self.cts_device = CTSDevice('cts', self.devices.get('climate').resource)
        # Register collections
        self.add_collection('environ', EnvironCollection)
        self.add_collection('iv', IVCollection)
        # Register services
        self.add_service('mon', Monitoring)
        # Register states
        self.add_job('ramp_up', RampUp)
        self.add_job('ramp_bias', RampBias)
        self.add_job('longterm', Longterm)
        self.add_job('ramp_down', RampDown)

        self.fake_i = 0.0
        self.fake_v = 0.0

    def on_configure(self):
        time.sleep(3.0)
        writer = comet.HephyDBFileWriter('iv.hephydb')
        writer.create(["IV","demo","testing"])
        self.table = writer.create_table('iv_curve', ['time', 'i', 'v', 'temp', 'humid'])

    def on_running(self):
        self.jobs.get('ramp_up').run()
        self.jobs.get('ramp_bias').run()
        self.jobs.get('longterm').run()

    def on_stopping(self):
        self.jobs.get('ramp_down').run()

class EnvironCollection(comet.Collection):

    def setup(self):
        self.add_metric('time', unit='s')
        self.add_metric('temp', unit='°C')
        self.add_metric('humid', unit='%')
        self.add_metric('water', unit='l')
        writer = comet.CSVFileWriter("dump.csv", fieldnames=['time', 'temp', 'humid', 'water'])
        self.add_handle(writer)

class IVCollection(comet.Collection):

    def setup(self):
        self.add_metric('time', unit='s')
        self.add_metric('i', unit='A')
        self.add_metric('v', unit='V')
        self.add_metric('temp', unit='°C')
        self.add_metric('humid', unit='%')

    def configure(self):
        self.clear()

class Monitoring(comet.Service):

    def run(self):
        environ = self.app.collections.get('environ')
        cts = self.app.cts_device
        while self.is_alive:
            t = self.time()
            temp_actual, temp_target = cts.get_analog_channel(1)
            humid_actual, humid_target = cts.get_analog_channel(2)
            water_actual, water_target = cts.get_analog_channel(3)
            environ.append(time=t, temp=temp_actual, humid=humid_actual, water=water_actual)
            self.wait(5)

class RampUp(comet.Job):

    steps = 64

    def run(self):
        environ = self.app.collections.get('environ')
        iv = self.app.collections.get('iv')
        for step in range(self.steps):
            #i = float(self.app.devices.get('climate').query('?FREQ'))
            #v = float(self.app.devices.get('climate').query('?FREQ'))
            self.app.fake_i += random.uniform(1.3,1.4)
            self.app.fake_v += random.uniform(1.45,1.55)
            _, temp, humid = environ.snapshot(1)[0]
            t = time.time()
            iv.append(time=t, i=self.app.fake_i, v=self.app.fake_v, temp=temp, humid=humid)
            time.sleep(.1)
            self.update_progress(step, self.steps)

        print()

class RampBias(comet.Job):

    steps = 16

    def run(self):
        for step in range(self.steps):
            environ = self.app.collections.get('environ')
            iv = self.app.collections.get('iv')
            #i = float(self.app.devices.get('climate').query('?FREQ'))
            #v = float(self.app.devices.get('climate').query('?FREQ'))
            self.app.fake_i += random.uniform(-1.3,-1.4)
            self.app.fake_v += random.uniform(-1.45,-1.55)
            _, temp, humid = environ.snapshot(1)[0]
            iv.append(time=time.time(), i=self.app.fake_i, v=self.app.fake_v, temp=temp, humid=humid)
            time.sleep(.1)
            self.update_progress(step, self.steps)
        print()
        self.wait(2)

class Longterm(comet.Job):

    def run(self):
        t_longterm_sec = self.app.params.get('t_longterm').value * 60
        t_interval_sec = self.app.params.get('t_interval').value
        t_begin = self.time()
        t_end = t_begin + t_longterm_sec
        while self.app.is_running:
            t_now = self.time()
            if t_end < t_now:
                break
            environ = self.app.collections.get('environ')
            iv = self.app.collections.get('iv')
            #i = float(self.app.devices.get('climate').query('?FREQ'))
            #v = float(self.app.devices.get('climate').query('?FREQ'))
            self.app.fake_i += random.uniform(-0.05, 0.05)
            self.app.fake_v += random.uniform(-0.001,-0.005)
            _, temp, humid = environ.snapshot(1)[0]
            t = time.time()
            iv.append(time=t, i=self.app.fake_i, v=self.app.fake_v, temp=temp, humid=humid)
            self.app.table.append(dict(time=t, i=self.app.fake_i, v=self.app.fake_v, temp=temp, humid=humid))
            self.update_progress(t_now-t_begin, t_end-t_begin)
            self.wait_on_pause()
            self.wait_while_running(t_interval_sec)
        print()
        self.wait(2)

class RampDown(comet.Job):

    steps = 32

    def run(self):
        offset = self.app.fake_v
        while self.app.fake_v > 0.0:
            environ = self.app.collections.get('environ')
            iv = self.app.collections.get('iv')
            #i = float(self.app.devices.get('climate').query('?FREQ'))
            #v = float(self.app.devices.get('climate').query('?FREQ'))
            self.app.fake_i += random.uniform(-5.3,-5.4)
            self.app.fake_v += random.uniform(-5.45,-5.55)
            _, temp, humid = environ.snapshot(1)[0]
            iv.append(time=time.time(), i=self.app.fake_i, v=self.app.fake_v, temp=temp, humid=humid)
            time.sleep(.1)
            self.update_progress(offset-self.app.fake_v, offset)
        print()
        self.wait(2)


def main():
    # Create user application
    app = Application('Longterm', backend='@py')

    logging.getLogger().setLevel(logging.INFO)

    # Serve application on default host/ports
    server = comet.HttpServer(app)
    server.run()

if __name__ == '__main__':
    main()
