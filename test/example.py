import unittest

from ..comet.application import Application
#from comet.monitoring import Monitor

class ExampleApplication(Application):
    def __init__(self):
        super(ExampleApplication, self).__init__()
    def code(self):
        pass

class ExampleTest(unittest.TestCase):
    def testMain():
        app = ExampleApplication()
        app.run()

if __name__ == '__main__':
    unittest.main()
