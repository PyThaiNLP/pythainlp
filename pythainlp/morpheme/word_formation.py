# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import Optional

from pythainlp import thai_consonants

# Consonant that follows nighit, by the first consonant of the next word.
# Each consonant appears in at most one row, sorted in Thai alphabetical
# order. ฎ and ด are kept for compatibility.
# Unsupported: ฃ ฅ ซ บ ฝ ฟ อ ฮ
_NIGHIT_ENDINGS: tuple[tuple[tuple[str, ...], str], ...] = (
    (("ก", "ข", "ค", "ฆ", "ง"), "ง"),
    (("จ", "ฉ", "ช", "ฌ", "ญ"), "ญ"),
    (("ฎ", "ฏ", "ฐ", "ฑ", "ฒ", "ณ"), "ณ"),
    (("ด", "ต", "ถ", "ท", "ธ", "น"), "น"),
    (("ป", "ผ", "พ", "ภ", "ม"), "ม"),
    (("ย", "ร", "ล", "ว", "ศ", "ษ", "ส", "ห", "ฬ"), "ง"),
)


def _nighit_ending(consonant: str) -> Optional[str]:
    """Return the consonant that follows nighit, or None if unsupported."""
    for consonants, ending in _NIGHIT_ENDINGS:
        if consonant in consonants:
            return ending
    return None


def nighit(w1: str, w2: str) -> str:
    """Create a new word using Nighit (นิคหิต or ํ).

    Nighit is the niggahita in Thai, used to form new words
    from Pali roots. This function applies a simple rule to
    combine two Thai words derived from Pali.

    Reference: https://www.trueplookpanya.com/learning/detail/1180

    :param str w1: a Thai word ending with a nighit (ํ)
    :param str w2: a Thai word
    :return: combined Thai word
    :rtype: str
    :Example:

        >>> from pythainlp.morpheme import nighit
        >>> nighit("สํ", "คีต")
        'สังคีต'
        >>> nighit("สํ", "จร")
        'สัญจร'
        >>> nighit("สํ", "ญา")
        'สัญญา'
        >>> nighit("สํ", "มา")
        'สัมมา'
        >>> nighit("สํ", "ฐาน")
        'สัณฐาน'
        >>> nighit("สํ", "นิษฐาน")
        'สันนิษฐาน'
        >>> nighit("สํ", "ปทา")
        'สัมปทา'
        >>> nighit("สํ", "โยค")
        'สังโยค'
    """
    if not isinstance(w1, str) or not isinstance(w2, str):
        raise TypeError("Both w1 and w2 must be strings.")
    w1 = w1.strip()
    w2 = w2.strip()
    if not w1:
        return w2
    if not w2:
        return w1
    if not w1.endswith("ํ"):
        raise NotImplementedError(f"The function doesn't support {w1}.")
    list_w1 = list(w1)
    list_w2 = list(w2)
    newword = []
    newword.append(list_w1[0])
    newword.append("ั")
    _consonants = set(thai_consonants)
    consonants_in_w2 = [i for i in list_w2 if i in _consonants]
    if not consonants_in_w2:
        raise ValueError(f"w2 {w2!r} contains no Thai consonants.")
    consonant_start = consonants_in_w2[0]
    ending = _nighit_ending(consonant_start)
    if ending is None:
        raise NotImplementedError(f"""
        The function doesn't support {w1} and {w2}.
        """)
    newword.append(ending)
    newword.extend(list_w2)
    return "".join(newword)
