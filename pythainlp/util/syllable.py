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

# vowel's short sound
short = "ะัิึุ"
re_short = re.compile("เ(.*)ะ|แ(.*)ะ|เ(.*)อะ|โ(.*)ะ|เ(.*)าะ", re.U)
pattern = re.compile("เ(.*)า", re.U)  # เ-า is live syllable

_check_1 = []
# these spelling consonant are live syllable.
for i in ["กง", "กน", "กม", "เกย", "เกอว"]:
    _check_1.extend(spelling_class[i])
# these spelling consonant are dead syllable.
_check_2 = spelling_class["กก"]+spelling_class["กบ"]+spelling_class["กด"]


def sound_syllable(syllable: str) -> str:
    """
    Sound syllable classification

    This function is sound syllable classification.
    It is live syllable or dead syllable.

    :param str syllable: Thai syllable
    :return: syllable's type (live or dead)
    :rtype: str

    :Example:
    ::

        from pythainlp.util import sound_syllable

        print(sound_syllable("มา"))
        # output: live

        print(sound_syllable("เลข"))
        # output: dead
    """
    # get consonants
    consonants = [i for i in syllable if i in list(thai_consonants_all)]
    # get spelling consonants
    spelling_consonant = consonants[-1]
    # if len of syllable < 2
    if len(syllable) < 2:
        return "dead"
    elif (
        (
            spelling_consonant in _check_2)
            and
            (
                any((c in set("าีืแูาเโ")) for c in syllable) == False
                and any((c in set("ำใไ")) for c in syllable) == False
                and pattern.findall(syllable) != True
            )
    ):
        return "dead"
    elif any((c in set("าีืแูาโ")) for c in syllable):  # in syllable:
        if spelling_consonant != syllable[-1]:
            return "live"
        elif spelling_consonant in _check_1:
            return "live"
        elif spelling_consonant in _check_2:
            return "dead"
        elif (
            re_short.findall(syllable)
            or
            any((c in set(short)) for c in syllable)
        ):
            return "dead"
        return "live"
    elif any((c in set("ำใไ")) for c in syllable):
        return "live"  # if these vowel's long sound are live syllable
    elif pattern.findall(syllable):  # if it is เ-า
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
        re_short.findall(syllable)  # if found vowel's short sound
        or
        any((c in set(short)) for c in syllable)  # consonant in short
    ):
        return "dead"
    else:
        return "dead"
