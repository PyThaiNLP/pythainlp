# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest
from os import path

from pythainlp.tag import (
    NER,
    PerceptronTagger,
    perceptron,
    pos_tag,
    pos_tag_sents,
    tag_provinces,
    unigram,
)

TEST_TOKENS = ["ผม", "รัก", "คุณ"]


class TagTestCase(unittest.TestCase):
    """Test pythainlp.tag.pos_tag"""

    def test_pos_tag(self):
        self.assertEqual(pos_tag(None), [])
        self.assertEqual(pos_tag([]), [])
        self.assertEqual(
            pos_tag(["นักเรียน", "ถาม", "ครู"]),
            [("นักเรียน", "NCMN"), ("ถาม", "VACT"), ("ครู", "NCMN")],
        )
        self.assertEqual(
            len(pos_tag(["การ", "เดินทาง", "มี", "ความ", "ท้าทาย"])), 5
        )

        self.assertEqual(unigram.tag(None, corpus="pud"), [])
        self.assertEqual(unigram.tag([], corpus="pud"), [])
        self.assertEqual(unigram.tag(None, corpus="orchid"), [])
        self.assertEqual(unigram.tag([], corpus="orchid"), [])
        self.assertEqual(unigram.tag(None, corpus="blackboard"), [])
        self.assertEqual(unigram.tag([], corpus="blackboard"), [])
        self.assertEqual(unigram.tag(None, corpus="tud"), [])
        self.assertEqual(unigram.tag([], corpus="tud"), [])
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="unigram", corpus="orchid")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="unigram", corpus="orchid_ud")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="unigram", corpus="pud")
        )
        self.assertIsNotNone(pos_tag([""], engine="unigram", corpus="pud"))
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="unigram", corpus="blackboard")
        )
        self.assertIsNotNone(
            pos_tag([""], engine="unigram", corpus="blackboard")
        )
        self.assertIsNotNone(
            pos_tag([""], engine="unigram", corpus="blackboard_ud")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="unigram", corpus="tdtb")
        )
        self.assertIsNotNone(pos_tag([""], engine="unigram", corpus="tdtb"))
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="unigram", corpus="tud")
        )
        self.assertIsNotNone(pos_tag([""], engine="unigram", corpus="tud"))
        self.assertEqual(
            pos_tag(["คุณ", "กำลัง", "ประชุม"], engine="unigram"),
            [("คุณ", "PPRS"), ("กำลัง", "XVBM"), ("ประชุม", "VACT")],
        )

        self.assertTrue(
            pos_tag(["การ", "รัฐประหาร"], corpus="orchid_ud")[0][1], "NOUN"
        )
        self.assertTrue(
            pos_tag(["ความ", "พอเพียง"], corpus="orchid_ud")[0][1], "NOUN"
        )

        self.assertEqual(pos_tag_sents(None), [])
        self.assertEqual(pos_tag_sents([]), [])
        self.assertEqual(
            pos_tag_sents([["ผม", "กิน", "ข้าว"], ["แมว", "วิ่ง"]]),
            [
                [("ผม", "PPRS"), ("กิน", "VACT"), ("ข้าว", "NCMN")],
                [("แมว", "NCMN"), ("วิ่ง", "VACT")],
            ],
        )

    def test_NER_error_handling(self):
        # Test error handling for invalid engine/corpus combination
        with self.assertRaises(ValueError):
            NER(engine="thainer", corpus="cat")



