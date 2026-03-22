# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import Union, cast

try:
    from tltk import nlp
except ImportError as e:
    raise ImportError(
        "tltk is not installed. Install it with: pip install tltk"
    ) from e
from pythainlp.tokenize import word_tokenize

nlp.pos_load()
nlp.ner_load()


def pos_tag(words: list[str], corpus: str = "tnc") -> list[tuple[str, str]]:
    if corpus != "tnc":
        raise ValueError(f"tltk not support {corpus!r} corpus.")
    return cast(list[tuple[str, str]], nlp.pos_tag_wordlist(words))


def _post_process(text: str) -> str:
    return text.replace("<s/>", " ")


def get_ner(
    text: str, pos: bool = True, tag: bool = False
) -> Union[list[tuple[str, str]], list[tuple[str, str, str]], str]:
    """Named-entity recognizer from **TLTK**

    This function tags named-entities in text in IOB format.

    :param str text: text in Thai to be tagged
    :param bool pos: To include POS tags in the results (`True`) or
        exclude (`False`). The default value is `True`
    :param bool tag: output HTML-like tag.
    :return: a list of tuples associated with tokenized words, NER tags,
        POS tags (if the parameter `pos` is specified as `True`),
        and output HTML-like tags (if the parameter `tag` is
        specified as `True`).
        Otherwise, return a list of tuples associated with tokenized
        words and NER tags
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
    list_word = []
    for i in word_tokenize(text, engine="tltk"):
        if i == " ":
            i = "<s/>"
        list_word.append(i)
    _pos = nlp.pos_tag_wordlist(list_word)
    sent_ner = [
        (_post_process(word), pos, ner) for word, pos, ner in nlp.ner(_pos)
    ]
    if tag:
        temp = ""
        sent = ""
        for idx, (word, pos, ner) in enumerate(sent_ner):
            if ner.startswith("B-") and temp != "":
                sent += "</" + temp + ">"
                temp = ner[2:]
                sent += "<" + temp + ">"
            elif ner.startswith("B-"):
                temp = ner[2:]
                sent += "<" + temp + ">"
            elif ner == "O" and temp != "":
                sent += "</" + temp + ">"
                temp = ""
            sent += word

            if idx == len(sent_ner) - 1 and temp != "":
                sent += "</" + temp + ">"

        return sent
    if pos is False:
        return [(word, ner) for word, pos, ner in sent_ner]
    return sent_ner
