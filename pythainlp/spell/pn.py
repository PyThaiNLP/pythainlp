# -*- coding: utf-8 -*-
"""
Spell checker, using Peter Norvig algorithm.
Spelling dictionary can be customized.
Default spelling dictionary is based on Thai National Corpus.

Based on Peter Norvig's Python code from http://norvig.com/spell-correct.html
"""
from collections import Counter

from pythainlp.corpus import tnc
from pythainlp.util import is_thaichar

_THAI_CHARS = [
    "ก",
    "ข",
    "ฃ",
    "ค",
    "ฅ",
    "ฆ",
    "ง",
    "จ",
    "ฉ",
    "ช",
    "ซ",
    "ฌ",
    "ญ",
    "ฎ",
    "ฏ",
    "ฐ",
    "ฑ",
    "ฒ",
    "ณ",
    "ด",
    "ต",
    "ถ",
    "ท",
    "ธ",
    "น",
    "บ",
    "ป",
    "ผ",
    "ฝ",
    "พ",
    "ฟ",
    "ภ",
    "ม",
    "ย",
    "ร",
    "ฤ",
    "ล",
    "ฦ",
    "ว",
    "ศ",
    "ษ",
    "ส",
    "ห",
    "ฬ",
    "อ",
    "ฮ",
    "ฯ",
    "ะ",
    "ั",
    "า",
    "ำ",
    "ิ",
    "ี",
    "ึ",
    "ื",
    "ุ",
    "ู",
    "ฺ",
    "\u0e3b",
    "\u0e3c",
    "\u0e3d",
    "\u0e3e",
    "฿",
    "เ",
    "แ",
    "โ",
    "ใ",
    "ไ",
    "ๅ",
    "ๆ",
    "็",
    "่",
    "้",
    "๊",
    "๋",
    "์",
]


def _is_thai_and_not_num(word):
    for ch in word:
        if ch != "." and not is_thaichar(ch):
            return False
        if ch in "๐๑๒๓๔๕๖๗๘๙0123456789":
            return False
    return True


def _keep(wf, min_freq, min_len, max_len, condition_func):
    """
    Keep only Thai words with at least min_freq frequency
    and has length between min_len and (max_len characters
    """
    if not wf or wf[1] < min_freq:
        return False

    word = wf[0]
    if not word or len(word) < min_len or len(word) > max_len or word[0] == ".":
        return False

    return condition_func(word)


def _edits1(word):
    """
    Return a set of words with edit distance of 1 from the input word
    """
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in _THAI_CHARS]
    inserts = [L + c + R for L, R in splits for c in _THAI_CHARS]

    return set(deletes + transposes + replaces + inserts)


def _edits2(word):
    """
    Return a set of words with edit distance of 2 from the input word
    """
    return set(e2 for e1 in _edits1(word) for e2 in _edits1(e1))


class NorvigSpellChecker:
    def __init__(
        self,
        word_freqs=None,
        min_freq=2,
        min_len=2,
        max_len=40,
        condition_func=_is_thai_and_not_num,
    ):
        """
        Initialize Peter Norvig's spell checker object

        :param str word_freqs: A list of tuple (word, frequency) to create a spelling dictionary. Default is from Thai National Corpus (around 40,000 words).
        :param int min_freq: Minimum frequency of a word to keep (default = 2)
        :param int min_len: Minimum length (in characters) of a word to keep (default = 2)
        :param int max_len: Maximum length (in characters) of a word to keep (default = 40)
        """
        if not word_freqs:  # default, use Thai National Corpus
            word_freqs = tnc.get_word_frequency_all()

        # filter word list
        word_freqs = [
            wf
            for wf in word_freqs
            if _keep(wf, min_freq, min_len, max_len, condition_func)
        ]

        self.__WORDS = Counter(dict(word_freqs))
        self.__WORDS_TOTAL = sum(self.__WORDS.values())

    def dictionary(self):
        """
        Return the spelling dictionary currently used by this spell checker
        """
        return self.__WORDS.items()

    def known(self, words):
        """
        Return a list of given words that found in the spelling dictionary

        :param str words: A list of words to check if they are in the spelling dictionary
        """
        return list(w for w in words if w in self.__WORDS)

    def prob(self, word):
        """
        Return probability of an input word, according to the spelling dictionary

        :param str word: A word to check its probability of occurrence
        """
        return self.__WORDS[word] / self.__WORDS_TOTAL

    def spell(self, word):
        """
        Return a list of possible words, according to edit distance of 1 and 2,
        sorted by probability of word occurrance in the spelling dictionary

        :param str word: A word to check its spelling
        """
        if not word:
            return ""

        candidates = (
            self.known([word])
            or self.known(_edits1(word))
            or self.known(_edits2(word))
            or [word]
        )
        candidates.sort(key=self.prob, reverse=True)

        return candidates

    def correct(self, word):
        """
        Return the most possible word, using the probability from the spelling dictionary

        :param str word: A word to correct its spelling
        """
        if not word:
            return ""

        return self.spell(word)[0]


DEFAULT_SPELL_CHECKER = NorvigSpellChecker()


def dictionary():
    """
    Return the spelling dictionary currently used by this spell checker.
    The spelling dictionary is based on words found in the Thai National Corpus.
    """
    return DEFAULT_SPELL_CHECKER.dictionary()


def known(words):
    """
    Return a list of given words that found in the spelling dictionary.
    The spelling dictionary is based on words found in the Thai National Corpus.

    :param str words: A list of words to check if they are in the spelling dictionary
    """
    return DEFAULT_SPELL_CHECKER.known(words)


def prob(word):
    """
    Return probability of an input word, according to the Thai National Corpus

    :param str word: A word to check its probability of occurrence
    """
    return DEFAULT_SPELL_CHECKER.prob(word)


def spell(word):
    """
    Return a list of possible words, according to edit distance of 1 and 2,
    sorted by probability of word occurrance in the Thai National Corpus.

    :param str word: A word to check its spelling
    """
    return DEFAULT_SPELL_CHECKER.spell(word)


def correct(word):
    """
    Return the most possible word, according to probability from the Thai National Corpus

    :param str word: A word to correct its spelling
    """
    return DEFAULT_SPELL_CHECKER.correct(word)
