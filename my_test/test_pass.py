# encoding: utf-8
__author__ = 'lgl'
from __init__ import PyTest

class TestPass(object):
    def test_success(self):
        file_name = 'test_case/pass'
        idx = 1
        while True:
            try:
                name = file_name + str(idx) + '.json'
                fp = open(name)
                s = fp.read()
            except IOError:
                break #self.fail("open fail: "+name)
            finally:
                fp.close()
            try:
                self.load(s)
            except ValueError:
                self.fail("Expected pass for pass{0}.json: {1!r}".format(idx, s))
            else:
                pass
            out_json = self.dump()
            d1 = self.dumpDict()
            self.load(out_json)
            d2 = self.dumpDict()
            self.assertEqual(d1, d2)
            idx += 1

class TestPyPass(TestPass, PyTest): pass

# if __name__ == '__main__':
#     unittest.main()