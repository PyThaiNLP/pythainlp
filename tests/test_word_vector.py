# -*- coding: utf-8 -*-

import unittest

from pythainlp import word_vector


class TestWordVectorPackage(unittest.TestCase):
    def test_thai2vec(self):
        self.assertGreaterEqual(word_vector.similarity("แบคทีเรีย", "คน"), 0)
        self.assertIsNotNone(word_vector.sentence_vectorizer(""))
        self.assertIsNotNone(
            word_vector.sentence_vectorizer("เสรีภาพในการชุมนุม")
        )
        self.assertIsNotNone(
            word_vector.sentence_vectorizer(
                "เสรีภาพในการรวมตัว\nสมาคม", use_mean=True
            )
        )
        self.assertIsNotNone(
            word_vector.sentence_vectorizer("I คิด therefore I am ผ็ฎ์")
        )
        self.assertIsNotNone(
            word_vector.most_similar_cosmul(
                ["สหรัฐอเมริกา", "ประธานาธิบดี"], ["ประเทศไทย"]
            )[0][0]
        )
        self.assertEqual(
            word_vector.doesnt_match(["ญี่ปุ่น", "พม่า", "ไอติม"]), "ไอติม"
        )
