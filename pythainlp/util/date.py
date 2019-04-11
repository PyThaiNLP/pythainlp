# -*- coding: utf-8 -*-
"""
Thai date/time conversion and formatting

Note: Does not take into account the change of new year's day in Thailand
"""
# BE คือ พ.ศ.
# AD คือ ค.ศ.
# AH ปีฮิจเราะห์ศักราชเป็นปีพุทธศักราช จะต้องบวกด้วย 1122
# ไม่ได้รองรับปี พ.ศ. ก่อนการเปลี่ยนวันขึ้นปีใหม่ของประเทศไทย

import datetime

__all__ = [
    "thai_abbr_months",
    "thai_abbr_weekdays",
    "thai_full_months",
    "thai_full_weekdays",
    "thai_strftime",
]

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

_HA_TH_DIGITS = str.maketrans("0123456789", "๐๑๒๓๔๕๖๗๘๙")


# Conversion support for thai_strftime()
def _thai_strftime(datetime, fmt_c: str) -> str:
    text = ""
    if fmt_c == "a":  # abbreviated weekday
        text = thai_abbr_weekdays[datetime.weekday()]
    elif fmt_c == "A":  # full weekday
        text = thai_full_weekdays[datetime.weekday()]
    elif fmt_c == "b":  # abbreviated month
        text = thai_abbr_months[datetime.month - 1]
    elif fmt_c == "B":  # full month
        text = thai_full_months[datetime.month - 1]
    elif fmt_c == "y":  # year without century
        text = str(datetime.year + 543)[2:4]
    elif fmt_c == "Y":  # year with century
        text = str(datetime.year + 543)
    elif fmt_c == "c":
        # Wed  6 Oct 01:40:00 1976
        # พ   6 ต.ค. 01:40:00 2519  <-- left-aligned weekday, right-aligned day
        text = "{:<2} {:>2} {} {} {}".format(
            thai_abbr_weekdays[datetime.weekday()],
            datetime.day,
            thai_abbr_months[datetime.month - 1],
            datetime.strftime("%H:%M:%S"),
            datetime.year + 543,
        )
    elif fmt_c == "v":  # undocumented format: ' 6-Oct-1976'
        text = "{:>2}-{}-{}".format(
            datetime.day, thai_abbr_months[datetime.month - 1], datetime.year + 543
        )
    else:  # matched with nothing
        text = datetime.strftime("%{}".format(fmt_c))

    return text


def thai_strftime(datetime, fmt: str, thaidigit=False) -> str:
    """
    Thai date and time string formatter

    Formatting directives similar to datetime.strftime()

    Will use Thai names and Thai Buddhist Era for these directives:
    - %a abbreviated weekday name
    - %A full weekday name
    - %b abbreviated month name
    - %B full month name
    - %y year without century
    - %Y year with century
    - %c date and time representation
    - %v short date representation (undocumented)

    Other directives will be passed to datetime.strftime()

    Note 1:
    The Thai Buddhist Era (BE) year is simply converted from AD by adding 543.
    This is certainly not accurate for years before 1941 AD,
    due to the change in Thai New Year's Day.

    Note 2:
    This meant to be an interrim solution, since Python standard's locale module
    (which relied on C's strftime()) does not support "th" or "th_TH" locale yet.
    If supported, we can just locale.setlocale(locale.LC_TIME, "th_TH") and
    then use native datetime.strftime().

    :return: Date and time spelled out, with day and month names in Thai and year in Thai Buddhist Era (BE).
    """
    thaidate_parts = []

    i = 0
    fmt_len = len(fmt)
    while i < fmt_len:
        text = ""
        if fmt[i] == "%":
            j = i + 1
            if j < fmt_len:
                fmt_c = fmt[j]
                if fmt_c in "aAbByYcv":  # weekday/month names, years: to be localized
                    text = _thai_strftime(datetime, fmt_c)
                elif fmt_c == "-":  # no padding day or month
                    k = j + 1
                    if k < fmt_len:
                        fmt_c_nopad = fmt[k]
                        if fmt_c_nopad in "aAbByYcv":  # check if requires localization
                            text = _thai_strftime(datetime, fmt_c_nopad)
                        else:
                            text = datetime.strftime("%-{}".format(fmt_c_nopad))
                        i = i + 1  # consume char after "-"
                    else:
                        text = "-"
                elif fmt_c:
                    text = datetime.strftime("%{}".format(fmt_c))

                i = i + 1  # consume char after "%"
            else:
                text = "%"
        else:
            text = fmt[i]

        thaidate_parts.append(text)
        i = i + 1

    thaidate_text = "".join(thaidate_parts)

    if thaidigit:
        thaidate_text = thaidate_text.translate(_HA_TH_DIGITS)

    return thaidate_text


def now_reign_year():
    """
    :return: now year reign for King.
    """
    now_ = datetime.datetime.now()
    return now_.year - 2015


def reign_year_to_ad(reign_year, reign):
    if int(reign) == 10:
        ad = int(reign_year) + 2015
    elif int(reign) == 9:
        ad = int(reign_year) + 1945
    elif int(reign) == 8:
        ad = int(reign_year) + 1928
    elif int(reign) == 7:
        ad = int(reign_year) + 1924
    return ad
