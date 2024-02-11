# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
import re
from typing import List
from pythainlp import (
    thai_above_vowels,
    thai_below_vowels,
    thai_consonants,
    thai_follow_vowels,
    thai_lead_vowels,
    thai_letters,
    thai_tonemarks,
)
from pythainlp.tokenize import subword_tokenize, Tokenizer


_r1 = ["เ-ย", "เ-ะ", "แ-ะ", "โ-ะ", "เ-าะ", "เ-อะ", "เ-อ", "เ-า"]
_r2 = ["–ั:วะ", "เ–ี:ยะ", "เ–ือะ", "–ั:ว", "เ–ี:ย", "เ–ื:อ", "–ื:อ"]
tonemarks = {
    i: "ไม้" + j
    for i, j in zip(list(thai_tonemarks), ["เอก", "โท", "ตรี", "จัตวา"])
}

rule1 = [i.replace("-", f"([{thai_letters}](thai_tonemarks)?)") for i in _r1]
rule2 = [i.replace("–", f"([{thai_letters}])").replace(":", "") for i in _r2]
rule3 = [
    i.replace("–", f"([{thai_letters}])").replace(":", f"([{thai_tonemarks}])")
    for i in _r2
]
dict_vowel_ex = {}
for i in _r1 + _r2:
    dict_vowel_ex[i.replace("-", "อ").replace("–", "อ").replace(":", "")] = (
        i.replace("-", "อ").replace(":", "").replace("–", "อ")
    )
dict_vowel = {}
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

_cut = Tokenizer(list(dict_vowel.keys()) + list(thai_consonants), engine="mm")


def _clean(w):
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


def spell_syllable(text: str) -> List[str]:
    """
    Spell out syllables in Thai word distribution form.

    :param str s: Thai syllables only
    :return: List of spelled out syllables
    :rtype: List[str]

    :Example:
    ::

        from pythainlp.util.spell_words import spell_syllable

        print(spell_syllable("แมว"))
        # output: ['มอ', 'วอ', 'แอ', 'แมว']
    """
    tokens = _cut.word_tokenize(_clean(text))

    c_only = [tok + "อ" for tok in tokens if tok in set(thai_consonants)]
    v_only = [dict_vowel[tok] for tok in tokens if tok in set(dict_vowel)]
    t_only = [tonemarks[tok] for tok in tokens if tok in set(tonemarks.keys())]

    return c_only + v_only + t_only + [text]


def spell_word(text: str) -> List[str]:
    """
    Spell out words in Thai word distribution form.

    :param str w: Thai words only
    :return: List of spelled out words
    :rtype: List[str]

    :Example:
    ::

        from pythainlp.util.spell_words import spell_word

        print(spell_word("คนดี"))
        # output: ['คอ', 'นอ', 'คน', 'ดอ', 'อี', 'ดี', 'คนดี']
    """
    spellouts = []
    tokens = subword_tokenize(text, engine="han_solo")

    for tok in tokens:
        spellouts.extend(spell_syllable(tok))

    if len(tokens) > 1:
        spellouts.append(text)

    return spellouts
