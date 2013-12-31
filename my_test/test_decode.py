# encoding: utf8
__author__ = 'lgl'

import decimal
from __init__ import PyTest

class TestDecode(object):
    def test_float(self):
        self.load('{"key":1.1}')
        rval = self.dumpDict()['key']
        self.assertTrue(isinstance(rval, float))
        self.assertEqual(rval, 1.1)

    def test_decoder(self):
        # Several optimizations were made that skip over calls to
        # the whitespace regex, so this test is designed to try and
        # exercise the uncommon cases. The array cases are already covered.
        self.load('{   "key"    :    "value"    ,  "k":"v"    }')
        d = self.dumpDict()
        self.assertEqual(d, {"key":"value", "k":"v"})

    def test_empty_objects(self):
        self.load('{}')
        d = self.dumpDict()
        self.assertEqual(d, {})

    def test_deep_copy(self):
        d = {'key': [u'key', 123], 'key2':{'a':321}}
        self.loadDict(d)
        self.assertNotEqual(id(d), self.dict_id())
        self.assertNotEqual(id(d['key2']), self.dumpDict()['key2'])
        self.assertNotEqual(id(d['key']), self.dumpDict()['key'])

class TestPyDecode(TestDecode, PyTest): pass

# if __name__ == '__main__':
#     unittest.main()