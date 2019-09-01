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

        # arguement `tag` is True
        self.assertEqual(
            ner.get_ner(
                "วันที่ 15 ก.ย. 61 ทดสอบระบบเวลา 14:49 น.",
                tag=True
            ),
            "วันที่ <DATE>15 ก.ย. 61</DATE> "
            "ทดสอบระบบเวลา <TIME>14:49 น.</TIME>")

        self.assertEqual(
            ner.get_ner(
                "url = https://thainlp.org/pythainlp/docs/2.0/",
                tag=True
            ),
            "url = <URL>https://thainlp.org/pythainlp/docs/2.0/</URL>")

        self.assertEqual(
            ner.get_ner(
                "example@gmail.com",
                tag=True
            ),
            "<EMAIL>example@gmail.com</EMAIL>")

        self.assertEqual(
            ner.get_ner(
                "รหัสไปรษณีย์ 19130",
                tag=True
            ),
            "รหัสไปรษณีย์ <ZIP>19130</ZIP>")

        self.assertEqual(
            ner.get_ner(
                "เบอร์โทรศัพท์ 091-123-4567",
                tag=True
            ),
            "เบอร์โทรศัพท์ <PHONE>091-123-4567</PHONE>")

        self.assertEqual(
            ner.get_ner(
                "อาจารย์เอกพล ประจำคณะวิศวกรรมศาสตร์ ",
                tag=True
            ),
            "<PERSON>อาจารย์เอกพล</PERSON> ประจำ<ORGANIZATION>"
            "คณะวิศวกรรมศาสตร์</ORGANIZATION> ")

        self.assertEqual(
            ner.get_ner(
                "มาตรา 80 ปพพ ให้ใช้อัตราภาษีร้อยละ 10.0"
                " ในการคำนวณภาษีมูลค่าเพิ่ม",
                tag=True
            ),
            "<LAW>มาตรา 80 ปพพ</LAW> "
            "ให้ใช้อัตราภาษี<PERCENT>ร้อยละ 10.0</PERCENT>"
            " ในการคำนวณภาษีมูลค่าเพิ่ม")

        self.assertEqual(
            ner.get_ner(
                "ยาว 20 เซนติเมตร",
                tag=True
            ),
            "ยาว <LEN>20 เซนติเมตร</LEN>")

        self.assertEqual(
            ner.get_ner(
                "1 บาท",
                pos=True,
                tag=True),
            "<MONEY>1 บาท</MONEY>")

        self.assertEqual(
            ner.get_ner(
                "ไทย",
                pos=False,
                tag=True
            ),
            "<LOCATION>ไทย</LOCATION>")

        # arguement `tag` is False and `pos` is True
        self.assertEqual(
            ner.get_ner(
                "ไทย",
                pos=True,
                tag=False
            ),
            [('ไทย', 'PROPN', 'B-LOCATION')])

        # arguement `tag` is False and `pos` is False
        self.assertEqual(
            ner.get_ner(
                "วันที่ 15 ก.ย. 61 ทดสอบระบบเวลา 14:49 น.",
                pos=False,
                tag=False
            ),
            [('วันที่', 'O'), (' ', 'O'), ('15', 'B-DATE'),
             (' ', 'I-DATE'), ('ก.ย.', 'I-DATE'), (' ', 'I-DATE'),
             ('61', 'I-DATE'), (' ', 'O'), ('ทดสอบ', 'O'), ('ระบบ', 'O'),
             ('เวลา', 'O'), (' ', 'O'), ('14', 'B-TIME'), (':', 'I-TIME'),
             ('49', 'I-TIME'), (' ', 'I-TIME'), ('น.', 'I-TIME')])

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
