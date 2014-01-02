JsonParser
=================

JSON (JavaScript Object Notation) <http://json.org> is a subset of JavaScript syntax (ECMA-262 3rd edition) used as a lightweight data interchange format.

JsonParser(https://github.com/lugliang/JsonParser), a simple Json encoder and decoder for Python 2.7. It is pure Python code with no dependencies.

The encoder can serialize Python Dict into Json representation. It can handle Python str of any specified encoding (UTF-8 by default). It supports the following objects and types:

    +-------------------+---------------+
    | Python            | JSON          |
    +===================+===============+
    | dict              | object        |
    +-------------------+---------------+
    | list              | array         |
    +-------------------+---------------+
    | str, unicode      | string        |
    +-------------------+---------------+
    | int, long, float  | number        |
    +-------------------+---------------+
    | True              | true          |
    +-------------------+---------------+
    | False             | false         |
    +-------------------+---------------+
    | None              | null          |
    +-------------------+---------------+

The decoder can parse the Json representation into Python object. It can handle incoming JSON strings of any specified encoding (UTF-8 by default). It performs the following translations in decoding by default:

    +---------------+-------------------+
    | JSON          | Python            |
    +===============+===================+
    | object        | dict              |
    +---------------+-------------------+
    | array         | list              |
    +---------------+-------------------+
    | string        | unicode           |
    +---------------+-------------------+
    | number (int)  | int, long         |
    +---------------+-------------------+
    | number (real) | float             |
    +---------------+-------------------+
    | true          | True              |
    +---------------+-------------------+
    | false         | False             |
    +---------------+-------------------+
    | null          | None              |
    +---------------+-------------------+

Usage:

Encoding basic Python object hierarchies:

    from JsonParser import JsonParser
    json = JsonParser('utf8')           # the encoding of str in Python dict is utf8
    json.loadDict({'bar': ['baz', u'baz', True, False, None, 1.0, 2]})
    print json.dump()                   # generate Json representation of dict loaded
    #{"bar":["baz","baz",true,false,null,1.0,2]}
    json.dumpJson('json_file.json')     # save Json to file
    json.loadJson('json_file.json')     # load Json from file


Decoding Json into Python representation:

    json_str = r'{"bar":["\b\\u60a8\u597d","baz","baz",true,false,null,1.0,2]}'
    json.load(json_str)
    json.dumpDict()
    #{u'bar': [u'\x08\\u60a8\u597d', u'baz', u'baz', True, False, None, 1.0, 2]}
    print json
    #{u'bar': [u'\x08\\u60a8\u597d', u'baz', u'baz', True, False, None, 1.0, 2]}

Method of JsonParser like dict in Python:
    
    json_str = r'{"bar":["\b\\u60a8\u597d","baz","baz",true,false,null,1.0,2]}'
    json.load(json_str)
    json['bar']                         # get item
    #[u'\x08\\u60a8\u597d', u'baz', u'baz', True, False, None, 1.0, 2]
    json.update({'another dict': 8e+89}) # update by another dict
    json
    #{'another dict': 8e+89, u'bar': [u'\x08\\u60a8\u597d', u'baz', u'baz', True, False, None, 1.0, 2]}
    json['another dict'] = 0.8          # set item
    json
    #{u'another dict': 0.8, u'bar': [u'\x08\\u60a8\u597d', u'baz', u'baz', True, False, None, 1.0, 2], 'anthor dict': 8e+89}
