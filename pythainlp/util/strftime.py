# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai date/time formatting."""

from __future__ import annotations

import warnings
from collections.abc import Callable  # noqa: TC003  # for get_type_hints()
from datetime import datetime  # noqa: TC003  # for get_type_hints()
from string import digits

from pythainlp import thai_digits
from pythainlp.util._calendar import _BE_AD_OFFSET
from pythainlp.util.date import (
    thai_abbr_months,
    thai_abbr_weekdays,
    thai_full_months,
    thai_full_weekdays,
)

__all__: list[str] = [
    "thai_strftime",
]

_HA_TH_DIGITS: dict[int, int] = str.maketrans(digits, thai_digits)

_EXTENSIONS: str = "EO-_0^#"  # extension flags


def _std_strftime(dt_obj: datetime, fmt_char: str) -> str:
    """Standard datetime.strftime() with normalization and exception handling."""
    str_ = ""
    try:
        str_ = dt_obj.strftime(f"%{fmt_char}")
        if not str_ or str_ == f"%{fmt_char}":
            # Normalize outputs for unsupported directives
            # in different platforms:
            # "%Q" may result "", "%Q", or "Q", make it all "Q"
            str_ = fmt_char
    except ValueError as err:
        # Unsupported directives may raise ValueError on Windows,
        # in that case just use the fmt_char
        warnings.warn(
            (
                f"String format directive unknown/not support: %{fmt_char}\n"
                f"The system raises this ValueError: {err}\n"
                f"Continue working without the directive."
            ),
            category=UserWarning,
            stacklevel=2,
        )
        str_ = fmt_char
    return str_


def _be_year(dt_obj: datetime) -> str:
    """Buddhist Era year, at least 4 digits."""
    return str(dt_obj.year + _BE_AD_OFFSET).zfill(4)


def _iso_be_year(dt_obj: datetime) -> str:
    """Buddhist Era year of the ISO week-based year (``%G``)."""
    return str(int(dt_obj.strftime("%G")) + _BE_AD_OFFSET)


def _fmt_century(dt_obj: datetime) -> str:
    # Thai Buddhist century (AD+543)/100 + 1 as decimal number
    return str(int((dt_obj.year + _BE_AD_OFFSET) / 100) + 1).zfill(2)


def _fmt_datetime(dt_obj: datetime) -> str:
    # Locale's appropriate date and time representation
    # Wed  6 Oct 01:40:00 1976
    # พ   6 ต.ค. 01:40:00 2519  <-- left-aligned weekday, right-aligned day
    return "{:<2} {:>2} {} {} {}".format(
        thai_abbr_weekdays[dt_obj.weekday()],
        dt_obj.day,
        thai_abbr_months[dt_obj.month - 1],
        dt_obj.strftime("%H:%M:%S"),
        _be_year(dt_obj),
    )


def _fmt_year_short(dt_obj: datetime) -> str:
    # Year without century
    return (str(dt_obj.year + _BE_AD_OFFSET)[-2:]).zfill(2)


def _fmt_us_date(dt_obj: datetime) -> str:
    # Equivalent to ``%m/%d/%y''
    return f"{dt_obj.strftime('%m/%d')}/{_fmt_year_short(dt_obj)}"


def _fmt_iso_date(dt_obj: datetime) -> str:
    # Equivalent to ``%Y-%m-%d''
    return "{}-{}".format(_be_year(dt_obj), dt_obj.strftime("%m-%d"))


def _fmt_iso_year(dt_obj: datetime) -> str:
    # ISO 8601 year with century representing the year that contains
    # the greater part of the ISO week (%V). Monday as the first day
    # of the week.
    return _iso_be_year(dt_obj).zfill(4)


def _fmt_iso_year_short(dt_obj: datetime) -> str:
    # Same year as in ``%G'', but as a decimal number without century (00-99)
    return _iso_be_year(dt_obj)[-2:].zfill(2)


