# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Characterization tests for pythainlp.transliterate.spoonerism.

The w2p engine needs optional dependencies, so pronunciate is mocked.
Expected values were recorded from the implementation before refactoring.
"""

import unittest
from unittest import mock

from pythainlp.transliterate import spoonerism
from pythainlp.transliterate.spoonerism import puan

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
    ("ะ-กา-ขา", True, "กา-ะ"),
    ("ะ-กา-ขา", False, "กาะ"),
    ("ะ-กา", True, "ะ-กา"),
    ("ะ-กา", False, "ะกา"),
    ("กา-ะ", True, "กา-ะ"),
    ("กา-ะ", False, "กาะ"),
    ("กา-ะ-ขา", True, "ะ-ขา"),
    ("กา-ะ-ขา", False, "ะขา"),
    ("กา", True, "กา"),
    ("กา", False, "กา"),
    ("", True, ""),
    ("", False, ""),
    ("กา-", True, "กา-"),
    ("กา-", False, "กา"),
    ("-กา", True, "-กา"),
    ("-กา", False, "กา"),
    ("กา--ขา", True, "-ขา"),
    ("กา--ขา", False, "ขา"),
    ("หะ-กา", True, "หา-กะ"),
    ("หะ-กา", False, "หากะ"),
    ("เห-กา", True, "หา-เก"),
    ("เห-กา", False, "หาเก"),
    ("หะ-หา", True, "หา-หะ"),
    ("หะ-หา", False, "หาหะ"),
    ("ก-ะ-ข-ะ", True, "ะ-ข"),
    ("ก-ะ-ข-ะ", False, "ะข"),
    ("ก-ขา-คา-ะ", True, "ก-ขา-คา"),
    ("ก-ขา-คา-ะ", False, "กขาคา"),
    ("ะ", True, "ะ"),
    ("ะ", False, "ะ"),
    ("กา-ะะ-ะะ-ขา", True, "ะะ-ขา"),
    ("กา-ะะ-ะะ-ขา", False, "ะะขา"),
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


class PuanTestCase(unittest.TestCase):
    def test_golden_cases(self) -> None:
        for pron, show, expected in CASES:
            with self.subTest(pron=pron, show=show):
                self.assertEqual(run_puan(pron, show), expected)

    # BUG-LEDGER: puan-missing-initial
    def test_syllable_without_initial(self) -> None:
        # A syllable with no consonant is dropped from the output
        # and shifts the swap; it should keep its place.
        self.assertEqual(run_puan("ก-ะ-ข-ะ"), "ะ-ข")
        self.assertEqual(run_puan("ะ-กา-ขา"), "กา-ะ")

    # BUG-LEDGER: puan-missing-initial
    def test_no_initial_raises_index_error(self) -> None:
        for pron in NO_INITIAL:
            with self.subTest(pron=pron):
                with self.assertRaises(IndexError):
                    run_puan(pron)

    def test_wrong_type_pronunciation(self) -> None:
        with self.assertRaises(AttributeError):
            run_puan(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
