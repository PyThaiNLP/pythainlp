# -*- coding: utf-8 -*-
"""
Spell checker, using Peter Norvig algorithm.
Spelling dictionary can be customized.
Default spelling dictionary is based on Thai National Corpus.

Based on Peter Norvig's Python code from http://norvig.com/spell-correct.html
"""
from collections import Counter
from string import digits
from typing import Callable, List, Set, Tuple

from pythainlp import thai_digits, thai_letters
from pythainlp.corpus import tnc
from pythainlp.util import isthaichar


def _no_filter(word: str) -> bool:
    return True


def _is_thai_and_not_num(word: str) -> bool:
    for ch in word:
        if ch != "." and not isthaichar(ch):
            return False
        if ch in digits or ch in thai_digits:
            return False
    return True


def _keep(
    word_freq: int,
    min_freq: int,
    min_len: int,
    max_len: int,
    dict_filter: Callable[[str], bool],
) -> Callable[[str], bool]:
    """
    Keep only Thai words with at least min_freq frequency
    and has length between min_len and max_len characters
    """
    if not word_freq or word_freq[1] < min_freq:
        return False

    word = word_freq[0]
    if not word or len(word) < min_len or len(word) > max_len or word[0] == ".":
        return False

    return dict_filter(word)


def _edits1(word: str) -> Set[str]:
    """
    Return a set of words with edit distance of 1 from the input word
    """
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in thai_letters]
    inserts = [L + c + R for L, R in splits for c in thai_letters]

    return set(deletes + transposes + replaces + inserts)


def _edits2(word: str) -> Set[str]:
    """
    Return a set of words with edit distance of 2 from the input word
    """
    return set(e2 for e1 in _edits1(word) for e2 in _edits1(e1))


