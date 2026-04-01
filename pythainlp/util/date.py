# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai date/time conversion.

Note: It does not take into account the change of new year's day in Thailand
"""

# BE คือ พ.ศ.
# AD คือ ค.ศ.
# AH ปีฮิจเราะห์ศักราชเป็นปีพุทธศักราช จะต้องบวกด้วย 1122
# ไม่ได้รองรับปี พ.ศ. ก่อนการเปลี่ยนวันขึ้นปีใหม่ของประเทศไทย
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


def convert_years(year: str, src: str = "be", target: str = "ad") -> str:
    """Convert years

    :param int year: Year
    :param str src: The source year
    :param str target: The target year
    :return: The converted year
    :rtype: str

    **Options for year**
        * *be* - Buddhist calendar
        * *ad* - Anno Domini
        * *re* - Rattanakosin era
        * *ah* - Anno Hejira

    **Warning**: This function works properly only after 1941 \
    because Thailand has change the Thai calendar in 1941.
    If you are the time traveler or the historian, \
    you should care about the correct calendar.

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
    """
    output_year = None
    if src == "be":
        # พ.ศ. - 543  = ค.ศ.
        if target == "ad":
            output_year = str(int(year) - 543)
        # พ.ศ. - 2324 = ร.ศ.
        elif target == "re":
            output_year = str(int(year) - 2324)
        # พ.ศ. - 1122 = ฮ.ศ.
        elif target == "ah":
            output_year = str(int(year) - 1122)
    elif src == "ad":
        # ค.ศ. + 543 = พ.ศ.
        if target == "be":
            output_year = str(int(year) + 543)
        # ค.ศ. + 543 - 2324 = ร.ศ.
        elif target == "re":
            output_year = str(int(year) + 543 - 2324)
        # ค.ศ. +543- 1122 = ฮ.ศ.
        elif target == "ah":
            output_year = str(int(year) + 543 - 1122)
    elif src == "re":
        # ร.ศ. + 2324 = พ.ศ.
        if target == "be":
            output_year = str(int(year) + 2324)
        # ร.ศ. + 2324 - 543 = ค.ศ.
        elif target == "ad":
            output_year = str(int(year) + 2324 - 543)
        # ร.ศ. + 2324 - 1122 = ฮ.ศ.
        elif target == "ah":
            output_year = str(int(year) + 2324 - 1122)
    elif src == "ah":
        # ฮ.ศ. + 1122 = พ.ศ.
        if target == "be":
            output_year = str(int(year) + 1122)
        # ฮ.ศ. +1122 - 543= ค.ศ.
        elif target == "ad":
            output_year = str(int(year) + 1122 - 543)
        # ฮ.ศ. +1122 - 2324 = ร.ศ.
        elif target == "re":
            output_year = str(int(year) + 1122 - 2324)
    if output_year is None:
        raise NotImplementedError(
            f"This function doesn't support {src} to {target}"
        )
    return output_year


def _find_month(text: str) -> int:
    for i, m in enumerate(thai_full_month_lists):
        for j in m:
            if j in text:
                return i + 1
    return 0  # Not found in list


def thai_strptime(
    text: str,
    fmt: str,
    year: str = "be",
    add_year: Optional[int] = None,
    tzinfo: Optional[ZoneInfo] = ZoneInfo("Asia/Bangkok"),
) -> datetime:
    """Thai strptime

    :param str text: text
    :param str fmt: string containing date and time directives
    :param str year: year of the text \
        (ad is Anno Domini and be is Buddhist Era)
    :param Optional[int] add_year: add to year when converting to ad. Default is None.
    :param object tzinfo: tzinfo (default is Asia/Bangkok)
    :return: The year that is converted to datetime.datetime
    :rtype: datetime.datetime

    The fmt chars that are supported:
        * *%d* - Day (1 - 31)
        * *%B* - Thai month (03, 3, มี.ค., or มีนาคม)
        * *%Y* - Year (66, 2566, or 2023)
        * *%H* - Hour (0 - 23)
        * *%M* - Minute (0 - 59)
        * *%S* - Second (0 - 59)
        * *%f* - Microsecond

    :Example:

        >>> from pythainlp.util import thai_strptime

        >>> thai_strptime("15 ก.ค. 2565 09:00:01","%d %B %Y %H:%M:%S")
        datetime.datetime(2022, 7, 15, 9, 0, 1, tzinfo=zoneinfo.ZoneInfo(key='Asia/Bangkok'))
    """
    fmt = fmt.replace("%-m", "%m")
    fmt = fmt.replace("%-d", "%d")
    fmt = fmt.replace("%b", "%B")
    fmt = fmt.replace("%-y", "%y")
    data = {}
    _old = fmt
    if "%d" in fmt:
        fmt = fmt.replace("%d", dates_list)
    if "%B" in fmt:
        fmt = fmt.replace("%B", thai_full_month_lists_regex)
    if "%Y" in fmt:
        fmt = fmt.replace("%Y", year_all_regex)
    if "%H" in fmt:
        fmt = fmt.replace("%H", r"(\d\d|\d)")
    if "%M" in fmt:
        fmt = fmt.replace("%M", r"(\d\d|\d)")
    if "%S" in fmt:
        fmt = fmt.replace("%S", r"(\d\d|\d)")
    if "%f" in fmt:
        fmt = fmt.replace("%f", r"(\d+)")
    keys = [
        i.strip().strip("-").strip(":").strip(".")
        for i in _old.split("%")
        if i != ""
    ]
    y_matches = re.findall(fmt, text)

    data = {i: "".join(list(j)) for i, j in zip(keys, y_matches[0])}
    hour: Union[int, str] = 0
    minute: Union[int, str] = 0
    second: Union[int, str] = 0
    f: Union[int, str] = 0
    d = data["d"]
    m: int = _find_month(data["B"])
    y = data["Y"]
    if "H" in keys:
        hour = data["H"]
    if "M" in keys:
        minute = data["M"]
    if "S" in keys:
        second = data["S"]
    if "f" in keys:
        f = data["f"]
    if int(y) < 100 and year == "be":
        if add_year is None:
            y = str(2500 + int(y))
        else:
            y = str(int(add_year) + int(y))
    elif int(y) < 100 and year == "ad":
        if add_year is None:
            y = str(2000 + int(y))
        else:
            y = str(int(add_year) + int(y))
    if year == "be":
        y = convert_years(y, src="be", target="ad")
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
    """Return the reign year of the 10th King of Chakri dynasty.

    :return: reign year of the 10th King of Chakri dynasty.
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
    """Convert reign year to AD.

    Return AD year according to the reign year for
    the 7th to 10th King of Chakri dynasty, Thailand.
    For instance, the AD year of the 4th reign year of the 10th King is 2019.

    :param int reign_year: reign year of the King
    :param int reign: the reign of the King (i.e. 7, 8, 9, and 10)

    :return: the year in AD of the King given the reign and reign year.
    :rtype: int

    :Example:

        >>> from pythainlp.util import reign_year_to_ad
        >>> print("The 4th reign year of the King Rama X is in",
        ...     reign_year_to_ad(4, 10))
        The 4th reign year of the King Rama X is in 2019
        >>> print("The 1st reign year of the King Rama IX is in",
        ...     reign_year_to_ad(1, 9))
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
    """Convert Thai relative date to :class:`datetime.datetime`.

    :param str text: Thai text containing relative date
    :param datetime.datetime date: date (default is datetime.datetime.now())

    :return: datetime object, if it can be calculated. Otherwise, None.
    :rtype: datetime.datetime

    :Example:

        thaiword_to_date("พรุ่งนี้")
        # output:
        # datetime of tomorrow
    """
    if text not in _DAY:
        return None

    day_num = _DAY.get(text, 0)

    if not date:
        date = datetime.now()

    return date + timedelta(days=day_num)
