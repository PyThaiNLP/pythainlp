# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Functions related to keyboard layout.
"""

EN_TH_KEYB_PAIRS = {
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

TH_EN_KEYB_PAIRS = {v: k for k, v in EN_TH_KEYB_PAIRS.items()}

EN_TH_TRANSLATE_TABLE = str.maketrans(EN_TH_KEYB_PAIRS)
TH_EN_TRANSLATE_TABLE = str.maketrans(TH_EN_KEYB_PAIRS)

TIS_820_2531_MOD = [
    ["-", "ๅ", "/", "", "_", "ภ", "ถ", "ุ", "ึ", "ค", "ต", "จ", "ข", "ช"],
    ["ๆ", "ไ", "ำ", "พ", "ะ", "ั", "ี", "ร", "น", "ย", "บ", "ล", "ฃ"],
    ["ฟ", "ห", "ก", "ด", "เ", "้", "่", "า", "ส", "ว", "ง"],
    ["ผ", "ป", "แ", "อ", "ิ", "ื", "ท", "ม", "ใ", "ฝ"],
]
TIS_820_2531_MOD_SHIFT = [
    ["%", "+", "๑", "๒", "๓", "๔", "ู", "฿", "๕", "๖", "๗", "๘", "๙"],
    ["๐", '"', "ฎ", "ฑ", "ธ", "ํ", "๊", "ณ", "ฯ", "ญ", "ฐ", ",", "ฅ"],
    ["ฤ", "ฆ", "ฏ", "โ", "ฌ", "็", "๋", "ษ", "ศ", "ซ", "."],
    ["(", ")", "ฉ", "ฮ", "ฺ", "์", "?", "ฒ", "ฬ", "ฦ"],
]


def eng_to_thai(text: str) -> str:
    """
    Corrects the given text that was incorrectly typed using English-US
    Qwerty keyboard layout to the originally intended keyboard layout
    that is the Thai Kedmanee keyboard.

    :param str text: incorrect text input (Thai typed using English keyboard)
    :return: Thai text with typing using
             incorrect keyboard layout is corrected
    :rtype: str

    :Example:

    Intentionally type "ธนาคารแห่งประเทศไทย", but got "Tok8kicsj'xitgmLwmp"::

        from pythainlp.util import eng_to_thai

        eng_to_thai("Tok8kicsj'xitgmLwmp")
        # output: ธนาคารแห่งประเทศไทย
    """
    return text.translate(EN_TH_TRANSLATE_TABLE)


def thai_to_eng(text: str) -> str:
    """
    Corrects the given text that was incorrectly typed using Thai Kedmanee
    keyboard layout to the originally intended keyboard layout
    that is the English-US Qwerty keyboard.

    :param str text: incorrect text input (English typed using Thai keyboard)
    :return: English text with typing with
             incorrect keyboard layout is corrected
    :rtype: str

    :Example:

    Intentionally type "Bank of Thailand", but got "ฺฟืา นด ธ้ฟรสฟืก"::

        from pythainlp.util import eng_to_thai

        thai_to_eng("ฺฟืา นด ธ้ฟรสฟืก")
        # output: 'Bank of Thailand'
    """
    return text.translate(TH_EN_TRANSLATE_TABLE)


def thai_keyboard_dist(c1: str, c2: str, shift_dist: float = 0.0) -> float:
    """
    Calculate Euclidean distance between two Thai characters
    according to their location on a Thai keyboard layout.

    A modified TIS 820-2531 standard keyboard layout, which is developed
    from Kedmanee layout and is the most commonly used Thai keyboard layout,
    is used in distance calculation.

    The modified TIS 820-2531 is TIS 820-2531 with few key extensions
    proposed in TIS 820-2536 draft. See Figure 4, notice grey keys, in
    https://www.nectec.or.th/it-standards/keyboard_layout/thai-key.html

    Noted that the latest TIS 820-2538 has slight changes in layout from
    TIS 820-2531. See Figure 2, notice the Thai Baht sign and ฅ-ฃ pair, in
    https://www.nectec.or.th/it-standards/std820/std820.html
    Since TIS 820-2538 is not widely adopted by keyboard manufacturer,
    this function uses the de facto standard modified TIS 820-2531 instead.

    :param str c1: first character
    :param str c2: second character
    :param str shift_dist: return value if they're shifted
    :return: Euclidean distance between two characters
    :rtype: float

    :Example:

        from pythainlp.util import thai_keyboard_dist
        thai_keyboard_dist("ด", "ะ")
        # output: 1.4142135623730951
        thai_keyboard_dist("ฟ", "ฤ")
        # output: 0.0
        thai_keyboard_dist("ฟ", "ห")
        # output: 1.0
        thai_keyboard_dist("ฟ", "ก")
        # output: 2.0
        thai_keyboard_dist("ฟ", "ฤ", 0.5)
        # output: 0.5
    """

    def get_char_coord(
        ch: str, layouts=[TIS_820_2531_MOD, TIS_820_2531_MOD_SHIFT]
    ):
        for layout in layouts:
            for row in layout:
                if ch in row:
                    r = layout.index(row)
                    c = row.index(ch)
                    return (r, c)
        raise ValueError(ch + " not found in given keyboard layout")

    coord1 = get_char_coord(c1)
    coord2 = get_char_coord(c2)
    distance = (
        (coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2
    ) ** (0.5)
    if distance == 0 and c1 != c2:
        return shift_dist
    return distance
