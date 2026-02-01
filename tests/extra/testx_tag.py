# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

# Tests for tag functions that need extra dependencies
# Note: Tests requiring transformers/tltk have been moved to tests.noautotest

import unittest

from pythainlp.tag.thainer import ThaiNameTagger


class TagTestCaseX(unittest.TestCase):
    # Tests for ThaiNameTagger (doesn't require transformers or tltk)
    # All tltk and transformers-based tests have been moved to tests.noautotest

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

