# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0

"""
Common lists of words.
"""

__all__ = [
    "countries",
    "find_synonyms",
    "provinces",
    "thai_family_names",
    "thai_female_names",
    "thai_male_names",
    "thai_negations",
    "thai_dict",
    "thai_stopwords",
    "thai_syllables",
    "thai_synonym",
    "thai_synonyms",
    "thai_words",
    "thai_wsd_dict",
]

from typing import FrozenSet, List, Union
import warnings

from pythainlp.corpus import get_corpus, get_corpus_as_is, get_corpus_path

_THAI_COUNTRIES: FrozenSet[str] = frozenset()
_THAI_COUNTRIES_FILENAME = "countries_th.txt"

_THAI_THAILAND_PROVINCES: FrozenSet[str] = frozenset()
_THAI_THAILAND_PROVINCES_DETAILS: List[dict] = []
_THAI_THAILAND_PROVINCES_FILENAME = "thailand_provinces_th.csv"

_THAI_SYLLABLES: FrozenSet[str] = frozenset()
_THAI_SYLLABLES_FILENAME = "syllables_th.txt"

_THAI_WORDS: FrozenSet[str] = frozenset()
_THAI_WORDS_FILENAME = "words_th.txt"

_THAI_STOPWORDS: FrozenSet[str] = frozenset()
_THAI_STOPWORDS_FILENAME = "stopwords_th.txt"

_THAI_NEGATIONS: FrozenSet[str] = frozenset()
_THAI_NEGATIONS_FILENAME = "negations_th.txt"

_THAI_FAMLIY_NAMES: FrozenSet[str] = frozenset()
_THAI_FAMLIY_NAMES_FILENAME = "family_names_th.txt"
_THAI_FEMALE_NAMES: FrozenSet[str] = frozenset()
_THAI_FEMALE_NAMES_FILENAME = "person_names_female_th.txt"
_THAI_MALE_NAMES: FrozenSet[str] = frozenset()
_THAI_MALE_NAMES_FILENAME = "person_names_male_th.txt"

_THAI_ORST_WORDS: FrozenSet[str] = frozenset()

_THAI_DICT = {}
_THAI_WSD_DICT = {}
_THAI_SYNONYMS = {}


def countries() -> FrozenSet[str]:
    """
    Return a frozenset of country names in Thai such as "แคนาดา", "โรมาเนีย",
    "แอลจีเรีย", and "ลาว".
    \n(See: `dev/pythainlp/corpus/countries_th.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/countries_th.txt>`_)

    :return: :class:`frozenset` containing country names in Thai
    :rtype: :class:`frozenset`
    """
    global _THAI_COUNTRIES
    if not _THAI_COUNTRIES:
        _THAI_COUNTRIES = get_corpus(_THAI_COUNTRIES_FILENAME)

    return _THAI_COUNTRIES


def provinces(details: bool = False) -> Union[FrozenSet[str], List[dict]]:
    """
    Return a frozenset of Thailand province names in Thai such as "กระบี่",
    "กรุงเทพมหานคร", "กาญจนบุรี", and "อุบลราชธานี".
    \n(See: `dev/pythainlp/corpus/thailand_provinces_th.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/thailand_provinces_th.txt>`_)

    :param bool details: return details of provinces or not

    :return: :class:`frozenset` containing province names of Thailand \
    (if details is False) or :class:`list` containing :class:`dict` of \
    province names and details such as \
    [{'name_th': 'นนทบุรี', 'abbr_th': 'นบ', 'name_en': 'Nonthaburi', \
    'abbr_en': 'NBI'}].
    :rtype: :class:`frozenset` or :class:`list`
    """
    global _THAI_THAILAND_PROVINCES, _THAI_THAILAND_PROVINCES_DETAILS

    if not _THAI_THAILAND_PROVINCES or not _THAI_THAILAND_PROVINCES_DETAILS:
        provs = set()
        prov_details = []

        for line in get_corpus_as_is(_THAI_THAILAND_PROVINCES_FILENAME):
            p = line.split(",")

            prov = {}
            prov["name_th"] = p[0]
            prov["abbr_th"] = p[1]
            prov["name_en"] = p[2]
            prov["abbr_en"] = p[3]

            provs.add(prov["name_th"])
            prov_details.append(prov)

        _THAI_THAILAND_PROVINCES = frozenset(provs)
        _THAI_THAILAND_PROVINCES_DETAILS = prov_details

    if details:
        return _THAI_THAILAND_PROVINCES_DETAILS

    return _THAI_THAILAND_PROVINCES


