# -*- coding: utf-8 -*-
"""
Thai date/time conversion.

Note: Does not take into account the change of new year's day in Thailand
"""

# BE คือ พ.ศ.
# AD คือ ค.ศ.
# AH ปีฮิจเราะห์ศักราชเป็นปีพุทธศักราช จะต้องบวกด้วย 1122
# ไม่ได้รองรับปี พ.ศ. ก่อนการเปลี่ยนวันขึ้นปีใหม่ของประเทศไทย

__all__ = [
    "thai_abbr_months",
    "thai_abbr_weekdays",
    "thai_full_months",
    "thai_full_weekdays",
    "thaiword_to_date",
]

from datetime import datetime, timedelta
from typing import Union

thai_abbr_weekdays = ["จ", "อ", "พ", "พฤ", "ศ", "ส", "อา"]
thai_full_weekdays = [
    "วันจันทร์",
    "วันอังคาร",
    "วันพุธ",
    "วันพฤหัสบดี",
    "วันศุกร์",
    "วันเสาร์",
    "วันอาทิตย์",
]

thai_abbr_months = [
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
thai_full_months = [
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

_DAY = {
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


def now_reign_year() -> int:
    """
    Return the reign year of the 10th King of Chakri dynasty.

    :return: reign year of the 10th King of Chakri dynasty.
    :rtype: int

    :Example:
    ::

        from pythainlp.util import now_reign_year

        text = "เป็นปีที่ {reign_year} ในรัชกาลปัจจุบัน"\\
            .format(reign_year=now_reign_year())

        print(text)
        # output: เป็นปีที่ 4 ในรัชการปัจจุบัน
    """
    now_ = datetime.now()
    return now_.year - 2015


def reign_year_to_ad(reign_year: int, reign: int) -> int:
    """
    Convert reigh year to AD.

    Return AD year according to the reign year for
    the 7th to 10th King of Chakri dynasty, Thailand.
    For instance, the AD year of the 4th reign year of the 10th King is 2019.

    :param int reign_year: reign year of the King
    :param int reign: the reign of the King (i.e. 7, 8, 9, and 10)

    :return: the year in AD of the King given the reign and reign year.
    :rtype: int

    :Example:
    ::

        from pythainlp.util import reign_year_to_ad

        print("The 4th reign year of the King Rama X is in", \\
            reign_year_to_ad(4, 10))
        # output: The 4th reign year of the King Rama X is in 2019

        print("The 1st reign year of the King Rama IX is in", \\
            reign_year_to_ad(1, 9))
        # output: The 4th reign year of the King Rama X is in 1946
    """
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
    text: str, date: datetime = None
) -> Union[datetime, None]:
    """
    Convert Thai relative date to :class:`datetime.datetime`.

    :param str text: Thai text contains relative date
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

    day_num = _DAY.get(text)

    if not date:
        date = datetime.now()

    return date + timedelta(days=day_num)
