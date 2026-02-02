# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.ancient import aksonhan_to_current, convert_currency


class AncientTestCase(unittest.TestCase):
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

        # Edge cases
        self.assertEqual(aksonhan_to_current(""), "")  # empty string
        self.assertEqual(aksonhan_to_current("ก"), "ก")  # single char
        self.assertEqual(aksonhan_to_current("กา"), "กา")  # two chars

    def test_convert_currency(self):
        self.assertEqual(
            convert_currency(80, "บาท")["ตำลึง"],
            20.0
        )
        self.assertEqual(
            convert_currency(80, "บาท")["ชั่ง"],
            1.0
        )
        self.assertEqual(
            convert_currency(80, "บาท")["บาท"],
            80.0
        )
        self.assertEqual(
            convert_currency(1,"ชั่ง")["บาท"],
            80.0
        )
        self.assertEqual(
            convert_currency(1,"ชั่ง")["ชั่ง"],
            1.0
        )

        # Test all supported units
        result = convert_currency(1, "บาท")
        self.assertIn("เบี้ย", result)
        self.assertIn("อัฐ", result)
        self.assertIn("ไพ", result)
        self.assertIn("เฟื้อง", result)
        self.assertIn("สลึง", result)
        self.assertIn("ตำลึง", result)

        # Test with zero value
        result = convert_currency(0, "บาท")
        self.assertEqual(result["บาท"], 0.0)

        # Test with fractional value
        result = convert_currency(0.5, "บาท")
        self.assertEqual(result["บาท"], 0.5)

        # Test invalid unit
        with self.assertRaises(NotImplementedError):
            convert_currency(1, "invalid_unit")
