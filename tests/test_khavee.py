# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

import unittest
from pythainlp.khavee import KhaveeVerifier

kv = KhaveeVerifier()


class TestKhaveePackage(unittest.TestCase):
    def test_check_sara(self):
        self.assertEqual(kv.check_sara("เริง"), "เออ")

    def test_check_marttra(self):
        self.assertEqual(kv.check_marttra("สาว"), "เกอว")

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
                "Can't find rhyme between paragraphs ('หมา', 'จอง') in paragraph 2",
                "Can't find rhyme between paragraphs ('หมา', 'ทอง') in paragraph 2",
            ],
        )

    def test_check_aek_too(self):
        self.assertEqual(kv.check_aek_too("ไกด์"), False)
        self.assertEqual(kv.check_aek_too("ไก่"), "aek")
        self.assertEqual(kv.check_aek_too("ไก้"), "too")
        self.assertTrue(
            kv.check_aek_too(["หนม", "หน่ม", "หน้ม"]), [False, "aek", "too"]
        )
