# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Syllable tools."""

from __future__ import annotations

import itertools
import re
from typing import Optional, Pattern

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
    "เ(.*)ะ|แ(.*)ะ|เ(.*)อะ|โ(.*)ะ|เ(.*)าะ", re.UNICODE
)
pattern: Pattern[str] = re.compile(
    "เ(.*)า", re.UNICODE
)  # เ-า is live syllable

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


_SHORT_SET: frozenset[str] = frozenset(short)
_VOWELS_ANY_1: frozenset[str] = frozenset("าีืแูเโไใำ")
_VOWELS_ANY_2: frozenset[str] = frozenset("าีืแูาเโ")
_VOWELS_ANY_3: frozenset[str] = frozenset("าีืแูาโ")
_VOWELS_ANY_4: frozenset[str] = frozenset("ำใไ")


def _has_any(syllable: str, chars: frozenset[str]) -> bool:
    """Check whether the syllable has any of the given characters."""
    return not chars.isdisjoint(syllable)


def _has_short_sound(syllable: str) -> bool:
    """Check whether the syllable has a short vowel sound."""
    return bool(re_short.search(syllable)) or _has_any(syllable, _SHORT_SET)


def _sound_vowel_only(syllable: str) -> str:
    """Classify a syllable with อ but no other consonant."""
    if _has_any(syllable, _VOWELS_ANY_1):
        return "live"
    if _has_any(syllable, _SHORT_SET):
        return "dead"
    return "live"


def _sound_with_long_vowel(syllable: str, spelling_consonant: str) -> str:
    """Classify a syllable with า, ี, ื, แ, ู, or โ."""
    has_re_short = bool(re_short.search(syllable))
    if not has_re_short and (
        spelling_consonant in _check_1 or spelling_consonant != syllable[-1]
    ):
        return "live"
    if spelling_consonant in _check_2:
        return "dead"
    if _has_short_sound(syllable):
        return "dead"
    return "live"


def _sound_live_final(syllable: str, consonant_count: int) -> str:
    """Classify a syllable whose final consonant is a live final."""
    if _has_short_sound(syllable) and consonant_count < 2:
        return "dead"
    if syllable[-1] in _SHORT_SET:
        return "dead"
    return "live"


def sound_syllable(syllable: str) -> str:
    """
    Classify the sound of a Thai syllable as live or dead.

    :param str syllable: Thai syllable
    :return: type of the syllable ("live" or "dead")
    :rtype: str

    :Example:

        >>> from pythainlp.util import sound_syllable
        >>> sound_syllable("มา")
        'live'
        >>> sound_syllable("เลข")
        'dead'
        >>> sound_syllable("ฤๅ")
        'live'
    """
    if len(syllable) < 2:
        return "dead"

    consonants = [i for i in syllable if i in thai_consonants_all]
    if len(consonants) == 0 and "อ" in syllable:
        return _sound_vowel_only(syllable)

    if not consonants:
        return "dead" if _has_short_sound(syllable) else "live"

    spelling_consonant = consonants[-1]
    if (
        spelling_consonant in _check_2
        and not _has_any(syllable, _VOWELS_ANY_2)
        and not _has_any(syllable, _VOWELS_ANY_4)
        and not pattern.search(syllable)
    ):
        return "dead"

    if _has_any(syllable, _VOWELS_ANY_3):
        return _sound_with_long_vowel(syllable, spelling_consonant)

    # ำ, ใ, ไ and เ-า are live
    if _has_any(syllable, _VOWELS_ANY_4) or pattern.search(syllable):
        return "live"

    if spelling_consonant in _check_1:
        return _sound_live_final(syllable, len(consonants))

    return "dead"


