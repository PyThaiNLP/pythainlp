# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Unit test.

Each file in tests/ is for each main package.
"""

from unittest import TestLoader, TestSuite

# Names of module to be tested
test_packages: list[str] = [
    "tests.core.test_ancient",
    "tests.core.test_cli",
    "tests.core.test_corpus",
    "tests.core.test_generate",
    "tests.core.test_khavee",
    "tests.core.test_morpheme",
    "tests.core.test_soundex",
    "tests.core.test_spell",
    "tests.core.test_tag",
    "tests.core.test_tokenize",
    "tests.core.test_tools",
    "tests.core.test_transliterate",
    "tests.core.test_util",
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
