# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.soundex import (
    complete_soundex,
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
        self.assertIsNotNone(soundex("a", engine="complete_soundex"))
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

        # Test complete_soundex
        self.assertEqual(complete_soundex(None), "")
        self.assertEqual(complete_soundex(""), "")
        
        # Single syllable test cases from the paper
        self.assertEqual(complete_soundex("ก้าน"), "กก1Bน2-")
        self.assertEqual(complete_soundex("มารค"), "มม1B-ก0-")
        self.assertEqual(complete_soundex("กลับ"), "กก1Aบ0ล")
        self.assertEqual(complete_soundex("กมล"), "กก1A-0-มม7Mน0-")
        self.assertEqual(complete_soundex("ใกล้"), "กก1Aย2ล")
        self.assertEqual(complete_soundex("โก่ง"), "กก7Nง1-")
        self.assertEqual(complete_soundex("เครื่อง"), "คคBVง1ร")
        self.assertEqual(complete_soundex("ก้ม"), "กก7Mม2-")
        self.assertEqual(complete_soundex("แกน"), "กก6Lน0-")
        self.assertEqual(complete_soundex("ทราย"), "ซซ1Bย0-")
        self.assertEqual(complete_soundex("สวรรค์"), "ซศ1A-0-วว1Aน0-")
        
        # Individual syllable encoding (for use with pre-tokenized syllables)
        self.assertEqual(complete_soundex("ปัน"), "ปป1A0น-")
        self.assertEqual(complete_soundex("นา"), "นน1B0--")
        self.assertEqual(complete_soundex("ปุญ"), "ปป4G0น-")
        self.assertEqual(complete_soundex("ญา"), "ยย1B0--*")
        self.assertEqual(complete_soundex("ปัญ"), "ปป1A0น-")
        self.assertEqual(complete_soundex("บุญ"), "บบ4G0น-")
        self.assertEqual(complete_soundex("บุณ"), "บบ4G0น-")
        self.assertEqual(complete_soundex("ยา"), "ยย1B0--")
        
        # Multi-syllable words should be tokenized first:
        # from pythainlp.tokenize import syllable_tokenize
        # syllables = syllable_tokenize("ปุญญา")  # ['ปุญ', 'ญา']
        # result = ''.join([complete_soundex(syl) for syl in syllables])
        # Expected: 'ปป4G0น-ยย1B0--*'
