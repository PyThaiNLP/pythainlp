# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Spell checker, using Peter Norvig algorithm.
Spelling dictionary can be customized.
Default spelling dictionary is based on Phupha: Thai Word Frequency Dataset,
filtered with Royal Society of Thailand word list.

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
    """Checks whether a given word has the required minimum frequency min_freq
    and its character length is between min_len and max_len (inclusive).
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
    """Returns a set of words with an edit distance of 1 from the input word"""
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
    """Returns a set of words with an edit distance of 2 from the input word"""
    return set(e2 for e1 in _edits1(word) for e2 in _edits1(e1))


def _convert_custom_dict(
    custom_dict: Union[
        dict[str, int], Iterable[str], Iterable[tuple[str, int]]
    ],
    min_freq: int,
    min_len: int,
    max_len: int,
    dict_filter: Optional[Callable[[str], bool]],
) -> list[tuple[str, int]]:
    """Converts a custom dictionary to a list of (str, int) tuples"""
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
        """Initializes Peter Norvig's spell checker object.
        Spelling dictionary can be customized.
        By default, spelling dictionary is from
        `Phupha: Thai Word Frequency Dataset <https://github.com/PyThaiNLP/Phupha-Word-freq>`_
        (filtered with Royal Society of Thailand word list).

        Basically, Norvig's spell checker will choose the most likely
        corrected spelling given a word by searching for candidates of
        corrected words based on edit distance.
        Then, it selects the candidate with
        the highest word occurrence probability.

        :param custom_dict: A custom spelling dictionary. This can be:
                            (1) a dictionary (`dict`), with words (`str`)
                                as keys and frequencies (`int`) as values;
                            (2) an iterable (list, tuple, or set) of words
                                (`str`) and frequency (`int`) tuples:
                                ``(str, int)``; or
                            (3) an iterable of just words (`str`), without
                                frequencies -- in this case ``1`` will be
                                assigned to every word.
                            Default is from Phupha dataset, filtered with
                            Royal Society of Thailand word list (38,160 words).
        :type custom_dict: Union[dict[str, int], Iterable[str],
            Iterable[tuple[str, int]]], optional
        :param int min_freq: Minimum frequency of a word to keep (default = 2)
        :param int min_len: Minimum length (in characters) of a word to keep
                            (default = 2)
        :param int max_len: Maximum length (in characters) of a word to keep
                            (default = 40)
        :param func dict_filter: A function to filter the dictionary.
                                 Default filter removes any word
                                 with numbers or non-Thai characters.
                                 If no filter is required, use None.
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
        """Returns the spelling dictionary currently used by this spell checker

        :return: spelling dictionary of this instance
        :rtype: ItemsView[str, int]

        :Example:

            >>> from pythainlp.spell import NorvigSpellChecker  # doctest: +SKIP

            >>> dictionary = [("หวาน", 30), ("มะนาว", 2), ("แอบ", 3223)]  # doctest: +SKIP

            >>> checker = NorvigSpellChecker(custom_dict=dictionary)  # doctest: +SKIP
            >>> checker.dictionary()  # doctest: +SKIP
            dict_items([('หวาน', 30), ('มะนาว', 2), ('แอบ', 3223)])
        """
        return self.__WORDS.items()

    def known(self, words: Iterable[str]) -> list[str]:
        """Returns a list of given words found in the spelling dictionary

        :param list[str] words: A list of words to check if they exist
                                in the spelling dictionary

        :return: intersection of the given word list and words
                 in the spelling dictionary
        :rtype: list[str]

        :Example:

            >>> from pythainlp.spell import NorvigSpellChecker  # doctest: +SKIP

            >>> checker = NorvigSpellChecker()  # doctest: +SKIP

            >>> checker.known(["เพยน", "เพล", "เพลง"])  # doctest: +SKIP
            ['เพล', 'เพลง']

            >>> checker.known(["ยกไ", "ไฟล์ม"])  # doctest: +SKIP
            []

            >>> checker.known([])  # doctest: +SKIP
            []
        """
        return list(w for w in words if w in self.__WORDS)

    def prob(self, word: str) -> float:
        """Returns the probability of an input word,
        according to the spelling dictionary

        :param str word: A word to check occurrence probability of

        :return: word occurrence probability
        :rtype: float

        :Example:

            >>> from pythainlp.spell import NorvigSpellChecker  # doctest: +SKIP

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
        """Returns the frequency of an input word,
        according to the spelling dictionary

        :param str word: A word to check frequency of
        :return: frequency of the given word in the spelling dictionary
        :rtype: int

        :Example:

            >>> from pythainlp.spell import NorvigSpellChecker  # doctest: +SKIP

            >>> checker = NorvigSpellChecker()  # doctest: +SKIP

            >>> checker.freq("ปัญญา")  # doctest: +SKIP
            3639

            >>> checker.freq("บิญชา")  # doctest: +SKIP
            0
        """
        return self.__WORDS[word]

    def spell(self, word: str) -> list[str]:
        """Returns a list of all correctly-spelled words whose spelling
        is similar to the given word by edit distance metrics.
        The returned list of words will be sorted by decreasing
        order of word frequencies in the word spelling dictionary.

        First, if the input word is spelled correctly,
        this method returns a list of exactly one word which is itself.
        Next, this method looks for a list of all correctly spelled words
        whose edit distance value is 1 from the input word.
        If there is no such word, then the search expands to
        a list of words whose edit distance value is 2.
        And if that still fails, the list of input words is returned.

        :param str word: A word to check spelling of

        :return: list of possibly correct words within 1 or 2 edit distance
                 and sorted by frequency of word occurrence in the
                 spelling dictionary in descending order.
        :rtype: list[str]

        :Example:

            >>> from pythainlp.spell import NorvigSpellChecker  # doctest: +SKIP

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
        """Returns the most possible word, using the probability from
        the spelling dictionary

        :param str word: A word to correct spelling of

        :return: the correct spelling of the given word
        :rtype: str

        :Example:

            >>> from pythainlp.spell import NorvigSpellChecker  # doctest: +SKIP

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
