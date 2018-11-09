# -*- coding: utf-8 -*-
"""
Part-Of-Speech tagger
"""

_ARTAGGER_URL = "https://github.com/wannaphongcom/artagger/archive/master.zip"


def pos_tag(words, engine="unigram", corpus="orchid"):
    """
    Part of Speech tagging function.

    :param list words: takes in a list of tokenized words (put differently, a list of strings)
    :param str engine:
        * unigram - unigram tagger (default)
        * perceptron - perceptron tagger
        * artagger - RDR POS tagger
    :param str corpus:
        * orchid - annotated Thai academic articles
        * pud - Parallel Universal Dependencies (PUD) treebanks
    :return: returns a list of labels regarding which part of speech it is
    """
    if engine == "perceptron":
        from .perceptron import tag as _tag
    elif engine == "artagger":

        def _tag(text, corpus=None):
            from artagger import Tagger
            words = Tagger().tag(" ".join(text))

            return [(word.word, word.tag) for word in words]

    else:  # default, use "unigram" ("old") engine
        from .unigram import tag as _tag

    return _tag(words, corpus=corpus)


def pos_tag_sents(sentences, engine="unigram", corpus="orchid"):
    return [pos_tag(sent, engine=engine, corpus=corpus) for sent in sentences]
