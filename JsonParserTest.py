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
    j = JsonParser()
    j.load(r'["a\tb"]')
    print j
    print j.dump()
    print json.loads(r'"\ttabcharacterinstring"', strict = True)


def test_json_loadJson():
    # fp = open(u"中文_utf8.txt")
    # print fp.read().decode('utf8')
    # fp = open(u"中文_gbk.txt")
    # print fp.read().decode('gbk')
    jp = JsonParser()
    # print jp.loadJson(u"中文_utf8.txt", 'utf8')
    jp.loadJson(u"TestCaseForLoad.txt", 'utf8')
    print 'load from file: ', jp
    fp = open(u'my_test/test_case/pass3.json')
    s = fp.read()
    jp.load(s)
    print jp
    jp.loadJson(u'my_test/test_case/pass3.json')
    fp = open("save.txt", mode='w')
    s = jp.dump()
    fp.write(s.encode('utf8'))
    fp = open(u'my_test/test_case/pass3.json')
    print json.load(fp, 'utf8')

def test_json_dump():
    d = {"abc": 123}
    a = json.dumps(d)

    jp = JsonParser()
    jp.loadJson(u"TestCaseForLoad.txt", 'utf8')
    print jp
    json_str = jp.dump()
    print repr(json_str)
    print jp['a']
    print jp[u'我']

def test_json_loadDict():
    d = {'您key': [u'key', 123], 'key2':{'a':321}}
    jp = JsonParser()
    jp.loadDict(d)
    print repr(jp)
    print repr(jp.dump())
    print jp['您key']

from JsonParser import has_utf8_char
from JsonParser import encode_string
def test_utf8_char():
    print has_utf8_char('您好')
    print has_utf8_char('您好')
    print has_utf8_char(u'asdfas')
    encode_string_utf8 = encode_string('utf8')
    encode_string_utf8('\xce\xb1\xce\xa9')

def test_check_circular():
    x = []
    x.append(x)
    d = {'x': x}
    jp = JsonParser()
    jp.loadDict(d)
    jp.dump()

def test_float_out_of_range():
    jp = JsonParser()
    jp.loadJson('my_test/test_case/fail35.json')
    print jp
    print jp.dump()

JSON = r'{ "abc":[[[[[[[[[[[[[[[[[[["Not too deep"]]]]]]]]]]]]]]]]]]] }'
def test_parse():
    jp = JsonParser()
    jp.load(JSON)
    out = jp.dump()
    print repr(out)
    d1 = jp.dumpDict()
    jp.load(out)
    d2 = jp.dumpDict()
    print d1==d2

# test_scan_string()s
# test_white_space_match()
# test_json_object()
# test_match_number()
# test_json_load()
# test_json_loadJson()
# test_json_dump()
# print JsonParser.__module__
# import my_test.test_fail
# test_json_loadDict()
# test_utf8_char()
# test_check_circular()
# test_float_out_of_range()
# test_parse()
