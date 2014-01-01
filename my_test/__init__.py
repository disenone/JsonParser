# encoding: utf-8
__author__ = 'lgl'

import JsonParser
import unittest

encode_string_utf8 = JsonParser.encode_string('utf8')
encode_string_unicode = JsonParser.encode_string()
scan_string = JsonParser.scan_string

class PyTest(unittest.TestCase):
    pyjson = JsonParser.JsonParser()
    load = pyjson.load
    dump = pyjson.dump
    loadJson = pyjson.loadJson
    dumpJson = pyjson.dumpJson
    loadDict = pyjson.loadDict
    dumpDict = pyjson.dumpDict
    update = pyjson.update
    dict_id = pyjson.dict_id
    # def __init__(self):
    #     self.pyjson = JsonParser()
    #     self.load = self.pyjson.load
    #     self.dump = self.pyjson.dump
    #     self.loadJson = self.pyjson.loadJson
    #     self.dumpJson = self.pyjson.dumpJson
    #     self.loadDict = self.pyjson.loadDict
