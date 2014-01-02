JsonParser
=================

JSON (JavaScript Object Notation) <http://json.org> is a subset of JavaScript syntax (ECMA-262 3rd edition) used as a lightweight data interchange format.

JsonParser, a simple Json encoder and decoder for Python 2.7. It is pure Python code with no dependencies.

The encoder can serialize dict into Json presentation. Support keys are str or unicode, supported value types in dict are [dict, list, int, float, bool, None, str, unicode].
It can handle Python str of any specified encoding.

The decoder can handle incoming JSON strings of any specified encoding (UTF-8 by default).

Usage:
Encoding basic Python object hierarchies:
>>> from JsonParser import JsonParser
>>> json = JsonParser('utf8')           # the encoding of str in dict is utf8
>>> json.loadDict({'bar': ['baz', u'baz', True, False, None, 1.0, 2]})
>>> print json.dump()                   # generate Json representation of dict loaded
{"bar":["baz","baz",true,false,null,1.0,2]}
>>> json.dumpJson('json_file.json')     # save Json to file
>>> json.loadJson('json_file.json')     # load Json from file

Decoding Json into Python representation:
>>> json_str = r'{"bar":["\b\\u60a8\u597d","baz","baz",true,false,null,1.0,2]}'
>>> json.load(json_str)
>>> json.dumpDict()
{u'bar': [u'\x08\\u60a8\u597d', u'baz', u'baz', True, False, None, 1.0, 2]}
>>> json
{u'bar': [u'\x08\\u60a8\u597d', u'baz', u'baz', True, False, None, 1.0, 2]}

Method of JsonParser like dict in Python:
>>> json['bar']                         # get item
[u'\x08\\u60a8\u597d', u'baz', u'baz', True, False, None, 1.0, 2]
>>> json.update({'anthor dict': 8e+89}) # update by another dict
>>> json
{u'bar': [u'\x08\\u60a8\u597d', u'baz', u'baz', True, False, None, 1.0, 2], 'anthor dict':8e+89}
>>> json['another dict'] = 0.8          # set item
>>> json
{u'another dict': 0.8, u'bar': [u'\x08\\u60a8\u597d', u'baz', u'baz', True, False, None, 1.0, 2], 'anthor dict': 8e+89}