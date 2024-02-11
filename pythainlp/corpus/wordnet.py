# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
NLTK WordNet wrapper

API here is exactly the same as NLTK WordNet API,
except that the lang (language) argument is "tha" (Thai) by default.

For more on usage, see NLTK Howto:
https://www.nltk.org/howto/wordnet.html
"""
import nltk

try:
    nltk.data.find("corpora/omw")
except LookupError:
    nltk.download("omw")

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")

from nltk.corpus import wordnet


def synsets(word: str, pos: str = None, lang: str = "tha"):
    """
    This function returns the synonym set for all lemmas of the given word
    with an optional argument to constrain the part of speech of the word.

    :param str word: word to find synsets of
    :param str pos: constraint of the part of speech (i.e. *n* for Noun, *v*
                    for Verb, *a* for Adjective, *s* for Adjective
                    satellites, and *r* for Adverb)
    :param str lang: abbreviation of language (i.e. *eng*, *tha*).
                     By default, it is *tha*

    :return: :class:`Synset` all lemmas of the word constrained with
             the argument *pos*.
    :rtype: list[:class:`Synset`]

    :Example:

        >>> from pythainlp.corpus.wordnet import synsets
        >>>
        >>> synsets("ทำงาน")
        [Synset('function.v.01'), Synset('work.v.02'),
         Synset('work.v.01'), Synset('work.v.08')]
        >>>
        >>> synsets("บ้าน", lang="tha"))
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
    return wordnet.synsets(lemma=word, pos=pos, lang=lang)


def synset(name_synsets):
    """
    This function returns the synonym set (synset) given the name of the synset
    (i.e. 'dog.n.01', 'chase.v.01').

    :param str name_synsets: name of the synset

    :return: :class:`Synset` of the given name
    :rtype: :class:`Synset`

    :Example:

        >>> from pythainlp.corpus.wordnet import synset
        >>>
        >>> difficult = synset('difficult.a.01')
        >>> difficult
        Synset('difficult.a.01')
        >>>
        >>> difficult.definition()
        'not easy; requiring great physical or mental effort to accomplish
                   or comprehend or endure'
    """
    return wordnet.synset(name_synsets)


def all_lemma_names(pos: str = None, lang: str = "tha"):
    """
    This function returns all lemma names for all synsets of the given
    part of speech tag and language. If part of speech tag is not
    specified, all synsets of all parts of speech will be used.

    :param str pos: constraint of the part of speech (i.e. *n* for Noun,
                    *v* for Verb, *a* for Adjective, *s* for
                    Adjective satellites, and *r* for Adverb).
                    By default, *pos* is **None**.
    :param str lang: abbreviation of language (i.e. *eng*, *tha*).
                     By default, it is *tha*.

    :return: :class:`Synset` of lemmas names given the POS and language
    :rtype: list[:class:`Synset`]

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
    return wordnet.all_lemma_names(pos=pos, lang=lang)


def all_synsets(pos: str = None):
    """
    This function iterates over all synsets constrained by the given
    part of speech tag.

    :param str pos: part of speech tag

    :return: list of synsets constrained by the given part of speech tag.
    :rtype: Iterable[:class:`Synset`]

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
    return wordnet.all_synsets(pos=pos)


def langs():
    """
    This function returns a set of ISO-639 language codes.

    :return: ISO-639 language codes
    :rtype: list[str]

    :Example:
        >>> from pythainlp.corpus.wordnet import langs
        >>> langs()
        ['eng', 'als', 'arb', 'bul', 'cat', 'cmn', 'dan',
         'ell', 'eus', 'fas', 'fin', 'fra', 'glg', 'heb',
         'hrv', 'ind', 'ita', 'jpn', 'nld', 'nno', 'nob',
         'pol', 'por', 'qcn', 'slv', 'spa', 'swe', 'tha',
         'zsm']
    """
    return wordnet.langs()


