# -*- coding: utf-8 -*-

"""
thai2fit - Thai word vector
Code by https://github.com/cstorm125/thai2fit
"""
from typing import List

import numpy as np
from gensim.models import KeyedVectors
from pythainlp.corpus import download as download_data
from pythainlp.corpus import get_corpus_path
from pythainlp.tokenize import word_tokenize

WV_DIM = 300


def _download() -> str:
    path = get_corpus_path("thai2fit_wv")
    if not path:
        download_data("thai2fit_wv")
        path = get_corpus_path("thai2fit_wv")
    return path


def get_model():
    """
    Download model

    :return: `gensim` model
    """
    return KeyedVectors.load_word2vec_format(_download(), binary=True)


_MODEL = get_model()


def most_similar_cosmul(positive: List[str], negative: List[str]):
    """
    Word arithmetic operations
    If a word is not in the vocabulary, KeyError will be raised.

    :param list positive: a list of words to add
    :param list negative: a list of words to substract

    :return: the cosine similarity between the two word vectors
    """

    return _MODEL.most_similar_cosmul(positive=positive, negative=negative)


def doesnt_match(words: List[str]) -> str:
    """
    Pick one word that doesn't match other words in the list
    If a word is not in the vocabulary, KeyError will be raised.

    :param list words: a list of words
    :return: word that doesn't match
    """
    return _MODEL.doesnt_match(words)


def similarity(word1: str, word2: str) -> float:
    """
    Get cosine similarity between two words.
    If a word is not in the vocabulary, KeyError will be raised.

    :param string word1: first word
    :param string word2: second word
    :return: the cosine similarity between the two word vectors
    """
    return _MODEL.similarity(word1, word2)


def sentence_vectorizer(text: str, use_mean: bool = True):
    """
    Get sentence vector from text
    If a word is not in the vocabulary, KeyError will be raised.

    :param string text: text input
    :param boolean use_mean: if `True` use mean of all word vectors else use summation

    :return: sentence vector of given input text
    """
    words = word_tokenize(text, engine="ulmfit")
    vec = np.zeros((1, WV_DIM))

    for word in words:
        if word == " ":
            word = "xxspace"
        elif word == "\n":
            word = "xxeol"

        if word in _MODEL.wv.index2word:
            vec += _MODEL.wv.word_vec(word)
        else:
            pass

    if use_mean:
        vec /= len(words)

    return vec
