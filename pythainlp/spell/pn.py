# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Spell checker using Peter Norvig's algorithm.

The spelling dictionary can be customized.
The default spelling dictionary is based on Phupha: Thai Word Frequency
Dataset, filtered with the Royal Society of Thailand word list.

Based on Peter Norvig's Python code from https://norvig.com/spell-correct.html
"""

from __future__ import annotations

from collections import Counter
from string import digits
from typing import TYPE_CHECKING, Optional, Union, cast

if TYPE_CHECKING:
    from collections.abc import Callable, ItemsView, Iterable

from pythainlp import thai_digits, thai_letters
from pythainlp.corpus import phupha, thai_orst_words
from pythainlp.util import is_thai_char


def _no_filter(word: str) -> bool:
    return True


def _is_thai_and_not_num(word: str) -> bool:
    for ch in word:
        if ch != "." and not is_thai_char(ch):
            return False
        if ch in thai_digits or ch in digits:
            return False
    return True


def _keep(
    word_freq: tuple[str, int],
    min_freq: int,
    min_len: int,
    max_len: int,
    dict_filter: Optional[Callable[[str], bool]],
) -> bool:
    """
    Check if a word has the required minimum frequency and length.

    The word must have a frequency of at least ``min_freq`` and a length
    between ``min_len`` and ``max_len`` (inclusive).

    :param tuple[str, int] word_freq: word and its frequency
    :param int min_freq: minimum frequency of a word to keep
    :param int min_len: minimum length (in characters) of a word to keep
    :param int max_len: maximum length (in characters) of a word to keep
    :param Optional[Callable[[str], bool]] dict_filter: function that
        returns ``True`` for a word to keep
    :return: ``True`` if the word satisfies all conditions
    :rtype: bool
    """
    if not word_freq or word_freq[1] < min_freq:
        return False

    word = word_freq[0]
    if not (word and min_len <= len(word) <= max_len and word[0] != "."):
        return False

    if not dict_filter:
        dict_filter = _no_filter

    return dict_filter(word)


def _edits1(word: str) -> set[str]:
    """
    Return the set of words with an edit distance of 1 from a word.

    :param str word: input word
    :return: set of words with an edit distance of 1
    :rtype: set[str]
    """
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in thai_letters]
    inserts = [L + c + R for L, R in splits for c in thai_letters]

    # Use set union for better performance than list concatenation
    result = set(deletes)
    result.update(transposes)
    result.update(replaces)
    result.update(inserts)

    return result


def _edits2(word: str) -> set[str]:
    """
    Return the set of words with an edit distance of 2 from a word.

    :param str word: input word
    :return: set of words with an edit distance of 2
    :rtype: set[str]
    """
    return {e2 for e1 in _edits1(word) for e2 in _edits1(e1)}


def _convert_custom_dict(
    custom_dict: Union[
        dict[str, int], Iterable[str], Iterable[tuple[str, int]]
    ],
    min_freq: int,
    min_len: int,
    max_len: int,
    dict_filter: Optional[Callable[[str], bool]],
) -> list[tuple[str, int]]:
    """
    Convert a custom dictionary to a list of (word, frequency) tuples.

    :param custom_dict: custom spelling dictionary
    :type custom_dict: Union[dict[str, int], Iterable[str],
        Iterable[tuple[str, int]]]
    :param int min_freq: minimum frequency of a word to keep
    :param int min_len: minimum length (in characters) of a word to keep
    :param int max_len: maximum length (in characters) of a word to keep
    :param Optional[Callable[[str], bool]] dict_filter: function that
        returns ``True`` for a word to keep
    :return: list of (word, frequency) tuples
    :rtype: list[tuple[str, int]]
    :raises TypeError: if the dictionary members are neither words nor
        (word, frequency) tuples
    """
    if isinstance(custom_dict, dict):
        custom_dict = list(custom_dict.items())

    i = iter(custom_dict)
    first_member = next(i)

    result: list[tuple[str, int]]

    if isinstance(first_member, str):
        # create tuples of a word with frequency equaling 1,
        # and filter word list
        custom_dict = cast("Iterable[str]", custom_dict)
        result = [
            (word, 1)
            for word in custom_dict
            if _keep((word, 1), 1, min_len, max_len, dict_filter)
        ]
    elif isinstance(first_member, tuple):
        # filter word list
        custom_dict = cast("Iterable[tuple[str, int]]", custom_dict)
        result = [
            word_freq
            for word_freq in custom_dict
            if _keep(word_freq, min_freq, min_len, max_len, dict_filter)
        ]
    else:
        raise TypeError(
            "custom_dict must be either Dict[str, int], "
            "Iterable[Tuple[str, int]], or Iterable[str]"
        )

    return result


class NorvigSpellChecker:
    """Check and correct spelling using Peter Norvig's algorithm."""

    def __init__(
        self,
        custom_dict: Optional[
            Union[dict[str, int], Iterable[str], Iterable[tuple[str, int]]]
        ] = None,
        min_freq: int = 2,
        min_len: int = 2,
        max_len: int = 40,
        dict_filter: Optional[Callable[[str], bool]] = _is_thai_and_not_num,
    ) -> None:
        """
        Initialize Peter Norvig's spell checker.

        The spelling dictionary can be customized. By default, it is from
        `Phupha: Thai Word Frequency Dataset
        <https://github.com/PyThaiNLP/Phupha-Word-freq>`_
        (filtered with the Royal Society of Thailand word list).

        Norvig's spell checker chooses the most likely corrected spelling
        of a word by searching for candidate words based on edit distance.
        Then, it selects the candidate with the highest word occurrence
        probability.

        :param custom_dict: custom spelling dictionary, one of:

            (1) a dict with words (``str``) as keys and frequencies
                (``int``) as values;
            (2) an iterable (list, tuple, or set) of tuples of word and
                frequency: ``(str, int)``; or
            (3) an iterable of words (``str``) without frequencies;
                in this case, ``1`` is assigned to every word.

            The default is the Phupha dataset, filtered with the Royal
            Society of Thailand word list (38,160 words).
        :type custom_dict: Union[dict[str, int], Iterable[str],
            Iterable[tuple[str, int]]], optional
        :param int min_freq: minimum frequency of a word to keep
            (default: 2)
        :param int min_len: minimum length (in characters) of a word to
            keep (default: 2)
        :param int max_len: maximum length (in characters) of a word to
            keep (default: 40)
        :param Optional[Callable[[str], bool]] dict_filter: function to
            filter the dictionary. The default filter removes any word
            with numbers or non-Thai characters. Use ``None`` for no filter
        """
        if not custom_dict:  # default, use Phupha filtered with ORST words
            orst_words = thai_orst_words()
            custom_dict = [
                (word, freq)
                for word, freq in phupha.word_freqs()
                if word in orst_words
            ]

        if not dict_filter:
            dict_filter = _no_filter

        custom_dict = _convert_custom_dict(
            custom_dict, min_freq, min_len, max_len, dict_filter
        )

        self.__WORDS: Counter[str] = Counter(dict(custom_dict))
        self.__WORDS += Counter()  # remove zero and negative counts
        self.__WORDS_TOTAL: int = sum(self.__WORDS.values())

    def dictionary(self) -> ItemsView[str, int]:
        """
        Return the spelling dictionary used by this spell checker.

        :return: spelling dictionary of this instance
        :rtype: ItemsView[str, int]

        :Example:

            >>> from pythainlp.spell import (
            ...     NorvigSpellChecker,
            ... )  # doctest: +SKIP

            >>> dictionary = [
            ...     ("หวาน", 30),
            ...     ("มะนาว", 2),
            ...     ("แอบ", 3223),
            ... ]  # doctest: +SKIP

            >>> checker = NorvigSpellChecker(
            ...     custom_dict=dictionary
            ... )  # doctest: +SKIP
            >>> checker.dictionary()  # doctest: +SKIP
            dict_items([('หวาน', 30), ('มะนาว', 2), ('แอบ', 3223)])
        """
        return self.__WORDS.items()

    def known(self, words: Iterable[str]) -> list[str]:
        """
        Return the given words that are found in the spelling dictionary.

        :param Iterable[str] words: words to look up in the spelling
            dictionary
        :return: intersection of the given words and words in the
            spelling dictionary
        :rtype: list[str]

        :Example:

            >>> from pythainlp.spell import (
            ...     NorvigSpellChecker,
            ... )  # doctest: +SKIP

            >>> checker = NorvigSpellChecker()  # doctest: +SKIP

            >>> checker.known(["เพยน", "เพล", "เพลง"])  # doctest: +SKIP
            ['เพล', 'เพลง']

            >>> checker.known(["ยกไ", "ไฟล์ม"])  # doctest: +SKIP
            []

            >>> checker.known([])  # doctest: +SKIP
            []
        """
        return [w for w in words if w in self.__WORDS]

    def prob(self, word: str) -> float:
        """
        Return the occurrence probability of a word.

        The probability is according to the spelling dictionary.

        :param str word: word to get the occurrence probability of
        :return: word occurrence probability
        :rtype: float

        :Example:

            >>> from pythainlp.spell import (
            ...     NorvigSpellChecker,
            ... )  # doctest: +SKIP

            >>> checker = NorvigSpellChecker()  # doctest: +SKIP

            >>> checker.prob("ครัช")  # doctest: +SKIP
            0.0

            >>> checker.prob("รัก")  # doctest: +SKIP
            0.0006959172792052158

            >>> checker.prob("น่ารัก")  # doctest: +SKIP
            9.482306849763902e-05
        """
        return self.__WORDS[word] / self.__WORDS_TOTAL

    def freq(self, word: str) -> int:
        """
        Return the frequency of a word.

        The frequency is according to the spelling dictionary.

        :param str word: word to get the frequency of
        :return: frequency of the word in the spelling dictionary
        :rtype: int

        :Example:

            >>> from pythainlp.spell import (
            ...     NorvigSpellChecker,
            ... )  # doctest: +SKIP

            >>> checker = NorvigSpellChecker()  # doctest: +SKIP

            >>> checker.freq("ปัญญา")  # doctest: +SKIP
            3639

            >>> checker.freq("บิญชา")  # doctest: +SKIP
            0
        """
        return self.__WORDS[word]

    def spell(self, word: str) -> list[str]:
        """
        Return correctly spelled words that are similar to a word.

        The similarity is by edit distance. The returned words are sorted
        by word frequency in the spelling dictionary, in descending order.

        First, if the word is spelled correctly, this method returns a
        list of exactly one word, which is the word itself.
        Next, this method looks for all correctly spelled words with an
        edit distance of 1 from the word.
        If there is no such word, the search expands to words with an
        edit distance of 2.
        If that still fails, this method returns a list of the input word.

        :param str word: word to be checked
        :return: list of possible correct words within 1 or 2 edit distance,
            sorted by frequency of occurrence in the spelling dictionary
            in descending order
        :rtype: list[str]

        :Example:

            >>> from pythainlp.spell import (
            ...     NorvigSpellChecker,
            ... )  # doctest: +SKIP

            >>> checker = NorvigSpellChecker()  # doctest: +SKIP

            >>> checker.spell("เส้นตรบ")  # doctest: +SKIP
            ['เส้นตรง']

            >>> checker.spell("ครัช")  # doctest: +SKIP
            ['ครับ', 'ครัว', 'รัช', 'ครัม', 'ครัน',
            'วรัช', 'ครัส', 'ปรัช', 'บรัช', 'ครัง',
            'คัช', 'คลัช', 'ครัย', 'ครัด']
        """
        if not word:
            return [""]

        candidates = (
            self.known([word])
            or self.known(_edits1(word))
            or self.known(_edits2(word))
            or [word]
        )
        candidates.sort(key=self.freq, reverse=True)

        return candidates

    def correct(self, word: str) -> str:
        """
        Return the most probable correct spelling of a word.

        The probability is from the spelling dictionary.

        :param str word: word to be corrected
        :return: corrected word
        :rtype: str

        :Example:

            >>> from pythainlp.spell import (
            ...     NorvigSpellChecker,
            ... )  # doctest: +SKIP

            >>> checker = NorvigSpellChecker()  # doctest: +SKIP

            >>> checker.correct("ปัญชา")  # doctest: +SKIP
            'ปัญหา'

            >>> checker.correct("บิญชา")  # doctest: +SKIP
            'บัญชา'

            >>> checker.correct("มิตรภาบ")  # doctest: +SKIP
            'มิตรภาพ'
        """
        if not word:
            return ""

        # Check for numeric type
        try:
            if "." in word:
                float(word)
            else:
                int(word)
            return word
        except ValueError:
            pass

        return self.spell(word)[0]