def thai_syllables() -> FrozenSet[str]:
    """
    Return a frozenset of Thai syllables such as "กรอบ", "ก็", "๑", "โมบ",
    "โมน", "โม่ง", "กา", "ก่า", and, "ก้า".
    \n(See: `dev/pythainlp/corpus/syllables_th.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/syllables_th.txt>`_)
    We use the Thai syllable list from `KUCut <https://github.com/Thanabhat/KUCut>`_.

    :return: :class:`frozenset` containing syllables in the Thai language.
    :rtype: :class:`frozenset`
    """
    global _THAI_SYLLABLES
    if not _THAI_SYLLABLES:
        _THAI_SYLLABLES = get_corpus(_THAI_SYLLABLES_FILENAME)

    return _THAI_SYLLABLES


def thai_words() -> FrozenSet[str]:
    """
    Return a frozenset of Thai words such as "กติกา", "กดดัน", "พิษ",
    and "พิษภัย". \n(See: `dev/pythainlp/corpus/words_th.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/words_th.txt>`_)

    :return: :class:`frozenset` containing words in the Thai language.
    :rtype: :class:`frozenset`
    """
    global _THAI_WORDS
    if not _THAI_WORDS:
        _THAI_WORDS = get_corpus(_THAI_WORDS_FILENAME)

    return _THAI_WORDS


def thai_orst_words() -> FrozenSet[str]:
    """
    Return a frozenset of Thai words from Royal Society of Thailand
    \n(See: `dev/pythainlp/corpus/thai_orst_words.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/orst_words_th.txt>`_)

    :return: :class:`frozenset` containing words in the Thai language.
    :rtype: :class:`frozenset`
    """
    global _THAI_ORST_WORDS
    if not _THAI_ORST_WORDS:
        _THAI_ORST_WORDS = get_corpus("orst_words_th.txt")

    return _THAI_ORST_WORDS


def thai_stopwords() -> FrozenSet[str]:
    """
    Return a frozenset of Thai stopwords such as "มี", "ไป", "ไง", "ขณะ",
    "การ", and "ประการหนึ่ง". \n(See: `dev/pythainlp/corpus/stopwords_th.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/stopwords_th.txt>`_)
    We use stopword lists by thesis's เพ็ญศิริ ลี้ตระกูล.

    :See Also:

    เพ็ญศิริ ลี้ตระกูล . \
    การเลือกประโยคสำคัญในการสรุปความภาษาไทยโดยใช้แบบจำลองแบบลำดับชั้น. \
    กรุงเทพมหานคร : มหาวิทยาลัยธรรมศาสตร์; 2551.

    :return: :class:`frozenset` containing stopwords.
    :rtype: :class:`frozenset`
    """
    global _THAI_STOPWORDS
    if not _THAI_STOPWORDS:
        _THAI_STOPWORDS = get_corpus(_THAI_STOPWORDS_FILENAME)

    return _THAI_STOPWORDS


def thai_negations() -> FrozenSet[str]:
    """
    Return a frozenset of Thai negation words including "ไม่" and "แต่".
    \n(See: `dev/pythainlp/corpus/negations_th.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/negations_th.txt>`_)

    :return: :class:`frozenset` containing negations in the Thai language.
    :rtype: :class:`frozenset`
    """
    global _THAI_NEGATIONS
    if not _THAI_NEGATIONS:
        _THAI_NEGATIONS = get_corpus(_THAI_NEGATIONS_FILENAME)

    return _THAI_NEGATIONS


def thai_family_names() -> FrozenSet[str]:
    """
    Return a frozenset of Thai family names
    \n(See: `dev/pythainlp/corpus/family_names_th.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/family_names_th.txt>`_)

    :return: :class:`frozenset` containing Thai family names.
    :rtype: :class:`frozenset`
    """
    global _THAI_FAMLIY_NAMES
    if not _THAI_FAMLIY_NAMES:
        _THAI_FAMLIY_NAMES = get_corpus(_THAI_FAMLIY_NAMES_FILENAME)

    return _THAI_FAMLIY_NAMES


def thai_female_names() -> FrozenSet[str]:
    """
    Return a frozenset of Thai female names
    \n(See: `dev/pythainlp/corpus/person_names_female_th.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/person_names_female_th.txt>`_)

    :return: :class:`frozenset` containing Thai female names.
    :rtype: :class:`frozenset`
    """
    global _THAI_FEMALE_NAMES
    if not _THAI_FEMALE_NAMES:
        _THAI_FEMALE_NAMES = get_corpus(_THAI_FEMALE_NAMES_FILENAME)

    return _THAI_FEMALE_NAMES


