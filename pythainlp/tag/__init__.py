# -*- coding: utf-8 -*-
"""
Part-Of-Speech Tagging
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import sys

ARTAGGER_URL = "https://github.com/wannaphongcom/artagger/archive/master.zip"


def pos_tag(texts, engine="unigram", corpus="orchid"):
    """
    Part of Speech tagging function.

    :param list texts: takes in a list of tokenized words (put differently, a list of strings)
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
        from .perceptron import tag
    elif engine == "artagger":

        def tag(text):
            try:
                from artagger import Tagger
            except ImportError:
                from pythainlp.tools import install_package

                install_package(ARTAGGER_URL)
                try:
                    from artagger import Tagger
                except ImportError:
                    print("Error: Try 'pip install " + ARTAGGER_URL + "'")
                    sys.exit(0)
            words = Tagger().tag(" ".join(text))
            totag = []
            for word in words:
                totag.append((word.word, word.tag))
            return totag

        return tag(texts)
    else:  # default, use "unigram" ("old") engine
        from .old import tag

    return tag(texts, corpus=corpus)


def pos_tag_sents(sentences, engine="unigram", corpus="orchid"):
    return [pos_tag(i, engine=engine, corpus=corpus) for i in sentences]
