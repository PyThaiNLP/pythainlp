# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Unit test. Extra version.

Test functions that require dependencies beyond "compact" (see pyproject.toml).
"""

from unittest import TestLoader, TestSuite

# Names of module to be tested
test_packages: list[str] = [
    "tests.extra.testx_augment",
    "tests.extra.testx_benchmarks",
    "tests.extra.testx_cli",
    "tests.extra.testx_lm",
    "tests.extra.testx_spell",
    "tests.extra.testx_tag",
    "tests.extra.testx_tokenize",
    "tests.extra.testx_word_vector",
]


def load_tests(
    loader: TestLoader, standard_tests: TestSuite, pattern: str
) -> TestSuite:
    """Load test protocol
    See: https://docs.python.org/3/library/unittest.html#id1
    """
    suite = TestSuite()
    for test_package in test_packages:
        tests = loader.loadTestsFromName(test_package)
        suite.addTests(tests)
    return suite


if __name__ == "__main__":
    import unittest

    unittest.main()
