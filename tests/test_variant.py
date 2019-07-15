import unittest
import env

from comet.variant import Variant

class VariantTest(unittest.TestCase):

    def testValue(self):
        value = Variant(42)
        self.assertEqual(value.value, 42)
        value = Variant(4.2)
        self.assertEqual(value.value, 4.2)
        value = Variant('spam')
        self.assertEqual(value.value, 'spam')

    def testType(self):
        value = Variant(42)
        self.assertEqual(value.type, int)
        value = Variant(4.2)
        self.assertEqual(value.type, float)
        value = Variant('spam')
        self.assertEqual(value.type, str)
        value = Variant(42)

    def testLen(self):
        value = Variant(' 0x2a ')
        self.assertEqual(len(value), 6)

    def testTo(self):
        value = Variant(' 0x2a ').to(int, 16)
        self.assertEqual(value.value, 42)
        self.assertEqual(value.type, int)
        value = value.to(float)
        self.assertEqual(value.value, 42.0)
        self.assertEqual(value.type, float)
        value = value.to(int)
        self.assertEqual(value.value, 42)
        self.assertEqual(value.type, int)
        value = value.to(str)
        self.assertEqual(value.value, '42')
        self.assertEqual(value.type, str)

    def testToInt(self):
        value = Variant(' 0x2a ').toint(16)
        self.assertEqual(value.value, 42)
        self.assertEqual(value.type, int)
        value = Variant(42.1).toint()
        self.assertEqual(value.value, 42)
        self.assertEqual(value.type, int)
        value = int(value)
        self.assertEqual(value, 42)
        self.assertEqual(type(value), int)

    def testToFloat(self):
        value = Variant('4.2').tofloat()
        self.assertEqual(value.value, 4.2)
        self.assertEqual(value.type, float)
        value = float(Variant(4.2))
        self.assertEqual(value, 4.2)
        self.assertEqual(type(value), float)

    def testToStr(self):
        value = Variant(4.2).tostr()
        self.assertEqual(value.value, '4.2')
        self.assertEqual(value.type, str)
        value = str(Variant(4.2))
        self.assertEqual(value, '4.2')
        self.assertEqual(type(value), str)

    def testEncode(self):
        value = Variant('spam').encode()
        self.assertEqual(value.value, b'spam')
        self.assertEqual(value.type, bytes)

    def testDecode(self):
        value = Variant(b'spam').decode()
        self.assertEqual(value.value, 'spam')
        self.assertEqual(value.type, str)

if __name__ == '__main__':
    unittest.main()
