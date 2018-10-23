# -*- coding: utf-8 -*-
"""
Wrapper for WordCut Thai word segmentation
"""
import sys

try:
    from wordcut import Wordcut
except ImportError:
    """
    ในกรณีที่ยังไม่ติดตั้ง wordcutpy ในระบบ
    """
    from pythainlp.tools import install_package

    install_package("wordcutpy")
    try:
        from wordcut import Wordcut
    except ImportError:
        raise ImportError("ImportError: Try 'pip install wordcutpy'")


def segment(text, word_list=None):
    if not word_list:
        wordcut = Wordcut.bigthai()
    else:
        word_list = list(set(word_list))
        wordcut = Wordcut(word_list)
    return wordcut.tokenize(text)
