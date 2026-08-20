# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Unit test suite for TensorFlow-based functionalities.

Test functions that require TensorFlow and its ecosystem dependencies:
- tensorflow
- keras

These tests are NOT run in automated CI workflows due to:
- Very large dependencies (~1-2 GB for tensorflow)
- Potential version conflicts with PyTorch
- Long installation time

These tests are kept for manual testing and may be run in separate CI
workflows dedicated to TensorFlow-based features.

NOTE: deepcut tokenizer was migrated to ONNX; its tests are now in
tests/noauto_onnx/.
"""

from tests._noauto_loader import make_load_tests

# Names of module to be tested
test_packages: list[str] = []

load_tests = make_load_tests(test_packages)

if __name__ == "__main__":
    from unittest import main

    main()
