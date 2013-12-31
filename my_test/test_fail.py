# encoding: utf-8
__author__ = 'lgl'

from __init__ import PyTest

class TestFail(object):
    def test_failures(self):
        file_name = 'test_case/fail'
        idx = 1
        while True:
            try:
                name = file_name + str(idx) + '.json'
                fp = open(name)
            except IOError:
                break #self.fail("open fail: "+name)
            s = fp.read()
            try:
                self.load(s)
            except ValueError:
                pass
            else:
                self.fail("Expected failure for fail{0}.json: {1!r}".format(idx, s))
            idx += 1

    def test_non_string_keys_dict(self):
        data = {'a' : 1, (1, 2) : 2}
        self.loadDict(data)
        d = self.dumpDict()
        self.assertEqual(d, {'a':1})

class TestPyFail(TestFail, PyTest): pass

# if __name__ == '__main__':
#     unittest.main()
