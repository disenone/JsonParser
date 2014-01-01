# encoding: utf-8
__author__ = 'lgl'
from __init__ import PyTest

class TestIO(object):
    def test_io(self):
        fn = 'not_exist_file'
        try:
            self.loadJson(fn)
        except IOError:
            pass
        else:
            self.fail("Except failure in opening file: {0}".format(fn))
        with self.assertRaises(IOError):
            self.dumpJson(fn)

class TestPyIO(TestIO, PyTest): pass