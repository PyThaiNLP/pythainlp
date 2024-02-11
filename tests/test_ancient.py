# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
import unittest
from pythainlp.ancient import aksonhan_to_current


class TestAncientPackage(unittest.TestCase):
    def test_aksonhan_to_current(self):
        self.assertEqual(aksonhan_to_current("ก"), "ก")
        self.assertEqual(aksonhan_to_current("กก"), "กก")
        self.assertEqual(aksonhan_to_current("ถนน"), "ถนน")
        self.assertEqual(aksonhan_to_current("จกก"), "จัก")
        self.assertEqual(aksonhan_to_current("ดง่ง"), "ดั่ง")
        self.assertEqual(aksonhan_to_current("นน้น"), "นั้น")
        self.assertEqual(aksonhan_to_current("ขดด"), "ขัด")
        self.assertEqual(aksonhan_to_current("ตรสส"), "ตรัส")
        self.assertEqual(aksonhan_to_current("ขบบ"), "ขับ")
        self.assertEqual(aksonhan_to_current("วนน"), "วัน")
        self.assertEqual(aksonhan_to_current("หลงง"), "หลัง")
        self.assertEqual(aksonhan_to_current("บงงคบบ"), "บังคับ")
        self.assertEqual(aksonhan_to_current("สรรเพชญ"), "สรรเพชญ")
