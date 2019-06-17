import unittest
import env

from comet import Application

class ExampleApplication(Application):

    def __init__(self):
        super(ExampleApplication, self).__init__('app')

    def code(self):
        pass

class ExampleTest(unittest.TestCase):

    def testMain(self):
        app = ExampleApplication()
        self.assertEqual(app.name, 'app')
        # app.run()

if __name__ == '__main__':
    unittest.main()
