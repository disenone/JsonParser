# encoding: utf-8
__author__ = 'lgl'

import os
import sys
import unittest

here = os.path.dirname(__file__)

def test_suite():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    i = 0
    for fn in os.listdir(here):
        if fn.startswith("test") and fn.endswith(".py"):
            i += 1
            modname = fn[:-3]
            __import__(modname)
            module = sys.modules[modname]
            suite.addTests(loader.loadTestsFromModule(module))
    return suite

def main():
    suite = test_suite()
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    main()