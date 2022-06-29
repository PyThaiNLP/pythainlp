# -*- coding: utf-8 -*-
"""
Syllable tools
"""
import re
from pythainlp import thai_consonants

spelling_class = {
    "กง": list("ง"),
    "กม": list("ม"),
    "เกย": list("ย"),
    "เกอว": list("ว"),
    "กน": list("นญณรลฬ"),
    "กก": list("กขคฆ"),
    "กด": list("ดจชซฎฏฐฑฒตถทธศษส"),
    "กบ": list("บปภพฟ")
}

thai_consonants_all = list(thai_consonants)
thai_consonants_all.remove("อ")

_temp = list(
    "".join(["".join(spelling_class[i]) for i in spelling_class.keys()])
)
not_spelling_class = [j for j in thai_consonants_all if j not in _temp]

short = "ะัิึุ"
re_short = re.compile("เ(.*)ะ|แ(.*)ะ|เ(.*)อะ|โ(.*)ะ|เ(.*)าะ", re.U)
pattern = re.compile("เ(.*)า", re.U)

_check_1 = spelling_class["กง"]+spelling_class["กน"]+spelling_class["กม"]+spelling_class["เกย"]+spelling_class["เกอว"]
_check_2 = spelling_class["กก"]+spelling_class["กบ"]+spelling_class["กด"]


def sound_syllable(syllable:str) -> str:
    consonants = [i for i in syllable if i in list(thai_consonants_all)]
    spelling_consonant = consonants[-1]
    if len(syllable) < 2:
        return "dead"
    elif (
        (
            spelling_consonant in _check_2)
            and
            (
                any((c in set("าีืแูาเโ")) for c in syllable) == False
                and any((c in set("ำใไ")) for c in syllable) == False
                and pattern.findall(syllable)!=True
            )
        ):
        return "dead"
    elif any((c in set("าีืแูาโ")) for c in syllable): # in syllable:
        if spelling_consonant != syllable[-1]:
            return "live"
        elif spelling_consonant in _check_1:
            return "live"
        elif spelling_consonant in _check_2:
            return "dead"
        elif (re_short.findall(syllable) or any((c in set(short)) for c in syllable)):
            return "dead"
        return "live"
    elif any((c in set("ำใไ")) for c in syllable):
        return "live"
    elif pattern.findall(syllable):
        return "live"
    elif spelling_consonant in _check_1:
        if (
            re_short.findall(syllable)
            or
            any((c in set(short)) for c in syllable)
        ) and len(consonants) < 2:
            return "dead"
        return "live"
    elif (
        re_short.findall(syllable)
        or
        any((c in set(short)) for c in syllable)
    ):
        return "dead"
    else:
        return "dead"
