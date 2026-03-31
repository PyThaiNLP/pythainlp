# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai braille conversion core functionality."""

from __future__ import annotations

import re
from typing import Union, cast

from pythainlp.tokenize import word_tokenize
from pythainlp.util import Trie

# Thai character to braille pattern mapping
# Braille patterns are represented as dot numbers (1-8)
# Following international braille standards
thai_braille_mapping_dict: dict[str, list[str]] = {
    "ก": ["1245"],
    "ข": ["13"],
    "ฃ": ["356", "13"],
    "ค": ["136"],
    "ฅ": ["36", "136"],
    "ฆ": ["6", "136"],
    "ง": ["12456"],
    "จ": ["245"],
    "ฉ": ["34"],
    "ช": ["346"],
    "ซ": ["2346"],
    "ฌ": ["6", "346"],
    "ญ": ["6", "13456"],
    "ฎ": ["6", "145"],
    "ฏ": ["6", "1256"],
    "ฐ": ["6", "2345"],
    "ฑ": ["6", "23456"],
    "ฒ": ["36", "23456"],
    "ณ": ["6", "1345"],
    "ด": ["145"],
    "ต": ["1256"],
    "ถ": ["2345"],
    "ท": ["23456"],
    "ธ": ["356", "23456"],
    "น": ["1345"],
    "บ": ["1236"],
    "ป": ["12346"],
    "ผ": ["1234"],
    "ฝ": ["1346"],
    "พ": ["1456"],
    "ฟ": ["1246"],
    "ภ": ["6", "1456"],
    "ม": ["134"],
    "ย": ["13456"],
    "ร": ["1235"],
    "ล": ["123"],
    "ว": ["2456"],
    "ศ": ["6", "234"],
    "ษ": ["36", "234"],
    "ส": ["234"],
    "ห": ["125"],
    "ฬ": ["6", "123"],
    "อ": ["135"],
    "ฮ": ["123456"],
    "ฤ": ["1235", "2"],
    "ฦ": ["123", "2"],
    "<N>": ["3456"],  # Number prefix (used by replace_number function)
    "1": ["1"],
    "2": ["12"],
    "3": ["14"],
    "4": ["145"],
    "5": ["15"],
    "6": ["124"],
    "7": ["1245"],
    "8": ["125"],
    "9": ["24"],
    "0": ["245"],
    "๑": ["1"],
    "๒": ["12"],
    "๓": ["14"],
    "๔": ["145"],
    "๕": ["15"],
    "๖": ["124"],
    "๗": ["1245"],
    "๘": ["125"],
    "๙": ["24"],
    "๐": ["245"],
    "ะ": ["1"],
    "า": ["16"],
    "ิ": ["12"],
    "ี": ["23"],
    "ุ": ["14"],
    "ู": ["25"],
    "ึ": ["246"],
    "ื": ["26"],
    "เ": ["124"],
    "โ": ["24"],
    "ั": ["345"],
    "ำ": ["1356"],
    "แ": ["126"],
    "ไ": ["156"],
    "ใ": ["156", "2"],
    "่": ["35"],
    "้": ["256"],
    "๊": ["2356"],
    "๋": ["236"],
    "์": ["356"],
    "ๆ": ["2"],
    " ": ["-1"],
    "ฯ": ["56", "23"],  # Thai abbreviation mark
    "ฯลฯ": ["56", "123"],  # Thai abbreviation (special multi-character case)
    ".": ["456", "256"],
    "@": ["1", "1"],
    "?": ["456", "236"],
    "!": ["456", "235"],
    ";": ["456", "23"],
    ":": ["456", "25"],
    "/": ["456", "34"],
    "\\": ["456", "16"],
    "-": ["36"],
    "=": ["56", "2356"],
    "%": ["4", "356"],
    '"': ["5", "2"],
    "(": ["5", "126"],
    ")": ["5", "345"],
}

# Special vowel patterns for Thai braille
_dict_2: dict[str, list[str]] = {
    "เ-อ": ["146"],
    "เ-ีย": ["12356"],
    "เ-ือ": ["12345"],
    "-ัว": ["15"],
    "เ-า": ["235"],
    "เ-าะ": ["135", "1"],
}

# Merge special vowel patterns into main mapping
thai_braille_mapping_dict = {**thai_braille_mapping_dict, **_dict_2}

