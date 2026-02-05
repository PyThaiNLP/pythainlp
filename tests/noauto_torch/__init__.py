# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Unit test suite for PyTorch-based functionalities.

Test functions that require PyTorch and its ecosystem dependencies:
- torch
- transformers (when using PyTorch backend)
- sentence-transformers
- attacut
- thai_nner
- wtpsplit

These tests are NOT run in automated CI workflows due to:
- Very large dependencies (~2-3 GB for torch)
- Potential version conflicts with other frameworks
- Long installation time

These tests are kept for manual testing and may be run in separate CI
workflows dedicated to PyTorch-based features.
"""

from unittest import TestLoader, TestSuite

# Names of module to be tested
test_packages: list[str] = [
    "tests.noauto_torch.testn_spell_torch",
    "tests.noauto_torch.testn_tag_torch",
    "tests.noauto_torch.testn_tokenize_torch",
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
