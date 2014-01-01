# encoding: utf-8
__author__ = 'lgl'
from __init__ import PyTest


class TestRecursion(object):
    def test_listrecursion(self):
        x = []
        x.append(x)
        d = {'x': x}
        try:
            self.loadDict(d)
            self.dump()
        except ValueError:
            pass
        else:
            self.fail("didn't raise ValueError on list recursion")
        x = []
        y = [x]
        x.append(y)
        d = {'x': x}
        try:
            self.loadDict(d)
            self.dump()
        except ValueError:
            pass
        else:
            self.fail("didn't raise ValueError on alternating list recursion")
        y = []
        x = [y, y]
        d = {'x': x}
        # ensure that the marker is cleared
        self.loadDict(d)
        self.dump()

    def test_dictrecursion(self):
        x = {}
        x["test"] = x
        try:
            self.loadDict(x)
            self.dump()
        except ValueError:
            pass
        else:
            self.fail("didn't raise ValueError on dict recursion")
        x = {}
        y = {"a": x, "b": x}
        # ensure that the marker is cleared
        self.loadDict(y)
        self.dump()

    def test_highly_nested_objects_decoding(self):
        # test that loading highly-nested objects doesn't segfault when C
        # accelerations are used. See #12017
        # str
        with self.assertRaises(RuntimeError):
            self.load('{"a":' * 100000 + '1' + '}' * 100000)
        with self.assertRaises(RuntimeError):
            self.load('{"a":' * 100000 + '[1]' + '}' * 100000)
        with self.assertRaises(RuntimeError):
            self.load('{"a":'+'[' * 100000 + '1' + ']' * 100000 + '}')
        # unicode
        with self.assertRaises(RuntimeError):
            self.load(u'{"a":' * 100000 + u'1' + u'}' * 100000)
        with self.assertRaises(RuntimeError):
            self.load(u'{"a":' * 100000 + u'[1]' + u'}' * 100000)
        with self.assertRaises(RuntimeError):
            self.load(u'{"a":'+u'[' * 100000 + u'1' + u']' * 100000+u'}')

    def test_highly_nested_objects_encoding(self):
        # See #12051
        l, d = [], {}
        for x in xrange(100000):
            l, d = [l], {'k':d}
        with self.assertRaises(RuntimeError):
            self.loadDict(d)
            self.dump()

class TestPyRecursion(TestRecursion, PyTest): pass