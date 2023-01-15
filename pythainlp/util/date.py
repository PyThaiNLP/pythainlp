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
    "bc2ad",
    "thai_abbr_months",
    "thai_abbr_weekdays",
    "thai_full_months",
    "thai_full_weekdays",
    "thai_strptime",
    "thaiword_to_date",
]

from datetime import datetime, timedelta
from typing import Union
import re

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo


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
thai_full_month_lists = [
    ["มกราคม", "มกรา", "ม.ค.", "01", "1"],
    ["กุมภาพันธ์", "กุมภา", "ก.w.", "02", "2"],
    ["มีนาคม", "มีนา", "มี.ค.", "03", "3"],
    ["เมษายน", "เมษา", "เม.ย.", "04", "4"],
    ["พฤษภาคม", "พฤษภา", "พ.ค.", "05", "5"],
    ["มิถุนายน", "มิถุนา", "มิ.ย.", "06", "6"],
    ["กรกฎาคม", "ก.ค.", "07", "7"],
    ["สิงหาคม", "สิงหา", "ส.ค.", "08", "8"],
    ["กันยายน", "กันยา", "ก.ย.", "09", "9"],
    ["ตุลาคม", "ตุลา", "ต.ค.", "10"],
    ["พฤศจิกายน", "พฤศจิกา", "พ.ย.", "11"],
    ["ธันวาคม", "ธันวา", "ธ.ค.", "12"]
]
thai_full_month_lists_regex = "("+'|'.join(
    [str('|'.join([j for j in i])) for i in thai_full_month_lists]
)+")"
year_all_regex = "(\d\d\d\d|\d\d)"
dates_list = "("+'|'.join(
    [""+str(i)+"" for i in range(32,0,-1)]
)+")"

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


def bc2ad(year: str) -> str:
    """
    Convert Buddhist calendar year to Anno Domin year

    *Warning: This function works properly only after 1941.
    because Thailand has change the Thai calendar in 1941.
    If you are the time traveler or the historian, you should care about the correct calendar.
    - https://krunongpasathai.com/2017/12/25/do-you-know-when-thailand-changed-its-new-year-to-the-1st-of-january/
    """
    return str(int(year) - 543)


def _find_month(text):
    for i,m in enumerate(thai_full_month_lists):
        for j in m:
            if j in text:
                return i+1


def thai_strptime(text, type, tzinfo=ZoneInfo("Asia/Bangkok")):
    d = ""
    m = ""
    y= ""
    type = type.replace("%-m","%m")
    type = type.replace("%-d","%d")
    type = type.replace("%b","%B")
    type = type.replace("%-y","%y")
    data = {}
    _old = type
    if "%d" in type:
        type = type.replace("%d", dates_list)
    if "%B" in type:
        type = type.replace("%B", thai_full_month_lists_regex)
    if "%Y" in type:
        type = type.replace("%Y", year_all_regex)
    if "%H" in type:
        type = type.replace("%H", "(\d\d)")
    if "%M" in type:
        type = type.replace("%M", "(\d\d)")
    if "%S" in type:
        type = type.replace("%S", "(\d\d|\d)")
    if "%f" in type:
        type = type.replace("%f", "(\d+)")
    keys = [i.strip().strip('-').strip(':').strip('.') for i in _old.split("%") if i!='']
    y = re.findall(type,text)
    
    data = {i:''.join(list(j)) for i,j in zip(keys,y[0])}
    H=0
    M=0
    S=0
    f=0
    d=data['d']
    m=_find_month(data['B'])
    y=data['Y']
    if "H" in keys:
        H = data['H']
    if "M" in keys:
        M = data['M']
    if "S" in keys:
        S = data['S']
    if "f" in keys:
        f = data['f']
    if int(y) < 100:
        y = "25"+y
    if int(y) > 2112:
        y = bc2ad(y)
    return datetime(
        year=int(y),
        month=int(m),
        day=int(d),
        hour=int(H),
        minute=int(M),
        second=int(S),
        microsecond=int(f),
        tzinfo=tzinfo
    )


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
