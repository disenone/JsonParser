# encoding: utf-8

from JsonParser import JsonParser
from JsonParser import match_string
from JsonParser import scan_string
from JsonParser import match_whitespace
from json import decoder
import json

def test_scan_string():
    #print matchString('"d"', 1)
    print scan_string('"da sdf"', 1)
    print scan_string('"da sdf\u1234\f\b\n\x21"', 1)
    print '-------------------------'
    print decoder.py_scanstring('"das df\u1234\f\b\n\x21"', 1, strict = False)

def test_scan_num():
    print json.loads('[NaN]', strict = False)

def test_num_change(num):
     num+=1
     print num

def test_white_space_match():
    white_space, end = match_whitespace('\n', 0)
    print repr(white_space), end
#test_scan_string()

from JsonParser import json_object
from JsonParser import JsonDecoder
from json import scanner
def test_json_object():
    jd = JsonDecoder()
    pairs, end = json_object(('"abc":213}', 0), 'utf-8', jd.scan)
    print pairs, type(pairs)
    jd = decoder.JSONDecoder()
    pairs, end = decoder.JSONObject(('"abc":213}', 0), 'utf-8', scan_once = jd.scan_once, strict=False, object_hook=None, object_pairs_hook=None)
    print pairs, type(pairs)
    p = []
    print type(p)
    p.append(('abc', 213))
    print type(p)

from JsonParser import match_number
def test_match_number():
    print match_number('e1', 0)
    print match_number('1,', 0)

def test_json_load():
    print json.loads('"asdba"')
    j = JsonParser()
    print j.load('["asdba"]')


def test_json_loadJson():
    # fp = open(u"中文_utf8.txt")
    # print fp.read().decode('utf8')
    # fp = open(u"中文_gbk.txt")
    # print fp.read().decode('gbk')
    jp = JsonParser()
    # print jp.loadJson(u"中文_utf8.txt", 'utf8')
    jp.loadJson(u"TestCaseForLoad.txt", 'utf8')
    print jp
    fp = open(u"TestCaseForLoad.txt")
    print json.load(fp, 'utf8')

def test_json_dump():
    d = {"abc": 123}
    a = json.dumps(d)

    jp = JsonParser()
    jp.loadJson(u"TestCaseForLoad.txt", 'utf8')
    print jp
    json_str = jp.dump()
    print repr(json_str)

# test_scan_string()
# test_white_space_match()
# test_json_object()
# test_match_number()
# test_json_load()
# test_json_loadJson()
test_json_dump()