# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""The Royal Thai General System of Transcription (RTGS)
is the official system for rendering Thai words in the Latin alphabet.
It was published by the Royal Institute of Thailand.

:See Also:
    * `Wikipedia <https://en.wikipedia.org/wiki/Royal_Thai_General_System_of_Transcription>`_
"""

from __future__ import annotations

import re

from pythainlp import thai_consonants, word_tokenize

# Romanized vowels for checking
_ROMANIZED_VOWELS: str = "aeiou"

# vowel
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
    """Remove silence, no sound, and tonal characters.

    ตัดอักษรที่ไม่ออกเสียง (การันต์ ไปยาลน้อย ไม้ยมก*) และวรรณยุกต์ทิ้ง
    """
    return _RE_NORMALIZE.sub("", word)


def _replace_vowels(word: str) -> str:
    for vowel in _VOWELS:
        word = re.sub(vowel[0], vowel[1], word)

    return word


def _replace_consonants(word: str, consonants: str) -> str:
    _HO_HIP = "\u0e2b"  # ห
    _RO_RUA = "\u0e23"  # ร
    _LO_LING = "\u0e25"  # ล
    _WO_WAEN = "\u0e27"  # ว
    _DOUBLE_RO_RUA = _RO_RUA + _RO_RUA

    # Consonants that can be second in a cluster
    _CLUSTER_SECOND = {_RO_RUA, _LO_LING, _WO_WAEN}

    if not consonants:
        return word

    skip = False
    mod_chars = []
    j = 0  # j is the index of consonants
    vowel_seen = False  # Track if we've seen a vowel (non-consonant character)

    for i in range(len(word)):
        if skip:
            skip = False
            j += 1
        elif word[i] not in _CONSONANTS:  # word[i] is not a Thai consonant.
            vowel_seen = True
            mod_chars.append(word[i])
        elif (
            len(mod_chars) == 0 and word[i] == _HO_HIP and len(consonants) != 1
        ):  # Skip HO HIP except that HO HIP is the only one consonant
            j += 1
        elif word[i:] == _DOUBLE_RO_RUA:  # Double RO RUA is in end of word
            skip = True
            mod_chars.append("a")
            mod_chars.append("n")
            vowel_seen = True  # 'a' acts as a vowel
            j += 1
        elif word[i : i + 2] == _DOUBLE_RO_RUA:
            skip = True
            mod_chars.append("a")
            vowel_seen = True  # 'a' acts as a vowel
            j += 1
        elif not vowel_seen:  # Building initial consonant cluster
            # Check if we've added any actual initial consonants (non-empty romanized characters)
            # We check for non-vowel characters since mod_chars contains romanized output
            has_initial = any(
                c and c not in _ROMANIZED_VOWELS for c in mod_chars
            )

            if not has_initial:
                # First consonant in the cluster
                initial = _CONSONANTS[consonants[j]][0]
                if (
                    initial
                ):  # Only append if not empty (e.g., อ has empty initial)
                    mod_chars.append(initial)
                j += 1
            else:
                # Check if this consonant can be part of a cluster
                is_cluster_consonant = word[i] in _CLUSTER_SECOND
                is_last_char = i + 1 >= len(word)
                has_vowel_next = (
                    not is_last_char and word[i + 1] not in _CONSONANTS
                )

                # Cluster consonants (ร/r, ล/l, ว/w) are part of initial cluster if:
                # - followed by a vowel, OR
                # - not the last character (e.g., กรม/krom: ก/k+ร/r are cluster, ม/m is final)
                if is_cluster_consonant and (
                    has_vowel_next or not is_last_char
                ):
                    # This is part of initial cluster (ร/r, ล/l, or ว/w after first consonant)
                    mod_chars.append(_CONSONANTS[consonants[j]][0])
                    j += 1
                elif not is_cluster_consonant and not is_last_char:
                    # Not a cluster consonant, and there are more characters
                    # This likely starts a new syllable, so add implicit 'a' to previous syllable
                    mod_chars.append("a")
                    vowel_seen = True
                    # Now process this consonant as start of new syllable
                    initial = _CONSONANTS[consonants[j]][0]
                    if initial:  # Only append if not empty
                        mod_chars.append(initial)
                    vowel_seen = False  # Reset for new syllable
                    j += 1
                elif has_vowel_next:
                    # Not a cluster consonant, but vowel follows - still initial
                    mod_chars.append(_CONSONANTS[consonants[j]][0])
                    j += 1
                elif is_last_char:
                    # This is a final consonant with no vowel, need to add 'o'
                    mod_chars.append("o")
                    mod_chars.append(_CONSONANTS[consonants[j]][1])
                    vowel_seen = True
                    j += 1
                else:
                    # There's another consonant after this one
                    # Add implicit 'o' and treat this as final
                    mod_chars.append("o")
                    mod_chars.append(_CONSONANTS[consonants[j]][1])
                    vowel_seen = True
                    j += 1
        else:  # After vowel - could be final consonant or start of new syllable
            has_vowel_next = (
                i + 1 < len(word) and word[i + 1] not in _CONSONANTS
            )
            if has_vowel_next:
                # Consonant followed by vowel - start of new syllable
                mod_chars.append(_CONSONANTS[consonants[j]][0])
                vowel_seen = False  # Reset for new syllable
                j += 1
            else:
                # No vowel follows - this is a final consonant
                mod_chars.append(_CONSONANTS[consonants[j]][1])
                j += 1
    return "".join(mod_chars)


# support function for romanize()
def _romanize(word: str) -> str:
    # Special case: single ห character should be empty (silent)
    if word == "ห":
        return ""

    word = _replace_vowels(_normalize(word))
    consonants = _RE_CONSONANT.findall(word)

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
    """Determine if 'a' should be added between two romanized syllables.

    This applies when:
    - Previous word has explicit vowel and ends with consonant
    - Current word is a 2-consonant cluster with no vowels (e.g., 'กร')

    :param prev_word: The previous Thai word/token
    :param curr_word: The current Thai word/token
    :param prev_romanized: The romanized form of the previous word
    :return: True if 'a' should be added before the current word
    """
    if not prev_romanized or len(curr_word) < 2:
        return False

    # Check if previous word has explicit vowel
    prev_normalized = _normalize(prev_word)
    prev_after_vowels = _replace_vowels(prev_normalized)
    prev_consonants = _RE_CONSONANT.findall(prev_word)
    has_explicit_vowel_prev = len(prev_after_vowels) > len(prev_consonants)

    # Check if current word is 2 Thai consonants with no vowel
    consonants_in_word = _RE_CONSONANT.findall(curr_word)
    vowels_in_word = len(curr_word) - len(consonants_in_word)

    # Add 'a' if conditions are met
    return (
        has_explicit_vowel_prev
        and len(consonants_in_word) == 2
        and vowels_in_word == 0
        and prev_romanized[-1] not in _ROMANIZED_VOWELS
    )


def romanize(text: str) -> str:
    """Render Thai words in Latin alphabet, using RTGS

    Royal Thai General System of Transcription (RTGS),
    is the official system by the Royal Institute of Thailand.

    :param text: Thai text to be romanized
    :type text: str
    :return: A string of Thai words rendered in the Latin alphabet
    :rtype: str
    """
    words = word_tokenize(text)
    romanized_words: list[str] = []

    for i, word in enumerate(words):
        romanized = _romanize(word)

        # Check if we need to add syllable separator 'a'
        if i > 0 and romanized:
            prev_word = words[i - 1]
            prev_romanized = romanized_words[-1] if romanized_words else ""
            if _should_add_syllable_separator(prev_word, word, prev_romanized):
                romanized = "a" + romanized

        romanized_words.append(romanized)

    return "".join(romanized_words)
