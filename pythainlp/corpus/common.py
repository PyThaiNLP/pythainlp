# -*- coding: utf-8 -*-

from pythainlp.corpus import get_corpus

__all__ = [
    "countries",
    "provinces",
    "thai_negations",
    "thai_stopwords",
    "thai_syllables",
    "thai_words",
]


_THAI_COUNTRIES = set()
_THAI_COUNTRIES_FILENAME = "countries_th.txt"

_THAI_THAILAND_PROVINCES = set()
_THAI_THAILAND_PROVINCES_FILENAME = "thailand_provinces_th.txt"

_THAI_SYLLABLES = set()
_THAI_SYLLABLES_FILENAME = "syllables_th.txt"

_THAI_WORDS = set()
_THAI_WORDS_FILENAME = "words_th.txt"

_THAI_STOPWORDS = set()
_THAI_STOPWORDS_FILENAME = "stopwords_th.txt"

_THAI_NEGATIONS = set()
_THAI_NEGATIONS_FILENAME = "negations_th.txt"


def countries() -> frozenset:
    """
    Return a frozenset of country names in Thai such as "แคนาดา", "โรมาเนีย", "แอลจีเรีย", and "ลาว".
    \n(See: `2.0/pythainlp/corpus/countries_th.txt <https://github.com/PyThaiNLP/pythainlp/blob/2.0/pythainlp/corpus/countries_th.txt>`_)

    :return: :class:`frozenset` containing countries names in Thai
    :rtype: :class:`frozenset`
    """
    global _THAI_COUNTRIES
    if not _THAI_COUNTRIES:
        _THAI_COUNTRIES = get_corpus(_THAI_COUNTRIES_FILENAME)

    return _THAI_COUNTRIES


def provinces() -> frozenset:
    """
    Return a frozenset of Thailand province names in Thai such as "กระบี่", "กรุงเทพมหานคร", "กาญจนบุรี", and "อุบลราชธานี".
    \n(See: `2.0/pythainlp/corpus/thailand_provinces_th.txt <https://github.com/PyThaiNLP/pythainlp/blob/2.0/pythainlp/corpus/thailand_provinces_th.txt>`_)
    
    :return: :class:`frozenset` containing province names of Thailand
    :rtype: :class:`frozenset`
    """
    global _THAI_THAILAND_PROVINCES
    if not _THAI_THAILAND_PROVINCES:
        _THAI_THAILAND_PROVINCES = get_corpus(_THAI_THAILAND_PROVINCES_FILENAME)

    return _THAI_THAILAND_PROVINCES


def thai_syllables() -> frozenset:
    """
    Return a frozenset of Thai syllables such as "กรอบ", "ก็", "๑", "โมบ", "โมน", "โม่ง", "กา", "ก่า", and, "ก้า".
    \n(See: `2.0/pythainlp/corpus/syllables_th.txt <https://github.com/PyThaiNLP/pythainlp/blob/2.0/pythainlp/corpus/syllables_th.txt>`_)

    :return: :class:`frozenset` containing syllables in Thai language.
    :rtype: :class:`frozenset`
    """
    global _THAI_SYLLABLES
    if not _THAI_SYLLABLES:
        _THAI_SYLLABLES = get_corpus(_THAI_SYLLABLES_FILENAME)

    return _THAI_SYLLABLES


def thai_words() -> frozenset:
    """
    Return a frozenset of Thai words
    """
    global _THAI_WORDS
    if not _THAI_WORDS:
        _THAI_WORDS = get_corpus(_THAI_WORDS_FILENAME)

    return _THAI_WORDS


def thai_stopwords() -> frozenset:
    """
    Return a frozenset of Thai stopwords
    """
    global _THAI_STOPWORDS
    if not _THAI_STOPWORDS:
        _THAI_STOPWORDS = get_corpus(_THAI_STOPWORDS_FILENAME)

    return _THAI_STOPWORDS


def thai_negations() -> frozenset:
    """
    Return a frozenset of Thai negation words
    """
    global _THAI_NEGATIONS
    if not _THAI_NEGATIONS:
        _THAI_NEGATIONS = get_corpus(_THAI_NEGATIONS_FILENAME)

    return _THAI_NEGATIONS
