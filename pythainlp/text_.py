# -*- coding: utf-8 -*-
"""
NLTK Text() wrapper
"""
import nltk
from pythainlp.tokenize import word_tokenize


def Text(text):
    if not isinstance(text, list):
        text = word_tokenize(str(text))
    return nltk.Text(text)