def lemmas(word: str, pos: str = None, lang: str = "tha"):
    """
    This function returns all lemmas given the word with an optional
    argument to constrain the part of speech of the word.

    :param str word: word to find lemmas of
    :param str pos: constraint of the part of speech (i.e. *n* for Noun,
                    *v* for Verb, *a* for Adjective, *s* for
                    Adjective satellites, and *r* for Adverb)
    :param str lang: abbreviation of language (i.e. *eng*, *tha*).
                     By default, it is *tha*.

    :return: :class:`Synset` of all lemmas of the word constrained
              by the argument *pos*.
    :rtype: list[:class:`Lemma`]

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
    return wordnet.lemmas(word, pos=pos, lang=lang)


def lemma(name_synsets):
    """
    This function returns lemma object given the name.

    .. note::
        Support only English language (*eng*).

    :param str name_synsets: name of the synset

    :return: lemma object with the given name
    :rtype: :class:`Lemma`

    :Example:

        >>> from pythainlp.corpus.wordnet import lemma
        >>>
        >>> lemma('practice.v.01.exercise')
        Lemma('practice.v.01.exercise')
        >>>
        >>> lemma('drill.v.03.exercise')
        Lemma('drill.v.03.exercise')
        >>>
        >>> lemma('exercise.n.01.exercise')
        Lemma('exercise.n.01.exercise')
    """
    return wordnet.lemma(name_synsets)


def lemma_from_key(key):
    """
    This function returns lemma object given the lemma key.
    This is similar to :func:`lemma` but it needs to be given the key
    of lemma instead of the name of lemma.

    .. note::
        Support only English language (*eng*).

    :param str key: key of the lemma object

    :return: lemma object with the given key
    :rtype: :class:`Lemma`

    :Example:

        >>> from pythainlp.corpus.wordnet import lemma, lemma_from_key
        >>>
        >>> practice = lemma('practice.v.01.exercise')
        >>> practice.key()
        exercise%2:41:00::
        >>> lemma_from_key(practice.key())
        Lemma('practice.v.01.exercise')
    """
    return wordnet.lemma_from_key(key)


def path_similarity(synsets1, synsets2):
    """
    This function returns similarity between two synsets based on the
    shortest path distance calculated using the equation below.

    .. math::

        path\\_similarity = {1 \\over shortest\\_path\\_distance(synsets1,
                             synsets2) + 1}

    The shortest path distance is calculated by the connection through
    the is-a (hypernym/hyponym) taxonomy. The score is in the range of
    0 to 1. Path similarity of 1 indicates identicality.

    :param `Synset` synsets1: first synset supplied to measures
                              the path similarity with
    :param `Synset` synsets2: second synset supplied to measures
                              the path similarity with

    :return: path similarity between two synsets
    :rtype: float

    :Example:

        >>> from pythainlp.corpus.wordnet import path_similarity, synset
        >>>
        >>> entity = synset('entity.n.01')
        >>> obj = synset('object.n.01')
        >>> cat = synset('cat.n.01')
        >>>
        >>> path_similarity(entity, obj)
        0.3333333333333333
        >>> path_similarity(entity, cat)
        0.07142857142857142
        >>> path_similarity(obj, cat)
        0.08333333333333333
    """
    return wordnet.path_similarity(synsets1, synsets2)


def lch_similarity(synsets1, synsets2):
    """
    This function returns Leacock Chodorow similarity (LCH)
    between two synsets, based on the shortest path distance
    and the maximum depth of the taxonomy. The equation to
    calculate LCH similarity is shown below:

    .. math::

        lch\\_similarity = {-log(shortest\\_path\\_distance(synsets1,
                           synsets2) \\over 2 * taxonomy\\_depth}

    :param `Synset` synsets1: first synset supplied to measures
                              the LCH similarity
    :param `Synset` synsets2: second synset supplied to measures
                              the LCH similarity

    :return: LCH similarity between two synsets
    :rtype: float

    :Example:

        >>> from pythainlp.corpus.wordnet import lch_similarity, synset
        >>>
        >>> entity = synset('entity.n.01')
        >>> obj = synset('object.n.01')
        >>> cat = synset('cat.n.01')
        >>>
        >>> lch_similarity(entity, obj)
        2.538973871058276
        >>> lch_similarity(entity, cat)
        0.9985288301111273
        >>> lch_similarity(obj, cat)
        1.1526795099383855
    """
    return wordnet.lch_similarity(synsets1, synsets2)


def wup_similarity(synsets1, synsets2):
    """
    This function returns Wu-Palmer similarity (WUP) between two synsets,
    based on the depth of the two senses in the taxonomy and their
    Least Common Subsumer (most specific ancestor node).

    :param `Synset` synsets1: first synset supplied to measures
                              the WUP similarity with
    :param `Synset` synsets2: second synset supplied to measures
                              the WUP similarity with

    :return: WUP similarity between two synsets
    :rtype: float

    :Example:

        >>> from pythainlp.corpus.wordnet import wup_similarity, synset
        >>>
        >>> entity = synset('entity.n.01')
        >>> obj = synset('object.n.01')
        >>> cat = synset('cat.n.01')
        >>>
        >>> wup_similarity(entity, obj)
        0.5
        >>> wup_similarity(entity, cat)
        0.13333333333333333
        >>> wup_similarity(obj, cat)
        0.35294117647058826
    """
    return wordnet.wup_similarity(synsets1, synsets2)


def morphy(form, pos: str = None):
    """
    This function finds a possible base form for the given form,
    with the given part of speech.

    :param str form: the form to finds the base form of
    :param str pos: part of speech tag of words to be searched

    :return: base form of the given form
    :rtype: str

    :Example:

        >>> from pythainlp.corpus.wordnet import morphy
        >>>
        >>> morphy("dogs")
        'dogs'
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
    return wordnet.morphy(form, pos=None)


def custom_lemmas(tab_file, lang: str):
    """
    This function reads a custom tab file
    (see: http://compling.hss.ntu.edu.sg/omw/)
    containing mappings of lemmas in the given language.

    :param tab_file: Tab file as a file or file-like object
    :param str lang: abbreviation of language (i.e. *eng*, *tha*).
    """
    return wordnet.custom_lemmas(tab_file, lang)