def thai_male_names() -> FrozenSet[str]:
    """
    Return a frozenset of Thai male names
    \n(See: `dev/pythainlp/corpus/person_names_male_th.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/person_names_male_th.txt>`_)

    :return: :class:`frozenset` containing Thai male names.
    :rtype: :class:`frozenset`
    """
    global _THAI_MALE_NAMES
    if not _THAI_MALE_NAMES:
        _THAI_MALE_NAMES = get_corpus(_THAI_MALE_NAMES_FILENAME)

    return _THAI_MALE_NAMES


def thai_dict() -> dict:
    """
    Return Thai dictionary with definition from wiktionary.
    \n(See: `thai_dict\
    <https://pythainlp.github.io/pythainlp-corpus/thai_dict.html>`_)

    :return: Thai words with part-of-speech type and definition
    :rtype: dict
    """
    global _THAI_DICT
    if not _THAI_DICT:
        import csv

        _THAI_DICT = {"word": [], "meaning": []}
        with open(
            get_corpus_path("thai_dict"), newline="\n", encoding="utf-8"
        ) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            for row in reader:
                _THAI_DICT["word"].append(row["word"])
                _THAI_DICT["meaning"].append(row["meaning"])

    return _THAI_DICT


def thai_wsd_dict() -> dict:
    """
    Return Thai Word Sense Disambiguation dictionary with definition from wiktionary.
    \n(See: `thai_dict\
    <https://pythainlp.github.io/pythainlp-corpus/thai_dict.html>`_)

    :return: Thai words with part-of-speech type and definition
    :rtype: dict
    """
    global _THAI_WSD_DICT
    if not _THAI_WSD_DICT:
        _thai_wsd = thai_dict()
        _THAI_WSD_DICT = {"word": [], "meaning": []}
        for i, j in zip(_thai_wsd["word"], _thai_wsd["meaning"]):
            _all_value = list(eval(j).values())
            _use = []
            for k in _all_value:
                _use.extend(k)
            _use = list(set(_use))
            if len(_use) > 1:
                _THAI_WSD_DICT["word"].append(i)
                _THAI_WSD_DICT["meaning"].append(_use)

    return _THAI_WSD_DICT


def thai_synonyms() -> dict:
    """
    Return Thai synonyms.
    \n(See: `thai_synonym\
    <https://pythainlp.github.io/pythainlp-corpus/thai_synonym.html>`_)

    :return: Thai words with part-of-speech type and synonym
    :rtype: dict
    """
    global _THAI_SYNONYMS
    if not _THAI_SYNONYMS:
        import csv

        _THAI_SYNONYMS = {"word": [], "pos": [], "synonym": []}
        with open(
            get_corpus_path("thai_synonym"), newline="\n", encoding="utf-8"
        ) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            for row in reader:
                _THAI_SYNONYMS["word"].append(row["word"])
                _THAI_SYNONYMS["pos"].append(row["pos"])
                _THAI_SYNONYMS["synonym"].append(row["synonym"].split("|"))

    return _THAI_SYNONYMS


def thai_synonym() -> dict:
    warnings.warn("Deprecated: Use thai_synonyms() instead.", DeprecationWarning)
    return thai_synonyms()


def find_synonyms(word: str) -> List[str]:
    """
    Find synonyms

    :param str word: Thai word
    :return: List of synonyms of the input word or an empty list if it isn't exist.
    :rtype: List[str]

    :Example:
    ::

        from pythainlp.corpus import find_synonyms

        print(find_synonyms("หมู"))
        # output: ['จรุก', 'วราหะ', 'วราห์', 'ศูกร', 'สุกร']
    """
    synonyms = thai_synonyms()  # get a dictionary of {word, synonym}
    list_synonym = []

    if word in synonyms["word"]:  # find by word
        list_synonym.extend(synonyms["synonym"][synonyms["word"].index(word)])

    for idx, words in enumerate(synonyms["synonym"]):  # find by synonym
        if word in words:
            list_synonym.extend(synonyms["synonym"][idx])
            list_synonym.append(synonyms["word"][idx])

    list_synonym = sorted(list(set(list_synonym)))

    if word in list_synonym:  # remove same word
        list_synonym.remove(word)

    return list_synonym
