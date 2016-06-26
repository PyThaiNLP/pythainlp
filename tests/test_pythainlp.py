#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pythainlp
----------------------------------

Tests for `pythainlp` module.
"""


import sys
import unittest
from contextlib import contextmanager
from pythainlp.segment.pyicu import icu

from pythainlp import pythainlp



class TestPythainlp(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    def test_command_line_interface(self):
        runner = icu("ทดสอบระบบ")
        #result = runner.invoke(icu.main)
        assert result.exit_code == 0
        #assert 'pythainlp.segment.pyicu.main' in result.output
        #help_result = runner.invoke(cli.main, ['--help'])
        #assert help_result.exit_code == 0
        #assert '--help  Show this message and exit.' in help_result.output


if __name__ == '__main__':
    sys.exit(unittest.main())
