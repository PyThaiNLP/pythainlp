# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2024 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Unigram Part-Of-Speech tagger
"""
import json
import os
from typing import List, Tuple

from pythainlp.corpus import corpus_path, get_corpus_path
from pythainlp.tag import blackboard, orchid

_ORCHID_FILENAME = "pos_orchid_unigram.json"
_ORCHID_PATH = os.path.join(corpus_path(), _ORCHID_FILENAME)

_PUD_FILENAME = "pos_ud_unigram-v0.2.json"
_PUD_PATH = os.path.join(corpus_path(), _PUD_FILENAME)

_BLACKBOARD_NAME = "blackboard_unigram_tagger"

_ORCHID_TAGGER = None
_PUD_TAGGER = None
_BLACKBOARD_TAGGER = None


def _orchid_tagger():
    global _ORCHID_TAGGER
    if not _ORCHID_TAGGER:
        with open(_ORCHID_PATH, encoding="utf-8-sig") as fh:
            _ORCHID_TAGGER = json.load(fh)
    return _ORCHID_TAGGER


def _pud_tagger():
    global _PUD_TAGGER
    if not _PUD_TAGGER:
        with open(_PUD_PATH, encoding="utf-8-sig") as fh:
            _PUD_TAGGER = json.load(fh)
    return _PUD_TAGGER


def _blackboard_tagger():
    global _BLACKBOARD_TAGGER
    if not _BLACKBOARD_TAGGER:
        path = get_corpus_path(_BLACKBOARD_NAME)
        with open(path, encoding="utf-8-sig") as fh:
            _BLACKBOARD_TAGGER = json.load(fh)
    return _BLACKBOARD_TAGGER


def _find_tag(
    words: List[str], dictdata: dict, default_tag: str = ""
) -> List[Tuple[str, str]]:
    keys = list(dictdata.keys())
    return [
        (word, dictdata[word]) if word in keys else (word, default_tag)
        for word in words
    ]


def tag(words: List[str], corpus: str = "pud") -> List[Tuple[str, str]]:
    """
    :param list words: a list of tokenized words
    :param str corpus: corpus name (orchid or pud)
    :return: a list of tuples (word, POS tag)
    :rtype: list[tuple[str, str]]
    """
    if not words:
        return []

    to_ud = False
    if corpus[-3:] == "_ud":
        to_ud = True

    word_tags = []
    if corpus in ("orchid", "orchid_ud"):
        words = orchid.pre_process(words)
        word_tags = _find_tag(words, _orchid_tagger())
        word_tags = orchid.post_process(word_tags, to_ud)
    elif corpus in ("blackboard", "blackboard_ud"):
        words = blackboard.pre_process(words)
        word_tags = _find_tag(words, _blackboard_tagger())
        word_tags = blackboard.post_process(word_tags, to_ud)
    else:  # by default, use "pud" for corpus
        word_tags = _find_tag(words, _pud_tagger())

    return word_tags
