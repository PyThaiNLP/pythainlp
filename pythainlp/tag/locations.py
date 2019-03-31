# -*- coding: utf-8 -*-
"""
Recognizes locations in text
"""

from pythainlp.corpus import provinces


def tag_provinces(tokens):
    """
    Recognize Thailand provinces in text

    Input is a list of words
    Return a list of tuples

    Example::
     >>> text = ['หนองคาย', 'น่าอยู่']
     >>> tag_provinces(text)
     [('หนองคาย', 'B-LOCATION'), ('น่าอยู่', 'O')]
    """
    province_list = provinces()

    output = []
    for token in tokens:
        if token in province_list:
            output.append((token, "B-LOCATION"))
        else:
            output.append((token, "O"))

    return output
