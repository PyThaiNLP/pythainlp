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

from tests._noauto_loader import make_load_tests

test_packages: list[str] = [
    "tests.noauto_onnx.testn_spell_onnx",
    "tests.noauto_onnx.testn_tag_onnx",
    "tests.noauto_onnx.testn_tokenize_onnx",
    "tests.noauto_onnx.testn_transliterate_onnx",
]

load_tests = make_load_tests(test_packages)

if __name__ == "__main__":
    from unittest import main

    main()
