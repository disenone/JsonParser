# encoding: utf-8
__author__ = 'lgl'

def output_err(msg, string, begin, end = None):
    def get_line_col(string, begin):
        line_num = 1 + string.count('/n', 0, begin)
        if line_num == 1:
            return line_num, begin
        else:
            col_num = begin - string.rindex('\n', 0, begin)
            return line_num, col_num
    row, col = get_line_col(string, begin)
    out = '{0}: line {1}, col {2}, char {3}: "{4}"'
    return out.format(msg, row, col, begin, string[begin: end if end else begin + 1 ])


__all__ = ['JsonParser']

INFINITY = float('inf')
NEG_INFINITY = float('-inf')
NAN = float('nan')

FLOAT_CONSTANTS = {
    '-Infinity': INFINITY,
    'Infinity': NEG_INFINITY,
    'NaN': NAN,
}

NUMBER = '0123456789'
HEX_NUMBER = '0123456789abcdefABCDEF'

BACKSLASH = {
    '"': u'"', '\\': u'\\', '/': u'/',
    'b': u'\b', 'f': u'\f', 'n': u'\n', 'r': u'\r', 't': u'\t',
}

CONTROL_CHAR = [
    '\b', '\f', '\n', '\r', '\t'
]

WHITESPACE_STR = ' \t\n\r'

ESCAPE_Python_2_Json = {
    u'\\': u'\\\\',
    u'"': u'\\"',
    u'\b': u'\\b',
    u'\f': u'\\f',
    u'\n': u'\\n',
    u'\r': u'\\r',
    u'\t': u'\\t',
}

# predefined encoding
DEFAULT_ENCODING = "utf-8"
UNICODE_ENCODING = 'unicode'



def has_utf8_char(s):
    """
    simply check if s has utf8 char
    """
    for c in s:
        i = ord(c)
        if i > 0x80 and i <= 0xff:
            return True
    return False

def convert_str_2_unicode(s, encoding = UNICODE_ENCODING):
    """
    convert a str to unicode, if encoding is given, will try to decode the str by the given encoding
    it will also guess if the string is utf8
    if fail to convert the string, it will just return u''
    """
    if isinstance(s, str):
        if encoding != UNICODE_ENCODING:
            s = s.decode(encoding)
        elif has_utf8_char(s):
            s = s.decode('utf8')
        else:
            s = unicode(s)
    if isinstance(s, unicode):
        return s
    return u''

def match_string(s, idx):
    """
    match [", \, /, \f, \b, \n, \r, \t, \u, chars] begin at s[idx], return matched string
    for a string s = '"abc"', idx should not less than 1, which is the position of 'a',
    or the function will return u'' for nothing found
    """
    # catch index error
    try:
        char = ""
        if s[idx] == '"':
            # reach the end of the string
            return (None, idx + 1)
        elif s[idx] == '\\':
            # find backslash
            idx += 1;
            if s[idx] == 'u':
                # find json \uxxxx
                nums = s[idx + 1: idx + 5]
                next_end = idx + 5
                # check the four char is num
                for one_num in nums:
                    if one_num not in HEX_NUMBER:
                        raise ValueError(output_err("Invalid \\uXXXX", s, idx, idx+5))
                uni = int(nums, 16)
                char = unichr(uni)
                return (char, next_end)
            else:
                # control char
                try:
                    char = BACKSLASH[s[idx]]
                except KeyError:
                    raise ValueError(output_err('Invalid \\escape: ' + repr(s[idx]), s, idx))
                return (char, idx + 1)
        elif s[idx] > '\x1f':
            # find normal chars
            while s[idx] != '"' and s[idx] != '\\' and s[idx] > '\x1f':
                char += s[idx]
                idx += 1
            return (unicode(char), idx)
        else:
            # others invalid char
            raise ValueError(output_err('Invalid control character', s, idx))
    except IndexError:
        raise ValueError(output_err("Unterminated string starting at", s, idx - 1))


def parse_json_string(s, idx, encoding=DEFAULT_ENCODING):
    """
    Return a unicode Python representation of a Json string
    """
    trunks = []
    _append = trunks.append;
    s = convert_str_2_unicode(s, encoding)
    while True:
        ustr, idx = match_string(s, idx)
        if not ustr:
            break
        _append(ustr)
    return u''.join(trunks), idx

def match_integer(s, idx):
    """
    greedily match integer of [0123456789]
    """
    integer = ''
    nextchar = s[idx:idx + 1]
    while nextchar != '' and nextchar in NUMBER:
        integer += nextchar
        idx += 1
        nextchar = s[idx:idx + 1]
    return integer, idx


