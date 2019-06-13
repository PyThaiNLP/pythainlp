# -*- coding: utf-8 -*-
"""
Spell checking
"""

from typing import List

from .pn import DEFAULT_SPELL_CHECKER, NorvigSpellChecker

__all__ = ["DEFAULT_SPELL_CHECKER", "correct", "spell", "NorvigSpellChecker"]


def spell(word: str, engine: str = "pn") -> List[str]:
    """
    :param str word: word to check spelling
    :param str engine:
        * pn - Peter Norvig's algorithm (default)
    :return: list of words
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
        >>> correct("เหตการณ")
        'เหตุการณ์'
    """

    return DEFAULT_SPELL_CHECKER.correct(word)
