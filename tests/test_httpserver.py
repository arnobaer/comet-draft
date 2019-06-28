import unittest
import time
import env

from comet import Job
from comet import Application
from comet import HttpServer

class MyJob(Job):
    """Prints list of application params and shuts down application."""

    def run(self):
        for name, param in self.app.params.items():
            print(name, param.value)
        self.app.quit()

class MyApplication(Application):

    def __init__(self):
        super(MyApplication, self).__init__('MyApp')
        self.add_param('v_min', default=0.0, min=0.0, max=100.0, unit='V')
        self.add_param('v_max', default=100.0, min=0.0, max=100.0, unit='V')
        self.add_param('i_compliance', default=1.0, min=0.0, max=2.0, unit='A', label="I compl.")
        self.add_job('list_params', MyJob)

class CommandLineTest(unittest.TestCase):

    def testMain(self):
        app = MyApplication()
        server = HttpServer(app)
        app.start()
        server.run()

if __name__ == '__main__':
    unittest.main()
