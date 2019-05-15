import unittest
import env

from comet import Application

class ExampleApplication(Application):

    def __init__(self):
        super(ExampleApplication, self).__init__()

    def code(self):
        pass

class ExampleTest(unittest.TestCase):

    def testMain(self):
        app = ExampleApplication()
        app.run()

if __name__ == '__main__':
    unittest.main()
