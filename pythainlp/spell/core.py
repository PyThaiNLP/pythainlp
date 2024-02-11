# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Spell checking functions
"""

import itertools
from typing import List

from pythainlp.spell import DEFAULT_SPELL_CHECKER


def spell(word: str, engine: str = "pn") -> List[str]:
    """
    Provides a list of possible correct spellings of the given word.
    The list of words are from the words in the dictionary
    that incurs an edit distance value of 1 or 2.
    The result is a list of words sorted by their occurrences
    in the spelling dictionary in descending order.

    :param str word: Word to check spell of
    :param str engine:
        * *pn* - Peter Norvig's algorithm [#norvig_spellchecker]_ (default)
        * *phunspell* - A spell checker utilizing spylls, a port of Hunspell.
        * *symspellpy* - symspellpy is a Python port of SymSpell v6.5.
        * *tltk* - wrapper for `TLTK <https://pypi.org/project/tltk/>`_.

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

        spell("เส้นตรบ",  engine="tltk")
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
    if engine == "phunspell":
        from pythainlp.spell.phunspell import spell as SPELL_CHECKER

        text_correct = SPELL_CHECKER(word)
    elif engine == "symspellpy":
        from pythainlp.spell.symspellpy import spell as SPELL_CHECKER

        text_correct = SPELL_CHECKER(word)
    elif engine == "tltk":
        from pythainlp.spell.tltk import spell as SPELL_CHECKER

        text_correct = SPELL_CHECKER(word)
    else:
        text_correct = DEFAULT_SPELL_CHECKER.spell(word)

    return text_correct


def correct(word: str, engine: str = "pn") -> str:
    """
    Corrects the spelling of the given word by returning
    the correctly spelled word.

    :param str word: word to correct spelling of
    :param str engine:
        * *pn* - Peter Norvig's algorithm [#norvig_spellchecker]_ (default)
        * *phunspell* - A spell checker utilizing spylls, a port of Hunspell.
        * *symspellpy* - symspellpy is a Python port of SymSpell v6.5.
        * *wanchanberta_thai_grammarly* - WanchanBERTa Thai Grammarly
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
    if engine == "phunspell":
        from pythainlp.spell.phunspell import correct as SPELL_CHECKER

        text_correct = SPELL_CHECKER(word)
    elif engine == "symspellpy":
        from pythainlp.spell.symspellpy import correct as SPELL_CHECKER

        text_correct = SPELL_CHECKER(word)
    elif engine == "wanchanberta_thai_grammarly":
        from pythainlp.spell.wanchanberta_thai_grammarly import correct as SPELL_CHECKER

        text_correct = SPELL_CHECKER(word)

    else:
        text_correct = DEFAULT_SPELL_CHECKER.correct(word)

    return text_correct


def spell_sent(list_words: List[str], engine: str = "pn") -> List[List[str]]:
    """
    Provides a list of possible correct spellings of sentence

    :param List[str] list_words: list of words in sentence
    :param str engine:
        * *pn* - Peter Norvig's algorithm [#norvig_spellchecker]_ (default)
        * *phunspell* - A spell checker utilizing spylls, a port of Hunspell.
        * *symspellpy* - symspellpy is a Python port of SymSpell v6.5.
    :return: list of possibly correct words
    :rtype: List[List[str]]

    :Example:
    ::

        from pythainlp.spell import spell_sent

        spell_sent(["เด็","อินอร์เน็ต","แรง"],engine='symspellpy')
        # output: [['เด็ก', 'อินเทอร์เน็ต', 'แรง']]
    """
    if engine == "symspellpy":
        from pythainlp.spell.symspellpy import spell_sent as symspellpy_spell

        list_new = symspellpy_spell(list_words)
    else:
        _temp = list(
            itertools.product(*[spell(i, engine=engine) for i in list_words])
        )
        list_new = []
        for i in _temp:
            _temp2 = []
            for j in i:
                _temp2.append(j)
            list_new.append(_temp2)

    return list_new


def correct_sent(list_words: List[str], engine: str = "pn") -> List[str]:
    """
    Corrects and returns the spelling of the given sentence

    :param List[str] list_words: list of words in sentence
    :param str engine:
        * *pn* - Peter Norvig's algorithm [#norvig_spellchecker]_ (default)
        * *phunspell* - A spell checker utilizing spylls, a port of Hunspell.
        * *symspellpy* - symspellpy is a Python port of SymSpell v6.5.
        * *wanchanberta_thai_grammarly* - WanchanBERTa Thai Grammarly
    :return: the corrected list of words in sentence
    :rtype: List[str]

    :Example:
    ::

        from pythainlp.spell import correct_sent

        correct_sent(["เด็","อินอร์เน็ต","แรง"],engine='symspellpy')
        # output: ['เด็ก', 'อินเทอร์เน็ต', 'แรง']
    """
    return spell_sent(list_words, engine=engine)[0]
