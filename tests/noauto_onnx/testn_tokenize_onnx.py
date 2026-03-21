# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for tokenize functions that require ONNX Runtime
# These tests are NOT run in automated CI workflows due to:
# - Large dependencies (onnxruntime)
# - Platform-specific compatibility issues
# - Version constraints

import unittest

from pythainlp.tokenize import (
    oskut,
    sefr_cut,
    word_tokenize,
)

from ..core.test_tokenize import TEXT_1
from ..test_helpers import assert_segment_handles_none_and_empty


class DetokenizeSEFRCutTestCaseN(unittest.TestCase):
    """Tests for sefr_cut tokenizer numeric handling (requires onnxruntime)"""

    def test_numeric_data_format_sefr_cut(self):
        self.assertIn(
            "127.0.0.1",
            word_tokenize("ไอพีของคุณคือ 127.0.0.1 ครับ", engine="sefr_cut"),
        )

        tokens = word_tokenize(
            "เวลา 12:12pm มีโปรโมชั่น 11.11", engine="sefr_cut"
        )
        self.assertTrue(
            any(value in tokens for value in ["12:12pm", "12:12"]),
            msg=f"sefr_cut: {tokens}",
        )
        self.assertIn("11.11", tokens)

        self.assertIn(
            "1,234,567.89",
            word_tokenize("รางวัลมูลค่า 1,234,567.89 บาท", engine="sefr_cut"),
        )

        tokens = word_tokenize("อัตราส่วน 2.5:1 คือ 5:2", engine="sefr_cut")
        self.assertIn("2.5:1", tokens)
        self.assertIn("5:2", tokens)


class WordTokenizeOSKutTestCaseN(unittest.TestCase):
    """Tests for oskut tokenizer (requires onnxruntime)"""

    def test_word_tokenize_oskut(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="oskut"))

    def test_oskut(self):
        assert_segment_handles_none_and_empty(self, oskut.segment)
        self.assertIsNotNone(
            oskut.segment("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย"),
        )
        self.assertIsNotNone(
            oskut.segment("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="scads"),
        )


class WordTokenizeSEFRCutTestCaseN(unittest.TestCase):
    """Tests for sefr_cut tokenizer (requires onnxruntime)"""

    def test_word_tokenize_sefr_cut(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="sefr_cut"))

    def test_sefr_cut(self):
        assert_segment_handles_none_and_empty(self, sefr_cut.segment)
        self.assertIsNotNone(
            sefr_cut.segment("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย"),
        )
        self.assertIsNotNone(
            sefr_cut.segment("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="tnhc"),
        )

