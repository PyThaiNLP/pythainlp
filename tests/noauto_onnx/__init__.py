# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Unit test suite for ONNX Runtime-based functionalities.

Test functions that require ONNX Runtime and its ecosystem dependencies:
- onnxruntime
- oskut
- sefr_cut

These tests are NOT run in automated CI workflows due to:
- Large dependencies
- Potential compatibility issues across platforms
- Version constraints

These tests are kept for manual testing and may be run in separate CI
workflows dedicated to ONNX Runtime-based features.
"""

from unittest import TestLoader, TestSuite

# Names of module to be tested
test_packages: list[str] = [
    "tests.noauto_onnx.testn_spell_onnx",
    "tests.noauto_onnx.testn_tag_onnx",
    "tests.noauto_onnx.testn_tokenize_onnx",
    "tests.noauto_onnx.testn_transliterate_onnx",
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
    from unittest import main

    main()
