# -*- coding: utf-8 -*-
"""
Wrapper for LexTo Thai word segmentation
"""
import sys

_LEXTO_URL = "https://github.com/PyThaiNLP/pylexto/archive/master.zip"

try:
    from pylexto import LexTo
except ImportError:
    from pythainlp.tools import install_package

    install_package(_LEXTO_URL)
    try:
        from pylexto import LexTo
    except ImportError:
        sys.exit("Error: Try pip install '" + _LEXTO_URL + "'")

_LEXTO = LexTo()


def segment(text, full=False):
    words, types = _LEXTO.tokenize(text)
    if full:
        return (words, types)

    return words
