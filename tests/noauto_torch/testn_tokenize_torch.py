# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for tokenize functions that require torch and transformers
# These tests are NOT run in automated CI workflows due to:
# - Large dependencies (torch, transformers)
# - Python 3.13+ compatibility issues

import unittest

from pythainlp.tokenize import (
    paragraph_tokenize,
    sent_tokenize,
)

from ..core.test_tokenize import (
    SENT_3,
)
from ..test_helpers import (
    assert_subword_tokenize_basic,
)


class ParagraphTokenizeTestCaseN(unittest.TestCase):
    """Tests for paragraph tokenization (requires transformers)"""

    def test_paragraph_tokenize(self):
        sent = (
            "(1) บทความนี้ผู้เขียนสังเคราะห์ขึ้นมา"
            "จากผลงานวิจัยที่เคยทำมาในอดีต"
            " มิได้ทำการศึกษาค้นคว้าใหม่อย่างกว้างขวางแต่อย่างใด"
            " จึงใคร่ขออภัยในความบกพร่องทั้งปวงมา ณ ที่นี้"
        )
        self.assertIsNotNone(paragraph_tokenize(sent))
        with self.assertRaises(ValueError):
            paragraph_tokenize(
                sent, engine="ai2+2thai"
            )  # engine does not exist


class SentTokenizeWTPTestCaseN(unittest.TestCase):
    """Tests for WTP sentence tokenizer (requires transformers and torch)"""

    def test_sent_tokenize_wtp(self):
        self.assertIsNotNone(
            sent_tokenize(
                SENT_3,
                engine="wtp",
            ),
        )

    def test_sent_tokenize_wtp_tiny(self):
        self.assertIsNotNone(
            sent_tokenize(
                SENT_3,
                engine="wtp-tiny",
            ),
        )


class SubwordTokenizePhayathaiTestCaseN(unittest.TestCase):
    """Tests for phayathai subword tokenizer (requires transformers)"""

    def test_subword_tokenize_phayathai(self):
        assert_subword_tokenize_basic(self, "phayathai")


class SubwordTokenizeWangchanbertaTestCaseN(unittest.TestCase):
    """Tests for wangchanberta subword tokenizer (requires transformers)"""

    def test_subword_tokenize_wangchanberta(self):
        assert_subword_tokenize_basic(self, "wangchanberta")
