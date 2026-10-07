# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Thai soundex, MetaSound system.

References:
Snae & Brückner. (2009). Novel Phonetic Name Matching Algorithm with
a Statistical Ontology for Analysing Names Given in Accordance
with Thai Astrology.
https://pdfs.semanticscholar.org/3983/963e87ddc6dfdbb291099aa3927a0e3e4ea6.pdf

"""

from __future__ import annotations

_CONS_THANTHAKHAT: str = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ์"
_THANTHAKHAT: str = "์"  # \u0e4c
_C1: str = "กขฃคฆฅ"  # sound K -> coded letter 1
_C2: str = "จฉชฌซฐฏทฑฒถธดฎตสศษ"  # D -> 2
_C3: str = "ฟฝพผภบป"  # B -> 3
_C4: str = "ง"  # NG -> 4
_C5: str = "ลฬรนณฦญ"  # N -> 5
_C6: str = "ม"  # M -> 6
_C7: str = "ย"  # Y -> 7
_C8: str = "ว"  # W -> 8


def _build_code_table() -> dict[str, str]:
    """Map each consonant to its code; the first matching group wins."""
    table: dict[str, str] = {}
    groups = (_C1, _C2, _C3, _C4, _C5, _C6, _C7, _C8)
    for code, group in enumerate(groups, start=1):
        for ch in group:
            table.setdefault(ch, str(code))
    return table


_CODES: dict[str, str] = _build_code_table()


def _remove_karan(chars: list[str]) -> list[str]:
    """Remove each thanthakhat and the character before it."""
    if _THANTHAKHAT not in chars:
        return chars
    kept: list[str] = []
    prev = ""
    for ch in chars:
        if ch != _THANTHAKHAT:
            kept.append(ch)
        elif kept and prev != _THANTHAKHAT:
            kept.pop()
        prev = ch
    return kept


def metasound(text: str, length: int = 4) -> str:
    """
    Convert text into a MetaSound phonetic code.

    MetaSound [#metasound]_ is a combination of the Soundex and
    Metaphone algorithms.

    The MetaSound algorithm was developed specifically for Thai.

    :param str text: Thai word to be encoded
    :param int length: preferred length of the MetaSound code (default is 4)
    :return: MetaSound code
    :rtype: str

    :Example:

        >>> from pythainlp.soundex.metasound import metasound
        >>> metasound("ลัก")
        'ล100'
        >>> metasound("รัก")
        'ร100'
        >>> metasound("รักษ์")
        'ร100'
        >>> metasound("บูรณการ", 5)
        'บ5515'
        >>> metasound("บูรณการ", 6)
        'บ55150'
        >>> metasound("บูรณการ", 4)
        'บ551'
    """
    if not text or not isinstance(text, str):
        return ""

    # keep only consonants and thanthakhat
    chars = [ch for ch in text if ch in _CONS_THANTHAKHAT]
    chars = _remove_karan(chars)[:length]

    # the first character stays; the rest are coded
    coded = [chars[0]] if chars else []
    coded.extend(_CODES.get(ch, "0") for ch in chars[1:])
    if len(coded) < length:
        coded.extend("0" * (length - len(coded)))
    return "".join(coded)
