# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
from pythainlp import thai_consonants


def nighit(w1: str, w2: str) -> str:
    """
    Nighit (นิคหิต or  ํ ) is the niggahita in Thai language for create new \
    words from Pali language in Thai.
    The function use simple method to create new Thai word from two words \
    that the root is from Pali language.

    Read more: https://www.trueplookpanya.com/learning/detail/1180

    :param str w1: A Thai word that has a nighit.
    :param str w2: A Thai word.
    :return: Thai word.
    :rtype: str
    :Example:

    ::

        from pythainlp.morpheme import nighit

        assert nighit("สํ","คีต")=="สังคีต"
        assert nighit("สํ","จร")=="สัญจร"
        assert nighit("สํ","ฐาน")=="สัณฐาน"
        assert nighit("สํ","นิษฐาน")=="สันนิษฐาน"
        assert nighit("สํ","ปทา")=="สัมปทา"
        assert nighit("สํ","โยค")=="สังโยค"
    """
    if not str(w1).endswith('ํ') and len(w1) != 2:
        raise NotImplementedError(f"The function doesn't support {w1}.")
    list_w1 = list(w1)
    list_w2 = list(w2)
    newword = list()
    newword.append(list_w1[0])
    newword.append("ั")
    consonant_start = [i for i in list_w2 if i in set(thai_consonants)][0]
    if consonant_start in ["ก", "ช", "ค", "ข", "ง"]:
        newword.append("ง")
    elif consonant_start in ["จ", "ฉ", "ช", "ฌ"]:
        newword.append("ญ")
    elif consonant_start in ["ฎ", "ฐ", "ฑ", "ณ"]:
        newword.append("ณ")
    elif consonant_start in ["ด", "ถ", "ท", "ธ", "น"]:
        newword.append("น")
    elif consonant_start in ["ป", "ผ", "พ", "ภ"]:
        newword.append("ม")
    elif consonant_start in ["ย", "ร", "ล", "ฬ", "ว", "ศ", "ษ", "ส", "ห"]:
        newword.append("ง")
    else:
        raise NotImplementedError(f"""
        The function doesn't support {w1} and {w2}.
        """)
    newword.extend(list_w2)
    return ''.join(newword)
