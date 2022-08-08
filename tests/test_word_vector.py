# -*- coding: utf-8 -*-

import unittest

from pythainlp.word_vector import WordVector


class TestWordVectorPackage(unittest.TestCase):
    def test_thai2vec(self):
        _wv = WordVector("thai2fit_wv")
        self.assertGreaterEqual(
            _wv.similarity("แบคทีเรีย", "คน"), 0
        )
        self.assertIsNotNone(_wv.sentence_vectorizer(""))
        self.assertIsNotNone(_wv.get_model())
        self.assertIsNotNone(
            _wv.sentence_vectorizer("เสรีภาพในการชุมนุม")
        )
        self.assertIsNotNone(
            _wv.sentence_vectorizer(
                "เสรีภาพในการรวมตัว\nสมาคม", use_mean=True
            )
        )
        self.assertIsNotNone(
            _wv.sentence_vectorizer("I คิด therefore I am ผ็ฎ์")
        )
        self.assertIsNotNone(
            _wv.most_similar_cosmul(
                ["สหรัฐอเมริกา", "ประธานาธิบดี"], ["ประเทศไทย"]
            )[0][0]
        )
        self.assertEqual(
            _wv.doesnt_match(["ญี่ปุ่น", "พม่า", "ไอติม"]), "ไอติม"
        )

    def test_ltw2v(self):
        _wv = WordVector("ltw2v")
        self.assertGreaterEqual(
            _wv.similarity("แบคทีเรีย", "คน"), 0
        )
        self.assertIsNotNone(_wv.sentence_vectorizer(""))
        self.assertIsNotNone(_wv.get_model())
        self.assertIsNotNone(
            _wv.sentence_vectorizer("เสรีภาพในการชุมนุม")
        )
        self.assertIsNotNone(
            _wv.sentence_vectorizer(
                "เสรีภาพในการรวมตัว\nสมาคม", use_mean=True
            )
        )
        self.assertIsNotNone(
            _wv.sentence_vectorizer("I คิด therefore I am ผ็ฎ์")
        )
        self.assertIsNotNone(
            _wv.most_similar_cosmul(
                ["สหรัฐอเมริกา", "ประธานาธิบดี"], ["ไทย"]
            )[0][0]
        )
        self.assertEqual(
            _wv.doesnt_match(["ญี่ปุ่น", "พม่า", "ไอติม"]), "ไอติม"
        )
