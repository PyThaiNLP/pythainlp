# -*- coding: utf-8 -*-
"""
Unit test.

Each file in tests/ is for each main package.
"""
import sys
import unittest

sys.path.append("../pythainlp")

loader = unittest.TestLoader()
testSuite = loader.discover("tests")
testRunner = unittest.TextTestRunner(verbosity=1)
testRunner.run(testSuite)
