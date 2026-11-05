# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai names of Thai vowels, marks, and symbols."""

from __future__ import annotations

from typing import Final

_char_to_name: Final[dict[str, str]] = {
    "\u0e2f": "ไปยาลน้อย",
    "\u0e30": "สระอะ",
    "\u0e31": "ไม้หันอากาศ",
    "\u0e32": "สระอา",
    "\u0e33": "สระอำ",
    "\u0e34": "สระอิ",
    "\u0e35": "สระอี",
    "\u0e36": "สระอึ",
    "\u0e37": "สระอือ",
    "\u0e38": "สระอุ",
    "\u0e39": "สระอู",
    "\u0e3a": "พินทุ",
    "\u0e40": "สระเอ",
    "\u0e41": "สระแอ",
    "\u0e42": "สระโอ",
    "\u0e43": "สระใอไม้ม้วน",
    "\u0e44": "สระไอไม้มลาย",
    "\u0e45": "ลากข้าง",
    "\u0e46": "ไม้ยมก",
    "\u0e47": "ไม้ไต่คู้",
    "\u0e48": "ไม้เอก",
    "\u0e49": "ไม้โท",
    "\u0e4a": "ไม้ตรี",
    "\u0e4b": "ไม้จัตวา",
    "\u0e4c": "ทัณฑฆาต",
    "\u0e4d": "นิคหิต",
    "\u0e4e": "ยามักการ",
    "\u0e4f": "ฟองมัน",
    "\u0e5a": "อังคั่นคู่",
    "\u0e5b": "โคมูตร",
}

_alias_to_char: Final[dict[str, str]] = {
    "การันต์": "\u0e4c",
    "ตาไก่": "\u0e4f",
    "นฤคหิต": "\u0e4d",
    "วิสรรชนีย์": "\u0e30",
    "ไม้ทัณฑฆาต": "\u0e4c",
    "ไม้ผัด": "\u0e31",
    "ไม้มลาย": "\u0e44",
    "ไม้ม้วน": "\u0e43",
    "ไม้ยามักการ": "\u0e4e",
}

_name_to_char: Final[dict[str, str]] = {
    **{name: ch for ch, name in _char_to_name.items()},
    **_alias_to_char,
}


def thai_name_to_char(name: str) -> str:
    """
    Get a Thai vowel, mark, or symbol from its Thai name.

    Useful for typing characters that are not on a Thai keyboard,
    such as Yamakkan, Fongman, Angkhankhu, and Khomut.

    :param str name: Thai name of the character, such as "ยามักการ"
        or "ไม้ยามักการ"
    :return: the character
    :rtype: str
    :raises ValueError: if the name is unknown

    :Example:

        >>> from pythainlp.util import thai_name_to_char
        >>> thai_name_to_char("โคมูตร")
        '๛'
        >>> thai_name_to_char("ฟองมัน")
        '๏'
    """
    key = name.strip() if isinstance(name, str) else ""
    if key not in _name_to_char:
        raise ValueError(f"Unknown Thai character name: {name!r}")
    return _name_to_char[key]


def thai_char_to_name(ch: str) -> str:
    """
    Get the Thai name of a Thai vowel, mark, or symbol.

    :param str ch: a single Thai vowel, mark, or symbol, without
        a placeholder such as "◌"
    :return: Thai name of the character
    :rtype: str
    :raises ValueError: if the character has no name in the dictionary

    :Example:

        >>> from pythainlp.util import thai_char_to_name
        >>> thai_char_to_name("๛")
        'โคมูตร'
        >>> thai_char_to_name("่")
        'ไม้เอก'
    """
    if not isinstance(ch, str) or ch not in _char_to_name:
        raise ValueError(f"No Thai name for character: {ch!r}")
    return _char_to_name[ch]
