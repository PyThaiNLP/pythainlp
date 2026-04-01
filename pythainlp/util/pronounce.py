# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import re
from functools import lru_cache

from pythainlp import thai_consonants, thai_tonemarks
from pythainlp.corpus import thai_words
from pythainlp.khavee import KhaveeVerifier
from pythainlp.tokenize import Tokenizer, syllable_tokenize
from pythainlp.util import remove_tonemark

kv: KhaveeVerifier = KhaveeVerifier()


@lru_cache(maxsize=None)
def _single_syllable_thai_words() -> list[str]:
    """Return cached list of single-syllable Thai words."""
    return [i for i in thai_words() if len(syllable_tokenize(i)) == 1]


@lru_cache(maxsize=1024)
def rhyme(word: str) -> list[str]:
    """Find Thai rhyme

    :param str word: A Thai word
    :return: All list Thai rhyme words
    :rtype: List[str]

    :Example:

        >>> from pythainlp.util import rhyme  # doctest: +SKIP
        >>> rhyme("จีบ")  # doctest: +SKIP
        ['กลีบ', 'กีบ', 'ครีบ', 'คีบ', 'งีบ', ... ]
    """
    return sorted(
        i
        for i in _single_syllable_thai_words()
        if kv.is_sumpus(word, i) and i != word
    )


_vowel_str: str = "".join(
    (
        "อะ,อา,อิ,อี,อึ,อื,อุ,อู,เอะ,เอ,แอะ,แอ,เอียะ,เอีย,เอือะ,เอือ,อัวะ,อัว,โอะ,",
        "โอ,เอาะ,ออ,เออะ,เออ,อำ,ใอ,ไอ,เอา,ฤ,ฤๅ,ฦ,ฦๅ",
    )
)
thai_vowel: list[str] = _vowel_str.split(",")
thai_vowel_all: list[tuple[str, str]] = [
    ("([ก-ฮ])ะ", "\\1อะ"),
    ("([ก-ฮ])า", "\\1อา"),
    ("อิ".replace("อ", "([ก-ฮ])"), "อิ".replace("อ", "\\1อ")),
    ("อี".replace("อ", "([ก-ฮ])"), "อี".replace("อ", "\\1อ")),
    ("อึ".replace("อ", "([ก-ฮ])", 1), "อึ".replace("อ", "\\1อ", 1)),
    ("อื".replace("อ", "([ก-ฮ])", 1), "อื".replace("อ", "\\1อ", 1)),
    ("อุ".replace("อ", "([ก-ฮ])", 1), "อุ".replace("อ", "\\1อ", 1)),
    ("อู".replace("อ", "([ก-ฮ])", 1), "อู".replace("อ", "\\1อ", 1)),
    ("เอะ".replace("อ", "([ก-ฮ])", 1), "\\1เอะ"),
    ("เอ".replace("อ", "([ก-ฮ])", 1), "\\1เอ"),
    ("แอะ".replace("อ", "([ก-ฮ])", 1), "\\1แอะ"),
    ("แอ".replace("อ", "([ก-ฮ])", 1), "\\1แอ"),
    ("เอียะ".replace("อ", "([ก-ฮ])", 1), "\\1เอียะ"),
    ("เอีย".replace("อ", "([ก-ฮ])", 1), "\\1เอีย"),
    ("เอือะ".replace("อ", "([ก-ฮ])", 1), "\\1เอือะ"),
    ("เอือ".replace("อ", "([ก-ฮ])", 1), "\\1เอือ"),
    ("อัวะ".replace("อ", "([ก-ฮ])", 1), "\\1อัวะ"),
    ("อัว".replace("อ", "([ก-ฮ])", 1), "\\1อัว"),
    ("โอะ".replace("อ", "([ก-ฮ])", 1), "\\1โอะ"),
    ("โอ".replace("อ", "([ก-ฮ])", 1), "\\1โอ"),
    ("เอาะ".replace("อ", "([ก-ฮ])", 1), "\\1เอาะ"),
    ("ออ".replace("อ", "([ก-ฮ])", 1), "\\1ออ"),
    ("เออะ".replace("อ", "([ก-ฮ])", 1), "\\1เออะ"),
    ("เออ".replace("อ", "([ก-ฮ])", 1), "\\1เออ"),
    ("อำ".replace("อ", "([ก-ฮ])", 1), "\\1อำ"),
    ("ใอ".replace("อ", "([ก-ฮ])", 1), "\\1ใอ"),
    ("ไอ".replace("อ", "([ก-ฮ])", 1), "\\1ไอ"),
    ("เอา".replace("อ", "([ก-ฮ])", 1), "\\1เอา"),
    ("อั".replace("อ", "([ก-ฮ])", 1), "\\1อะ"),
]
thai_vowel_all.sort(key=lambda t: len(t[0]), reverse=True)


