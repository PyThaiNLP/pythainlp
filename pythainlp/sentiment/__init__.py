# -*- coding: utf-8 -*-

import os
import dill

from pythainlp.corpus import thai_stopwords
from pythainlp.tokenize import word_tokenize
from pythainlp.tools import get_pythainlp_path

_SENTIMENT_DIRNAME = "sentiment"
_SENTIMENT_PATH = os.path.join(get_pythainlp_path(), _SENTIMENT_DIRNAME)

_STOPWORDS = thai_stopwords()


def sentiment(text, engine="old"):
    """
    :param str text: thai text
    :param str engine: sentiment analysis engine ("old" [default] or "ulmfit")
    :return: pos or neg

    **Example**::
        >>> from pythainlp.sentiment import sentiment
        >>> text="วันนี้อากาศดีจัง"
        >>> sentiment(text)
        'pos'
        >>> sentiment(text,'ulmfit')
        'pos'
        >>> text="วันนี้อารมณ์เสียมาก"
        >>> sentiment(text)
        'neg'
        >>> sentiment(text,'ulmfit')
        'neg'
    """
    if engine == "ulmfit":
        from pythainlp.sentiment import ulmfit_sent

        tag = ulmfit_sent.get_sentiment(text)

        return "pos" if tag else "neg"
    else:  # default, use "old" vocabulary-based engine
        with open(os.path.join(_SENTIMENT_PATH, "vocabulary.data"), "rb") as in_strm:
            vocabulary = dill.load(in_strm)

        with open(os.path.join(_SENTIMENT_PATH, "sentiment.data"), "rb") as in_strm:
            classifier = dill.load(in_strm)

        text = set(word_tokenize(text)) - _STOPWORDS
        featurized_test_sentence = {i: (i in text) for i in vocabulary}

        return classifier.classify(featurized_test_sentence)
