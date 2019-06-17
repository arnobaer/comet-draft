import argparse
import random, time
import comet

from comet.filewriter import CSVFileWriter, HephyDBFileWriter

class Application(comet.Application):

    def __init__(self):
        super(Application, self).__init__('CLT', backend='@sim')
        # Set attributes
        self.set('default_op', 'Monty')
        # Register parameters
        self.register_param('n_sensors', type=int, min=0, max=16, label="# of sensors")
        self.register_param('operator', default=self.get('default_op'), type=str)
        self.register_param('v_max', default=800.0, prec=2, unit='V', label="ramp up end voltage")
        self.register_param('v_step', default=5.0, prec=1, unit='V', label="stepsize")
        self.register_param('t_ramp', default=1.0, prec=2, unit='sec')
        self.register_param('v_bias', default=600.0, prec=2, unit='V')
        self.register_param('i_smu_compliance', default=80.0, prec=1, unit='uA')
        self.register_param('i_sensor_compliance', default=25.0, prec=1, unit='uA')
        self.register_param('t_meas', default=1.0, prec=2, unit='min')
        self.register_param('t_tcp_recover', min=0, type=int, label="Wait on TCP reconnect to cliamte chamber")
        # register devices
        self.register_device('climate', 'ASRL1::INSTR')
        self.register_device('smu', 'ASRL2::INSTR')
        self.register_device('multi', 'ASRL3::INSTR')
        self.register_device('shunt', 'ASRL4::INSTR')
        # Register collections
        self.register_collection('environ', EnvironCollection)
        self.register_collection('iv', IVCollection)
        # Register continous monitoring
        self.register_monitoring('mon', Monitoring)
        # Register procedures
        self.register_procedure('ramp_up', RampUp)
        self.register_procedure('ramp_down', RampDown)

class EnvironCollection(comet.Collection):

    def setup(self):
        self.register_metric('time')
        self.register_metric('temp', unit='°C')
        self.register_metric('humid', unit='%')
        writer = CSVFileWriter("dump.csv", fieldnames=['time', 'temp', 'humid'])
        self.register_handle(writer)

class IVCollection(comet.Collection):

    def setup(self):
        self.register_metric('time')
        self.register_metric('i')
        self.register_metric('v')
        self.register_metric('temp')
        self.register_metric('humid')

class Monitoring(comet.Procedure):

    def setup(self):
        pass

    def run(self):
        environ = self.app.collections.get('environ')
        temp = float(self.app.devices.get('climate').query('?FREQ')) * len(environ.data)
        humid = float(self.app.devices.get('climate').query('?FREQ')) * len(environ.data)
        environ.append(time=time.time(), temp=temp, humid=humid)
        self.wait(2)

class RampUp(comet.Procedure):

    def setup(self):
        pass

    def run(self):
        print("RAMP_UP")
        writer = HephyDBFileWriter('iv.hephydb')
        writer.create(["IV","demo","testing"])
        table = writer.create_table('iv_curve', ['time', 'i', 'v', 'temp', 'humid'])
        for _ in range(80):
            environ = self.app.collections.get('environ')
            iv = self.app.collections.get('iv')
            i = float(self.app.devices.get('climate').query('?FREQ'))
            v = float(self.app.devices.get('climate').query('?FREQ'))
            _, temp, humid = environ.data[-1]
            t = time.time()
            iv.append(time=t, i=i, v=v, temp=temp, humid=humid)
            table.append(dict(time=t, i=i, v=v, temp=temp, humid=humid))
            time.sleep(.1)
        print()

class RampDown(comet.Procedure):

    def setup(self):
        pass

    def run(self):
        print("RAMP_DOWN")
        for _ in range(80):
            environ = self.app.collections.get('environ')
            iv = self.app.collections.get('iv')
            i = float(self.app.devices.get('climate').query('?FREQ'))
            v = float(self.app.devices.get('climate').query('?FREQ'))
            _, temp, humid = environ.data[-1]
            iv.append(time=time.time(), i=i, v=v, temp=temp, humid=humid)
            time.sleep(.1)
        print()
        self.wait(2)


def main():
    # Create user application
    app = Application()

    # Serve application on default host/ports
    server = comet.HttpServer(app)
    server.run()

if __name__ == '__main__':
    main()
