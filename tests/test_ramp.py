import unittest
import env

from comet.ramp import Ramp

class RampTest(unittest.TestCase):

    def testRampUp(self):
        ref = 0
        start = 0.
        stop = 10.
        step = .5
        for v in Ramp(start, stop, step, delay=0.01):
            self.assertEqual(v, ref)
            ref += step

    def testRampDown(self):
        ref = 10
        start = 10.
        stop = 0.
        step = -.5
        for v in Ramp(start, stop, step, delay=0.01):
            self.assertEqual(v, ref)
            ref += step

if __name__ == '__main__':
    unittest.main()
