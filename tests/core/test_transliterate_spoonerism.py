# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Characterization tests for pythainlp.transliterate.spoonerism.

The w2p engine needs optional dependencies, so pronunciate is mocked.
Expected values were recorded from the implementation before refactoring.
"""

import hashlib
import random
import unittest
from unittest import mock

from pythainlp.transliterate import spoonerism
from pythainlp.transliterate.spoonerism import _initial_char, puan

# (pronunciation from w2p, show_pronunciation, expected output)
CASES: tuple[tuple[str, bool, str], ...] = (
    ("นา-ริน", True, "นิน-รา"),
    ("นา-ริน", False, "นินรา"),
    ("นา-ริน-ทร", True, "นา-รร-ทิน"),
    ("นา-ริน-ทร", False, "นารรทิน"),
    ("กา-ขา-คา-งา", True, "งา-ขา-คา-กา"),
    ("กา-ขา-คา-งา", False, "งาขาคากา"),
    ("กา-ขา-คา-งา-จา", True, "จา-ขา-คา-งา-กา"),
    ("กา-ขา-คา-งา-จา", False, "จาขาคางากา"),
    ("กา-ขา-คา-งา-จา-ฉา", True, "ฉา-ขา-คา-งา-จา-กา"),
    ("กา-ขา-คา-งา-จา-ฉา", False, "ฉาขาคางาจากา"),
    ("หมา-กา", True, "มา-หกา"),
    ("หมา-กา", False, "มาหกา"),
    ("หมา-กา-ขา", True, "หมา-กา-ขา"),
    ("หมา-กา-ขา", False, "หมากาขา"),
    ("กา-หมา", True, "หกา-มา"),
    ("กา-หมา", False, "หกามา"),
    ("หนู-หมา-นา", True, "หนู-มา-หนา"),
    ("หนู-หมา-นา", False, "หนูมาหนา"),
    ("หฺมา-กา", True, "มา-หฺกา"),
    ("หฺมา-กา", False, "มากา"),
    ("หฺมา-กา-ขา-คา", True, "หฺคา-กา-ขา-มา"),
    ("หฺมา-กา-ขา-คา", False, "คากาขามา"),
    ("อา-กา", True, "อา-กา"),
    ("อา-กา", False, "อากา"),
    ("ก-ข", True, "ก-ข"),
    ("ก-ข", False, "กข"),
    ("ะ-กา-ขา", True, "ะ-กา-ขา"),
    ("ะ-กา-ขา", False, "ะกาขา"),
    ("ะ-กา", True, "ะ-กา"),
    ("ะ-กา", False, "ะกา"),
    ("กา-ะ", True, "กา-ะ"),
    ("กา-ะ", False, "กาะ"),
    ("กา-ะ-ขา", True, "กา-ะ-ขา"),
    ("กา-ะ-ขา", False, "กาะขา"),
    ("กา", True, "กา"),
    ("กา", False, "กา"),
    ("", True, ""),
    ("", False, ""),
    ("กา-", True, "กา-"),
    ("กา-", False, "กา"),
    ("-กา", True, "-กา"),
    ("-กา", False, "กา"),
    ("กา--ขา", True, "กา--ขา"),
    ("กา--ขา", False, "กาขา"),
    ("หะ-กา", True, "หา-กะ"),
    ("หะ-กา", False, "หากะ"),
    ("เห-กา", True, "หา-เก"),
    ("เห-กา", False, "หาเก"),
    ("หะ-หา", True, "หา-หะ"),
    ("หะ-หา", False, "หาหะ"),
    ("ก-ะ-ข-ะ", True, "ก-ะ-ข-ะ"),
    ("ก-ะ-ข-ะ", False, "กะขะ"),
    ("ก-ขา-คา-ะ", True, "ก-ขา-คา-ะ"),
    ("ก-ขา-คา-ะ", False, "กขาคาะ"),
    ("ะ", True, "ะ"),
    ("ะ", False, "ะ"),
    ("กา-ะ-ขิน", True, "กิน-ะ-ขา"),
    ("กา-ะ-ขิน", False, "กินะขา"),
    ("ก-ะ-ขา-ะ-คิน", True, "ก-ะ-ขิน-ะ-คา"),
    ("ก-ะ-ขา-ะ-คิน", False, "กะขินะคา"),
    ("กา--ขิน", True, "กิน--ขา"),
    ("กา--ขิน", False, "กินขา"),
    ("ะ-กา-ขิน-คุ-ดี", True, "ะ-ดา-ขิน-คุ-กี"),
    ("ะ-กา-ขิน-คุ-ดี", False, "ะดาขินคุกี"),
    ("กา-ะะ-ะะ-ขา", True, "กา-ะะ-ะะ-ขา"),
    ("กา-ะะ-ะะ-ขา", False, "กาะะะะขา"),
)

# Pronunciations with no consonant to swap in any syllable
NO_INITIAL = ("ะ-ะ", "-", "ะ-ะ-ะ", "ะ-ะ-ะ-ะ")


def run_puan(pron: str, show: bool = True) -> str:
    with mock.patch.object(
        spoonerism, "pronunciate", return_value=pron
    ) as pronunciate:
        result = puan("x", show)
    pronunciate.assert_called_once_with("x", engine="w2p")
    return result


# Seeded syllable lists in which every syllable has an initial consonant.
# Outputs were recorded from the implementation before the fix for
# syllables without an initial; they must not change.
GRID_SIZE = 3000
GRID_DIGEST = (
    "413b65e1e19c5229c8aa1c8a7c49d41d7ab0993d947bd1d01e051661df721797"
)
_GRID_CONSONANTS: tuple[str, ...] = (
    *"กขคงจฉนมรทดบพ",
    "หม",
    "หน",
    "หฺม",
    "ทร",
    "กร",
    "กล",
)
_GRID_VOWELS: tuple[str, ...] = ("า", "ิ", "ุ", "ี", "ะ", "ู", "", "เ", "แ")


def _grid_syllable(rng: random.Random) -> str:
    initial = rng.choice(_GRID_CONSONANTS)
    vowel = rng.choice(_GRID_VOWELS)
    body = vowel + initial if vowel in "เแ" else initial + vowel
    tail: str = rng.choice(("", "น", "ง"))
    return body + tail


def _grid() -> list[str]:
    rng = random.Random(0)  # noqa: S311
    grid: list[str] = []
    while len(grid) < GRID_SIZE:
        syllables = [_grid_syllable(rng) for _ in range(rng.randint(1, 7))]
        if all(_initial_char(s) is not None for s in syllables):
            grid.append("-".join(syllables))
    return grid


# (pronunciation, old behavior, new behavior with show_pronunciation=True)
# Syllables without an initial used to be dropped or shifted, or the
# call raised IndexError; they now stay in place.
CHANGED_CASES: tuple[tuple[str, str, str], ...] = (
    ("ก-ะ-ข-ะ", "ะ-ข", "ก-ะ-ข-ะ"),
    ("ก-ขา-คา-ะ", "ก-ขา-คา", "ก-ขา-คา-ะ"),
    ("กา-ะะ-ะะ-ขา", "ะะ-ขา", "กา-ะะ-ะะ-ขา"),
    ("ะ-กา-ขา", "กา-ะ", "ะ-กา-ขา"),
    ("กา-ะ-ขา", "ะ-ขา", "กา-ะ-ขา"),
    ("กา--ขา", "-ขา", "กา--ขา"),
    ("ะ-ะ", "IndexError", "ะ-ะ"),
    ("-", "IndexError", "-"),
    ("ะ-ะ-ะ", "IndexError", "ะ-ะ-ะ"),
    ("ะ-ะ-ะ-ะ", "IndexError", "ะ-ะ-ะ-ะ"),
    ("กา-ะ-ขิน", "ะ-ขิน", "กิน-ะ-ขา"),
    ("ก-ะ-ขา-ะ-คิน", "ะ-ขา-คิน", "ก-ะ-ขิน-ะ-คา"),
    ("กา--ขิน", "-ขิน", "กิน--ขา"),
    ("ะ-กา-ขิน-คุ-ดี", "กา-ขิน-คุ", "ะ-ดา-ขิน-คุ-กี"),
)

# (pronunciation, output with show_pronunciation=True, output with False)
# Expected values are derived by hand (comments below), not recorded.
# Rows with a syllable that has no Thai consonant (empty, space, digit,
# ASCII, zero-width, or a bare vowel sign) used to raise IndexError, drop
# syllables, or shift the swap; all other rows are unchanged.
ADVERSARIAL: tuple[tuple[str, str, str], ...] = (
    # Hand-derived with the rule: found = syllables that have an initial.
    # 0 or 1 found: unchanged. 2 or 3: last two swap rimes, initials stay.
    # 4 or more: first and last swap initials. 1 syllable: unchanged.
    # No consonant at all (empty, space, digit, ASCII): unchanged.
    ("--", "--", ""),
    (" ", " ", " "),
    (" - ", " - ", "  "),
    ("\u200b", "\u200b", "\u200b"),
    # 2 found (ก, ขา): rimes swap, so ก+า and ข: กา, ZWSP+า, ข.
    ("ก-\u200bา-ขา", "กา-\u200bา-ข", "กา\u200bาข"),
    # 2 found: the zero-width space stays in its syllable (ข+ZWSP).
    ("ก\u200b-ขา", "กา-ข\u200b", "กาข\u200b"),
    ("๑-๒-๓", "๑-๒-๓", "๑๒๓"),
    # 2 found (ก, ข): rimes swap; the digit prefix stays.
    ("๑ก-๒ข", "๒ก-๑ข", "๒ก๑ข"),
    ("a-b-c", "a-b-c", "abc"),
    ("ab-cd", "ab-cd", "abcd"),
    # 3 found, last two have empty rimes: unchanged.
    ("ก-ข-ค", "ก-ข-ค", "กขค"),
    # Tone marks belong to the rime and move with it.
    ("ก่า-ข้า", "ก้า-ข่า", "ก้าข่า"),
    ("ก่า-ข้า-ค๊า", "ก่า-ข๊า-ค้า", "ก่าข๊าค้า"),
    # หฺ is not an initial (initial is ม); same rimes: unchanged.
    # show_pronunciation=False strips หฺ.
    ("หฺม-กา-ขา", "หฺม-กา-ขา", "มกาขา"),
    ("หฺม-หฺน", "หฺม-หฺน", "มน"),
    # Two-char ห syllables have initial ห: whole syllables swap.
    ("หม-หน", "หน-หม", "หนหม"),
    # 4 found, all initial ห: swapping equal initials changes nothing.
    ("หม-หน-หร-หล", "หม-หน-หร-หล", "หมหนหรหล"),
    ("หา-หา", "หา-หา", "หาหา"),
    # Identical syllables: swapping changes nothing.
    ("กา-กา-กา", "กา-กา-กา", "กากากา"),
    ("กา-กา-กา-กา", "กา-กา-กา-กา", "กากากากา"),
    ("กา-กา-กา-กา-กา", "กา-กา-กา-กา-กา", "กากากากากา"),
    # Syllables without an initial stay in place; found syllables have
    # equal rimes (า), so the swap is invisible.
    ("ะ-กา-ขา-ะ", "ะ-กา-ขา-ะ", "ะกาขาะ"),
    ("ะ-กา-ะ", "ะ-กา-ะ", "ะกาะ"),
    ("ะ-ก-ะ", "ะ-ก-ะ", "ะกะ"),
    ("ก-ะ", "ก-ะ", "กะ"),
    ("ะ-ะ-ะ-ะ-ะ", "ะ-ะ-ะ-ะ-ะ", "ะะะะะ"),
    ("ะ-กา-ขา-คา-ะ", "ะ-กา-ขา-คา-ะ", "ะกาขาคาะ"),
    ("ะ-ะ-กา-ขา-ะ", "ะ-ะ-กา-ขา-ะ", "ะะกาขาะ"),
    # 5 found: ก and จ swap initials; trailing ะ-ะ stay.
    ("กา-ขา-คา-งา-จา-ะ-ะ", "จา-ขา-คา-งา-กา-ะ-ะ", "จาขาคางากาะะ"),
    ("กา-ขา-คา", "กา-ขา-คา", "กาขาคา"),
    ("ะ-กา-ขา-คา", "ะ-กา-ขา-คา", "ะกาขาคา"),
    ("ะ-ะ-กา", "ะ-ะ-กา", "ะะกา"),
    ("-กา-ขา", "-กา-ขา", "กาขา"),
    ("กา-ขา-", "กา-ขา-", "กาขา"),
    ("กา-ขา-คา-", "กา-ขา-คา-", "กาขาคา"),
)


class PuanTestCase(unittest.TestCase):
    def test_golden_cases(self) -> None:
        for pron, show, expected in CASES:
            with self.subTest(pron=pron, show=show):
                self.assertEqual(run_puan(pron, show), expected)

    def test_unchanged_grid(self) -> None:
        grid = _grid()
        self.assertEqual(len(grid), GRID_SIZE)
        digest = hashlib.sha256()
        for pron in grid:
            for show in (True, False):
                line = f"{pron}|{show}|{run_puan(pron, show)}\n"
                digest.update(line.encode("utf-8"))
        self.assertEqual(digest.hexdigest(), GRID_DIGEST)

    def test_changed_cases(self) -> None:
        for pron, _old, new in CHANGED_CASES:
            with self.subTest(pron=pron):
                self.assertEqual(run_puan(pron), new)
                self.assertEqual(run_puan(pron, False), new.replace("-", ""))

    def test_syllable_without_initial(self) -> None:
        # Syllables without an initial keep their place.
        for pron in ("ก-ะ-ข-ะ", "ะ-กา-ขา", "กา--ขา"):
            with self.subTest(pron=pron):
                self.assertEqual(run_puan(pron), pron)
        self.assertEqual(run_puan("ะ-กา-ขิน-คุ-ดี"), "ะ-ดา-ขิน-คุ-กี")

    def test_no_initial_unchanged(self) -> None:
        for pron in NO_INITIAL:
            for show in (True, False):
                with self.subTest(pron=pron, show=show):
                    expected = pron if show else pron.replace("-", "")
                    self.assertEqual(run_puan(pron, show), expected)

    def test_adversarial_inputs(self) -> None:
        for pron, shown, hidden in ADVERSARIAL:
            with self.subTest(pron=pron):
                self.assertEqual(run_puan(pron), shown)
                self.assertEqual(run_puan(pron, False), hidden)

    def test_long_syllable_lists(self) -> None:
        n = 1000
        same = "-".join(["กา"] * n)
        self.assertEqual(run_puan(same), same)
        mixed = run_puan("-".join(["กา", "ขิน"] * (n // 2))).split("-")
        self.assertEqual(len(mixed), n)
        self.assertEqual((mixed[0], mixed[-1]), ("ขา", "กิน"))
        self.assertEqual(mixed[1:-1], ["ขิน", "กา"] * (n // 2 - 1))
        for pron in (
            "-".join(["ะ"] * n),
            "-".join(["ะ", *["กา"] * (n - 2), "ะ"]),
        ):
            self.assertEqual(run_puan(pron), pron)
            self.assertEqual(run_puan(pron, False), pron.replace("-", ""))

    def test_wrong_type_pronunciation(self) -> None:
        # Exception types are current behavior, not a promise.
        for value, error in (
            (None, AttributeError),
            (123, AttributeError),
            (["ก-ข"], AttributeError),
            (b"a-b", TypeError),
        ):
            with self.subTest(value=value):
                with self.assertRaises(error):
                    run_puan(value)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
