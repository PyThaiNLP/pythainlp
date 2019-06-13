# -*- coding: utf-8 -*-
"""
Spell checking
"""

from typing import List

from .pn import DEFAULT_SPELL_CHECKER, NorvigSpellChecker

__all__ = ["DEFAULT_SPELL_CHECKER", "correct", "spell", "NorvigSpellChecker"]


def spell(word: str, engine: str = "pn") -> List[str]:
    """
    This function provides a list of possible correct spelling of the given word.

    :param str word: word to check spelling
    :param str engine:
        * pn - Peter Norvig's algorithm (default)
    :return: list of possible correct words
    :rtype: list[str]

    :Example:
        >>> from pythainlp.spell import spell
        >>> 
        >>> spell("เส้นตรบ")
        ['เส้นตรง']
        >>>
        >>> spell("ครัช")
        ['ครับ', 'ครัว', 'รัช', 'ครัม', 'ครัน', 'วรัช', 'ครัส', 
        'ปรัช', 'บรัช', 'ครัง', 'คัช', 'คลัช', 'ครัย', 'ครัด']
        >>>
        >>> spell("กระปิ") 
        ['กะปิ', 'กระบิ']
        >>>
        >>> spell("สังเกตุ")
        ['สังเกต']
        >>>
        >>> spell("เหตการณ")
        ['เหตุการณ์']
    """

    return DEFAULT_SPELL_CHECKER.spell(word)


def correct(word: str, engine: str = "pn") -> str:
    """
    This function corrects spelling of the given word by returning the correctly spelled word.

    :param str word: word to correct spelling
    :param str engine:
        * pn - Peter Norvig's algorithm (default)
    :return: the corrected word
    :rtype: str

    :Example:
        >>> from pythainlp.spell import correct
        >>> 
        >>> correct("เส้นตรบ")
        'เส้นตรง'
        >>> correct("ครัช")
        'ครับ'
        >>> correct("สังเกตุ")
        'สังเกต'
        >>> correct("กระปิ")
        'กะปิ'
        >>> correct("เหตการณ")
        'เหตุการณ์'
    """

    return DEFAULT_SPELL_CHECKER.correct(word)
