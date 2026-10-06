# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Characterization tests for pythainlp.util.thai.count_thai_chars.

Golden data was recorded from the pre-refactor implementation.
"""

import unittest

from pythainlp.util import count_thai_chars

_KEYS = (
    "vowels",
    "lead_vowels",
    "follow_vowels",
    "above_vowels",
    "below_vowels",
    "consonants",
    "tonemarks",
    "signs",
    "thai_digits",
    "punctuations",
    "non_thai",
)

# Counted categories (besides "vowels") -> characters, for every
# character in U+0000..U+02FF, U+0E00..U+0E7F, and a few others.
# "vowels" is counted in addition to the vowel sub-categories.
_SINGLE_CHAR = [
    (
        ("non_thai",),
        (
            " "
            "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x00\n"
            "é\u200b—一\u0e80"
        ),
    ),
    (("consonants",), "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ"),
    (("vowels", "non_thai"), "ฤฦ"),
    (("signs",), "ฯฺๆ์๎"),
    (("vowels", "follow_vowels"), "ะาำๅ"),
    (("vowels", "above_vowels"), "ัิีึื็ํ"),
    (("vowels", "below_vowels"), "ุู"),
    (("vowels", "lead_vowels"), "เแโใไ"),
    (("tonemarks",), "่้๊๋"),
    (("punctuations",), "๏๚๛"),
    (("thai_digits",), "๐๑๒๓๔๕๖๗๘๙"),
]

# (text, counts in the order of _KEYS)
_TEXTS = [
    ("ทดสอบภาษาไทย", (3, 1, 2, 0, 0, 9, 0, 0, 0, 0, 0)),
    ("", (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    ("สวัสดี ๑๒๓ abc ฯ ๏ ่ ฤ", (3, 0, 0, 2, 0, 4, 1, 1, 3, 1, 10)),
    ("ฤๅษี", (3, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1)),
    (["ก", "ที", "", "ฤ"], (2, 1, 0, 0, 0, 1, 0, 0, 0, 0, 2)),
    ("เเปลก", (2, 2, 0, 0, 0, 3, 0, 0, 0, 0, 0)),
    ("ๆ๛ๅ", (1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0)),
    (
        "กกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกก",
        (0, 0, 0, 0, 0, 50, 0, 0, 0, 0, 0),
    ),
    ("a b\tc\n", (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6)),
    ("กิ่ง ก้าน ๆ ฯ", (2, 0, 1, 1, 0, 4, 2, 2, 0, 0, 3)),
]


def _counts(text: object) -> tuple[int, ...]:
    result = count_thai_chars(text)  # type: ignore[arg-type]
    return tuple(result[key] for key in _KEYS)


class CountThaiCharsTestCase(unittest.TestCase):
    def test_keys_and_order(self) -> None:
        self.assertEqual(tuple(count_thai_chars("")), _KEYS)
        self.assertEqual(_counts(""), (0,) * 11)

    def test_single_chars(self) -> None:
        for categories, chars in _SINGLE_CHAR:
            expected = tuple(int(key in categories) for key in _KEYS)
            for char in chars:
                with self.subTest(char=char, categories=categories):
                    self.assertEqual(_counts(char), expected)

    def test_texts(self) -> None:
        for text, expected in _TEXTS:
            with self.subTest(text=text):
                self.assertEqual(_counts(text), expected)

    def test_length_threshold(self) -> None:
        # Short and long inputs use different code paths; results must match.
        unit = "กิ่ง ก้าน ๆ ฯฤฦ๑ a"
        for length in (63, 64, 65, 200):
            text = (unit * 20)[:length]
            expected = [0] * 11
            for char in text:
                for index, count in enumerate(_counts(char)):
                    expected[index] += count
            with self.subTest(length=length):
                self.assertEqual(_counts(text), tuple(expected))
                self.assertEqual(tuple(count_thai_chars(text)), _KEYS)

    def test_docstring_example(self) -> None:
        self.assertEqual(
            count_thai_chars("ทดสอบภาษาไทย"),
            {
                "vowels": 3,
                "lead_vowels": 1,
                "follow_vowels": 2,
                "above_vowels": 0,
                "below_vowels": 0,
                "consonants": 9,
                "tonemarks": 0,
                "signs": 0,
                "thai_digits": 0,
                "punctuations": 0,
                "non_thai": 0,
            },
        )

    # BUG-LEDGER: count-thai-chars-double
    def test_bug_chars_counted_twice(self) -> None:
        # Expected: "ฤ" and "ฦ" are counted once. Currently they count
        # as "vowels" and also as "non_thai".
        for char in "ฤฦ":
            with self.subTest(char=char):
                result = count_thai_chars(char)
                self.assertEqual(result["vowels"], 1)
                self.assertEqual(result["non_thai"], 1)
        # Every other vowel is counted in "vowels" and in one sub-category,
        # and an empty string element counts as "vowels" and "lead_vowels".
        self.assertEqual(_counts(["", "ฤ"]), (2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1))

    def test_invalid_input(self) -> None:
        for value in (None, 5):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    count_thai_chars(value)  # type: ignore[arg-type]
        for bad in ([1], b"ab", ["ก", None]):
            with self.subTest(bad=bad):
                with self.assertRaises(TypeError):
                    count_thai_chars(bad)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
