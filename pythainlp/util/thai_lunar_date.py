# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""This file is a port from
> https://gist.github.com/touchiep/99f4f5bb349d6b983ef78697630ab78e
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Union

_YEAR_DEV: dict[int, float] = {
    0: 0,
    1901: 0.122733000004352,
    1906: 1.91890000045229e-02,
    1911: -8.43549999953059e-02,
    1916: -0.187898999995135,
    1921: -0.291442999994964,
    1926: 7.44250000052413e-02,
    1931: -2.91189999945876e-02,
    1936: -0.132662999994416,
    1941: -0.236206999994245,
    1946: -0.339750999994074,
    1951: -0.443294999993903,
    1956: -7.74269999936981e-02,
    1961: -0.180970999993527,
    1966: -0.284514999993356,
    1971: -0.388058999993185,
    1976: -0.491602999993014,
    1981: -0.595146999992842,
    1986: -0.698690999992671,
    1991: -0.332822999992466,
    1996: -0.436366999992295,
    2001: -0.539910999992124,
    2006: -0.643454999991953,
    2011: 0.253001000008218,
    2016: 0.149457000008389,
    2021: -0.484674999991406,
    2026: -0.588218999991235,
    2031: 0.308237000008937,
    2036: 0.204693000009108,
    2041: 0.101149000009279,
    2046: -2.39499999055015e-03,
    2051: -0.105938999990379,
    2056: 0.259929000009826,
    2061: 0.156385000009997,
    2066: 5.28410000101682e-02,
    2071: -5.07029999896607e-02,
    2076: -0.15424699998949,
    2081: -0.257790999989318,
    2086: 0.108077000010887,
    2091: 4.53300001105772e-03,
    2096: -9.90109999887712e-02,
    2101: -0.2025549999886,
    2106: -0.306098999988429,
    2111: -0.409642999988258,
    2116: -4.37749999880528e-02,
    2121: -0.147318999987882,
    2126: -0.250862999987711,
    2131: -0.354406999987539,
    2136: -0.457950999987368,
    2141: -0.561494999987197,
    2146: -0.665038999987026,
    2151: -0.299170999986821,
    2156: -0.40271499998665,
    2161: -0.506258999986479,
    2166: -0.609802999986308,
    2171: -0.713346999986137,
    2176: 0.183109000014035,
    2181: -0.45102299998576,
    2186: -0.554566999985589,
    2191: 0.341889000014582,
    2196: 0.238345000014753,
    2201: 0.134801000014924,
    2206: 3.12570000150951e-02,
    2211: -7.22869999847338e-02,
    2216: 0.293581000015471,
    2221: 0.190037000015642,
    2226: 8.64930000158135e-02,
    2231: -1.70509999840154e-02,
    2236: -0.120594999983844,
    2241: -0.224138999983673,
    2246: 0.141729000016532,
    2251: 0.038185000016703,
    2256: -6.53589999831259e-02,
    2261: -0.168902999982955,
    2266: -0.272446999982784,
    2271: -0.375990999982613,
    2276: -1.01229999824075e-02,
    2281: -0.113666999982236,
    2286: -0.217210999982065,
    2291: -0.320754999981894,
    2296: -0.424298999981723,
    2301: -0.527842999981552,
    2306: -0.631386999981381,
    2311: -0.265518999981176,
    2316: -0.369062999981005,
    2321: -0.472606999980834,
    2326: -0.576150999980662,
    2331: -0.679694999980491,
    2336: 0.21676100001968,
    2341: -0.417370999980115,
    2346: -0.520914999979944,
    2351: -0.624458999979773,
    2356: 0.271997000020398,
    2361: 0.168453000020569,
    2366: 6.49090000207404e-02,
    2371: -3.86349999790885e-02,
    2376: 0.327233000021117,
    2381: 0.223689000021288,
    2386: 0.120145000021459,
    2391: 1.66010000216299e-02,
    2396: -0.086942999978199,
    2401: -0.190486999978028,
    2406: 0.175381000022177,
    2411: 7.18370000223483e-02,
    2416: -3.17069999774806e-02,
    2421: -0.135250999977309,
    2426: -0.238794999977138,
    2431: -0.342338999976967,
    2436: 2.35290000232378e-02,
    2441: -8.00149999765911e-02,
    2446: -0.18355899997642,
    2451: -0.287102999976249,
    2456: -0.390646999976078,
}

