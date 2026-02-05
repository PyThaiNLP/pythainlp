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
- noauto-torch: PyTorch and transformers-based tests
- noauto-tensorflow: TensorFlow-based tests
- noauto-onnx: ONNX Runtime-based tests
- noauto-cython: Cython-compiled package tests
- noauto-network: Network-dependent tests

For targeted testing, use the specific test suites instead of this umbrella.
"""

from unittest import TestLoader, TestSuite

# Names of module to be tested
# Note: These tests are NOT included in automated CI runs
# Legacy test files (deprecated, kept for backward compatibility)
test_packages: list[str] = [
    "tests.noauto.testn_spell",
    "tests.noauto.testn_tag",
    "tests.noauto.testn_tokenize",
]

# New modular test suites by dependency group
modular_test_packages: list[str] = [
    "tests.noauto-torch",
    "tests.noauto-tensorflow",
    "tests.noauto-onnx",
    "tests.noauto-cython",
    "tests.noauto-network",
]


def load_tests(
    loader: TestLoader, standard_tests: TestSuite, pattern: str
) -> TestSuite:
    """Load test protocol
    See: https://docs.python.org/3/library/unittest.html#id1

    This loads both legacy and new modular test suites.
    For targeted testing, use specific test suites directly:
    - unittest tests.noauto-torch
    - unittest tests.noauto-tensorflow
    - unittest tests.noauto-onnx
    - unittest tests.noauto-cython
    - unittest tests.noauto-network
    """
    suite = TestSuite()

    # Load legacy test files (for backward compatibility)
    for test_package in test_packages:
        tests = loader.loadTestsFromName(test_package)
        suite.addTests(tests)

    # Load new modular test suites
    for test_package in modular_test_packages:
        tests = loader.loadTestsFromName(test_package)
        suite.addTests(tests)

    return suite


if __name__ == "__main__":
    import unittest

    unittest.main()
