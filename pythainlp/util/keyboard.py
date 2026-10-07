# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Functions related to keyboard layout."""

from __future__ import annotations

from typing import Optional, Union, cast

EN_TH_KEYB_PAIRS: dict[str, str] = {
    "Z": "(",
    "z": "ผ",
    "X": ")",
    "x": "ป",
    "C": "ฉ",
    "c": "แ",
    "V": "ฮ",
    "v": "อ",
    "B": "\u0e3a",  # พินทุ
    "b": "\u0e34",  # สระอุ
    "N": "\u0e4c",  # การันต์
    "n": "\u0e37",  # สระอือ
    "M": "?",
    "m": "ท",
    "<": "ฒ",
    ",": "ม",
    ">": "ฬ",
    ".": "ใ",
    "?": "ฦ",
    "/": "ฝ",
    "A": "ฤ",
    "a": "ฟ",
    "S": "ฆ",
    "s": "ห",
    "D": "ฏ",
    "d": "ก",
    "F": "โ",
    "f": "ด",
    "G": "ฌ",
    "g": "เ",
    "H": "\u0e47",  # ไม้ไต่คู้
    "h": "\u0e49",  # ไม้โท
    "J": "\u0e4b",  # ไม้จัตวา
    "j": "\u0e48",  # ไม้เอก
    "K": "ษ",
    "k": "า",
    "L": "ศ",
    "l": "ส",
    ":": "ซ",
    ";": "ว",
    '"': ".",
    "'": "ง",
    "Q": "๐",
    "q": "ๆ",
    "W": '"',
    "w": "ไ",
    "E": "ฎ",
    "e": "\u0e33",  # สระอำ
    "R": "ฑ",
    "r": "พ",
    "T": "ธ",
    "t": "ะ",
    "Y": "\u0e4d",  # นิคหิต
    "y": "\u0e31",  # ไม้หันอากาศ
    "U": "\u0e4a",  # ไม้ตรี
    "u": "\u0e35",  # สระอ ี
    "I": "ณ",
    "i": "ร",
    "O": "ฯ",
    "o": "น",
    "P": "ญ",
    "p": "ย",
    "{": "ฐ",
    "[": "บ",
    "}": ",",
    "]": "ล",
    "|": "ฅ",
    "\\": "ฃ",
    "~": "%",
    "`": "_",
    "@": "๑",
    "2": "/",
    "#": "๒",
    "3": "-",
    "$": "๓",
    "4": "ภ",
    "%": "๔",
    "5": "ถ",
    "^": "\u0e39",  # สระอู
    "6": "\u0e38",  # สระอุ
    "&": "฿",
    "7": "\u0e36",  # สระอึ
    "*": "๕",
    "8": "ค",
    "(": "๖",
    "9": "ต",
    ")": "๗",
    "0": "จ",
    "_": "๘",
    "-": "ข",
    "+": "๙",
    "=": "ช",
}

TH_EN_KEYB_PAIRS: dict[str, str] = {v: k for k, v in EN_TH_KEYB_PAIRS.items()}

EN_TH_TRANSLATE_TABLE: dict[int, Union[int, str, None]] = str.maketrans(
    cast("dict[str, Union[int, str, None]]", EN_TH_KEYB_PAIRS)
)
TH_EN_TRANSLATE_TABLE: dict[int, Union[int, str, None]] = str.maketrans(
    cast("dict[str, Union[int, str, None]]", TH_EN_KEYB_PAIRS)
)

TIS_820_2531_MOD: list[list[str]] = [
    ["-", "ๅ", "/", "", "_", "ภ", "ถ", "ุ", "ึ", "ค", "ต", "จ", "ข", "ช"],
    ["ๆ", "ไ", "ำ", "พ", "ะ", "ั", "ี", "ร", "น", "ย", "บ", "ล", "ฃ"],
    ["ฟ", "ห", "ก", "ด", "เ", "้", "่", "า", "ส", "ว", "ง"],
    ["ผ", "ป", "แ", "อ", "ิ", "ื", "ท", "ม", "ใ", "ฝ"],
]
TIS_820_2531_MOD_SHIFT: list[list[str]] = [
    ["%", "+", "๑", "๒", "๓", "๔", "ู", "฿", "๕", "๖", "๗", "๘", "๙"],
    ["๐", '"', "ฎ", "ฑ", "ธ", "ํ", "๊", "ณ", "ฯ", "ญ", "ฐ", ",", "ฅ"],
    ["ฤ", "ฆ", "ฏ", "โ", "ฌ", "็", "๋", "ษ", "ศ", "ซ", "."],
    ["(", ")", "ฉ", "ฮ", "ฺ", "์", "?", "ฒ", "ฬ", "ฦ"],
]