class PerceptronTaggerTestCase(unittest.TestCase):
    """Test pythainlp.tag.PerceptronTagger

    :param unittest: _description_
    :type unittest: _type_
    """

    def test_perceptron_tagger(self):
        self.assertEqual(perceptron.tag(None, corpus="orchid"), [])
        self.assertEqual(perceptron.tag([], corpus="orchid"), [])
        self.assertEqual(perceptron.tag(None, corpus="orchid_ud"), [])
        self.assertEqual(perceptron.tag([], corpus="orchid_ud"), [])
        self.assertEqual(perceptron.tag(None, corpus="pud"), [])
        self.assertEqual(perceptron.tag([], corpus="pud"), [])
        self.assertEqual(perceptron.tag(None, corpus="blackboard"), [])
        self.assertEqual(perceptron.tag([], corpus="blackboard"), [])
        self.assertEqual(perceptron.tag(None, corpus="tud"), [])
        self.assertEqual(perceptron.tag([], corpus="tud"), [])

        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="perceptron", corpus="orchid")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="perceptron", corpus="orchid_ud")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="perceptron", corpus="pud")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="perceptron", corpus="blackboard")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="perceptron", corpus="blackboard_ud")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="perceptron", corpus="tdtb")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="perceptron", corpus="tdtb")
        )
        self.assertIsNotNone(
            pos_tag(TEST_TOKENS, engine="perceptron", corpus="tud")
        )

    def test_perceptron_tagger_custom(self):
        """Test pythainlp.tag.PerceptronTagger"""
        tagger = PerceptronTagger()
        # train data, with "กิน" > 20 instances to trigger conditions
        # in _make_tagdict()
        data = [
            [("คน", "N"), ("เดิน", "V")],
            [("ฉัน", "N"), ("เดิน", "V")],
            [("แมว", "N"), ("เดิน", "V")],
            [("คน", "N"), ("วิ่ง", "V")],
            [("ปลา", "N"), ("ว่าย", "V")],
            [("นก", "N"), ("บิน", "V")],
            [("คน", "N"), ("พูด", "V")],
            [("C-3PO", "N"), ("พูด", "V")],
            [("คน", "N"), ("กิน", "V")],
            [("แมว", "N"), ("กิน", "V")],
            [("นก", "N"), ("กิน", "V")],
            [("นก", "N"), ("นก", "V")],
            [("คน", "N"), ("นก", "V")],
            [("คน", "N"), ("กิน", "V"), ("นก", "N")],
            [("คน", "N"), ("กิน", "V"), ("ปลา", "N")],
            [("นก", "N"), ("กิน", "V"), ("ปลา", "N")],
            [("คน", "N"), ("กิน", "V"), ("กาแฟ", "N")],
            [("คน", "N"), ("คน", "V"), ("กาแฟ", "N")],
            [("พระ", "N"), ("ฉัน", "V"), ("กาแฟ", "N")],
            [("พระ", "N"), ("คน", "V"), ("กาแฟ", "N")],
            [("พระ", "N"), ("ฉัน", "V"), ("ข้าว", "N")],
            [("ฉัน", "N"), ("กิน", "V"), ("ข้าว", "N")],
            [("เธอ", "N"), ("กิน", "V"), ("ปลา", "N")],
            [("ปลา", "N"), ("กิน", "V"), ("แมลง", "N")],
            [("แมวน้ำ", "N"), ("กิน", "V"), ("ปลา", "N")],
            [("หนู", "N"), ("กิน", "V")],
            [("เสือ", "N"), ("กิน", "V")],
            [("ยีราฟ", "N"), ("กิน", "V")],
            [("แรด", "N"), ("กิน", "V")],
            [("หมู", "N"), ("กิน", "V")],
            [("แมลง", "N"), ("กิน", "V")],
            [("สิงโต", "N"), ("กิน", "V")],
            [("เห็บ", "N"), ("กิน", "V")],
            [("เหา", "N"), ("กิน", "V")],
            [("เต่า", "N"), ("กิน", "V")],
            [("กระต่าย", "N"), ("กิน", "V")],
            [("จิ้งจก", "N"), ("กิน", "V")],
            [("หมี", "N"), ("กิน", "V")],
            [("หมา", "N"), ("กิน", "V")],
            [("ตะพาบ", "N"), ("กิน", "V")],
            [("เม่น", "N"), ("กิน", "V")],
            [("หนอน", "N"), ("กิน", "V")],
            [("ปี", "N"), ("2021", "N")],
        ]
        filename = "ptagger_temp4XcDf.json"
        tagger.train(data, save_loc=filename)
        self.assertTrue(path.exists(filename))

        words = ["นก", "เดิน"]
        word_tags = tagger.tag(words)
        self.assertEqual(len(words), len(word_tags))

        words2, _ = zip(*word_tags)
        self.assertEqual(words, list(words2))

        with self.assertRaises(IOError):
            tagger.load("ptagger_notexistX4AcOcX.pkl")  # file does not exist


class TagLocationsTestCase(unittest.TestCase):
    """Test pythainlp.tag.locations"""

    def test_ner_locations(self):
        self.assertEqual(
            tag_provinces(["หนองคาย", "น่าอยู่"]),
            [("หนองคาย", "B-LOCATION"), ("น่าอยู่", "O")],
        )
