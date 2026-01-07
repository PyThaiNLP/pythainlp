# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.soundex import (
    lk82,
    metasound,
    prayut_and_somchaip,
    soundex,
    udom83,
)


class SoundexTestCase(unittest.TestCase):
    def test_soundex(self):
        self.assertIsNotNone(soundex("a", engine="lk82"))
        self.assertIsNotNone(soundex("a", engine="udom83"))
        self.assertIsNotNone(soundex("a", engine="metasound"))
        self.assertEqual(
            soundex("vp", engine="prayut_and_somchaip"),
            soundex("วีพี", engine="prayut_and_somchaip"),
        )
        self.assertIsNotNone(soundex("a", engine="XXX"))

        self.assertEqual(lk82(None), "")
        self.assertEqual(lk82(""), "")
        self.assertEqual(lk82("เหตุ"), lk82("เหด"))
        self.assertEqual(lk82("รถ"), "ร3000")
        self.assertIsNotNone(lk82("เกาะ"))
        self.assertIsNotNone(lk82("อุยกูร์"))
        self.assertIsNotNone(lk82("หยากไย่"))
        self.assertIsNotNone(lk82("หอ"))
        self.assertIsNotNone(lk82("อยู่"))
        self.assertIsNotNone(lk82("อู่"))
        self.assertIsNotNone(lk82("อย่าง"))
        self.assertIsNotNone(lk82("เหย้า"))
        self.assertIsNotNone(lk82("หยุด"))
        self.assertIsNotNone(lk82("หืออือ"))
        self.assertEqual(lk82("น์"), "")

        # Comprehensive LK82 test cases from issue #1131
        # Test similar-sounding names starting with ส (s sound)
        self.assertEqual(lk82("สุวัช"), "สE300")
        self.assertEqual(lk82("สุวัจจ์"), "สE300")
        self.assertEqual(lk82("สุวัชช์"), "สE300")
        self.assertEqual(lk82("สุวัจน์"), "สE300")
        self.assertEqual(lk82("สุวัชร"), "สE300")
        self.assertEqual(lk82("สุวัฒน์"), "สE300")
        self.assertEqual(lk82("สุวัต"), "สE300")
        self.assertEqual(lk82("สุวัติ"), "สE300")
        self.assertEqual(lk82("สุวัตถ์"), "สE300")
        self.assertEqual(lk82("สุวัตดี"), "สE300")
        self.assertEqual(lk82("สุวัชน์"), "สE300")
        self.assertEqual(lk82("สุวัตร"), "สE300")
        self.assertEqual(lk82("สุวัตร์"), "สE300")
        self.assertEqual(lk82("สุวัศ"), "สE300")
        self.assertEqual(lk82("สุวรรดิ"), "สE300")
        self.assertEqual(lk82("ศุวัตร"), "สE300")
        self.assertEqual(lk82("สุวิทย์"), "สE300")
        self.assertEqual(lk82("สุวิช"), "สE300")
        self.assertEqual(lk82("สุวิชย์"), "สE300")

        # Test similar-sounding names starting with ป (p sound)
        self.assertEqual(lk82("ประพาส"), "ป5930")
        self.assertEqual(lk82("ประพาศ"), "ป5930")
        self.assertEqual(lk82("ประพาศน์"), "ป5930")
        self.assertEqual(lk82("ประภาส"), "ป5930")
        self.assertEqual(lk82("ประภาศ"), "ป5930")
        self.assertEqual(lk82("ประภาศน์"), "ป5930")
        self.assertEqual(lk82("ประภาสน์"), "ป5930")
        self.assertEqual(lk82("ประภาศรี"), "ป5930")

        # Test similar names with ญ/น
        self.assertEqual(lk82("ปันนา"), "ป4900")
        self.assertEqual(lk82("ปัญญา"), "ป4900")

        # Test similar names with double consonants
        self.assertEqual(lk82("ธรรมะ"), "ท6000")
        self.assertEqual(lk82("ธัมมะ"), "ท6000")

        # Test names with ญ/ย
        self.assertEqual(lk82("บุญยา"), "บE490")
        self.assertEqual(lk82("บุญญา"), "บE490")

        # Test leading vowel handling
        self.assertEqual(lk82("เกม"), "กB600")

        # Test semivowel
        self.assertEqual(lk82("กิ่ว"), "ก7000")

        self.assertEqual(udom83(None), "")
        self.assertEqual(udom83(""), "")
        self.assertEqual(udom83("เหตุ"), udom83("เหด"))
        self.assertEqual(udom83("รถ"), "ร800000")
        self.assertEqual(udom83("น์"), "")

        self.assertEqual(metasound(None), "")
        self.assertEqual(metasound(""), "")
        self.assertEqual(metasound("เหตุ"), metasound("เหด"))
        self.assertEqual(metasound("รักษ์"), metasound("รัก"))
        self.assertEqual(metasound("บูรณะ"), "บ550")
        self.assertEqual(metasound("คน"), "ค500")
        self.assertEqual(metasound("คนA"), "ค500")
        self.assertEqual(metasound("ดา"), "ด000")
        self.assertIsNotNone(metasound("จะ"))
        self.assertIsNotNone(metasound("ปา"))
        self.assertIsNotNone(metasound("งง"))
        self.assertIsNotNone(metasound("ลา"))
        self.assertIsNotNone(metasound("มา"))
        self.assertIsNotNone(metasound("ยา"))
        self.assertIsNotNone(metasound("วา"))
        self.assertIsNotNone(metasound("บูชา"))
        self.assertIsNotNone(metasound("กมลา"))
        self.assertIsNotNone(metasound("กาโวกาโว"))
        self.assertIsNotNone(metasound("สุวรรณา"))
        self.assertIsNotNone(metasound("ดอยบอย"))

        self.assertEqual(prayut_and_somchaip(None), "")
        self.assertEqual(prayut_and_somchaip(""), "")
        self.assertEqual(prayut_and_somchaip("vp"), "11")
        self.assertIsNotNone(prayut_and_somchaip("บา"))
        self.assertIsNotNone(prayut_and_somchaip("go"))
        self.assertIsNotNone(prayut_and_somchaip("อด"))
        self.assertIsNotNone(prayut_and_somchaip("ลน"))
        self.assertIsNotNone(prayut_and_somchaip("มอ"))
        self.assertIsNotNone(prayut_and_somchaip("รอ"))
        self.assertIsNotNone(prayut_and_somchaip("ขอ"))
        self.assertIsNotNone(prayut_and_somchaip("บน"))
        self.assertIsNotNone(prayut_and_somchaip("ณาญ"))
        self.assertIsNotNone(prayut_and_somchaip("กาง"))
        self.assertIsNotNone(prayut_and_somchaip("ว้าว"))
