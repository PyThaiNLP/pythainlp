# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Characterization tests for pythainlp.util.time.

Golden cases were recorded from the pre-refactor implementation.
"""

from __future__ import annotations

import hashlib
import random
import unittest
from typing import Optional

from pythainlp.util.time import (
    _DICT_THAI_TIME,
    _THAI_TIME_AFFIX,
    _format,
    thaiword_to_time,
    time_to_thaiword,
)

# fmt: off
_HOUR_GOLDEN: dict[str, tuple[str, ...]] = {
    "6h": (
        "เที่ยงคืน",
        "ตีหนึ่ง",
        "ตีสอง",
        "ตีสาม",
        "ตีสี่",
        "ตีห้า",
        "ตีหก",
        "หนึ่งโมงเช้า",
        "สองโมงเช้า",
        "สามโมงเช้า",
        "สี่โมงเช้า",
        "ห้าโมงเช้า",
        "เที่ยง",
        "บ่ายโมง",
        "บ่ายสองโมง",
        "บ่ายสามโมง",
        "บ่ายสี่โมง",
        "บ่ายห้าโมง",
        "หกโมงเย็น",
        "หนึ่งทุ่ม",
        "สองทุ่ม",
        "สามทุ่ม",
        "สี่ทุ่ม",
        "ห้าทุ่ม",
    ),
    "m6h": (
        "เที่ยงคืน",
        "ตีหนึ่ง",
        "ตีสอง",
        "ตีสาม",
        "ตีสี่",
        "ตีห้า",
        "หกโมง",
        "เจ็ดโมง",
        "แปดโมง",
        "เก้าโมง",
        "สิบโมง",
        "สิบเอ็ดโมง",
        "เที่ยง",
        "หนึ่งโมง",
        "สองโมง",
        "สามโมง",
        "สี่โมง",
        "ห้าโมง",
        "หกโมง",
        "หนึ่งทุ่ม",
        "สองทุ่ม",
        "สามทุ่ม",
        "สี่ทุ่ม",
        "ห้าทุ่ม",
    ),
    "24h": (
        "ศูนย์นาฬิกา",
        "หนึ่งนาฬิกา",
        "สองนาฬิกา",
        "สามนาฬิกา",
        "สี่นาฬิกา",
        "ห้านาฬิกา",
        "หกนาฬิกา",
        "เจ็ดนาฬิกา",
        "แปดนาฬิกา",
        "เก้านาฬิกา",
        "สิบนาฬิกา",
        "สิบเอ็ดนาฬิกา",
        "สิบสองนาฬิกา",
        "สิบสามนาฬิกา",
        "สิบสี่นาฬิกา",
        "สิบห้านาฬิกา",
        "สิบหกนาฬิกา",
        "สิบเจ็ดนาฬิกา",
        "สิบแปดนาฬิกา",
        "สิบเก้านาฬิกา",
        "ยี่สิบนาฬิกา",
        "ยี่สิบเอ็ดนาฬิกา",
        "ยี่สิบสองนาฬิกา",
        "ยี่สิบสามนาฬิกา",
    ),
}

_FORMAT_OK: tuple[tuple[int, int, int, str, Optional[str], str], ...] = (
    (12, 1, 59, "24h", "x", "สิบสองนาฬิกาหนึ่งนาทีห้าสิบเก้าวินาที"),
    (14, 59, 0, "m6h", "s", "สองโมงห้าสิบเก้านาทีศูนย์วินาที"),
    (19, 30, 0, "6h", "", "หนึ่งทุ่มครึ่ง"),
    (0, 30, 59, "6h", "m", "เที่ยงคืนครึ่ง"),
    (14, 0, 30, "24h", "", "สิบสี่นาฬิกาสามสิบวินาที"),
    (18, 27, 1, "24h", "m", "สิบแปดนาฬิกายี่สิบเจ็ดนาที"),
)

_FORMAT_ERR: tuple[tuple[int, int, int, Optional[str], Optional[str], str], ...] = (
    (-1, 6, 30, "24H", "", "Time format not supported: 24H"),
    (14, 39, 59, "", "s", "Time format not supported: "),
    (13, 0, 1, "x", "s", "Time format not supported: x"),
    (5, 1, 0, None, None, "Time format not supported: None"),
    (23, 59, 1, "x", "x", "Time format not supported: x"),
)

_TW_OK: tuple[tuple[str, bool, str], ...] = (
    ("เที่ยงกสิบเอ็ดสี่ยี่สิบตีห้ายี่", True, "12:177"),
    ("ตีห้าตีสี่", True, "05:00"),
    ("ทุ่มเที่ยงคืนๆ", False, "19:00"),
    ("หกโมงเช้า", False, "6:00"),
    ("โมงเย็นเที่ยงคืนสามสองตีหนึ่งตีห้าตีห้า", True, "25:16"),
    ("นาทีเที่ยงคืนบ่ายเที่ยงคืน", True, "00:13"),
    ("บ่ายโมงครึ่งตีสองสิบเอ็ด", False, "13:321"),
    ("หนึ่งทุ่มกว่า", True, "19:00"),
    ("ยี่โมงเช้าเจ็ดสิบเอ็ดสองตีห้า", True, "08:78"),
    ("บ่ายสี่สองหกโมงเย็น", True, "16:00"),
    ("ยี่นาฬิกาสิบ", True, "02:10"),
    ("ตีสามสิบห้า", True, "03:15"),
    ("ตีหนึ่ง", False, "1:00"),
    ("ตีหก", True, "06:00"),
    ("ตีหก", False, "6:00"),
    ("ตีหกสิบห้านาที", True, "06:15"),
    ("ตีหกครึ่ง", True, "06:30"),
    ("ตีหกครึ่ง", False, "6:30"),
    ("เที่ยงครึ่ง", True, "12:30"),
    ("บ่ายโมงครึ่ง", False, "13:30"),
)

_TW_ERR: tuple[tuple[str, bool, type[Exception], str], ...] = (
    ("เที่ยงคืนสิบหกบ่ายโมง", True, ValueError, "Cannot find any Thai word for hour."),
    ("สามสิบเอ็ดๆแปดสามสิบตีหกเจ็ด", True, ValueError, "Cannot find any Thai word for hour."),
    ("ตีเที่ยงวันนาฬิกาตีห้า", False, ValueError, "The input string is not a valid Thai numeral"),
    ("ๆกตีสองทุ่มศูนย์", True, ValueError, "Cannot find any Thai word for hour."),
    (" นาทีครึ่งๆสามสิบทุ่มเจ็ด", True, ValueError, "Cannot find any Thai word for hour."),
    ("กนาทีทุ่ม", True, ValueError, "Cannot find any Thai word for hour."),
    ("กกๆกว่าศูนย์ทุ่ม", False, ValueError, "Cannot find any Thai word for hour."),
    ("กกนาทีทุ่ม", True, ValueError, "Cannot find any Thai word for hour."),
    ("นาทีนาทีทุ่ม", True, ValueError, "Cannot find any Thai word for hour."),
    ("กหกสี่สามทุ่มยี่", True, ValueError, "Cannot find any Thai word for hour."),
    ("นาทีกทุ่ม", True, ValueError, "Cannot find any Thai word for hour."),
    ("กทุ่ม", True, ValueError, "Cannot find any Thai word for hour."),
    ("นาทีทุ่ม", True, ValueError, "Cannot find any Thai word for hour."),
    ("บ่ายกโมงเย็น", True, ValueError, "Cannot find any Thai word for hour."),
    ("ตีสิบห้า", True, ValueError, "Cannot find any Thai word for time affix."),
    ("ตี", True, ValueError, "Cannot find any Thai word for time affix."),
    ("", True, ValueError, "Cannot find any Thai word for time affix."),
)
# fmt: on

_NO_AFFIX = "Cannot find any Thai word for time affix."
_NO_HOUR = "Cannot find any Thai word for hour."


_FUZZ_EXTRA = ("กว่า", "ๆ", "ครึ่ง", "นาที", "ก", "สิบ", "เอ็ด", "ยี่", "ตี")


def _fuzz_inputs() -> list[str]:
    vocab = list(
        dict.fromkeys((*_DICT_THAI_TIME, *_THAI_TIME_AFFIX, *_FUZZ_EXTRA))
    )
    rng = random.Random(0)  # noqa: S311  # seeded, not crypto
    return [
        "".join(rng.choice(vocab) for _ in range(rng.randint(1, 4)))
        for _ in range(GRID_SIZE)
    ]


def _time_outcome(text: str, padding: bool) -> str:
    try:
        return thaiword_to_time(text, padding)
    except Exception as err:
        return "!" + type(err).__name__ + ":" + str(err)


def _out_of_range(outcome: str) -> bool:
    if outcome.startswith("!"):
        return False
    hour, minute = outcome.split(":")
    return int(hour) > 23 or int(minute) > 59


GRID_SIZE = 4000
GRID_COUNT = 5976
GRID_DIGEST = (
    "bfc81a1e46999437d0b683b2e7bd7374d7c0708a1791fd838969ca0f446c5b18"
)


class FormatTestCase(unittest.TestCase):
    def test_hour_formats(self) -> None:
        for fmt, expected in _HOUR_GOLDEN.items():
            for hour, text in enumerate(expected):
                with self.subTest(fmt=fmt, hour=hour):
                    self.assertEqual(_format(hour, 0, 0, fmt), text)

    def test_golden(self) -> None:
        for h, m, s, fmt, precision, expected in _FORMAT_OK:
            with self.subTest(h=h, m=m, s=s, fmt=fmt, precision=precision):
                self.assertEqual(_format(h, m, s, fmt, precision), expected)

    def test_unsupported_format(self) -> None:
        for h, m, s, fmt, precision, message in _FORMAT_ERR:
            with self.subTest(fmt=fmt, precision=precision):
                with self.assertRaises(NotImplementedError) as ctx:
                    _format(h, m, s, fmt, precision)  # type: ignore[arg-type]
                self.assertEqual(str(ctx.exception), message)

    def test_half_hour(self) -> None:
        self.assertEqual(_format(8, 30, 0, "6h"), "สองโมงเช้าครึ่ง")
        self.assertEqual(_format(8, 30, 5, "6h"), "สองโมงเช้าสามสิบนาทีห้าวินาที")
        self.assertEqual(_format(8, 30, 0, "24h"), "แปดนาฬิกาสามสิบนาที")
        self.assertEqual(_format(8, 30, 5, "m6h", "m"), "แปดโมงครึ่ง")
        self.assertEqual(_format(8, 30, 5, "m6h", "s"), "แปดโมงสามสิบนาทีห้าวินาที")
        self.assertEqual(_format(8, 30, 0, "m6h", "s"), "แปดโมงครึ่ง")


class ThaiwordToTimeTestCase(unittest.TestCase):
    def test_golden(self) -> None:
        for text, padding, expected in _TW_OK:
            with self.subTest(text=text, padding=padding):
                self.assertEqual(thaiword_to_time(text, padding), expected)

    def test_golden_errors(self) -> None:
        for text, padding, exc_type, message in _TW_ERR:
            with self.subTest(text=text, padding=padding):
                with self.assertRaises(exc_type) as ctx:
                    thaiword_to_time(text, padding)
                self.assertEqual(str(ctx.exception), message)

    def test_hour_rules(self) -> None:
        cases = (
            ("สิบสองนาฬิกาสามสิบนาที", "12:30"),
            ("หกโมงเช้าห้านาที", "06:05"),
            ("เจ็ดโมงเช้า", "07:00"),
            ("บ่ายสามโมง", "15:00"),
            ("บ่ายสามโมงเย็น", "15:00"),
            ("สองโมงเย็น", "14:00"),
            ("สามโมง", "15:00"),
            ("เที่ยงคืนห้านาที", "00:05"),
            ("เที่ยงวันสิบนาที", "12:10"),
            ("เที่ยงห้านาที", "12:05"),
            ("บ่ายโมงสิบนาที", "13:10"),
            ("ทุ่มห้านาที", "19:05"),
            ("สองทุ่มสิบนาที", "20:10"),
            ("ตีสามสิบห้านาที", "03:15"),
            ("ห้านาฬิกากว่าๆ", "05:00"),
            ("ห้า นาฬิกา ยี่สิบ นาที", "05:20"),
        )
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(thaiword_to_time(text), expected)

    def test_adversarial(self) -> None:
        for bad in (None, 42):
            with self.subTest(value=bad):
                with self.assertRaises(AttributeError):
                    thaiword_to_time(bad)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            thaiword_to_time(b"x")  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValueError, _NO_AFFIX):
            thaiword_to_time("ก" * 10000)
        with self.assertRaisesRegex(ValueError, _NO_AFFIX):
            thaiword_to_time("\u200b😀|")
        with self.assertRaisesRegex(ValueError, _NO_HOUR):
            thaiword_to_time("นาฬิกาห้านาที")

    def test_ti_fallthrough(self) -> None:
        # BUG-LEDGER: thaiword-to-time-ti
        # A "ตี" match does not stop the affix search; a later affix
        # (here "เที่ยง") re-splits the text, so the minute differs.
        self.assertEqual(thaiword_to_time("ตีสามเที่ยงสิบ"), "03:10")
        self.assertEqual(thaiword_to_time("ตีสามเที่ยงวันสิบห้า"), "03:15")
        self.assertEqual(thaiword_to_time("ตีสามสิบห้าเที่ยงครึ่ง"), "03:30")
        self.assertEqual(
            thaiword_to_time("โมงเย็นเที่ยงคืนสามสองตีหนึ่งตีห้าตีห้า"), "25:16"
        )

    def test_ti_six(self) -> None:
        for padding, expected in ((True, "06:00"), (False, "6:00")):
            with self.subTest(padding=padding):
                self.assertEqual(thaiword_to_time("ตีหก", padding), expected)
        for fmt in ("6h", "24h"):
            with self.subTest(fmt=fmt):
                text = time_to_thaiword("06:00", fmt=fmt)
                self.assertEqual(thaiword_to_time(text), "06:00")
        # "ตีสิบห้า" is not Thai usage
        with self.assertRaisesRegex(ValueError, _NO_AFFIX):
            thaiword_to_time("ตีสิบห้า")

    def test_out_of_range_values(self) -> None:
        # BUG-LEDGER: thaiword-to-time-range
        # Hour above 23 and minute above 59 are returned unchecked.
        self.assertEqual(
            thaiword_to_time("โมงเย็นเที่ยงคืนสามสองตีหนึ่งตีห้าตีห้า"), "25:16"
        )
        self.assertEqual(
            thaiword_to_time("บ่ายโมงครึ่งตีสองสิบเอ็ด", False), "13:321"
        )

    def test_unknown_token(self) -> None:
        # Formerly KeyError; "ตีหก" and "ตีสิบห้า" are in test_ti_six.
        for text in ("กนาทีทุ่ม", "บ่ายกโมงเย็น", "กทุ่ม"):
            with self.subTest(text=text):
                with self.assertRaisesRegex(ValueError, _NO_HOUR):
                    thaiword_to_time(text)
        with self.assertRaisesRegex(ValueError, "not a valid Thai numeral"):
            thaiword_to_time("ตีเที่ยงวันนาฬิกาตีห้า")

    def test_adversarial_inputs(self) -> None:
        # Current behavior, not a promise; only the ตีหก row differs from
        # the behavior before the fix.
        cases: tuple[tuple[str, str], ...] = (
            ("   ", _NO_AFFIX),
            ("\u200b", _NO_AFFIX),
            ("ตี\u200bหนึ่ง", _NO_AFFIX),
            ("ตี๑", _NO_AFFIX),
            ("\u0e47", _NO_AFFIX),
            ("ก" * 10000, _NO_AFFIX),
        )
        for text, message in cases:
            with self.subTest(text=text[:10]):
                with self.assertRaisesRegex(ValueError, message):
                    thaiword_to_time(text)
        for text, expected in (
            ("ตีหนึ่ง1", "01:00"),
            ("ตีหนึ่ง\u0e47", "01:00"),
            ("ตีสาม\u200bสิบ", "03:10"),
            ("ตีหนึ่ง" + "ก" * 10000, "01:00"),
            ("ตีหก\u200b", "06:00"),
        ):
            with self.subTest(text=text[:10]):
                self.assertEqual(thaiword_to_time(text), expected)

    def test_unchanged_grid(self) -> None:
        # Seeded random token strings; outcomes recorded before the fix.
        # Excluded: texts with "ตี" (ตีหก is fixed; the rest touches the
        # unfixed bug thaiword-to-time-ti), results out of range (unfixed
        # bug thaiword-to-time-range), and the hour error (formerly
        # KeyError; see test_unknown_token).
        digest = hashlib.sha256()
        count = 0
        for text in _fuzz_inputs():
            if "ตี" in text:
                continue
            for padding in (True, False):
                outcome = _time_outcome(text, padding)
                if outcome.startswith("!KeyError") or outcome == (
                    "!ValueError:" + _NO_HOUR
                ):
                    continue
                if _out_of_range(outcome):
                    continue
                digest.update(repr((text, padding, outcome)).encode())
                count += 1
        self.assertEqual(count, GRID_COUNT)
        self.assertEqual(digest.hexdigest(), GRID_DIGEST)


if __name__ == "__main__":
    unittest.main()
