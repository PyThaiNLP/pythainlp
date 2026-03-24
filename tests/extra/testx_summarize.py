# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.summarize import extract_keywords, summarize

INPUT_TEXT = (
    "อาหาร หมายถึง ของแข็งหรือของเหลว "
    "ที่กินหรือดื่มเข้าสู่ร่างกายแล้ว "
    "จะทำให้เกิดพลังงานและความร้อนแก่ร่างกาย "
    "ทำให้ร่างกายเจริญเติบโต "
    "ซ่อมแซมส่วนที่สึกหรอ ควบคุมการเปลี่ยนแปลงต่างๆ ในร่างกาย "
    "ช่วยทำให้อวัยวะต่างๆ ทำงานได้อย่างปกติ "
    "อาหารจะต้องไม่มีพิษและไม่เกิดโทษต่อร่างกาย"
)


class SummarizeTestCaseX(unittest.TestCase):
    def test_summarize(self):
        self.assertEqual(
            summarize(text=INPUT_TEXT, n=1),
            ["อาหารจะต้องไม่มีพิษและไม่เกิดโทษต่อร่างกาย"],
        )
        # self.assertIsNotNone(summarize(text, engine="mt5-small"))
        # self.assertIsNotNone(summarize([]))
        # self.assertIsNotNone(summarize(text, 1, engine="mt5-small"))
        self.assertIsNotNone(
            summarize(INPUT_TEXT, 1, engine="mt5-cpe-kmutt-thai-sentence-sum")
        )
        self.assertIsNotNone(summarize(INPUT_TEXT, 1, engine="XX"))

    def test_keyword_extraction(self):
        self.assertEqual(extract_keywords(""), [])
        self.assertEqual(extract_keywords("   "), [])

        # test default engine, common case
        keywords = extract_keywords(INPUT_TEXT)
        expected = ["ซ่อมแซมส่วน", "เจริญเติบโต", "อวัยวะต่างๆ", "ควบคุมการเปลี่ยนแปลง"]
        for exp_kw in expected:
            self.assertIn(exp_kw, keywords)

        # test another engine
        for max_kw in (5, 10):
            keywords = extract_keywords(
                INPUT_TEXT, engine="frequency", max_keywords=max_kw
            )
            self.assertEqual(len(keywords), max_kw)

        # test invalid engine
        with self.assertRaises(ValueError):
            extract_keywords(INPUT_TEXT, engine="random engine")

        # test different tokenizer
        keywords = extract_keywords(INPUT_TEXT, tokenizer="attacut")

        expected = ["อวัยวะต่างๆ", "ซ่อมแซมส่วน", "เจริญเติบโต", "เกิดพลังงาน"]
        for exp_kw in expected:
            self.assertIn(exp_kw, keywords)

        # test overriding stop words
        stpw = "เจริญเติบโต"
        keywords = extract_keywords(INPUT_TEXT, stop_words=[stpw])
        self.assertNotIn(stpw, keywords)

    def test_keybert(self):
        from pythainlp.summarize.keybert import KeyBERT
        from pythainlp.tokenize import word_tokenize

        keybert = KeyBERT()
        # test ngram range
        ng_ranges = [(1, 1), (1, 2), (2, 2), (3, 3)]
        for ng_min, ng_max in ng_ranges:
            keywords = keybert.extract_keywords(
                INPUT_TEXT, keyphrase_ngram_range=(ng_min, ng_max)
            )

            for kw in keywords:
                kw_text = kw[0] if isinstance(kw, tuple) else kw
                self.assertTrue(ng_min <= len(word_tokenize(kw_text)) <= ng_max)

        # test max_keywords
        max_kws = 10
        keywords = keybert.extract_keywords(INPUT_TEXT, max_keywords=max_kws)
        self.assertLessEqual(len(keywords), max_kws)

        text_short = "เฮลโหล"
        keywords = keybert.extract_keywords(text_short, max_keywords=max_kws)
        self.assertLessEqual(len(keywords), max_kws)
