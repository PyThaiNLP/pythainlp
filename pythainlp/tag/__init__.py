# -*- coding: utf-8 -*-
"""
Tagging each token in a sentence with supplementary information,
such as its part of speech and class of named-entity.
"""

__all__ = [
    "pos_tag",
    "pos_tag_sents",
    "tag_provinces",
    "ThaiNameTagger",
]

from .named_entity import ThaiNameTagger
from .locations import tag_provinces


def pos_tag(words, engine="unigram", corpus="orchid"):
    """
    Part of Speech tagging function.

    :param list words: a list of tokenized words
    :param str engine:
        * unigram - unigram tagger (default)
        * perceptron - perceptron tagger
        * artagger - RDR POS tagger
    :param str corpus:
        * orchid - annotated Thai academic articles
        * pud - Parallel Universal Dependencies (PUD) treebanks
    :return: returns a list of labels regarding which part of speech it is
    """
    if not words:
        return []

    if engine == "perceptron":
        from .perceptron import tag as tag_
    elif engine == "artagger":

        def tag_(words, corpus=None):
            if not words:
                return []

            from artagger import Tagger
            words_ = Tagger().tag(" ".join(words))

            return [(word.word, word.tag) for word in words_]

    else:  # default, use "unigram" ("old") engine
        from .unigram import tag as tag_

    return tag_(words, corpus=corpus)


def pos_tag_sents(sentences, engine="unigram", corpus="orchid"):
    if not sentences:
        return []

    return [pos_tag(sent, engine=engine, corpus=corpus) for sent in sentences]
