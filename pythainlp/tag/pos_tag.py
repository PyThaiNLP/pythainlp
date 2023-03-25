# -*- coding: utf-8 -*-
# Copyright (C) 2016-2023 PyThaiNLP Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import List, Tuple


def pos_tag(
    words: List[str], engine: str = "perceptron", corpus: str = "orchid"
) -> List[Tuple[str, str]]:
    """
    Marks words with part-of-speech (POS) tags, such as 'NOUN' and 'VERB'.

    :param list words: a list of tokenized words
    :param str engine:
        * *perceptron* - perceptron tagger (default)
        * *unigram* - unigram tagger
        * *wangchanberta* - wangchanberta model.
        * *tltk* - TLTK: Thai Language Toolkit (support TNC corpus only.\
            if you choose other corpus, It's change to TNC corpus.)
    :param str corpus: the corpus that used to create the language model for tagger
        * *orchid* - `ORCHID \
            <https://www.academia.edu/9127599/Thai_Treebank>`_ corpus, \
            text from Thai academic articles (default)
        * *orchid_ud* - ORCHID text, with tags mapped to Universal POS tags
        * *blackboard* - `blackboard treebank <https://bitbucket.org/kaamanita/blackboard-treebank/src/master/>`_
        * *blackboard_ud* - blackboard text, with tags mapped to Universal POS tag \
            from `Universal Dependencies <https://universaldependencies.org/>`
        * *pud* - `Parallel Universal Dependencies (PUD)\
            <https://github.com/UniversalDependencies/UD_Thai-PUD>`_ \
            treebanks, natively use Universal POS tags
        * *tnc* - Thai National Corpus (support tltk engine only)
    :return: a list of tuples (word, POS tag)
    :rtype: list[tuple[str, str]]

    :Example:

    Tag words with corpus `orchid` (default)::

        from pythainlp.tag import pos_tag

        words = ['ฉัน','มี','ชีวิต','รอด','ใน','อาคาร','หลบภัย','ของ', \\
            'นายก', 'เชอร์ชิล']
        pos_tag(words)
        # output:
        # [('ฉัน', 'PPRS'), ('มี', 'VSTA'), ('ชีวิต', 'NCMN'), ('รอด', 'NCMN'),
        #   ('ใน', 'RPRE'), ('อาคาร', 'NCMN'), ('หลบภัย', 'NCMN'),
        #   ('ของ', 'RPRE'), ('นายก', 'NCMN'), ('เชอร์ชิล', 'NCMN')]

    Tag words with corpus `orchid_ud`::

        from pythainlp.tag import pos_tag

        words = ['ฉัน','มี','ชีวิต','รอด','ใน','อาคาร','หลบภัย','ของ', \\
            'นายก', 'เชอร์ชิล']
        pos_tag(words, corpus='orchid_ud')
        # output:
        # [('ฉัน', 'PROPN'), ('มี', 'VERB'), ('ชีวิต', 'NOUN'),
        #   ('รอด', 'NOUN'), ('ใน', 'ADP'),  ('อาคาร', 'NOUN'),
        #   ('หลบภัย', 'NOUN'), ('ของ', 'ADP'), ('นายก', 'NOUN'),
        #   ('เชอร์ชิล', 'NOUN')]

    Tag words with corpus `pud`::

        from pythainlp.tag import pos_tag

        words = ['ฉัน','มี','ชีวิต','รอด','ใน','อาคาร','หลบภัย','ของ', \\
            'นายก', 'เชอร์ชิล']
        pos_tag(words, corpus='pud')
        # [('ฉัน', 'PRON'), ('มี', 'VERB'), ('ชีวิต', 'NOUN'), ('รอด', 'VERB'),
        #   ('ใน', 'ADP'), ('อาคาร', 'NOUN'), ('หลบภัย', 'NOUN'),
        #   ('ของ', 'ADP'), ('นายก', 'NOUN'), ('เชอร์ชิล', 'PROPN')]

    Tag words with different engines including *perceptron* and *unigram*::

        from pythainlp.tag import pos_tag

        words = ['เก้าอี้','มี','จำนวน','ขา', ' ', '=', '3']

        pos_tag(words, engine='perceptron', corpus='orchid')
        # output:
        # [('เก้าอี้', 'NCMN'), ('มี', 'VSTA'), ('จำนวน', 'NCMN'),
        #   ('ขา', 'NCMN'), (' ', 'PUNC'),
        #   ('=', 'PUNC'), ('3', 'NCNM')]

        pos_tag(words, engine='unigram', corpus='pud')
        # output:
        # [('เก้าอี้', None), ('มี', 'VERB'), ('จำนวน', 'NOUN'), ('ขา', None),
        #   ('<space>', None), ('<equal>', None), ('3', 'NUM')]
    """
    if not words:
        return []

    _support_corpus = [
        "blackboard",
        "blackboard_ud",
        "orchid",
        "orchid_ud",
        "pud",
    ]

    if engine == "perceptron" and corpus in _support_corpus:
        from pythainlp.tag.perceptron import tag as tag_
    elif engine == "tltk":
        from pythainlp.tag.tltk import pos_tag as tag_

        corpus = "tnc"
    elif engine == "unigram" and corpus in _support_corpus:  # default
        from pythainlp.tag.unigram import tag as tag_
    else:
        raise ValueError(
            "pos_tag not support {0} engine or {1} corpus.".format(
                engine, corpus
            )
        )

    word_tags = tag_(words, corpus=corpus)

    return word_tags


