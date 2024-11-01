# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Unit test.

Each file in tests/ is for each main package.
"""

from unittest import TestLoader, TestSuite

test_packages: list[str] = [
#    "tests.test_cli.TestMainPackage",
#    "tests.test_soundex.TestSoundexPackage",
#    "tests.test_spell.TestSpellPackage",
#    "tests.test_tokenize.TestTokenizePackage",
#    "tests.test_util.TestUtilPackage",
]


def load_tests(loader: TestLoader, tests, pattern) -> TestSuite:
    """A function to load tests."""
    suite = TestSuite()
    for test_package in test_packages:
        tests = loader.loadTestsFromName(test_package)
        suite.addTests(tests)
    return suite