# Template patterns for vowel matching
_v1: list[str] = ["เ-tอ", "เ-ีtย", "เ-ืtอ", "-ัtว", "เ-tา", "เ-tาะ"]

# Create trie for efficient pattern matching
char_trie: Trie = Trie(
    list(thai_braille_mapping_dict.keys()) + _v1 + [" ", "<N>"]
)

# Build vowel replacement patterns
_vowel_patterns: list[str] = [
    i.replace("-", "([ก-ฮ])").replace("t", "([่้๊๋])")
    + ",\\1"
    + i.replace("t", "")
    + "\\2"
    for i in _v1
]
_vowel_patterns += [
    i.replace("-", "([ก-ฮ])") + ",\\1" + i for i in _dict_2.keys()
]
_VOWELS: list[tuple[str, str]] = [
    (x.split(",")[0], x.split(",")[1]) for x in _vowel_patterns
]


def replace_number(word: str) -> str:
    """Add number prefix if word starts with a digit.

    :param str word: Word to check
    :return: Word with number prefix if applicable
    :rtype: str
    """
    if word and word[0] in "1234567890๐๑๒๓๔๕๖๗๘๙":
        return "<N>" + word
    return word


def _replace_vowels(word: str) -> str:
    """Replace complex Thai vowel patterns for braille conversion.

    :param str word: Word containing Thai vowels
    :return: Word with vowels replaced for braille processing
    :rtype: str
    """
    for pattern, replacement in _VOWELS:
        word = re.sub(pattern, replacement, word)
    return word


def thai_word_braille(word: str) -> str:
    """Convert a Thai word to braille representation.

    :param str word: Thai word to convert
    :return: Braille representation of the word
    :rtype: str

    :Example:

        >>> from pythainlp.braille import thai_word_braille
        >>> thai_word_braille("กก")
        '⠛⠛'
        >>> thai_word_braille("น้ำ")
        '⠝⠲⠵'
    """
    if not word:
        return ""
    word = _replace_vowels(word)
    word = replace_number(word)
    _temp: list[list[str]] = []
    for token in word_tokenize(word, custom_dict=char_trie, engine="mm"):
        if token.isspace() and len(token) > 1:
            # Handle multiple spaces by converting each space individually
            for char in token:
                if char in thai_braille_mapping_dict:
                    _temp.append(thai_braille_mapping_dict[char])
        elif token in thai_braille_mapping_dict:
            _temp.append(thai_braille_mapping_dict[token])
    if not _temp:
        return ""
    braille_obj = Braille(_temp)
    return braille_obj.tobraille()


def thai_text_braille(text: str) -> list[str]:
    """Convert Thai text to braille representation by word.

    :param str text: Thai text to convert
    :return: List of braille representations for each word
    :rtype: list[str]

    :Example:

        >>> from pythainlp.braille import thai_text_braille
        >>> thai_text_braille("สวัสดี ครับ")
        ['⠎⠺⠜⠎⠙⠆', ' ', '⠥⠗⠜⠧']
    """
    _list_braille: list[str] = []
    for token in word_tokenize(text):
        _list_braille.append(thai_word_braille(token))
    return _list_braille


