# encoding: utf8
__author__ = 'lgl'

from __init__ import PyTest

class TestCheckCircular(object):
    def test_circular_dict(self):
        dct = {}
        dct['a'] = dct
        self.loadDict(dct)
        self.assertRaises(ValueError, self.dump)

    def test_circular_composite(self):
        dct2 = {}
        dct2['a'] = []
        dct2['a'].append(dct2)
        self.loadDict(dct2)
        self.assertRaises(ValueError, self.dump)


class TestPyCheckCircular(TestCheckCircular, PyTest): pass