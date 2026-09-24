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
    attacut,
    oskut,
    sefr_cut,
    word_tokenize,
)

from ..core.test_tokenize import TEXT_1
from ..test_helpers import assert_segment_handles_none_and_empty


class TokenizeDeepcutTestCaseN(unittest.TestCase):
    """Tests for deepcut tokenizer numeric handling (requires onnxruntime)"""

    def test_numeric_data_format_deepcut(self):
        self.assertIn(
            "127.0.0.1",
            word_tokenize("ไอพีของคุณคือ 127.0.0.1 ครับ", engine="deepcut"),
        )

        tokens = word_tokenize("เวลา 12:12pm มีโปรโมชั่น 11.11", engine="deepcut")
        self.assertTrue(
            any(value in tokens for value in ["12:12pm", "12:12"]),
            msg=f"deepcut: {tokens}",
        )
        self.assertIn("11.11", tokens)

        self.assertIn(
            "1,234,567.89",
            word_tokenize("รางวัลมูลค่า 1,234,567.89 บาท", engine="deepcut"),
        )

        tokens = word_tokenize("อัตราส่วน 2.5:1 คือ 5:2", engine="deepcut")
        self.assertIn("2.5:1", tokens)
        self.assertIn("5:2", tokens)


class DetokenizeAttacutTestCaseN(unittest.TestCase):
    """Tests for attacut tokenizer numeric handling (requires lekcut/onnx)"""

    def test_numeric_data_format_attacut(self):
        self.assertIn(
            "127.0.0.1",
            word_tokenize("ไอพีของคุณคือ 127.0.0.1 ครับ", engine="attacut"),
        )

        tokens = word_tokenize("เวลา 12:12pm มีโปรโมชั่น 11.11", engine="attacut")
        self.assertTrue(
            any(value in tokens for value in ["12:12pm", "12:12"]),
            msg=f"attacut: {tokens}",
        )
        self.assertIn("11.11", tokens)

        self.assertIn(
            "1,234,567.89",
            word_tokenize("รางวัลมูลค่า 1,234,567.89 บาท", engine="attacut"),
        )

        tokens = word_tokenize("อัตราส่วน 2.5:1 คือ 5:2", engine="attacut")
        self.assertIn("2.5:1", tokens)
        self.assertIn("5:2", tokens)

        # try turning off `join_broken_num`
        self.assertNotIn(
            "127.0.0.1",
            word_tokenize(
                "ไอพีของคุณคือ 127.0.0.1 ครับ",
                engine="attacut",
                join_broken_num=False,
            ),
        )
        self.assertNotIn(
            "1,234,567.89",
            word_tokenize(
                "รางวัลมูลค่า 1,234,567.89 บาท",
                engine="attacut",
                join_broken_num=False,
            ),
        )


class WordTokenizeAttacutTestCaseN(unittest.TestCase):
    """Tests for attacut tokenizer (requires lekcut/onnx)"""

    def test_word_tokenize_attacut(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="attacut"))

    def test_attacut(self):
        assert_segment_handles_none_and_empty(self, attacut.segment)
        self.assertEqual(
            word_tokenize("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", engine="attacut"),
            ["ฉัน", "รัก", "ภาษา", "ไทย", "เพราะ", "ฉัน", "เป็น", "คน", "ไทย"],
        )
        self.assertEqual(
            attacut.segment("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", model="attacut-sc"),
            ["ฉัน", "รัก", "ภาษา", "ไทย", "เพราะ", "ฉัน", "เป็น", "คน", "ไทย"],
        )
        self.assertIsNotNone(
            attacut.segment("ฉันรักภาษาไทยเพราะฉันเป็นคนไทย", model="attacut-c")
        )

    def test_attacut_tokenizer_class(self):
        tok = attacut.AttacutTokenizer(model="attacut-sc")
        self.assertEqual(tok.tokenize(""), [])
        self.assertIsNotNone(tok.tokenize("ฉันรักภาษาไทย"))
        tok_c = attacut.AttacutTokenizer(model="attacut-c")
        self.assertIsNotNone(tok_c.tokenize("ฉันรักภาษาไทย"))


class DetokenizeOskutTestCaseN(unittest.TestCase):
    """Tests for oskut tokenizer numeric handling (requires lekcut/onnx)"""

    def test_numeric_data_format_oskut(self):
        self.assertIn(
            "127.0.0.1",
            word_tokenize("ไอพีของคุณคือ 127.0.0.1 ครับ", engine="oskut"),
        )

        tokens = word_tokenize("เวลา 12:12pm มีโปรโมชั่น 11.11", engine="oskut")
        self.assertTrue(
            any(value in tokens for value in ["12:12pm", "12:12"]),
            msg=f"oskut: {tokens}",
        )
        self.assertIn("11.11", tokens)

        self.assertIn(
            "1,234,567.89",
            word_tokenize("รางวัลมูลค่า 1,234,567.89 บาท", engine="oskut"),
        )

        tokens = word_tokenize("อัตราส่วน 2.5:1 คือ 5:2", engine="oskut")
        self.assertIn("2.5:1", tokens)
        self.assertIn("5:2", tokens)


class WordTokenizeOskutTestCaseN(unittest.TestCase):
    """Tests for oskut tokenizer (requires lekcut/onnx)"""

    def test_word_tokenize_oskut(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="oskut"))

    def test_oskut(self):
        assert_segment_handles_none_and_empty(self, oskut.segment)
        self.assertEqual(
            word_tokenize("เบียร์ยูไม่อร่อย", engine="oskut"),
            ["เบียร์", "ยู", "ไม่", "อ", "ร่อย"],
        )
        self.assertEqual(
            oskut.segment("เบียร์ยูไม่อร่อย", engine="ws"),
            ["เบียร์", "ยู", "ไม่", "อ", "ร่อย"],
        )
        self.assertEqual(
            oskut.segment("เบียร์ยูไม่อร่อย", engine="tnhc"),
            ["เบียร์", "ยู", "ไม่", "อร่อย"],
        )


class DetokenizeSefrCutTestCaseN(unittest.TestCase):
    """Tests for sefr_cut tokenizer numeric handling (requires lekcut/onnx)"""

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


class WordTokenizeSefrCutTestCaseN(unittest.TestCase):
    """Tests for sefr_cut tokenizer (requires lekcut/onnx)"""

    def test_word_tokenize_sefr_cut(self):
        self.assertIsNotNone(word_tokenize(TEXT_1, engine="sefr_cut"))

    def test_sefr_cut(self):
        assert_segment_handles_none_and_empty(self, sefr_cut.segment)
        self.assertEqual(
            word_tokenize("เบียร์ยูไม่อร่อย", engine="sefr_cut"),
            ["เบียร์", "ยู", "ไม่", "อร่อย"],
        )
        self.assertEqual(
            sefr_cut.segment("เบียร์ยูไม่อร่อย", engine="ws1000"),
            ["เบียร์", "ยู", "ไม่", "อร่อย"],
        )
        self.assertEqual(
            sefr_cut.segment("เบียร์ยูไม่อร่อย", engine="tnhc"),
            ["เบียร์", "ยู", "ไม่", "อร่อย"],
        )
        self.assertEqual(
            sefr_cut.segment("เบียร์ยูไม่อร่อย", engine="best"),
            ["เบียร์", "ยูไม่", "อร่อย"],
        )
