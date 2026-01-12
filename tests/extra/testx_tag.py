# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.tag import (
    NER,
    NNER,
    pos_tag,
    pos_tag_transformers,
    tltk,
)
from pythainlp.tag.thainer import ThaiNameTagger


class TagTestCaseX(unittest.TestCase):
    # ### pythainlp.tag.pos_tag

    def test_pos_tag(self):
        tokens = ["ผม", "รัก", "คุณ"]
        self.assertIsNotNone(pos_tag(tokens, engine="tltk"))
        with self.assertRaises(ValueError):
            tltk.pos_tag(tokens, corpus="blackboard")

    # ### pythainlp.tag.named_entity

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

    def test_thai_name_tagger_1_5(self):
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
        self.assertIsNotNone(
            ner.get_ner("วันที่ 15 ก.ย. 61 ทดสอบระบบเวลา 14:49 น.", tag=True)
        )

    def test_thai_name_tagger_1_4(self):
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
        # self.assertEqual(
        #     ner.get_ner(
        #         "มาตรา 80 ปพพ ให้ใช้อัตราภาษีร้อยละ 10.0"
        #         " ในการคำนวณภาษีมูลค่าเพิ่ม",
        #         tag=True,
        #     ),
        #     "<LAW>มาตรา 80 ปพพ</LAW> "
        #     "ให้ใช้อัตราภาษี<PERCENT>ร้อยละ 10.0</PERCENT>"
        #     " ในการคำนวณภาษีมูลค่าเพิ่ม",
        # )
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
        self.assertEqual(
            ner.get_ner("ไทย", pos=True, tag=False),
            [("ไทย", "PROPN", "B-LOCATION")],
        )
        self.assertIsNotNone(
            ner.get_ner(
                "วันที่ 15 ก.ย. 61 ทดสอบระบบเวลา 14:49 น.",
                pos=False,
                tag=False,
            )
        )

    def test_NER_class(self):
        with self.assertRaises(ValueError):
            NER(engine="thainer", corpus="cat")

        ner = NER(engine="thainer")
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า"))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", pos=False))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", tag=True))

        ner = NER(engine="thainer-v2")
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า"))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", pos=False))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", tag=True))

        ner = NER(engine="wangchanberta")
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า"))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", pos=False))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", tag=True))

        ner = NER(engine="tltk")
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า"))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", pos=False))
        self.assertIsNotNone(ner.tag("แมวทำอะไรตอนห้าโมงเช้า", tag=True))

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
                corpus="pud",
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