def thai_consonant_to_spelling(c: str) -> str:
    """Thai consonants to spelling

    :param str c: A Thai consonant
    :return: spelling
    :rtype: str

    :Example:

        >>> from pythainlp.util import thai_consonant_to_spelling
        >>> print(thai_consonant_to_spelling("ก"))
        กอ
    """
    if len(c) == 1 and c in thai_consonants:
        return c + "อ"
    return c


def tone_to_spelling(t: str) -> str:
    """Thai tonemarks to spelling

    :param str t: A Thai tonemarks
    :return: spelling
    :rtype: str

    :Example:

        >>> from pythainlp.util import tone_to_spelling
        >>> print(tone_to_spelling("่"))  # ไม้เอก
        ไม้เอก
    """
    if t == "่":
        return "ไม้เอก"
    elif t == "้":
        return "ไม้โท"
    elif t == "๊":
        return "ไม้ตรี"
    elif t == "๋":
        return "ไม้จัตวา"
    return t


@lru_cache(maxsize=None)
def _spelling_tokenizer() -> Tokenizer:
    """Lazy-load and cache the vowel/consonant tokenizer used by spelling()."""
    return Tokenizer(
        custom_dict=thai_vowel + list(thai_consonants), engine="longest"
    )


@lru_cache(maxsize=1024)
def _spelling_impl(word: str) -> list[str]:
    """Cached implementation of spelling() for valid string inputs."""
    thai_vowel_tokenizer = _spelling_tokenizer()
    word_pre = remove_tonemark(word).replace("็", "")
    tone = [tone_to_spelling(i) for i in word if i in thai_tonemarks]
    word_output = word_pre
    for i, j in thai_vowel_all:
        if len(re.findall(i, word_pre, re.U)) > 0:
            if "็" in word and i == "เ([ก-ฮ])":
                word_output = re.sub(i, "\\1เอะ", word_pre)
            else:
                word_output = re.sub(i, j, word_pre)
            break
    list_word_output = thai_vowel_tokenizer.word_tokenize(word_output)
    output = [
        i
        for i in [thai_consonant_to_spelling(i) for i in list_word_output]
        if "์" not in i
    ]
    if word_pre == word:
        return output + [word]
    elif tone != []:
        return output + [word_pre, tone[0], word]
    elif "็" in word:
        return output + [word]
    else:
        return output + [word_pre, word]


def spelling(word: str) -> list[str]:
    """Thai word to spelling

    This function supports Thai root words only.

    :param str word: A Thai word
    :return: spelling
    :rtype: List[str]

    :Example:

        >>> from pythainlp.util import spelling
        >>> spelling("เรียน")
        ['รอ', 'เอีย', 'นอ', 'เรียน']
        >>> spelling("เฝ้า")
        ['ฝอ', 'เอา', 'เฝา', 'ไม้โท', 'เฝ้า']
    """
    if not word or not isinstance(word, str):
        return []
    return _spelling_impl(word)
