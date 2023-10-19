# -*- coding: utf-8 -*-
"""
Spell checker, using Peter Norvig algorithm.
Spelling dictionary can be customized.
Default spelling dictionary is based on Thai National Corpus.

Based on Peter Norvig's Python code from http://norvig.com/spell-correct.html
"""
from collections import Counter
from string import digits
from typing import (
    Callable,
    Dict,
    ItemsView,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

from pythainlp import thai_digits, thai_letters
from pythainlp.corpus import tnc
from pythainlp.util import isthaichar


def _no_filter(word: str) -> bool:
    return True


def _is_thai_and_not_num(word: str) -> bool:
    for ch in word:
        if ch != "." and not isthaichar(ch):
            return False
        if ch in thai_digits or ch in digits:
            return False
    return True


def _keep(
    word_freq: Tuple[str, int],
    min_freq: int,
    min_len: int,
    max_len: int,
    dict_filter: Callable[[str], bool],
) -> bool:
    """
    Checks whether a given word has the required minimum frequency min_freq
    and its character length is between min_len and max_len (inclusive).
    """
    if not word_freq or word_freq[1] < min_freq:
        return False

    word = word_freq[0]
    if not (word and min_len <= len(word) <= max_len and word[0] != "."):
        return False

    return dict_filter(word)


def _edits1(word: str) -> Set[str]:
    """
    Returns a set of words with an edit distance of 1 from the input word
    """
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in thai_letters]
    inserts = [L + c + R for L, R in splits for c in thai_letters]

    return set(deletes + transposes + replaces + inserts)


def _edits2(word: str) -> Set[str]:
    """
    Returns a set of words with an edit distance of 2 from the input word
    """
    return set(e2 for e1 in _edits1(word) for e2 in _edits1(e1))


def _convert_custom_dict(
    custom_dict: Union[
        Dict[str, int], Iterable[str], Iterable[Tuple[str, int]]
    ],
    min_freq: int,
    min_len: int,
    max_len: int,
    dict_filter: Optional[Callable[[str], bool]],
) -> List[Tuple[str, int]]:
    """
    Converts a custom dictionary to a list of (str, int) tuples
    """
    if isinstance(custom_dict, dict):
        custom_dict = list(custom_dict.items())

    i = iter(custom_dict)
    first_member = next(i)
    if isinstance(first_member, str):
        # create tuples of a word with frequency equaling 1,
        # and filter word list
        custom_dict = [
            (word, 1)
            for word in custom_dict
            if _keep((word, 1), 1, min_len, max_len, dict_filter)
        ]
    elif isinstance(first_member, tuple):
        # filter word list
        custom_dict = [
            word_freq
            for word_freq in custom_dict
            if _keep(word_freq, min_freq, min_len, max_len, dict_filter)
        ]
    else:
        raise TypeError(
            "custom_dict must be either Dict[str, int], "
            "Iterable[Tuple[str, int]], or Iterable[str]"
        )

    return custom_dict


