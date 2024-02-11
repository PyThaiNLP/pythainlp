# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.soundex import (
    lk82,
    metasound,
    prayut_and_somchaip,
    soundex,
    udom83,
)
from pythainlp.soundex.sound import word_approximation, audio_vector


class TestSoundexPackage(unittest.TestCase):
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

    def test_word_approximation(self):
        self.assertIsNotNone(word_approximation("รถ", ["รส", "รด", "คน"]))

    def test_audio_vector(self):
        self.assertIsNotNone(audio_vector("คน"))