class NorvigSpellChecker:
    def __init__(
        self,
        custom_dict: List[Tuple[str, int]] = None,
        min_freq: int = 2,
        min_len: int = 2,
        max_len: int = 40,
        dict_filter: Callable[[str], bool] = _is_thai_and_not_num,
    ):
        """
        Initialize Peter Norvig's spell checker object. Spelling dictionary
        can be customized. By default, spelling dictionary is from
        `Thai National Corpus <http://www.arts.chula.ac.th/ling/tnc/>`_

        Basically, Norvig's spell checker will choose the most likely
        spelling correction give a word by searching for candidate
        corrected words based on edit distance. Then, it selects the candidate
        with the highest word occurrence probability.

        :param str custom_dict: A list of tuple (word, frequency) to create
                                a spelling dictionary. Default is from
                                Thai National Corpus (around 40,000 words).
        :param int min_freq: Minimum frequency of a word to keep (default = 2)
        :param int min_len: Minimum length (in characters) of a word to keep
                            (default = 2)
        :param int max_len: Maximum length (in characters) of a word to keep
                            (default = 40)
        :param func dict_filter: A function to filter the dictionary.
                                 Default filter removes any word
                                 with number or non-Thai characters.
                                 If no filter is required, use None.
        """
        if not custom_dict:  # default, use Thai National Corpus
            custom_dict = tnc.word_freqs()

        if not dict_filter:
            dict_filter = _no_filter

        # filter word list
        custom_dict = [
            word_freq
            for word_freq in custom_dict
            if _keep(word_freq, min_freq, min_len, max_len, dict_filter)
        ]

        self.__WORDS = Counter(dict(custom_dict))
        self.__WORDS_TOTAL = sum(self.__WORDS.values())
        if self.__WORDS_TOTAL < 1:
            self.__WORDS_TOTAL = 0

    def dictionary(self) -> List[Tuple[str, int]]:
        """
        Return the spelling dictionary currently used by this spell checker

        :return: spelling dictionary of this instance
        :rtype: list[tuple[str, int]]

        :Example:

            >>> from pythainlp.spell import NorvigSpellChecker
            >>>
            >>> dictionary= [("หวาน", 30), ("มะนาว", 2), ("แอบ", 3223)]
            >>>
            >>> _spell_checker = NorvigSpellChecker(custom_dict=dictionary)
            >>> _spell_checker.dictionary()
            dict_items([('หวาน', 30), ('มะนาว', 2), ('แอบ', 3223)])
        """
        return self.__WORDS.items()

    def known(self, words: List[str]) -> List[str]:
        """
        Return a list of given words that found in the spelling dictionary

        :param list[str] words: A list of words to check if they exist
                                in the spelling dictionary

        :return: intersection of the given words list and words
                 in the spelling dictionary
        :rtype: list[str]

        :Example:

            >>> from pythainlp.spell import NorvigSpellChecker
            >>>
            >>> _spell_checker = NorvigSpellChecker()
            >>>
            >>> _spell_checker.known(["ร้าย"])
            ['ร้าย']
            >>>
            >>> _spell_checker.known(["เพยน", "เพล", "เพลง"])
            ['เพล', 'เพลง']
            >>>
            >>> _spell_checker.known(['ยกไ', 'ไฟล์ม'])
            []
            >>>
            >>> _spell_checker.known(['])
            []
        """
        return list(w for w in words if w in self.__WORDS)

    def prob(self, word: str) -> float:
        """
        Return probability of an input word, according to
        the spelling dictionary

        :param str word: A word to check its probability of occurrence

        :return: word occurrence probability
        :rtype: float

        :Example:

            >>> from pythainlp.spell import NorvigSpellChecker
            >>>
            >>> _spell_checker = NorvigSpellChecker()
            >>> _spell_checker.prob("เส้นตรบ")
            0.0
            >>> _spell_checker.prob("ครัช")
            0.0
            >>> _spell_checker.prob("รัก")
            0.0006959172792052158
            >>> _spell_checker.prob("น่ารัก")
            9.482306849763902e-05
            >>> _spell_checker.prob("เหตุการณ์")
            0.00026403687441972634
        """
        return self.__WORDS[word] / self.__WORDS_TOTAL

    def freq(self, word: str) -> int:
        """
        Return frequency of an input word, according to the spelling dictionary

        :param str word: A word to check its frequency
        :return: frequency of the given word in the spelling dictionary
        :rtype: int

        :Example:

            >>> from pythainlp.spell import NorvigSpellChecker
            >>>
            >>> _spell_checker = NorvigSpellChecker()
            >>>
            >>> _spell_checker.freq("ปัญชา")
            0
            >>> _spell_checker.freq("ปัญญา")
            3639
            >>>
            >>> _spell_checker.freq("บิญชา")
            0
            >>> _spell_checker.freq("บัญชา")
            335
            >>>
            >>> _spell_checker.freq("มิตรภาบ")
            0
            >>> _spell_checker.freq("มิตรภาพ")
            572
            >>> _spell_checker.freq("มิตร")
            1923
        """
        return self.__WORDS[word]

    def spell(self, word: str) -> List[str]:
        """
        Return a list of possible words, according to edit distance of 1 and 2,
        sorted by frequency of word occurrance in the spelling dictionary

        :param str word: A word to check its spelling

        :return: list of possible correct words within 1 or 2 edit distance
                 and sorted by frequency of word occurence in the
                 spelling dictionary in descending order.
        :rtype: list[str]

        :Example:

            >>> from pythainlp.spell import NorvigSpellChecker
            >>>
            >>> _spell_checker = NorvigSpellChecker()
            >>>
            >>> _spell_checker.spell("เส้นตรบ")
            ['เส้นตรง']
            >>>
            >>> _spell_checker.spell("ครัช")
            ['ครับ', 'ครัว', 'รัช', 'ครัม', 'ครัน',
            'วรัช', 'ครัส', 'ปรัช', 'บรัช', 'ครัง',
            'คัช', 'คลัช', 'ครัย', 'ครัด']
            >>>
            >>> _spell_checker.spell("กระปิ")
            ['กะปิ', 'กระบิ']
        """
        if not word:
            return ""

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
        Return the most possible word, using the probability from
        the spelling dictionary

        :param str word: A word to correct its spelling

        :return: the corrrect spelling of the given word
        :rtype: str

        :Example:

            >>> from pythainlp.spell import NorvigSpellChecker
            >>>
            >>> _spell_checker = NorvigSpellChecker()
            >>> _spell_checker.correct("ปัญชา")
            'ปัญหา'
            >>> _spell_checker.correct("บิญชา")
            'บัญชา'
            >>> _spell_checker.correct("มิตรภาบ")
            'มิตรภาพ'
        """
        if not word:
            return ""

        return self.spell(word)[0]


DEFAULT_SPELL_CHECKER = NorvigSpellChecker()
