# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Profanity detection for Thai."""

from __future__ import annotations

from typing import Optional

from pythainlp.corpus.common import thai_profanity_words, thai_words
from pythainlp.tokenize import word_tokenize
from pythainlp.util.trie import dict_trie


def contains_profanity(
    text: str, custom_words: Optional[set[str]] = None, engine: str = "newmm"
) -> bool:
    """
    Check whether text contains profanity words.

    :param str text: Thai text to check
    :param Optional[set[str]] custom_words: additional profanity words
        (default is None)
    :param str engine: word tokenization engine (default is *newmm*)
    :return: True if the text contains profanity, False otherwise
    :rtype: bool

    :Example:

        >>> from pythainlp.util import contains_profanity  # doctest: +SKIP

        >>> print(contains_profanity("สวัสดีครับ"))  # doctest: +SKIP
        False

        >>> print(contains_profanity("คำหยาบคาย"))  # doctest: +SKIP
        True if the word is in the profanity list

        >>> # Add custom profanity words
        >>> print(
        ...     contains_profanity("คำใหม่", custom_words={"คำใหม่"})
        ... )  # doctest: +SKIP
        True
    """
    if not text:
        return False

    profanity_set = set(thai_profanity_words())
    if custom_words:
        profanity_set.update(custom_words)

    # Create custom dictionary that merges thai_words and profanity_set
    # for better tokenization
    custom_dict_set = set(thai_words())
    custom_dict_set.update(profanity_set)
    custom_dict = dict_trie(dict_source=custom_dict_set)

    tokens = word_tokenize(text, custom_dict=custom_dict, engine=engine)

    return any(token in profanity_set for token in tokens)


def find_profanity(
    text: str, custom_words: Optional[set[str]] = None, engine: str = "newmm"
) -> list[str]:
    """
    Find all profanity words in text.

    :param str text: Thai text to check
    :param Optional[set[str]] custom_words: additional profanity words
        (default is None)
    :param str engine: word tokenization engine (default is *newmm*)
    :return: list of profanity words found in the text
    :rtype: list[str]

    :Example:

        >>> from pythainlp.util import find_profanity  # doctest: +SKIP

        >>> print(find_profanity("สวัสดีครับ"))  # doctest: +SKIP
        []

        >>> print(
        ...     find_profanity("text with profanity words")
        ... )  # doctest: +SKIP
        ['profanity_word1', 'profanity_word2']

        >>> # Add custom profanity words
        >>> print(
        ...     find_profanity("คำใหม่", custom_words={"คำใหม่"})
        ... )  # doctest: +SKIP
        ['คำใหม่']
    """
    if not text:
        return []

    profanity_set = set(thai_profanity_words())
    if custom_words:
        profanity_set.update(custom_words)

    # Create custom dictionary that merges thai_words and profanity_set
    # for better tokenization
    custom_dict_set = set(thai_words())
    custom_dict_set.update(profanity_set)
    custom_dict = dict_trie(dict_source=custom_dict_set)

    tokens = word_tokenize(text, custom_dict=custom_dict, engine=engine)

    return [token for token in tokens if token in profanity_set]


def censor_profanity(
    text: str,
    replacement: str = "*",
    custom_words: Optional[set[str]] = None,
    engine: str = "newmm",
) -> str:
    """
    Replace profanity words in text with a replacement character.

    :param str text: Thai text to censor
    :param str replacement: character to replace profanity with
        (default is ``"*"``)
    :param Optional[set[str]] custom_words: additional profanity words
        (default is None)
    :param str engine: word tokenization engine (default is *newmm*)
    :return: text with profanity words censored
    :rtype: str

    :Example:

        >>> from pythainlp.util import censor_profanity  # doctest: +SKIP

        >>> print(censor_profanity("สวัสดีครับ"))  # doctest: +SKIP
        สวัสดีครับ

        >>> print(
        ...     censor_profanity("text with profanity word")
        ... )  # doctest: +SKIP
        text with *** word

        >>> # Add custom profanity words
        >>> print(
        ...     censor_profanity("คำใหม่", custom_words={"คำใหม่"})
        ... )  # doctest: +SKIP
        ******
    """
    if not text:
        return text

    profanity_set = set(thai_profanity_words())
    if custom_words:
        profanity_set.update(custom_words)

    # Create custom dictionary that merges thai_words and profanity_set
    # for better tokenization
    custom_dict_set = set(thai_words())
    custom_dict_set.update(profanity_set)
    custom_dict = dict_trie(dict_source=custom_dict_set)

    tokens = word_tokenize(
        text, custom_dict=custom_dict, engine=engine, keep_whitespace=True
    )

    censored_tokens = []
    for token in tokens:
        if token in profanity_set:
            censored_tokens.append(replacement * len(token))
        else:
            censored_tokens.append(token)

    return "".join(censored_tokens)
