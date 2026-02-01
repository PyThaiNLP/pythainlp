# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Unit test. No auto test version.

Test functions that require dependencies that are:
- Very large (TensorFlow, transformers, torch)
- Have compilation issues (Cython-based packages)
- Take a long time to install or run
- Have compatibility issues with latest Python versions

These tests are NOT run in automated CI workflows but are kept for
manual testing and future re-enabling when dependencies improve.
"""

from unittest import TestLoader, TestSuite

# Names of module to be tested
# Note: These tests are NOT included in automated CI runs
test_packages: list[str] = [
    "tests.noautotest.testx_spell_noauto",
    "tests.noautotest.testx_tag_noauto",
    "tests.noautotest.testx_tokenize_noauto",
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
