# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
NLTK WordNet wrapper.

The API is the same as the NLTK WordNet API, except that the *lang*
(language) argument is "tha" (Thai) by default.

For more on usage, see NLTK Howto:
https://www.nltk.org/howto/wordnet.html
"""

from __future__ import annotations

import re
from typing import IO, TYPE_CHECKING, Optional, Union, cast

if TYPE_CHECKING:
    from collections.abc import Iterable

import nltk


def _omw_package(nltk_version: str) -> str:
    """
    Return the Open Multilingual Wordnet (OMW) package of an NLTK version.

    :param str nltk_version: NLTK version, such as ``"3.10.3"`` or
        ``"3.9.0rc1"``
    :return: ``"omw-2.0"`` for NLTK 3.10 or later, ``"omw-1.4"`` for
        NLTK 3.6.6 to 3.9, ``"omw"`` for older versions
    :rtype: str
    """
    match = re.match(r"(\d+)\.(\d+)(?:\.(\d+))?", nltk_version)
    if match is None:
        return "omw-2.0"
    version = tuple(int(x or 0) for x in match.groups())
    if version >= (3, 10):
        return "omw-2.0"
    if version >= (3, 6, 6):
        return "omw-1.4"
    return "omw"


def _ensure_corpus(package: str) -> None:
    """
    Download an NLTK corpus package unless it is already installed.

    NLTK keeps a package either unzipped or as ``<package>.zip``.

    :param str package: NLTK package name
    """
    for resource in (f"corpora/{package}", f"corpora/{package}.zip"):
        try:
            nltk.data.find(resource)
            return
        except LookupError:
            pass
    nltk.download(package)


_ensure_corpus(_omw_package(nltk.__version__))
_ensure_corpus("wordnet")

from nltk.corpus import wordnet

# Runtime import keeps typing.get_type_hints() working on this module.
from nltk.corpus.reader.wordnet import (  # noqa: TC002
    Lemma,
    Synset,
)


def synsets(
    word: str, pos: Optional[str] = None, lang: str = "tha"
) -> list[Synset]:
    """
    Return the synonym sets (synsets) of all lemmas of a word.

    The function can constrain the part of speech of the word.

    :param str word: word to find synsets of
    :param Optional[str] pos: part-of-speech (POS) tag to constrain the
        search (*n* for noun, *v* for verb, *a* for adjective, *s* for
        adjective satellite, and *r* for adverb; default is None)
    :param str lang: language code, such as *eng* or *tha*
        (default is *tha*)
    :return: synsets of all lemmas of the word, constrained by *pos*
    :rtype: list[nltk.corpus.reader.wordnet.Synset]

    :Example:

        >>> from pythainlp.corpus.wordnet import synsets
        >>>
        >>> synsets("ทำงาน")
        [Synset('function.v.01'), Synset('work.v.02'),
         Synset('work.v.01'), Synset('work.v.08')]
        >>>
        >>> synsets("บ้าน", lang="tha")
        [Synset('duplex_house.n.01'), Synset('dwelling.n.01'),
         Synset('house.n.01'), Synset('family.n.01'), Synset('home.n.03'),
         Synset('base.n.14'), Synset('home.n.01'),
         Synset('houseful.n.01'), Synset('home.n.07')]

        When specifying the constraint of the part of speech. For example,
        the word "แรง" could be interpreted as force (n.) or hard (adj.).

        >>> from pythainlp.corpus.wordnet import synsets
        >>> # By default, allow all parts of speech
        >>> synsets("แรง", lang="tha")
        >>>
        >>> # only Noun
        >>> synsets("แรง", pos="n", lang="tha")
        [Synset('force.n.03'), Synset('force.n.02')]
        >>>
        >>> # only Adjective
        >>> synsets("แรง", pos="a", lang="tha")
        [Synset('hard.s.10'), Synset('strong.s.02')]
    """
    return cast(
        "list[Synset]", wordnet.synsets(lemma=word, pos=pos, lang=lang)
    )


def synset(name_synsets: str) -> Synset:
    """
    Return the synonym set (synset) of a given name.

    The name looks like "dog.n.01" or "chase.v.01".

    :param str name_synsets: name of the synset
    :return: synset of the given name
    :rtype: nltk.corpus.reader.wordnet.Synset

    :Example:

        >>> from pythainlp.corpus.wordnet import synset
        >>>
        >>> difficult = synset("difficult.a.01")
        >>> difficult
        Synset('difficult.a.01')
        >>>
        >>> difficult.definition()
        'not easy; requiring great physical or mental effort to accomplish
                   or comprehend or endure'
    """
    return wordnet.synset(name_synsets)


def all_lemma_names(pos: Optional[str] = None, lang: str = "tha") -> list[str]:
    """
    Return all lemma names of all synsets of a part of speech and language.

    If *pos* is not specified, the function uses all synsets of all parts
    of speech.

    :param Optional[str] pos: part-of-speech (POS) tag to constrain the
        search (*n* for noun, *v* for verb, *a* for adjective, *s* for
        adjective satellite, and *r* for adverb; default is None)
    :param str lang: language code, such as *eng* or *tha*
        (default is *tha*)
    :return: list of lemma names for the given POS tag and language
    :rtype: list[str]

    :Example:

        >>> from pythainlp.corpus.wordnet import all_lemma_names
        >>>
        >>> all_lemma_names()
        ['อเมริโก_เวสปุชชี',
         'เมืองชีย์เอนเน',
         'การรับเลี้ยงบุตรบุญธรรม',
         'ผู้กัด',
         'ตกแต่งเรือด้วยธง',
         'จิโอวานนิ_เวอร์จินิโอ',...]
        >>>
        >>> len(all_lemma_names())
        80508
        >>>
        >>> all_lemma_names(pos="a")
        ['ซึ่งไม่มีแอลกอฮอล์',
         'ซึ่งตรงไปตรงมา',
         'ที่เส้นศูนย์สูตร',
         'ทางจิตใจ',...]
        >>>
        >>> len(all_lemma_names(pos="a"))
        5277
    """
    return cast("list[str]", wordnet.all_lemma_names(pos=pos, lang=lang))


def all_synsets(pos: Optional[str] = None) -> Iterable[Synset]:
    """
    Iterate over all synsets, constrained by a part of speech.

    :param Optional[str] pos: part-of-speech (POS) tag to constrain the
        search (*n* for noun, *v* for verb, *a* for adjective, *s* for
        adjective satellite, and *r* for adverb; default is None)
    :return: synsets constrained by the given POS tag
    :rtype: Iterable[nltk.corpus.reader.wordnet.Synset]

    :Example:

        >>> from pythainlp.corpus.wordnet import all_synsets
        >>>
        >>> generator = all_synsets(pos="n")
        >>> next(generator)
        Synset('entity.n.01')
        >>> next(generator)
        Synset('physical_entity.n.01')
        >>> next(generator)
        Synset('abstraction.n.06')
        >>>
        >>>  generator = all_synsets()
        >>> next(generator)
        Synset('able.a.01')
        >>> next(generator)
        Synset('unable.a.01')
    """
    return cast("Iterable[Synset]", wordnet.all_synsets(pos=pos))


def langs() -> list[str]:
    """
    Return the ISO 639 language codes.

    :return: ISO 639 language codes
    :rtype: list[str]

    :Example:
        >>> from pythainlp.corpus.wordnet import langs
        >>> langs()
        ['eng', 'als', 'arb', 'bul', 'cmn', 'dan', 'ell', 'fin',
         'fra', 'heb', 'hrv', 'isl', 'ita', 'ita_iwn', 'jpn', 'cat',
         'eus', 'glg', 'spa', 'ind', 'zsm', 'nld', 'nno', 'nob',
         'pol', 'por', 'ron', 'lit', 'slk', 'slv', 'swe', 'tha']
    """
    # NLTK 3.8+ loads OMW languages on first use; load them now so they
    # are listed.
    if hasattr(wordnet, "add_omw") and not getattr(wordnet, "omw_langs", True):
        wordnet.add_omw()
    return cast("list[str]", wordnet.langs())


def lemmas(
    word: str, pos: Optional[str] = None, lang: str = "tha"
) -> list[Lemma]:
    """
    Return all lemmas of a word.

    The function can constrain the part of speech of the word.

    :param str word: word to find lemmas of
    :param Optional[str] pos: part-of-speech (POS) tag to constrain the
        search (*n* for noun, *v* for verb, *a* for adjective, *s* for
        adjective satellite, and *r* for adverb; default is None)
    :param str lang: language code, such as *eng* or *tha*
        (default is *tha*)
    :return: all lemmas of the word, constrained by *pos*
    :rtype: list[nltk.corpus.reader.wordnet.Lemma]

    :Example:

        >>> from pythainlp.corpus.wordnet import lemmas
        >>>
        >>> lemmas("โปรด")
        [Lemma('like.v.03.โปรด'), Lemma('like.v.02.โปรด')]

        >>> print(lemmas("พระเจ้า"))
        [Lemma('god.n.01.พระเจ้า'), Lemma('godhead.n.01.พระเจ้า'),
         Lemma('father.n.06.พระเจ้า'), Lemma('god.n.03.พระเจ้า')]

        When the part of speech tag is specified:

        >>> from pythainlp.corpus.wordnet import lemmas
        >>>
        >>> lemmas("ม้วน")
        [Lemma('roll.v.18.ม้วน'), Lemma('roll.v.17.ม้วน'),
         Lemma('roll.v.08.ม้วน'),  Lemma('curl.v.01.ม้วน'),
         Lemma('roll_up.v.01.ม้วน'), Lemma('wind.v.03.ม้วน'),
         Lemma('roll.n.11.ม้วน')]
        >>>
        >>> # only lemmas with Noun as the part of speech
        >>> lemmas("ม้วน", pos="n")
        [Lemma('roll.n.11.ม้วน')]
    """
    return cast("list[Lemma]", wordnet.lemmas(word, pos=pos, lang=lang))


def lemma(name_synsets: str) -> Lemma:
    """
    Return the lemma object of a given name.

    .. note::
        The function supports only the English language (*eng*).

    :param str name_synsets: name of the lemma
    :return: lemma object of the given name
    :rtype: nltk.corpus.reader.wordnet.Lemma

    :Example:

        >>> from pythainlp.corpus.wordnet import lemma
        >>>
        >>> lemma("practice.v.01.exercise")
        Lemma('practice.v.01.exercise')
        >>>
        >>> lemma("drill.v.03.exercise")
        Lemma('drill.v.03.exercise')
        >>>
        >>> lemma("exercise.n.01.exercise")
        Lemma('exercise.n.01.exercise')
    """
    return wordnet.lemma(name_synsets)


def lemma_from_key(key: str) -> Lemma:
    """
    Return the lemma object of a given key.

    The function is similar to :func:`lemma`, but it takes the key of the
    lemma instead of the name of the lemma.

    .. note::
        The function supports only the English language (*eng*).

    :param str key: key of the lemma object
    :return: lemma object of the given key
    :rtype: nltk.corpus.reader.wordnet.Lemma

    :Example:

        >>> from pythainlp.corpus.wordnet import lemma, lemma_from_key
        >>>
        >>> practice = lemma("practice.v.01.exercise")
        >>> practice.key()
        exercise%2:41:00::
        >>> lemma_from_key(practice.key())
        Lemma('practice.v.01.exercise')
    """
    return wordnet.lemma_from_key(key)


def path_similarity(synsets1: Synset, synsets2: Synset) -> float:
    r"""
    Return the path similarity between two synsets.

    The similarity is based on the shortest path distance, calculated with
    the equation below.

    .. math::

        path\_similarity = {1 \over shortest\_path\_distance(synsets1,
                             synsets2) + 1}

    The shortest path distance is calculated by the connection through
    the is-a (hypernym/hyponym) taxonomy. The score is in the range of
    0 to 1. A path similarity of 1 indicates identity.

    :param nltk.corpus.reader.wordnet.Synset synsets1: first synset
    :param nltk.corpus.reader.wordnet.Synset synsets2: second synset
    :return: path similarity between the two synsets
    :rtype: float

    :Example:

        >>> from pythainlp.corpus.wordnet import path_similarity, synset
        >>>
        >>> entity = synset("entity.n.01")
        >>> obj = synset("object.n.01")
        >>> cat = synset("cat.n.01")
        >>>
        >>> path_similarity(entity, obj)
        0.3333333333333333
        >>> path_similarity(entity, cat)
        0.07142857142857142
        >>> path_similarity(obj, cat)
        0.08333333333333333
    """
    return cast("float", wordnet.path_similarity(synsets1, synsets2))


def lch_similarity(synsets1: Synset, synsets2: Synset) -> float:
    r"""
    Return the Leacock-Chodorow (LCH) similarity between two synsets.

    The similarity is based on the shortest path distance and the maximum
    depth of the taxonomy, calculated with the equation below.

    .. math::

        lch\_similarity = {-log(shortest\_path\_distance(synsets1,
                           synsets2) \over 2 * taxonomy\_depth}

    :param nltk.corpus.reader.wordnet.Synset synsets1: first synset
    :param nltk.corpus.reader.wordnet.Synset synsets2: second synset
    :return: LCH similarity between the two synsets
    :rtype: float

    :Example:

        >>> from pythainlp.corpus.wordnet import lch_similarity, synset
        >>>
        >>> entity = synset("entity.n.01")
        >>> obj = synset("object.n.01")
        >>> cat = synset("cat.n.01")
        >>>
        >>> lch_similarity(entity, obj)
        2.538973871058276
        >>> lch_similarity(entity, cat)
        0.9985288301111273
        >>> lch_similarity(obj, cat)
        1.1526795099383855
    """
    return cast("float", wordnet.lch_similarity(synsets1, synsets2))


def wup_similarity(synsets1: Synset, synsets2: Synset) -> float:
    """
    Return the Wu-Palmer (WUP) similarity between two synsets.

    The similarity is based on the depth of the two senses in the taxonomy
    and their Least Common Subsumer (most specific ancestor node).

    :param nltk.corpus.reader.wordnet.Synset synsets1: first synset
    :param nltk.corpus.reader.wordnet.Synset synsets2: second synset
    :return: WUP similarity between the two synsets
    :rtype: float

    :Example:

        >>> from pythainlp.corpus.wordnet import wup_similarity, synset
        >>>
        >>> entity = synset("entity.n.01")
        >>> obj = synset("object.n.01")
        >>> cat = synset("cat.n.01")
        >>>
        >>> wup_similarity(entity, obj)
        0.5
        >>> wup_similarity(entity, cat)
        0.13333333333333333
        >>> wup_similarity(obj, cat)
        0.35294117647058826
    """
    return cast("float", wordnet.wup_similarity(synsets1, synsets2))


def morphy(form: str, pos: Optional[str] = None) -> str:
    """
    Find a possible base form of a given form and part of speech.

    :param str form: form to find the base form of
    :param Optional[str] pos: part-of-speech (POS) tag of the words to be
        searched (default is None)
    :return: base form of the given form
    :rtype: str

    :Example:

        >>> from pythainlp.corpus.wordnet import morphy
        >>>
        >>> morphy("dogs")
        'dog'
        >>>
        >>> morphy("thieves")
        'thief'
        >>>
        >>> morphy("mixed")
        'mix'
        >>>
        >>> morphy("calculated")
        'calculate'
    """
    return cast("str", wordnet.morphy(form, pos=pos))


def custom_lemmas(tab_file: Union[str, IO[str]], lang: str) -> None:
    """
    Read a custom tab file of lemma mappings in a given language.

    See `Open Multilingual Wordnet <https://omwn.org/>`_
    for the file format.

    :param Union[str, IO[str]] tab_file: tab file, as a file name or a
        file-like object
    :param str lang: language code, such as *eng* or *tha*
    """
    wordnet.custom_lemmas(tab_file, lang)
