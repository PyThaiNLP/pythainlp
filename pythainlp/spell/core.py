# -*- coding: utf-8 -*-
"""
Spell checking functions
"""

from typing import List

from pythainlp.spell import DEFAULT_SPELL_CHECKER


def spell(word: str, engine: str = "pn") -> List[str]:
    """
    Provides a list of possible correct spelling of the given word.
    The list of words are from the words in the dictionary
    that incurs an edit distance value of 1 or 2.
    The result is a list of words sorted by their occurrences
    in the spelling dictionary in descending order.

    :param str word: Word to spell check
    :param str engine:
        * *pn* - Peter Norvig's algorithm [#norvig_spellchecker]_ (default)

    :return: list of possible correct words within 1 or 2 edit distance and
             sorted by frequency of word occurrences in the spelling dictionary
             in descending order.
    :rtype: list[str]

    :Example:
    ::

        from pythainlp.spell import spell

        spell("เส้นตรบ",  engine="pn")
        # output: ['เส้นตรง']

        spell("เส้นตรบ")
        # output: ['เส้นตรง']

        spell("ครัช")
        # output: ['ครับ', 'ครัว', 'รัช', 'ครัม', 'ครัน', 'วรัช', 'ครัส',
        # 'ปรัช', 'บรัช', 'ครัง', 'คัช', 'คลัช', 'ครัย', 'ครัด']

        spell("กระปิ")
        # output: ['กะปิ', 'กระบิ']

        spell("สังเกตุ")
        # output:  ['สังเกต']

        spell("เหตการณ")
        # output:  ['เหตุการณ์']
    """

    return DEFAULT_SPELL_CHECKER.spell(word)


def correct(word: str, engine: str = "pn") -> str:
    """
    Corrects the spelling of the given word by returning
    the correctly spelled word.

    :param str word: word to correct spelling
    :param str engine:
        * pn - Peter Norvig's algorithm [#norvig_spellchecker]_ (default)
    :return: the corrected word
    :rtype: str

    :Example:
    ::

        from pythainlp.spell import correct

        correct("เส้นตรบ")
        # output: 'เส้นตรง'

        correct("ครัช")
        # output: 'ครับ'

        correct("สังเกตุ")
        # output: 'สังเกต'

        correct("กระปิ")
        # output: 'กะปิ'

        correct("เหตการณ")
        # output: 'เหตุการณ์'
    """

    return DEFAULT_SPELL_CHECKER.correct(word)
