# -*- coding: utf-8 -*-
"""
thai2vec - Thai word vector
Code by https://github.com/cstorm125/thai2vec/blob/master/notebooks/examples.ipynb
"""
import numpy as np
from gensim.models import KeyedVectors
from pythainlp.corpus import download as download_data
from pythainlp.corpus import get_file
from pythainlp.tokenize import word_tokenize


def _download():
    path = get_file("thai2vec02")
    if not path:
        download_data("thai2vec02")
        path = get_file("thai2vec02")
    return path


def get_model():
    """
    Download model
    :return: `gensim` model
    """
    return KeyedVectors.load_word2vec_format(_download(), binary=False)


_MODEL = get_model()


def most_similar_cosmul(positive, negative):
    """
    การใช้งาน
    input list
    """
    return _MODEL.most_similar_cosmul(positive=positive, negative=negative)


def doesnt_match(listdata):
    return _MODEL.doesnt_match(listdata)


def similarity(word1, word2):
    """
    Get cosine similarity between two words.
    If a word is not in the vocabulary, KeyError will be raised.
    :param str word1: first word
    :param str word2: second word
    :return: the cosine similarity between the two word vectors
    """
    return _MODEL.similarity(word1, word2)


def sentence_vectorizer(text, dim=300, use_mean=False):
    words = word_tokenize(text)
    vec = np.zeros((1, dim))
    for word in words:
        if word in _MODEL.wv.index2word:
            vec += _MODEL.wv.word_vec(word)
        else:
            pass
    if use_mean:
        vec /= len(words)
    return vec


def about():
    return """
    thai2vec
    State-of-the-Art Language Modeling, Text Feature Extraction and Text Classification in Thai Language.
    Created as part of pyThaiNLP with ULMFit implementation from fast.ai

    Development: Charin Polpanumas
    GitHub: https://github.com/cstorm125/thai2vec
    """
