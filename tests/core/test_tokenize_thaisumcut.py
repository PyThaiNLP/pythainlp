# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Unit tests for pythainlp.tokenize.thaisumcut."""

import unittest

from pythainlp.tokenize import sent_tokenize
from pythainlp.tokenize.thaisumcut import (
    ThaiSentenceSegmentor,
    list_to_string,
    middle_cut,
)

# Phrases that contain a splitting word (such as "แต่", "เพื่อ", or "ทำให้")
# but must stay in one sentence.
PROTECTED_PHRASES = (
    "โดยเร็ว",
    "เพื่อน",
    "แต่ง",
    "โดยสาร",
    "แล้วแต่",
    "หรือเปล่า",
    "หรือไม่",
    "จึงรุ่งเรืองกิจ",
    "ตั้งแต่",
    "แต่ละ",
    "วิตแล้ว",
    "โดยประ",
    "แต่หลังจากนั้น",
    "พรรคเพื่อ",
    "แต่เนื่อง",
    "เพื่อทำให้",
    "ทำเพื่อ",
    "จึงทำให้",
    "มาโดยตลอด",
    "แต่อย่างใด",
    "แต่หลังจาก",
    "คงทำให้",
    "แต่ทั้งนี้",
    "มีแต่",
    "เหตุที่ทำให้",
    "โดยหลังจาก",
    "ซึ่งหลังจาก",
    "ตั้งโดย",
    "โดยตรง",
    "นั้นหรือ",
    "ซึ่งต้องทำให้",
    "ชื่อต่อมา",
    "โดยเร่งด่วน",
    "ไม่ได้ทำให้",
    "จะทำให้",
    "จนทำให้",
    "เว้นแต่",
    "ก็ทำให้",
    "บางส่วน",
    "หรือแม้แต่",
    "โดยทำให้",
    "หรือเพราะ",
    "มาแต่",
    "แต่ไม่ทำให้",
    "ฉะนั้นเมื่อ",
    "เพราะฉะนั้น",
    "เพราะหลังจาก",
    "สามารถทำให้",
    "อาจทำ",
    "จะทำ",
    "อีกทั้งเพื่อ",
    "ทั้งนี้เพื่อ",
    "เวลาต่อมา",
    "อย่างไรก็ตามหลังจาก",
    "ซึ่งทำให้",
    "โดยประมาท",
    "โดยธรรม",
    "โดยสัจจริง",
)

WORDS = ["ผม", "กิน", "ข้าว", "เธอ", "เล่น", "เกม"]


class ListToStringTestCase(unittest.TestCase):
    def test_list_to_string(self):
        self.assertEqual(list_to_string([]), "")
        self.assertEqual(list_to_string(["ผม", "กิน"]), "ผมกิน")
        self.assertEqual(
            list_to_string(["ผม", " ", "  กิน", "\n", "ข้าว"]), "ผม กิน ข้าว"
        )


