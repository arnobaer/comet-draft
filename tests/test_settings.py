import unittest
import env

from comet import Settings

class SettingsTest(unittest.TestCase):

    def testPersistent(self):
        with Settings('HEPHY', 'comet', persistent=False) as settings:
            print(settings)

if __name__ == '__main__':
    unittest.main()
