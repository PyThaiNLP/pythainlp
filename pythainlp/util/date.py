# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Thai date and time conversion.

Note: It does not take into account the change of New Year's Day in
Thailand.
"""

from __future__ import annotations

from typing import Optional, Union

__all__: list[str] = [
    "convert_years",
    "thai_abbr_months",
    "thai_abbr_weekdays",
    "thai_full_months",
    "thai_full_weekdays",
    "thai_strptime",
    "thaiword_to_date",
]

import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from pythainlp.util._calendar import _ERA_OFFSETS_FROM_BE

thai_abbr_weekdays: list[str] = ["จ", "อ", "พ", "พฤ", "ศ", "ส", "อา"]
thai_full_weekdays: list[str] = [
    "วันจันทร์",
    "วันอังคาร",
    "วันพุธ",
    "วันพฤหัสบดี",
    "วันศุกร์",
    "วันเสาร์",
    "วันอาทิตย์",
]

thai_abbr_months: list[str] = [
    "ม.ค.",
    "ก.พ.",
    "มี.ค.",
    "เม.ย.",
    "พ.ค.",
    "มิ.ย.",
    "ก.ค.",
    "ส.ค.",
    "ก.ย.",
    "ต.ค.",
    "พ.ย.",
    "ธ.ค.",
]
thai_full_months: list[str] = [
    "มกราคม",
    "กุมภาพันธ์",
    "มีนาคม",
    "เมษายน",
    "พฤษภาคม",
    "มิถุนายน",
    "กรกฎาคม",
    "สิงหาคม",
    "กันยายน",
    "ตุลาคม",
    "พฤศจิกายน",
    "ธันวาคม",
]
thai_full_month_lists: list[list[str]] = [
    ["มกราคม", "มกรา", "ม.ค.", "01", "1"],
    ["กุมภาพันธ์", "กุมภา", "ก.พ.", "02", "2"],
    ["มีนาคม", "มีนา", "มี.ค.", "03", "3"],
    ["เมษายน", "เมษา", "เม.ย.", "04", "4"],
    ["พฤษภาคม", "พฤษภา", "พ.ค.", "05", "5"],
    ["มิถุนายน", "มิถุนา", "มิ.ย.", "06", "6"],
    ["กรกฎาคม", "ก.ค.", "07", "7"],
    ["สิงหาคม", "สิงหา", "ส.ค.", "08", "8"],
    ["กันยายน", "กันยา", "ก.ย.", "09", "9"],
    ["ตุลาคม", "ตุลา", "ต.ค.", "10"],
    ["พฤศจิกายน", "พฤศจิกา", "พ.ย.", "11"],
    ["ธันวาคม", "ธันวา", "ธ.ค.", "12"],
]
thai_full_month_lists_regex: str = (
    "(" + "|".join(["|".join(i) for i in thai_full_month_lists]) + ")"
)
year_all_regex: str = r"(\d\d\d\d|\d\d)"
dates_list: str = (
    "("
    + "|".join(
        list(map(str, range(32, 0, -1))) + ["0" + str(i) for i in range(1, 10)]
    )
    + ")"
)

_DAY: dict[str, int] = {
    "วันนี้": 0,
    "คืนนี้": 0,
    "พรุ่งนี้": 1,
    "วันพรุ่งนี้": 1,
    "คืนถัดจากนี้": 1,
    "คืนหน้า": 1,
    "มะรืน": 2,
    "มะรืนนี้": 2,
    "วันมะรืนนี้": 2,
    "ถัดจากพรุ่งนี้": 2,
    "ถัดจากวันพรุ่งนี้": 2,
    "เมื่อวาน": -1,
    "เมื่อวานนี้": -1,
    "วานนี้": -1,
    "เมื่อคืน": -1,
    "เมื่อคืนนี้": -1,
    "วานซืน": -2,
    "เมื่อวานซืน": -2,
    "เมื่อวานของเมื่อวาน": -2,
}


def _is_known_era(era: object) -> bool:
    return isinstance(era, str) and era in _ERA_OFFSETS_FROM_BE


def convert_years(year: str, src: str = "be", target: str = "ad") -> str:
    """
    Convert a year from one era to another.

    :param str year: year, as an integer string
    :param str src: source era
    :param str target: target era
    :return: converted year
    :rtype: str
    :raises NotImplementedError: if ``src`` or ``target`` is not a
        supported era
    :raises ValueError: if ``year`` is not an integer string

    Options for ``src`` and ``target``:
        * *be* - Buddhist Era
        * *ad* - Anno Domini
        * *re* - Rattanakosin Era
        * *ah* - Anno Hegirae

    **Warning**: This function works properly only after 1941,
    because Thailand changed its calendar in 1941.
    Historians need to take the correct calendar into account.

    :Example:

        >>> from pythainlp.util import convert_years
        >>> # Convert Buddhist Era (BE) to Anno Domini (AD)
        >>> convert_years("2566", src="be", target="ad")
        '2023'
        >>> # Convert AD to BE
        >>> convert_years("2023", src="ad", target="be")
        '2566'
        >>> # Convert BE to Rattanakosin Era (RE)
        >>> convert_years("2566", src="be", target="re")
        '242'
        >>> # The same era returns the year as a normalized integer string
        >>> convert_years("2566", src="be", target="be")
        '2566'
    """
    if not _is_known_era(src) or not _is_known_era(target):
        raise NotImplementedError(
            f"This function doesn't support {src} to {target}"
        )
    be_year = int(year) - _ERA_OFFSETS_FROM_BE[src]
    return str(be_year + _ERA_OFFSETS_FROM_BE[target])


def _find_month(text: str) -> int:
    for i, m in enumerate(thai_full_month_lists):
        for j in m:
            if j in text:
                return i + 1
    return 0  # Not found in list


# Directives of thai_strptime() and their regular expressions.
# The order matters: each replacement is applied in turn.
_STRPTIME_REGEX: tuple[tuple[str, str], ...] = (
    ("%d", dates_list),
    ("%B", thai_full_month_lists_regex),
    ("%Y", year_all_regex),
    ("%H", r"(\d\d|\d)"),
    ("%M", r"(\d\d|\d)"),
    ("%S", r"(\d\d|\d)"),
    ("%f", r"(\d+)"),
)
_TIME_KEYS: tuple[str, ...] = ("H", "M", "S", "f")


def _fmt_to_regex(fmt: str) -> str:
    for directive, regex in _STRPTIME_REGEX:
        fmt = fmt.replace(directive, regex)
    return fmt


def _fmt_keys(fmt: str) -> list[str]:
    """Names of the directives in ``fmt``, with the separators removed."""
    return [
        i.strip().strip("-").strip(":").strip(".")
        for i in fmt.split("%")
        if i != ""
    ]


def _full_year(y: str, year: str, add_year: Optional[int]) -> str:
    """
    Normalize a year text, and convert a BE year to an AD year.

    Add a year below 100 to ``add_year``, or to 2500 (BE) or 2000 (AD)
    if ``add_year`` is None.
    """
    if int(y) < 100 and year in ("be", "ad"):
        if add_year is None:
            add_year = 2500 if year == "be" else 2000
        y = str(int(add_year) + int(y))
    if year == "be":
        y = convert_years(y, src="be", target="ad")
    return y


def thai_strptime(
    text: str,
    fmt: str,
    year: str = "be",
    add_year: Optional[int] = None,
    tzinfo: Optional[ZoneInfo] = ZoneInfo("Asia/Bangkok"),  # noqa: B008
) -> datetime:
    """
    Parse Thai date and time text into a :class:`datetime.datetime`.

    :param str text: text containing date and time
    :param str fmt: string containing date and time directives
    :param str year: era of the year in the text
        (*ad* for Anno Domini, *be* for Buddhist Era)
    :param Optional[int] add_year: year to add to a two-digit year
        (default is None)
    :param Optional[zoneinfo.ZoneInfo] tzinfo: time zone
        (default is Asia/Bangkok)
    :return: parsed date and time
    :rtype: datetime.datetime

    Supported directives in ``fmt``:
        * *%d* - Day (1 - 31)
        * *%B* - Thai month (03, 3, มี.ค., or มีนาคม)
        * *%Y* - Year (66, 2566, or 2023)
        * *%H* - Hour (0 - 23)
        * *%M* - Minute (0 - 59)
        * *%S* - Second (0 - 59)
        * *%f* - Microsecond

    :Example:

        >>> from pythainlp.util import thai_strptime

        >>> thai_strptime("15 ก.ค. 2565 09:00:01", "%d %B %Y %H:%M:%S")
        datetime.datetime(2022, 7, 15, 9, 0, 1, tzinfo=zoneinfo.ZoneInfo(key='Asia/Bangkok'))
    """
    fmt = fmt.replace("%-m", "%m")
    fmt = fmt.replace("%-d", "%d")
    fmt = fmt.replace("%b", "%B")
    fmt = fmt.replace("%-y", "%y")
    keys = _fmt_keys(fmt)
    y_matches = re.findall(_fmt_to_regex(fmt), text)

    data = {i: "".join(list(j)) for i, j in zip(keys, y_matches[0])}
    d = data["d"]
    m: int = _find_month(data["B"])
    y = data["Y"]
    time_parts: list[Union[int, str]] = [
        data[name] if name in keys else 0 for name in _TIME_KEYS
    ]
    hour, minute, second, f = time_parts
    y = _full_year(y, year, add_year)
    return datetime(
        year=int(y),
        month=m,
        day=int(d),
        hour=int(hour),
        minute=int(minute),
        second=int(second),
        microsecond=int(f),
        tzinfo=tzinfo,
    )


def now_reign_year() -> int:
    """
    Return the current reign year of the 10th King of Chakri dynasty.

    :return: reign year of the 10th King of Chakri dynasty
    :rtype: int

    :Example:

        >>> from pythainlp.util import now_reign_year  # doctest: +SKIP
        >>> text = "เป็นปีที่ {reign_year} ในรัชกาลปัจจุบัน"\\  # doctest: +SKIP
        ...     .format(reign_year=now_reign_year())
        >>> print(text)  # doctest: +SKIP
        เป็นปีที่ 11 ในรัชกาลปัจจุบัน
    """
    now_ = datetime.now()
    return now_.year - 2015  # hard coded


def reign_year_to_ad(reign_year: int, reign: int) -> int:
    """
    Convert a reign year to an AD year.

    Return the AD year for a reign year of the 7th to 10th King of
    Chakri dynasty, Thailand.
    For instance, the AD year of the 4th reign year of the 10th King is
    2019.

    :param int reign_year: reign year of the King
    :param int reign: reign of the King (7, 8, 9, or 10)
    :return: AD year of the given reign and reign year
    :rtype: int

    :Example:

        >>> from pythainlp.util import reign_year_to_ad
        >>> print(
        ...     "The 4th reign year of the King Rama X is in",
        ...     reign_year_to_ad(4, 10),
        ... )
        The 4th reign year of the King Rama X is in 2019
        >>> print(
        ...     "The 1st reign year of the King Rama IX is in",
        ...     reign_year_to_ad(1, 9),
        ... )
        The 1st reign year of the King Rama IX is in 1946
    """
    ad = 0
    if int(reign) == 10:
        ad = int(reign_year) + 2015
    elif int(reign) == 9:
        ad = int(reign_year) + 1945
    elif int(reign) == 8:
        ad = int(reign_year) + 1928
    elif int(reign) == 7:
        ad = int(reign_year) + 1924
    return ad


def thaiword_to_date(
    text: str, date: Optional[datetime] = None
) -> Optional[datetime]:
    """
    Convert Thai relative date to :class:`datetime.datetime`.

    :param str text: Thai text containing a relative date
    :param datetime.datetime date: reference date
        (default is datetime.datetime.now())
    :return: date and time if it can be calculated, otherwise None
    :rtype: Optional[datetime.datetime]

    :Example:

        >>> from datetime import datetime
        >>> from pythainlp.util import thaiword_to_date

        >>> thaiword_to_date("พรุ่งนี้", datetime(2024, 1, 31))
        datetime.datetime(2024, 2, 1, 0, 0)
        >>> thaiword_to_date("เมื่อวาน", datetime(2024, 1, 31))
        datetime.datetime(2024, 1, 30, 0, 0)
        >>> print(thaiword_to_date("ไม่มีคำนี้"))
        None
    """
    if text not in _DAY:
        return None

    day_num = _DAY.get(text, 0)

    if not date:
        date = datetime.now()

    return date + timedelta(days=day_num)
