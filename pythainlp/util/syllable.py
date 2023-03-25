# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Syllable tools
"""
import re
from pythainlp import thai_consonants, thai_tonemarks

spelling_class = {
    "กง": list("ง"),
    "กม": list("ม"),
    "เกย": list("ย"),
    "เกอว": list("ว"),
    "กน": list("นญณรลฬ"),
    "กก": list("กขคฆ"),
    "กด": list("ดจชซฎฏฐฑฒตถทธศษส"),
    "กบ": list("บปภพฟ"),
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
_check_2 = spelling_class["กก"] + spelling_class["กบ"] + spelling_class["กด"]

thai_low_sonorants = list("งนมยรลว")
thai_low_aspirates = list("คชซทพฟฮ")
thai_low_irregular = list("ฆญณธภฅฌฑฒฬ")

thai_mid_plains = list("กจดตบปอฎฏ")

thai_high_aspirates = list("ขฉถผฝสห")
thai_high_irregular = list("ศษฃฐ")
thai_initial_consonant_type = {
    "low": thai_low_sonorants + thai_low_aspirates + thai_low_irregular,
    "mid": thai_mid_plains,
    "high": thai_high_aspirates + thai_high_irregular,
}
thai_initial_consonant_to_type = {}
for k, v in thai_initial_consonant_type.items():
    for i in v:
        thai_initial_consonant_to_type[i] = k


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
    elif (spelling_consonant in _check_2) and (
        any((c in set("าีืแูาเโ")) for c in syllable) == False
        and any((c in set("ำใไ")) for c in syllable) == False
        and bool(pattern.search(syllable)) != True
    ):
        return "dead"
    elif any((c in set("าีืแูาโ")) for c in syllable):  # in syllable:
        if (
            spelling_consonant in _check_1
            and bool(re_short.search(syllable)) != True
        ):
            return "live"
        elif (
            spelling_consonant != syllable[-1]
            and bool(re_short.search(syllable)) != True
        ):
            return "live"
        elif spelling_consonant in _check_2:
            return "dead"
        elif bool(re_short.search(syllable)) or any(
            (c in set(short)) for c in syllable
        ):
            return "dead"
        return "live"
    elif any((c in set("ำใไ")) for c in syllable):
        return "live"  # if these vowel's long sound are live syllable
    elif bool(pattern.search(syllable)):  # if it is เ-า
        return "live"
    elif spelling_consonant in _check_1:
        if (
            bool(re_short.search(syllable))
            or any((c in set(short)) for c in syllable)
        ) and len(consonants) < 2:
            return "dead"
        return "live"
    elif bool(
        re_short.search(syllable)
    ) or any(  # if found vowel's short sound
        (c in set(short)) for c in syllable
    ):  # consonant in short
        return "dead"
    else:
        return "dead"


def syllable_open_close_detector(syllable: str) -> str:
    """
    Thai syllable open/close detector

    This function is use for find Thai syllable that open or closed sound.

    :param str syllable: Thai syllable
    :return: open / close
    :rtype: str

    :Example:
    ::

        from pythainlp.util import syllable_open_close_detector

        print(syllable_open_close_detector("มาก"))
        # output: close

        print(syllable_open_close_detector("คะ"))
        # output: open
    """
    consonants = [i for i in syllable if i in list(thai_consonants)]
    if len(consonants) < 2:
        return "open"
    elif len(consonants) == 2 and consonants[-1] == "อ":
        return "open"
    return "close"


def syllable_length(syllable: str) -> str:
    """
    Thai syllable length

    This function is use for find syllable's length. (long or short)

    :param str syllable: Thai syllable
    :return: syllable's length (long or short)
    :rtype: str

    :Example:
    ::

        from pythainlp.util import syllable_length

        print(syllable_length("มาก"))
        # output: long

        print(syllable_length("คะ"))
        # output: short
    """
    consonants = [i for i in syllable if i in list(thai_consonants)]
    if len(consonants) < 3 and any((c in set(short)) for c in syllable):
        return "short"
    elif bool(re_short.search(syllable)):
        return "short"
    else:
        return "long"


def _tone_mark_detector(syllable: str) -> str:
    tone_mark = [i for i in syllable if i in list(thai_tonemarks)]
    if tone_mark == []:
        return ""
    else:
        return tone_mark[0]


def _check_sonorant_syllable(syllable: str) -> bool:
    _sonorant = [i for i in syllable if i in thai_low_sonorants]
    consonants = [i for i in syllable if i in list(thai_consonants)]
    if _sonorant[-1] == consonants[-2]:
        return True
    elif _sonorant[-1] == consonants[-1]:
        return True
    return False


def tone_detector(syllable: str) -> str:
    """
    Thai tone detector for syllables

    :param str syllable: Thai syllable
    :return: syllable's tone (l, m, h, r, f or empty if it cannot detector)
    :rtype: str

    :Example:
    ::

        from pythainlp.util import tone_detector

        print(tone_detector("มา"))
        # output: m

        print(tone_detector("ไม้"))
        # output: h
    """
    s = sound_syllable(syllable)
    # get consonants
    consonants = [i for i in syllable if i in list(thai_consonants)]
    initial_consonant = consonants[0]
    tone_mark = _tone_mark_detector(syllable)
    syllable_check = syllable_open_close_detector(syllable)
    syllable_check_lenght = syllable_length(syllable)
    initial_consonant_type = thai_initial_consonant_to_type[initial_consonant]
    # r for store value
    r = ""
    if len(consonants) > 1 and (
        initial_consonant == "อ" or initial_consonant == "ห"
    ):
        consonant_ending = _check_sonorant_syllable(syllable)
        if (
            initial_consonant == "อ"
            and consonant_ending
            and s == "live"
            and tone_mark == "่"
        ):
            r = "l"
        elif initial_consonant == "อ" and consonant_ending and s == "dead":
            r = "l"
        elif (
            initial_consonant == "ห"
            and consonant_ending
            and s == "live"
            and tone_mark == "่"
        ):
            r = "l"
        elif (
            initial_consonant == "ห"
            and consonant_ending
            and s == "live"
            and tone_mark == "้"
        ):
            r = "f"
        elif initial_consonant == "ห" and consonant_ending and s == "dead":
            r = "l"
        elif initial_consonant == "ห" and consonant_ending and s == "live":
            r = "r"
    elif (
        initial_consonant_type == "low"
        and syllable_check_lenght == "short"
        and syllable_check == "close"
        and s == "dead"
    ):
        r = "h"
    elif (
        initial_consonant_type == "low"
        and syllable_check_lenght == "long"
        and syllable_check == "close"
        and s == "dead"
    ):
        r = "f"
    elif (
        initial_consonant_type == "low"
        and syllable_check_lenght == "short"
        and syllable_check == "open"
    ):
        r = "h"
    elif initial_consonant_type == "high" and s == "live" and tone_mark == "่":
        r = "l"
    elif initial_consonant_type == "mid" and s == "live" and tone_mark == "่":
        r = "l"
    elif initial_consonant_type == "low" and tone_mark == "้":
        r = "h"
    elif initial_consonant_type == "mid" and tone_mark == "๋":
        r = "r"
    elif initial_consonant_type == "mid" and tone_mark == "๊":
        r = "h"
    elif initial_consonant_type == "low" and tone_mark == "่":
        r = "f"
    elif initial_consonant_type == "mid" and tone_mark == "้":
        r = "f"
    elif initial_consonant_type == "high" and tone_mark == "้":
        r = "f"
    elif initial_consonant_type == "mid" and s == "dead":
        r = "l"
    elif initial_consonant_type == "high" and s == "dead":
        r = "l"
    elif initial_consonant_type == "low" and s == "live":
        r = "m"
    elif initial_consonant_type == "mid" and s == "live":
        r = "m"
    elif initial_consonant_type == "high" and s == "live":
        r = "r"
    return r
