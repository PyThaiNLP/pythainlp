# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Thai pronunciation transliteration from Wiktionary th-pron module.
Source code: https://en.wiktionary.org/wiki/Module:th-pron
"""

from __future__ import annotations

import re
import unicodedata
from typing import Optional, cast

from pythainlp import thai_digits, thai_tonemarks

_THAI_RANGE: str = r"[ก-๛̄]"

_SYSTEMS: dict[str, int] = {
    "paiboon": 0,
    "royin": 1,
    "ipa": 2,
}

_INITIAL: dict[str, dict[str, list[str] | str]] = {
    "ก": {"seq": ["g", "k", "k"], "class": "mid"},
    "จ": {"seq": ["j", "ch", "t͡ɕ"], "class": "mid"},
    "ด": {"seq": ["d", "d", "d"], "class": "mid"},
    "ฎ": {"seq": ["d", "d", "d"], "class": "mid"},
    "ฏ": {"seq": ["dt", "t", "t"], "class": "mid"},
    "ต": {"seq": ["dt", "t", "t"], "class": "mid"},
    "บ": {"seq": ["b", "b", "b"], "class": "mid"},
    "ป": {"seq": ["bp", "p", "p"], "class": "mid"},
    "อ": {"seq": ["", "@", "ʔ"], "class": "mid"},
    "ง": {"seq": ["ng", "$ng", "ŋ"], "class": "low"},
    "ณ": {"seq": ["n", "n", "n"], "class": "low"},
    "น": {"seq": ["n", "n", "n"], "class": "low"},
    "ม": {"seq": ["m", "m", "m"], "class": "low"},
    "ญ": {"seq": ["y", "y", "j"], "class": "low"},
    "ย": {"seq": ["y", "y", "j"], "class": "low"},
    "ร": {"seq": ["r", "r", "r"], "class": "low"},
    "ล": {"seq": ["l", "l", "l"], "class": "low"},
    "ฬ": {"seq": ["l", "l", "l"], "class": "low"},
    "ว": {"seq": ["w", "w", "w"], "class": "low"},
    "ค": {"seq": ["k", "kh", "kʰ"], "class": "low"},
    "ฅ": {"seq": ["k", "kh", "kʰ"], "class": "low"},
    "ฆ": {"seq": ["k", "kh", "kʰ"], "class": "low"},
    "ข": {"seq": ["k", "kh", "kʰ"], "class": "high"},
    "ฃ": {"seq": ["k", "kh", "kʰ"], "class": "high"},
    "ช": {"seq": ["ch", "ch", "t͡ɕʰ"], "class": "low"},
    "ฌ": {"seq": ["ch", "ch", "t͡ɕʰ"], "class": "low"},
    "ฉ": {"seq": ["ch", "ch", "t͡ɕʰ"], "class": "high"},
    "ฑ": {"seq": ["t", "th", "tʰ"], "class": "low"},
    "ฒ": {"seq": ["t", "th", "tʰ"], "class": "low"},
    "ท": {"seq": ["t", "th", "tʰ"], "class": "low"},
    "ธ": {"seq": ["t", "th", "tʰ"], "class": "low"},
    "ฐ": {"seq": ["t", "th", "tʰ"], "class": "high"},
    "ถ": {"seq": ["t", "th", "tʰ"], "class": "high"},
    "พ": {"seq": ["p", "ph", "pʰ"], "class": "low"},
    "ภ": {"seq": ["p", "ph", "pʰ"], "class": "low"},
    "ผ": {"seq": ["p", "ph", "pʰ"], "class": "high"},
    "ฟ": {"seq": ["f", "f", "f"], "class": "low"},
    "ฝ": {"seq": ["f", "f", "f"], "class": "high"},
    "ซ": {"seq": ["s", "s", "s"], "class": "low"},
    "ศ": {"seq": ["s", "s", "s"], "class": "high"},
    "ษ": {"seq": ["s", "s", "s"], "class": "high"},
    "ส": {"seq": ["s", "s", "s"], "class": "high"},
    "ฮ": {"seq": ["h", "h", "h"], "class": "low"},
    "ห": {"seq": ["h", "h", "h"], "class": "high"},
    "หง": {"seq": ["ng", "$ng", "ŋ"], "class": "high"},
    "หน": {"seq": ["n", "n", "n"], "class": "high"},
    "หม": {"seq": ["m", "m", "m"], "class": "high"},
    "หญ": {"seq": ["y", "y", "j"], "class": "high"},
    "หย": {"seq": ["y", "y", "j"], "class": "high"},
    "หร": {"seq": ["r", "r", "r"], "class": "high"},
    "หล": {"seq": ["l", "l", "l"], "class": "high"},
    "หว": {"seq": ["w", "w", "w"], "class": "high"},
    "…": {"seq": ["…", "…", "…"], "class": ""},
    "": {"seq": ["", "", ""], "class": ""},
}

_VOWEL: dict[str, dict[str, list[str]]] = {
    "open": {
        "ะ": ["a", "a", "a"],
        "": ["a", "a", "a"],
        "ิ": ["i", "i", "i"],
        "ึ": ["ʉ", "ue", "ɯ"],
        "ุ": ["u", "u", "u"],
        "เะ": ["e", "e", "eʔ"],
        "แะ": ["ɛ", "ae", "ɛʔ"],
        "โะ": ["o", "o", "oʔ"],
        "เาะ": ["ɔ", "o", "ɔʔ"],
        "็": ["ɔ", "o", "ɔ"],
        "เิ": ["ə", "oe", "ɤ"],
        "เอะ": ["ə", "oe", "ɤʔ"],
        "า": ["aa", "a", "aː"],
        "ี": ["ii", "i", "iː"],
        "ู": ["uu", "u", "uː"],
        "ือ": ["ʉʉ", "ue", "ɯː"],
        "เ": ["ee", "e", "eː"],
        "แ": ["ɛɛ", "ae", "ɛː"],
        "โ": ["oo", "o", "oː"],
        "อ": ["ɔɔ", "o", "ɔː"],
        "ร": ["ɔɔn", "on", "ɔːn"],
        "เอ": ["əə", "oe", "ɤː"],
        "เียะ": ["ia", "ia", "ia̯ʔ"],
        "เือะ": ["ʉa", "uea", "ɯa̯ʔ"],
        "ัวะ": ["ua", "ua", "ua̯ʔ"],
        "เีย": ["iia", "ia", "ia̯"],
        "เือ": ["ʉʉa", "uea", "ɯa̯"],
        "ัว": ["uua", "ua", "ua̯"],
        "ิว": ["iu", "io", "iw"],
        "ีว": ["iiu", "io", "iːw"],
        "เ็ว": ["eo", "eo", "ew"],
        "แ็ว": ["ɛo", "aeo", "ɛw"],
        "เา": ["ao", "ao", "aw"],
        "เว": ["eeo", "eo", "eːw"],
        "แว": ["ɛɛo", "aeo", "ɛːw"],
        "าว": ["aao", "ao", "aːw"],
        "เอว": ["əəo", "oeu", "ɤːw"],
        "โว": ["oow", "ou", "oːw"],
        "เียว": ["iao", "iao", "ia̯w"],
        "ัย": ["ai", "ai", "aj"],
        "ใ": ["ai", "ai", "aj"],
        "ไ": ["ai", "ai", "aj"],
        "ไย": ["ai", "ai", "aj"],
        "ึย": ["ʉi", "uei", "ɯj"],
        "็อย": ["ɔi", "oi", "ɔj"],
        "เิ็ย": ["əi", "oei", "ɤj"],
        "ุย": ["ui", "ui", "uj"],
        "าย": ["aai", "ai", "aːj"],
        "อย": ["ɔɔi", "oi", "ɔːj"],
        "โย": ["ooi", "oi", "oːj"],
        "เย": ["əəi", "oei", "ɤːj"],
        "ูย": ["uui", "ui", "uːj"],
        "วย": ["uai", "uai", "ua̯j"],
        "เือย": ["ʉai", "ueai", "ɯa̯j"],
        "ำ": ["am", "am", "am"],
    },
    "closed": {
        "ั": ["a", "a", "a"],
        "รร": ["a", "a", "a"],
        "ิ": ["i", "i", "i"],
        "ึ": ["ʉ", "ue", "ɯ"],
        "ุ": ["u", "u", "u"],
        "เ": ["ee", "e", "eː"],
        "เ็": ["e", "e", "e"],
        "แ็": ["ɛ", "ae", "ɛ"],
        "แ": ["ɛɛ", "ae", "ɛː"],
        "": ["o", "o", "o"],
        "็อ": ["ɔ", "o", "ɔ"],
        "เิ็": ["ə", "oe", "ɤ"],
        "า": ["aa", "a", "aː"],
        "ี": ["ii", "i", "iː"],
        "ื": ["ʉʉ", "ue", "ɯː"],
        "ู": ["uu", "u", "uː"],
        "โ": ["oo", "o", "oː"],
        "อ": ["ɔɔ", "o", "ɔː"],
        "เิ": ["əə", "oe", "ɤː"],
        "เอ": ["əə", "oe", "ɤː"],
        "เีย": ["iia", "ia", "ia̯"],
        "เือ": ["ʉʉa", "uea", "ɯa̯"],
        "ว": ["uua", "ua", "ua̯"],
        "ไ": ["ai", "ai", "aj"],
        "เา": ["ao", "ao", "aw"],
        "็อย": ["ɔi", "oi", "ɔj"],
    },
}

_UNROM_LONG: dict[str, bool] = {
    "เีย": True,
    "เือ": True,
    "ัว": True,
    "ว": True,
    "เือย": True,
    "วาย": True,
    "เอว": True,
    "เียว": True,
}

_LIVE_EXC: dict[str, bool] = {
    "ัย": True,
    "ใ": True,
    "ไ": True,
    "ไย": True,
    "ุย": True,
    "วย": True,
    "็อย": True,
    "เิ็ย": True,
    "เา": True,
    "ิว": True,
    "เ็ว": True,
    "แ็ว": True,
    "ำ": True,
}

_CODA: dict[str, list[str]] = {
    "ก": ["k", "k", "k̚"],
    "ข": ["k", "k", "k̚"],
    "ฃ": ["k", "k", "k̚"],
    "ค": ["k", "k", "k̚"],
    "ฅ": ["k", "k", "k̚"],
    "ฆ": ["k", "k", "k̚"],
    "จ": ["t", "t", "t̚"],
    "ฉ": ["t", "t", "t̚"],
    "ช": ["ch", "ch", "t͡ɕʰ"],
    "ซ": ["s", "s", "s"],
    "ฌ": ["t", "t", "t̚"],
    "ฎ": ["t", "t", "t̚"],
    "ฏ": ["t", "t", "t̚"],
    "ฐ": ["t", "t", "t̚"],
    "ฑ": ["t", "t", "t̚"],
    "ฒ": ["t", "t", "t̚"],
    "ด": ["t", "t", "t̚"],
    "ต": ["t", "t", "t̚"],
    "ถ": ["t", "t", "t̚"],
    "ท": ["t", "t", "t̚"],
    "ธ": ["t", "t", "t̚"],
    "ศ": ["t", "t", "t̚"],
    "ษ": ["t", "t", "t̚"],
    "ส": ["s", "s", "s"],
    "บ": ["p", "p", "p̚"],
    "ป": ["p", "p", "p̚"],
    "ผ": ["p", "p", "p̚"],
    "ฝ": ["p", "p", "p̚"],
    "พ": ["p", "p", "p̚"],
    "ฟ": ["f", "f", "f"],
    "ภ": ["p", "p", "p̚"],
    "ง": ["ng", "ng$", "ŋ"],
    "ญ": ["n", "n", "n"],
    "ณ": ["n", "n", "n"],
    "น": ["n", "n", "n"],
    "ร": ["n", "n", "n"],
    "ล": ["l", "l", "l"],
    "ฬ": ["n", "n", "n"],
    "ม": ["m", "m", "m"],
    "ฯ": ["ʔ", "ʔ", "ʔ"],
}

_TONE_FROM_MARK: dict[str, dict[str, str]] = {
    "่": {"high": "low", "mid": "low", "low": "falling"},
    "้": {"high": "falling", "mid": "falling", "low": "high"},
    "๊": {"high": "high", "mid": "high", "low": "high"},
    "๋": {"high": "rising", "mid": "rising", "low": "rising"},
    "̄": {"high": "mid", "mid": "mid", "low": "mid"},
}

_TONE_NO_MARK: dict[str, dict[str, str]] = {
    "dead-short": {"high": "low", "mid": "low", "low": "high"},
    "dead-long": {"high": "low", "mid": "low", "low": "falling"},
    "live": {"high": "rising", "mid": "mid", "low": "mid"},
}

_TONE_ROM_MARKS: dict[str, str] = {
    "high": "́",
    "mid": "",
    "low": "̀",
    "rising": "̌",
    "falling": "̂",
}

_TONE_LEVELS: dict[str, str] = {
    "high": "˦˥",
    "mid": "˧",
    "low": "˨˩",
    "rising": "˩˩˦",
    "falling": "˥˩",
}

_DIGIT_MAP: dict[str, str] = dict(zip(thai_digits, "0123456789"))
_RE_THAI_DIGIT: re.Pattern[str] = re.compile(f"[{thai_digits}]")

# Final consonant character class
_FINAL_C: str = "[คฅฆกขฃพฟภบปชฌฑฒทธจฎฏดตฐถศษสมญณนรลฬง]"

_MGVC_PATTERN = re.compile(rf"^([รลว]?)([ิึุ็ีืัำู]?[าอรยว]?[วยร]?ะ?)({_FINAL_C}?)$")
_FULL_PATTERN = re.compile(
    rf"^([เแโใไ]?)(หฺ[ก-รลว-ฮ])(ฺ?[รลว]?)([ิึุ็ีืัู]?็?[่้๊๋̄]?[าอรยวำ]?[วยร]?ะ?)({_FINAL_C}?{_FINAL_C}?)$"
)
_PARTIAL_PATTERN = re.compile(
    rf"^([เแโใไ]?)([ก-รลว-ฮ])(ฺ?[รลว]?)([ิึุ็ีืัู]?็?[่้๊๋̄]?[าอรยวำ]?[วยร]?ะ?)({_FINAL_C}?{_FINAL_C}?)$"
)


def _c2_decomp(c2_char: str, seq_idx: int) -> str:
    return "".join(_CODA.get(char, ["", "", ""])[seq_idx] for char in c2_char)


_TONE_MARK_CHARS: str = thai_tonemarks + "\u0304"
_RE_TONE_MARK: re.Pattern[str] = re.compile(f"[{_TONE_MARK_CHARS}]")
_RE_TWO_TONE_MARKS: re.Pattern[str] = re.compile(
    f"[{_TONE_MARK_CHARS}].?[{_TONE_MARK_CHARS}]"
)
_RE_HO_PAIR: re.Pattern[str] = re.compile(r"^ห.$")
_RE_DOUBLED_VOWEL: re.Pattern[str] = re.compile(r"([aiʉueɛoɔə])\1")
_RE_SONORANT: re.Pattern[str] = re.compile(r"[มญณนรลฬง]")
_FIRST_VOWEL_PATTERN: str = r"^([^aiʉueɛoɔə]*)([aiʉueɛoɔə])"
_RE_THAI_RUN: re.Pattern[str] = re.compile(f"{_THAI_RANGE}+")

# Cleanup steps for Royal Institute output, applied in order
_ROYIN_CLEANUPS: tuple[tuple[re.Pattern[str], str], ...] = tuple(
    (re.compile(pattern), repl)
    for pattern, repl in (
        (r"^@", ""),
        (r"([\s\W])@", r"\1"),
        (r"@", "-"),
        (r"^\$ng", "ng"),
        (r"([\s\W])\$ng", r"\1ng"),
        (r"([aeiou])\$ng", r"\1-ng"),
        (r"\$ng", "ng"),
        (r"ng\$([^\w\s])", r"ng\1"),
        (r"ng\$", "ng"),
    )
)


def _apply_ho_rule(
    c1: str, g: str, v2: str, c2: str
) -> tuple[str, str, str, str]:
    """Re-split a syllable that starts with HO HIP plus a consonant."""
    if _RE_HO_PAIR.match(c1):
        mgvc_match = _MGVC_PATTERN.match(c1[1] + g + v2 + c2)
        if mgvc_match:
            g_new, v2_new, c2_new = mgvc_match.groups()
            c1, g, v2, c2 = "ห", g_new, v2_new, c2_new
            if g and v2 != "ย":
                c1, g = c1 + g, ""
    return c1, g, v2, c2


def _lookup_vowel(
    v1: str, g: str, v2: str, openness: str, seq_idx: int
) -> tuple[str, str, str]:
    """Return the vowel output, the original vowel, and the glide output.

    The glide output is empty if the glide is part of the vowel.
    """
    vowels = _VOWEL[openness]
    if (v1 + g + v2) in vowels:
        return vowels[v1 + g + v2][seq_idx], v1 + g + v2, ""

    v_lookup = vowels.get(v1 + v2)
    v = v_lookup[seq_idx] if v_lookup else (v1 + v2)
    g_lookup = _INITIAL.get(g.replace("ฺ", ""), _INITIAL[""])
    return v, v1 + v2, cast("list[str]", g_lookup["seq"])[seq_idx]


def _vowel_length(v: str, orig_v: str) -> str:
    """Return "long" or "short" for a vowel."""
    if _RE_DOUBLED_VOWEL.search(v) or "ː" in v or orig_v in _UNROM_LONG:
        return "long"
    return "short"


def _syllable_life(c2: str, orig_v: str, v: str, length: str) -> str:
    """Return "live" or "dead" for a syllable."""
    if (
        _RE_SONORANT.search(c2)
        or (orig_v.endswith("ย") and v.endswith("i"))
        or (c2 == "" and length == "long")
        or _LIVE_EXC.get(orig_v)
    ):
        return "live"
    return "dead"


def _tone_name(
    tmark: Optional[str], life: str, length: str, cls: str
) -> Optional[str]:
    """Return the tone name from the tone mark, life, length, and class."""
    if tmark:
        tone_dict = _TONE_FROM_MARK.get(tmark)
    else:
        tone_dict = _TONE_NO_MARK.get(
            f"{life}-{length}", _TONE_NO_MARK.get(life)
        )
    return tone_dict.get(cls) if tone_dict else None


def _syllable(match: re.Match[str], seq_idx: int, mode: str) -> str:
    """Transliterate one syllable matched by a syllable pattern."""
    v1, c1, g, v2, c2 = match.groups()

    tmark_match = _RE_TONE_MARK.search(v2)
    tmark = tmark_match.group(0) if tmark_match else None
    v2 = _RE_TONE_MARK.sub("", v2)

    c1, g, v2, c2 = _apply_ho_rule(c1, g, v2, c2)

    if g == "ล" and not (v2 + c2):
        c2 = g
        g = ""

    openness = "closed" if c2 != "" else "open"
    v, orig_v, g = _lookup_vowel(v1, g, v2, openness, seq_idx)

    c1_clean = c1.replace("ฺ", "")
    if c1_clean not in _INITIAL:
        return match.group(0)
    ini = cast("list[str]", _INITIAL[c1_clean]["seq"])[seq_idx]
    cls = cast("str", _INITIAL[c1_clean]["class"])

    length = _vowel_length(v, orig_v)
    life = _syllable_life(c2, orig_v, v, length)

    if c2 in _CODA:
        c2 = _CODA[c2][seq_idx]
    else:
        c2 = _c2_decomp(c2, seq_idx)

    tone = _tone_name(tmark, life, length, cls)

    if mode == "paiboon":
        mark = _TONE_ROM_MARKS.get(tone, "") if tone else ""
        v = re.sub(_FIRST_VOWEL_PATTERN, f"\\g<1>\\g<2>{mark}", v)
    elif mode == "ipa":
        c2 = c2 + (_TONE_LEVELS.get(tone, "") if tone else "")

    return ini + g + v + c2


def _process_word(word: str, seq_idx: int, mode: str) -> str:
    """Transliterate a run of Thai characters."""
    if _RE_TWO_TONE_MARKS.search(word):
        return word

    def convert(match: re.Match[str]) -> str:
        return _syllable(match, seq_idx, mode)

    word = _FULL_PATTERN.sub(convert, word)
    return _PARTIAL_PATTERN.sub(convert, word)


def transliterate_wiktionary(text: str, mode: str = "ipa") -> str:
    """Transliterate Thai text using Wiktionary th-pron logic.

    :param str text: Thai text input (single word or text fragment).
    :param str mode: Output mode: ``paiboon``, ``royin``, or ``ipa``.
    Unsupported modes return the input text unchanged.

    :return: Transliterated text.
    :rtype: str

    :Example:

        >>> transliterate_wiktionary("แมว", mode="royin")
        'maeo'
    """
    seq_idx = _SYSTEMS.get(mode)
    if seq_idx is None:
        return text

    text = _RE_THAI_RUN.sub(
        lambda m: _process_word(m.group(0), seq_idx, mode), text
    )
    text = _RE_THAI_DIGIT.sub(lambda m: _DIGIT_MAP[m.group(0)], text)

    if mode == "royin":
        for pattern, repl in _ROYIN_CLEANUPS:
            text = pattern.sub(repl, text)

    if mode == "ipa":
        text = re.sub(r"[ \-–]", ".", text)
        text = re.sub(r"([aiɯu])([˥-˩]+)$", r"\1ʔ\2", text)

    return unicodedata.normalize("NFC", text)


def get_word_dict(word: str) -> dict[str, str]:
    """Return Wiktionary transliteration outputs in all supported systems.

    :param str word: Thai input word.
    :return: ``dict[str, str]`` with ``word``, ``paiboon``, ``royin``, and ``ipa``.
    :rtype: dict[str, str]

    :Example:

        >>> get_word_dict("แมว")
        {'word': 'แมว', 'paiboon': 'mɛɛo', 'royin': 'maeo', 'ipa': 'mɛːw˧'}
    """
    return {
        "word": word,
        "paiboon": transliterate_wiktionary(word, mode="paiboon"),
        "royin": transliterate_wiktionary(word, mode="royin"),
        "ipa": transliterate_wiktionary(word, mode="ipa"),
    }
