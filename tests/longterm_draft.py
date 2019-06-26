import time
import comet

class Application(comet.Application):

    def setup(self):
        # set attributes
        self.set_attr('name', 'QXS') # required for CometData/ path
        self.set_attr('title', 'Longterm Sensor Test')
        self.set_attr('description', 'Long term measurement for silicon sensors')
        self.set_attr('version', '1.0.0')
        # register params
        self.add_param('v_max', type=float, default=100.0, min=0.0, max=1000.0, unit='V', label='V max')
        self.add_param('v_longterm', type=float, default=80.0, min=0.0, max=1000.0, unit='V', label='V longterm')
        self.add_param('ramp_delay', type=float, default=.25, min=.05, max=5.0, unit='s') # label defaults: "Ramp delay"
        self.add_param('i_compliance', type=float, default=1.5, max=2.0, unit='A', label='I comp.')
        self.add_param('run_mode', default='normal', choices=('normal', 'fast')) # label defaults: "Run mode"
        # register devices
        self.add_device('climate', type='cts2200')
        self.add_device('smu', type='k2700')
        self.add_device('multi', type='k2100')
        self.add_device('shunt', type='shuntbox')
        # register data collections
        self.add_collection(EnvCollection('environ', continious=True)) # not reset on [start]
        self.add_collection(IVCollection('iv')) # content will be cleared on every [start]
        # create continious procedure
        self.add_procedure(Monitoring(), continious=True) # starts immediately
        # create sequence of procedures
        self.add_procedure(RampUp()) # executed on [start]
        self.add_procedure(RampDownLongterm())
        self.add_procedure(Longterm())
        self.add_procedure(RampDownFinal())

        # every [start] creates a new data directory containing all logs
        # ~/CometData/QXS_2019_06_11_001/iv_curve.csv
        # ~/CometData/QXS_2019_06_11_002/iv_curve.csv
        # ~/CometData/QXS_2019_06_14_001/iv_curve.csv

class EnvCollection(comet.Collection):

    def setup(self):
        climate = self.devices.get('climate')
        self.add_metric('time')
        self.add_metric('temp')
        self.add_metric('humid')

    def update(self):
        climate = self.devices.get('climate')
        t = time.time()
        status = climate.get_status()
        self.write(time=t, temp=status.get('temp'), humid=status.get('humid'))

class IVCollection(comet.Collection):

    def setup(self):
        self.add_metric('time')
        self.add_metric('i', unit='A')
        self.add_metric('v', unit='V')
        self.add_metric('temp', unit='degC')
        self.add_metric('humid', unit='perc')

        writer = comet.HephyDbFileWriter('iv_curve.csv') # comet.FileWriter is bond to CometData/ path
        writer.tags.add('IV')
        writer.tags.add(self.attrs.get('name'))
        iv_table = writer.create_table(name='IV', columns=self.metrics.values())
        self.add_handler(iv_table.append) # appends data on every write()

    def update(self):
        multi = self.device.get('multi')
        t = time.time()
        multi.set_mode(multi.MODE_VOLT)
        volts = multi.read()
        multi.set_mode(multi.MODE_CURR)
        amps = multi.read()
        ss = self.collections.get('environ').snapshot(-1) # get last reading from env collection
        temp = ss.get('temp')
        humid = ss.get('humid')
        self.write(time=t, v=volts, i=amps, temp=temp, humid=humid)

class Monitoring(comet.Procedure):

    def run(self):
        self.collections.get('environ').update()
        self.wait(5.0) # throttle

class Ramp(comet.Procedure):

    def setup(self):
        self.smu = self.devices.get('smu')

    def run(self):
        for v in self.get_ramp():
            self.smu.set_voltage(v)
            self.wait(self.params.get('ramp_delay'))

class RampUp(Ramp):

    def get_ramp(self):
        return comet.Ramp(
            start=self.smu.get_voltage(),
            stop=self.params.get('v_max'),
            step=self.params.get('vstep', 1.0),
        )

class RampDownLongterm(Ramp):

    def get_ramp(self):
        return comet.Ramp(
            start=self.smu.get_voltage(),
            stop=self.params.get('v_longterm'),
            step=self.params.get('vstep', 1.0),
        )

class Longterm(comet.Procedure):

    def run(self):
        while self.running:
            self.collections.get('iv').update()
            self.wait(1.0)

class RampDownFinal(Ramp):

    def get_ramp(self):
        return comet.Ramp(
            start=self.smu.get_voltage(),
            stop=0.0,
            step=self.params.get('vstep', 5.0),
        )
