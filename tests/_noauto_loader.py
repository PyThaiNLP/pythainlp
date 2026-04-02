# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Shared loader factory for noauto test suites."""

from unittest import TestLoader, TestSuite


def make_load_tests(test_packages: list[str]):
    """Return a load_tests function bound to *test_packages*.

    Each noauto ``__init__.py`` calls this factory so the
    unittest load-test protocol is implemented in one place.
    See: https://docs.python.org/3/library/unittest.html#id1
    """

    def load_tests(
        loader: TestLoader, standard_tests: TestSuite, pattern: str
    ) -> TestSuite:
        suite = TestSuite()
        for name in test_packages:
            suite.addTests(loader.loadTestsFromName(name))
        return suite

    return load_tests
