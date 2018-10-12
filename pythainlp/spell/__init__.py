# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
def spell(word,engine='pn'):
    """
    :param str word: the word to check spelling
    :param str engine:
        * pn - Peter Norvig's algorithm
        * hunspell - uses hunspell's algorithm, which should already exist in linux
    :return: list word
    """
    if engine=='pn':
        from .pn import spell as spell1
    elif engine=='hunspell':
        from .hunspell import spell as spell1
    return spell1(word)
