# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Syllable tools"""

from __future__ import annotations

import re
from typing import Pattern

from pythainlp import thai_consonants, thai_tonemarks

spelling_class: dict[str, list[str]] = {
    "กง": list("ง"),
    "กม": list("ม"),
    "เกย": list("ย"),
    "เกอว": list("ว"),
    "กน": list("นญณรลฬ"),
    "กก": list("กขคฆ"),
    "กด": list("ดจชซฎฏฐฑฒตถทธศษส"),
    "กบ": list("บปภพฟ"),
}

thai_consonants_all: set[str] = set(thai_consonants)
thai_consonants_all.remove("อ")

_temp: list[str] = list("".join(["".join(v) for v in spelling_class.values()]))
not_spelling_class: list[str] = [
    j for j in thai_consonants_all if j not in _temp
]

# vowel's short sound
short: str = "ะัิึุ"
re_short: Pattern[str] = re.compile(
    "เ(.*)ะ|แ(.*)ะ|เ(.*)อะ|โ(.*)ะ|เ(.*)าะ", re.U
)
pattern: Pattern[str] = re.compile("เ(.*)า", re.U)  # เ-า is live syllable

_check_1: list[str] = []
# These spelling consonants are live syllables.
for i in ["กง", "กน", "กม", "เกย", "เกอว"]:
    _check_1.extend(spelling_class[i])

# These spelling consonants are dead syllables.
_check_2: list[str] = (
    spelling_class["กก"] + spelling_class["กบ"] + spelling_class["กด"]
)

thai_low_sonorants: list[str] = list("งนมยรลว")
thai_low_aspirates: list[str] = list("คชซทพฟฮ")
thai_low_irregular: list[str] = list("ฆญณธภฅฌฑฒฬ")

thai_mid_plains: list[str] = list("กจดตบปอฎฏ")

thai_high_aspirates: list[str] = list("ขฉถผฝสห")
thai_high_irregular: list[str] = list("ศษฃฐ")
thai_initial_consonant_type: dict[str, list[str]] = {
    "low": thai_low_sonorants + thai_low_aspirates + thai_low_irregular,
    "mid": thai_mid_plains,
    "high": thai_high_aspirates + thai_high_irregular,
}
thai_initial_consonant_to_type: dict[str, str] = {}

k: str
v: list[str]
for k, v in thai_initial_consonant_type.items():
    for i in v:
        thai_initial_consonant_to_type[i] = k


def sound_syllable(syllable: str) -> str:
    """Sound syllable classification

    This function is sound syllable classification.
    The syllable is a live syllable or dead syllable.

    :param str syllable: Thai syllable
    :return: syllable's type ("live" or "dead")
    :rtype: str

    :Example:

        >>> from pythainlp.util import sound_syllable
        >>> sound_syllable("มา")
        'live'
        >>> sound_syllable("เลข")
        'dead'
    """
    # if len of syllable < 2
    if len(syllable) < 2:
        return "dead"

    # get consonants
    consonants = [i for i in syllable if i in thai_consonants_all]
    if (
        (len(consonants) == 0)
        and ("อ" in syllable)
        and any((c in set("เ")) for c in syllable)
        and (len(syllable) == 2)
    ):
        return "live"

    # Handle syllables with only อ (no other consonants from thai_consonants_all)
    if len(consonants) == 0 and "อ" in syllable:
        # Syllables with only อ and long vowels are live
        if any((c in set("าีืแูเโไใำ")) for c in syllable):
            return "live"
        # Short vowels or special cases
        if any((c in set(short)) for c in syllable):
            return "dead"
        # Default to live for vowel-only syllables
        return "live"

    # get spelling consonants
    spelling_consonant = consonants[-1]
    if (spelling_consonant in _check_2) and (
        any((c in set("าีืแูาเโ")) for c in syllable) is False
        and any((c in set("ำใไ")) for c in syllable) is False
        and bool(pattern.search(syllable)) is not True
    ):
        return "dead"

    if any((c in set("าีืแูาโ")) for c in syllable):  # in syllable:
        if (
            spelling_consonant in _check_1
            and bool(re_short.search(syllable)) is not True
        ):
            return "live"

        if (
            spelling_consonant != syllable[-1]
            and bool(re_short.search(syllable)) is not True
        ):
            return "live"

        if spelling_consonant in _check_2:
            return "dead"

        if bool(re_short.search(syllable)) or any(
            (c in set(short)) for c in syllable
        ):
            return "dead"

        return "live"

    if any((c in set("ำใไ")) for c in syllable):
        return "live"  # if these vowel's long sounds are live syllables

    if bool(pattern.search(syllable)):  # if it is เ-า
        return "live"

    if spelling_consonant in _check_1:
        if (
            bool(re_short.search(syllable))
            or any((c in set(short)) for c in syllable)
        ) and len(consonants) < 2:
            return "dead"

        if syllable[-1] in set(short):
            return "dead"

        return "live"

    if bool(
        re_short.search(syllable)
    ) or any(  # if vowel's short sound is found
        (c in set(short)) for c in syllable
    ):  # consonant in short
        return "dead"

    return "dead"


