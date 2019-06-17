import unittest
import env

from comet.application import Parameter

class ParameterTest(unittest.TestCase):

    def testParameterEmpty(self):
        param = Parameter('val')
        self.assertEqual(param.name, 'val')
        self.assertEqual(param.type, float)
        self.assertEqual(param.value, param.type())

    def testParameterDefault(self):
        default = 42.0
        param = Parameter('val', default=default)
        self.assertEqual(param.value, default)

    def testParameterType(self):
        param = Parameter('val', type=int)
        self.assertEqual(param.type, int)
        self.assertEqual(param.value, int())

    def testParameterMin(self):
        cases = [
            (100, 10), (-10, -100)
        ]
        for default, minimum in cases:
            param = Parameter('val', type=int, min=minimum, default=default)
            self.assertEqual(param.value, default)
            param.value = minimum
            self.assertEqual(param.value, minimum)
            def assign_value_wrapper():
                param.value = minimum-1
            self.assertRaises(ValueError, assign_value_wrapper)
            self.assertEqual(param.value, minimum)

    def testParameterMax(self):
        cases = [
            (10, 100), (-100, -10)
        ]
        for default, maximum in cases:
            param = Parameter('val', type=int, max=maximum, default=default)
            self.assertEqual(param.value, default)
            param.value = maximum
            self.assertEqual(param.value, maximum)
            def assign_value_wrapper():
                param.value = maximum+1
            self.assertRaises(ValueError, assign_value_wrapper)
            self.assertEqual(param.value, maximum)

    def testParameterMinMax(self):
        pass

    def testParameterPrec(self):
        param = Parameter('val')
        self.assertEqual(param.prec, None)
        param = Parameter('val', prec=3)
        self.assertEqual(param.prec, 3)
        self.assertEqual(format(param), '0.000')
        param = Parameter('val', prec=1, default=42.42)
        self.assertEqual(param.value, 42.42)
        self.assertEqual(param.prec, 1)
        self.assertEqual(format(param), '42.4')

    def testParameterUnit(self):
        param = Parameter('val')
        self.assertEqual(param.unit, None)
        param = Parameter('val', unit='V')
        self.assertEqual(param.unit, 'V')

    def testParameterLabel(self):
        param = Parameter('val')
        self.assertEqual(param.label, 'Val')
        param = Parameter('v_min')
        self.assertEqual(param.label, 'V min')
        param = Parameter('v_min', label='a value')
        self.assertEqual(param.label, 'a value')

if __name__ == '__main__':
    unittest.main()