def match_number(s, idx):
    """
    match a valid number of int or float
    """
    integer = None
    frac = None
    exp = None
    nextchar = s[idx:idx + 1]

    # get integer part
    if nextchar == '-':
        integer = nextchar
        idx += 1
    _int, idx = match_integer(s, idx)
    # check heading 0 of integer
    if len(_int) > 1:
        if _int[0:1] == '0':
            return None, None, None
    if integer:
        integer += _int
    else:
        integer = _int

    # get frac part
    nextchar = s[idx:idx + 1]
    if nextchar == '.':
        frac = '.'
        idx += 1
        _int, idx = match_integer(s, idx)
        frac += _int
    # check fraction which only has '.'
    if frac:
        if frac == '.':
            return None, None, None

    # get exp part
    nextchar = s[idx:idx + 1]
    if nextchar == 'e' or nextchar == 'E':
        exp = nextchar
        idx += 1
        nextchar = s[idx:idx + 1]
        if nextchar == '-' or nextchar == '+':
            exp += nextchar
            idx += 1
        _int, idx = match_integer(s, idx)
        if _int != '':
            exp += _int
        else:
            exp = ''
            idx -= 1

    # check number validity
    if (integer == '-' or integer == '') and (frac == '.' or frac == ''):
        integer = None
        frac = None
        exp = None

    return integer, frac, exp, idx

def match_whitespace(s, idx):
    """
    greedily match white spaces, return white spaces matched and index follows
    """
    white_space = ''
    length = len(s)
    if idx >= length:
        return "", idx
    while s[idx] in WHITESPACE_STR:
        white_space += s[idx]
        idx += 1
        if idx >= length:
            break
    return white_space, idx

def get_next_char(string, idx):
    try:
        return string[idx], idx+1
    except IndexError:
        raise ValueError(output_err('unexpected end of string', string, idx))

def parse_json_object(string, begin, encoding):
    # check string or empty
    white_space, idx = match_whitespace(string, begin)
    c, idx = get_next_char(string, idx)
    if c != '"':
        if c == '}':
            return {}, idx
        else:
            raise ValueError(output_err('Object is not complete, expecting "}"', string, idx))

    out_dict = {}
    while True:
        # get key
        key, idx = parse_json_string(string, idx, encoding)

        # find :
        white_space, idx = match_whitespace(string, idx)
        c, idx = get_next_char(string, idx)
        if c != ':':
            raise ValueError(output_err('Excepting ":" after key string', string, idx))

        # get value
        value, idx = decode_one_json(string, idx, encoding)

        # add to dict
        out_dict[key] = value

        # find ,
        white_space, idx = match_whitespace(string, idx)
        c, idx = get_next_char(string, idx)
        if c == '}':
            break
        if c != ',':
            raise ValueError(output_err('Excepting "," or "}"', string, idx))

        white_space, idx = match_whitespace(string, idx)
        c, idx = get_next_char(string, idx)
        if c != '"':
            raise ValueError(output_err('Excepting """', string, idx))

    return out_dict, idx

def parse_json_array(string, begin, encoding):
    # check empty
    white_space, idx = match_whitespace(string, begin)
    c, idx = get_next_char(string, idx)
    if c == ']':
        return [], idx
    out_array = []
    idx = idx - 1
    while True:
        # get one value in array
        value, idx = decode_one_json(string, idx, encoding)
        out_array.append(value)

        # check for the next or end
        white_space, idx = match_whitespace(string, idx)
        c, idx = get_next_char(string, idx)
        if c == ']':
            break
        if c != ',':
            raise ValueError(output_err('Excepting "," or "]"', string, idx))
        white_space, idx = match_whitespace(string, idx)
    return out_array, idx

def parse_json_null(string, begin):
    if string[begin: begin+4] == 'null':
        return None, begin+4
    else:
        raise KeyError

def parse_json_true(string, begin):
    if string[begin: begin+4] == 'true':
        return True, begin+4
    else:
        raise KeyError

def parse_json_false(string, begin):
    if string[begin: begin+5] == 'false':
        return False, begin+5
    else:
        raise KeyError

def parse_json_number(string, begin):
    integer, frac, exp, idx = match_number(string, begin)
    # find number
    if integer or frac :
        # if float
        if frac or exp:
            res = float((integer or '') + (frac or '') + (exp or ''))
            if res == float('inf') or res == float('-inf') or res == float('nan'):
                raise ValueError(output_err('Number out of range: ', string, begin, idx))
        # else integer
        else:
            res = int(integer)
        return res, idx
    else:
        raise ValueError(output_err('Can not parse json string: ', string, idx))

