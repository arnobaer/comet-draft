import time
import logging

import comet

class Application(comet.Application):

    max_sensors = 10

    def __init__(self):
        super(Application, self).__init__('CLT', backend='@sim')
        # Set attributes
        self.set('default_op', 'Monty')
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
        self.add_param('t_meas', default=1.0, prec=2, unit='min')
        self.add_param('t_tcp_recover', min=0, type=int, label="Wait on TCP reconnect to cliamte chamber")
        # register devices
        self.add_device('climate', 'ASRL1::INSTR')
        self.add_device('smu', 'ASRL1::INSTR')
        self.add_device('multi', 'ASRL1::INSTR')
        self.add_device('shunt', 'ASRL1::INSTR')
        # Register collections
        self.add_collection('environ', EnvironCollection)
        self.add_collection('iv', IVCollection)
        # Register continous process
        self.add_process('mon', Monitoring)
        # Register states
        self.add_procedure('ramp_up', RampUp)
        self.add_procedure('ramp_bias', RampBias)
        self.add_procedure('longterm', Longterm)
        self.add_procedure('ramp_down', RampDown)

    def on_running(self):
        self.procedures.get('ramp_up').run()
        self.procedures.get('ramp_bias').run()
        self.procedures.get('longterm').run()

    def on_stopping(self):
        self.procedures.get('ramp_down').run()

class EnvironCollection(comet.Collection):

    def configure(self):
        self.add_metric('time', unit='s')
        self.add_metric('temp', unit='°C')
        self.add_metric('humid', unit='%')
        writer = comet.CSVFileWriter("dump.csv", fieldnames=['time', 'temp', 'humid'])
        self.add_handle(writer)

class IVCollection(comet.Collection):

    def configure(self):
        self.add_metric('time', unit='s')
        self.add_metric('i', unit='A')
        self.add_metric('v', unit='V')
        self.add_metric('temp', unit='°C')
        self.add_metric('humid', unit='%')

class Monitoring(comet.Procedure):

    def configure(self):
        pass

    def run(self):
        environ = self.app.collections.get('environ')
        temp = float(self.app.devices.get('climate').query('?FREQ')) * len(environ) / 100.
        humid = float(self.app.devices.get('climate').query('?FREQ')) * len(environ) / 100.
        environ.append(time=time.time(), temp=temp, humid=humid)
        self.wait(2)

class RampUp(comet.Procedure):

    def configure(self):
        writer = comet.HephyDBFileWriter('iv.hephydb')
        writer.create(["IV","demo","testing"])
        self.table = writer.create_table('iv_curve', ['time', 'i', 'v', 'temp', 'humid'])

    def run(self):
        for step in range(80):
            environ = self.app.collections.get('environ')
            iv = self.app.collections.get('iv')
            i = float(self.app.devices.get('climate').query('?FREQ'))
            v = float(self.app.devices.get('climate').query('?FREQ'))
            _, temp, humid = environ.snapshot(1)[0]
            t = time.time()
            iv.append(time=t, i=i, v=v, temp=temp, humid=humid)
            self.table.append(dict(time=t, i=i, v=v, temp=temp, humid=humid))
            time.sleep(.1)
            self.progress = 100/80*step
        print()

class RampBias(comet.Procedure):

    def configure(self):
        pass

    def run(self):
        for step in range(20):
            environ = self.app.collections.get('environ')
            iv = self.app.collections.get('iv')
            i = float(self.app.devices.get('climate').query('?FREQ'))
            v = float(self.app.devices.get('climate').query('?FREQ'))
            _, temp, humid = environ.snapshot(1)[0]
            iv.append(time=time.time(), i=i, v=v, temp=temp, humid=humid)
            time.sleep(.1)
            self.progress = 100/80*step
        print()
        self.wait(2)

class Longterm(comet.Procedure):

    def configure(self):
        pass

    def run(self):
        for step in range(101):
            environ = self.app.collections.get('environ')
            iv = self.app.collections.get('iv')
            i = float(self.app.devices.get('climate').query('?FREQ'))
            v = float(self.app.devices.get('climate').query('?FREQ'))
            _, temp, humid = environ.snapshot(1)[0]
            iv.append(time=time.time(), i=i, v=v, temp=temp, humid=humid)
            time.sleep(.1)
            self.progress = 100/80*step
        print()
        self.wait(2)

class RampDown(comet.Procedure):

    def configure(self):
        pass

    def run(self):
        for step in range(60):
            environ = self.app.collections.get('environ')
            iv = self.app.collections.get('iv')
            i = float(self.app.devices.get('climate').query('?FREQ'))
            v = float(self.app.devices.get('climate').query('?FREQ'))
            _, temp, humid = environ.snapshot(1)[0]
            iv.append(time=time.time(), i=i, v=v, temp=temp, humid=humid)
            time.sleep(.1)
            self.progress = 100/60*step
        print()
        self.wait(2)


def main():
    # Create user application
    app = Application()

    logging.getLogger().setLevel(logging.INFO)

    # Serve application on default host/ports
    server = comet.HttpServer(app)
    server.run()

if __name__ == '__main__':
    main()