_BEGIN_DATES: list[date] = [
    date(1902, 11, 30),
    date(1912, 12, 8),
    date(1922, 11, 19),
    date(1932, 11, 27),
    date(1942, 12, 7),
    date(1952, 11, 16),
    date(1962, 11, 26),
    date(1972, 12, 5),
    date(1982, 11, 15),
    date(1992, 11, 24),
    date(2002, 12, 4),
    date(2012, 11, 13),
    date(2022, 11, 23),
    date(2032, 12, 2),
    date(2042, 12, 12),
    date(2052, 11, 21),
    date(2062, 12, 1),
    date(2072, 12, 9),
    date(2082, 11, 20),
    date(2092, 11, 28),
    date(2102, 12, 9),
    date(2112, 11, 18),
    date(2122, 11, 28),
    date(2132, 12, 7),
    date(2142, 11, 17),
    date(2152, 11, 26),
    date(2162, 12, 6),
    date(2172, 11, 15),
    date(2182, 11, 25),
    date(2192, 12, 4),
    date(2202, 12, 15),
    date(2212, 11, 24),
    date(2222, 12, 4),
    date(2232, 12, 12),
    date(2242, 11, 23),
    date(2252, 12, 1),
    date(2262, 12, 11),
    date(2272, 11, 20),
    date(2282, 11, 30),
    date(2292, 12, 9),
    date(2302, 11, 20),
    date(2312, 11, 29),
    date(2322, 12, 9),
    date(2332, 11, 18),
    date(2342, 11, 28),
    date(2352, 12, 7),
    date(2362, 12, 17),
    date(2372, 11, 26),
    date(2382, 12, 6),
    date(2392, 12, 14),
    date(2402, 11, 25),
    date(2412, 12, 3),
    date(2422, 12, 13),
    date(2432, 11, 23),
    date(2442, 12, 2),
    date(2452, 12, 11),
]

_DAYS_354: list[int] = [29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30]
_DAYS_355: list[int] = [29, 30, 29, 30, 29, 30, 30, 30, 29, 30, 29, 30, 29, 30]
_DAYS_384: list[int] = [
    29,
    30,
    29,
    30,
    29,
    30,
    29,
    30,
    30,
    29,
    30,
    29,
    30,
    29,
    30,
]

# Zodiac names in Thai, English, and Numeric representations
_ZODIAC: dict[int, list[Union[str, int]]] = {
    1: [
        "ชวด",
        "ฉลู",
        "ขาล",
        "เถาะ",
        "มะโรง",
        "มะเส็ง",
        "มะเมีย",
        "มะแม",
        "วอก",
        "ระกา",
        "จอ",
        "กุน",
    ],
    2: [
        "RAT",
        "OX",
        "TIGER",
        "RABBIT",
        "DRAGON",
        "SNAKE",
        "HORSE",
        "GOAT",
        "MONKEY",
        "ROOSTER",
        "DOG",
        "PIG",
    ],
    3: list(range(1, 13)),
}


def _calculate_f_year_f_dev(year: int) -> tuple[int, float]:
    if year in _YEAR_DEV:
        return year, _YEAR_DEV[year]

    nearest_lower_year = max(y for y in _YEAR_DEV if y < year)
    return nearest_lower_year, _YEAR_DEV[nearest_lower_year]


def athikamas(year: int) -> bool:
    athi = ((year - 78) - 0.45222) % 2.7118886
    return athi < 1


def athikavar(year: int) -> bool:
    if athikamas(year):
        return False

    if athikamas(year + 1):
        cutoff = 1.69501433191599e-02
    else:
        cutoff = -1.42223099315486e-02
    return deviation(year) > cutoff


def deviation(year: int) -> float:
    curr_dev = 0.0
    last_dev = 0.0
    f_year, f_dev = _calculate_f_year_f_dev(year)
    if year == f_year:
        curr_dev = f_dev
    else:
        f_year = f_year + 1
        for i in range(f_year, year + 1):
            if i == f_year:
                last_dev = f_dev
            else:
                last_dev = curr_dev
            if athikamas(i - 1):
                curr_dev = -0.102356
            elif athikavar(i - 1):
                curr_dev = -0.632944
            else:
                curr_dev = 0.367056
            curr_dev = last_dev + curr_dev

    return curr_dev