def pos_tag_sents(
    sentences: List[List[str]],
    engine: str = "perceptron",
    corpus: str = "orchid",
) -> List[List[Tuple[str, str]]]:
    """
    Marks sentences with part-of-speech (POS) tags.

    :param list sentences: a list of lists of tokenized words
    :param str engine:
        * *perceptron* - perceptron tagger (default)
        * *unigram* - unigram tagger
        * *tltk* - TLTK: Thai Language Toolkit (support TNC corpus only.\
            if you choose other corpus, It's change to TNC corpus.)
    :param str corpus: the corpus that used to create the language model for tagger
        * *orchid* - `ORCHID \
            <https://www.academia.edu/9127599/Thai_Treebank>`_ corpus, \
            text from Thai academic articles (default)
        * *orchid_ud* - ORCHID text, with tags mapped to Universal POS tags
        * *blackboard* - `blackboard treebank <https://bitbucket.org/kaamanita/blackboard-treebank/src/master/>`_
        * *blackboard_ud* - blackboard text, with tags mapped to Universal POS tag \
            from `Universal Dependencies <https://universaldependencies.org/>`
        * *pud* - `Parallel Universal Dependencies (PUD)\
            <https://github.com/UniversalDependencies/UD_Thai-PUD>`_ \
            treebanks, natively use Universal POS tags
        * *tnc* - Thai National Corpus (support tltk engine only)
    :return: a list of lists of tuples (word, POS tag)
    :rtype: list[list[tuple[str, str]]]

    :Example:

    Labels POS for two sentences::

        from pythainlp.tag import pos_tag_sents

        sentences = [['เก้าอี้','มี','3','ขา'], \\
                            ['นก', 'บิน', 'กลับ', 'รัง']]
        pos_tag_sents(sentences, corpus='pud)
        # output:
        # [[('เก้าอี้', 'PROPN'), ('มี', 'VERB'), ('3', 'NUM'),
        #   ('ขา', 'NOUN')], [('นก', 'NOUN'), ('บิน', 'VERB'),
        #   ('กลับ', 'VERB'), ('รัง', 'NOUN')]]
    """
    if not sentences:
        return []

    return [pos_tag(sent, engine=engine, corpus=corpus) for sent in sentences]
