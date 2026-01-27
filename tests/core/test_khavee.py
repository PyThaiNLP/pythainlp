# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.khavee import KhaveeVerifier

kv = KhaveeVerifier()


class KhaveeTestCase(unittest.TestCase):
    def test_check_sara(self):
        self.assertEqual(kv.check_sara("เริง"), "เออ")

    def test_check_marttra(self):
        self.assertEqual(kv.check_marttra("ปลิง"), "กง")
        self.assertEqual(kv.check_marttra("ยูง"), "กง")
        self.assertEqual(kv.check_marttra("กล่อง"), "กง")
        self.assertEqual(kv.check_marttra("สอง"), "กง")
        self.assertEqual(kv.check_marttra("เอ็ง"), "กง")
        self.assertEqual(kv.check_marttra("งง"), "กง")

        self.assertEqual(kv.check_marttra("ลม"), "กม")
        self.assertEqual(kv.check_marttra("เฉลิม"), "กม")
        self.assertEqual(kv.check_marttra("เข็ม"), "กม")
        self.assertEqual(kv.check_marttra("จาม"), "กม")
        self.assertEqual(kv.check_marttra("ยิ้ม"), "กม")
        self.assertEqual(kv.check_marttra("เกม"), "กม")
        self.assertEqual(kv.check_marttra("ขำ"), "กม")
        self.assertEqual(kv.check_marttra("รมย์"), "กม")

        self.assertEqual(kv.check_marttra("สวย"), "เกย")
        self.assertEqual(kv.check_marttra("โปรย"), "เกย")
        self.assertEqual(kv.check_marttra("เนย"), "เกย")
        self.assertEqual(kv.check_marttra("คอย"), "เกย")
        self.assertEqual(kv.check_marttra("ง่าย"), "เกย")
        self.assertEqual(kv.check_marttra("ทัย"), "เกย")
        self.assertEqual(kv.check_marttra("ไทย"), "เกย")
        self.assertEqual(kv.check_marttra("ไกล"), "เกย")
        self.assertEqual(kv.check_marttra("ใกล้"), "เกย")

        self.assertEqual(kv.check_marttra("สาว"), "เกอว")
        self.assertEqual(kv.check_marttra("นิ้ว"), "เกอว")
        self.assertEqual(kv.check_marttra("แมว"), "เกอว")
        self.assertEqual(kv.check_marttra("ดาว"), "เกอว")
        self.assertEqual(kv.check_marttra("แก้ว"), "เกอว")

        self.assertEqual(kv.check_marttra("บก"), "กก")
        self.assertEqual(kv.check_marttra("โรค"), "กก")
        self.assertEqual(kv.check_marttra("ลาก"), "กก")
        self.assertEqual(kv.check_marttra("นัข"), "กก")
        self.assertEqual(kv.check_marttra("จักร"), "กก")

        self.assertEqual(kv.check_marttra("จด"), "กด")
        self.assertEqual(kv.check_marttra("ตรวจ"), "กด")
        self.assertEqual(kv.check_marttra("เสริฐ"), "กด")
        self.assertEqual(kv.check_marttra("บุตร"), "กด")
        self.assertEqual(kv.check_marttra("ตรุษ"), "กด")
        self.assertEqual(kv.check_marttra("มืด"), "กด")
        self.assertEqual(kv.check_marttra("โยชน์"), "กด")

        self.assertEqual(kv.check_marttra("มึน"), "กน")
        self.assertEqual(kv.check_marttra("ร้าน"), "กน")
        self.assertEqual(kv.check_marttra("ขนุน"), "กน")
        self.assertEqual(kv.check_marttra("คน"), "กน")
        self.assertEqual(kv.check_marttra("ทมิฬ"), "กน")
        self.assertEqual(kv.check_marttra("ซีน"), "กน")
        self.assertEqual(kv.check_marttra("บรร"), "กน")
        self.assertEqual(kv.check_marttra("กร"), "กน")
        self.assertEqual(kv.check_marttra("เณร"), "กน")
        self.assertEqual(kv.check_marttra("ยนต์"), "กน")
        self.assertEqual(kv.check_marttra("กรรณ"), "กน")

        self.assertEqual(kv.check_marttra("ชอบ"), "กบ")
        self.assertEqual(kv.check_marttra("ภาพ"), "กบ")
        self.assertEqual(kv.check_marttra("เทพ"), "กบ")
        self.assertEqual(kv.check_marttra("รูป"), "กบ")
        self.assertEqual(kv.check_marttra("เวฟ"), "กบ")
        self.assertEqual(kv.check_marttra("โลพ"), "กบ")

        self.assertEqual(kv.check_marttra("ปลา"), "กา")
        self.assertEqual(kv.check_marttra("งู"), "กา")
        self.assertEqual(kv.check_marttra("หมู"), "กา")
        self.assertEqual(kv.check_marttra("มือ"), "กา")
        self.assertEqual(kv.check_marttra("ล้อ"), "กา")

    def test_is_sumpus(self):
        self.assertTrue(kv.is_sumpus("สรร", "อัน"))
        self.assertFalse(kv.is_sumpus("สรร", "แมว"))

    def test_check_klon(self):
        self.assertEqual(
            kv.check_klon(
                "ฉันชื่อหมูกรอบ ฉันชอบกินไก่ แล้วก็วิ่งไล่ หมาชื่อนํ้าทอง \
                    ลคคนเก่ง เอ๋งเอ๋งคะนอง มีคนจับจอง เขาชื่อน้องเธียร",
                k_type=4,
            ),
            "The poem is correct according to the principle.",
        )
        self.assertEqual(
            kv.check_klon(
                "ฉันชื่อหมูกรอบ ฉันชอบกินไก่ แล้วก็วิ่งไล่ หมาชื่อนํ้าทอง \
                    ลคคนเก่ง เอ๋งเอ๋งเสียงหมา มีคนจับจอง เขาชื่อน้องเธียร",
                k_type=4,
            ),
            [
                (
                    "Can't find rhyme between paragraphs ('หมา', 'จอง') "
                    "in paragraph 2"
                ),
                (
                    "Can't find rhyme between paragraphs ('หมา', 'ทอง') "
                    "in paragraph 2"
                ),
            ],
        )

    def test_check_aek_too(self):
        self.assertFalse(kv.check_aek_too("ไกด์"))
        self.assertEqual(kv.check_aek_too("ไก่"), "aek")
        self.assertEqual(kv.check_aek_too("ไก้"), "too")
        self.assertTrue(
            kv.check_aek_too(["หนม", "หน่ม", "หน้ม"]), [False, "aek", "too"]
        )
