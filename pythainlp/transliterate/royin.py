# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
The Royal Thai General System of Transcription (RTGS)
is the official system for rendering Thai words in the Latin alphabet.
It was published by the Royal Institute of Thailand.

:See Also:
    * `Wikipedia`_

.. _Wikipedia:
    https://en.wikipedia.org/wiki/Royal_Thai_General_System_of_Transcription
"""

from __future__ import annotations

import re
from typing import Optional

from pythainlp import thai_consonants, word_tokenize

_ROMANIZED_VOWELS: str = "aeiou"

# Vowel patterns: Thai pattern, replacement
_vowel_patterns: str = """เ*ียว,\\1iao
แ*็ว,\\1aeo
เ*ือย,\\1ueai
แ*ว,\\1aeo
เ*็ว,\\1eo
เ*ว,\\1eo
*ิว,\\1io
*วย,\\1uai
เ*ย,\\1oei
*อย,\\1oi
โ*ย,\\1oi
*ุย,\\1ui
*าย,\\1ai
ไ*ย,\\1ai
*ัย,\\1ai
ไ**,\\1\\2ai
ไ*,\\1ai
ใ*,\\1ai
*ว*,\\1ua\\2
*ัวะ,\\1ua
*ัว,\\1ua
เ*ือะ,\\1uea
เ*ือ,\\1uea
เ*ียะ,\\1ia
เ*ีย,\\1ia
เ*อะ,\\1oe
เ*อ,\\1oe
เ*ิ,\\1oe
*อ,\\1o
เ*าะ,\\1o
เ*็,\\1e
โ*ะ,\\1o
โ*,\\1o
แ*ะ,\\1ae
แ*,\\1ae
เ*าะ,\\1e
*าว,\\1ao
เ*า,\\1ao
เ*,\\1e
*ู,\\1u
*ุ,\\1u
*ื,\\1ue
*ึ,\\1ue
*ี,\\1i
*ิ,\\1i
*ำ,\\1am
*า,\\1a
*ั,\\1a
*ะ,\\1a
#ฤ,\\1rue
$ฤ,\\1ri"""
_vowel_patterns = _vowel_patterns.replace("*", f"([{thai_consonants}])")
_vowel_patterns = _vowel_patterns.replace("#", "([คนพมห])")
_vowel_patterns = _vowel_patterns.replace("$", "([กตทปศส])")

_VOWELS: list[list[str]] = [x.split(",") for x in _vowel_patterns.split("\n")]

# พยัญชนะ ต้น สะกด
_CONSONANTS: dict[str, list[str]] = {
    "ก": ["k", "k"],
    "ข": ["kh", "k"],
    "ฃ": ["kh", "k"],
    "ค": ["kh", "k"],
    "ฅ": ["kh", "k"],
    "ฆ": ["kh", "k"],
    "ง": ["ng", "ng"],
    "จ": ["ch", "t"],
    "ฉ": ["ch", "t"],
    "ช": ["ch", "t"],
    "ซ": ["s", "t"],
    "ฌ": ["ch", "t"],
    "ญ": ["y", "n"],
    "ฎ": ["d", "t"],
    "ฏ": ["t", "t"],
    "ฐ": ["th", "t"],
    # ฑ พยัญชนะต้น เป็น d ได้
    "ฑ": ["th", "t"],
    "ฒ": ["th", "t"],
    "ณ": ["n", "n"],
    "ด": ["d", "t"],
    "ต": ["t", "t"],
    "ถ": ["th", "t"],
    "ท": ["th", "t"],
    "ธ": ["th", "t"],
    "น": ["n", "n"],
    "บ": ["b", "p"],
    "ป": ["p", "p"],
    "ผ": ["ph", "p"],
    "ฝ": ["f", "p"],
    "พ": ["ph", "p"],
    "ฟ": ["f", "p"],
    "ภ": ["ph", "p"],
    "ม": ["m", "m"],
    "ย": ["y", ""],
    "ร": ["r", "n"],
    "ฤ": ["rue", ""],
    "ล": ["l", "n"],
    "ว": ["w", ""],
    "ศ": ["s", "t"],
    "ษ": ["s", "t"],
    "ส": ["s", "t"],
    "ห": ["h", ""],
    "ฬ": ["l", "n"],
    "อ": ["", ""],
    "ฮ": ["h", ""],
}

_THANTHAKHAT: str = "\u0e4c"
_RE_CONSONANT: re.Pattern[str] = re.compile(f"[{thai_consonants}]")
_RE_NORMALIZE: re.Pattern[str] = re.compile(
    f"จน์|มณ์|ณฑ์|ทร์|ตร์|[{thai_consonants}]{_THANTHAKHAT}|"
    f"[{thai_consonants}][\u0e30-\u0e39]{_THANTHAKHAT}"
    # Paiyannoi, Maiyamok, Tonemarks, Thanthakhat, Nikhahit, other signs
    r"|[\u0e2f\u0e46\u0e48-\u0e4f\u0e5a\u0e5b]"
)


def _normalize(word: str) -> str:
    """
    Remove silence, no sound, and tonal characters.

    ตัดอักษรที่ไม่ออกเสียง (การันต์ ไปยาลน้อย ไม้ยมก*) และวรรณยุกต์ทิ้ง
    """
    return _RE_NORMALIZE.sub("", word)


def _replace_vowels(word: str) -> str:
    for vowel in _VOWELS:
        word = re.sub(vowel[0], vowel[1], word)

    return word


_HO_HIP: str = "\u0e2b"  # ห
_RO_RUA: str = "\u0e23"  # ร
_LO_LING: str = "\u0e25"  # ล
_WO_WAEN: str = "\u0e27"  # ว
_DOUBLE_RO_RUA: str = _RO_RUA + _RO_RUA

# Consonants that can be second in a cluster
_CLUSTER_SECOND: frozenset[str] = frozenset({_RO_RUA, _LO_LING, _WO_WAEN})


def _double_ro_rua(word: str, i: int) -> Optional[list[str]]:
    """Return romanized chars for double RO RUA (รร) at i, or None."""
    if word[i:] == _DOUBLE_RO_RUA:  # at the end of the word
        return ["a", "n"]
    if word[i : i + 2] == _DOUBLE_RO_RUA:
        return ["a"]
    return None


def _initial_consonant(
    word: str, i: int, consonants: str, j: int, mod_chars: list[str]
) -> tuple[list[str], bool]:
    """
    Romanize a consonant of an initial cluster.

    :return: romanized chars to append, and the new vowel-seen flag
    """
    # mod_chars contains romanized output: look for non-vowel characters
    if not any(c and c not in _ROMANIZED_VOWELS for c in mod_chars):
        # First consonant in the cluster; an empty initial (e.g. อ) is skipped
        initial = _CONSONANTS[consonants[j]][0]
        return ([initial] if initial else []), False

    is_cluster_consonant = word[i] in _CLUSTER_SECOND
    is_last_char = i + 1 >= len(word)

    if is_cluster_consonant and not is_last_char:
        # ร/r, ล/l, or ว/w after the first consonant is part of the initial
        # cluster (e.g. กรม/krom: ก/k+ร/r are cluster, ม/m is final)
        return [_CONSONANTS[consonants[j]][0]], False
    if not is_cluster_consonant and not is_last_char:
        # Start of a new syllable: close the previous one with implicit "a"
        initial = _CONSONANTS[consonants[j]][0]
        return (["a", initial] if initial else ["a"]), False
    # Last character without a vowel: final consonant with implicit "o"
    return ["o", _CONSONANTS[consonants[j]][1]], True


def _consonant_after_vowel(
    word: str, i: int, consonants: str, j: int
) -> tuple[str, bool]:
    """
    Romanize a consonant after a vowel: final or start of a new syllable.

    :return: romanized string to append, and the new vowel-seen flag
    """
    if i + 1 < len(word) and word[i + 1] not in _CONSONANTS:
        return _CONSONANTS[consonants[j]][0], False  # new syllable
    return _CONSONANTS[consonants[j]][1], True


def _replace_consonants(word: str, consonants: str) -> str:
    if not consonants:
        return word

    mod_chars: list[str] = []
    skip = False
    j = 0  # index of the consonants string
    vowel_seen = False  # True once a non-consonant character is seen

    for i in range(len(word)):
        char = word[i]
        if skip:
            skip = False
            j += 1
        elif char not in _CONSONANTS:  # not a Thai consonant
            vowel_seen = True
            mod_chars.append(char)
        elif not mod_chars and char == _HO_HIP and len(consonants) != 1:
            # Skip HO HIP unless it is the only consonant
            j += 1
        else:
            double_ro_rua = _double_ro_rua(word, i)
            if double_ro_rua is not None:
                mod_chars.extend(double_ro_rua)
                skip = True
                vowel_seen = True  # "a" acts as a vowel
            elif not vowel_seen:
                chars, vowel_seen = _initial_consonant(
                    word, i, consonants, j, mod_chars
                )
                mod_chars.extend(chars)
            else:
                final, vowel_seen = _consonant_after_vowel(
                    word, i, consonants, j
                )
                mod_chars.append(final)
            j += 1
    return "".join(mod_chars)


def _romanize(word: str) -> str:
    # A lone ห is silent
    if word == "ห":
        return ""

    word = _replace_vowels(_normalize(word))
    # Use the same membership test as _replace_consonants(), which treats
    # every key of _CONSONANTS as a consonant. _RE_CONSONANT only matches
    # thai_consonants, so it misses ฤ and the two lists fall out of sync.
    consonants = [c for c in word if c in _CONSONANTS]

    # 2-character word, all consonants
    if len(word) == 2 and len(consonants) == 2:
        word_list = list(word)
        word_list.insert(1, "o")
        word = "".join(word_list)

    word = _replace_consonants(word, "".join(consonants))
    return word


def _should_add_syllable_separator(
    prev_word: str, curr_word: str, prev_romanized: str
) -> bool:
    """
    Determine if 'a' should be added between two romanized syllables.

    This applies when:

    * the previous word has an explicit vowel and ends with a consonant
    * the current word is a 2-consonant cluster with no vowels
      (e.g., 'กร')

    :param prev_word: previous Thai word
    :param curr_word: current Thai word
    :param prev_romanized: romanized form of the previous word
    :return: ``True`` if 'a' should be added before the current word
    """
    if not prev_romanized or len(curr_word) < 2:
        return False

    prev_normalized = _normalize(prev_word)
    prev_after_vowels = _replace_vowels(prev_normalized)
    prev_consonants = _RE_CONSONANT.findall(prev_word)
    has_explicit_vowel_prev = len(prev_after_vowels) > len(prev_consonants)

    consonants_in_word = _RE_CONSONANT.findall(curr_word)
    vowels_in_word = len(curr_word) - len(consonants_in_word)

    return (
        has_explicit_vowel_prev
        and len(consonants_in_word) == 2
        and vowels_in_word == 0
        and prev_romanized[-1] not in _ROMANIZED_VOWELS
    )


def romanize(text: str) -> str:
    """
    Render Thai words in the Latin alphabet, using RTGS.

    The Royal Thai General System of Transcription (RTGS) is the
    official system by the Royal Institute of Thailand.

    :param str text: Thai text to be romanized
    :return: text rendered in the Latin alphabet
    :rtype: str
    """
    words = word_tokenize(text)
    romanized_words: list[str] = []

    for i, word in enumerate(words):
        romanized = _romanize(word)

        if i > 0 and romanized:
            prev_word = words[i - 1]
            prev_romanized = romanized_words[-1] if romanized_words else ""
            if _should_add_syllable_separator(prev_word, word, prev_romanized):
                romanized = "a" + romanized

        romanized_words.append(romanized)

    return "".join(romanized_words)
