# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Spell checking functions"""

from __future__ import annotations

import itertools
from functools import lru_cache
from typing import TYPE_CHECKING

from pythainlp.spell import DEFAULT_SPELL_CHECKER

if TYPE_CHECKING:
    from pythainlp.spell.pn import NorvigSpellChecker


@lru_cache
def default_spell_checker() -> "NorvigSpellChecker":
    """Lazy load default spell checker with cache"""
    return DEFAULT_SPELL_CHECKER()


def spell(word: str, engine: str = "pn") -> list[str]:
    """Provides a list of possible correct spellings of the given word.
    The list of words is from words in the dictionary
    that have an edit distance value of 1 or 2.
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

        >>> from pythainlp.spell import spell  # doctest: +SKIP

        >>> spell("เส้นตรบ", engine="pn")  # doctest: +SKIP
        ['เส้นตรง']

        >>> spell("เส้นตรบ")  # doctest: +SKIP
        ['เส้นตรง']

        >>> spell("เส้นตรบ", engine="tltk")  # doctest: +SKIP
        ['เส้นตรง']

        >>> spell("ครัช")  # doctest: +SKIP
        ['ครับ', 'ครัว', 'รัช', 'ครัม', 'ครัน', 'วรัช', 'ครัส',
        'ปรัช', 'บรัช', 'ครัง', 'คัช', 'คลัช', 'ครัย', 'ครัด']

        >>> spell("กระปิ")  # doctest: +SKIP
        ['กะปิ', 'กระบิ']

        >>> spell("สังเกตุ")  # doctest: +SKIP
        ['สังเกต']

        >>> spell("เหตการณ")  # doctest: +SKIP
        ['เหตุการณ์']
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
        text_correct = default_spell_checker().spell(word)

    return text_correct


def correct(word: str, engine: str = "pn") -> str:
    """Corrects the spelling of the given word by returning
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

        >>> from pythainlp.spell import correct  # doctest: +SKIP

        >>> correct("เส้นตรบ")  # doctest: +SKIP
        'เส้นตรง'

        >>> correct("ครัช")  # doctest: +SKIP
        'ครับ'

        >>> correct("สังเกตุ")  # doctest: +SKIP
        'สังเกต'

        >>> correct("กระปิ")  # doctest: +SKIP
        'กะปิ'

        >>> correct("เหตการณ")  # doctest: +SKIP
        'เหตุการณ์'
    """
    if engine == "phunspell":
        from pythainlp.spell.phunspell import correct as SPELL_CHECKER

        text_correct = SPELL_CHECKER(word)
    elif engine == "symspellpy":
        from pythainlp.spell.symspellpy import correct as SPELL_CHECKER

        text_correct = SPELL_CHECKER(word)
    elif engine == "wanchanberta_thai_grammarly":
        from pythainlp.spell.wanchanberta_thai_grammarly import (
            correct as SPELL_CHECKER,
        )

        text_correct = SPELL_CHECKER(word)

    else:
        text_correct = default_spell_checker().correct(word)

    return text_correct


def spell_sent(list_words: list[str], engine: str = "pn") -> list[list[str]]:
    """Provides a list of possible correct spellings of sentence

    :param list[str] list_words: list of words in sentence
    :param str engine:
        * *pn* - Peter Norvig's algorithm [#norvig_spellchecker]_ (default)
        * *phunspell* - A spell checker utilizing spylls, a port of Hunspell.
        * *symspellpy* - symspellpy is a Python port of SymSpell v6.5.
    :return: list of possibly correct words
    :rtype: list[list[str]]

    :Example:

        >>> from pythainlp.spell import spell_sent  # doctest: +SKIP

        >>> spell_sent(["เด็", "อินอร์เน็ต", "แรง"], engine="symspellpy")  # doctest: +SKIP
        [['เด็ก', 'อินเทอร์เน็ต', 'แรง']]
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


def correct_sent(list_words: list[str], engine: str = "pn") -> list[str]:
    """Corrects and returns the spelling of the given sentence

    :param list[str] list_words: list of words in sentence
    :param str engine:
        * *pn* - Peter Norvig's algorithm [#norvig_spellchecker]_ (default)
        * *phunspell* - A spell checker utilizing spylls, a port of Hunspell.
        * *symspellpy* - symspellpy is a Python port of SymSpell v6.5.
        * *wanchanberta_thai_grammarly* - WanchanBERTa Thai Grammarly
    :return: the corrected list of words in sentence
    :rtype: list[str]

    :Example:

        >>> from pythainlp.spell import correct_sent  # doctest: +SKIP

        >>> correct_sent(["เด็", "อินอร์เน็ต", "แรง"], engine="symspellpy")  # doctest: +SKIP
        ['เด็ก', 'อินเทอร์เน็ต', 'แรง']
    """
    return spell_sent(list_words, engine=engine)[0]
