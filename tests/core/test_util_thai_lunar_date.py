# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Characterization tests for pythainlp.util.thai_lunar_date.

Golden data was recorded from the pre-refactor implementation.
It covers every begin date and every year length (354, 355, 384 days).
"""

from __future__ import annotations

import unittest
from datetime import date, datetime
from unittest.mock import patch

from pythainlp.util import thai_lunar_date
from pythainlp.util.thai_lunar_date import (
    _adjust_month,
    _month_and_day,
    to_lunar_date,
)

# fmt: off
_LUNAR_GOLDEN: tuple[tuple[str, str], ...] = (
    ("1934-08-10", "แรม 15 ค่ำ เดือน 8"),
    ("1903-11-21", "ขึ้น 2 ค่ำ เดือน 1"),
    ("1922-07-19", "แรม 10 ค่ำ เดือน 8"),
    ("2121-12-11", "ขึ้น 2 ค่ำ เดือน 1"),
    ("2045-05-05", "แรม 5 ค่ำ เดือน 6"),
    ("2147-05-17", "แรม 3 ค่ำ เดือน 6"),
    ("2076-03-08", "ขึ้น 4 ค่ำ เดือน 4"),
    ("2012-12-02", "แรม 4 ค่ำ เดือน 1"),
    ("2035-09-07", "ขึ้น 6 ค่ำ เดือน 10"),
    ("1907-04-21", "ขึ้น 9 ค่ำ เดือน 6"),
    ("2227-01-17", "แรม 14 ค่ำ เดือน 2"),
    ("2188-07-07", "ขึ้น 14 ค่ำ เดือน 8"),
    ("2289-09-01", "ขึ้น 15 ค่ำ เดือน 9"),
    ("2330-03-05", "ขึ้น 15 ค่ำ เดือน 4"),
    ("2101-09-19", "แรม 12 ค่ำ เดือน 10"),
    ("2111-08-17", "ขึ้น 13 ค่ำ เดือน 9"),
    ("2160-03-26", "แรม 5 ค่ำ เดือน 4"),
    ("2451-12-26", "ขึ้น 4 ค่ำ เดือน 2"),
    ("2334-10-14", "แรม 1 ค่ำ เดือน 11"),
    ("2125-11-09", "ขึ้น 14 ค่ำ เดือน 12"),
    ("1964-06-14", "ขึ้น 5 ค่ำ เดือน 8"),
    ("1926-03-22", "ขึ้น 9 ค่ำ เดือน 5"),
    ("2302-04-19", "แรม 6 ค่ำ เดือน 5"),
    ("2028-03-21", "แรม 11 ค่ำ เดือน 4"),
    ("2377-05-04", "แรม 11 ค่ำ เดือน 5"),
    ("2073-09-13", "ขึ้น 12 ค่ำ เดือน 10"),
    ("2454-05-03", "ขึ้น 7 ค่ำ เดือน 6"),
    ("2373-03-21", "แรม 12 ค่ำ เดือน 4"),
    ("2258-09-17", "แรม 4 ค่ำ เดือน 10"),
    ("2143-09-24", "แรม 1 ค่ำ เดือน 10"),
    ("2422-06-18", "แรม 14 ค่ำ เดือน 7"),
    ("2269-02-08", "ขึ้น 6 ค่ำ เดือน 3"),
    ("2305-06-02", "ขึ้น 9 ค่ำ เดือน 7"),
    ("2411-04-21", "แรม 13 ค่ำ เดือน 5"),
    ("2345-08-18", "แรม 4 ค่ำ เดือน 9"),
    ("2436-12-24", "แรม 1 ค่ำ เดือน 1"),
    ("2176-12-27", "แรม 11 ค่ำ เดือน 1"),
    ("2000-01-10", "ขึ้น 5 ค่ำ เดือน 2"),
    ("2086-10-09", "ขึ้น 2 ค่ำ เดือน 11"),
    ("2429-06-30", "แรม 13 ค่ำ เดือน 7"),
    ("2214-04-20", "ขึ้น 10 ค่ำ เดือน 5"),
    ("1949-07-29", "ขึ้น 4 ค่ำ เดือน 9"),
    ("2245-10-03", "ขึ้น 12 ค่ำ เดือน 11"),
    ("2360-12-01", "แรม 8 ค่ำ เดือน 12"),
    ("2403-09-21", "ขึ้น 5 ค่ำ เดือน 10"),
    ("2206-11-18", "แรม 2 ค่ำ เดือน 12"),
    ("1974-06-25", "ขึ้น 6 ค่ำ เดือน 8"),
    ("2201-02-10", "ขึ้น 7 ค่ำ เดือน 3"),
    ("2058-04-23", "ขึ้น 1 ค่ำ เดือน 6"),
    ("2019-03-01", "แรม 10 ค่ำ เดือน 3"),
    ("2386-02-22", "แรม 8 ค่ำ เดือน 3"),
    ("1958-02-10", "แรม 7 ค่ำ เดือน 3"),
    ("2282-01-28", "แรม 4 ค่ำ เดือน 2"),
    ("2320-11-15", "ขึ้น 14 ค่ำ เดือน 12"),
    ("2240-02-02", "ขึ้น 9 ค่ำ เดือน 3"),
    ("2169-06-13", "แรม 4 ค่ำ เดือน 7"),
    ("1984-09-27", "ขึ้น 2 ค่ำ เดือน 11"),
    ("2190-11-13", "แรม 2 ค่ำ เดือน 12"),
    ("2046-03-08", "ขึ้น 2 ค่ำ เดือน 4"),
    ("2371-09-04", "แรม 9 ค่ำ เดือน 9"),
    ("2325-11-06", "แรม 14 ค่ำ เดือน 11"),
    ("2036-04-04", "ขึ้น 9 ค่ำ เดือน 5"),
    ("2028-07-09", "แรม 3 ค่ำ เดือน 8"),
    ("2422-01-04", "ขึ้น 12 ค่ำ เดือน 2"),
    ("2064-11-16", "ขึ้น 8 ค่ำ เดือน 12"),
    ("2093-01-17", "แรม 6 ค่ำ เดือน 2"),
    ("2064-10-30", "แรม 5 ค่ำ เดือน 11"),
    ("2109-05-31", "ขึ้น 3 ค่ำ เดือน 7"),
    ("2143-08-31", "แรม 6 ค่ำ เดือน 9"),
    ("2089-12-12", "ขึ้น 10 ค่ำ เดือน 1"),
    ("2340-05-16", "แรม 5 ค่ำ เดือน 6"),
    ("2264-06-10", "ขึ้น 15 ค่ำ เดือน 7"),
    ("1903-01-01", "ขึ้น 3 ค่ำ เดือน 2"),
    ("2460-12-31", "แรม 3 ค่ำ เดือน 1"),
    ("2024-01-01", "แรม 5 ค่ำ เดือน 1"),
    ("2024-12-31", "ขึ้น 2 ค่ำ เดือน 2"),
    ("2020-10-31", "ขึ้น 15 ค่ำ เดือน 12"),
)
# fmt: on


class ToLunarDateTestCase(unittest.TestCase):
    def test_golden(self) -> None:
        for iso, expected in _LUNAR_GOLDEN:
            with self.subTest(date=iso):
                self.assertEqual(
                    to_lunar_date(date.fromisoformat(iso)), expected
                )

    def test_unsupported_range(self) -> None:
        for d in (date(1902, 12, 31), date(2461, 1, 1), date(1, 1, 1)):
            with self.subTest(date=d):
                with self.assertRaisesRegex(
                    NotImplementedError, "^Unsupported date$"
                ):
                    to_lunar_date(d)

    def test_unexpected_last_day(self) -> None:
        with patch.object(
            thai_lunar_date, "last_day_in_year", return_value=353
        ):
            with self.assertRaisesRegex(
                ValueError, "Unexpected last_day value: 353"
            ):
                to_lunar_date(date(1903, 1, 1))

    def test_wrong_input_type(self) -> None:
        with self.assertRaises(AttributeError):
            to_lunar_date(None)  # type: ignore[arg-type]
        with self.assertRaises(AttributeError):
            to_lunar_date("2024-01-01")  # type: ignore[arg-type]
        # datetime is not subtractable from date
        with self.assertRaises(TypeError):
            to_lunar_date(datetime(2024, 1, 1))

    def test_month_helpers(self) -> None:
        self.assertEqual(_month_and_day(1, [29, 30]), (1, 1))
        self.assertEqual(_month_and_day(30, [29, 30]), (2, 1))
        # days beyond the table: last month, remaining days
        self.assertEqual(_month_and_day(100, [29, 30]), (2, 41))
        self.assertEqual(_month_and_day(0, [29, 30]), (2, -59))
        self.assertEqual(_adjust_month(13, 354), 1)
        self.assertEqual(_adjust_month(14, 355), 2)
        self.assertEqual(_adjust_month(5, 354), 5)
        self.assertEqual(_adjust_month(9, 384), 8)
        self.assertEqual(_adjust_month(14, 384), 1)
        self.assertEqual(_adjust_month(8, 384), 8)
        self.assertEqual(_adjust_month(7, 400), 7)

    def test_athikasurathin_solar_leap_year(self) -> None:
        # The argument is a Gregorian (CE) year, as in the rest of the module.
        self.assertTrue(thai_lunar_date.athikasurathin(2000))
        self.assertTrue(thai_lunar_date.athikasurathin(2568))
        self.assertFalse(thai_lunar_date.athikasurathin(2025))
        self.assertTrue(thai_lunar_date.athikasurathin(2024))
        self.assertFalse(thai_lunar_date.athikasurathin(1900))
        self.assertEqual(thai_lunar_date.number_day_in_year(2568), 366)


if __name__ == "__main__":
    unittest.main()