def eng_to_thai(text: str) -> str:
    """
    Convert text typed in the wrong layout to Thai Kedmanee.

    The text was typed with the English-US Qwerty keyboard layout.

    :param str text: text typed with the wrong layout
        (Thai typed using an English keyboard)
    :return: Thai text, corrected from the wrong keyboard layout
    :rtype: str

    :Example:

    Intentionally type "ธนาคารแห่งประเทศไทย", but got "Tok8kicsj'xitgmLwmp":

        >>> from pythainlp.util import eng_to_thai
        >>> eng_to_thai("Tok8kicsj'xitgmLwmp")
        'ธนาคารแห่งประเทศไทย'
    """
    return text.translate(EN_TH_TRANSLATE_TABLE)


def thai_to_eng(text: str) -> str:
    """
    Convert text typed in the wrong layout to English-US Qwerty.

    The text was typed with the Thai Kedmanee keyboard layout.

    :param str text: text typed with the wrong layout
        (English typed using a Thai keyboard)
    :return: English text, corrected from the wrong keyboard layout
    :rtype: str

    :Example:

    Intentionally type "Bank of Thailand", but got "ฺฟืา นด ธ้ฟรสฟืก":

        >>> from pythainlp.util import thai_to_eng
        >>> thai_to_eng("ฺฟืา นด ธ้ฟรสฟืก")
        'Bank of Thailand'
    """
    return text.translate(TH_EN_TRANSLATE_TABLE)


def thai_keyboard_dist(c1: str, c2: str, shift_dist: float = 0.0) -> float:
    """
    Calculate the Euclidean distance between two Thai characters.

    The distance follows the location of the characters on a Thai
    keyboard layout. The calculation uses a modified TIS 820-2531
    standard layout, which is developed from the Kedmanee layout and is
    the most commonly used Thai keyboard layout.

    The modified TIS 820-2531 is TIS 820-2531 with a few key extensions
    proposed in the TIS 820-2536 draft. See Figure 4, notice the grey
    keys, in
    https://www.nectec.or.th/it-standards/keyboard_layout/thai-key.html

    Note that the latest TIS 820-2538 has slight changes in layout from
    TIS 820-2531. See Figure 2, notice the Thai Baht sign and the ฅ-ฃ
    pair, in
    https://www.nectec.or.th/it-standards/std820/std820.html
    Since keyboard manufacturers have not widely adopted TIS 820-2538,
    this function uses the de facto standard modified TIS 820-2531.

    :param str c1: first character
    :param str c2: second character
    :param float shift_dist: distance to return if the characters are
        on shifted keys
    :return: Euclidean distance between the two characters
    :rtype: float

    :Example:

        >>> from pythainlp.util import thai_keyboard_dist
        >>> thai_keyboard_dist("ด", "ะ")
        1.4142135623730951
        >>> thai_keyboard_dist("ฟ", "ฤ")
        0.0
        >>> thai_keyboard_dist("ฟ", "ห")
        1.0
        >>> thai_keyboard_dist("ฟ", "ก")
        2.0
        >>> thai_keyboard_dist("ฟ", "ฤ", 0.5)
        0.5
    """

    def get_char_coord(
        ch: str, layouts: Optional[list[list[list[str]]]] = None
    ) -> tuple[int, int]:
        if layouts is None:
            layouts = [TIS_820_2531_MOD, TIS_820_2531_MOD_SHIFT]
        for layout in layouts:
            for row in layout:
                if ch in row:
                    r = layout.index(row)
                    c = row.index(ch)
                    return (r, c)
        raise ValueError(ch + " not found in given keyboard layout")

    coord1 = get_char_coord(c1)
    coord2 = get_char_coord(c2)
    distance: float = (
        (coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2
    ) ** (0.5)
    if distance == 0 and c1 != c2:
        return shift_dist
    return distance
