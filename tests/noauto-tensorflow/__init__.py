# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Unit test suite for TensorFlow-based functionalities.

Test functions that require TensorFlow and its ecosystem dependencies:
- tensorflow
- keras
- deepcut

These tests are NOT run in automated CI workflows due to:
- Very large dependencies (~1-2 GB for tensorflow)
- Potential version conflicts with PyTorch
- Long installation time

These tests are kept for manual testing and may be run in separate CI
workflows dedicated to TensorFlow-based features.
"""

from unittest import TestLoader, TestSuite

# Names of module to be tested
test_packages: list[str] = [
    "tests.noauto-tensorflow.testn_tokenize_tensorflow",
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
