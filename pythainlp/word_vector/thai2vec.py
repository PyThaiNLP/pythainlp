# -*- coding: utf-8 -*-
"""
thai2vec - Thai word vector
Code by https://github.com/cstorm125/thai2vec/blob/master/notebooks/examples.ipynb
"""
from pythainlp.corpus import download as download_data
from pythainlp.corpus import get_file
from pythainlp.tokenize import word_tokenize

try:
    from gensim.models import KeyedVectors
    import numpy as np
except ImportError:
    from pythainlp.tools import install_package

    install_package("gensim")
    install_package("numpy")
    try:
        from gensim.models import KeyedVectors
        import numpy as np
    except ImportError:
        raise ImportError("ImportError: Try 'pip install gensim numpy'")


def download():
    path = get_file("thai2vec02")
    if not path:
        download_data("thai2vec02")
        path = get_file("thai2vec02")
    return path


def get_model():
    """
    :return: Downloads the `gensim` model."""
    return KeyedVectors.load_word2vec_format(download(), binary=False)


def most_similar_cosmul(positive, negative):
    """
    การใช้งาน
    input list
    """
    return get_model().most_similar_cosmul(positive=positive, negative=negative)


def doesnt_match(listdata):
    return get_model().doesnt_match(listdata)


def similarity(word1, word2):
    """
    :param str word1: first word
    :param str word2: second word
    :return: the cosine similarity between the two word vectors
    """
    return get_model().similarity(word1, word2)


def sentence_vectorizer(text, dim=300, use_mean=False):
    words = word_tokenize(text)
    vec = np.zeros((1, dim))
    for word in words:
        if word in get_model().wv.index2word:
            vec += get_model().wv.word_vec(word)
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
