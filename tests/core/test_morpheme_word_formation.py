# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Characterization tests for pythainlp.morpheme.word_formation.nighit.

Golden cases were recorded from the code before the complexity refactor.
"""

from __future__ import annotations

import hashlib
import unittest
from typing import Any

from pythainlp import thai_consonants
from pythainlp.morpheme import nighit
from pythainlp.morpheme.word_formation import _NIGHIT_ENDINGS

# First consonant of w2 -> consonant added after "สั".
# Rows follow the vagga rule. ฎ and ด are kept for backward compatibility
# (they are not in the vagga rule); ย ร ล ว ศ ษ ส ห ฬ map to ง.
# None means the consonant is not supported and an error is raised.
CONSONANT_TO_ENDING: dict[str, Any] = {
    "ก": "ง",
    "ข": "ง",
    "ฃ": None,
    "ค": "ง",
    "ฅ": None,
    "ฆ": "ง",
    "ง": "ง",
    "จ": "ญ",
    "ฉ": "ญ",
    "ช": "ญ",
    "ซ": None,
    "ฌ": "ญ",
    "ญ": "ญ",
    "ฎ": "ณ",
    "ฏ": "ณ",
    "ฐ": "ณ",
    "ฑ": "ณ",
    "ฒ": "ณ",
    "ณ": "ณ",
    "ด": "น",
    "ต": "น",
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
    "ม": "ม",
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
    [
        "ab",
        "คา",
        ["exc", "NotImplementedError", "The function doesn't support ab."],
    ],
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

NIE = "NotImplementedError"
VE = "ValueError"
NO_CONSONANT = "w2 {!r} contains no Thai consonants."
UNSUPPORTED = "The function doesn't support {}."

# Adversarial rows whose outcome is the same before and after the fix.
# Exception types and messages are current behavior, not a promise.
ADVERSARIAL: list[list[Any]] = [
    ["", "ก", ["ok", "ก"]],
    ["สํ", "ั", ["exc", VE, NO_CONSONANT.format("ั")]],
    ["สํ", "เ", ["exc", VE, NO_CONSONANT.format("เ")]],
    ["สํ", "โ", ["exc", VE, NO_CONSONANT.format("โ")]],
    ["สํ", "ำ", ["exc", VE, NO_CONSONANT.format("ำ")]],
    ["สํ", "๑๒๓", ["exc", VE, NO_CONSONANT.format("๑๒๓")]],
    ["สํ", "ｋา", ["exc", VE, NO_CONSONANT.format("ｋา")]],
    ["สํ", "ꙮ", ["exc", VE, NO_CONSONANT.format("ꙮ")]],
    ["สํ", "\u200b", ["exc", VE, NO_CONSONANT.format("\u200b")]],
    ["สํ", "ะก", ["ok", "สังะก"]],
    ["สํ", "ก้", ["ok", "สังก้"]],
    ["สํ", "\u200bก", ["ok", "สัง\u200bก"]],
    ["สํ", "ก\u200b", ["ok", "สังก\u200b"]],
    ["สํ", "ากา", ["ok", "สังากา"]],
    ["สํ", "คายคา" * 2000, ["ok", "สัง" + "คายคา" * 2000]],
    ["สํ", "ก" * 5000, ["ok", "สัง" + "ก" * 5000]],
    ["\tสํ ", "คา", ["ok", "สังคา"]],
    [
        "กขํ",
        "ซา",
        [
            "exc",
            NIE,
            # BUG-LEDGER: nighit-message-format
            # Expected: a one-line message.
            "\n        The function doesn't support กขํ and ซา.\n        ",
        ],
    ],
    ["abc", "123", ["exc", NIE, UNSUPPORTED.format("abc")]],
    ["สําา", "คา", ["exc", NIE, UNSUPPORTED.format("สําา")]],
    ["ก", "123", ["exc", NIE, UNSUPPORTED.format("ก")]],
    ["ก", "\u200b", ["exc", NIE, UNSUPPORTED.format("ก")]],
    ["", "", ["ok", ""]],
    ["", "\u200b", ["ok", "\u200b"]],
    ["\u3000", "ก", ["ok", "ก"]],
    ["สํ", "\u3000ก", ["ok", "สังก"]],
]

# Regression: a w1 that does not end with nighit is rejected,
# even when it has two characters (formerly accepted).
W1_REJECTED: list[list[Any]] = [
    ["ab", "คา", ["exc", NIE, UNSUPPORTED.format("ab")]],
    ["ab", "123", ["exc", NIE, UNSUPPORTED.format("ab")]],
    ["ab", "ซา", ["exc", NIE, UNSUPPORTED.format("ab")]],
    ["สั", "คา", ["exc", NIE, UNSUPPORTED.format("สั")]],
    ["กข", "คา", ["exc", NIE, UNSUPPORTED.format("กข")]],
    ["12", "ก", ["exc", NIE, UNSUPPORTED.format("12")]],
    ["ๆก", "ก", ["exc", NIE, UNSUPPORTED.format("ๆก")]],
    ["ｓｔ", "ก", ["exc", NIE, UNSUPPORTED.format("ｓｔ")]],
    ["ํก", "คา", ["exc", NIE, UNSUPPORTED.format("ํก")]],
    ["สํา", "คา", ["exc", NIE, UNSUPPORTED.format("สํา")]],
]

# Outputs of w1 values with extra characters before nighit are not pinned;
# see test_w1_prefix_dropped.
# SHA-256 of the outcomes of nighit(w1, w2) over the grid below,
# recorded before the fix. Rows with changed behavior are excluded:
# the consonants ช ฆ ญ ฏ ฒ ต ม and the two-character w1 without nighit.
GRID_W1 = (
    "", "  ", "สํ", "กํ", "สํ ", "\tสํ", "สําา", "abc", "ก",
)  # fmt: skip
GRID_W2 = (
    "", "  ", "คา", "ากา", "ั", "ก้", "เ", "123", "๑๒๓", "ｋ", "\u200b",
    "\u200bก", "ก\u200b", "ะก", "โ", "ำ", "กกกกก", "ก\n", "abc", "ꙮ",
    "ｋา", "ฯ", "สํ", "คา" * 2000,
)  # fmt: skip
CHANGED_CONSONANTS = frozenset("ชฆญฏฒตม")
GRID_SIZE = 549
GRID_DIGEST = (
    "37ef3bd348e6a35d3d326f920016b426d5b58e506de2f6b93c4339f9648ccaad"
)


def _outcome(w1: str, w2: str) -> tuple[Any, ...]:
    try:
        return ("ok", nighit(w1, w2))
    except Exception as exc:
        return ("exc", type(exc).__name__, str(exc))


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
                    # BUG-LEDGER: nighit-message-format
                    self.assertEqual(
                        str(ctx.exception),
                        "\n        The function doesn't support "
                        f"สํ and {w2}.\n        ",
                    )
                else:
                    self.assertEqual(nighit("สํ", w2), "สั" + ending + w2)

    def test_golden_cases(self) -> None:
        for w1, w2, expected in EXTRA_GOLDEN + ADVERSARIAL + W1_REJECTED:
            with self.subTest(w1=w1, w2=w2):
                if expected[0] == "exc":
                    with self.assertRaises(EXCEPTIONS[expected[1]]) as ctx:
                        nighit(w1, w2)
                    self.assertEqual(str(ctx.exception), expected[2])
                else:
                    self.assertEqual(nighit(w1, w2), expected[1])

    def test_unchanged_grid(self) -> None:
        """Outcomes that the fix must not change, recorded from old code."""
        digest = hashlib.sha256()
        count = 0
        consonant_grid = ["เ" + c + "า" for c in thai_consonants]
        for w1 in GRID_W1:
            for w2 in GRID_W2 + tuple(
                c for c in consonant_grid if c[1] not in CHANGED_CONSONANTS
            ):
                digest.update(repr((w1, w2, _outcome(w1, w2))).encode())
                count += 1
        self.assertEqual(count, GRID_SIZE)
        self.assertEqual(digest.hexdigest(), GRID_DIGEST)

    def test_changed_behavior(self) -> None:
        # (w1, w2, old behavior, new behavior); the new one is asserted.
        # สํ + ช: สังชา -> สัญชา
        # สํ + ฆ, ญ, ฏ, ฒ, ต, ม: NotImplementedError -> สัง/สัญ/สัณ/สัณ/สัน/สัม
        # ab + คา: aังคา -> NotImplementedError (w1 check)
        # สั + คา: สังคา -> NotImplementedError (w1 check)
        # ab + 123: ValueError (no consonant) -> NotImplementedError (w1 first)
        # Expected values follow the Pali rule: nighit becomes the nasal of
        # the vagga (consonant group) of the next consonant.
        cases = (
            ("สํ", "ชาติ", "สัญชาติ"),  # real word; ช is in the จ vagga
            ("สํ", "ตาน", "สันตาน"),  # real word; ต is in the ต vagga
            ("สํ", "ชา", "สัญชา"),
            ("สํ", "ฆา", "สังฆา"),
            ("สํ", "ญา", "สัญญา"),
            ("สํ", "ฏา", "สัณฏา"),
            ("สํ", "ฒา", "สัณฒา"),
            ("สํ", "ตา", "สันตา"),
            ("สํ", "มา", "สัมมา"),
        )
        for w1, w2, expected in cases:
            with self.subTest(w1=w1, w2=w2):
                self.assertEqual(nighit(w1, w2), expected)
        for w1, w2 in (("ab", "คา"), ("สั", "คา"), ("ab", "123")):
            with self.subTest(w1=w1, w2=w2):
                with self.assertRaises(NotImplementedError):
                    nighit(w1, w2)

    def test_ch_and_ta(self) -> None:
        """Regression: ช maps to ญ and ต maps to น."""
        self.assertEqual(nighit("สํ", "ชา"), "สัญชา")
        self.assertEqual(nighit("สํ", "ตา"), "สันตา")

    def test_w1_must_end_with_nighit(self) -> None:
        """Regression: a two-character w1 without nighit is rejected."""
        for w1 in ("ab", "สั", "ก"):
            with self.subTest(w1=w1):
                with self.assertRaises(NotImplementedError):
                    nighit(w1, "คา")

    def test_consonant_in_at_most_one_row(self) -> None:
        listed = [c for row, _ in _NIGHIT_ENDINGS for c in row]
        self.assertEqual(len(listed), len(set(listed)))
        for row, _ in _NIGHIT_ENDINGS:
            self.assertEqual(list(row), sorted(row, key=thai_consonants.index))

    def test_w1_prefix_dropped(self) -> None:
        # BUG-LEDGER: nighit-w1-prefix
        # Only the first character of w1 is used, so characters between it
        # and ํ are silently dropped.
        # Expected: keep the stem or reject it.
        self.assertEqual(nighit("สงฆํ", "คา"), "สังคา")
        self.assertEqual(nighit("สงฆํ", "คา"), nighit("สํ", "คา"))
        # A bare ํ is accepted too. Expected: reject it.
        self.assertEqual(nighit("ํ", "คา"), "ํังคา")


if __name__ == "__main__":
    unittest.main()
