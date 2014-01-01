# encoding: utf8
__author__ = 'lgl'

from __init__ import PyTest
from __init__ import encode_string_unicode
from __init__ import encode_string_utf8

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
    ('\xce\xb1\xce\xa9', u'"\\u03b1\\u03a9"'),
    ('\xce\xb1\xce\xa9', u'"\\u03b1\\u03a9"'),
]

class TestEncodeString(object):
    def test_encode_unicode(self):
        for input_string, expect in UNICODE_CASES:
            result = encode_string_unicode(input_string)
            self.assertEqual(result, expect,
                '{0!r} != {1!r} for ({2!r})'.format(
                    result, expect, input_string))

    def test_encode_utf8(self):
        for input_string, expect in UTF8_CASE:
            result = encode_string_utf8(input_string)
            self.assertEqual(result, expect,
                '{0!r} != {1!r} for ({2!r})'.format(
                    result, expect, input_string))

class TestPyEncodeString(TestEncodeString, PyTest): pass