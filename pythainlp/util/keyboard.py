# -*- coding: utf-8 -*-
"""
Correct text in one language that is incorrectly-typed
with a keyboard layout in another language.
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
    "B": "ฺ",
    "b": "ิ",
    "N": "์",
    "n": "ื",
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
    "H": "็",
    "h": "้",
    "J": "๋",
    "j": "j",
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
    "e": "ำ",
    "R": "ฑ",
    "r": "พ",
    "T": "ธ",
    "t": "ะ",
    "Y": "ํ",
    "y": "ั",
    "U": "๊",
    "u": "ี",
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
    "^": "ู",
    "6": "ุ",
    "&": "฿",
    "7": "ึ",
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


def eng_to_thai(text: str) -> str:
    """
    Correct text in one language that is incorrectly-typed with a keyboard layout in another language. (type Thai with English keyboard)

    :param str text: Incorrect input (type Thai with English keyboard)
    :return: Thai text
    """
    return "".join(
        [EN_TH_KEYB_PAIRS[ch] if (ch in EN_TH_KEYB_PAIRS) else ch for ch in text]
    )


def thai_to_eng(text: str) -> str:
    """
    Correct text in one language that is incorrectly-typed with a keyboard layout in another language. (type Thai with English keyboard)

    :param str text: Incorrect input (type English with Thai keyboard)
    :return: English text
    """
    return "".join(
        [TH_EN_KEYB_PAIRS[ch] if (ch in TH_EN_KEYB_PAIRS) else ch for ch in text]
    )
