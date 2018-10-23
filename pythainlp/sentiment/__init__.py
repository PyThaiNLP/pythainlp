# -*- coding: utf-8 -*-

import os
import dill

import pythainlp
from pythainlp.corpus import stopwords
from pythainlp.tokenize import word_tokenize

TEMPLATES_DIR = os.path.join(os.path.dirname(pythainlp.__file__), "sentiment")


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
        with open(os.path.join(TEMPLATES_DIR, "vocabulary.data"), "rb") as in_strm:
            vocabulary = dill.load(in_strm)
        with open(os.path.join(TEMPLATES_DIR, "sentiment.data"), "rb") as in_strm:
            classifier = dill.load(in_strm)
        text = set(word_tokenize(text)) - set(stopwords.words("thai"))
        featurized_test_sentence = {i: (i in text) for i in vocabulary}
        return classifier.classify(featurized_test_sentence)


if __name__ == "__main__":
    text = "เสียใจแย่มากเลย"
    print(sentiment(text))
