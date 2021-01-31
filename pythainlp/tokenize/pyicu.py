# -*- coding: utf-8 -*-
"""
Wrapper for PyICU word segmentation. This wrapper module uses
:class:`icu.BreakIterator` with Thai as :class:`icu.Local`
to locate boundaries between words from the text.

:See Also:
    * `GitHub repository <https://github.com/ovalhub/pyicu>`_
"""
import re
from typing import List

from icu import BreakIterator, Locale


def _gen_words(text: str) -> str:
    bd = BreakIterator.createWordInstance(Locale("th"))
    bd.setText(text)
    p = bd.first()
    for q in bd:
        yield text[p:q]
        p = q


def segment(text: str) -> List[str]:
    """
    :param str text: text to be tokenized to words
    :return: list of words, tokenized from the text
    """
    if not text or not isinstance(text, str):
        return []

    text = re.sub("([^\u0E00-\u0E7F\n ]+)", " \\1 ", text)

    return list(_gen_words(text))
