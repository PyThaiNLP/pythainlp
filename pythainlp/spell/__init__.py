# -*- coding: utf-8 -*-
"""
Spell checking
"""

from typing import List

from .pn import DEFAULT_SPELL_CHECKER, NorvigSpellChecker

__all__ = ["DEFAULT_SPELL_CHECKER", "correct", "spell", "NorvigSpellChecker"]


def spell(word: str, engine: str = "pn") -> List[str]:
    """
    Provides a list of possible correct spelling of the given word.
    The list of words are from the words in the dictionary
    that incurs an edit distance value of 1 or 2.
    The result is a list of words sorted by their occurrences
    in the spelling dictionary in descending order.

    :param str word: Word to spell check
    :param str engine:
        * *pn* - Peter Norvig's algorithm [norvig_spellchecker]_ (default)

    :return: list of possible correct words within 1 or 2 edit distance and
             sorted by frequency of word occurrences in the spelling dictionary
             in descending order.
    :rtype: list[str]

    :Example:
        >>> from pythainlp.spell import spell
        >>>
        >>> spell("เส้นตรบ",  engine="pn")
        ['เส้นตรง']
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
    Corrects the spelling of the given word by returning
    the correctly spelled word.

    :param str word: word to correct spelling
    :param str engine:
        * pn - Peter Norvig's algorithm [norvig_spellchecker]_ (default)
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
