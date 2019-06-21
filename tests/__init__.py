# -*- coding: utf-8 -*-
"""
Unit test
"""
import unittest


def run_tests():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite
