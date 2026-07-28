# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.khavee import KhaveeVerifier

kv = KhaveeVerifier()


class KhaveeCheckKlonExtendedTestCase(unittest.TestCase):

    """Tests for check_klon k_type=8 and invalid k_type."""

    def setUp(self):
        """Set up test fixtures."""
        self.kv = KhaveeVerifier()

    def test_invalid_k_type_returns_error_string(self):
        """Test that invalid k_type returns error string."""
        poem = "บทกวีทดสอบ"
        result = self.kv.check_klon(poem, k_type=99)
        self.assertIsInstance(result, str)
        self.assertIn(
            result,
            "Something went wrong. Make sure you enter it in the correct form "
            "(k_type 4 or 8)."
        )

    def test_incomplete_klon4_poem(self):
        """Test that incomplete klon4 poem is detected."""
        result = self.kv.check_klon("ฉันชื่อหมูกรอบ", k_type=4)
        self.assertIsInstance(result, str)
        self.assertIn(
            result,
            "The poem does not have complete stanzas (บท). "
            "A stanza must contain exactly 4 sentences (วรรค)."
        )

    def test_incomplete_klon8_poem(self):
        """Test that incomplete klon8 poem is detected."""
        poem = "ฉันชื่อหมูกรอบ"
        result = self.kv.check_klon(poem, k_type=8)
        self.assertIsInstance(result, str)
        self.assertIn(
            result,
            "The poem does not have complete stanzas (บท). "
            "A stanza must contain exactly 4 sentences (วรรค)."
        )

    def test_check_klon4_incorrect_poem(self):
        """Test that invalid klon4 poem is detected."""
        poem = (
            "มวลไม้ดอกสวด ระรวยกลิ่นหอม หมู่ผึ้งดมดอม พรั่งพร้อมนานา "
            "ผีเสื้อปีกบาง บินกางปีกมา ช่างงามจับตา เริงร่าสุขใจ"
        )
        result = self.kv.check_klon(poem, k_type=4)
        self.assertIsInstance(result, list)
        self.assertEqual(
            result, [
                "Rhyme error in Stanza (บทที่) 1: 'สวด' (Wak 1) "
                "does not rhyme with ['ระ', 'รวย'] (Wak 2)"
            ])

    def test_check_klon4_incorrect_poem_2(self):
        """Test that invalid klon4 poem with wrong inter-stanza rhyme is detected."""
        poem = (
            "มวลไม้ดอกสวด ระรวยกลิ่นหอม หมู่ผึ้งดมดอม พรั่งพร้อมนานะ "
            "ผีเสื้อปีกบาง บินกางปีกมา ช่างงามจับตา เริงร่าสุขใจ"
        )
        result = self.kv.check_klon(poem, k_type=4)
        self.assertIsInstance(result, list)
        self.assertEqual(
            result,
            [
                "Rhyme error in Stanza (บทที่) 1: "
                "'สวด' (Wak 1) does not rhyme with ['ระ', 'รวย'] (Wak 2)",
                "Inter-stanza rhyme error (ผิดสัมผัสระหว่างบท) between Stanza 1 and 2: "
                "'นะ' (Wak 4) does not rhyme with 'มา' (Wak 2)"
            ]
        )

    def test_check_klon4_correct_poem(self):
        """Test that valid klon4 poem is recognized."""
        poem = (
            "มวลไม้ดอกสวย ระรวยกลิ่นหอม หมู่ผึ้งดมดอม พรั่งพร้อมนานา "
            "ผีเสื้อปีกบาง บินกางปีกมา ช่างงามจับตา เริงร่าสุขใจ"
        )
        self.assertIsNotNone(self.kv.check_klon(poem, k_type=4))
        result = self.kv.check_klon(poem, k_type=4)
        self.assertEqual(result, "The poem is correct according to the principle.")

    def test_check_klon8_correct_poem(self):
        """Test that valid klon8 poem is recognized."""
        poem = (
            "มวลไม้ดอกสวยระรวยกลิ่นหอม หมู่ผึ้งดมดอมพรั่งพร้อมนานา "
            "ผีเสื้อปีกบางบินกางปีกมา ช่างงามจับตาเริงร่าสุขใจ"
        )
        self.assertIsNotNone(self.kv.check_klon(poem, k_type=8))
        result = self.kv.check_klon(poem, k_type=8)
        self.assertEqual(result, "The poem is correct according to the principle.")

    def test_check_klon8_correct_poem_2(self):
        """Test that another valid klon8 poem is recognized."""
        poem = (
            "แม่รักลูกลูกก็รู้อยู่ว่ารัก คนอื่นสักหมื่นแสนไม่แม้นเหมือน "
            "จะกินนอนวอนว่าเมตตาเตือน จะจากเรือนร้างแม่ไปแต่ตัว "
            "แม่วันทองของลูกจงกลับบ้าน เขาจะพาลว้าวุ่นแม่ทูนหัว "
            "จะก้มหน้าลาไปมิได้กลัว แม่อย่ามัวหมองนักจงหักใจ"
        )
        self.assertEqual(
            self.kv.check_klon(poem, k_type=8),
            "The poem is correct according to the principle."
        )

    def test_check_klon8_correct_poem_3(self):
        """Test that third valid klon8 poem is recognized."""
        poem = (
            "นางกอดจูบลูบหลังแล้วสั่งสอน อำนวยพรพลายน้อยละห้อยไห้ "
            "พ่อไปดีศรีสวัสดิ์กำจัดภัย จนเติบใหญ่ยิ่งยวดได้บวชเรียน "
            "ลูกผู้ชายลายมือนั้นคือยศ เเจ้าจงอตส่าห์ทำสม่ำเสมียน "
            "แล้วพาลูกออกมาข้างท่าเกวียน จะจากเจียนใจขาดอนาถใจ"
        )
        self.assertEqual(
            self.kv.check_klon(poem, k_type=8),
            "The poem is correct according to the principle."
        )

    def test_check_klon8_invalid_poem(self):
        """Test that invalid klon8 poem with too many words.
        (แม่รักลูกลูกก็รู้อยู่ว่ารักมากมาก)"""
        poem = (
            "แม่รักลูกลูกก็รู้อยู่ว่ารักมากมาก คนอื่นสักหมื่นแสนไม่แม้นเหมือน "
            "จะกินนอนวอนว่าเมตตาเตือน จะจากเรือนร้างแม่ไปแต่ตัว "
            "แม่วันทองของลูกจงกลับบ้าน เขาจะพาลว้าวุ่นแม่ทูนหัว "
            "จะก้มหน้าลาไปมิได้กลัว แม่อย่ามัวหมองนักจงหักใจ"
        )
        result = self.kv.check_klon(poem, k_type=8)
        self.assertIsInstance(result, list)
        self.assertEqual(
            result,
            [
                "Stanza (บทที่) 1 Wak 1: Word count exceeds 10: "
                "['แม่', 'รัก', 'ลูก', 'ลูก', 'ก็', 'รู้', 'อยู่', 'ว่า', 'รัก', 'มาก', 'มาก']",
                "Rhyme error in Stanza (บทที่) 1: 'มาก' (Wak 1) does not rhyme with "
                "['คน', 'อื่น', 'สัก', 'หมื่น', 'แสน'] (Wak 2)"
            ]
        )

    def test_check_klon8_invalid_poem_2(self):
        """Test that invalid klon8 poem with incorrect rhyme is detected."""
        poem = (
            "แม่รักลูกลูกก็รู้อยู่ว่ารักมาก คนอื่นสักหมื่นแสนไม่แม้นเหมือน "
            "จะกินนอนวอนว่าเมตตาเตือน จะจากเรือร้างแม่ไปแต่ตัว "
            "แม่วันทองของลูกจงกลับบ้าน เขาจะพาลว้าวุ่นแม่ทูนหัว "
            "จะก้มหน้าลาไปมิได้กลัว แม่อย่ามัวหมองนักจงหักใจ"
        )
        result = self.kv.check_klon(poem, k_type=8)
        self.assertIsInstance(result, list)
        self.assertEqual(
            result, [
                "Rhyme error in Stanza (บทที่) 1: 'มาก' (Wak 1) "
                "does not rhyme with ['คน', 'อื่น', 'สัก', 'หมื่น', 'แสน'] (Wak 2)",
                "Rhyme error in Stanza (บทที่) 1: 'เตือน' (Wak 3) does not rhyme with "
                "['จะ', 'จาก', 'เรือ', 'ร้าง', 'แม่'] (Wak 4)"]
        )

    def test_check_klon8_invalid_poem_3(self):
        """Test that invalid klon8 poem with wrong final word is detected."""
        poem = (
            "แม่รักลูกลูกก็รู้อยู่ว่ารัก คนอื่นสักหมื่นแสนไม่แม้นเหมือน "
            "จะกินนอนวอนว่าเมตตาเตือด จะจากเรือนร้างแม่ไปแต่ตัว "
            "แม่วันทองของลูกจงกลับบ้าน เขาจะพาลว้าวุ่นแม่ทูนหัว "
            "จะก้มหน้าลาไปมิได้กลัว แม่อย่ามัวหมองนักจงหักใจ"
        )
        result = self.kv.check_klon(poem, k_type=8)
        self.assertIsInstance(result, list)
        self.assertEqual(
            result, [
                "Rhyme error in Stanza (บทที่) 1: 'เหมือน' (Wak 2) "
                "does not rhyme with 'เตือด' (Wak 3)",
                "Rhyme error in Stanza (บทที่) 1: 'เตือด' (Wak 3) "
                "does not rhyme with ['จะ', 'จาก', 'เรือน', 'ร้าง', 'แม่'] (Wak 4)"]
        )

    def test_check_klon8_invalid_poem_4(self):
        """Test that invalid klon8 poem with wrong inter-stanza rhyme is detected."""
        poem = (
            "แม่รักลูกลูกก็รู้อยู่ว่ารัก คนอื่นสักหมื่นแสนไม่แม้นเหมือน "
            "จะกินนอนวอนว่าเมตตาเตือน จะจากเรือนร้างแม่ไปแต่ตัง "
            "แม่วันทองของลูกจงกลับบ้าน เขาจะพาลว้าวุ่นแม่ทูนหัว "
            "จะก้มหน้าลาไปมิได้กลัว แม่อย่ามัวหมองนักจงหักใจ"
        )
        result = self.kv.check_klon(poem, k_type=8)
        self.assertIsInstance(result, list)
        self.assertEqual(
            result,
            [
                "Inter-stanza rhyme error (ผิดสัมผัสระหว่างบท) "
                "between Stanza 1 and 2: 'ตัง' (Wak 4) "
                "does not rhyme with 'หัว' (Wak 2)"
            ]
        )

    def test_check_klon(self):
        """Test check_klon for Thai poem verification (k_type=4)."""
        poem = (
            "ฉันชื่อหมูกรอบ ฉันชอบกินไก่ แล้ววิ่งตามไป ไล่หมาน้ำทอง "
            "ฉันมันคนเก่ง เอ๋งเอ๋งคะนอง มีคนจับจอง เป็นของน้องเธียร"
        )
        result = self.kv.check_klon(poem, k_type=4)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "The poem is correct according to the principle.")

        poem_invalid = (
            "ฉันชื่อหมูกรอบ ฉันชอบกินไก่ แล้ววิ่งตามไล่ น้องหมาน้ำทอง "
            "ฉันมันคนโหด เอ๋งเอ๋งคะนอง มีคนจับจอง เป็นของน้องเธียร"
        )
        result_invalid = self.kv.check_klon(poem_invalid, k_type=4)
        self.assertIsInstance(result_invalid, list)
        self.assertEqual(
            result_invalid, [
                "Rhyme error in Stanza (บทที่) 1: 'ไล่' (Wak 3) "
                "does not rhyme with ['น้อง', 'หมา'] (Wak 4)",
                "Rhyme error in Stanza (บทที่) 2: 'โหด' (Wak 1) "
                "does not rhyme with ['เอ๋ง', 'เอ๋ง'] (Wak 2)"]
        )
