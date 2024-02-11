# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Thai date/time formatting.
"""
import warnings
from datetime import datetime
from string import digits

from pythainlp import thai_digits
from pythainlp.util.date import (
    thai_abbr_months,
    thai_abbr_weekdays,
    thai_full_months,
    thai_full_weekdays,
)

__all__ = [
    "thai_strftime",
]

_HA_TH_DIGITS = str.maketrans(digits, thai_digits)
_BE_AD_DIFFERENCE = 543

_NEED_L10N = "AaBbCcDFGgvXxYy+"  # flags that need localization
_EXTENSIONS = "EO-_0^#"  # extension flags


def _std_strftime(dt_obj: datetime, fmt_char: str) -> str:
    """
    Standard datetime.strftime() with normalization and exception handling.
    """
    str_ = ""
    try:
        str_ = dt_obj.strftime(f"%{fmt_char}")
        if not str_ or str_ == "%{}".format(fmt_char):
            # normalize outputs for unsupported directives
            # in different platforms
            # "%Q" may result "%Q", "Q", or "", make it "Q"
            str_ = fmt_char
    except ValueError as err:
        # Unsupported directives may raise ValueError on Windows,
        # in that case just use the fmt_char
        warnings.warn(
            (
                f"String format directive unknown/not support: %{fmt_char}"
                f"The system raises this ValueError: {err}"
            ),
            UserWarning,
        )
        str_ = fmt_char
    return str_


def _thai_strftime(dt_obj: datetime, fmt_char: str) -> str:
    """
    Conversion support for thai_strftime().

    The fmt_char should be in _NEED_L10N when calling this function.
    """
    str_ = ""
    if fmt_char == "A":
        # National representation of the full weekday name
        str_ = thai_full_weekdays[dt_obj.weekday()]
    elif fmt_char == "a":
        # National representation of the abbreviated weekday
        str_ = thai_abbr_weekdays[dt_obj.weekday()]
    elif fmt_char == "B":
        # National representation of the full month name
        str_ = thai_full_months[dt_obj.month - 1]
    elif fmt_char == "b":
        # National representation of the abbreviated month name
        str_ = thai_abbr_months[dt_obj.month - 1]
    elif fmt_char == "C":
        # Thai Buddhist century (AD+543)/100 + 1 as decimal number;
        str_ = str(int((dt_obj.year + _BE_AD_DIFFERENCE) / 100) + 1).zfill(2)
    elif fmt_char == "c":
        # Locale's appropriate date and time representation
        # Wed  6 Oct 01:40:00 1976
        # พ   6 ต.ค. 01:40:00 2519  <-- left-aligned weekday, right-aligned day
        str_ = "{:<2} {:>2} {} {} {}".format(
            thai_abbr_weekdays[dt_obj.weekday()],
            dt_obj.day,
            thai_abbr_months[dt_obj.month - 1],
            dt_obj.strftime("%H:%M:%S"),
            str(dt_obj.year + _BE_AD_DIFFERENCE).zfill(4),
        )
    elif fmt_char == "D":
        # Equivalent to ``%m/%d/%y''
        str_ = "{}/{}".format(
            dt_obj.strftime("%m/%d"),
            (str(dt_obj.year + _BE_AD_DIFFERENCE)[-2:]).zfill(2),
        )
    elif fmt_char == "F":
        # Equivalent to ``%Y-%m-%d''
        str_ = "{}-{}".format(
            str(dt_obj.year + _BE_AD_DIFFERENCE).zfill(4),
            dt_obj.strftime("%m-%d"),
        )
    elif fmt_char == "G":
        # ISO 8601 year with century representing the year that contains
        # the greater part of the ISO week (%V). Monday as the first day
        # of the week.
        str_ = str(int(dt_obj.strftime("%G")) + _BE_AD_DIFFERENCE).zfill(4)
    elif fmt_char == "g":
        # Same year as in ``%G'',
        # but as a decimal number without century (00-99).
        str_ = (
            str(int(dt_obj.strftime("%G")) + _BE_AD_DIFFERENCE)[-2:]
        ).zfill(2)
    elif fmt_char == "v":
        # BSD extension, ' 6-Oct-1976'
        str_ = "{:>2}-{}-{}".format(
            dt_obj.day,
            thai_abbr_months[dt_obj.month - 1],
            str(dt_obj.year + _BE_AD_DIFFERENCE).zfill(4),
        )
    elif fmt_char == "X":
        # Locale’s appropriate time representation.
        str_ = dt_obj.strftime("%H:%M:%S")
    elif fmt_char == "x":
        # Locale’s appropriate date representation.
        str_ = "{}/{}/{}".format(
            str(dt_obj.day).zfill(2),
            str(dt_obj.month).zfill(2),
            str(dt_obj.year + _BE_AD_DIFFERENCE).zfill(4),
        )
    elif fmt_char == "Y":
        # Year with century
        str_ = (str(dt_obj.year + _BE_AD_DIFFERENCE)).zfill(4)
    elif fmt_char == "y":
        # Year without century
        str_ = (str(dt_obj.year + _BE_AD_DIFFERENCE)[-2:]).zfill(2)
    elif fmt_char == "+":
        # National representation of the date and time
        # (the format is similar to that produced by date(1))
        # Wed  6 Oct 1976 01:40:00
        str_ = "{:<2} {:>2} {} {} {}".format(
            thai_abbr_weekdays[dt_obj.weekday()],
            dt_obj.day,
            thai_abbr_months[dt_obj.month - 1],
            dt_obj.year + _BE_AD_DIFFERENCE,
            dt_obj.strftime("%H:%M:%S"),
        )
    else:
        # No known localization available, use Python's default
        str_ = _std_strftime(dt_obj, fmt_char)

    return str_


def thai_strftime(
    dt_obj: datetime,
    fmt: str = "%-d %b %y",
    thaidigit: bool = False,
) -> str:
    """
    Convert :class:`datetime.datetime` into Thai date and time format.

    The formatting directives are similar to :func:`datatime.strrftime`.

    This function uses Thai names and Thai Buddhist Era for these directives:
        * **%a** - abbreviated weekday name
          (i.e. "จ", "อ", "พ", "พฤ", "ศ", "ส", "อา")
        * **%A** - full weekday name
          (i.e. "วันจันทร์", "วันอังคาร", "วันเสาร์", "วันอาทิตย์")
        * **%b** - abbreviated month name
          (i.e. "ม.ค.","ก.พ.","มี.ค.","เม.ย.","พ.ค.","มิ.ย.", "ธ.ค.")
        * **%B** - full month name
          (i.e. "มกราคม", "กุมภาพันธ์", "พฤศจิกายน", "ธันวาคม",)
        * **%y** - year without century (i.e. "56", "10")
        * **%Y** - year with century (i.e. "2556", "2410")
        * **%c** - date and time representation
          (i.e. "พ   6 ต.ค. 01:40:00 2519")
        * **%v** - short date representation
          (i.e. " 6-ม.ค.-2562", "27-ก.พ.-2555")

    Other directives will be passed to datetime.strftime()

    :Note:
        * The Thai Buddhist Era (BE) year is simply converted from AD
          by adding 543. This is certainly not accurate for years
          before 1941 AD, due to the change in Thai New Year's Day.
        * This meant to be an interim solution, since
          Python standard's locale module (which relied on C's strftime())
          does not support "th" or "th_TH" locale yet. If supported,
          we can just locale.setlocale(locale.LC_TIME, "th_TH")
          and then use native datetime.strftime().

    We are trying to make this platform-independent and support extensions
    as many as possible. See these links for strftime() extensions
    in POSIX, BSD, and GNU libc:

        * Python
          https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        * C http://www.cplusplus.com/reference/ctime/strftime/
        * GNU https://metacpan.org/pod/POSIX::strftime::GNU
        * Linux https://linux.die.net/man/3/strftime
        * OpenBSD https://man.openbsd.org/strftime.3
        * FreeBSD https://www.unix.com/man-page/FreeBSD/3/strftime/
        * macOS
          https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man3/strftime.3.html
        * PHP https://secure.php.net/manual/en/function.strftime.php
        * JavaScript's implementation https://github.com/samsonjs/strftime
        * strftime() quick reference http://www.strftime.net/

    :param datetime dt_obj: an instantiatetd object of
                            :mod:`datetime.datetime`
    :param str fmt: string containing date and time directives
    :param bool thaidigit: If `thaidigit` is set to **False** (default),
                           number will be represented in Arabic digit.
                           If it is set to **True**, it will be represented
                           in Thai digit.

    :return: Date and time text, with month in Thai name and year in
             Thai Buddhist era. The year is simply converted from AD
             by adding 543 (will not accurate for years before 1941 AD,
             due to change in Thai New Year's Day).
    :rtype: str

    :Example:
    ::

        from datetime import datetime
        from pythainlp.util import thai_strftime

        datetime_obj = datetime(year=2019, month=6, day=9, \\
            hour=5, minute=59, second=0, microsecond=0)

        print(datetime_obj)
        # output: 2019-06-09 05:59:00

        thai_strftime(datetime_obj, "%A %d %B %Y")
        # output: 'วันอาทิตย์ 09 มิถุนายน 2562'

        thai_strftime(datetime_obj, "%a %-d %b %y")  # no padding
        # output: 'อา 9 มิ.ย. 62'

        thai_strftime(datetime_obj, "%a %_d %b %y")  # space padding
        # output: 'อา  9 มิ.ย. 62'

        thai_strftime(datetime_obj, "%a %0d %b %y")  # zero padding
        # output: 'อา 09 มิ.ย. 62'

        thai_strftime(datetime_obj, "%-H นาฬิกา %-M นาที", thaidigit=True)
        # output: '๕ นาฬิกา ๕๙ นาที'

        thai_strftime(datetime_obj, "%D (%v)")
        # output: '06/09/62 ( 9-มิ.ย.-2562)'

        thai_strftime(datetime_obj, "%c")
        # output: 'อา  9 มิ.ย. 05:59:00 2562'

        thai_strftime(datetime_obj, "%H:%M %p")
        # output: '01:40 AM'

        thai_strftime(datetime_obj, "%H:%M %#p")
        # output: '01:40 am'
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
                    str_ = _thai_strftime(dt_obj, fmt_char)
                elif fmt_char in _EXTENSIONS:
                    fmt_char_ext = fmt_char
                    k = j + 1
                    if k < fmt_len:
                        fmt_char = fmt[k]
                        if fmt_char in _NEED_L10N:
                            str_ = _thai_strftime(dt_obj, fmt_char)
                        else:
                            str_ = _std_strftime(dt_obj, fmt_char)

                        if fmt_char_ext == "-":
                            # GNU libc extension,
                            # no padding
                            if str_[0] and str_[0] in " 0":
                                str_ = str_[1:]
                        elif fmt_char_ext == "_":
                            # GNU libc extension,
                            # explicitly specify space (" ") for padding
                            if str_[0] and str_[0] == "0":
                                str_ = " " + str_[1:]
                        elif fmt_char_ext == "0":
                            # GNU libc extension,
                            # explicitly specify zero ("0") for padding
                            if str_[0] and str_[0] == " ":
                                str_ = "0" + str_[1:]
                        elif fmt_char_ext == "^":
                            # GNU libc extension,
                            # convert to upper case
                            str_ = str_.upper()
                        elif fmt_char_ext == "#":
                            # GNU libc extension,
                            # swap case - useful for %Z
                            str_ = str_.swapcase()
                        elif fmt_char_ext == "E":
                            # POSIX extension,
                            # uses the locale's alternative representation
                            # Not implemented yet
                            pass
                        elif fmt_char_ext == "O":
                            # POSIX extension,
                            # uses the locale's alternative numeric symbols
                            str_ = str_.translate(_HA_TH_DIGITS)
                        i = i + 1  # consume char after format char
                    else:
                        # format char at string's end has no meaning
                        str_ = fmt_char_ext
                else:  # not in _NEED_L10N nor _EXTENSIONS
                    # no known localization available, use Python's default
                    str_ = _std_strftime(dt_obj, fmt_char)

                i = i + 1  # consume char after "%"
            else:
                # % char at string's end has no meaning
                str_ = "%"
        else:
            str_ = fmt[i]

        thaidate_parts.append(str_)
        i = i + 1

    thaidate_text = "".join(thaidate_parts)

    if thaidigit:
        thaidate_text = thaidate_text.translate(_HA_TH_DIGITS)

    return thaidate_text