class MiddleCutTestCase(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(middle_cut([]), [])

    def test_short_sentence_is_unchanged(self):
        self.assertEqual(middle_cut(["ผมกินข้าว"]), ["ผมกินข้าว"])

    def test_remove_space_around_digits(self):
        self.assertEqual(
            middle_cut(["ก 5ข", "คะแนน 12 คะแนน", "1 2 3"]),
            ["ก5ข", "คะแนน12คะแนน", "12 3"],
        )

    def test_long_sentence_is_cut_at_whitespace(self):
        # 24 words: one cut
        text = " ".join(WORDS * 4)
        self.assertEqual(
            middle_cut([text]),
            [
                "ผม กิน ข้าว เธอ เล่น เกม",
                " ".join(WORDS * 3),
            ],
        )

    def test_very_long_sentence_is_cut_more_than_once(self):
        # 45 words: two cuts
        text = " ".join((WORDS * 8)[:45])
        parts = middle_cut([text])
        self.assertEqual(len(parts), 3)
        self.assertEqual(" ".join(parts), text)

    def test_long_sentence_without_whitespace_is_unchanged(self):
        text = "".join(WORDS * 5)
        self.assertEqual(middle_cut([text]), [text])


class SplitIntoSentencesTestCase(unittest.TestCase):
    def setUp(self):
        self.segmentor = ThaiSentenceSegmentor()

    def test_empty_inputs(self):
        for text in ["", " ", "\n", "nan", " nan "]:
            with self.subTest(text=text):
                self.assertEqual(self.segmentor.split_into_sentences(text), [])

    def test_sentences(self):
        cases = [
            ("ผมไปโรงเรียนครับ วันนี้อากาศดีค่ะ", ["ผมไปโรงเรียนครับ", "วันนี้อากาศดีค่ะ"]),
            (
                "เขาไปตลาดเพราะฝนตกหนัก แต่ไม่ได้ซื้อของ",
                ["เขาไปตลาด", "เพราะฝนตกหนัก", "แต่ไม่ได้ซื้อของ"],
            ),
            (
                "นายกรัฐมนตรีกล่าวว่าจะแก้ปัญหา รัฐมนตรีเปิดเผยว่าเตรียมงบไว้แล้ว",
                [
                    "นายกรัฐมนตรีกล่าวว่า",
                    "จะแก้ปัญหา รัฐมนตรีเปิดเผยว่า",
                    "เตรียมงบไว้แล้ว",
                ],
            ),
            (
                "เกิดเหตุไฟไหม้ ล่าสุด ตำรวจมาถึงที่เกิดเหตุ เบื้องต้น ไม่มีผู้บาดเจ็บ",
                ["เกิดเหตุไฟไหม้", "ล่าสุด ตำรวจมาถึงที่เกิดเหตุ", "เบื้องต้น ไม่มีผู้บาดเจ็บ"],
            ),
            (
                "ผู้เสียชีวิตได้แก่ 1.นายสมชาย 12.นางสมศรี 3.น.ส.สมหญิง",
                ["ผู้เสียชีวิตได้แก่", "1.นายสมชาย", "12.นางสมศรี", "3.น.ส.สมหญิง"],
            ),
            (
                "เขากินข้าวแล้ว เธอกลับบ้านอีกด้วย ผมไปทำงาน",
                ["เขากินข้าวแล้ว", "เธอกลับบ้านอีกด้วย", "ผมไปทำงาน"],
            ),
            (
                'เขาตะโกนว่า "ช่วยด้วย." เธอตอบว่า “ได้เลย.”',
                ['เขาตะโกนว่า "ช่วยด้วย". เธอตอบว่า “ได้เลย”.'],
            ),
            (
                'ใครมา?" เขาถามว่า "ไปไหน?" และ "ไม่!"',
                ['ใครมา"?', 'เขาถามว่า "ไปไหน"?', 'และ "ไม่"!'],
            ),
            ("ไปไหน? กลับบ้าน! ตกลง", ["ไปไหน?", "กลับบ้าน!", "ตกลง"]),
            ("nan nan ผม", ["nan nan ผม"]),
            (
                "ผมกินข้าว\nเธอกลับบ้านครับ\nวันนี้ดีค่ะ",
                ["ผมกินข้าว เธอกลับบ้านครับ", "วันนี้ดีค่ะ"],
            ),
            (
                "กลับมาจึงทำให้เขาเหนื่อย ทำเพื่อลูกหลานด้วย",
                ["กลับมา", "จึงทำให้เขาเหนื่อย ทำเพื่อลูกหลานด้วย"],
            ),
            (
                "ผมกินข้าวและ ดื่มน้ำ ส่วนเธอเล่นเกมและดูหนัง",
                ["ผมกินข้าวและ ดื่มน้ำ", "ส่วนเธอเล่นเกมและดูหนัง"],
            ),
            (
                "ผมชอบแมวหรือ หมา ส่วนเธอเลือกกินข้าวหรือขนมก็ได้",
                ["ผมชอบแมวหรือ หมา", "ส่วนเธอเลือกกินข้าวหรือขนมก็ได้"],
            ),
            ("ผมไปบ้านจึง กลับ", ["ผมไปบ้านจึง กลับ"]),
            (
                "เขาไปถึงทั้งนี้เพื่อลูก อย่างไรก็ตามหลังจากนั้นกลับ และนอกจากนี้ยังมีอีก",
                ["เขาไปถึงทั้งนี้เพื่อลูก", "อย่างไรก็ตามหลังจากนั้นกลับ", "นอกจากนี้ยังมีอีก"],
            ),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(
                    self.segmentor.split_into_sentences(text), expected
                )

    def test_protected_phrases_are_not_split(self):
        for phrase in PROTECTED_PHRASES:
            with self.subTest(phrase=phrase):
                sentences = self.segmentor.split_into_sentences(
                    f"เขาเดินทางไป{phrase}ต่อไป"
                )
                self.assertTrue(any(phrase in s for s in sentences))
                self.assertFalse(any("<" in s for s in sentences))

    def test_conjunction_with_space_nearby(self):
        # A split goes at the space when it is close to the keyword,
        # before the keyword when it is farther: และ at 5 tokens,
        # หรือ at 4, and จึง at 3.
        cases = [
            ("ผมและกินข้าวเล่นเกม ไปดีมากรถ", ["ผมและกินข้าวเล่นเกม", "ไปดีมากรถ"]),
            (
                "ผมและกินข้าวเล่นเกมแมว ไปดีมากรถ",
                ["ผม", "และกินข้าวเล่นเกมแมว ไปดีมากรถ"],
            ),
            ("ผมหรือกินข้าวเล่น ไปดีมากรถ", ["ผมหรือกินข้าวเล่น", "ไปดีมากรถ"]),
            ("ผมหรือกินข้าวเล่นเกม ไปดีมากรถ", ["ผม", "หรือกินข้าวเล่นเกม ไปดีมากรถ"]),
            ("ผมจึงกินข้าว ไปดีมากรถ", ["ผมจึงกินข้าว", "ไปดีมากรถ"]),
            ("ผมจึงกินข้าวเล่น ไปดีมากรถ", ["ผม", "จึงกินข้าวเล่น ไปดีมากรถ"]),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(
                    self.segmentor.split_into_sentences(text), expected
                )

    def test_conjunction_near_end(self):
        cases = [
            ("ผมกินและกินข้าว ไป", ["ผมกินและกินข้าว", "ไป"]),
            ("ผมกินหรือกิน ไป", ["ผมกินหรือกิน", "ไป"]),
            ("ผมกินจึงกิน ไป", ["ผมกินจึงกิน", "ไป"]),
            ("ผมกินและกินข้าวเล่น", ["ผมกินและกินข้าวเล่น"]),
            ("ผมกินหรือกินข้าวเล่น", ["ผมกินหรือกินข้าวเล่น"]),
            ("ผมกินจึงกินข้าว", ["ผมกินจึงกินข้าว"]),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(
                    self.segmentor.split_into_sentences(text), expected
                )

    def test_middle_cut(self):
        text = " ".join(WORDS * 4)
        sentences = self.segmentor.split_into_sentences(text)
        self.assertEqual(sentences, [text])
        self.assertEqual(
            self.segmentor.split_into_sentences(text, isMiddleCut=True),
            middle_cut(sentences),
        )
        self.assertGreater(
            len(self.segmentor.split_into_sentences(text, isMiddleCut=True)),
            1,
        )

    def test_sent_tokenize_thaisum(self):
        self.assertEqual(
            sent_tokenize("ผมไปโรงเรียนครับ วันนี้อากาศดีค่ะ", engine="thaisum"),
            ["ผมไปโรงเรียนครับ", "วันนี้อากาศดีค่ะ"],
        )
