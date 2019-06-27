# -*- coding: utf-8 -*-

import datetime
import os
import sys
import unittest

from pythainlp.tag import perceptron, pos_tag, pos_tag_sents, unigram
from pythainlp.tag.locations import tag_provinces
from pythainlp.tag.named_entity import ThaiNameTagger
from pythainlp.tokenize import (
    word_tokenize,
)


class TestTagPackage(unittest.TestCase):

    def test_pos_tag(self):
        tokens = ["ผม", "รัก", "คุณ"]

        self.assertEqual(pos_tag(None), [])
        self.assertEqual(pos_tag([]), [])

        self.assertEqual(unigram.tag(None, corpus="pud"), [])
        self.assertEqual(unigram.tag([], corpus="pud"), [])
        self.assertEqual(unigram.tag(None, corpus="orchid"), [])
        self.assertEqual(unigram.tag([], corpus="orchid"), [])

        self.assertIsNotNone(
            pos_tag(tokens, engine="unigram", corpus="orchid")
        )
        self.assertIsNotNone(pos_tag(tokens, engine="unigram", corpus="pud"))
        self.assertIsNotNone(pos_tag([""], engine="unigram", corpus="pud"))
        self.assertEqual(
            pos_tag(word_tokenize("คุณกำลังประชุม"), engine="unigram"),
            [("คุณ", "PPRS"), ("กำลัง", "XVBM"), ("ประชุม", "VACT")],
        )

        self.assertIsNotNone(
            pos_tag(tokens, engine="perceptron", corpus="orchid")
        )
        self.assertIsNotNone(
            pos_tag(tokens, engine="perceptron", corpus="pud")
        )
        self.assertEqual(perceptron.tag(None, corpus="pud"), [])
        self.assertEqual(perceptron.tag([], corpus="pud"), [])
        self.assertEqual(perceptron.tag(None, corpus="orchid"), [])
        self.assertEqual(perceptron.tag([], corpus="orchid"), [])

        self.assertIsNotNone(pos_tag(None, engine="artagger"))
        self.assertIsNotNone(pos_tag([], engine="artagger"))
        self.assertIsNotNone(pos_tag(tokens, engine="artagger"))
        self.assertEqual(
            pos_tag(word_tokenize("คุณกำลังประชุม"), engine="artagger"),
            [("คุณ", "PPRS"), ("กำลัง", "XVBM"), ("ประชุม", "VACT")],
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

    # ### pythainlp.tag.locations

    def test_ner_locations(self):
        self.assertEqual(
            tag_provinces(["หนองคาย", "น่าอยู่"]),
            [("หนองคาย", "B-LOCATION"), ("น่าอยู่", "O")],
        )

    # ### pythainlp.tag.named_entity

    def test_ner(self):
        ner = ThaiNameTagger()
        self.assertEqual(ner.get_ner(""), [])
        self.assertIsNotNone(ner.get_ner("แมวทำอะไรตอนห้าโมงเช้า"))
        self.assertIsNotNone(ner.get_ner("แมวทำอะไรตอนห้าโมงเช้า", pos=False))
        self.assertIsNotNone(
            ner.get_ner(
                """คณะวิทยาศาสตร์ประยุกต์และวิศวกรรมศาสตร์ มหาวิทยาลัยขอนแก่น
                วิทยาเขตหนองคาย 112 หมู่ 7 บ้านหนองเดิ่น ตำบลหนองกอมเกาะ อำเภอเมือง
                จังหวัดหนองคาย 43000"""
            )
        )
        # self.assertEqual(
        #     ner.get_ner("แมวทำอะไรตอนห้าโมงเช้า"),
        #     [
        #         ("แมว", "NCMN", "O"),
        #         ("ทำ", "VACT", "O"),
        #         ("อะไร", "PNTR", "O"),
        #         ("ตอน", "NCMN", "O"),
        #         ("ห้า", "VSTA", "B-TIME"),
        #         ("โมง", "NCMN", "I-TIME"),
        #         ("เช้า", "ADVN", "I-TIME"),
        #     ],
        # )
        # self.assertEqual(
        #     ner.get_ner("แมวทำอะไรตอนห้าโมงเช้า", pos=False),
        #     [
        #         ("แมว", "O"),
        #         ("ทำ", "O"),
        #         ("อะไร", "O"),
        #         ("ตอน", "O"),
        #         ("ห้า", "B-TIME"),
        #         ("โมง", "I-TIME"),
        #         ("เช้า", "I-TIME"),
        #     ],
        # )
