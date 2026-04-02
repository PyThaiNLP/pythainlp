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

from tests._noauto_loader import make_load_tests

test_packages: list[str] = [
    "tests.noauto_tensorflow.testn_tokenize_tensorflow",
]

load_tests = make_load_tests(test_packages)

if __name__ == "__main__":
    from unittest import main

    main()
