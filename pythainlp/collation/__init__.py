# -*- coding: utf-8 -*-
"""
Thai collation (sort according to dictionary order)
For Unicode collation, please refer to Unicode Common Locale Data Repository (CLDR)
https://unicode.org/cldr/charts/latest/collation/th.html
"""
import re

RE_TONE = re.compile(r"[็-์]")
RE_LV_C = re.compile(r"([เ-ไ])([ก-ฮ])")

try:
    import icu

    thkey = icu.Collator.createInstance(icu.Locale("th_TH")).getSortKey
except ImportError:

    def thkey(word):
        cv = RE_TONE.sub("", word)  # remove tone
        cv = RE_LV_C.sub("\\2\\1", cv)  # switch lead vowel
        tone = RE_TONE.sub(" ", word)  # just tone
        return cv + tone


def collation(data):
    """
    :param list data: a list of thai text
    :return: a list of thai text, sorted alphabetically
    **Example**::
        >>> from pythainlp.collation import *
        >>> collation(['ไก่', 'เป็ด', 'หมู', 'วัว'])
        ['ไก่', 'เป็ด', 'วัว', 'หมู']
    """
    return sorted(data, key=thkey)


if __name__ == "__main__":
    a = collation(["ไก่", "ไข่", "ก", "ฮา"]) == ["ก", "ไก่", "ไข่", "ฮา"]
    print(a)
    print(collation(["หลาย", "หญิง"]) == ["หญิง", "หลาย"])
    print(collation(["ไก่", "เป็ด", "หมู", "วัว"]) == ["ไก่", "เป็ด", "วัว", "หมู"])
