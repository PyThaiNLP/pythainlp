# -*- coding: utf-8 -*-
"""
Spell checking
"""

from .pn import spell as pn_spell


def spell(word, engine="pn"):
    """
    :param str word: word to check spelling
    :param str engine:
        * pn - Peter Norvig's algorithm (default)
    :return: list of words
    """

    return pn_spell(word)