def _fmt_bsd_date(dt_obj: datetime) -> str:
    # BSD extension, ' 6-Oct-1976'
    day = f"{dt_obj.day:>2}"
    return f"{day}-{thai_abbr_months[dt_obj.month - 1]}-{_be_year(dt_obj)}"


def _fmt_local_date(dt_obj: datetime) -> str:
    # Locale's appropriate date representation
    return (
        f"{str(dt_obj.day).zfill(2)}/{str(dt_obj.month).zfill(2)}"
        f"/{_be_year(dt_obj)}"
    )


def _fmt_date_command(dt_obj: datetime) -> str:
    # National representation of the date and time
    # (the format is similar to that produced by date(1))
    # Wed  6 Oct 1976 01:40:00
    return "{:<2} {:>2} {} {} {}".format(
        thai_abbr_weekdays[dt_obj.weekday()],
        dt_obj.day,
        thai_abbr_months[dt_obj.month - 1],
        dt_obj.year + _BE_AD_OFFSET,
        dt_obj.strftime("%H:%M:%S"),
    )


# Directives in _NEED_L10N and their conversion functions.
_L10N_HANDLERS: dict[str, Callable[[datetime], str]] = {
    # National representation of the full weekday name
    "A": lambda dt_obj: thai_full_weekdays[dt_obj.weekday()],
    # National representation of the abbreviated weekday
    "a": lambda dt_obj: thai_abbr_weekdays[dt_obj.weekday()],
    # National representation of the full month name
    "B": lambda dt_obj: thai_full_months[dt_obj.month - 1],
    # National representation of the abbreviated month name
    "b": lambda dt_obj: thai_abbr_months[dt_obj.month - 1],
    "C": _fmt_century,
    "c": _fmt_datetime,
    "D": _fmt_us_date,
    "F": _fmt_iso_date,
    "G": _fmt_iso_year,
    "g": _fmt_iso_year_short,
    "v": _fmt_bsd_date,
    # Locale's appropriate time representation
    "X": lambda dt_obj: dt_obj.strftime("%H:%M:%S"),
    "x": _fmt_local_date,
    # Year with century
    "Y": _be_year,
    "y": _fmt_year_short,
    "+": _fmt_date_command,
}

_NEED_L10N: str = "".join(_L10N_HANDLERS)  # flags that need localization


def _thai_strftime(dt_obj: datetime, fmt_char: str) -> str:
    """Conversion support for thai_strftime().

    The fmt_char should be in _NEED_L10N when calling this function.
    """
    handler = _L10N_HANDLERS.get(fmt_char)
    if handler is None:
        # No known localization available, use Python's default
        return _std_strftime(dt_obj, fmt_char)
    return handler(dt_obj)


def _l10n_or_std_strftime(dt_obj: datetime, fmt_char: str) -> str:
    if fmt_char in _NEED_L10N:
        return _thai_strftime(dt_obj, fmt_char)
    return _std_strftime(dt_obj, fmt_char)


def _strip_padding(text: str) -> str:
    # GNU libc extension, "-": no padding
    return text[1:] if text[0] in " 0" else text


def _space_padding(text: str) -> str:
    # GNU libc extension, "_": explicitly specify space (" ") for padding
    return " " + text[1:] if text[0] == "0" else text


def _zero_padding(text: str) -> str:
    # GNU libc extension, "0": explicitly specify zero ("0") for padding
    return "0" + text[1:] if text[0] == " " else text


def _keep_text(text: str) -> str:
    return text


# Extension flags and their conversion functions.
_EXTENSION_HANDLERS: dict[str, Callable[[str], str]] = {
    "-": _strip_padding,
    "_": _space_padding,
    "0": _zero_padding,
    # GNU libc extension, convert to upper case
    "^": str.upper,
    # GNU libc extension, swap case - useful for %Z
    "#": str.swapcase,
    # POSIX extension, use the locale's alternative representation.
    # Not implemented yet.
    "E": _keep_text,
    # POSIX extension, use the locale's alternative numeric symbols
    "O": lambda text: text.translate(_HA_TH_DIGITS),
}


