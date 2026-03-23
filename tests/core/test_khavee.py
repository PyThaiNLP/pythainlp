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
                "Can't find rhyme between paragraphs ('หมา', 'จอง') in paragraph 2",
                "Can't find rhyme between paragraphs ('หมา', 'ทอง') in paragraph 2",
            ],
        )

    def test_check_aek_too(self):
        self.assertFalse(kv.check_aek_too("ไกด์"))
        self.assertEqual(kv.check_aek_too("ไก่"), "aek")
        self.assertEqual(kv.check_aek_too("ไก้"), "too")
        self.assertTrue(
            kv.check_aek_too(["หนม", "หน่ม", "หน้ม"]), [False, "aek", "too"]
        )


class KhaveeCheckKaruLahuTestCase(unittest.TestCase):
    """Tests for KhaveeVerifier.check_karu_lahu"""

    def setUp(self):
        self.kv = KhaveeVerifier()

    def test_dead_syllable_is_karu(self):
        self.assertEqual(self.kv.check_karu_lahu("กด"), "karu")

    def test_long_live_syllable_is_karu(self):
        self.assertEqual(self.kv.check_karu_lahu("กา"), "karu")

    def test_live_syllable_with_final_consonant_is_karu(self):
        self.assertEqual(self.kv.check_karu_lahu("กาน"), "karu")

    def test_bo_mai_ek_is_lahu(self):
        self.assertEqual(self.kv.check_karu_lahu("บ่"), "lahu")

    def test_no_short_word_is_lahu(self):
        self.assertEqual(self.kv.check_karu_lahu("ณ"), "lahu")

    def test_tho_short_word_is_lahu(self):
        self.assertEqual(self.kv.check_karu_lahu("ธ"), "lahu")

    def test_ko_mai_is_lahu(self):
        self.assertEqual(self.kv.check_karu_lahu("ก็"), "lahu")


class KhaveeHandleKarunTestCase(unittest.TestCase):
    """Tests for KhaveeVerifier.handle_karun_sound_silence"""

    def setUp(self):
        self.kv = KhaveeVerifier()

    def test_word_without_karun_unchanged(self):
        self.assertEqual(self.kv.handle_karun_sound_silence("คน"), "คน")
        self.assertEqual(self.kv.handle_karun_sound_silence("กา"), "กา")

    def test_word_ending_with_karun_stripped(self):
        # เกมส์ → drop ์ and the consonant before it (ส) → เกม
        self.assertEqual(self.kv.handle_karun_sound_silence("เกมส์"), "เกม")

    def test_word_ending_with_karun_stripped_2(self):
        # รักษ์ → drop ์ + ษ → รัก
        self.assertEqual(self.kv.handle_karun_sound_silence("รักษ์"), "รัก")

    def test_returns_string(self):
        self.assertIsInstance(self.kv.handle_karun_sound_silence("สวัสดี"), str)


class KhaveeCheckAekTooEdgeCasesTestCase(unittest.TestCase):
    """Edge-case tests for KhaveeVerifier.check_aek_too"""

    def setUp(self):
        self.kv = KhaveeVerifier()

    def test_non_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.kv.check_aek_too(123)  # type: ignore[arg-type]

    def test_dead_syllable_as_aek_flag(self):
        self.assertEqual(self.kv.check_aek_too("บท", dead_syllable_as_aek=True), "aek")

    def test_dead_syllable_without_flag_returns_false(self):
        self.assertFalse(self.kv.check_aek_too("บท", dead_syllable_as_aek=False))

    def test_list_with_non_string_element_raises(self):
        with self.assertRaises(TypeError):
            self.kv.check_aek_too(["ไก่", 42])  # type: ignore[list-item]

    def test_both_tone_marks_returns_false(self):
        # word with both ่ and ้ should return False
        self.assertFalse(self.kv.check_aek_too("ก่้"))


class KhaveeCheckKlonExtendedTestCase(unittest.TestCase):
    """Tests for check_klon k_type=8 and invalid k_type"""

    def setUp(self):
        self.kv = KhaveeVerifier()

    def test_invalid_k_type_returns_error_string(self):
        result = self.kv.check_klon("บทกวีทดสอบ", k_type=99)
        self.assertIsInstance(result, str)
        self.assertIn("Something went wrong", result)

    def test_incomplete_klon4_poem(self):
        result = self.kv.check_klon("ฉันชื่อหมูกรอบ", k_type=4)
        self.assertIsInstance(result, str)
        self.assertIn("does not have 4 complete sentences", result)

    def test_incomplete_klon8_poem(self):
        result = self.kv.check_klon("ฉันชื่อหมูกรอบ", k_type=8)
        self.assertIsInstance(result, str)

    def test_check_klon8_correct_poem(self):
        poem = (
            "ฉันชื่อหมูกรอบ ฉันชอบกินไก่ แล้วก็วิ่งไล่ หมาชื่อนํ้าทอง "
            "ลคคนเก่ง เอ๋งเอ๋งคะนอง มีคนจับจอง เขาชื่อน้องเธียร"
        )
        self.assertIsNotNone(self.kv.check_klon(poem, k_type=8))


class KhaveeCheckSaraEdgeCasesTestCase(unittest.TestCase):
    """Edge-case tests for KhaveeVerifier.check_sara"""

    def setUp(self):
        self.kv = KhaveeVerifier()

    def test_bo_mai_ek_returns_oo(self):
        self.assertEqual(self.kv.check_sara("บ่"), "ออ")

    def test_special_word_เออ(self):
        self.assertEqual(self.kv.check_sara("เออ"), "เออ")

    def test_special_word_เอ(self):
        self.assertEqual(self.kv.check_sara("เอ"), "เอ")

    def test_special_word_เอะ(self):
        self.assertEqual(self.kv.check_sara("เอะ"), "เอะ")

    def test_special_word_เอา(self):
        self.assertEqual(self.kv.check_sara("เอา"), "เอา")

    def test_special_word_เอาะ(self):
        self.assertEqual(self.kv.check_sara("เอาะ"), "เอาะ")

    def test_ru_sara(self):
        self.assertEqual(self.kv.check_sara("ฤ"), "อึ")

    def test_ruea_sara(self):
        # ฤา (ฤ + sara aa U+0E32) → อือ; note: ฤๅ uses lakkhangyao, not sara aa
        self.assertEqual(self.kv.check_sara("ฤา"), "อือ")

    def test_เอือ_sara(self):
        self.assertEqual(self.kv.check_sara("เรือ"), "เอือ")

    def test_returns_string(self):
        self.assertIsInstance(self.kv.check_sara("เริง"), str)