def syllable_open_close_detector(syllable: str) -> str:
    """Open/close Thai syllables detector

    This function is used for finding Thai syllables that are open or closed sound.

    :param str syllable: Thai syllable
    :return: open / close
    :rtype: str

    :Example:

        >>> from pythainlp.util import syllable_open_close_detector
        >>> syllable_open_close_detector("มาก")
        'close'
        >>> syllable_open_close_detector("คะ")
        'open'
    """
    consonants = [i for i in syllable if i in thai_consonants]

    if len(consonants) < 2:
        return "open"

    if len(consonants) == 2 and consonants[-1] == "อ":
        return "open"

    return "close"


def syllable_length(syllable: str) -> str:
    """Thai syllable length

    This function is used for finding syllable's length. (long or short)

    :param str syllable: Thai syllable
    :return: syllable's length (long or short)
    :rtype: str

    :Example:

        >>> from pythainlp.util import syllable_length
        >>> syllable_length("มาก")
        'long'
        >>> syllable_length("คะ")
        'short'
    """
    consonants = [i for i in syllable if i in thai_consonants]
    if len(consonants) <= 3 and any((c in set(short)) for c in syllable):
        return "short"

    if bool(re_short.search(syllable)):
        return "short"

    return "long"


def _tone_mark_detector(syllable: str) -> str:
    tone_mark = [i for i in syllable if i in thai_tonemarks]
    if tone_mark == []:
        return ""

    return tone_mark[0]


def _check_sonorant_syllable(syllable: str) -> bool:
    _sonorant = [i for i in syllable if i in thai_low_sonorants]
    consonants = [i for i in syllable if i in thai_consonants]

    # Return False if no sonorants or not enough consonants
    if not _sonorant or len(consonants) < 2:
        return False

    if _sonorant[-1] == consonants[-2]:
        return True

    if _sonorant[-1] == consonants[-1]:
        return True

    return False


def tone_detector(syllable: str) -> str:
    """Thai tone detector for syllables

    Return tone of a syllable.

    - l: low
    - m: mid
    - r: rising
    - f: falling
    - h: high
    - empty string: cannot be detected

    :param str syllable: Thai syllable
    :return: syllable's tone (l, m, h, r, f) or empty if it cannot be detected
    :rtype: str

    :Example:

        >>> from pythainlp.util import tone_detector
        >>> tone_detector("มา")
        'm'
        >>> tone_detector("ไม้")
        'h'
    """
    s = sound_syllable(syllable)
    # get consonants
    consonants = [i for i in syllable if i in thai_consonants]

    # Handle syllables with no consonants (e.g., ฤ, ฦ)
    if len(consonants) == 0:
        return ""

    initial_consonant = consonants[0]
    tone_mark = _tone_mark_detector(syllable)
    syllable_check = syllable_open_close_detector(syllable)
    syllable_check_length = syllable_length(syllable)
    initial_consonant_type = thai_initial_consonant_to_type[initial_consonant]
    # r for store value
    r = ""
    # Special handling for อ and ห with sonorants
    if len(consonants) > 1 and (initial_consonant in ("อ", "ห")):
        consonant_ending = _check_sonorant_syllable(syllable)
        if consonant_ending:
            # Only apply special rules if there are sonorants
            if initial_consonant == "อ" and s == "live" and tone_mark == "่":
                r = "l"
            elif initial_consonant == "ห" and s == "live" and tone_mark == "่":
                r = "l"
            elif initial_consonant == "อ" and s == "dead":
                r = "l"
            elif initial_consonant == "ห" and s == "live" and tone_mark == "้":
                r = "f"
            elif initial_consonant == "ห" and s == "dead":
                r = "l"
            elif initial_consonant == "ห" and s == "live":
                r = "r"
    # If r is still empty, apply general tone rules
    if (
        r == ""
        and initial_consonant_type == "high"
        and s == "live"
        and tone_mark == "่"
    ):
        r = "l"
    if (
        r == ""
        and initial_consonant_type == "mid"
        and s == "live"
        and tone_mark == "่"
    ):
        r = "l"
    if r == "" and initial_consonant_type == "low" and tone_mark == "้":
        r = "h"
    if r == "" and initial_consonant_type == "mid" and tone_mark == "๋":
        r = "r"
    if r == "" and initial_consonant_type == "mid" and tone_mark == "๊":
        r = "h"
    if r == "" and initial_consonant_type == "low" and tone_mark == "่":
        r = "f"
    if r == "" and initial_consonant_type == "mid" and tone_mark == "้":
        r = "f"
    if r == "" and initial_consonant_type == "high" and tone_mark == "้":
        r = "f"
    if (
        r == ""
        and initial_consonant_type == "low"
        and syllable_check_length == "short"
        and syllable_check == "close"
        and s == "dead"
    ):
        r = "h"
    if (
        r == ""
        and initial_consonant_type == "low"
        and syllable_check_length == "long"
        and syllable_check == "close"
        and s == "dead"
    ):
        r = "f"
    if (
        r == ""
        and initial_consonant_type == "low"
        and syllable_check_length == "short"
        and syllable_check == "open"
    ):
        r = "h"
    if (
        r == ""
        and initial_consonant_type == "low"
        and syllable_check_length == "long"
        and syllable_check == "open"
        and s == "dead"
    ):
        r = "f"
    if r == "" and initial_consonant_type == "mid" and s == "dead":
        r = "l"
    if r == "" and initial_consonant_type == "high" and s == "dead":
        r = "l"
    if r == "" and initial_consonant_type == "low" and s == "live":
        r = "m"
    if r == "" and initial_consonant_type == "mid" and s == "live":
        r = "m"
    if r == "" and initial_consonant_type == "high" and s == "live":
        r = "r"

    return r
