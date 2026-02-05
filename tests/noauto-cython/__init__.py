# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Unit test suite for Cython-compiled package functionalities.

Test functions that require packages that need Cython compilation:
- phunspell (requires Cython and hunspell C library)

These tests are NOT run in automated CI workflows due to:
- Compilation requirements (Cython, C compiler)
- System library dependencies
- Platform-specific build issues

These tests are kept for manual testing and may be run in separate CI
workflows with appropriate build environments.
"""

from unittest import TestLoader, TestSuite

# Names of module to be tested
test_packages: list[str] = [
    "tests.noauto-cython.testn_spell_cython",
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
