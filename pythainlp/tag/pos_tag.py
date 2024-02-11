# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
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
        * *tltk* - TLTK: Thai Language Toolkit (support TNC corpora only.\
            If you choose other corpora, they will be converted to TNC corpora.)
    :param str corpus: the corpus that is used to create the language model for tagger
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
            If you choose other corpora, they will be converted to TNC corpora.)
    :param str corpus: the corpus that is used to create the language model for tagger
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


def pos_tag_transformers(
    sentence: str,
    engine: str = "bert",
    corpus: str = "blackboard",
) -> List[List[Tuple[str, str]]]:
    """
    Marks sentences with part-of-speech (POS) tags.

    :param str sentence: a list of lists of tokenized words
    :param str engine:
        * *bert* -  BERT: Bidirectional Encoder Representations from Transformers (default)
        * *wangchanberta* - fine-tuned version of airesearch/wangchanberta-base-att-spm-uncased on pud corpus (support PUD cotpus only)
        * *phayathaibert* - fine-tuned version of clicknext/phayathaibert \
            on blackboard corpus (support blackboard cotpus only)
        * *mdeberta* - mDeBERTa: Multilingual Decoding-enhanced BERT with disentangled attention (support PUD corpus only)
    :param str corpus: the corpus that is used to create the language model for tagger
        * *blackboard* - `blackboard treebank (support bert engine only) <https://bitbucket.org/kaamanita/blackboard-treebank/src/master/>`_
        * *pud* - `Parallel Universal Dependencies (PUD)\
            <https://github.com/UniversalDependencies/UD_Thai-PUD>`_ \
            treebanks, natively use Universal POS tags (support wangchanberta and mdeberta engine)
    :return: a list of lists of tuples (word, POS tag)
    :rtype: list[list[tuple[str, str]]]

    :Example:

    Labels POS for given sentence::

        from pythainlp.tag import pos_tag_transformers

        sentences = "แมวทำอะไรตอนห้าโมงเช้า"
        pos_tag_transformers(sentences, engine="bert", corpus='blackboard')
        # output:
        # [[('แมว', 'NOUN'), ('ทําอะไร', 'VERB'), ('ตอนห้าโมงเช้า', 'NOUN')]]
    """

    try:
        from transformers import (
            AutoModelForTokenClassification,
            AutoTokenizer,
            TokenClassificationPipeline,
        )
    except ImportError:
        raise ImportError(
            "Not found transformers! Please install transformers by pip install transformers"
        )

    if not sentence:
        return []

    _blackboard_support_engine = {
        "bert": "lunarlist/pos_thai",
        "phayathai": "lunarlist/pos_thai_phayathai",
    }

    _pud_support_engine = {
        "wangchanberta": "Pavarissy/wangchanberta-ud-thai-pud-upos",
        "mdeberta": "Pavarissy/mdeberta-v3-ud-thai-pud-upos",
    }

    if corpus == "blackboard" and engine in _blackboard_support_engine.keys():
        base_model = _blackboard_support_engine.get(engine)
        model = AutoModelForTokenClassification.from_pretrained(base_model)
        tokenizer = AutoTokenizer.from_pretrained(base_model)
    elif corpus == "pud" and engine in _pud_support_engine.keys():
        base_model = _pud_support_engine.get(engine)
        model = AutoModelForTokenClassification.from_pretrained(base_model)
        tokenizer = AutoTokenizer.from_pretrained(base_model)
    else:
        raise ValueError(
            "pos_tag_transformers not support {0} engine or {1} corpus.".format(
                engine, corpus
            )
        )

    pipeline = TokenClassificationPipeline(model=model,
                                           tokenizer=tokenizer,
                                           aggregation_strategy="simple",
                                           )

    outputs = pipeline(sentence)
    word_tags = [[(tag["word"], tag["entity_group"]) for tag in outputs]]
    return word_tags
