# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Characterization tests for pythainlp.tokenize.multi_cut.

Golden data were recorded from the implementation before its refactor.
"""

import unittest
from typing import Any

from pythainlp.tokenize import multi_cut
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

# Each case: text, dictionary name, expected outcome of
# [(token, multi, unique, in_dict) list, find_all_segment result].
_GOLDEN: list[list[Any]] = [
    [
        "กกกกฟโรงเรียน  ฤๅ",
        "A",
        [
            "ok",
            [
                [
                    [
                        "กกกก",
                        ["ก/ก/ก/ก", "ก/ก/กก", "ก/กก/ก", "กก/ก/ก", "กก/กก"],
                        False,
                        True,
                    ],
                    ["ฟ", ["ฟ"], True, False],
                    ["โรงเรียน", ["โรงเรียน"], True, True],
                    ["  ", ["  "], True, False],
                    ["ฤๅ", ["ฤๅ"], True, False],
                ],
                [
                    "ก|ก|ก|ก|ฟ|โรงเรียน|  |ฤๅ|",
                    "ก|ก|กก|ฟ|โรงเรียน|  |ฤๅ|",
                    "ก|กก|ก|ฟ|โรงเรียน|  |ฤๅ|",
                    "กก|ก|ก|ฟ|โรงเรียน|  |ฤๅ|",
                    "กก|กก|ฟ|โรงเรียน|  |ฤๅ|",
                ],
            ],
        ],
    ],
    ["ฮ", "A", ["ok", [[["ฮ", ["ฮ"], True, False]], ["ฮ|"]]]],
    [
        "น้ำๆการกินกลับฯ\tฯ",
        "A",
        [
            "ok",
            [
                [
                    ["น้ำ", ["น้ำ"], True, True],
                    ["ๆ", ["ๆ"], True, True],
                    ["การ", ["การ"], True, True],
                    ["กิน", ["กิน"], True, True],
                    ["กลับ", ["กลับ"], True, True],
                    ["ฯ", ["ฯ"], True, True],
                    ["\t", ["\t"], True, False],
                    ["ฯ", ["ฯ"], True, True],
                ],
                ["น้ำ|ๆ|การ|กิน|กลับ|ฯ|\t|ฯ|"],
            ],
        ],
    ],
    [
        "abcใหญ่งานไปฉฏกิน!!เธอ",
        "A",
        [
            "ok",
            [
                [
                    ["abc", ["abc"], True, False],
                    ["ใหญ่", ["ใหญ่"], True, True],
                    ["งาน", ["งาน"], True, True],
                    ["ไป", ["ไป"], True, True],
                    ["ฉฏ", ["ฉฏ"], True, False],
                    ["กิน", ["กิน"], True, True],
                    ["!!", ["!!"], True, False],
                    ["เธอ", ["เธอ"], True, True],
                ],
                ["abc|ใหญ่|งาน|ไป|ฉฏ|กิน|!!|เธอ|"],
            ],
        ],
    ],
    [
        "ภาษาเกม@ข้าว",
        "A",
        [
            "ok",
            [
                [
                    ["ภาษา", ["ภาษา"], True, True],
                    ["เกม", ["เกม"], True, True],
                    ["@", ["@"], True, False],
                    ["ข้าว", ["ข้าว"], True, True],
                ],
                ["ภาษา|เกม|@|ข้าว|"],
            ],
        ],
    ],
    [
        "ข้าวเธอ",
        "A",
        [
            "ok",
            [
                [["ข้าว", ["ข้าว"], True, True], ["เธอ", ["เธอ"], True, True]],
                ["ข้าว|เธอ|"],
            ],
        ],
    ],
    [
        "ฤๅเทศไปกก",
        "A",
        [
            "ok",
            [
                [
                    ["ฤๅ", ["ฤๅ"], True, False],
                    ["เทศ", ["เทศ"], True, True],
                    ["ไป", ["ไป"], True, True],
                    ["กก", ["ก/ก", "กก"], False, True],
                ],
                ["ฤๅ|เทศ|ไป|ก|ก|", "ฤๅ|เทศ|ไป|กก|"],
            ],
        ],
    ],
    ["\n", "A", ["ok", [[["\n", ["\n"], True, False]], ["\n|"]]]],
    [
        "บ้านไป日本เล่นปวดเธอึเกมกิน",
        "A",
        [
            "ok",
            [
                [
                    ["บ้าน", ["บ้าน"], True, True],
                    ["ไป", ["ไป"], True, True],
                    ["日本", ["日本"], True, False],
                    ["เล่น", ["เล่น"], True, True],
                    ["ปวด", ["ปวด"], True, True],
                    ["เธอ", ["เธอ"], True, True],
                    ["ึ", ["ึ"], True, False],
                    ["เกม", ["เกม"], True, True],
                    ["กิน", ["กิน"], True, True],
                ],
                ["บ้าน|ไป|日本|เล่น|ปวด|เธอ|ึ|เกม|กิน|"],
            ],
        ],
    ],
    [
        "!!!!123",
        "A",
        [
            "ok",
            [
                [
                    ["!!!!", ["!!!!"], True, False],
                    ["123", ["123"], True, False],
                ],
                ["!!!!|123|"],
            ],
        ],
    ],
    [
        "บ้าน123ญน้ำบ้านฮฯรถเล่น",
        "A",
        [
            "ok",
            [
                [
                    ["บ้าน", ["บ้าน"], True, True],
                    ["123", ["123"], True, False],
                    ["ญ", ["ญ"], True, False],
                    ["น้ำ", ["น้ำ"], True, True],
                    ["บ้าน", ["บ้าน"], True, True],
                    ["ฮ", ["ฮ"], True, False],
                    ["ฯ", ["ฯ"], True, True],
                    ["รถ", ["รถ"], True, True],
                    ["เล่น", ["เล่น"], True, True],
                ],
                ["บ้าน|123|ญ|น้ำ|บ้าน|ฮ|ฯ|รถ|เล่น|"],
            ],
        ],
    ],
    [
        "์เกมๅเกม\r\nน้ำๅผมใหญ่",
        "A",
        [
            "ok",
            [
                [
                    ["์", ["์"], True, False],
                    ["เกม", ["เกม"], True, True],
                    ["ๅ", ["ๅ"], True, False],
                    ["เกม", ["เกม"], True, True],
                    ["\r\n", ["\r\n"], True, False],
                    ["น้ำ", ["น้ำ"], True, True],
                    ["ๅ", ["ๅ"], True, False],
                    ["ผม", ["ผม"], True, True],
                    ["ใหญ่", ["ใหญ่"], True, True],
                ],
                ["์|เกม|ๅ|เกม|\r\n|น้ำ|ๅ|ผม|ใหญ่|"],
            ],
        ],
    ],
    [
        "-xญข้าวบ้านเฉียบผมน้ำ",
        "A",
        [
            "ok",
            [
                [
                    ["-x", ["-x"], True, False],
                    ["ญ", ["ญ"], True, False],
                    ["ข้าว", ["ข้าว"], True, True],
                    ["บ้าน", ["บ้าน"], True, True],
                    ["เฉียบ", ["เฉียบ"], True, True],
                    ["ผม", ["ผม"], True, True],
                    ["น้ำ", ["น้ำ"], True, True],
                ],
                ["-x|ญ|ข้าว|บ้าน|เฉียบ|ผม|น้ำ|"],
            ],
        ],
    ],
    [
        "กา@ฟกกบ้านงานฤๅ",
        "A",
        [
            "ok",
            [
                [
                    ["กา", ["กา"], True, True],
                    ["@ฟ", ["@ฟ"], True, False],
                    ["กก", ["ก/ก", "กก"], False, True],
                    ["บ้าน", ["บ้าน"], True, True],
                    ["งาน", ["งาน"], True, True],
                    ["ฤๅ", ["ฤๅ"], True, False],
                ],
                ["กา|@ฟ|ก|ก|บ้าน|งาน|ฤๅ|", "กา|@ฟ|กก|บ้าน|งาน|ฤๅ|"],
            ],
        ],
    ],
    [
        "ทำเฉียบแมวฤๅฤๅเธอขบ้านเฉียบพลัน",
        "A",
        [
            "ok",
            [
                [
                    ["ทำ", ["ทำ"], True, True],
                    ["เฉียบ", ["เฉียบ"], True, True],
                    ["แมว", ["แมว"], True, True],
                    ["ฤๅฤๅ", ["ฤๅฤๅ"], True, False],
                    ["เธอ", ["เธอ"], True, True],
                    ["ข", ["ข"], True, False],
                    ["บ้าน", ["บ้าน"], True, True],
                    ["เฉียบพลัน", ["เฉียบ/พลัน", "เฉียบพลัน"], False, True],
                ],
                [
                    "ทำ|เฉียบ|แมว|ฤๅฤๅ|เธอ|ข|บ้าน|เฉียบ|พลัน|",
                    "ทำ|เฉียบ|แมว|ฤๅฤๅ|เธอ|ข|บ้าน|เฉียบพลัน|",
                ],
            ],
        ],
    ],
    [
        "เธอไป",
        "A",
        [
            "ok",
            [
                [["เธอ", ["เธอ"], True, True], ["ไป", ["ไป"], True, True]],
                ["เธอ|ไป|"],
            ],
        ],
    ],
    [
        "\r\nประเทศ",
        "A",
        [
            "ok",
            [
                [
                    ["\r\n", ["\r\n"], True, False],
                    ["ประเทศ", ["ประ/เทศ", "ประเทศ"], False, True],
                ],
                ["\r\n|ประ|เทศ|", "\r\n|ประเทศ|"],
            ],
        ],
    ],
    [
        "มากเฉียบ",
        "A",
        [
            "ok",
            [
                [["มาก", ["มาก"], True, True], ["เฉียบ", ["เฉียบ"], True, True]],
                ["มาก|เฉียบ|"],
            ],
        ],
    ],
    ["่@", "A", ["ok", [[["่@", ["่@"], True, False]], ["่@|"]]]],
    [
        "ไปน้ำๅ",
        "A",
        [
            "ok",
            [
                [
                    ["ไป", ["ไป"], True, True],
                    ["น้ำ", ["น้ำ"], True, True],
                    ["ๅ", ["ๅ"], True, False],
                ],
                ["ไป|น้ำ|ๅ|"],
            ],
        ],
    ],
    [
        "เทศ  ๆ\nงาน",
        "A",
        [
            "ok",
            [
                [
                    ["เทศ", ["เทศ"], True, True],
                    ["  ", ["  "], True, False],
                    ["ๆ", ["ๆ"], True, True],
                    ["\n", ["\n"], True, False],
                    ["งาน", ["งาน"], True, True],
                ],
                ["เทศ|  |ๆ|\n|งาน|"],
            ],
        ],
    ],
    [
        "เฉียบๆถนน",
        "A",
        [
            "ok",
            [
                [
                    ["เฉียบ", ["เฉียบ"], True, True],
                    ["ๆ", ["ๆ"], True, True],
                    ["ถนน", ["ถนน"], True, True],
                ],
                ["เฉียบ|ๆ|ถนน|"],
            ],
        ],
    ],
    [
        " เฉียบพลันแมวๅถนน  ญ",
        "A",
        [
            "ok",
            [
                [
                    [" ", [" "], True, False],
                    ["เฉียบพลัน", ["เฉียบ/พลัน", "เฉียบพลัน"], False, True],
                    ["แมว", ["แมว"], True, True],
                    ["ๅ", ["ๅ"], True, False],
                    ["ถนน", ["ถนน"], True, True],
                    ["  ", ["  "], True, False],
                    ["ญ", ["ญ"], True, False],
                ],
                [" |เฉียบ|พลัน|แมว|ๅ|ถนน|  |ญ|", " |เฉียบพลัน|แมว|ๅ|ถนน|  |ญ|"],
            ],
        ],
    ],
    [
        "กลับ่ใหญ่ทำ1,234.5",
        "A",
        [
            "ok",
            [
                [
                    ["กลับ", ["กลับ"], True, True],
                    ["่", ["่"], True, False],
                    ["ใหญ่", ["ใหญ่"], True, True],
                    ["ทำ", ["ทำ"], True, True],
                    ["1,234.5", ["1,234.5"], True, False],
                ],
                ["กลับ|่|ใหญ่|ทำ|1,234.5|"],
            ],
        ],
    ],
    [
        "ภาษา日本ญข้าว์",
        "A",
        [
            "ok",
            [
                [
                    ["ภาษา", ["ภาษา"], True, True],
                    ["日本ญ", ["日本ญ"], True, False],
                    ["ข้าว", ["ข้าว"], True, True],
                    ["์", ["์"], True, False],
                ],
                ["ภาษา|日本ญ|ข้าว|์|"],
            ],
        ],
    ],
    [
        "\r\nไปทำ",
        "A",
        [
            "ok",
            [
                [
                    ["\r\n", ["\r\n"], True, False],
                    ["ไป", ["ไป"], True, True],
                    ["ทำ", ["ทำ"], True, True],
                ],
                ["\r\n|ไป|ทำ|"],
            ],
        ],
    ],
]


class MultiCutGoldenTestCase(unittest.TestCase):
    def test_multicut_golden(self):
        for text, dict_name, expected in _GOLDEN:
            with self.subTest(text=text, dict=dict_name):
                trie = Trie(_DICTS[dict_name])
                segs = list(multi_cut._multicut(text, trie))
                got = [[str(s), s.multi, s.unique, s.in_dict] for s in segs]
                self.assertEqual(expected[0], "ok")
                self.assertEqual(got, expected[1][0])
                self.assertEqual(
                    multi_cut.find_all_segment(text, trie), expected[1][1]
                )
                self.assertEqual(
                    multi_cut.segment(text, trie), [str(s) for s in segs]
                )

    def test_empty_and_wrong_type(self):
        trie = Trie(_DICT_A)
        for func in (multi_cut.segment, multi_cut.find_all_segment):
            for value in (None, "", 123, ["ก"]):
                with self.subTest(func=func.__name__, value=value):
                    self.assertEqual(func(value, trie), [])  # type: ignore[arg-type]

    def test_multicut_is_lazy(self):
        gen = multi_cut._multicut("ผมกินข้าว", Trie(_DICT_A))
        self.assertEqual(str(next(gen)), "ผม")

    def test_lattice_string(self):
        single = multi_cut.LatticeString("กา")
        self.assertTrue(single.unique)
        self.assertEqual(single.multi, ["กา"])
        multi = multi_cut.LatticeString("กา", ["ก/า", "กา"], in_dict=False)
        self.assertFalse(multi.unique)
        self.assertFalse(multi.in_dict)
        self.assertEqual(multi.multi, ["ก/า", "กา"])
        one = multi_cut.LatticeString("กา", ["กา"])
        self.assertTrue(one.unique)

    def test_combine_empty(self):
        self.assertEqual(list(multi_cut._combine([])), [""])

    def test_mmcut(self):
        got: Any = multi_cut.mmcut("ผมกินข้าวabc")
        self.assertEqual("".join(got), "ผมกินข้าวabc")


class MultiCutDefaultDictTestCase(unittest.TestCase):
    def test_default_dict(self):
        text = "ผมกินข้าว"
        for func in (multi_cut.segment, multi_cut.find_all_segment):
            with self.subTest(func=func.__name__):
                self.assertTrue(func(text))
        self.assertEqual("".join(multi_cut.segment(text)), text)
        self.assertEqual(
            "".join(str(s) for s in multi_cut._multicut(text)), text
        )


if __name__ == "__main__":
    unittest.main()
