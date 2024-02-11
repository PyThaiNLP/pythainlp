# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

import unittest
from os import path

from pythainlp.tag import (
    NER,
    NNER,
    PerceptronTagger,
    chunk_parse,
    perceptron,
    pos_tag,
    pos_tag_sents,
    pos_tag_transformers,
    tag_provinces,
    tltk,
    unigram,
)
from pythainlp.tag.thainer import ThaiNameTagger


class TestTagPackage(unittest.TestCase):
    # ### pythainlp.tag.PerceptronTagger

    def test_chunk_parse(self):
        tokens = ["ผม", "รัก", "คุณ"]

        w_p = pos_tag(tokens, engine="perceptron", corpus="orchid")
        self.assertIsNotNone(chunk_parse(w_p))

    # ### pythainlp.tag.pos_tag

    def test_pos_tag(self):
        tokens = ["ผม", "รัก", "คุณ"]

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
        self.assertIsNotNone(
            pos_tag(tokens, engine="unigram", corpus="orchid")
        )
        self.assertIsNotNone(
            pos_tag(tokens, engine="unigram", corpus="orchid_ud")
        )
        self.assertIsNotNone(pos_tag(tokens, engine="unigram", corpus="pud"))
        self.assertIsNotNone(pos_tag([""], engine="unigram", corpus="pud"))
        self.assertIsNotNone(
            pos_tag(tokens, engine="unigram", corpus="blackboard")
        )
        self.assertIsNotNone(
            pos_tag([""], engine="unigram", corpus="blackboard")
        )
        self.assertIsNotNone(
            pos_tag([""], engine="unigram", corpus="blackboard_ud")
        )
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

        self.assertEqual(perceptron.tag(None, corpus="orchid"), [])
        self.assertEqual(perceptron.tag([], corpus="orchid"), [])
        self.assertEqual(perceptron.tag(None, corpus="orchid_ud"), [])
        self.assertEqual(perceptron.tag([], corpus="orchid_ud"), [])
        self.assertEqual(perceptron.tag(None, corpus="pud"), [])
        self.assertEqual(perceptron.tag([], corpus="pud"), [])
        self.assertEqual(perceptron.tag(None, corpus="blackboard"), [])
        self.assertEqual(perceptron.tag([], corpus="blackboard"), [])
        self.assertIsNotNone(
            pos_tag(tokens, engine="perceptron", corpus="orchid")
        )
        self.assertIsNotNone(
            pos_tag(tokens, engine="perceptron", corpus="orchid_ud")
        )
        self.assertIsNotNone(
            pos_tag(tokens, engine="perceptron", corpus="pud")
        )
        self.assertIsNotNone(
            pos_tag(tokens, engine="perceptron", corpus="blackboard")
        )
        self.assertIsNotNone(
            pos_tag(tokens, engine="perceptron", corpus="blackboard_ud")
        )
        self.assertIsNotNone(pos_tag(tokens, engine="tltk"))

        self.assertEqual(pos_tag_sents(None), [])
        self.assertEqual(pos_tag_sents([]), [])
        self.assertEqual(
            pos_tag_sents([["ผม", "กิน", "ข้าว"], ["แมว", "วิ่ง"]]),
            [
                [("ผม", "PPRS"), ("กิน", "VACT"), ("ข้าว", "NCMN")],
                [("แมว", "NCMN"), ("วิ่ง", "VACT")],
            ],
        )
        with self.assertRaises(ValueError):
            self.assertIsNotNone(tltk.pos_tag(tokens, corpus="blackboard"))

    # ### pythainlp.tag.PerceptronTagger

    def test_perceptron_tagger(self):
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

    # ### pythainlp.tag.locations

    def test_ner_locations(self):
        self.assertEqual(
            tag_provinces(["หนองคาย", "น่าอยู่"]),
            [("หนองคาย", "B-LOCATION"), ("น่าอยู่", "O")],
        )

    # ### pythainlp.tag.named_entity

    def test_ner(self):
        ner = ThaiNameTagger(version="1.5")
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
        self.assertIsNotNone(
            ner.get_ner(
                """คณะวิทยาศาสตร์ประยุกต์และวิศวกรรมศาสตร์ มหาวิทยาลัยขอนแก่น
                วิทยาเขตหนองคาย 112 หมู่ 7 บ้านหนองเดิ่น ตำบลหนองกอมเกาะ อำเภอเมือง
                จังหวัดหนองคาย 43000""",
                tag=True,
            )
        )

        # argument `tag` is True
        self.assertIsNotNone(
            ner.get_ner("วันที่ 15 ก.ย. 61 ทดสอบระบบเวลา 14:49 น.", tag=True)
        )

        ner = ThaiNameTagger(version="1.4")
        self.assertEqual(ner.get_ner(""), [])
        self.assertIsNotNone(ner.get_ner("แมวทำอะไรตอนห้าโมงเช้า"))
        self.assertIsNotNone(ner.get_ner("แมวทำอะไรตอนห้าโมงเช้า", pos=False))
        self.assertIsNotNone(
            ner.get_ner(
                """คณะวิทยาศาสตร์ประยุกต์และวิศวกรรมศาสตร์ มหาวิทยาลัยขอนแก่น
                วิทยาเขตหนองคาย 112 หมู่ 7 บ้านหนองเดิ่น
                ตำบลหนองกอมเกาะ อำเภอเมือง
                จังหวัดหนองคาย 43000"""
            )
        )
        self.assertIsNotNone(
            ner.get_ner(
                """คณะวิทยาศาสตร์ประยุกต์และวิศวกรรมศาสตร์ มหาวิทยาลัยขอนแก่น
                วิทยาเขตหนองคาย 112 หมู่ 7 บ้านหนองเดิ่น
                ตำบลหนองกอมเกาะ อำเภอเมือง
                จังหวัดหนองคาย 43000""",
                tag=True,
            )
        )

        # argument `tag` is True
        self.assertEqual(
            ner.get_ner("วันที่ 15 ก.ย. 61 ทดสอบระบบเวลา 14:49 น.", tag=True),
            "วันที่ <DATE>15 ก.ย. 61</DATE> "
            "ทดสอบระบบเวลา <TIME>14:49 น.</TIME>",
        )

        self.assertEqual(
            ner.get_ner(
                "url = https://thainlp.org/pythainlp/docs/2.0/", tag=True
            ),
            "url = <URL>https://thainlp.org/pythainlp/docs/2.0/</URL>",
        )

        self.assertEqual(
            ner.get_ner("example@gmail.com", tag=True),
            "<EMAIL>example@gmail.com</EMAIL>",
        )

        self.assertEqual(
            ner.get_ner("รหัสไปรษณีย์ 19130", tag=True),
            "รหัสไปรษณีย์ <ZIP>19130</ZIP>",
        )

        self.assertEqual(
            ner.get_ner("อาจารย์เอกพล ประจำคณะวิศวกรรมศาสตร์ ", tag=True),
            "<PERSON>อาจารย์เอกพล</PERSON> ประจำ<ORGANIZATION>"
            "คณะวิศวกรรมศาสตร์</ORGANIZATION> ",
        )

        """self.assertEqual(
            ner.get_ner(
                "มาตรา 80 ปพพ ให้ใช้อัตราภาษีร้อยละ 10.0"
                " ในการคำนวณภาษีมูลค่าเพิ่ม",
                tag=True,
            ),
            "<LAW>มาตรา 80 ปพพ</LAW> "
            "ให้ใช้อัตราภาษี<PERCENT>ร้อยละ 10.0</PERCENT>"
            " ในการคำนวณภาษีมูลค่าเพิ่ม",
        )"""

        self.assertEqual(
            ner.get_ner("ยาว 20 เซนติเมตร", tag=True),
            "ยาว <LEN>20 เซนติเมตร</LEN>",
        )

        self.assertEqual(
            ner.get_ner("1 บาท", pos=True, tag=True), "<MONEY>1 บาท</MONEY>"
        )

        self.assertEqual(
            ner.get_ner("ไทย", pos=False, tag=True), "<LOCATION>ไทย</LOCATION>"
        )

        self.assertIsNotNone(ner.get_ner("บางแสนกรุงเทพ", pos=False, tag=True))

        # argument `tag` is False and `pos` is True
        self.assertEqual(
            ner.get_ner("ไทย", pos=True, tag=False),
            [("ไทย", "PROPN", "B-LOCATION")],
        )

        # arguement `tag` is False and `pos` is False
        self.assertIsNotNone(
            ner.get_ner(
                "วันที่ 15 ก.ย. 61 ทดสอบระบบเวลา 14:49 น.",
                pos=False,
                tag=False,
            )
        )

    def test_tltk_ner(self):
        self.assertEqual(tltk.get_ner(""), [])
        self.assertIsNotNone(tltk.get_ner("แมวทำอะไรตอนห้าโมงเช้า"))
        self.assertIsNotNone(tltk.get_ner("แมวทำอะไรตอนห้าโมงเช้า", pos=False))
        self.assertIsNotNone(
            tltk.get_ner("พลเอกประยุกธ์ จันทร์โอชา ประกาศในฐานะหัวหน้า")
        )
        self.assertIsNotNone(
            tltk.get_ner(
                "พลเอกประยุกธ์ จันทร์โอชา ประกาศในฐานะหัวหน้า",
                tag=True,
            )
        )
        self.assertIsNotNone(
            tltk.get_ner(
                """คณะวิทยาศาสตร์ประยุกต์และวิศวกรรมศาสตร์ มหาวิทยาลัยขอนแก่น
                จังหวัดหนองคาย 43000"""
            )
        )
        self.assertIsNotNone(
            tltk.get_ner(
                """คณะวิทยาศาสตร์ประยุกต์และวิศวกรรมศาสตร์ มหาวิทยาลัยขอนแก่น
                จังหวัดหนองคาย 43000""",
                tag=True,
            )
        )

    def test_NER_class(self):
        ner = NER(engine="thainer")
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า"))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", pos=False))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", tag=True))
        # ner = NER(engine="wangchanberta")
        # self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า"))
        # self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", pos=False))
        # self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", tag=True))
        ner = NER(engine="thainer-v2")
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า"))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", pos=False))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", tag=True))
        ner = NER(engine="tltk")
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า"))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", pos=False))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", tag=True))
        with self.assertRaises(ValueError):
            NER(engine="thainer", corpus="cat")

    def test_NNER_class(self):
        nner = NNER()
        self.assertIsNotNone(nner.tag("แมวทำอะไรตอนห้าโมงเช้า"))

    def test_pos_tag_transformers(self):
        self.assertIsNotNone(
            pos_tag_transformers(
                sentence="แมวทำอะไรตอนห้าโมงเช้า",
                engine="bert",
                corpus="blackboard",
            )
        )
        self.assertIsNotNone(
            pos_tag_transformers(
                sentence="แมวทำอะไรตอนห้าโมงเช้า",
                engine="mdeberta",
                corpus="pud"
            )
        )
        self.assertIsNotNone(
            pos_tag_transformers(
                sentence="แมวทำอะไรตอนห้าโมงเช้า",
                engine="wangchanberta",
                corpus="pud",
            )
        )
        with self.assertRaises(ValueError):
            pos_tag_transformers(
                sentence="แมวทำอะไรตอนห้าโมงเช้า", engine="non-existing-engine"
            )
        with self.assertRaises(ValueError):
            pos_tag_transformers(
                sentence="แมวทำอะไรตอนห้าโมงเช้า",
                engine="bert",
                corpus="non-existing corpus",
            )
