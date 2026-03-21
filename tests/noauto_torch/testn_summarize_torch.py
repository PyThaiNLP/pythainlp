# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for summarization functions that require transformers
# These tests are NOT run in automated CI workflows due to:
# - Large dependencies (torch, transformers)
# - Python 3.13+ compatibility issues

import unittest


class SummarizeTestCaseN(unittest.TestCase):
    """Tests for summarization functions (requires transformers)"""

    def test_summarize_keybert_returns_list(self):
        from pythainlp.summarize.keybert import KeyBERT

        text = "แมวเป็นสัตว์เลี้ยงที่น่ารัก แมวชอบกินปลา แมวชอบนอนหลับ"
        keybert = KeyBERT()
        result = keybert.extract_keywords(text, max_keywords=2)
        self.assertIsInstance(result, list)

    def test_summarize_keybert_max_keywords_respected(self):
        from pythainlp.summarize.keybert import KeyBERT

        text = "แมวเป็นสัตว์เลี้ยงที่น่ารัก แมวชอบกินปลา แมวชอบนอนหลับ"
        keybert = KeyBERT()
        result = keybert.extract_keywords(text, max_keywords=2)
        self.assertLessEqual(len(result), 2)

    def test_summarize_mt5_returns_list(self):
        from pythainlp.summarize.mt5 import mT5Summarizer

        text = "แมวเป็นสัตว์เลี้ยงที่น่ารัก แมวชอบกินปลา แมวชอบนอนหลับ"
        summarizer = mT5Summarizer()
        result = summarizer.summarize(text)
        self.assertIsInstance(result, list)

    def test_summarize_mt5_result_items_are_strings(self):
        from pythainlp.summarize.mt5 import mT5Summarizer

        text = "แมวเป็นสัตว์เลี้ยงที่น่ารัก แมวชอบกินปลา แมวชอบนอนหลับ"
        summarizer = mT5Summarizer()
        result = summarizer.summarize(text)
        for item in result:
            self.assertIsInstance(item, str)
