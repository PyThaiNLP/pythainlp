# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

"""Common lists of words."""

from __future__ import annotations

import ast
import warnings
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Union

__all__: list[str] = [
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


from pythainlp.corpus import get_corpus, get_corpus_as_is, get_corpus_path
from pythainlp.tools import warn_deprecation

_THAI_COUNTRIES: frozenset[str] = frozenset()
_THAI_COUNTRIES_FILENAME: str = "countries_th.txt"

_THAI_THAILAND_PROVINCES: frozenset[str] = frozenset()
_THAI_THAILAND_PROVINCES_DETAILS: list[dict[str, str]] = []
_THAI_THAILAND_PROVINCES_FILENAME: str = "thailand_provinces_th.csv"

_THAI_SYLLABLES: frozenset[str] = frozenset()
_THAI_SYLLABLES_FILENAME: str = "syllables_th.txt"

_THAI_WORDS: frozenset[str] = frozenset()
_THAI_WORDS_FILENAME: str = "words_th.txt"

_THAI_STOPWORDS: frozenset[str] = frozenset()
_THAI_STOPWORDS_FILENAME: str = "stopwords_th.txt"

_THAI_NEGATIONS: frozenset[str] = frozenset()
_THAI_NEGATIONS_FILENAME: str = "negations_th.txt"

_THAI_PROFANITY_WORDS: frozenset[str] = frozenset()
_THAI_PROFANITY_WORDS_FILENAME: str = "profanity_th.txt"

_THAI_FAMLIY_NAMES: frozenset[str] = frozenset()
_THAI_FAMLIY_NAMES_FILENAME: str = "family_names_th.txt"
_THAI_FEMALE_NAMES: frozenset[str] = frozenset()
_THAI_FEMALE_NAMES_FILENAME: str = "person_names_female_th.txt"
_THAI_MALE_NAMES: frozenset[str] = frozenset()
_THAI_MALE_NAMES_FILENAME: str = "person_names_male_th.txt"

_THAI_ORST_WORDS: frozenset[str] = frozenset()

_THAI_DICT: dict[str, list[str]] = {}
_THAI_WSD_DICT: dict[str, Union[list[str], list[list[str]]]] = {}
_THAI_SYNONYMS: dict[str, Union[list[str], list[list[str]]]] = {}


def countries() -> frozenset[str]:
    """Return a frozenset of country names in Thai such as "แคนาดา", "โรมาเนีย",
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


def provinces(
    details: bool = False,
) -> Union[frozenset[str], list[dict[str, str]]]:
    """Return a frozenset of Thailand province names in Thai such as "กระบี่",
    "กรุงเทพมหานคร", "กาญจนบุรี", and "อุบลราชธานี".
    \n(See: `dev/pythainlp/corpus/thailand_provinces_th.csv\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/thailand_provinces_th.csv>`_)

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
            # Skip completely empty or whitespace-only lines without warning.
            if not line.strip():
                continue
            parts = line.split(",")
            try:
                prov = {
                    "name_th": parts[0],
                    "abbr_th": parts[1],
                    "name_en": parts[2],
                    "abbr_en": parts[3],
                }
            except IndexError:
                warnings.warn(
                    f"Skipping malformed province entry (too few fields): {line!r}",
                    UserWarning,
                    stacklevel=2,
                )
                continue
            if not all(v.strip() for v in prov.values()):
                warnings.warn(
                    f"Skipping province entry with blank or empty field(s): {line!r}",
                    UserWarning,
                    stacklevel=2,
                )
                continue
            provs.add(prov["name_th"])
            prov_details.append(prov)

        _THAI_THAILAND_PROVINCES = frozenset(provs)
        _THAI_THAILAND_PROVINCES_DETAILS = prov_details

    if details:
        return _THAI_THAILAND_PROVINCES_DETAILS

    return _THAI_THAILAND_PROVINCES


def thai_syllables() -> frozenset[str]:
    """Return a frozenset of Thai syllables such as "กรอบ", "ก็", "๑", "โมบ",
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


def thai_words() -> frozenset[str]:
    """Return a frozenset of Thai words such as "กติกา", "กดดัน", "พิษ",
    and "พิษภัย". \n(See: `dev/pythainlp/corpus/words_th.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/words_th.txt>`_)

    :return: :class:`frozenset` containing words in the Thai language.
    :rtype: :class:`frozenset`
    """
    global _THAI_WORDS
    if not _THAI_WORDS:
        _THAI_WORDS = get_corpus(_THAI_WORDS_FILENAME)

    return _THAI_WORDS


def thai_orst_words() -> frozenset[str]:
    """Return a frozenset of Thai words from Royal Society of Thailand
    \n(See: `dev/pythainlp/corpus/orst_words_th.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/orst_words_th.txt>`_)

    :return: :class:`frozenset` containing words in the Thai language.
    :rtype: :class:`frozenset`
    """
    global _THAI_ORST_WORDS
    if not _THAI_ORST_WORDS:
        _THAI_ORST_WORDS = get_corpus("orst_words_th.txt")

    return _THAI_ORST_WORDS


def thai_stopwords() -> frozenset[str]:
    """Return a frozenset of Thai stopwords such as "มี", "ไป", "ไง", "ขณะ",
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


def thai_negations() -> frozenset[str]:
    """Return a frozenset of Thai negation words including "ไม่" and "แต่".
    \n(See: `dev/pythainlp/corpus/negations_th.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/negations_th.txt>`_)

    :return: :class:`frozenset` containing negations in the Thai language.
    :rtype: :class:`frozenset`
    """
    global _THAI_NEGATIONS
    if not _THAI_NEGATIONS:
        _THAI_NEGATIONS = get_corpus(_THAI_NEGATIONS_FILENAME)

    return _THAI_NEGATIONS


def thai_profanity_words() -> frozenset[str]:
    """Return a frozenset of Thai profanity words for content filtering.
    \n(See: `dev/pythainlp/corpus/profanity_th.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/profanity_th.txt>`_)

    :return: :class:`frozenset` containing profanity words in the Thai language.
    :rtype: :class:`frozenset`
    """
    global _THAI_PROFANITY_WORDS
    if not _THAI_PROFANITY_WORDS:
        _THAI_PROFANITY_WORDS = get_corpus(
            _THAI_PROFANITY_WORDS_FILENAME, comments=False
        )

    return _THAI_PROFANITY_WORDS


def thai_family_names() -> frozenset[str]:
    """Return a frozenset of Thai family names
    \n(See: `dev/pythainlp/corpus/family_names_th.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/family_names_th.txt>`_)

    :return: :class:`frozenset` containing Thai family names.
    :rtype: :class:`frozenset`
    """
    global _THAI_FAMLIY_NAMES
    if not _THAI_FAMLIY_NAMES:
        _THAI_FAMLIY_NAMES = get_corpus(_THAI_FAMLIY_NAMES_FILENAME)

    return _THAI_FAMLIY_NAMES


def thai_female_names() -> frozenset[str]:
    """Return a frozenset of Thai female names
    \n(See: `dev/pythainlp/corpus/person_names_female_th.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/person_names_female_th.txt>`_)

    :return: :class:`frozenset` containing Thai female names.
    :rtype: :class:`frozenset`
    """
    global _THAI_FEMALE_NAMES
    if not _THAI_FEMALE_NAMES:
        _THAI_FEMALE_NAMES = get_corpus(_THAI_FEMALE_NAMES_FILENAME)

    return _THAI_FEMALE_NAMES


def thai_male_names() -> frozenset[str]:
    """Return a frozenset of Thai male names
    \n(See: `dev/pythainlp/corpus/person_names_male_th.txt\
    <https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/person_names_male_th.txt>`_)

    :return: :class:`frozenset` containing Thai male names.
    :rtype: :class:`frozenset`
    """
    global _THAI_MALE_NAMES
    if not _THAI_MALE_NAMES:
        _THAI_MALE_NAMES = get_corpus(_THAI_MALE_NAMES_FILENAME)

    return _THAI_MALE_NAMES


def thai_dict() -> dict[str, list[str]]:
    """Return Thai dictionary with definition from wiktionary.
    \n(See: `thai_dict\
    <https://pythainlp.org/pythainlp-corpus/thai_dict.html>`_)

    :return: Thai words with part-of-speech type and definition
    :rtype: dict
    """
    global _THAI_DICT
    if _THAI_DICT:
        return _THAI_DICT

    import csv

    path = get_corpus_path("thai_dict")
    if not path:
        return _THAI_DICT
    path = str(path)

    words: list[str] = []
    meanings: list[str] = []
    with open(path, newline="\n", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            word = row.get("word")
            meaning = row.get("meaning")
            if not (word and word.strip() and meaning and meaning.strip()):
                warnings.warn(
                    f"Skipping thai_dict entry with missing or empty field(s): {dict(row)!r}",
                    UserWarning,
                    stacklevel=2,
                )
                continue
            words.append(word)
            meanings.append(meaning)
    _THAI_DICT = {"word": words, "meaning": meanings}

    return _THAI_DICT


def thai_wsd_dict() -> dict[str, Union[list[str], list[list[str]]]]:
    """Return Thai Word Sense Disambiguation dictionary with definition from wiktionary.
    \n(See: `thai_dict\
    <https://pythainlp.org/pythainlp-corpus/thai_dict.html>`_)

    :return: Thai words with part-of-speech type and definition
    :rtype: dict
    """
    global _THAI_WSD_DICT
    if _THAI_WSD_DICT:
        return _THAI_WSD_DICT

    thai_wsd = thai_dict()
    words: list[str] = []
    meanings: list[list[str]] = []
    for word, meaning in zip(thai_wsd["word"], thai_wsd["meaning"]):
        try:
            parsed = ast.literal_eval(meaning)
        except (SyntaxError, TypeError, ValueError):
            warnings.warn(
                f"Skipping thai_wsd_dict entry for word {word!r}: "
                f"meaning could not be parsed: {meaning!r}",
                UserWarning,
                stacklevel=2,
            )
            continue
        if not isinstance(parsed, dict):
            warnings.warn(
                f"Skipping thai_wsd_dict entry for word {word!r}: "
                f"expected dict after parsing, got {type(parsed).__name__!r}",
                UserWarning,
                stacklevel=2,
            )
            continue
        senses: list[str] = []
        for sense_list in parsed.values():
            senses.extend(sense_list)
        senses = list(set(senses))
        if len(senses) > 1:
            words.append(word)
            meanings.append(senses)
    _THAI_WSD_DICT = {"word": words, "meaning": meanings}
    return _THAI_WSD_DICT


def thai_synonyms() -> dict[str, Union[list[str], list[list[str]]]]:
    """Return Thai synonyms.
    \n(See: `thai_synonym\
    <https://pythainlp.org/pythainlp-corpus/thai_synonym.html>`_)

    :return: Thai words with part-of-speech type and synonym
    :rtype: dict
    """
    global _THAI_SYNONYMS
    if _THAI_SYNONYMS:
        return _THAI_SYNONYMS

    import csv

    path = get_corpus_path("thai_synonym")
    if not path:
        return _THAI_SYNONYMS
    path = str(path)

    words: list[str] = []
    pos_tags: list[str] = []
    synonym_groups: list[list[str]] = []
    with open(path, newline="\n", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            word = row.get("word")
            pos = row.get("pos")
            synonym = row.get("synonym")
            if not (
                word
                and word.strip()
                and pos
                and pos.strip()
                and synonym
                and synonym.strip()
            ):
                warnings.warn(
                    f"Skipping thai_synonyms entry with missing or empty field(s): {dict(row)!r}",
                    UserWarning,
                    stacklevel=2,
                )
                continue
            words.append(word)
            pos_tags.append(pos)
            synonym_groups.append(synonym.split("|"))
    _THAI_SYNONYMS = {
        "word": words,
        "pos": pos_tags,
        "synonym": synonym_groups,
    }
    return _THAI_SYNONYMS


def thai_synonym() -> dict[str, Union[list[str], list[list[str]]]]:
    warn_deprecation(
        "pythainlp.corpus.thai_synonym",
        "pythainlp.corpus.thai_synonyms",
        "5.1",
        "5.2",
    )
    return thai_synonyms()


def find_synonyms(word: str) -> list[str]:
    """Find synonyms

    :param str word: Thai word
    :return: list of synonyms of the input word, or an empty list if none exist.
    :rtype: list[str]

    :Example:

        >>> from pythainlp.corpus import find_synonyms  # doctest: +SKIP
        >>> print(find_synonyms("หมู"))  # doctest: +SKIP
        ['จรุก', 'วราหะ', 'วราห์', 'ศูกร', 'สุกร']
    """
    synonyms = thai_synonyms()  # get a dictionary of {word, synonym}
    list_synonym: list[Any] = []

    if word in synonyms["word"]:  # find by word
        word_list = synonyms["word"]
        if isinstance(word_list, list):
            list_synonym.extend(synonyms["synonym"][word_list.index(word)])  # type: ignore[arg-type]

    for idx, words in enumerate(synonyms["synonym"]):  # find by synonym
        if word in words:
            list_synonym.extend(synonyms["synonym"][idx])
            list_synonym.append(synonyms["word"][idx])

    list_synonym = sorted(set(list_synonym))

    if word in list_synonym:  # remove same word
        list_synonym.remove(word)

    return list_synonym
