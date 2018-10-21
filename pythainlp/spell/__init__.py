# -*- coding: utf-8 -*-
"""
Spell checking
"""
from __future__ import absolute_import, unicode_literals


def spell(word, engine="pn"):
    """
    :param str word: word to check spelling
    :param str engine:
        * pn - Peter Norvig's algorithm
        * hunspell - uses hunspell's algorithm, which should already exist in Linux
    :return: list of words
    """
    if engine == "hunspell":
        from .hunspell import spell as _spell
    else:  # default, use "pn" engine
        from .pn import spell as _spell

    return _spell(word)
