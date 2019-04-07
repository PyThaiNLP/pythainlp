# -*- coding: utf-8 -*-
"""
Spell checking
"""

from typing import List

from .pn import DEFAULT_SPELL_CHECKER, NorvigSpellChecker

__all__ = ["DEFAULT_SPELL_CHECKER", "correct", "spell", "NorvigSpellChecker"]


def spell(word: str, engine="pn") -> List[str]:
    """
    :param str word: word to check spelling
    :param str engine:
        * pn - Peter Norvig's algorithm (default)
    :return: list of words
    """

    return DEFAULT_SPELL_CHECKER.spell(word)


def correct(word: str, engine="pn") -> str:
    """
    :param str word: word to correct spelling
    :param str engine:
        * pn - Peter Norvig's algorithm (default)
    :return: the corrected word
    """

    return DEFAULT_SPELL_CHECKER.correct(word)
