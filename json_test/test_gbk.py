# encoding: gbk
__author__ = 'lgl'
from __init__ import PyTest
import os

GBK_DICT = {
    "JSON Test Pattern pass3": {
        "The outermost value": "must be an object or array.",
        "In this test": "It is an object."
    },
    "中文" : { "这个GBK编码的中文字符串": "chinese" }
}

UNICODE_DICT = {
    u"JSON Test Pattern pass3": {
        u"The outermost value": "must be an object or array.",
        u"In this test": "It is an object."
    },
    u"中文" : { u"这个GBK编码的中文字符串": "chinese" }
}

class TestGBK(object):
    def test_success(self):
        file_name = 'test_case/gbk.json'
        try:
            fp = open(file_name)
            s = fp.read()
        except IOError:
            pass
        finally:
            fp.close()
        try:
            self.pyjson_gbk.load(s)
            out_json = self.pyjson_gbk.dump()
            d1 = self.pyjson_gbk.dumpDict()
            self.pyjson_gbk.load(out_json)
            d2 = self.pyjson_gbk.dumpDict()
            self.assertEqual(d1, d2)
            name = 'test_case/gbk_temp.json'
            self.pyjson_gbk.dumpJson(name)
            self.pyjson_gbk.loadJson(name)
            d3 = self.pyjson_gbk.dumpDict()
            self.assertEqual(d1, d3)
            os.remove(name)
        except ValueError:
            self.fail("Expected pass for gbk.json: {0!r}".format(s))
        else:
            pass

    def test_gbk_dict(self):
        self.pyjson_gbk.loadDict(GBK_DICT)
        self.loadDict(UNICODE_DICT)
        uni1 = self.pyjson_gbk.dump()
        uni2 = self.dump()
        self.assertEqual(uni1, uni2)
        d1 = self.pyjson_gbk.dumpDict()
        self.assertEqual(d1, GBK_DICT)
        d2 = self.dumpDict()
        self.assertEqual(d2, UNICODE_DICT)
class TestPyGBK(TestGBK, PyTest): pass