class Braille:
    """Braille pattern converter.

    Converts dot number patterns to Unicode braille characters.
    """

    def __init__(self, data: Union[list[list[str]], list[str], str]) -> None:
        """Initialize Braille converter.

        :param data: Braille dot patterns as list or string
        :type data: Union[list[list[str]], list[str], str]
        """
        self.inputdata: Union[list[list[str]], list[str], str] = data
        if isinstance(data, list):
            if len(data) > 1:
                nested_data: list[list[str]] = [[] for _ in range(len(data))]
                for i, item in enumerate(data):
                    nested_data[i] = sorted(item)
                self.data: Union[list[list[str]], list[str]] = nested_data
            elif len(data) == 1:
                self.data = sorted(list(data[0]))
            else:
                self.data = []
        else:
            self.data = sorted(list(data)) if data else []

        # International standard Braille mapping
        # Dots 1,2,3 = left column (top, middle, bottom)
        # Dots 4,5,6 = right column (top, middle, bottom)
        # Dots 7,8 = bottom row (left, right) for 8-dot Braille
        self.db: dict[str, str] = {
            "-1": " ",
            "0": "⠀",
            "1": "⠁",
            "12": "⠃",
            "123": "⠇",
            "1234": "⠏",
            "12345": "⠟",
            "123456": "⠿",
            "1234567": "⡿",
            "12345678": "⣿",
            "1234568": "⢿",
            "123457": "⡟",
            "1234578": "⣟",
            "123458": "⢟",
            "12346": "⠯",
            "123467": "⡯",
            "1234678": "⣯",
            "123468": "⢯",
            "12347": "⡏",
            "123478": "⣏",
            "12348": "⢏",
            "1235": "⠗",
            "12356": "⠷",
            "123567": "⡷",
            "1235678": "⣷",
            "123568": "⢷",
            "12357": "⡗",
            "123578": "⣗",
            "12358": "⢗",
            "1236": "⠧",
            "12367": "⡧",
            "123678": "⣧",
            "12368": "⢧",
            "1237": "⡇",
            "12378": "⣇",
            "1238": "⢇",
            "124": "⠋",
            "1245": "⠛",
            "12456": "⠻",
            "124567": "⡻",
            "1245678": "⣻",
            "124568": "⢻",
            "12457": "⡛",
            "124578": "⣛",
            "12458": "⢛",
            "1246": "⠫",
            "12467": "⡫",
            "124678": "⣫",
            "12468": "⢫",
            "1247": "⡋",
            "12478": "⣋",
            "1248": "⢋",
            "125": "⠓",
            "1256": "⠳",
            "12567": "⡳",
            "125678": "⣳",
            "12568": "⢳",
            "1257": "⡓",
            "12578": "⣓",
            "1258": "⢓",
            "126": "⠣",
            "1267": "⡣",
            "12678": "⣣",
            "1268": "⢣",
            "127": "⡃",
            "1278": "⣃",
            "128": "⢃",
            "13": "⠅",
            "134": "⠍",
            "1345": "⠝",
            "13456": "⠽",
            "134567": "⡽",
            "1345678": "⣽",
            "134568": "⢽",
            "13457": "⡝",
            "134578": "⣝",
            "13458": "⢝",
            "1346": "⠭",
            "13467": "⡭",
            "134678": "⣭",
            "13468": "⢭",
            "1347": "⡍",
            "13478": "⣍",
            "1348": "⢍",
            "135": "⠕",
            "1356": "⠵",
            "13567": "⡵",
            "135678": "⣵",
            "13568": "⢵",
            "1357": "⡕",
            "13578": "⣕",
            "1358": "⢕",
            "136": "⠥",
            "1367": "⡥",
            "13678": "⣥",
            "1368": "⢥",
            "137": "⡅",
            "1378": "⣅",
            "138": "⢅",
            "14": "⠉",
            "145": "⠙",
            "1456": "⠹",
            "14567": "⡹",
            "145678": "⣹",
            "14568": "⢹",
            "1457": "⡙",
            "14578": "⣙",
            "1458": "⢙",
            "146": "⠩",
            "1467": "⡩",
            "14678": "⣩",
            "1468": "⢩",
            "147": "⡉",
            "1478": "⣉",
            "148": "⢉",
            "15": "⠑",
            "156": "⠱",
            "1567": "⡱",
            "15678": "⣱",
            "1568": "⢱",
            "157": "⡑",
            "1578": "⣑",
            "158": "⢑",
            "16": "⠡",
            "167": "⡡",
            "1678": "⣡",
            "168": "⢡",
            "17": "⡁",
            "178": "⣁",
            "18": "⢁",
            "2": "⠂",
            "23": "⠆",
            "234": "⠎",
            "2345": "⠞",
            "23456": "⠾",
            "234567": "⡾",
            "2345678": "⣾",
            "234568": "⢾",
            "23457": "⡞",
            "234578": "⣞",
            "23458": "⢞",
            "2346": "⠮",
            "23467": "⡮",
            "234678": "⣮",
            "23468": "⢮",
            "2347": "⡎",
            "23478": "⣎",
            "2348": "⢎",
            "235": "⠖",
            "2356": "⠶",
            "23567": "⡶",
            "235678": "⣶",
            "23568": "⢶",
            "2357": "⡖",
            "23578": "⣖",
            "2358": "⢖",
            "236": "⠦",
            "2367": "⡦",
            "23678": "⣦",
            "2368": "⢦",
            "237": "⡆",
            "2378": "⣆",
            "238": "⢆",
            "24": "⠊",
            "245": "⠚",
            "2456": "⠺",
            "24567": "⡺",
            "245678": "⣺",
            "24568": "⢺",
            "2457": "⡚",
            "24578": "⣚",
            "2458": "⢚",
            "246": "⠪",
            "2467": "⡪",
            "24678": "⣪",
            "2468": "⢪",
            "247": "⡊",
            "2478": "⣊",
            "248": "⢊",
            "25": "⠒",
            "256": "⠲",
            "2567": "⡲",
            "25678": "⣲",
            "2568": "⢲",
            "257": "⡒",
            "2578": "⣒",
            "258": "⢒",
            "26": "⠢",
            "267": "⡢",
            "2678": "⣢",
            "268": "⢢",
            "27": "⡂",
            "278": "⣂",
            "28": "⢂",
            "3": "⠄",
            "34": "⠌",
            "345": "⠜",
            "3456": "⠼",
            "34567": "⡼",
            "345678": "⣼",
            "34568": "⢼",
            "3457": "⡜",
            "34578": "⣜",
            "3458": "⢜",
            "346": "⠬",
            "3467": "⡬",
            "34678": "⣬",
            "3468": "⢬",
            "347": "⡌",
            "3478": "⣌",
            "348": "⢌",
            "35": "⠔",
            "356": "⠴",
            "3567": "⡴",
            "35678": "⣴",
            "3568": "⢴",
            "357": "⡔",
            "3578": "⣔",
            "358": "⢔",
            "36": "⠤",
            "367": "⡤",
            "3678": "⣤",
            "368": "⢤",
            "37": "⡄",
            "378": "⣄",
            "38": "⢄",
            "4": "⠈",
            "45": "⠘",
            "456": "⠸",
            "4567": "⡸",
            "45678": "⣸",
            "4568": "⢸",
            "457": "⡘",
            "4578": "⣘",
            "458": "⢘",
            "46": "⠨",
            "467": "⡨",
            "4678": "⣨",
            "468": "⢨",
            "47": "⡈",
            "478": "⣈",
            "48": "⢈",
            "5": "⠐",
            "56": "⠰",
            "567": "⡰",
            "5678": "⣰",
            "568": "⢰",
            "57": "⡐",
            "578": "⣐",
            "58": "⢐",
            "6": "⠠",
            "67": "⡠",
            "678": "⣠",
            "68": "⢠",
            "7": "⡀",
            "78": "⣀",
            "8": "⢀",
        }

    def tobraille(self) -> str:
        """Convert dot patterns to braille Unicode characters.

        :return: Unicode braille representation
        :rtype: str
        """
        if not self.data:
            return ""
        if len(self.data) > 1 and isinstance(self.inputdata, list):
            result = ""
            for pattern in self.data:
                pattern_str = "".join(str("".join(pattern)))
                if pattern_str in self.db:
                    result += self.db[pattern_str]
            return result
        else:
            pattern_str = "".join(cast("list[str]", self.data))
            return self.db.get(pattern_str, "")

    def printbraille(self) -> str:
        """Mirror dot patterns for physical braille printing.

        International standard: swap 1↔4, 2↔5, 3↔6, 7↔8

        :return: Mirrored braille for printing
        :rtype: str
        """
        mirror_map: dict[str, str] = {
            "1": "4",
            "2": "5",
            "3": "6",
            "4": "1",
            "5": "2",
            "6": "3",
            "7": "8",
            "8": "7",
        }

        if len(self.data) > 1 and isinstance(self.inputdata, list):
            mirrored_patterns: list[str] = []
            for pattern in self.data:
                mirrored = "".join(mirror_map[dot] for dot in pattern)
                mirrored_sorted = "".join(sorted(mirrored))
                mirrored_patterns.append(self.db[mirrored_sorted])
            mirrored_patterns.reverse()
            return "".join(mirrored_patterns)
        else:
            mirrored = "".join(
                mirror_map[dot] for dot in cast("list[str]", self.data)
            )
            mirrored_sorted = "".join(sorted(mirrored))
            return self.db[mirrored_sorted]
