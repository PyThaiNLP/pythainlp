# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for transliteration functions that require ONNX Runtime
# These tests are NOT run in automated CI workflows due to:
# - Large dependencies (onnxruntime)
# - Platform-specific compatibility issues
# - Version constraints

import unittest


class TransliterateONNXTestCaseN(unittest.TestCase):
    """Tests for ONNX-based transliteration (requires onnxruntime)"""

    def test_thai2rom_onnx_returns_string(self):
        from pythainlp.transliterate.thai2rom_onnx import romanize

        result = romanize("สวัสดี")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_thai2rom_onnx_empty_string(self):
        from pythainlp.transliterate.thai2rom_onnx import romanize

        result = romanize("")
        self.assertIsInstance(result, str)

    def test_thai2rom_onnx_ascii_passthrough(self):
        from pythainlp.transliterate.thai2rom_onnx import romanize

        result = romanize("hello")
        self.assertIsInstance(result, str)

    def test_thai2rom_onnx_mixed_text(self):
        from pythainlp.transliterate.thai2rom_onnx import romanize

        result = romanize("ภาษาไทย")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
