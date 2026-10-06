# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for POS tagging functions that require ONNX Runtime
# These tests are NOT run in automated CI workflows due to:
# - Large dependencies (onnxruntime, tokenizers, huggingface-hub)
# - Platform-specific compatibility issues
# - Version constraints

import unittest


class TagONNXTestCaseN(unittest.TestCase):
    """Tests for ONNX-based POS tagging (requires onnxruntime)."""

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


class TagPhayaThaiBERTONNXTestCaseN(unittest.TestCase):
    """Tests for the PhayaThaiBERT ONNX POS tagger
    (requires onnxruntime, tokenizers, huggingface-hub)"""

    WORDS = ["ฉัน", "กิน", "ข้าว", "ที่", "ร้านอาหาร"]

    def test_pos_tag_phayathaibert(self):
        from pythainlp.tag import pos_tag

        self.assertEqual(
            pos_tag(self.WORDS, engine="phayathaibert"),
            [
                ("ฉัน", "PRON"),
                ("กิน", "VERB"),
                ("ข้าว", "NOUN"),
                ("ที่", "ADP"),
                ("ร้านอาหาร", "NOUN"),
            ],
        )

    def test_pos_tag_phayathaibert_ignores_corpus(self):
        from pythainlp.tag import pos_tag

        self.assertEqual(
            pos_tag(self.WORDS, engine="phayathaibert", corpus="orchid"),
            pos_tag(self.WORDS, engine="phayathaibert", corpus="tud"),
        )

    def test_pos_tag_phayathaibert_whitespace_words(self):
        from pythainlp.tag import pos_tag

        result = pos_tag(["แมว", " ", "กิน", ""], engine="phayathaibert")
        self.assertEqual(len(result), 4)
        self.assertEqual(result[1], (" ", "PUNCT"))
        self.assertEqual(result[3], ("", "PUNCT"))
        self.assertEqual(
            [result[0], result[2]],
            pos_tag(["แมว", "กิน"], engine="phayathaibert"),
        )

    def test_pos_tag_phayathaibert_long_input(self):
        from pythainlp.tag import pos_tag

        words = self.WORDS * 300  # well over the 510-token model limit
        result = pos_tag(words, engine="phayathaibert")
        tags = [t for _, t in result]
        self.assertEqual([w for w, _ in result], words)
        # Every word, including those past the first 510 tokens, is tagged.
        self.assertNotIn("X", tags)
        self.assertEqual(tags[-5:], ["PRON", "VERB", "NOUN", "ADP", "NOUN"])

    def test_pos_tag_phayathaibert_overlong_word(self):
        from pythainlp.tag import pos_tag

        # A single word of far more than 510 subwords, between normal words.
        words = ["ฉัน", "กิน", "ก" * 5000, "ที่", "ร้านอาหาร"]
        result = pos_tag(words, engine="phayathaibert")
        tags = [t for _, t in result]
        self.assertEqual(len(result), 5)
        self.assertNotIn("X", tags)
        self.assertEqual(tags[:2], ["PRON", "VERB"])
        self.assertEqual(tags[3:], ["ADP", "NOUN"])

    def test_pos_tag_phayathaibert_format_characters(self):
        from pythainlp.tag import pos_tag

        # Zero-width space, zero-width non-joiner and BOM carry no text.
        for char in ("​", "‌", "﻿"):
            result = pos_tag(["แมว", char, "กิน"], engine="phayathaibert")
            self.assertEqual(result[1], (char, "PUNCT"))

    def test_pos_tag_sents_phayathaibert(self):
        from pythainlp.tag import pos_tag_sents

        result = pos_tag_sents(
            [self.WORDS, ["แมว", "กิน", "ปลา"]], engine="phayathaibert"
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[1]), 3)
