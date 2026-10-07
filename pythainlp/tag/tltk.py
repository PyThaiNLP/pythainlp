# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Thai NLP functions using TLTK."""

from __future__ import annotations

from typing import Union, cast

try:
    from tltk import nlp
except ImportError as e:
    raise ImportError(
        "tltk is not installed. Install it with: pip install tltk"
    ) from e
from pythainlp.tag._utils import _iob_to_markup
from pythainlp.tokenize import word_tokenize

nlp.pos_load()
nlp.ner_load()


def pos_tag(words: list[str], corpus: str = "tnc") -> list[tuple[str, str]]:
    """
    Tag part-of-speech (POS) in a list of words using **TLTK**.

    :param list[str] words: list of words
    :param str corpus: corpus used to train the tagger; only
        ``"tnc"`` is supported
    :return: list of tuples (word, POS tag)
    :rtype: list[tuple[str, str]]
    :raises ValueError: if the corpus is not supported
    """
    if corpus != "tnc":
        raise ValueError(f"tltk not support {corpus!r} corpus.")
    return cast("list[tuple[str, str]]", nlp.pos_tag_wordlist(words))


def _post_process(text: str) -> str:
    return text.replace("<s/>", " ")


def get_ner(
    text: str, pos: bool = True, tag: bool = False
) -> Union[list[tuple[str, str]], list[tuple[str, str, str]], str]:
    """
    Tag named entities in text using **TLTK**.

    This function tags named entities in text in IOB format.

    :param str text: Thai text to be tagged
    :param bool pos: include POS tags in the results (``True``, default)
        or exclude them (``False``)
    :param bool tag: return the text with HTML-like tags
        instead of a list of tuples
    :return: list of tuples of word, POS tag (if ``pos`` is ``True``),
        and named entity tag; or the text with HTML-like tags
        (if ``tag`` is ``True``)
    :rtype: Union[list[tuple[str, str]], list[tuple[str, str, str]], str]
    :Example:

        >>> from pythainlp.tag.tltk import get_ner
        >>> get_ner("เขาเรียนที่โรงเรียนนางรอง")
        [('เขา', 'PRON', 'O'),
        ('เรียน', 'VERB', 'O'),
        ('ที่', 'SCONJ', 'O'),
        ('โรงเรียน', 'NOUN', 'B-L'),
        ('นางรอง', 'VERB', 'I-L')]
        >>> get_ner("เขาเรียนที่โรงเรียนนางรอง", pos=False)
        [('เขา', 'O'),
        ('เรียน', 'O'),
        ('ที่', 'O'),
        ('โรงเรียน', 'B-L'),
        ('นางรอง', 'I-L')]
        >>> get_ner("เขาเรียนที่โรงเรียนนางรอง", tag=True)
        'เขาเรียนที่<L>โรงเรียนนางรอง</L>'
    """
    if not text:
        return []
    list_word = [
        "<s/>" if i == " " else i for i in word_tokenize(text, engine="tltk")
    ]
    _pos = nlp.pos_tag_wordlist(list_word)
    sent_ner = [
        (_post_process(word), pos, ner) for word, pos, ner in nlp.ner(_pos)
    ]
    if tag:
        return _iob_to_markup([(word, ner) for word, _, ner in sent_ner])
    if pos is False:
        return [(word, ner) for word, pos, ner in sent_ner]
    return sent_ner
