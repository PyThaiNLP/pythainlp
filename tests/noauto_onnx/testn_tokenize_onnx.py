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
    deepcut,
    word_tokenize,
)

from ..core.test_tokenize import TEXT_1
from ..test_helpers import assert_segment_handles_none_and_empty


class tokenizeDeepcutTestCaseN(unittest.TestCase):
    """Tests for deepcut tokenizer numeric handling (requires onnxruntime)"""

    def test_numeric_data_format_deepcut(self):
        self.assertIn(
            "127.0.0.1",
            word_tokenize("ไอพีของคุณคือ 127.0.0.1 ครับ", engine="deepcut"),
        )

        tokens = word_tokenize(
            "เวลา 12:12pm มีโปรโมชั่น 11.11", engine="deepcut"
        )
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
