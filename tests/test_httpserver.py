import unittest
import time
import env

from comet import Procedure
from comet import Application
from comet import HttpServer

class MyProcedure(Procedure):
    """Prints list of application params and shuts down application."""

    def run(self):
        for name, param in self.app.params.items():
            print(name, param.value)
        self.app.shutdown()

class MyApplication(Application):

    def __init__(self):
        super(MyApplication, self).__init__('MyApp')
        self.register_param('v_min', default=0.0, min=0.0, max=100.0, unit='V')
        self.register_param('v_max', default=100.0, min=0.0, max=100.0, unit='V')
        self.register_param('i_compliance', default=1.0, min=0.0, max=2.0, unit='A', label="I compl.")
        self.register_procedure('list_params', MyProcedure)

class CommandLineTest(unittest.TestCase):

    def testMain(self):
        app = MyApplication()
        server = HttpServer(app)
        app.start()
        server.run()

if __name__ == '__main__':
    unittest.main()
