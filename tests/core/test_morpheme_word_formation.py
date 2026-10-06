# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Characterization tests for pythainlp.morpheme.word_formation.nighit.

Golden cases were recorded from the code before the complexity refactor.
"""

from __future__ import annotations

import unittest
from typing import Any

from pythainlp import thai_consonants
from pythainlp.morpheme import nighit

# First consonant of w2 -> consonant added after "สั".
# None means the consonant is not supported and an error is raised.
CONSONANT_TO_ENDING: dict[str, Any] = {
    "ก": "ง",
    "ข": "ง",
    "ฃ": None,
    "ค": "ง",
    "ฅ": None,
    "ฆ": None,
    "ง": "ง",
    "จ": "ญ",
    "ฉ": "ญ",
    "ช": "ง",
    "ซ": None,
    "ฌ": "ญ",
    "ญ": None,
    "ฎ": "ณ",
    "ฏ": None,
    "ฐ": "ณ",
    "ฑ": "ณ",
    "ฒ": None,
    "ณ": "ณ",
    "ด": "น",
    "ต": None,
    "ถ": "น",
    "ท": "น",
    "ธ": "น",
    "น": "น",
    "บ": None,
    "ป": "ม",
    "ผ": "ม",
    "ฝ": None,
    "พ": "ม",
    "ฟ": None,
    "ภ": "ม",
    "ม": None,
    "ย": "ง",
    "ร": "ง",
    "ล": "ง",
    "ว": "ง",
    "ศ": "ง",
    "ษ": "ง",
    "ส": "ง",
    "ห": "ง",
    "ฬ": "ง",
    "อ": None,
    "ฮ": None,
}

# (w1, w2, outcome)
# The outcome is ["ok", result] or ["exc", exception name, message].
EXTRA_GOLDEN: list[list[Any]] = [
    ["สํ", "คีต", ["ok", "สังคีต"]],
    ["สํ ", "คีต ", ["ok", "สังคีต"]],
    ["", "คีต", ["ok", "คีต"]],
    ["สํ", "", ["ok", "สํ"]],
    [" ", " ", ["ok", ""]],
    ["  ", "x", ["ok", "x"]],
    ["ab", "คา", ["ok", "aังคา"]],
    [
        "abc",
        "คา",
        ["exc", "NotImplementedError", "The function doesn't support abc."],
    ],
    [
        "สํ",
        "abc",
        ["exc", "ValueError", "w2 'abc' contains no Thai consonants."],
    ],
    ["สํ", "1ก", ["ok", "สัง1ก"]],
    [
        "ก",
        "ก",
        ["exc", "NotImplementedError", "The function doesn't support ก."],
    ],
    ["กํ", "าก", ["ok", "กังาก"]],
    ["สํ", "เกาะ", ["ok", "สังเกาะ"]],
    ["สํ", "   ", ["ok", "สํ"]],
    ["x", "", ["ok", "x"]],
    [None, "ก", ["exc", "TypeError", "Both w1 and w2 must be strings."]],
    ["สํ", 1, ["exc", "TypeError", "Both w1 and w2 must be strings."]],
    [1, 2, ["exc", "TypeError", "Both w1 and w2 must be strings."]],
    ["สํ", None, ["exc", "TypeError", "Both w1 and w2 must be strings."]],
    ["สํ", "คา\n", ["ok", "สังคา"]],
    ["\tสํ", "\u200bก", ["ok", "สัง\u200bก"]],
]

EXCEPTIONS = {
    "TypeError": TypeError,
    "ValueError": ValueError,
    "NotImplementedError": NotImplementedError,
}


class NighitCharacterizationTestCase(unittest.TestCase):
    def test_every_consonant(self) -> None:
        self.assertEqual(set(CONSONANT_TO_ENDING), set(thai_consonants))
        for consonant, ending in CONSONANT_TO_ENDING.items():
            w2 = "เ" + consonant + "า"
            with self.subTest(consonant=consonant):
                if ending is None:
                    with self.assertRaises(NotImplementedError) as ctx:
                        nighit("สํ", w2)
                    self.assertEqual(
                        str(ctx.exception),
                        "\n        The function doesn't support "
                        f"สํ and {w2}.\n        ",
                    )
                else:
                    self.assertEqual(nighit("สํ", w2), "สั" + ending + w2)

    def test_golden_cases(self) -> None:
        for w1, w2, expected in EXTRA_GOLDEN:
            with self.subTest(w1=w1, w2=w2):
                if expected[0] == "exc":
                    with self.assertRaises(EXCEPTIONS[expected[1]]) as ctx:
                        nighit(w1, w2)
                    self.assertEqual(str(ctx.exception), expected[2])
                else:
                    self.assertEqual(nighit(w1, w2), expected[1])

    # BUG-LEDGER: nighit-consonant-table
    def test_bug_incomplete_consonant_table(self) -> None:
        """The consonant ช is listed twice, so it maps to ง, not ญ.

        The consonant ต is missing. Expected: ช maps to ญ and ต maps to น
        (the same class as ด, ถ, ท, ธ, น).
        """
        self.assertEqual(nighit("สํ", "ชา"), "สังชา")
        with self.assertRaises(NotImplementedError):
            nighit("สํ", "ตา")

    # BUG-LEDGER: nighit-w1-check
    def test_bug_w1_check_accepts_any_two_character_word(self) -> None:
        """A two-character w1 passes without ending in nighit (ํ)."""
        self.assertEqual(nighit("ab", "คา"), "aังคา")
        with self.assertRaises(NotImplementedError):
            nighit("ก", "คา")


if __name__ == "__main__":
    unittest.main()
