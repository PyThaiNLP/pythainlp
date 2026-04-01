# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import re
from functools import lru_cache
from typing import Optional

from pythainlp import (
    thai_above_vowels,
    thai_below_vowels,
    thai_consonants,
    thai_follow_vowels,
    thai_lead_vowels,
    thai_letters,
    thai_tonemarks,
)
from pythainlp.tokenize import Tokenizer, subword_tokenize

_r1: list[str] = ["เ-ย", "เ-ะ", "แ-ะ", "โ-ะ", "เ-าะ", "เ-อะ", "เ-อ", "เ-า"]
_r2: list[str] = ["–ั:วะ", "เ–ี:ยะ", "เ–ือะ", "–ั:ว", "เ–ี:ย", "เ–ื:อ", "–ื:อ"]
tonemarks: dict[str, str] = {
    i: "ไม้" + j
    for i, j in zip(list(thai_tonemarks), ["เอก", "โท", "ตรี", "จัตวา"])
}

rule1: list[str] = [
    i.replace("-", f"([{thai_letters}](thai_tonemarks)?)") for i in _r1
]
rule2: list[str] = [
    i.replace("–", f"([{thai_letters}])").replace(":", "") for i in _r2
]
rule3: list[str] = [
    i.replace("–", f"([{thai_letters}])").replace(":", f"([{thai_tonemarks}])")
    for i in _r2
]
dict_vowel_ex: dict[str, str] = {}
i: str
for i in _r1 + _r2:
    dict_vowel_ex[i.replace("-", "อ").replace("–", "อ").replace(":", "")] = (
        i.replace("-", "อ").replace(":", "").replace("–", "อ")
    )
dict_vowel: dict[str, str] = {}
for i in _r1 + _r2:
    dict_vowel[i.replace("-", "อ").replace("–", "อ").replace(":", "")] = (
        i.replace("-", "อ").replace(":", "").replace("–", "อ")
    )
for i in thai_lead_vowels:
    dict_vowel[i] = i + "อ"
for i in thai_follow_vowels:
    dict_vowel[i] = "อ" + i
for i in thai_above_vowels:
    dict_vowel[i] = "อ" + i
for i in thai_below_vowels:
    dict_vowel[i] = "อ" + i


@lru_cache
def _cut() -> Tokenizer:
    """Lazy load vowel tokenizer with cache"""
    return Tokenizer(
        list(dict_vowel.keys()) + list(thai_consonants), engine="mm"
    )


def _clean(w: str) -> str:
    if bool(re.match("|".join(rule3), w)):
        for r in rule3:
            if bool(re.match(r, w)):
                w = re.sub(r, "\\1==\\2==", w)
                temp = w.split("==")
                w = (
                    temp[0]
                    + r.replace(f"([{thai_letters}])", "อ").replace(
                        f"([{thai_tonemarks}])", ""
                    )
                    + temp[1]
                )
    elif bool(re.match("|".join(rule2), w)):
        for r in rule2:
            if bool(re.match(r, w)):
                w = re.sub(r, "\\1", w) + r.replace(f"([{thai_letters}])", "อ")
    elif bool(re.match("|".join(rule1), w)):
        for r in rule1:
            if bool(re.match(r, w)):
                w = re.sub(r, "\\1", w) + r.replace(
                    f"([{thai_letters}](thai_tonemarks)?)", "อ"
                )
    return w


def spell_syllable(text: str) -> list[str]:
    """Spell out syllables in Thai word distribution form.

    :param str text: Thai syllables only
    :return: list of spelled-out syllable components
    :rtype: list[str]

    :Example:

        >>> from pythainlp.util.spell_words import spell_syllable
        >>> spell_syllable("แมว")
        ['มอ', 'วอ', 'แอ', 'แมว']
    """
    tokens = _cut().word_tokenize(_clean(text))

    c_only = [tok + "อ" for tok in tokens if tok in set(thai_consonants)]
    v_only = [dict_vowel[tok] for tok in tokens if tok in set(dict_vowel)]
    t_only = [tonemarks[tok] for tok in tokens if tok in set(tonemarks.keys())]

    return c_only + v_only + t_only + [text]


def spell_word(text: Optional[str]) -> list[str]:
    """Spell out words in Thai word distribution form.

    :param Optional[str] text: Thai words only, or None
    :return: List of spelled out words, empty list if text is None or empty
    :rtype: list[str]

    :Example:

        >>> from pythainlp.util.spell_words import spell_word
        >>> spell_word("คนดี")
        ['คอ', 'นอ', 'คน', 'ดอ', 'อี', 'ดี', 'คนดี']
        >>> spell_word(None)
        []
    """
    if not text:
        return []

    spellouts = []
    tokens = subword_tokenize(text, engine="han_solo")

    for tok in tokens:
        spellouts.extend(spell_syllable(tok))

    if len(tokens) > 1:
        spellouts.append(text)

    return spellouts
