import unittest
import env

from comet.application import Application
from comet.service import Service

class MyApplication(Application):
    pass

class MyService(Service):

    def __init__(self, app, name):
        super(MyService, self).__init__(app, name)
        self.configure_done = False
        self.run_done = False

    def configure(self):
        self.configure_done = True

    def run(self):
        self.run_done = True

class ServiceTest(unittest.TestCase):

    # TODO

    def testService(self):
        app = MyApplication('MyApp')
        name = 'MyTestService'

        service = MyService(app, name)
        self.assertIs(service.app, app)
        self.assertEqual(service.name, name)

        self.assertFalse(service.configure_done)
        service.configure()
        self.assertTrue(service.configure_done)

        self.assertFalse(service.run_done)
        service.run()
        self.assertTrue(service.run_done)

        self.assertTrue(service.is_alive)
        service.quit()
        self.assertFalse(service.is_alive)

if __name__ == '__main__':
    unittest.main()
