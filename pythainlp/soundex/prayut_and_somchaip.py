# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Soundex for Thai-English cross-language transliterated word retrieval.

References:
Prayut Suwanvisat, Somchai Prasitjutrakul.
Thai-English Cross-Language Transliterated Word Retrieval using Soundex
Technique. In 1998 [cited 2022 Sep 8].
Available from:
https://www.cp.eng.chula.ac.th/~somchai/spj/papers/ThaiText/ncsec98-clir.pdf

"""

from __future__ import annotations

from pythainlp import thai_characters

_C0: str = "AEIOUHWYอ"
_C1: str = "BFPVบฝฟปผพภว"
_C2: str = "CGJKQSXZขฃคฅฆฉฌกจซศษส"
_C3: str = "DTฎดฏตฐฑฒถทธ"
_C4: str = "Lลฬ"
_C5: str = "MNมณน"
_C6: str = "Rร"
_C7: str = "AEIOUอ"
_C8: str = "Hหฮ"
_C1_1: str = "Wว"
_C9: str = "Yยญ"
_C52: str = "ง"


_VALID_CHARS: str = thai_characters + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _build_table(
    groups: tuple[tuple[str, str], ...],
) -> dict[str, str]:
    """Map each character to a code; the first matching group wins."""
    table: dict[str, str] = {}
    for chars, code in groups:
        for ch in chars:
            table.setdefault(ch, code)
    return table


_FIRST_GROUPS: tuple[tuple[str, str], ...] = (
    (_C0, "0"),
    (_C1, "1"),
    (_C2, "2"),
    (_C3, "3"),
    (_C4, "4"),
    (_C5, "5"),
    (_C6, "6"),
    (_C52, "52"),
)
# Codes for the first character
_FIRST_CODES: dict[str, str] = _build_table(_FIRST_GROUPS)
# Codes for the other characters
_REST_CODES: dict[str, str] = _build_table(
    _FIRST_GROUPS[1:]
    + (
        (_C7, "7"),
        (_C8, "8"),
        (_C1_1, "1"),
        (_C9, "9"),
    )
)


def prayut_and_somchaip(text: str, length: int = 4) -> str:
    """
    Convert a Thai-English transliterated word into a phonetic code.

    The code uses the Soundex matching technique
    [#prayut_and_somchaip]_.

    :param str text: English or Thai transliterated word to be encoded
    :param int length: preferred length of the soundex code (default is 4)
    :return: soundex code
    :rtype: str

    :Example:

        >>> from pythainlp.soundex.prayut_and_somchaip import (
        ...     prayut_and_somchaip,
        ... )
        >>> prayut_and_somchaip("king", 2)
        '52'
        >>> prayut_and_somchaip("คิง", 2)
        '52'
    """
    if not text or not isinstance(text, str):
        return ""
    text = text.upper()
    # keep only consonants (English-Thai)
    chars = [ch for ch in text if ch in _VALID_CHARS]

    codes = [_FIRST_CODES.get(chars[0], "")] if chars else []
    codes.extend(_REST_CODES.get(ch, "") for ch in chars[1:])
    # BUG-LEDGER: prayut-last-length (keeps the last `length` characters)
    return "".join(codes)[-length:]
