import time
import comet

class Application(comet.Application):

    max_sensors = 10

    def __init__(self):
        super(Application, self).__init__('CLT', backend='@sim')
        # Set attributes
        self.set('default_op', 'Monty')
        # Register parameters
        self.register_param('n_sensors', type=int, min=0, max=self.max_sensors, label="# of sensors")
        for i in range(self.max_sensors):
            self.register_param('sensors_{}'.format(i), type=str, required=True, label="Sensor #{}".format(i))
        self.register_param('operator', default=self.get('default_op'), type=str)
        self.register_param('v_max', default=800.0, min=0.0, max=1000.0, prec=4, unit='V', label="ramp up end voltage")
        self.register_param('v_step', default=5.0, prec=1, unit='V', label="stepsize")
        self.register_param('t_ramp', default=1.0, prec=2, unit='sec')
        self.register_param('v_bias', default=600.0, prec=2, unit='V')
        self.register_param('i_smu_compliance', default=80.0, prec=1, unit='uA')
        self.register_param('i_sensor_compliance', default=25.0, prec=1, unit='uA')
        self.register_param('t_meas', default=1.0, prec=2, unit='min')
        self.register_param('t_tcp_recover', min=0, type=int, label="Wait on TCP reconnect to cliamte chamber")
        # register devices
        self.register_device('climate', 'ASRL1::INSTR')
        self.register_device('smu', 'ASRL1::INSTR')
        self.register_device('multi', 'ASRL1::INSTR')
        self.register_device('shunt', 'ASRL1::INSTR')
        # Register collections
        self.register_collection('environ', EnvironCollection)
        self.register_collection('iv', IVCollection)
        # Register continous monitoring
        self.register_monitoring('mon', Monitoring)
        # Register states
        self.register_state('ramp_up', RampUp)
        self.register_state('ramp_bias', RampBias)
        self.register_state('longterm', Longterm)
        self.register_state('ramp_down', RampDown)

class EnvironCollection(comet.Collection):

    def setup(self):
        self.register_metric('time')
        self.register_metric('temp', unit='°C')
        self.register_metric('humid', unit='%')
        writer = comet.CSVFileWriter("dump.csv", fieldnames=['time', 'temp', 'humid'])
        self.register_handle(writer)

class IVCollection(comet.Collection):

    def setup(self):
        self.register_metric('time')
        self.register_metric('i', unit='A')
        self.register_metric('v', unit='V')
        self.register_metric('temp', unit='°C')
        self.register_metric('humid', unit='%')

class Monitoring(comet.State):

    def setup(self):
        pass

    def run(self):
        environ = self.app.collections.get('environ')
        temp = float(self.app.devices.get('climate').query('?FREQ')) * len(environ.data) / 100.
        humid = float(self.app.devices.get('climate').query('?FREQ')) * len(environ.data) / 100.
        environ.append(time=time.time(), temp=temp, humid=humid)
        self.wait(2)

class RampUp(comet.State):

    def setup(self):
        writer = comet.HephyDBFileWriter('iv.hephydb')
        writer.create(["IV","demo","testing"])
        self.table = writer.create_table('iv_curve', ['time', 'i', 'v', 'temp', 'humid'])

    def run(self):
        for step in range(80):
            if not self.app.running: return
            environ = self.app.collections.get('environ')
            iv = self.app.collections.get('iv')
            i = float(self.app.devices.get('climate').query('?FREQ'))
            v = float(self.app.devices.get('climate').query('?FREQ'))
            _, temp, humid = environ.data[-1]
            t = time.time()
            iv.append(time=t, i=i, v=v, temp=temp, humid=humid)
            self.table.append(dict(time=t, i=i, v=v, temp=temp, humid=humid))
            time.sleep(.1)
            self.progress = 100/80*step
        print()

class RampBias(comet.State):

    def setup(self):
        pass

    def run(self):
        for step in range(20):
            if not self.app.running: return
            environ = self.app.collections.get('environ')
            iv = self.app.collections.get('iv')
            i = float(self.app.devices.get('climate').query('?FREQ'))
            v = float(self.app.devices.get('climate').query('?FREQ'))
            _, temp, humid = environ.data[-1]
            iv.append(time=time.time(), i=i, v=v, temp=temp, humid=humid)
            time.sleep(.1)
            self.progress = 100/80*step
        print()
        self.wait(2)

class Longterm(comet.State):

    def setup(self):
        pass

    def run(self):
        for step in range(101):
            if not self.app.running: return
            environ = self.app.collections.get('environ')
            iv = self.app.collections.get('iv')
            i = float(self.app.devices.get('climate').query('?FREQ'))
            v = float(self.app.devices.get('climate').query('?FREQ'))
            _, temp, humid = environ.data[-1]
            iv.append(time=time.time(), i=i, v=v, temp=temp, humid=humid)
            time.sleep(.1)
            self.progress = 100/80*step
        print()
        self.wait(2)

class RampDown(comet.State):

    def setup(self):
        pass

    def run(self):
        for step in range(60):
            print("STOPPED", flush=True)
            environ = self.app.collections.get('environ')
            iv = self.app.collections.get('iv')
            i = float(self.app.devices.get('climate').query('?FREQ'))
            v = float(self.app.devices.get('climate').query('?FREQ'))
            _, temp, humid = environ.data[-1]
            iv.append(time=time.time(), i=i, v=v, temp=temp, humid=humid)
            time.sleep(.1)
            self.progress = 100/60*step
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