def syllable_open_close_detector(syllable: str) -> str:
    """
    Detect whether a Thai syllable is open or closed.

    :param str syllable: Thai syllable
    :return: "open" or "close"
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
    """
    Detect the vowel length of a Thai syllable.

    :param str syllable: Thai syllable
    :return: length of the syllable ("long" or "short")
    :rtype: str

    :Example:

        >>> from pythainlp.util import syllable_length
        >>> syllable_length("มาก")
        'long'
        >>> syllable_length("คะ")
        'short'
    """
    consonants = [i for i in syllable if i in thai_consonants]
    if len(consonants) <= 3 and _has_any(syllable, _SHORT_SET):
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

    return _sonorant[-1] == consonants[-1]


def _tone_ah_sonorant(initial: str, sound: str, tone_mark: str) -> str:
    """Tone rules for อ or ห followed by a sonorant ending."""
    if sound == "live":
        if tone_mark == "่":
            return "l" if initial in ("อ", "ห") else ""
        if initial == "ห":
            return "f" if tone_mark == "้" else "r"
        return ""
    return "l"


# Ordered rules: (initial type, tone mark, sound, length, open/close, tone).
# None matches any value. The first matching rule wins.
_TONE_RULES: tuple[
    tuple[
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        str,
    ],
    ...,
] = (
    ("high", "่", "live", None, None, "l"),
    ("mid", "่", "live", None, None, "l"),
    ("low", "้", None, None, None, "h"),
    ("mid", "๋", None, None, None, "r"),
    ("mid", "๊", None, None, None, "h"),
    ("low", "่", None, None, None, "f"),
    ("mid", "้", None, None, None, "f"),
    ("high", "้", None, None, None, "f"),
    ("low", None, "dead", "short", "close", "h"),
    ("low", None, "dead", "long", "close", "f"),
    ("low", None, None, "short", "open", "h"),
    ("low", None, "dead", "long", "open", "f"),
    ("mid", None, "dead", None, None, "l"),
    ("high", None, "dead", None, None, "l"),
    ("low", None, "live", None, None, "m"),
    ("mid", None, "live", None, None, "m"),
    ("high", None, "live", None, None, "r"),
)


def _match_tone_rule(actual: tuple[str, ...]) -> str:
    """Return the tone of the first rule that matches; "" if none does."""
    for rule in _TONE_RULES:
        if all(c is None or c == a for c, a in zip(rule, actual)):
            return rule[-1]
    return ""


def _build_tone_table() -> dict[tuple[str, ...], str]:
    """Expand ``_TONE_RULES`` into a table for every possible input."""
    table: dict[tuple[str, ...], str] = {}
    for key in itertools.product(
        thai_initial_consonant_type,
        ("", *thai_tonemarks),
        ("live", "dead"),
        ("short", "long"),
        ("open", "close"),
    ):
        table[key] = _match_tone_rule(key)
    return table


_TONE_TABLE: dict[tuple[str, ...], str] = _build_tone_table()


def tone_detector(syllable: str) -> str:
    """
    Detect the tone of a Thai syllable.

    The tone is one of:

    - l: low
    - m: mid
    - r: rising
    - f: falling
    - h: high
    - empty string: cannot be detected

    :param str syllable: Thai syllable
    :return: tone of the syllable (l, m, h, r, f),
        or an empty string if it cannot be detected
    :rtype: str

    :Example:

        >>> from pythainlp.util import tone_detector
        >>> tone_detector("มา")
        'm'
        >>> tone_detector("ไม้")
        'h'
    """
    sound = sound_syllable(syllable)
    consonants = [i for i in syllable if i in thai_consonants]

    # Syllables with no consonants (e.g., ฤ, ฦ)
    if len(consonants) == 0:
        return ""

    initial_consonant = consonants[0]
    tone_mark = _tone_mark_detector(syllable)

    # Special handling for อ and ห with sonorants
    if (
        len(consonants) > 1
        and initial_consonant in ("อ", "ห")
        and _check_sonorant_syllable(syllable)
    ):
        result = _tone_ah_sonorant(initial_consonant, sound, tone_mark)
        if result:
            return result

    initial_type = thai_initial_consonant_to_type[initial_consonant]
    length = syllable_length(syllable)
    open_close = syllable_open_close_detector(syllable)
    actual = (initial_type, tone_mark, sound, length, open_close)
    return _TONE_TABLE.get(actual, "")
