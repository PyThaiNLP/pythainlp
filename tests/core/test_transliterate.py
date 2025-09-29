# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import unittest

from pythainlp.transliterate import romanize, transliterate

BASIC_TESTS = {
    None: "",
    "": "",
    "abc": "abc",
    "หมอก": "mok",
    "หาย": "hai",
    "แมว": "maeo",
    "เดือน": "duean",
    "ดำ": "dam",
    "ดู": "du",
    "บัว": "bua",
    "กก": "kok",
    "พร": "phon",
    "กร": "kon",
    "กรร": "kan",
    "กรรม": "kam",
    # "กรม": "krom",  # failed
    "ฝ้าย": "fai",
    "นพพร": "nopphon",
    "อัก": "ak",
    # "ทีปกร": "thipakon",  # failed
    # "ธรรพ์": "than",  # failed
    # "ธรรม": "tham",  # failed
    # "มหา": "maha",  # failed
    # "หยาก": "yak",  # failed
    # "อยาก": "yak",  # failed
    # "ยมก": "yamok",  # failed
    # "กลัว": "klua",  # failed
    # "บ้านไร่": "banrai",  # failed
    # "ชารินทร์": "charin",  # failed
}

# these are set of two-syllable words,
# to test if the transliteration/romanization is consistent, say
# romanize(1+2) = romanize(1) + romanize(2)
CONSISTENCY_TESTS = [
    # ("กระจก", "กระ", "จก"),  # failed
    # ("ระเบิด", "ระ", "เบิด"),  # failed
    # ("หยากไย่", "หยาก", "ไย่"),  # failed
    ("ตากใบ", "ตาก", "ใบ"),
    # ("จัดสรร", "จัด", "สรร"),  # failed
]


class TransliterateTestCase(unittest.TestCase):
    def test_romanize(self):
        self.assertEqual(romanize(None), "")
        self.assertEqual(romanize(""), "")
        self.assertEqual(romanize("แมว"), "maeo")

    def test_romanize_royin_basic(self):
        for word, expect in BASIC_TESTS.items():
            self.assertEqual(romanize(word, engine="royin"), expect)

    def test_romanize_royin_consistency(self):
        for word, part1, part2 in CONSISTENCY_TESTS:
            self.assertEqual(
                romanize(word, engine="royin"),
                (
                    romanize(part1, engine="royin")
                    + romanize(part2, engine="royin")
                ),
            )

    def test_romanize_lookup(self):
        # found in v1.4
        self.assertEqual(romanize("บอล", engine="lookup"), "ball")
        self.assertEqual(romanize("บอยแบนด์", engine="lookup"), "boyband")
        self.assertEqual(romanize("กาแล็กซี", engine="lookup"), "galaxy")
        self.assertEqual(romanize("กีย์เซอไรต์", engine="lookup"), "geyserite")
        self.assertEqual(romanize("พลีโอนาสต์", engine="lookup"), "pleonaste")
        self.assertEqual(
            romanize("คาราเมล คาปูชิโน่", engine="lookup"),
            "caramel cappuccino",
        )
        ## found individually, but needs tokenization
        self.assertEqual(
            romanize("คาราเมลคาปูชิโน่", engine="lookup"), "khanamenkhaputino"
        )
        # not found in v1.4
        self.assertEqual(romanize("ภาพยนตร์", engine="lookup"), "phapn")
        self.assertEqual(romanize("แมว", engine="lookup"), "maeo")

    def test_transliterate(self):
        self.assertEqual(transliterate(""), "")
        self.assertIsNotNone(transliterate("คน", engine="iso_11940"))
        self.assertIsNotNone(transliterate("แมว", engine="iso_11940"))

    def test_transliterate_iso11940(self):
        self.assertEqual(
            transliterate("เชียงใหม่", engine="iso_11940"), "echīyngıh̄m̀"
        )
        self.assertEqual(
            transliterate("ภาษาไทย", engine="iso_11940"), "p̣hās̛̄āịthy"
        )
