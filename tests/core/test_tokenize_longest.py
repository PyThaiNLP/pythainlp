# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Characterization tests for pythainlp.tokenize.longest.

Golden data were recorded from the implementation before its refactor.
"""

import unittest
from typing import Any

from pythainlp.tokenize import longest
from pythainlp.util import Trie

_DICT_A: list[str] = [
    "ผม",
    "กิน",
    "ข้าว",
    "เธอ",
    "เล่น",
    "เกม",
    "แมว",
    "บ้าน",
    "โรงเรียน",
    "ไป",
    "กลับ",
    "มาก",
    "ดี",
    "รถ",
    "ถนน",
    "น้ำ",
    "ใหญ่",
    "ประเทศ",
    "ไทย",
    "ประ",
    "เทศ",
    "ภาษา",
    "เฉียบ",
    "พลัน",
    "เฉียบพลัน",
    "ปวด",
    "ก",
    "กก",
    "กา",
    "การ",
    "ทำ",
    "งาน",
    "ๆ",
    "ฯ",
    "ใ",
    "เ",
    "ั",
]
_DICT_G: list[str] = ["ก" * n for n in range(1, 60)] + ["กา", "ข"]
_DICTS: dict[str, list[str]] = {"A": _DICT_A, "G": _DICT_G}

# Each case: text, dictionary name, expected outcome.
_GOLDEN: list[list[Any]] = [
    [
        "日本  กํHelloฯถนน123ใหญ่ๆการ",
        "A",
        ["ok", ["日本", "  ", "กํhello", "ฯ", "ถนน", "123", "ใหญ่ๆ", "การ"]],
    ],
    [
        " น้ำดีงาน123ประเทศกดีปวดไป่ดีไทย!!",
        "A",
        [
            "ok",
            [
                " ",
                "น้ำ",
                "ดี",
                "งาน",
                "123",
                "ประเทศ",
                "ก",
                "ดี",
                "ปวด",
                "ไป่",
                "ดี",
                "ไทย",
                "!!",
            ],
        ],
    ],
    [
        "\r\nฟบ้านํ่  ปวดHelloๆปวด",
        "A",
        ["ok", ["\r", "\nฟ", "บ้านํ่", "  ", "ปวด", "hello", "ๆ", "ปวด"]],
    ],
    [
        "!!เธอ่ึ123มากไปแมวไทยบ้านการเฉียบพลันเฉียบพลันกลับ",
        "A",
        [
            "ok",
            [
                "!!",
                "เธอ่ึ",
                "123",
                "มาก",
                "ไป",
                "แมว",
                "ไทย",
                "บ้าน",
                "การ",
                "เฉียบพลัน",
                "เฉียบพลัน",
                "กลับ",
            ],
        ],
    ],
    [
        "เทศฉฏ123ๅพลัน\r\nพลัน",
        "A",
        ["ok", ["เทศ", "ฉฏ", "123ๅ", "พลัน", "\r\n", "พลัน"]],
    ],
    ["พลันประเฉียบ", "A", ["ok", ["พลัน", "ประ", "เฉียบ"]]],
    ["ดีรถแมวผม123", "A", ["ok", ["ดี", "รถ", "แมว", "ผม", "123"]]],
    [
        "ทำ-xข้าวไทยโรงเรียนก ึ@",
        "A",
        ["ok", ["ทำ", "-", "x", "ข้าว", "ไทย", "โรงเรียน", "ก", " ึ@"]],
    ],
    [
        "ประน้ำ!!ญ\r\nๆ日本ทำผมน้ำญ",
        "A",
        [
            "ok",
            ["ประ", "น้ำ", "!!ญ", "\r\n", "ๆ", "日本", "ทำ", "ผม", "น้ำ", "ญ"],
        ],
    ],
    ["ขมากไป", "A", ["ok", ["ข", "มาก", "ไป"]]],
    ["ฤๅ\t\tๆ", "A", ["ok", ["ฤๅ", "\t\t", "ๆ"]]],
    ["ึ日本ข日本ทำพลัน\nญขํดี", "A", ["ok", ["ึ日本ข日本", "ทำ", "พลัน", "\nญขํดี"]]],
    [
        "การมากเธอกลับมากก日本ํabcบ้านรถํประเทศึ",
        "A",
        [
            "ok",
            [
                "การ",
                "มาก",
                "เธอ",
                "กลับ",
                "มาก",
                "ก",
                "日本ํabc",
                "บ้าน",
                "รถํประ",
                "เทศึ",
            ],
        ],
    ],
    [
        "-x\tHelloผมabc\nกก",
        "A",
        ["ok", ["-", "x", "\t", "hello", "ผม", "abc", "\n", "กก"]],
    ],
    ["กลับกินงานข้าว", "A", ["ok", ["กลับ", "กิน", "งาน", "ข้าว"]]],
    ["มากเฉียบๆฝ์ผม", "A", ["ok", ["มาก", "เฉียบๆ", "ฝ์", "ผม"]]],
    [
        "ถนนเทศ!!ํกาๆขึ์ดี@ประเทศข้าว",
        "A",
        ["ok", ["ถนน", "เทศ", "!!ํกาๆขึ์", "ดี", "@", "ประเทศ", "ข้าว"]],
    ],
    ["ฯผมข้าวๆเธอฤๅกก", "A", ["ok", ["ฯ", "ผม", "ข้าวๆ", "เธอ", "ฤๅ", "กก"]]],
    [
        "ๆภาษาเล่นโรงเรียนกกเฉียบํ  ",
        "A",
        ["ok", ["ๆ", "ภาษา", "เล่น", "โรงเรียน", "กก", "เฉียบํ", "  "]],
    ],
    [
        "การประเทศผมภาษาเกมกลับแมว",
        "A",
        ["ok", ["การ", "ประเทศ", "ผม", "ภาษา", "เกม", "กลับ", "แมว"]],
    ],
    [
        "ญประ1,234.5ภาษาการ",
        "A",
        ["ok", ["ญ", "ประ", "1", ",", "234", ".", "5", "ภาษา", "การ"]],
    ],
    [
        "123ภาษา  ภาษาข่โรงเรียนเธอญ",
        "A",
        ["ok", ["123", "ภาษา", "  ", "ภาษา", "ข่", "โรงเรียน", "เธอ", "ญ"]],
    ],
    [
        "ไปดีเฉียบแมวๆเล่นทำกินถนนกกเล่นabc",
        "A",
        [
            "ok",
            [
                "ไป",
                "ดี",
                "เฉียบ",
                "แมวๆ",
                "เล่น",
                "ทำ",
                "กิน",
                "ถนน",
                "กก",
                "เล่น",
                "abc",
            ],
        ],
    ],
    [
        "พลันๆฯ่ฤๅไทยกาเทศน้ำ",
        "A",
        ["ok", ["พลันๆ", "ฯ่ฤๅ", "ไทย", "กา", "เทศ", "น้ำ"]],
    ],
    ["ๅญ", "A", ["ok", ["ๅญ"]]],
    [
        "ฟโรงเรียนเธอๆไปเธอรถ123ข้าว",
        "A",
        ["ok", ["ฟ", "โรงเรียน", "เธอๆ", "ไป", "เธอ", "รถ", "123", "ข้าว"]],
    ],
    [
        "รถฟโรงเรียน  123มากกินํภาษาเล่นแมวประเล่นมาก",
        "A",
        [
            "ok",
            [
                "รถ",
                "ฟ",
                "โรงเรียน",
                "  ",
                "123",
                "มาก",
                "กินํภาษา",
                "เล่น",
                "แมว",
                "ประ",
                "เล่น",
                "มาก",
            ],
        ],
    ],
    [" ผมแมวกิน ใหญ่", "A", ["ok", [" ", "ผม", "แมว", "กิน", " ", "ใหญ่"]]],
]


class LongestGoldenTestCase(unittest.TestCase):
    def test_segment_golden(self):
        for text, dict_name, expected in _GOLDEN:
            with self.subTest(text=text, dict=dict_name):
                trie = Trie(_DICTS[dict_name])
                self.assertEqual(expected[0], "ok")
                self.assertEqual(longest.segment(text, trie), expected[1])

    def test_empty_and_wrong_type(self):
        trie = Trie(_DICT_A)
        for value in (None, "", 123, ["ก"]):
            with self.subTest(value=value):
                self.assertEqual(longest.segment(value, trie), [])  # type: ignore[arg-type]

    def test_tokenizer_class(self):
        tokenizer = longest.LongestMatchTokenizer(Trie(_DICT_A))
        self.assertEqual(tokenizer.tokenize("ผมกินข้าว"), ["ผม", "กิน", "ข้าว"])
        self.assertEqual(tokenizer.tokenize(""), [])

    def test_front_dependent_character_list(self):
        # BUG-LEDGER: longest-front-dep-typo
        # _FRONT_DEP_CHAR holds "า " (with a space), so an unknown "า"
        # never joins the previous token by the front-dependent rule,
        # while "ะ" does.
        tokenizer: Any = longest.LongestMatchTokenizer(Trie(["ก", "ข"]))
        self.assertEqual(tokenizer.tokenize("กา"), ["ก", "า"])
        self.assertEqual(tokenizer.tokenize("กะ"), ["กะ"])
        self.assertIn("า ", longest._FRONT_DEP_CHAR)
        self.assertNotIn("า", longest._FRONT_DEP_CHAR)


class LongestDefaultDictTestCase(unittest.TestCase):
    def test_default_dict_and_cache(self):
        text = "ผมกินข้าว"
        first = longest.segment(text)
        self.assertEqual(longest.segment(text), first)
        self.assertEqual("".join(first), text)


if __name__ == "__main__":
    unittest.main()
