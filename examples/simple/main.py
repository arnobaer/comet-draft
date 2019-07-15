import comet

class MyApplication(comet.Application):

    def setup(self):
        # Create parameters
        self.add_param('loops', default=16, type=int, min=0, max=8, label="# of loops")
        self.add_param('delay', default=1.0, type=float, min=0.0, max=16.0, prec=2, unit='s')
        # Create VISA devices
        self.add_device('multi', 'ASRL3::INSTR')
        # Create data collections
        self.add_collection('iv', IVCollection)
        # Create jobs
        self.add_job('measure', MeasureJob)

    def on_configure(self):
        # Reset a device
        device = self.devices.get('multi')
        device.query('*ESR?')

    def on_running(self):
        # Run a job
        measure = self.jobs.get('measure')
        measure.run()

class IVCollection(comet.Collection):

    def setup(self):
        # Create metrics
        self.add_metric('time', unit='s')
        self.add_metric('i', unit='A')
        self.add_metric('v', unit='V')

class MeasureJob(comet.Job):

    def run(self):
        # Get parameters
        loops = self.app.params.get('loops').value
        delay = self.app.params.get('delay').value
        # Get device
        device = self.app.devices.get('multi')
        # Get collection
        coll = self.app.collections.get('iv')
        # Run measurement loop
        for step in range(loops):
            # Read current
            device.write(':CURR:IMM:AMPL 1.5')
            i = device.query(':CURR:IMM:AMPL?')
            # Read volts
            device.write(':VOLT:IMM:AMPL 1.0')
            v = device.query(':VOLT:IMM:AMPL?')
            # Append record to collection
            coll.append(time=self.time(), i=i, v=v)
            # Delay next iteration
            self.wait(delay)

# Create user application
app = MyApplication('MyApp', backend='@sim')

# Serve application on http://localhost:8080
server = comet.HttpServer(app)
server.run()