# a function map for decode different json type
decode_func_map = {
    '"': lambda string, idx, encoding: parse_json_string(string, idx, encoding),
    '{': lambda string, idx, encoding: parse_json_object(string, idx, encoding),
    '[': lambda string, idx, encoding: parse_json_array(string, idx, encoding),
    'n': lambda string, idx, encoding: parse_json_null(string, idx-1),
    't': lambda string, idx, encoding: parse_json_true(string, idx-1),
    'f': lambda string, idx, encoding: parse_json_false(string, idx-1)
}

def decode_one_json(string, begin, encoding):
    first = False
    if begin == 0:
        first = True

    white_space, idx = match_whitespace(string, begin)
    c, idx = get_next_char(string, idx)

    # if the first time enter this func, check if it's a json object, we will only parse json object
    if first and c != '{':
        raise ValueError(output_err('Expecting "{" at the beginning of json string: ', string, idx))

    # call different func to parse, based on the beginning char
    try:
        return decode_func_map[c](string, idx, encoding)
    except KeyError:
        return parse_json_number(string, idx-1)

def decode_json(string, begin, encoding = DEFAULT_ENCODING):
    """
    entry function to decode a json string, any error will be raise by ValueError with a error msg

    """
    obj, end = decode_one_json(string, begin, encoding)
    white_spaces, end = match_whitespace(string, end)
    # check if more data that we have not parsed
    str_len = len(string)
    if end != str_len:
        raise ValueError(output_err("Redundant data detected", string, end, str_len))
    return obj, end

def encode_python_string(encoding = UNICODE_ENCODING):
    """
    Return a unicode JSON representation of a Python unicode string
    """
    def _encode(pystr):
        def convert_escape(pc):
            """
            Convert python escape into json string
            """
            try:
                jc = ESCAPE_Python_2_Json[pc]
            except KeyError:
                n = ord(pc)
                if n < 0x20 or n > 0x7e:
                    return u'\\u{0:04x}'.format(n)
                else:
                    return pc
            return jc

        pystr = convert_str_2_unicode(pystr, encoding)
        # begining of the string
        json_uni = u'"'
        # convert escape
        for pc in pystr:
            json_uni += convert_escape(pc)
        # end of the string
        json_uni += u'"'
        return json_uni
    return _encode

def encode_python_float(f, encoding):
    """
    Encode python float num into json
    """
    if f != f  or f == INFINITY or f == NEG_INFINITY:
        raise ValueError("Float values out of range : " + repr(f))
    else:
        return repr(f).decode(encoding)

def encode_python_dict(dct, encoding, id_record):
    """
    Encode pyhton dict into json
    """
    if not dct:
        return '{}'
    # check circular
    dict_id = id(dct)
    if dict_id in id_record:
        raise ValueError("Circular reference found.")
    id_record[dict_id] = dct
    # beginning of dict
    str_arrray = ['{']
    append = str_arrray.append

    first = True
    for key, value in dct.iteritems():
        # if the first item, no ',' in front of it
        if first:
            first = False
        # else add ',' before this item
        else:
            append(',')
        # key must be string
        append(encode_python_string(encoding)(key))
        # ':' between key and value
        append(':')
        # encode value to json
        append(encode_python(value, encoding, id_record))
    # end of dict
    append('}')
    # return a single unicode
    return u''.join(str_arrray)

def encode_python_list(lst, encoding, id_record):
    """
    encode python list into json
    """
    if not lst:
        return '[]'
    # check circular
    list_id = id(lst)
    if list_id in id_record:
        raise ValueError("Circular reference found.")
    id_record[list_id] = lst
    # beginning of list
    str_array = ['[']
    append = str_array.append
    first = True
    for value in lst:
        # first item nothing before
        if first:
            first = False
        # else put a ',' before this item
        else:
            append(',')
        # encode value
        append(encode_python(value, encoding, id_record))
    # end of list
    append(']')
    # return a single unicode
    return u''.join(str_array)


def encode_python(obj, encoding = UNICODE_ENCODING, id_record = {}):
    """
    entry function to encode a python object, any error will be raise by ValueError with a error msg

    """
    str_array = []
    append = str_array.append
    if isinstance(obj, dict):
        append( encode_python_dict(obj, encoding, id_record) )
    elif isinstance(obj, list):
        append( encode_python_list(obj, encoding, id_record) )
    elif isinstance(obj, basestring):
        append(encode_python_string(encoding)(obj))
    elif isinstance(obj, float):
        append( encode_python_float(obj, encoding) )
    # True, False must be encode before int, because True, False is instance of int
    elif obj is True:
        append( u'true')
    elif obj is False:
        append( u'false')
    # now we can deal with int
    elif isinstance(obj, (int, long)):
        append( str(obj) )
    elif obj is None:
        append( u'null')
    # any other type will not be supported
    else:
        raise ValueError("Type {0} is not supported".format(repr(type(obj))))
    return u''.join(str_array)

