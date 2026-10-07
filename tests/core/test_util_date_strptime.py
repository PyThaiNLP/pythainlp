# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Characterization tests for pythainlp.util.date.thai_strptime.

Golden data was recorded from the pre-refactor implementation.
"""

import re
import unittest
from typing import Any
from zoneinfo import ZoneInfo

from pythainlp.util import thai_strptime

_BANGKOK = ZoneInfo("Asia/Bangkok")
_UTC = ZoneInfo("UTC")
_TZ = {"d": _BANGKOK, "utc": _UTC, None: None}


class _AnyMessage:
    """
    Match any message.

    For text that comes from the standard library
    and differs between Python versions.
    """

    def __eq__(self, other: object) -> bool:
        return True

    def __hash__(self) -> int:
        return 0

    def __repr__(self) -> str:
        return "<any message>"


_STDLIB_MESSAGE = _AnyMessage()

# ((text, fmt, year, add_year, tz), expected)
# tz is "d" for the default tzinfo, "utc", or None.
# Expected is (year, month, day, hour, minute, second, microsecond, tz key)
# or (exception name, message). A message from the standard library is
# not pinned, as it differs between Python versions.

_GOLDEN = [
    (
        ("15 ก.ค. 2565 09:00:01", "%d %B %Y %H:%M:%S", "be", None, "d"),
        (2022, 7, 15, 9, 0, 1, 0, "Asia/Bangkok"),
    ),
    (
        ("15 ก.ค. 2565 09:00:01", "%d %B %Y %H:%M:%S", "be", None, None),
        (2022, 7, 15, 9, 0, 1, 0, None),
    ),
    (
        ("15 ก.ค. 2565 09:00:01", "%d %B %Y %H:%M:%S", "be", None, "utc"),
        (2022, 7, 15, 9, 0, 1, 0, "UTC"),
    ),
    (
        ("15 กรกฎาคม 2565 9:5:7", "%d %B %Y %H:%M:%S", "be", None, "d"),
        (2022, 7, 15, 9, 5, 7, 0, "Asia/Bangkok"),
    ),
    (
        ("1 มกราคม 2565 0:0:0", "%d %B %Y %H:%M:%S", "be", None, "d"),
        (2022, 1, 1, 0, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("01 ธ.ค. 2565 23:59:59", "%d %B %Y %H:%M:%S", "be", None, "d"),
        (2022, 12, 1, 23, 59, 59, 0, "Asia/Bangkok"),
    ),
    (
        ("15 07 2565 09:00:01", "%d %B %Y %H:%M:%S", "be", None, "d"),
        (2022, 7, 15, 9, 0, 1, 0, "Asia/Bangkok"),
    ),
    (
        ("15 7 2565 09:00:01", "%d %B %Y %H:%M:%S", "be", None, "d"),
        (2022, 7, 15, 9, 0, 1, 0, "Asia/Bangkok"),
    ),
    (
        ("15 กรกฎา 2022 09:00:01", "%d %B %Y %H:%M:%S", "ad", None, "d"),
        ("IndexError", "list index out of range"),
    ),
    (
        ("29 ก.พ. 2567", "%d %B %Y", "be", None, "d"),
        (2024, 2, 29, 0, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("29 ก.พ. 2566", "%d %B %Y", "be", None, "d"),
        ("ValueError", _STDLIB_MESSAGE),
    ),
    (
        ("31 เมษายน 2566", "%d %B %Y", "be", None, "d"),
        ("ValueError", _STDLIB_MESSAGE),
    ),
    (
        ("9 มี.ค. 66", "%-d %B %Y", "be", None, "d"),
        (2023, 3, 9, 0, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("9 มี.ค. 66", "%-d %B %Y", "be", 2500, "d"),
        (2023, 3, 9, 0, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("9 มี.ค. 66", "%-d %B %Y", "be", "2400", "d"),
        (1923, 3, 9, 0, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("9 มี.ค. 66", "%d %b %Y", "ad", None, "d"),
        (2066, 3, 9, 0, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("9 มี.ค. 66", "%d %b %Y", "ad", 1900, "d"),
        (1966, 3, 9, 0, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("9 มี.ค. 66", "%d %b %Y", "ad", "1900", "d"),
        (1966, 3, 9, 0, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("9 มี.ค. 66", "%d %b %Y", "xx", None, "d"),
        (66, 3, 9, 0, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("9 มี.ค. 2566", "%d %b %Y", "xx", None, "d"),
        (2566, 3, 9, 0, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("9 มี.ค. 2023", "%d %b %Y", "ad", None, "d"),
        (2023, 3, 9, 0, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("9 มี.ค. 0000", "%d %b %Y", "be", None, "d"),
        (1957, 3, 9, 0, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("9 มี.ค. 00", "%d %b %Y", "ad", None, "d"),
        (2000, 3, 9, 0, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("15 ก.ค. 2565 09:00", "%d %B %Y %H:%M", "be", None, "d"),
        (2022, 7, 15, 9, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("15 ก.ค. 2565 09", "%d %B %Y %H", "be", None, "d"),
        (2022, 7, 15, 9, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("15 ก.ค. 2565 5", "%d %B %Y %M", "be", None, "d"),
        (2022, 7, 15, 0, 5, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("15 ก.ค. 2565 7", "%d %B %Y %S", "be", None, "d"),
        (2022, 7, 15, 0, 0, 7, 0, "Asia/Bangkok"),
    ),
    (
        (
            "15 ก.ค. 2565 09:00:01.123456",
            "%d %B %Y %H:%M:%S.%f",
            "be",
            None,
            "d",
        ),
        (2022, 7, 15, 9, 0, 1, 123456, "Asia/Bangkok"),
    ),
    (
        (
            "15 ก.ค. 2565 09:00:01.1234567",
            "%d %B %Y %H:%M:%S.%f",
            "be",
            None,
            "d",
        ),
        ("ValueError", _STDLIB_MESSAGE),
    ),
    (
        ("15-ก.ค.-2565", "%d-%B-%Y", "be", None, "d"),
        (2022, 7, 15, 0, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("15 ก.ค. 2565", "%-d %b %Y", "be", None, "d"),
        (2022, 7, 15, 0, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("ก.ค. 2565 15", "%B %Y %d", "be", None, "d"),
        (2022, 7, 15, 0, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("[15] ก.ค. 2565", "[%d] %B %Y", "be", None, "d"),
        ("IndexError", "list index out of range"),
    ),
    (
        ("15/07/2565", "%d/%m/%Y", "be", None, "d"),
        ("IndexError", "list index out of range"),
    ),
    (
        ("15/7/65", "%-d/%-m/%y", "be", None, "d"),
        ("IndexError", "list index out of range"),
    ),
    (
        ("15 ก.ค. 65", "%d %B %y", "be", None, "d"),
        ("IndexError", "list index out of range"),
    ),
    (
        ("15 ก.ค. 65", "%d %B %-y", "be", None, "d"),
        ("IndexError", "list index out of range"),
    ),
    (("15 ก.ค.", "%d %B", "be", None, "d"), ("KeyError", "'Y'")),
    (("ก.ค. 2565", "%B %Y", "be", None, "d"), ("KeyError", "'d'")),
    (("15 2565", "%d %Y", "be", None, "d"), ("KeyError", "'B'")),
    (
        ("15 ก.ค. 2565 %m 09", "%d %B %Y %m %H", "be", None, "d"),
        ("KeyError", "'H'"),
    ),
    (
        ("no match", "%d %B %Y %H:%M:%S", "be", None, "d"),
        ("IndexError", "list index out of range"),
    ),
    (
        ("", "%d %B %Y %H:%M:%S", "be", None, "d"),
        ("IndexError", "list index out of range"),
    ),
    (("15 ก.ค. 2565", "", "be", None, "d"), ("KeyError", "'d'")),
    (
        ("15 ก.ค. 2565", "plain", "be", None, "d"),
        ("IndexError", "list index out of range"),
    ),
    (
        ("15 ก.ค. 2565", "%d %B %Y", "be", "abc", "d"),
        (2022, 7, 15, 0, 0, 0, 0, "Asia/Bangkok"),
    ),
    (
        ("9 มี.ค. 66", "%d %B %Y", "be", "abc", "d"),
        ("ValueError", "invalid literal for int() with base 10: 'abc'"),
    ),
    (
        ("9 มี.ค. 66", "%d %B %Y", "be", 1.5, "d"),
        ("ValueError", _STDLIB_MESSAGE),
    ),
    (
        ("9 มี.ค. 66", "%d %B %Y", "ad", 2000, "d"),
        (2066, 3, 9, 0, 0, 0, 0, "Asia/Bangkok"),
    ),
]


def _run(
    text: str, fmt: str, year: str, add_year: Any, tz: Any
) -> tuple[Any, ...]:
    try:
        if tz == "d":
            dt_obj = thai_strptime(text, fmt, year, add_year)
        else:
            dt_obj = thai_strptime(text, fmt, year, add_year, _TZ[tz])
    except Exception as err:  # noqa: BLE001 - golden test records any error
        return (type(err).__name__, str(err))
    return (
        dt_obj.year,
        dt_obj.month,
        dt_obj.day,
        dt_obj.hour,
        dt_obj.minute,
        dt_obj.second,
        dt_obj.microsecond,
        getattr(dt_obj.tzinfo, "key", None),
    )


class ThaiStrptimeTestCase(unittest.TestCase):
    def test_golden(self) -> None:
        for args, expected in _GOLDEN:
            with self.subTest(args=args):
                self.assertEqual(_run(*args), expected)

    def test_docstring_example(self) -> None:
        self.assertEqual(
            thai_strptime(
                "15 ก.ค. 2565 09:00:01", "%d %B %Y %H:%M:%S"
            ).isoformat(),
            "2022-07-15T09:00:01+07:00",
        )

    # BUG-LEDGER: thai-strptime-m-y
    def test_bug_m_and_y_directives_unsupported(self) -> None:
        # Expected: parse "15/07/2565" with "%d/%m/%Y" and "15/7/65" with
        # "%-d/%-m/%y". Currently %m and %y are left in the pattern, so
        # nothing matches and IndexError is raised.
        for text, fmt in (
            ("15/07/2565", "%d/%m/%Y"),
            ("15/7/65", "%-d/%-m/%y"),
            ("15 ก.ค. 65", "%d %B %y"),
            ("15 ก.ค. 65", "%d %B %-y"),
        ):
            with self.subTest(fmt=fmt):
                with self.assertRaises(IndexError):
                    thai_strptime(text, fmt)

    def test_invalid_pattern(self) -> None:
        with self.assertRaises(re.error):
            thai_strptime("15 ก.ค. 2565", "(%d %B %Y")

    def test_invalid_input_types(self) -> None:
        with self.assertRaises(TypeError):
            thai_strptime(None, "%d %B %Y")  # type: ignore[arg-type]
        with self.assertRaises(AttributeError):
            thai_strptime("15 ก.ค. 2565", None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            thai_strptime(20220715, "%d %B %Y")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
