# encoding: utf-8
__author__ = 'lgl'

from __init__ import PyTest

class TestType(object):
    def test_list(self):
        lst = [1,2,4,5]
        with self.assertRaises(ValueError):
            self.loadDict(lst)
    def test_float(self):
        f = 1.0
        with self.assertRaises(ValueError):
            self.loadDict(f)
    def test_tuple(self):
        t = (1,2,3)
        d = {'t':t}
        with self.assertRaises(ValueError):
            self.loadDict(t)
        with self.assertRaises(ValueError):
            self.loadDict(d)

    def test_int(self):
        i = 2L
        with self.assertRaises(ValueError):
            self.loadDict(i)

    class UserObject(object):
        pass

    def test_uesr_object(self):
        u = self.UserObject()
        with self.assertRaises(ValueError):
            self.loadDict(u)


class TestPyType(TestType, PyTest): pass