class JsonParser:
    def __init__(self, encoding=DEFAULT_ENCODING):
        """
        encoding, specify the encoding of input json. The default is UTF-8.
        """
        self.__data = {}
        self.encoding = encoding
    def load(self, s):
        """
        load json string, save it as python dict in self.__data
        """
        if not isinstance(s, basestring):
            raise ValueError("Input must be str or unicode, (type {0} is given).".format(type(s)))
        s = convert_str_2_unicode(s, self.encoding)
        self.__data, end = decode_json(s, 0, self.encoding)
        end = end + 1;
        return end
    def loadJson(self, f):
        """
        load json string from file f, save it as python dict in self.__data
        """
        with open(f) as fp:
            s = fp.read()
        s = convert_str_2_unicode(s, self.encoding)
        self.__data, end = decode_json(s, 0, self.encoding)

    def dump(self):
        """
        return json string base on dict self.__data
        """
        return encode_python(self.__data, self.encoding)

    def dumpJson(self, f):
        """
        save json string base on dict self.__data into file f
        """
        with open(f, 'w') as fp:
            fp.write(encode_python(self.__data, self.encoding))

    def update(self, d):
        """
        update self.__data by another dict, use deepcopy
        only keys of str or unicode will be concerned, other type of object will be ignored
        """
        if not isinstance(d, dict):
            raise ValueError('Input must be dict, (type {0} is given).'.format(type(d)))
        for key, value in d.iteritems():
            if isinstance(key, basestring):
                self.__data[key] = my_deepcopy(value)

    def loadDict(self, d):
        """
        deep copy a dict into self.__data
        """
        self.__data = {}
        self.update(d)

    def dumpDict(self):
        """
        return a Python dict, deepcopy of self.__data
        """
        return my_deepcopy(self.__data)

    def dict_id(self):
        """
        get the object id of self.__data
        """
        return id(self.__data)

    def __getitem__(self, key):
        """
        method like dict, return value of key
        """
        return self.__data[key]

    def __setitem__(self, key, value):
        """
        set value of key, if not exist, create one
        """
        if isinstance(key, basestring):
            key = convert_str_2_unicode(key)
            self.__data[key] = value

    def __repr__(self):
        return repr(self.__data)

    def __str__(self):
        return str(self.__data)


def my_deepcopy(obj, memory={}):
    """
    make a deep copy of object obj
    """
    # check if obj exist in memory
    obj_id = id(obj)
    copy = memory.get(obj_id, None)
    if copy is not None:
        return copy

    # get the type copier
    cls = type(obj)
    deep_copier = _deepcopy_func_map.get(cls, None)
    if deep_copier:
        copy = deep_copier(obj, memory)
    else:
        raise ValueError( "Not support object of type {0}".format(str(cls)))

    # keep obj alive
    memory[obj_id] = copy
    _add_to_memory(obj, memory)
    return copy

def _add_to_memory(obj, memory):
    try:
        memory[id(memory)].append(obj)
    except KeyError:    # if not exist, create then
        memory[id(memory)]=[obj]

# a dict to remember types which can be deep copied
_deepcopy_func_map = {}

# a basic copy, only return obj itself
def _deepcopy_basic(obj, memory):
    return obj

# deep copy for list, iteratively deep copy items
def _deepcopy_list(lst, memory):
    y = []
    # memory the list
    memory[id(lst)] = y
    for value in lst:
        y.append(my_deepcopy(value, memory))
    return y

# deep copy for list, iteratively deep copy items
def _deepcopy_dict(dct, memory):
    y = {}
    # memory the dict
    memory[id(dct)] = y
    for key, value in dct.iteritems():
        y[my_deepcopy(key, memory)] = my_deepcopy(value, memory)
    return y

"""
only [None, int, long, float, bool, str, unicode, list, dict] can be deep copied
"""
_deepcopy_func_map[type(None)] = _deepcopy_basic
_deepcopy_func_map[int] = _deepcopy_basic
_deepcopy_func_map[long] = _deepcopy_basic
_deepcopy_func_map[float] = _deepcopy_basic
_deepcopy_func_map[bool] = _deepcopy_basic
_deepcopy_func_map[str] = _deepcopy_basic
_deepcopy_func_map[unicode] = _deepcopy_basic
_deepcopy_func_map[list] = _deepcopy_list
_deepcopy_func_map[dict] = _deepcopy_dict