class NorvigSpellChecker:
    def __init__(
        self,
        custom_dict: Union[
            Dict[str, int], Iterable[str], Iterable[Tuple[str, int]]
        ] = None,
        min_freq: int = 2,
        min_len: int = 2,
        max_len: int = 40,
        dict_filter: Optional[Callable[[str], bool]] = _is_thai_and_not_num,
    ):
        """
        Initializes Peter Norvig's spell checker object.
        Spelling dictionary can be customized.
        By default, spelling dictionary is from
        `Thai National Corpus <http://www.arts.chula.ac.th/ling/tnc/>`_

        Basically, Norvig's spell checker will choose the most likely
        corrected spelling given a word by searching for candidates of
        corrected words based on edit distance.
        Then, it selects the candidate with
        the highest word occurrence probability.

        :param str custom_dict: A custom spelling dictionary. This can be:
                                (1) a dictionary (`dict`), with words (`str`)
                                    as keys and frequencies (`int`) as values;
                                (2) an iterable (list, tuple, or set) of words
                                    (`str`) and frequency (`int`) tuples:
                                    `(str, int)`; or
                                (3) an iterable of just words (`str`), without
                                    frequencies -- in this case `1` will be
                                    assigned to every words.
                                Default is from Thai National Corpus (around
                                40,000 words).
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
        if not custom_dict:  # default, use Thai National Corpus
            # TODO: #680 change the dict
            custom_dict = [(i, j) for i, j in tnc.word_freqs()]

        if not dict_filter:
            dict_filter = _no_filter

        custom_dict = _convert_custom_dict(
            custom_dict, min_freq, min_len, max_len, dict_filter
        )

        self.__WORDS = Counter(dict(custom_dict))
        self.__WORDS += Counter()  # remove zero and negative counts
        self.__WORDS_TOTAL = sum(self.__WORDS.values())

    def dictionary(self) -> ItemsView[str, int]:
        """
        Returns the spelling dictionary currently used by this spell checker

        :return: spelling dictionary of this instance
        :rtype: list[tuple[str, int]]

        :Example:
        ::

            from pythainlp.spell import NorvigSpellChecker

            dictionary= [("หวาน", 30), ("มะนาว", 2), ("แอบ", 3223)]

            checker = NorvigSpellChecker(custom_dict=dictionary)
            checker.dictionary()
            # output: dict_items([('หวาน', 30), ('มะนาว', 2), ('แอบ', 3223)])
        """
        return self.__WORDS.items()

    def known(self, words: Iterable[str]) -> List[str]:
        """
        Returns a list of given words found in the spelling dictionary

        :param list[str] words: A list of words to check if they exist
                                in the spelling dictionary

        :return: intersection of the given word list and words
                 in the spelling dictionary
        :rtype: list[str]

        :Example:
        ::

            from pythainlp.spell import NorvigSpellChecker

            checker = NorvigSpellChecker()

            checker.known(["เพยน", "เพล", "เพลง"])
            # output: ['เพล', 'เพลง']

            checker.known(['ยกไ', 'ไฟล์ม'])
            # output: []

            checker.known([])
            # output: []
        """
        return list(w for w in words if w in self.__WORDS)

    def prob(self, word: str) -> float:
        """
        Returns the probability of an input word,
        according to the spelling dictionary

        :param str word: A word to check occurrence probability of

        :return: word occurrence probability
        :rtype: float

        :Example:
        ::

            from pythainlp.spell import NorvigSpellChecker

            checker = NorvigSpellChecker()

            checker.prob("ครัช")
            # output: 0.0

            checker.prob("รัก")
            # output: 0.0006959172792052158

            checker.prob("น่ารัก")
            # output: 9.482306849763902e-05
        """
        return self.__WORDS[word] / self.__WORDS_TOTAL

    def freq(self, word: str) -> int:
        """
        Returns the frequency of an input word,
        according to the spelling dictionary

        :param str word: A word to check frequency of
        :return: frequency of the given word in the spelling dictionary
        :rtype: int

        :Example:
        ::

            from pythainlp.spell import NorvigSpellChecker

            checker = NorvigSpellChecker()

            checker.freq("ปัญญา")
            # output: 3639

            checker.freq("บิญชา")
            # output: 0
        """
        return self.__WORDS[word]

    def spell(self, word: str) -> List[str]:
        """
        Returns a list of all correctly-spelled words whose spelling
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
        ::

            from pythainlp.spell import NorvigSpellChecker

            checker = NorvigSpellChecker()

            checker.spell("เส้นตรบ")
            # output: ['เส้นตรง']

            checker.spell("ครัช")
            # output: ['ครับ', 'ครัว', 'รัช', 'ครัม', 'ครัน',
            # 'วรัช', 'ครัส', 'ปรัช', 'บรัช', 'ครัง',
            #'คัช', 'คลัช', 'ครัย', 'ครัด']
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
        Returns the most possible word, using the probability from
        the spelling dictionary

        :param str word: A word to correct spelling of

        :return: the correct spelling of the given word
        :rtype: str

        :Example:
        ::

            from pythainlp.spell import NorvigSpellChecker

            checker = NorvigSpellChecker()

            checker.correct("ปัญชา")
            # output: 'ปัญหา'

            checker.correct("บิญชา")
            # output: 'บัญชา'

            checker.correct("มิตรภาบ")
            # output: 'มิตรภาพ'
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
