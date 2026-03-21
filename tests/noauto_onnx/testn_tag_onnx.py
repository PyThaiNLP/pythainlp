# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for POS tagging functions that require ONNX Runtime
# These tests are NOT run in automated CI workflows due to:
# - Large dependencies (onnxruntime)
# - Platform-specific compatibility issues
# - Version constraints

import unittest


class TagONNXTestCaseN(unittest.TestCase):
    """Tests for ONNX-based POS tagging (requires onnxruntime)"""

    def test_pos_tag_wangchanberta_onnx_returns_list(self):
        from pythainlp.tag import pos_tag

        result = pos_tag(
            ["แมว", "กิน", "ปลา"],
            engine="wangchanberta_onnx",
        )
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_pos_tag_wangchanberta_onnx_length_matches(self):
        from pythainlp.tag import pos_tag

        tokens = ["แมว", "กิน", "ปลา"]
        result = pos_tag(tokens, engine="wangchanberta_onnx")
        self.assertEqual(len(result), len(tokens))

    def test_pos_tag_wangchanberta_onnx_tuple_pairs(self):
        from pythainlp.tag import pos_tag

        result = pos_tag(
            ["แมว", "กิน", "ปลา"],
            engine="wangchanberta_onnx",
        )
        for item in result:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)
            word, tag = item
            self.assertIsInstance(word, str)
            self.assertIsInstance(tag, str)

    def test_pos_tag_wangchanberta_onnx_empty_list(self):
        from pythainlp.tag import pos_tag

        result = pos_tag([], engine="wangchanberta_onnx")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
