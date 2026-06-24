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
from typing import cast

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

_SYMBOLS: dict[str, str] = {
    "๐": "0",
    "๑": "1",
    "๒": "2",
    "๓": "3",
    "๔": "4",
    "๕": "5",
    "๖": "6",
    "๗": "7",
    "๘": "8",
    "๙": "9",
}

_MGVC_PATTERN = re.compile(
    r"^([รลว]?)([ิึุ็ีืัำู]?[าอรยว]?[วยร]?ะ?)([คฅฆกขฃพฟภบปชฌฑฒทธจฎฏดตฐถศษสมญณนรลฬง]?)$"
)
_FULL_PATTERN = re.compile(
    r"^([เแโใไ]?)(หฺ[ก-รลว-ฮ])(ฺ?[รลว]?)([ิึุ็ีืัู]?็?[่้๊๋̄]?[าอรยวำ]?[วยร]?ะ?)([คฅฆกขฃพฟภบปชฌฑฒทธจฎฏดตฐถศษสมญณนรลฬง]?[คฅฆกขฃพฟภบปชฌฑฒทธจฎฏดตฐถศษสมญณนรลฬง]?)$"
)
_PARTIAL_PATTERN = re.compile(
    r"^([เแโใไ]?)([ก-รลว-ฮ])(ฺ?[รลว]?)([ิึุ็ีืัู]?็?[่้๊๋̄]?[าอรยวำ]?[วยร]?ะ?)([คฅฆกขฃพฟภบปชฌฑฒทธจฎฏดตฐถศษสมญณนรลฬง]?[คฅฆกขฃพฟภบปชฌฑฒทธจฎฏดตฐถศษสมญณนรลฬง]?)$"
)


def _c2_decomp(c2_char: str, seq_idx: int) -> str:
    return "".join(_CODA.get(char, ["", "", ""])[seq_idx] for char in c2_char)


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

    def process_word(match_word: re.Match[str]) -> str:
        word = match_word.group(0)

        if re.search(r"[่้๊๋̄].?[่้๊๋̄]", word):
            return word

        def syllable(match: re.Match[str]) -> str:
            v1, c1, g, v2, c2 = match.groups()

            tmark_match = re.search(r"[่้๊๋̄]", v2)
            tmark = tmark_match.group(0) if tmark_match else None
            v2 = re.sub(r"[่้๊๋̄]", "", v2)

            if re.match(r"^ห.$", c1):
                mgvc_match = _MGVC_PATTERN.match(c1[1] + g + v2 + c2)
                if mgvc_match:
                    g_new, v2_new, c2_new = mgvc_match.groups()
                    c1, g, v2, c2 = "ห", g_new, v2_new, c2_new
                    if g and v2 != "ย":
                        c1, g = c1 + g, ""

            if g == "ล" and not (v2 + c2):
                c2 = g
                g = ""

            openness = "closed" if c2 != "" else "open"

            if (v1 + g + v2) in _VOWEL[openness]:
                orig_v = v1 + g + v2
                v = _VOWEL[openness][orig_v][seq_idx]
                g = ""
            else:
                orig_v = v1 + v2
                v_lookup = _VOWEL[openness].get(v1 + v2)
                v = v_lookup[seq_idx] if v_lookup else (v1 + v2)
                g_clean = g.replace("ฺ", "")
                g_lookup = _INITIAL.get(g_clean, _INITIAL[""])
                g = cast(list[str], g_lookup["seq"])[seq_idx]

            c1_clean = c1.replace("ฺ", "")
            if c1_clean in _INITIAL:
                ini = cast(list[str], _INITIAL[c1_clean]["seq"])[seq_idx]
                cls = cast(str, _INITIAL[c1_clean]["class"])
            else:
                return match.group(0)

            length = (
                "long"
                if re.search(r"([aiʉueɛoɔə])\1", v)
                or "ː" in v
                or orig_v in _UNROM_LONG
                else "short"
            )
            life = (
                "live"
                if re.search(r"[มญณนรลฬง]", c2)
                or (orig_v.endswith("ย") and v.endswith("i"))
                or (c2 == "" and length == "long")
                or _LIVE_EXC.get(orig_v)
                else "dead"
            )

            if c2 in _CODA:
                c2 = _CODA[c2][seq_idx]
            else:
                c2 = _c2_decomp(c2, seq_idx)

            tone_dict = (
                _TONE_FROM_MARK.get(tmark)
                if tmark
                else _TONE_NO_MARK.get(f"{life}-{length}", _TONE_NO_MARK.get(life))
            )
            tone = tone_dict.get(cls) if tone_dict else None

            if mode == "paiboon":
                v = re.sub(
                    r"^([^aiʉueɛoɔə]*)([aiʉueɛoɔə])",
                    f"\\g<1>\\g<2>{_TONE_ROM_MARKS.get(tone, '')}",
                    v,
                )
            elif mode == "ipa":
                c2 = c2 + _TONE_LEVELS.get(tone, "")

            return ini + g + v + c2

        word = _FULL_PATTERN.sub(syllable, word)
        word = _PARTIAL_PATTERN.sub(syllable, word)
        return word

    text = re.sub(f"{_THAI_RANGE}+", lambda m: process_word(m), text)

    text = re.sub(r"[๐-๙]", lambda m: _SYMBOLS.get(m.group(0), m.group(0)), text)

    if mode == "royin":
        text = re.sub(r"^@", "", text)
        text = re.sub(r"([\s\W])@", r"\1", text)
        text = text.replace("@", "-")
        text = re.sub(r"^\$ng", "ng", text)
        text = re.sub(r"([\s\W])\$ng", r"\1ng", text)
        text = re.sub(r"([aeiou])\$ng", r"\1-ng", text)
        text = text.replace("$ng", "ng")
        text = re.sub(r"ng\$([^\w\s])", r"ng\1", text)
        text = re.sub(r"ng\$", "ng", text)

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
