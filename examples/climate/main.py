import argparse
import comet

class Application(comet.Application):

    def __init__(self):
        super(Application, self).__init__('CLT', backend='@sim')
        # Set attributes
        self.set('default_op', 'Monty')
        # Register parameters
        self.register_param('v_max', default=1000.0, prec=1, unit='V')
        self.register_param('i_compliance', default=2.5, unit='A')
        self.register_param('operator', default=self.get('default_op'), type=str)
        # register devices
        self.register_device('climate', 'ASRL1::INSTR')
        self.register_device('smu', 'ASRL2::INSTR')
        self.register_device('multi', 'ASRL3::INSTR')
        self.register_device('shunt', 'ASRL4::INSTR')
        # Register collections
        self.register_collection('environ', EnvironCollection)
        self.register_collection('iv', IVCollection)
        # Register procedures
        self.register_procedure('monitoring', Monitoring, continious=True)
        self.register_procedure('ramp_up', RampUp)
        self.register_procedure('ramp_down', RampDown)

class EnvironCollection(comet.Collection):

    def setup(self):
        pass

    def run(self):
        pass

class IVCollection(comet.Collection):

    def setup(self):
        pass

    def run(self):
        pass

class RampUp(comet.Procedure):

    def setup(self):
        pass

    def run(self):
        pass

class RampDown(comet.Procedure):

    def setup(self):
        pass

    def run(self):
        pass

def main():
    # Create user application
    app = Application()

    # Serve application on default host/ports
    server = comet.HttpServer(app)
    server.run()

if __name__ == '__main__':
    main()
