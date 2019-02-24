# -*- coding: utf-8 -*-
"""
Summarization
"""

from pythainlp.tokenize import sent_tokenize

from .freq import FrequencySummarizer


def summarize(text, n, engine="frequency", tokenizer="newmm"):
    """
    Thai text summarization

    :param str text: text to be summarized
    :param int n: number of sentences to be included in the summary
    :param str engine: text summarization engine
    :param str tokenizer: word tokenizer
    :return List[str] summary: list of selected sentences
    """
    sents = []

    if engine == "frequency":
        sents = FrequencySummarizer().summarize(text, n, tokenizer)
    else:  # if engine not found, return first n sentences
        sents = sent_tokenize(text)[:n]

    return sents
