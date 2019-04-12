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

_HA_DIGITS = "0123456789"
_TH_DIGITS = "๐๑๒๓๔๕๖๗๘๙"
_HA_TH_DIGITS = str.maketrans(_HA_DIGITS, _TH_DIGITS)


_NEED_L10N = "AaBbCcDFGgvXxYy+"  # flags that need localization
_EXTENSIONS = "EO-_0#"  # extension flags


def _padding(n: int, length: int = 2, pad_char: str = "0") -> str:
    str_ = str(n)

    pad_len = length - len(str_)
    if pad_len < 0:
        pad_len = 0

    return (pad_char * pad_len) + str_


def _thai_strftime(datetime: datetime.datetime, fmt_char: str) -> str:
    """
    Conversion support for thai_strftime()
    """
    str_ = ""
    if fmt_char == "A":
        # National representation of the full weekday name
        str_ = thai_full_weekdays[datetime.weekday()]
    elif fmt_char == "a":
        # National representation of the abbreviated weekday
        str_ = thai_abbr_weekdays[datetime.weekday()]
    elif fmt_char == "B":
        # National representation of the full month name
        str_ = thai_full_months[datetime.month - 1]
    elif fmt_char == "b":
        # National representation of the abbreviated month name
        str_ = thai_abbr_months[datetime.month - 1]
    elif fmt_char == "C":
        # Thai Buddhist century (AD+543)/100 + 1 as decimal number;
        str_ = str(int((datetime.year + 543) / 100) + 1)
    elif fmt_char == "c":
        # Locale’s appropriate date and time representation
        # Wed  6 Oct 01:40:00 1976
        # พ   6 ต.ค. 01:40:00 2519  <-- left-aligned weekday, right-aligned day
        str_ = "{:<2} {:>2} {} {} {}".format(
            thai_abbr_weekdays[datetime.weekday()],
            datetime.day,
            thai_abbr_months[datetime.month - 1],
            datetime.strftime("%H:%M:%S"),
            datetime.year + 543,
        )
    elif fmt_char == "D":
        # Equivalent to ``%m/%d/%y''
        str_ = "{}/{}".format(datetime.strftime("%m/%d"), str(datetime.year + 543)[-2:])
    elif fmt_char == "F":
        # Equivalent to ``%Y-%m-%d''
        str_ = "{}-{}".format(str(datetime.year + 543), datetime.strftime("%m-%d"))
    elif fmt_char == "G":
        # ISO 8601 year with century representing the year that contains the greater part of the ISO week (%V). Monday as the first day of the week.
        str_ = str(int(datetime.strftime("%G")) + 543)
    elif fmt_char == "g":
        # Same year as in ``%G'', but as a decimal number without century (00-99).
        str_ = str(int(datetime.strftime("%G")) + 543)[-2:]
    elif fmt_char == "v":
        # BSD extension, ' 6-Oct-1976'
        str_ = "{:>2}-{}-{}".format(
            datetime.day, thai_abbr_months[datetime.month - 1], datetime.year + 543
        )
    elif fmt_char == "X":
        # Locale’s appropriate time representation.
        str_ = datetime.strftime("%H:%M:%S")
    elif fmt_char == "x":
        # Locale’s appropriate date representation.
        str_ = "{}/{}/{}".format(
            _padding(datetime.day), _padding(datetime.month), datetime.year + 543
        )
    elif fmt_char == "Y":
        # Year with century
        str_ = str(datetime.year + 543)
    elif fmt_char == "y":
        # Year without century
        str_ = str(datetime.year + 543)[2:4]
    elif fmt_char == "+":
        # National representation of the date and time (the format is similar to that produced by date(1))
        # Wed  6 Oct 1976 01:40:00
        str_ = "{:<2} {:>2} {} {} {}".format(
            thai_abbr_weekdays[datetime.weekday()],
            datetime.day,
            thai_abbr_months[datetime.month - 1],
            datetime.year + 543,
            datetime.strftime("%H:%M:%S"),
        )
    else:
        # No known localization available, use Python's default
        str_ = datetime.strftime(f"%{fmt_char}")

    return str_


def thai_strftime(
    datetime: datetime.datetime, fmt: str, thaidigit: bool = False
) -> str:
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

    Note 3:
    We trying to make this platform-independent and support extentions as many as possible,
    See these links for strftime() extensions in POSIX, BSD, and GNU libc:
    - Python https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
    - C http://www.cplusplus.com/reference/ctime/strftime/
    - GNU https://metacpan.org/pod/POSIX::strftime::GNU
    - Linux https://linux.die.net/man/3/strftime
    - OpenBSD https://man.openbsd.org/strftime.3
    - FreeBSD https://www.unix.com/man-page/FreeBSD/3/strftime/
    - macOS https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man3/strftime.3.html
    - PHP https://secure.php.net/manual/en/function.strftime.php
    - JavaScript's implementation https://github.com/samsonjs/strftime
    - strftime() quick reference http://www.strftime.net/

    :return: Date and time spelled out in text, with month in Thai name and year in Thai Buddhist era. The year is simply converted from AD by adding 543 (will not accurate for years before 1941 AD, due to change in Thai New Year's Day).
    """
    thaidate_parts = []

    i = 0
    fmt_len = len(fmt)
    while i < fmt_len:
        str_ = ""
        if fmt[i] == "%":
            j = i + 1
            if j < fmt_len:
                fmt_char = fmt[j]
                if fmt_char in _NEED_L10N:  # requires localization?
                    str_ = _thai_strftime(datetime, fmt_char)
                elif fmt_char in _EXTENSIONS:

                    if fmt_char == "-":
                        # GNU libc extension, no padding
                        k = j + 1
                        if k < fmt_len:
                            fmt_char_nopad = fmt[k]
                            if (
                                fmt_char_nopad in _NEED_L10N
                            ):  # check if requires localization
                                str_ = _thai_strftime(datetime, fmt_char_nopad)
                            else:
                                str_ = datetime.strftime(f"%-{fmt_char_nopad}")
                            i = i + 1  # consume char after "-"
                        else:
                            str_ = "-"  # "-" at the end of string has no meaning
                    elif fmt_char == "_":
                        # GNU libc extension, explicitly specify space (" ") for padding
                        # Not implemented yet
                        pass
                    elif fmt_char == "0":
                        # GNU libc extension, explicitly specify zero ("0") for padding
                        # Not implemented yet
                        pass
                    elif fmt_char == "E":
                        # POSIX extension, uses the locale's alternative representation
                        # Not implemented yet
                        pass
                    elif fmt_char == "O":
                        # POSIX extension, uses the locale's alternative numeric symbols
                        # Not implemented yet
                        pass

                elif fmt_char:
                    # the rest of directives, just pass to Python's standard strftime()
                    str_ = datetime.strftime(f"%{fmt_char}")

                i = i + 1  # consume char after "%"
            else:
                str_ = "%"
        else:
            str_ = fmt[i]

        thaidate_parts.append(str_)
        i = i + 1

    thaidate_text = "".join(thaidate_parts)

    if thaidigit:
        thaidate_text = thaidate_text.translate(_HA_TH_DIGITS)

    return thaidate_text


def now_reign_year():
    """
    :return: reign year for Rama X of Chakri dynasty
    """
    now_ = datetime.datetime.now()
    return now_.year - 2015


def reign_year_to_ad(reign_year: int, reign: int) -> int:
    """
    Reign year of Chakri dynasty, Thailand
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