def last_day_in_year(year: int) -> int:
    if athikamas(year):
        return 384
    elif athikavar(year):
        return 355

    return 354


def athikasurathin(year: int) -> bool:
    """Check if a year is a leap year in the Thai lunar calendar"""
    # Check divisibility by 400 (divisible by 400 is always a leap year)
    if year % 400 == 0:
        return True

    # Check divisibility by 100 (divisible by 100 but not 400 is not a leap
    # year)
    elif year % 100 == 0:
        return False

    # Check divisibility by 4 (divisible by 4 but not by 100 is a leap year)
    elif year % 4 == 0:
        return True

    # All other cases are not leap years
    return False


def number_day_in_year(year: int) -> int:
    if athikasurathin(year):
        return 366

    return 365


def th_zodiac(year: int, output_type: int = 1) -> Union[str, int]:
    """Thai Zodiac Year Name
    Converts a Gregorian year to its corresponding Zodiac name.

    :param int year: The Gregorian year. AD (Anno Domini)
    :param int output_type: Output type (1 = Thai, 2 = English, 3 = Number).

    :return: The Zodiac name or number corresponding to the input year.
    :rtype: Union[str, int]

    :Example:

        >>> from pythainlp.util import th_zodiac
        >>> # Get Thai zodiac name
        >>> th_zodiac(2024, output_type=1)
        'มะโรง'
        >>> # Get English zodiac name
        >>> th_zodiac(2024, output_type=2)
        'DRAGON'
        >>> # Get zodiac number
        >>> th_zodiac(2024, output_type=3)
        5
    """
    # Calculate zodiac index
    result = year % 12
    if result - 3 < 1:
        result = result - 3 + 12
    else:
        result = result - 3

    # Return the zodiac based on the output type
    return _ZODIAC[output_type][result - 1]


def to_lunar_date(input_date: date) -> str:
    """Convert the solar date to Thai Lunar Date

    :param date input_date: date of the day.
    :return: Thai text lunar date
    :rtype: str

    :Example:

        >>> from datetime import date
        >>> from pythainlp.util import to_lunar_date
        >>> to_lunar_date(date(2024, 1, 1))
        'แรม 5 ค่ำ เดือน 1'
        >>> to_lunar_date(date(2024, 12, 31))
        'ขึ้น 2 ค่ำ เดือน 2'
    """
    # Check if date is within supported range
    if input_date.year < 1903 or input_date.year > 2460:
        raise NotImplementedError("Unsupported date")  # Unsupported date

    # Choose the nearest begin date
    c_year = input_date.year - 1
    begin_date = _BEGIN_DATES[0]
    for _date in reversed(_BEGIN_DATES):
        if c_year > _date.year:
            begin_date = _date
            break

    current_date = begin_date
    for year in range(begin_date.year + 1, input_date.year):
        day_in_year = last_day_in_year(year)
        current_date += timedelta(days=day_in_year)

    r_day_prev = (date(current_date.year, 12, 31) - current_date).days
    day_of_year = (input_date - date(input_date.year, 1, 1)).days
    day_from_one = r_day_prev + day_of_year + 1
    last_day = last_day_in_year(input_date.year)

    if last_day == 354:
        days_in_month = _DAYS_354
    elif last_day == 355:
        days_in_month = _DAYS_355
    elif last_day == 384:
        days_in_month = _DAYS_384
    else:
        raise ValueError(
            f"Unexpected last_day value: {last_day!r}. "
            "Expected 354, 355, or 384."
        )

    days_of_year = day_from_one
    th_m = 0
    for j, days in enumerate(days_in_month, start=1):
        th_m = j
        if 0 < days_of_year <= days:
            break
        else:
            days_of_year -= days

    if last_day <= 355:  # 354 or 355
        if th_m > 12:
            th_m = th_m - 12
    elif last_day == 384:
        if th_m > 13:
            th_m = th_m - 13
        if th_m >= 9 and th_m <= 13:
            th_m = th_m - 1

    if days_of_year > 15:
        th_s = "แรม"
        days_of_year = days_of_year - 15
    else:
        th_s = "ขึ้น"

    thai_lunar_date = f"{th_s} {days_of_year} ค่ำ เดือน {th_m}"

    return thai_lunar_date
