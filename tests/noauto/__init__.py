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

This test suite serves as an umbrella that includes all specialized
noauto test suites:
- noauto_torch: PyTorch and transformers-based tests
- noauto_tensorflow: TensorFlow-based tests
- noauto_onnx: ONNX Runtime-based tests
- noauto_cython: Cython-compiled package tests
- noauto_network: Network-dependent tests

For targeted testing, use the specific test suites instead of this umbrella.
"""

from unittest import TestLoader, TestSuite

# Names of module to be tested
# Note: These tests are NOT included in automated CI runs
test_packages: list[str] = [
    "tests.noauto_torch",
    "tests.noauto_tensorflow",
    "tests.noauto_onnx",
    "tests.noauto_cython",
    "tests.noauto_network",
]


def load_tests(
    loader: TestLoader, standard_tests: TestSuite, pattern: str
) -> TestSuite:
    """Load test protocol
    See: https://docs.python.org/3/library/unittest.html#id1

    This loads all modular test suites.
    For targeted testing, use specific test suites directly:
    - unittest tests.noauto_torch
    - unittest tests.noauto_tensorflow
    - unittest tests.noauto_onnx
    - unittest tests.noauto_cython
    - unittest tests.noauto_network
    """
    suite = TestSuite()
    for test_package in test_packages:
        tests = loader.loadTestsFromName(test_package)
        suite.addTests(tests)
    return suite


if __name__ == "__main__":
    import unittest

    unittest.main()
