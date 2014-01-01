# encoding: utf8
__author__ = 'lgl'

from __init__ import PyTest

class TestEncode(object):
    def test_dump(self):
        d = {}
        self.loadDict(d)
        self.assertEqual(self.dump(), u'{}')

    def test_encode_truefalse(self):
        d = {'True': False, 'False': True, 'None': None}
        self.loadDict(d)
        self.assertEqual(self.dump(), u'{"True":false,"None":null,"False":true}')
        d = {2: 3.0, 4.0: 5L, False: 1, 6L: True}
        self.loadDict(d)
        self.assertEqual(self.dump(), u'{}')

    def test_deep_copy(self):
        d = {'key': [u'key', 123], 'key2':{'a':321}}
        self.loadDict(d)
        self.assertNotEqual(id(d), self.dict_id())
        self.assertNotEqual(id(d['key2']), self.dumpDict()['key2'])
        self.assertNotEqual(id(d['key']), self.dumpDict()['key'])

class TestPyEncode(TestEncode, PyTest): pass