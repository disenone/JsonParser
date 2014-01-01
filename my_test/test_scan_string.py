# encoding: utf-8
__author__ = 'lgl'
from __init__ import PyTest
from __init__ import scan_string

UNICODE_CASES = [
    (u'/\\"\ucafe\ubabe\uab98\ufcde\ubcda\uef4a\x08\x0c\n\r\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?', u'"/\\\\\\"\\ucafe\\ubabe\\uab98\\ufcde\\ubcda\\uef4a\\b\\f\\n\\r\\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?"'),
    (u'\u0123\u4567\u89ab\ucdef\uabcd\uef4a', u'"\\u0123\\u4567\\u89ab\\ucdef\\uabcd\\uef4a"'),
    (u'controls', u'"controls"'),
    (u'\x08\x0c\n\r\t', u'"\\b\\f\\n\\r\\t"'),
    (u'{"object with 1 member":["array with 1 element"]}', u'"{\\"object with 1 member\\":[\\"array with 1 element\\"]}"'),
    (u' s p a c e d ', u'" s p a c e d "'),
    (u'\U0001d120', u'"\\ud834\\udd20"'),
    (u'\u03b1\u03a9', u'"\\u03b1\\u03a9"'),
    (u'\u03b1\u03a9', u'"\\u03b1\\u03a9"'),
    (u'\u03b1\u03a9', u'"\\u03b1\\u03a9"'),
    (u'\u03b1\u03a9', u'"\\u03b1\\u03a9"'),
    (u"`1~!@#$%^&*()_+-={':[,]}|;.</>?", u'"`1~!@#$%^&*()_+-={\':[,]}|;.</>?"'),
    (u'\x08\x0c\n\r\t', u'"\\b\\f\\n\\r\\t"'),
    (u'\u0123\u4567\u89ab\ucdef\uabcd\uef4a', u'"\\u0123\\u4567\\u89ab\\ucdef\\uabcd\\uef4a"'),
]

UTF8_CASE = [
    (u'\u60a8\u597d', u'"您好"'),
    (u'\u60a8\u597d', '"您好"'),
]

class TestScanString(object):
    def test_encode_unicode(self):
        for expect, input_string in UNICODE_CASES:
            result, end = scan_string(input_string, 1)
            self.assertEqual(result, expect,
                '{0!r} != {1!r} for ({2!r})'.format(
                    result, expect, input_string))

    def test_encode_utf8(self):
        for expect, input_string in UTF8_CASE:
            result, end = scan_string(input_string, 1)
            self.assertEqual(result, expect,
                '{0!r} != {1!r} for ({2!r})'.format(
                    result, expect, input_string))

class TestPyScanString(TestScanString, PyTest): pass