# -*- coding: utf-8 -*-
"""
Wrapper for ICU word segmentation
"""
import re

try:
    import icu
except ImportError:
    from pythainlp.tools import install_package

    install_package("pyicu")
    try:
        import icu
    except ImportError:
        raise ImportError("ImportError: Try 'pip install pyicu'")


def _gen_words(text):
    bd = icu.BreakIterator.createWordInstance(icu.Locale("th"))
    bd.setText(text)
    p = bd.first()
    for q in bd:
        yield text[p:q]
        p = q


def segment(text):
    text = re.sub("([^\u0E00-\u0E7F\n ]+)", " \\1 ", text)
    return list(_gen_words(text))