def _convert_directive(
    dt_obj: datetime, fmt: str, start: int
) -> tuple[str, int]:
    """Convert the directive that starts with "%" at ``fmt[start]``.

    :return: converted text and the index of the next unread character
    """
    fmt_len = len(fmt)
    pos = start + 1
    if pos >= fmt_len:
        # % char at string's end has no meaning
        return "%", pos

    fmt_char = fmt[pos]
    if fmt_char not in _EXTENSIONS:
        return _l10n_or_std_strftime(dt_obj, fmt_char), pos + 1

    pos += 1
    if pos >= fmt_len:
        # format char at string's end has no meaning
        return fmt_char, pos

    text = _l10n_or_std_strftime(dt_obj, fmt[pos])
    return _EXTENSION_HANDLERS.get(fmt_char, _keep_text)(text), pos + 1


def thai_strftime(
    dt_obj: datetime,
    fmt: str = "%-d %b %y",
    thaidigit: bool = False,
) -> str:
    """Convert :class:`datetime.datetime` into Thai date and time format.

    The formatting directives are similar to :func:`datetime.strftime`.

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
        * C https://en.cppreference.com/w/cpp/chrono/c/strftime
        * GNU https://metacpan.org/pod/POSIX::strftime::GNU
        * Linux https://linux.die.net/man/3/strftime
        * OpenBSD https://man.openbsd.org/strftime.3
        * FreeBSD https://www.unix.com/man-page/FreeBSD/3/strftime/
        * macOS
          https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man3/strftime.3.html
        * PHP https://secure.php.net/manual/en/function.strftime.php
        * JavaScript's implementation https://github.com/samsonjs/strftime
        * strftime() quick reference https://strftime.net/

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

        >>> from datetime import datetime
        >>> from pythainlp.util import thai_strftime

        >>> datetime_obj = datetime(year=2019, month=6, day=9, \\
        ...     hour=5, minute=59, second=0, microsecond=0)

        >>> print(datetime_obj)
        2019-06-09 05:59:00

        >>> thai_strftime(datetime_obj, "%A %d %B %Y")
        'วันอาทิตย์ 09 มิถุนายน 2562'

        >>> thai_strftime(datetime_obj, "%a %-d %b %y")  # no padding
        'อา 9 มิ.ย. 62'

        >>> thai_strftime(datetime_obj, "%a %_d %b %y")  # space padding
        'อา  9 มิ.ย. 62'

        >>> thai_strftime(datetime_obj, "%a %0d %b %y")  # zero padding
        'อา 09 มิ.ย. 62'

        >>> thai_strftime(datetime_obj, "%-H นาฬิกา %-M นาที", thaidigit=True)
        '๕ นาฬิกา ๕๙ นาที'

        >>> thai_strftime(datetime_obj, "%D (%v)")
        '06/09/62 ( 9-มิ.ย.-2562)'

        >>> thai_strftime(datetime_obj, "%c")
        'อา  9 มิ.ย. 05:59:00 2562'

        >>> thai_strftime(datetime_obj, "%H:%M %p")
        '05:59 AM'

        >>> thai_strftime(datetime_obj, "%H:%M %#p")
        '05:59 am'
    """
    thaidate_parts: list[str] = []

    i = 0
    fmt_len = len(fmt)
    while i < fmt_len:
        if fmt[i] == "%":
            str_, i = _convert_directive(dt_obj, fmt, i)
        else:
            str_ = fmt[i]
            i += 1
        thaidate_parts.append(str_)

    thaidate_text = "".join(thaidate_parts)

    if thaidigit:
        thaidate_text = thaidate_text.translate(_HA_TH_DIGITS)

    return thaidate_text
