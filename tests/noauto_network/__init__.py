# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Unit test suite for network-dependent functionalities.

Test functions that require network access:
- HuggingFace Hub downloads
- Model downloads from remote servers
- API calls to external services

These tests are NOT run in automated CI workflows due to:
- Network dependency
- Potential for large downloads
- External service availability
- Rate limiting concerns

These tests are kept for manual testing and may be run in environments
with appropriate network access and caching.
"""

from unittest import TestLoader, TestSuite

# Names of module to be tested
test_packages: list[str] = [
    "tests.noauto_network.testn_spell_network",
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
